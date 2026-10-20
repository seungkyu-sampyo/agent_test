import json
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock

from app.database import get_session
from app.main import app
from app.dispatch.dispatch_infra.repository.re_mi_con_dispatch_repository_db import (
    ReMiConDispatchRepositoryDB,
)
from app.dispatch.dispatch_application.service.re_mi_con_dispatch_query_service_impl import (
    ReMiConDispatchQueryServiceImpl,
)
from app.dispatch.dispatch_application.agent.dispatch_agent_context import (
    DispatchAgentContext,
)
from app.dispatch.dispatch_application.agent.dispatch_tools import (
    list_distinct_plants,
    find_dispatches_by_plant_code,
    aggregate_dispatches_by_plant_code,
    find_all_dispatches,
)
from app.dispatch.dispatch_application_container import get_dispatch_agent_service
from app.dispatch.dispatch_core import DispatchChatResult


class DummyContextWrapper:
    def __init__(self, context):
        self.context = context


@pytest.mark.asyncio
async def test_repository_and_query_service(async_session):
    repo = ReMiConDispatchRepositoryDB(session=async_session)
    service = ReMiConDispatchQueryServiceImpl(dispatch_repository=repo)

    # 1. 플랜트 코드 목록 조회
    plants = await service.get_distinct_plant_codes()
    assert set(plants) == {"1001", "1002"}

    # 2. 특정 플랜트 상세 조회
    dispatches_1001 = await service.get_by_plant_code("1001")
    assert len(dispatches_1001) == 2
    assert {d.invoice_no for d in dispatches_1001} == {"INV-001", "INV-002"}

    # 3. 플랜트별 취합 (전체)
    all_aggregations = await service.aggregate_by_plant_code()
    assert len(all_aggregations) == 2
    agg_map = {agg.plant_code: agg for agg in all_aggregations}
    assert agg_map["1001"].total_quantity == 80  # 50 + 30
    assert agg_map["1001"].dispatch_count == 2
    assert agg_map["1002"].total_quantity == 45
    assert agg_map["1002"].dispatch_count == 1

    # 4. 특정 플랜트 취합
    agg_1001 = await service.aggregate_by_plant_code("1001")
    assert len(agg_1001) == 1
    assert agg_1001[0].plant_code == "1001"
    assert agg_1001[0].total_quantity == 80


@pytest.mark.asyncio
async def test_agent_tools(async_session):
    repo = ReMiConDispatchRepositoryDB(session=async_session)
    service = ReMiConDispatchQueryServiceImpl(dispatch_repository=repo)
    ctx_wrapper = DummyContextWrapper(
        context=DispatchAgentContext(query_service=service)
    )

    # list_distinct_plants tool
    fn_list_plants = list_distinct_plants.on_invoke_tool._get_wrapped_callable()
    plants_raw = await fn_list_plants(ctx_wrapper)
    plants_data = json.loads(plants_raw)
    assert set(plants_data["plant_codes"]) == {"1001", "1002"}

    # aggregate_dispatches_by_plant_code tool (전체 취합)
    fn_aggregate = (
        aggregate_dispatches_by_plant_code.on_invoke_tool._get_wrapped_callable()
    )
    agg_raw = await fn_aggregate(ctx_wrapper, plant_code=None)
    agg_data = json.loads(agg_raw)
    assert len(agg_data["aggregations"]) == 2

    # aggregate_dispatches_by_plant_code tool (특정 플랜트 1001 취합)
    agg_1001_raw = await fn_aggregate(ctx_wrapper, plant_code="1001")
    agg_1001_data = json.loads(agg_1001_raw)
    assert len(agg_1001_data["aggregations"]) == 1
    assert agg_1001_data["aggregations"][0]["plant_code"] == "1001"
    assert agg_1001_data["aggregations"][0]["total_quantity"] == 80
    assert agg_1001_data["aggregations"][0]["dispatch_count"] == 2

    # find_dispatches_by_plant_code tool
    fn_find = find_dispatches_by_plant_code.on_invoke_tool._get_wrapped_callable()
    disp_raw = await fn_find(ctx_wrapper, plant_code="1002")
    disp_data = json.loads(disp_raw)
    assert disp_data["plant_code"] == "1002"
    assert disp_data["count"] == 1
    assert disp_data["dispatches"][0]["quantity"] == 45

    # find_all_dispatches tool
    fn_all = find_all_dispatches.on_invoke_tool._get_wrapped_callable()
    all_raw = await fn_all(ctx_wrapper)
    all_data = json.loads(all_raw)
    assert all_data["total_count"] == 3


@pytest.mark.asyncio
async def test_api_endpoints(async_session):
    async def override_get_session():
        yield async_session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. 플랜트 목록 조회 API
        res_plants = await client.get("/dispatch/plants")
        assert res_plants.status_code == 200
        assert set(res_plants.json()) == {"1001", "1002"}

        # 2. 전체 플랜트 취합 API
        res_agg = await client.get("/dispatch/plants/aggregate")
        assert res_agg.status_code == 200
        agg_json = res_agg.json()
        assert len(agg_json) == 2
        plant_1001 = next(item for item in agg_json if item["plant_code"] == "1001")
        assert plant_1001["total_quantity"] == 80
        assert plant_1001["dispatch_count"] == 2

        # 3. 특정 플랜트 상세 조회 API
        res_detail = await client.get("/dispatch/plants/1001")
        assert res_detail.status_code == 200
        assert len(res_detail.json()) == 2

        # 4. Agent 대화 API (AgentService 모킹)
        mock_agent_service = AsyncMock()
        mock_agent_service.chat.return_value = DispatchChatResult(
            reply="1001 공장의 총 출하량은 80입니다.", thread_id="test-thread-1"
        )
        app.dependency_overrides[get_dispatch_agent_service] = (
            lambda: mock_agent_service
        )

        chat_payload = {
            "message": "1001 공장 출하 내역 취합해줘",
            "thread_id": "test-thread-1",
        }
        res_chat = await client.post("/dispatch/chat", json=chat_payload)
        assert res_chat.status_code == 200
        chat_json = res_chat.json()
        assert "80" in chat_json["reply"]
        assert chat_json["thread_id"] == "test-thread-1"

    app.dependency_overrides.clear()
