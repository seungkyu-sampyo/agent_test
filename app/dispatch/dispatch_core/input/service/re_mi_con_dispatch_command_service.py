from abc import ABC, abstractmethod
from typing import Optional
from uuid6 import UUID

from ...re_mi_con_dispatch import ReMiConDispatch


class ReMiConDispatchCommandService(ABC):

    @abstractmethod
    async def create_dispatch(
        self,
        quantity: int,
        invoice_no: Optional[str] = None,
        ship_date: Optional[str] = None,
        plant_code: Optional[str] = None,
        id_: Optional[UUID] = None,
    ) -> ReMiConDispatch: ...
