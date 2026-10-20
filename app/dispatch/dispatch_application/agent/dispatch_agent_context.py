from dataclasses import dataclass
from app.dispatch.dispatch_core import ReMiConDispatchQueryService


@dataclass
class DispatchAgentContext:
    """Agent 실행 시 Tool에 주입할 컨텍스트"""

    query_service: ReMiConDispatchQueryService
