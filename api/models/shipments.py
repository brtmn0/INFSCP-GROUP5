import json

from models.base import Base
from providers import data_provider

SHIPMENTS = []

class Shipments(Base):
    def __init__(self, root_path, is_debug=False):
        self.data_path = root_path + "shipment.json"
        self.load(is_debug)

    def get_shipments(self):
        result = []
        for x in self.data:
            result.append(self._with_items(x))
        return result

    def get_shipment(self, shipment_id):
        for x in self.data:
            if x["id"] == shipment_id:
                return self._with_items(x)
        return None

    def get_items_in_shipment(self, shipment_id):
        rows = data_provider.fetch_shipment_item_pool().get_items_for_shipment(shipment_id)
        return [{"item_id": r["item_id"], "amount": r["amount"]} for r in rows]

    def get_order_ids_in_shipment(self, shipment_id):
        """In the new schema shipment.order_id -> order.id (1:1), so a shipment
        carries exactly one order id (or none)."""
        for x in self.data:
            if x["id"] == shipment_id:
                order_id = x.get("order_id")
                return [order_id] if order_id is not None else []
        return []

    def add_shipment(self, shipment):
        items = shipment.pop("items", [])
        shipment["created_at"] = self.get_timestamp()
        shipment["updated_at"] = self.get_timestamp()
        self.data.append(shipment)
        data_provider.fetch_shipment_item_pool().set_items_for_shipment(shipment["id"], items)

    def update_shipment(self, shipment_id, shipment):
        items = shipment.pop("items", None)
        shipment["updated_at"] = self.get_timestamp()
        for i in range(len(self.data)):
            if self.data[i]["id"] == shipment_id:
                self.data[i] = shipment
                break
        if items is not None:
            self.update_items_in_shipment(shipment_id, items)

    def update_items_in_shipment(self, shipment_id, items):
        """Replace the items of a shipment and keep `quantity_ordered` in sync."""
        current = self.get_items_in_shipment(shipment_id)
        current_by_item = {x["item_id"]: x["amount"] for x in current}
        new_by_item = {x["item_id"]: x["amount"] for x in items}

        inventory_pool = data_provider.fetch_inventory_pool()
        for item_id, new_amount in new_by_item.items():
            old_amount = current_by_item.get(item_id, 0)
            delta = new_amount - old_amount
            if delta != 0:
                self._apply_ordered_delta(inventory_pool, item_id, delta)
        for item_id, old_amount in current_by_item.items():
            if item_id not in new_by_item:
                self._apply_ordered_delta(inventory_pool, item_id, -old_amount)

        data_provider.fetch_shipment_item_pool().set_items_for_shipment(shipment_id, items)

    @staticmethod
    def _apply_ordered_delta(inventory_pool, item_id, delta):
        inventories = inventory_pool.get_inventories_for_item(item_id)
        if not inventories:
            return
        target = max(inventories, key=lambda z: z["quantity_on_hand"])
        target["quantity_ordered"] = max(0, target["quantity_ordered"] + delta)
        inventory_pool.update_inventory(item_id, target["location_id"], target)

    def update_orders_in_shipment(self, shipment_id, order_ids):
        """In the new schema a shipment references a single order (shipment.order_id).
        We accept a list for backwards compatibility with the v1 endpoint and keep
        the first id, clearing the link when the list is empty."""
        for i in range(len(self.data)):
            if self.data[i]["id"] == shipment_id:
                self.data[i]["order_id"] = order_ids[0] if order_ids else None
                self.data[i]["updated_at"] = self.get_timestamp()
                break

    def remove_shipment(self, shipment_id):
        for x in self.data:
            if x["id"] == shipment_id:
                self.data.remove(x)
                break
        data_provider.fetch_shipment_item_pool().remove_items_for_shipment(shipment_id)

    def _with_items(self, shipment):
        shipment = dict(shipment)
        shipment["items"] = self.get_items_in_shipment(shipment["id"])
        return shipment

    def load(self, is_debug):
        if is_debug:
            self.data = SHIPMENTS
        else:
            with open(self.data_path, "r") as f:
                self.data = json.load(f)

    def save(self):
        with open(self.data_path, "w") as f:
            json.dump(self.data, f)
