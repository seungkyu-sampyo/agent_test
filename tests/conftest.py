import pytest_asyncio
from uuid6 import uuid7
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.database import Base
from app.thread.thread_infra.entity.thread_entity import ThreadEntity
from app.dispatch.dispatch_infra.entity.re_mi_con_dispatch_entity import (
    ReMiConDispatchEntity,
)
from app.dispatch.dispatch_infra.entity.dispatch_message_entity import (
    DispatchMessageEntity,
)


@pytest_asyncio.fixture
async def async_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        # 테스트 초기 데이터 세팅 (유효한 UUID 형식 사용)
        d1 = ReMiConDispatchEntity(
            id_=str(uuid7()),
            invoice_no="INV-001",
            ship_date="2026-10-20",
            plant_code="1001",
            quantity=50,
        )
        d2 = ReMiConDispatchEntity(
            id_=str(uuid7()),
            invoice_no="INV-002",
            ship_date="2026-10-20",
            plant_code="1001",
            quantity=30,
        )
        d3 = ReMiConDispatchEntity(
            id_=str(uuid7()),
            invoice_no="INV-003",
            ship_date="2026-10-20",
            plant_code="1002",
            quantity=45,
        )
        session.add_all([d1, d2, d3])
        await session.commit()

        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
