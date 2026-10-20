from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ReMiConDispatchEntity(Base):
    __tablename__ = "re_mi_con_dispatch"

    id_ = Column(String(36), name="id", primary_key=True)
    invoice_no: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    ship_date: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    plant_code: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
