from dataclasses import dataclass
from typing import Optional
from app.dispatch.dispatch_core import (
    ReMiConDispatchQueryService,
    ReMiConDispatchCommandService,
)


@dataclass
class DispatchAgentContext:
    """Agent 실행 시 Tool에 주입할 컨텍스트"""

    query_service: ReMiConDispatchQueryService
    command_service: Optional[ReMiConDispatchCommandService] = None
