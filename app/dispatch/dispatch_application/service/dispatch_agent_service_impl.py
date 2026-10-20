import logging
from typing import Optional
from uuid6 import UUID

from agents import Runner

from app.thread.thread_core import ThreadCommandService, Thread
from app.dispatch.dispatch_core import (
    DispatchAgentService,
    DispatchChatResult,
    ReMiConDispatchQueryService,
    ReMiConDispatchCommandService,
    DispatchMessageCommandService,
    DispatchMessageQueryService,
)
from ..agent.dispatch_agent import create_dispatch_agent
from ..agent.dispatch_agent_context import DispatchAgentContext

logger = logging.getLogger(__name__)


class DispatchAgentServiceImpl(DispatchAgentService):
    """
    Thread ID 및 DispatchMessage 기반 레미콘 출하 상담 에이전트 서비스.
    인메모리 세션이 아닌 데이터베이스 Thread 및 DispatchMessage에 대화 이력을 영속화하여 관리합니다.
    """

    def __init__(
        self,
        query_service: ReMiConDispatchQueryService,
        message_command_service: DispatchMessageCommandService,
        message_query_service: DispatchMessageQueryService,
        thread_command_service: ThreadCommandService,
        dispatch_command_service: Optional[ReMiConDispatchCommandService] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self._query_service = query_service
        self._message_command_service = message_command_service
        self._message_query_service = message_query_service
        self._thread_command_service = thread_command_service
        self._dispatch_command_service = dispatch_command_service
        self._agent = create_dispatch_agent(
            model=model,
            api_key=api_key,
            base_url=base_url,
        )

    async def chat(
        self, message: str, thread_id: Optional[str] = None
    ) -> DispatchChatResult:
        # 1. thread_id가 없으면 DB에 신규 Thread 생성
        if not thread_id:
            new_thread: Thread = await self._thread_command_service.create_thread()
            thread_uuid = new_thread.id_
        else:
            thread_uuid = UUID(thread_id)

        # 2. DB에서 이전 대화 메시지 목록 조회
        past_messages = await self._message_query_service.get_messages_by_thread_id(
            thread_id=thread_uuid
        )

        # 3. 사용자 질문 메시지를 DB에 영속화 (role='user')
        await self._message_command_service.create_message(
            thread_id=thread_uuid,
            role="user",
            content=message,
        )

        # 4. OpenAI Agent SDK 입력 형식(대화 히스토리 목록) 구성
        conversation_input = [
            {"role": msg.role, "content": msg.content}
            for msg in past_messages
            if msg.role in ("user", "assistant")
        ]
        conversation_input.append({"role": "user", "content": message})

        # 5. Agent 실행 컨텍스트 주입 (조회 서비스 + 등록 커맨드 서비스)
        context = DispatchAgentContext(
            query_service=self._query_service,
            command_service=self._dispatch_command_service,
        )

        try:
            result = await Runner.run(
                self._agent,
                input=conversation_input,
                context=context,
            )
            reply = (
                str(result.final_output)
                if result.final_output is not None
                else "응답을 생성할 수 없습니다."
            )

            # 6. 에이전트 답변 메시지를 DB에 영속화 (role='assistant')
            await self._message_command_service.create_message(
                thread_id=thread_uuid,
                role="assistant",
                content=reply,
            )

            return DispatchChatResult(reply=reply, thread_id=str(thread_uuid))

        except Exception as e:
            logger.error(
                f"Error during agent chat run for thread {thread_uuid}: {e}",
                exc_info=True,
            )
            raise e
