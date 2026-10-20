from datetime import datetime

from sqlalchemy import DateTime, String, Column
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ThreadEntity(Base):
    __tablename__ = "threads"

    id_ = Column(String(36), name="id", primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
