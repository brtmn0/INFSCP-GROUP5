from abc import ABC, abstractmethod
from typing import List

from entity.warehouse import Warehouse
from repository.interface.base_repository_interface import BaseRepositoryInterface


class WarehouseRepositoryInterface(BaseRepositoryInterface[Warehouse], ABC):
    pass