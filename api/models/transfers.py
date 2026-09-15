import json

from models.base import Base
from providers import data_provider

TRANSFERS = []

class Transfers(Base):
    def __init__(self, root_path, is_debug=False):
        self.data_path = root_path + "transfer.json"
        self.load(is_debug)

    def get_transfers(self):
        result = []
        for x in self.data:
            result.append(self._with_items(x))
        return result

    def get_transfer(self, transfer_id):
        for x in self.data:
            if x["id"] == transfer_id:
                return self._with_items(x)
        return None

    def get_items_in_transfer(self, transfer_id):
        rows = data_provider.fetch_transfer_item_pool().get_items_for_transfer(transfer_id)
        return [{"item_id": r["item_id"], "amount": r["amount"]} for r in rows]

    def add_transfer(self, transfer):
        items = transfer.pop("items", [])
        transfer["transfer_status"] = "Scheduled"
        transfer["created_at"] = self.get_timestamp()
        transfer["updated_at"] = self.get_timestamp()
        self.data.append(transfer)
        data_provider.fetch_transfer_item_pool().set_items_for_transfer(transfer["id"], items)

    def update_transfer(self, transfer_id, transfer):
        items = transfer.pop("items", None)
        transfer["updated_at"] = self.get_timestamp()
        for i in range(len(self.data)):
            if self.data[i]["id"] == transfer_id:
                self.data[i] = transfer
                break
        if items is not None:
            data_provider.fetch_transfer_item_pool().set_items_for_transfer(transfer_id, items)

    def remove_transfer(self, transfer_id):
        for x in self.data:
            if x["id"] == transfer_id:
                self.data.remove(x)
                break
        data_provider.fetch_transfer_item_pool().remove_items_for_transfer(transfer_id)

    def _with_items(self, transfer):
        transfer = dict(transfer)
        transfer["items"] = self.get_items_in_transfer(transfer["id"])
        return transfer

    def load(self, is_debug):
        if is_debug:
            self.data = TRANSFERS
        else:
            with open(self.data_path, "r") as f:
                self.data = json.load(f)

    def save(self):
        with open(self.data_path, "w") as f:
            json.dump(self.data, f)
