import json

from models.base import Base

INVENTORIES = []

class Inventories(Base):
    def __init__(self, root_path, is_debug=False):
        self.data_path = root_path + "inventory.json"
        self.load(is_debug)

    def get_inventories(self):
        return self.data

    def get_inventory(self, item_id, location_id):
        for x in self.data:
            if x["item_id"] == item_id and x["location_id"] == location_id:
                return x
        return None

    def get_inventories_for_item(self, item_id):
        result = []
        for x in self.data:
            if x["item_id"] == item_id:
                result.append(x)
        return result

    def get_inventory_totals_for_item(self, item_id):
        result = {
            "total_expected": 0,
            "total_ordered": 0,
            "total_allocated": 0,
            "total_available": 0,
        }
        for x in self.data:
            if x["item_id"] == item_id:
                result["total_expected"] += x["quantity_expected"]
                result["total_ordered"] += x["quantity_ordered"]
                result["total_allocated"] += x["quantity_allocated"]
                result["total_available"] += x["quantity_on_hand"] - x["quantity_allocated"]
        return result

    def add_inventory(self, inventory):
        # Composite key: upsert on (item_id, location_id).
        existing = self.get_inventory(inventory["item_id"], inventory["location_id"])
        inventory["created_at"] = self.get_timestamp()
        inventory["updated_at"] = self.get_timestamp()
        if existing is not None:
            existing.update(inventory)
        else:
            self.data.append(inventory)

    def update_inventory(self, item_id, location_id, inventory):
        inventory["updated_at"] = self.get_timestamp()
        for i in range(len(self.data)):
            if (self.data[i]["item_id"] == item_id
                    and self.data[i]["location_id"] == location_id):
                self.data[i] = inventory
                break

    def remove_inventory(self, item_id, location_id):
        self.data = [
            x for x in self.data
            if not (x["item_id"] == item_id and x["location_id"] == location_id)
        ]

    def load(self, is_debug):
        if is_debug:
            self.data = INVENTORIES
        else:
            with open(self.data_path, "r") as f:
                self.data = json.load(f)

    def save(self):
        with open(self.data_path, "w") as f:
            json.dump(self.data, f)