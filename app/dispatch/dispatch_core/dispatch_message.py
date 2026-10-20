from datetime import datetime
from uuid6 import UUID, uuid7
from dataclasses import dataclass


@dataclass
class DispatchMessage:
    """레미콘 출하 상담 대화 메시지 도메인 모델"""

    def __init__(
        self,
        id_: UUID | None = None,
        thread_id: UUID | None = None,
        role: str = "user",
        content: str = "",
        created_at: datetime | None = None,
    ):
        self.id_: UUID = id_ or uuid7()
        self.thread_id: UUID = thread_id or uuid7()
        self.role: str = role
        self.content: str = content
        self.created_at: datetime = created_at or datetime.now()
