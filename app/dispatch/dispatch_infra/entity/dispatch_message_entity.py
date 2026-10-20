from datetime import datetime

from sqlalchemy import DateTime, String, Column, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DispatchMessageEntity(Base):
    __tablename__ = "dispatch_messages"

    id_ = Column(String(36), name="id", primary_key=True)
    thread_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
