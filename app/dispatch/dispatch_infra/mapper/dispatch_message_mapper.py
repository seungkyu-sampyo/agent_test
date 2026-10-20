from uuid6 import UUID

from app.dispatch.dispatch_core import DispatchMessage
from ..entity.dispatch_message_entity import DispatchMessageEntity


def to_domain(entity: DispatchMessageEntity) -> DispatchMessage:
    """SQLAlchemy Entity (str ID) -> Domain Model (UUID ID) 변환"""
    return DispatchMessage(
        id_=UUID(entity.id_) if entity.id_ else None,
        thread_id=UUID(entity.thread_id) if entity.thread_id else None,
        role=entity.role,
        content=entity.content,
        created_at=entity.created_at,
    )


def to_entity(domain: DispatchMessage) -> DispatchMessageEntity:
    """Domain Model (UUID ID) -> SQLAlchemy Entity (str ID) 변환"""
    return DispatchMessageEntity(
        id_=str(domain.id_),
        thread_id=str(domain.thread_id),
        role=domain.role,
        content=domain.content,
        created_at=domain.created_at,
    )
