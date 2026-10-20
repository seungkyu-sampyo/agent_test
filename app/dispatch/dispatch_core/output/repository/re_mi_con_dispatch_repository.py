from uuid6 import UUID
from abc import ABC, abstractmethod
from typing import Optional

from ...re_mi_con_dispatch import ReMiConDispatch


class ReMiConDispatchRepository(ABC):

    @abstractmethod
    async def find_by_id(
        self, re_mi_con_dispatch_id: UUID
    ) -> Optional[ReMiConDispatch]: ...

    @abstractmethod
    async def save(self, re_mi_con_dispatch: ReMiConDispatch) -> ReMiConDispatch: ...
