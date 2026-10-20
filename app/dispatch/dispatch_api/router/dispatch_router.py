from fastapi import APIRouter, status, Depends
from uuid6 import UUID

from app.dispatch.dispatch_core import (
    DispatchAgentService,
    ReMiConDispatchQueryService,
    DispatchMessageQueryService,
    DispatchChatResult,
    PlantDispatchAggregation,
    ReMiConDispatch,
    DispatchMessage,
)
from app.dispatch.dispatch_application_container import (
    get_dispatch_agent_service,
    get_re_mi_con_dispatch_query_service,
    get_dispatch_message_query_service,
)
from ..dto.request.dispatch_chat_request import DispatchChatRequest
from ..dto.response.dispatch_chat_response import DispatchChatResponse
from ..dto.response.dispatch_response import DispatchResponse
from ..dto.response.dispatch_aggregation_response import DispatchAggregationResponse
from ..dto.response.dispatch_message_response import DispatchMessageResponse

dispatch_router = APIRouter(prefix="/dispatch", tags=["dispatch"])


def _map_dispatch(dispatch: ReMiConDispatch) -> DispatchResponse:
    return DispatchResponse(
        id=str(dispatch.id_),
        invoice_no=dispatch.invoice_no,
        ship_date=dispatch.ship_date,
        plant_code=dispatch.plant_code,
        quantity=dispatch.quantity,
    )


def _map_aggregation(
    aggregation: PlantDispatchAggregation,
) -> DispatchAggregationResponse:
    return DispatchAggregationResponse(
        plant_code=aggregation.plant_code,
        total_quantity=aggregation.total_quantity,
        dispatch_count=aggregation.dispatch_count,
        dispatches=[_map_dispatch(d) for d in aggregation.dispatches],
    )


def _map_message(message: DispatchMessage) -> DispatchMessageResponse:
    return DispatchMessageResponse(
        id=str(message.id_),
        thread_id=str(message.thread_id),
        role=message.role,
        content=message.content,
        created_at=int(message.created_at.timestamp()),
    )


@dispatch_router.post(
    path="/chat",
    summary="Chat with Dispatch Agent",
    description="OpenAI Agent SDK 기반 에이전트와 대화합니다. thread_id를 바탕으로 DB 대화 이력을 연계하며, 신규 및 이전 메시지를 DispatchMessage로 영속화합니다.",
    response_model=DispatchChatResponse,
    status_code=status.HTTP_200_OK,
)
async def chat_with_dispatch_agent(
    request: DispatchChatRequest,
    agent_service: DispatchAgentService = Depends(get_dispatch_agent_service),
) -> DispatchChatResponse:
    result: DispatchChatResult = await agent_service.chat(
        message=request.message,
        thread_id=request.thread_id,
    )
    return DispatchChatResponse(
        reply=result.reply,
        thread_id=result.thread_id or "",
    )


@dispatch_router.get(
    path="/threads/{thread_id}/messages",
    summary="Get conversation messages for a thread",
    description="특정 스레드의 모든 대화 메시지 이력을 시간순으로 조회합니다.",
    response_model=list[DispatchMessageResponse],
    status_code=status.HTTP_200_OK,
)
async def get_thread_messages(
    thread_id: str,
    message_query_service: DispatchMessageQueryService = Depends(
        get_dispatch_message_query_service
    ),
) -> list[DispatchMessageResponse]:
    messages = await message_query_service.get_messages_by_thread_id(
        thread_id=UUID(thread_id)
    )
    return [_map_message(m) for m in messages]


@dispatch_router.get(
    path="/plants/aggregate",
    summary="Aggregate dispatches by plant code",
    description="모든 플랜트 코드별 출하량 및 출하 건수를 취합하여 반환합니다.",
    response_model=list[DispatchAggregationResponse],
    status_code=status.HTTP_200_OK,
)
async def aggregate_all_plants(
    query_service: ReMiConDispatchQueryService = Depends(
        get_re_mi_con_dispatch_query_service
    ),
) -> list[DispatchAggregationResponse]:
    aggregations = await query_service.aggregate_by_plant_code(plant_code=None)
    return [_map_aggregation(a) for a in aggregations]


@dispatch_router.get(
    path="/plants/{plant_code}/aggregate",
    summary="Aggregate dispatches for a specific plant",
    description="특정 플랜트 코드의 출하량 및 출하 건수를 취합하여 반환합니다.",
    response_model=DispatchAggregationResponse | None,
    status_code=status.HTTP_200_OK,
)
async def aggregate_by_plant(
    plant_code: str,
    query_service: ReMiConDispatchQueryService = Depends(
        get_re_mi_con_dispatch_query_service
    ),
) -> DispatchAggregationResponse | None:
    aggregations = await query_service.aggregate_by_plant_code(plant_code=plant_code)
    if not aggregations:
        return DispatchAggregationResponse(
            plant_code=plant_code,
            total_quantity=0,
            dispatch_count=0,
            dispatches=[],
        )
    return _map_aggregation(aggregations[0])


@dispatch_router.get(
    path="/plants/{plant_code}",
    summary="Get dispatches by plant code",
    description="특정 플랜트 코드의 전체 출하 상세 목록을 반환합니다.",
    response_model=list[DispatchResponse],
    status_code=status.HTTP_200_OK,
)
async def get_dispatches_by_plant(
    plant_code: str,
    query_service: ReMiConDispatchQueryService = Depends(
        get_re_mi_con_dispatch_query_service
    ),
) -> list[DispatchResponse]:
    dispatches = await query_service.get_by_plant_code(plant_code=plant_code)
    return [_map_dispatch(d) for d in dispatches]


@dispatch_router.get(
    path="/plants",
    summary="List all distinct plant codes",
    description="등록되어 있는 모든 플랜트 코드 목록을 반환합니다.",
    response_model=list[str],
    status_code=status.HTTP_200_OK,
)
async def list_plants(
    query_service: ReMiConDispatchQueryService = Depends(
        get_re_mi_con_dispatch_query_service
    ),
) -> list[str]:
    return await query_service.get_distinct_plant_codes()
