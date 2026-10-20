from uuid6 import UUID
from app.thread.thread_core import Thread
from app.thread.thread_infra.entity.thread_entity import ThreadEntity


def to_domain(thread_entity: ThreadEntity) -> Thread:
    return Thread(
        id_=UUID(thread_entity.id_) if thread_entity.id_ else None,
        created_at=thread_entity.created_at,
        deleted_at=thread_entity.deleted_at,
    )


def to_entity(thread: Thread) -> ThreadEntity:
    return ThreadEntity(
        id_=str(thread.id_),
        created_at=thread.created_at,
        deleted_at=thread.deleted_at,
    )
