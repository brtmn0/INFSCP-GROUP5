from exceptions.not_found_error import NotFoundError


class WarehouseNotFoundError(NotFoundError):
    def __init__(self, warehouse_id: int):
        super().__init__("Warehouse", warehouse_id)
