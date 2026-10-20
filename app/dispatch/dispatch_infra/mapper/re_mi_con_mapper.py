from uuid6 import UUID

from app.dispatch.dispatch_core import ReMiConDispatch
from app.dispatch.dispatch_infra.entity.re_mi_con_dispatch_entity import (
    ReMiConDispatchEntity,
)


def to_domain(re_mi_con_dispatch_entity: ReMiConDispatchEntity) -> ReMiConDispatch:
    """SQLAlchemy Entity (str ID) -> Domain Model (UUID ID) 변환"""
    return ReMiConDispatch(
        id_=(
            UUID(re_mi_con_dispatch_entity.id_)
            if re_mi_con_dispatch_entity.id_
            else None
        ),  # str -> UUID 변환
        invoice_no=re_mi_con_dispatch_entity.invoice_no,
        ship_date=re_mi_con_dispatch_entity.ship_date,
        plant_code=re_mi_con_dispatch_entity.plant_code,
        quantity=re_mi_con_dispatch_entity.quantity,
    )


def to_entity(domain: ReMiConDispatch) -> ReMiConDispatchEntity:
    """Domain Model (UUID ID) -> SQLAlchemy Entity (str ID) 변환"""
    return ReMiConDispatchEntity(
        id_=str(domain.id_),  # UUID -> str 변환
        invoice_no=domain.invoice_no,
        ship_date=domain.ship_date,
        plant_code=domain.plant_code,
        quantity=domain.quantity,
    )
