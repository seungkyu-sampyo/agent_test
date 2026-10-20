from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from .dispatch_core import (
    ReMiConDispatchRepository,
    ReMiConDispatchUow,
    DispatchMessageRepository,
    DispatchMessageUow,
)
from .dispatch_infra import (
    ReMiConDispatchRepositoryDB,
    ReMiConDispatchUowImpl,
    DispatchMessageRepositoryDB,
    DispatchMessageUowImpl,
)


def get_re_mi_con_dispatch_repository(
    session: AsyncSession = Depends(get_session),
) -> ReMiConDispatchRepository:
    return ReMiConDispatchRepositoryDB(session=session)


def get_re_mi_con_dispatch_uow(
    session: AsyncSession = Depends(get_session),
) -> ReMiConDispatchUow:
    return ReMiConDispatchUowImpl(
        session=session,
        re_mi_con_dispatch_repository_factory=get_re_mi_con_dispatch_repository,
    )


def get_dispatch_message_repository(
    session: AsyncSession = Depends(get_session),
) -> DispatchMessageRepository:
    return DispatchMessageRepositoryDB(session=session)


def get_dispatch_message_uow(
    session: AsyncSession = Depends(get_session),
) -> DispatchMessageUow:
    return DispatchMessageUowImpl(
        session=session,
        dispatch_message_repository_factory=get_dispatch_message_repository,
    )
