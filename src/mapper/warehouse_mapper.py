from dto.warehouse_response import WarehouseResponse
from entity.warehouse import Warehouse


class WarehouseMapper:

    @staticmethod
    def to_dto(entity: Warehouse) -> WarehouseResponse:
        return WarehouseResponse(
            id=entity.id,
            code=entity.code,
            name=entity.name,
            address=entity.address,
            city=entity.city,
            zip_code=entity.zip_code,
            province=entity.province,
            country=entity.country,
            contact_name=entity.contact_name,
            contact_phone=entity.contact_phone,
            contact_email=entity.contact_email,
        )
