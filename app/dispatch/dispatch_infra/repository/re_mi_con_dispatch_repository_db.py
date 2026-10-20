from typing import Optional
from sqlalchemy import select, ScalarResult

from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import UUID

from app.dispatch.dispatch_core import ReMiConDispatchRepository, ReMiConDispatch
from ..entity.re_mi_con_dispatch_entity import ReMiConDispatchEntity
from ..mapper import re_mi_con_mapper


class ReMiConDispatchRepositoryDB(ReMiConDispatchRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(
        self, re_mi_con_dispatch_id: UUID
    ) -> Optional[ReMiConDispatch]:

        stmt = select(ReMiConDispatchEntity).where(
            ReMiConDispatchEntity.id_ == re_mi_con_dispatch_id
        )

        result = await self._session.execute(stmt)

        re_mi_con_dispatch_entity: ReMiConDispatchEntity | None = (
            result.scalar_one_or_none()
        )

        if re_mi_con_dispatch_entity is None:
            return None

        return re_mi_con_mapper.to_domain(
            re_mi_con_dispatch_entity=re_mi_con_dispatch_entity
        )

    async def find_by_plant_code(self, plant_code: str) -> list[ReMiConDispatch]:
        stmt = select(ReMiConDispatchEntity).where(
            ReMiConDispatchEntity.plant_code == plant_code
        )

        result = await self._session.execute(stmt)

        re_mi_con_dispatch_entities: ScalarResult[ReMiConDispatchEntity] = (
            result.scalars()
        )

        return [
            re_mi_con_mapper.to_domain(re_mi_con_dispatch_entity)
            for re_mi_con_dispatch_entity in re_mi_con_dispatch_entities
        ]

    async def save(self, re_mi_con_dispatch: ReMiConDispatch) -> ReMiConDispatch:

        re_mi_con_dispatch_entity = re_mi_con_mapper.to_entity(re_mi_con_dispatch)

        self._session.add(re_mi_con_dispatch_entity)

        return re_mi_con_dispatch
