import json
import pytest
from app.dispatch.dispatch_infra.repository.re_mi_con_dispatch_repository_db import (
    ReMiConDispatchRepositoryDB,
)
from app.dispatch.dispatch_infra.uow.re_mi_con_dispatch_uow_impl import (
    ReMiConDispatchUowImpl,
)
from app.dispatch.dispatch_application.service.re_mi_con_dispatch_command_service_impl import (
    ReMiConDispatchCommandServiceImpl,
)
from app.dispatch.dispatch_application.service.re_mi_con_dispatch_query_service_impl import (
    ReMiConDispatchQueryServiceImpl,
)
from app.dispatch.dispatch_application.agent.dispatch_agent_context import (
    DispatchAgentContext,
)
from app.dispatch.dispatch_application.agent.dispatch_tools import (
    register_dispatch,
    find_dispatches_by_plant_code,
)


class DummyContextWrapper:
    def __init__(self, context):
        self.context = context


@pytest.mark.asyncio
async def test_register_dispatch_without_plant_code(async_session):
    repo = ReMiConDispatchRepositoryDB(session=async_session)
    uow = ReMiConDispatchUowImpl(
        session=async_session,
        re_mi_con_dispatch_repository_factory=lambda s: ReMiConDispatchRepositoryDB(s),
    )
    cmd_service = ReMiConDispatchCommandServiceImpl(dispatch_uow=uow)
    query_service = ReMiConDispatchQueryServiceImpl(dispatch_repository=repo)

    ctx_wrapper = DummyContextWrapper(
        context=DispatchAgentContext(
            query_service=query_service,
            command_service=cmd_service,
        )
    )

    fn_register = register_dispatch.on_invoke_tool._get_wrapped_callable()

    # 1. 플랜트 코드 없이 수량만 전달하여 등록 (테스트 목적)
    result_raw = await fn_register(
        ctx=ctx_wrapper,
        quantity=120,
    )
    result_json = json.loads(result_raw)

    assert result_json["status"] == "success"
    dispatch_data = result_json["dispatch"]
    # 플랜트 코드가 없어도 'DEFAULT'로 안전하게 저장됨
    assert dispatch_data["plant_code"] == "DEFAULT"
    assert dispatch_data["quantity"] == 120
    # 송장번호와 출하일자도 자동 생성됨
    assert dispatch_data["invoice_no"].startswith("INV-")
    assert dispatch_data["ship_date"] != ""

    # 2. 실제로 DB에 저장되어 조회가 가능한지 확인
    saved_items = await query_service.get_by_plant_code("DEFAULT")
    assert len(saved_items) == 1
    assert saved_items[0].quantity == 120
    assert saved_items[0].plant_code == "DEFAULT"
