from typing import Optional
from uuid6 import UUID

from app.dispatch.dispatch_core import (
    ReMiConDispatchQueryService,
    ReMiConDispatchRepository,
    ReMiConDispatch,
    PlantDispatchAggregation,
)


class ReMiConDispatchQueryServiceImpl(ReMiConDispatchQueryService):

    def __init__(self, dispatch_repository: ReMiConDispatchRepository):
        self._dispatch_repository = dispatch_repository

    async def get_by_id(self, dispatch_id: UUID) -> Optional[ReMiConDispatch]:
        return await self._dispatch_repository.find_by_id(dispatch_id)

    async def get_by_plant_code(self, plant_code: str) -> list[ReMiConDispatch]:
        return await self._dispatch_repository.find_by_plant_code(plant_code)

    async def get_all(self) -> list[ReMiConDispatch]:
        return await self._dispatch_repository.find_all()

    async def get_distinct_plant_codes(self) -> list[str]:
        return await self._dispatch_repository.find_distinct_plant_codes()

    async def aggregate_by_plant_code(
        self, plant_code: Optional[str] = None
    ) -> list[PlantDispatchAggregation]:
        return await self._dispatch_repository.aggregate_by_plant_code(plant_code)
