from uuid6 import UUID
from abc import ABC, abstractmethod
from typing import Optional

from ...re_mi_con_dispatch import ReMiConDispatch
from ...plant_aggregation import PlantDispatchAggregation


class ReMiConDispatchRepository(ABC):

    @abstractmethod
    async def find_by_id(
        self, re_mi_con_dispatch_id: UUID
    ) -> Optional[ReMiConDispatch]: ...

    @abstractmethod
    async def find_by_plant_code(self, plant_code: str) -> list[ReMiConDispatch]: ...

    @abstractmethod
    async def find_all(self) -> list[ReMiConDispatch]: ...

    @abstractmethod
    async def find_distinct_plant_codes(self) -> list[str]: ...

    @abstractmethod
    async def aggregate_by_plant_code(
        self, plant_code: Optional[str] = None
    ) -> list[PlantDispatchAggregation]: ...

    @abstractmethod
    async def save(self, re_mi_con_dispatch: ReMiConDispatch) -> ReMiConDispatch: ...
