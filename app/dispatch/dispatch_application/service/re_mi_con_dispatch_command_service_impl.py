from datetime import datetime
from typing import Optional
from uuid6 import UUID, uuid7

from app.dispatch.dispatch_core import (
    ReMiConDispatchCommandService,
    ReMiConDispatch,
    ReMiConDispatchUow,
)


class ReMiConDispatchCommandServiceImpl(ReMiConDispatchCommandService):

    def __init__(self, dispatch_uow: ReMiConDispatchUow):
        self._dispatch_uow = dispatch_uow

    async def create_dispatch(
        self,
        quantity: int,
        invoice_no: Optional[str] = None,
        ship_date: Optional[str] = None,
        plant_code: Optional[str] = None,
        id_: Optional[UUID] = None,
    ) -> ReMiConDispatch:
        # 플랜트 코드가 없으면 기본값 'DEFAULT' 지정
        effective_plant_code = (plant_code or "").strip() or "DEFAULT"

        # 송장번호가 없으면 고유 송장번호 자동 생성
        effective_invoice_no = (
            (invoice_no or "").strip() or f"INV-{uuid7().hex[:8].upper()}"
        )

        # 출하일자가 없으면 현재 일자(YYYY-MM-DD)로 지정
        effective_ship_date = (
            (ship_date or "").strip() or datetime.now().strftime("%Y-%m-%d")
        )

        dispatch = ReMiConDispatch(
            id_=id_ or uuid7(),
            invoice_no=effective_invoice_no,
            ship_date=effective_ship_date,
            plant_code=effective_plant_code,
            quantity=quantity,
        )

        async with self._dispatch_uow as uow:
            await uow.re_mi_con_dispatch_repository.save(re_mi_con_dispatch=dispatch)

        return dispatch
