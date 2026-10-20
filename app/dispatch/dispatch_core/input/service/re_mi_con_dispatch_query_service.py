from abc import ABC, abstractmethod
from typing import Optional
from uuid6 import UUID

from ...re_mi_con_dispatch import ReMiConDispatch
from ...plant_aggregation import PlantDispatchAggregation


class ReMiConDispatchQueryService(ABC):

    @abstractmethod
    async def get_by_id(self, dispatch_id: UUID) -> Optional[ReMiConDispatch]: ...

    @abstractmethod
    async def get_by_plant_code(self, plant_code: str) -> list[ReMiConDispatch]: ...

    @abstractmethod
    async def get_all(self) -> list[ReMiConDispatch]: ...

    @abstractmethod
    async def get_distinct_plant_codes(self) -> list[str]: ...

    @abstractmethod
    async def aggregate_by_plant_code(
        self, plant_code: Optional[str] = None
    ) -> list[PlantDispatchAggregation]: ...
