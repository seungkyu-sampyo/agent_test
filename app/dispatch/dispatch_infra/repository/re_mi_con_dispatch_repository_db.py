from typing import Optional
from sqlalchemy import select, func, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import UUID

from app.dispatch.dispatch_core import (
    ReMiConDispatchRepository,
    ReMiConDispatch,
    PlantDispatchAggregation,
)
from ..entity.re_mi_con_dispatch_entity import ReMiConDispatchEntity
from ..mapper import re_mi_con_mapper


class ReMiConDispatchRepositoryDB(ReMiConDispatchRepository):

    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(
        self, re_mi_con_dispatch_id: UUID
    ) -> Optional[ReMiConDispatch]:
        stmt = select(ReMiConDispatchEntity).where(
            ReMiConDispatchEntity.id_ == str(re_mi_con_dispatch_id)
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

    async def find_all(self) -> list[ReMiConDispatch]:
        stmt = select(ReMiConDispatchEntity)
        result = await self._session.execute(stmt)
        entities = result.scalars().all()
        return [re_mi_con_mapper.to_domain(entity) for entity in entities]

    async def find_distinct_plant_codes(self) -> list[str]:
        stmt = select(ReMiConDispatchEntity.plant_code).distinct()
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def aggregate_by_plant_code(
        self, plant_code: Optional[str] = None
    ) -> list[PlantDispatchAggregation]:
        # 1. 집계 쿼리 실행 (플랜트별 총 수량, 총 건수)
        stmt = select(
            ReMiConDispatchEntity.plant_code,
            func.sum(ReMiConDispatchEntity.quantity).label("total_quantity"),
            func.count(ReMiConDispatchEntity.id_).label("dispatch_count"),
        )
        if plant_code:
            stmt = stmt.where(ReMiConDispatchEntity.plant_code == plant_code)

        stmt = stmt.group_by(ReMiConDispatchEntity.plant_code)
        result = await self._session.execute(stmt)
        rows = result.all()

        if not rows:
            return []

        # 2. 각 플랜트별 상세 출하 내역 조회
        aggregations: list[PlantDispatchAggregation] = []
        for row in rows:
            p_code = row[0]
            total_qty = int(row[1] or 0)
            count = int(row[2] or 0)

            detail_stmt = select(ReMiConDispatchEntity).where(
                ReMiConDispatchEntity.plant_code == p_code
            )
            detail_result = await self._session.execute(detail_stmt)
            detail_entities = detail_result.scalars().all()
            dispatches = [
                re_mi_con_mapper.to_domain(entity) for entity in detail_entities
            ]

            aggregations.append(
                PlantDispatchAggregation(
                    plant_code=p_code,
                    total_quantity=total_qty,
                    dispatch_count=count,
                    dispatches=dispatches,
                )
            )

        return aggregations

    async def save(self, re_mi_con_dispatch: ReMiConDispatch) -> ReMiConDispatch:
        re_mi_con_dispatch_entity = re_mi_con_mapper.to_entity(re_mi_con_dispatch)
        self._session.add(re_mi_con_dispatch_entity)
        return re_mi_con_dispatch
