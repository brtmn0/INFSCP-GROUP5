from typing import List, Annotated

from fastapi import APIRouter, Path, Body

from dto.error_response import ErrorResponse
from dto.warehouse_request import WarehouseRequest
from dto.warehouse_response import WarehouseResponse
from entity.warehouse import Warehouse
from mapper.warehouse_mapper import WarehouseMapper
from routes.abstract_route import AbstractRoute
from service.interface.warehouse_service_interface import WarehouseServiceInterface

class WarehouseRoutes(AbstractRoute):

    def __init__(self, warehouse_service: WarehouseServiceInterface):
        self.__warehouse_service = warehouse_service

        self.__router = APIRouter(prefix="/warehouses", tags=["warehouses"])

    def map_routes(self) -> APIRouter:
        self.__router.add_api_route(
            path="/",
            endpoint=self.__get_all_warehouses,
            methods=["GET"],
            summary="Get all warehouses.",
            response_description="A list of all warehouses.",
        )

        self.__router.add_api_route(
            path="/{warehouse_id}",
            endpoint=self.__get_warehouse_by_id,
            methods=["GET"],
            summary="Get a warehouse by id.",
            response_description="A single warehouse requested.",
            responses={404: {"model": ErrorResponse, "description": "Warehouse not found."}},
        )

        self.__router.add_api_route("/{warehouse_id}/locations", self.get_warehouse_locations, methods=["GET"])

        self.__router.add_api_route(
            path="/",
            endpoint=self.create_warehouse,
            methods=["POST"],
            status_code=201,
            summary="Create a new warehouse.",
            response_description="The new created warehouse.",
        )

        self.__router.add_api_route(
            path="/{warehouse_id}",
            endpoint=self.update_warehouse,
            methods=["PUT"],
            summary="Update a warehouse.",
            response_description="The updated warehouse.",
            responses={404: {"model": ErrorResponse, "description": "Warehouse not found."}},
        )

        self.__router.add_api_route(
            path="/{warehouse_id}",
            endpoint=self.delete_warehouse,
            methods=["DELETE"],
            status_code=204,
            summary="Delete a warehouse.",
            response_description="The warehouse was deleted.",
            responses={404: {"model": ErrorResponse, "description": "Warehouse not found."}},
        )

        return self.__router

    def __get_all_warehouses(self) -> List[WarehouseResponse]:
        """
            Returns all the warehouses.
        """
        warehouses: List[Warehouse] =  self.__warehouse_service.get_all_warehouses()
        if len(warehouses) == 0:
            return []

        return [WarehouseMapper.to_dto(wh) for wh in warehouses]

    def __get_warehouse_by_id(self, warehouse_id: Annotated[int, Path(description="Id of the warehouse", ge=1)]) -> WarehouseResponse:
        """
            Returns a single warehouse.

            Responds with **404** when no warehouse has the given id.
        """
        warehouse = self.__warehouse_service.get_warehouse_by_id(warehouse_id)

        return WarehouseMapper.to_dto(warehouse)

    def get_warehouse_locations(self):
        pass

    def create_warehouse(self, warehouse: Annotated[WarehouseRequest, Body(description="The requested new warehouse object", embed=True)]) -> WarehouseResponse:
        """
            Creates a new warehouse.
        """
        new_warehouse = self.__warehouse_service.create_warehouse(warehouse)

        return WarehouseMapper.to_dto(new_warehouse)

    def update_warehouse(
        self,
        warehouse_id: Annotated[int, Path(description="Id of the warehouse", ge=1)],
        warehouse: Annotated[WarehouseRequest, Body(description="The new values of the warehouse", embed=True)],
    ) -> WarehouseResponse:
        """
            Updates an existing warehouse.

            Responds with **404** when no warehouse has the given id.
        """
        updated_warehouse = self.__warehouse_service.update_warehouse(warehouse_id, warehouse)

        return WarehouseMapper.to_dto(updated_warehouse)

    def delete_warehouse(self, warehouse_id: Annotated[int, Path(description="Id of the warehouse", ge=1)]) -> None:
        """
            Deletes a warehouse.

            Responds with **404** when no warehouse has the given id.
        """
        self.__warehouse_service.delete_warehouse(warehouse_id)
