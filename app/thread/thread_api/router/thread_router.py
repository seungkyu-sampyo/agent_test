from fastapi import APIRouter, status, Depends

from app.thread.thread_core import ThreadCommandService, Thread
from app.thread.thread_application_container import get_thread_command_service
from ..dto.response.thread_response import ThreadResponse

thread_router = APIRouter(prefix="/threads", tags=["threads"])


@thread_router.post(
    path="",
    summary="Create a new thread",
    description="Create a new thread which represents a unit of grouped messages.",
    response_model=ThreadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_thread_api(
    thread_command_service: ThreadCommandService = Depends(get_thread_command_service),
) -> ThreadResponse:
    """
    신규 상담 대화 스레드를 생성하는 API 엔드포인트.

    Args:
        thread_command_service (ThreadCommandService): 스레드 커맨드 서비스 의존성.

    Returns:
        ThreadResponse: 생성된 스레드의 ID 및 생성 타임스탬프.
    """
    thread: Thread = await thread_command_service.create_thread()
    thread_id = str(thread.id_)

    return ThreadResponse(
        id=thread_id,
        created_at=int(thread.created_at.timestamp()),
    )
