from datetime import datetime

from uuid6 import UUID, uuid7
from dataclasses import dataclass


@dataclass
class Thread:

    def __init__(
        self,
        id_: UUID | None = None,
        created_at: datetime | None = None,
        deleted_at: datetime | None = None,
    ):
        self.id_: UUID = id_ or uuid7()
        self.created_at = created_at or datetime.now()
        self.deleted_at = deleted_at or datetime.now()
