import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine

from exceptions.exception_handlers import register_exception_handlers
from repository.interface.warehouse_repository_interface import WarehouseRepositoryInterface
from repository.warehouse_repository import WarehouseRepository
from routes.abstract_route import AbstractRoute
from routes.warehouse_routes import WarehouseRoutes
from service.interface.warehouse_service_interface import WarehouseServiceInterface
from service.warehouse_service import WarehouseService

CONNECTION_STRING = "postgresql+psycopg://pguser:example@localhost:5432/database"

engine = create_engine(CONNECTION_STRING)

warehouse_repository: WarehouseRepositoryInterface = WarehouseRepository(engine)

warehouse_service: WarehouseServiceInterface = WarehouseService(warehouse_repository)

# routes
routes: list[AbstractRoute] = [
    WarehouseRoutes(warehouse_service),
]

app = FastAPI()
register_exception_handlers(app)

for route in routes:
    app.include_router(route.map_routes())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
