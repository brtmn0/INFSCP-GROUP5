import json

from models.base import Base

class OrderItems(Base):
    def __init__(self, root_path, is_debug=False):
        self.data_path = root_path + "order_item.json"
        self.load(is_debug)

    def get_items_for_order(self, order_id):
        result = []
        for x in self.data:
            if x["order_id"] == order_id:
                result.append(x)
        return result

    def set_items_for_order(self, order_id, items):
        self.remove_items_for_order(order_id)
        next_id = self._next_id()
        for item in items:
            next_id += 1
            row = {
                "id": next_id,
                "order_id": order_id,
                "item_id": item["item_id"],
                "amount": item["amount"],
            }
            if "unit_price" in item:
                row["unit_price"] = item["unit_price"]
            self.data.append(row)

    def remove_items_for_order(self, order_id):
        self.data = [x for x in self.data if x["order_id"] != order_id]

    def _next_id(self):
        return max((x["id"] for x in self.data), default=0)

    def load(self, is_debug):
        if is_debug:
            self.data = []
        else:
            with open(self.data_path, "r") as f:
                self.data = json.load(f)

    def save(self):
        with open(self.data_path, "w") as f:
            json.dump(self.data, f)