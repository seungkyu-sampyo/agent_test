"""
스레드 SQLAlchemy ORM 엔티티 모듈.

`threads` 테이블과 매핑되는 데이터베이스 모델을 정의합니다.
"""

import uuid
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, UUID

from app.database import Base


class ThreadEntity(Base):
    __tablename__ = "threads"

    id_: Mapped[uuid.UUID] = mapped_column("id", UUID(as_uuid=True), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
