import json

from models.base import Base

class TransferItems(Base):
    """Rows of the `transfer_item` table (id, transfer_id, item_id, amount)."""

    def __init__(self, root_path, is_debug=False):
        self.data_path = root_path + "transfer_item.json"
        self.load(is_debug)

    def get_items_for_transfer(self, transfer_id):
        result = []
        for x in self.data:
            if x["transfer_id"] == transfer_id:
                result.append(x)
        return result

    def set_items_for_transfer(self, transfer_id, items):
        """Replace every item row belonging to `transfer_id` with `items`
        (a list of {item_id, amount} dicts). New surrogate ids are assigned."""
        self.remove_items_for_transfer(transfer_id)
        next_id = self._next_id()
        for item in items:
            next_id += 1
            self.data.append({
                "id": next_id,
                "transfer_id": transfer_id,
                "item_id": item["item_id"],
                "amount": item["amount"],
            })

    def remove_items_for_transfer(self, transfer_id):
        self.data = [x for x in self.data if x["transfer_id"] != transfer_id]

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
