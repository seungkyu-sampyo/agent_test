import pytest
from uuid6 import uuid7, UUID
from unittest.mock import AsyncMock, patch

from app.dispatch.dispatch_core import DispatchMessage
from app.dispatch.dispatch_infra.repository.dispatch_message_repository_db import (
    DispatchMessageRepositoryDB,
)
from app.dispatch.dispatch_infra.uow.dispatch_message_uow_impl import (
    DispatchMessageUowImpl,
)
from app.dispatch.dispatch_application.service.dispatch_message_command_service_impl import (
    DispatchMessageCommandServiceImpl,
)
from app.dispatch.dispatch_application.service.dispatch_message_query_service_impl import (
    DispatchMessageQueryServiceImpl,
)
from app.dispatch.dispatch_application.service.dispatch_agent_service_impl import (
    DispatchAgentServiceImpl,
)
from app.thread.thread_core import Thread
from app.thread.thread_infra.repository.thread_repository_db import ThreadRepositoryDB
from app.thread.thread_infra.uow.thread_uow_impl import ThreadUowImpl
from app.thread.thread_application.service.thread_command_service_impl import (
    ThreadCommandServiceImpl,
)
from app.dispatch.dispatch_infra.repository.re_mi_con_dispatch_repository_db import (
    ReMiConDispatchRepositoryDB,
)
from app.dispatch.dispatch_application.service.re_mi_con_dispatch_query_service_impl import (
    ReMiConDispatchQueryServiceImpl,
)


@pytest.mark.asyncio
async def test_dispatch_message_repository_and_services(async_session):
    # 1. Thread 생성
    thread_repo = ThreadRepositoryDB(session=async_session)
    thread_uow = ThreadUowImpl(
        session=async_session,
        thread_repository_factory=lambda sess: ThreadRepositoryDB(sess),
    )
    thread_cmd_service = ThreadCommandServiceImpl(thread_uow=thread_uow)
    thread: Thread = await thread_cmd_service.create_thread()

    # 2. DispatchMessage 저장 및 조회
    msg_repo = DispatchMessageRepositoryDB(session=async_session)
    msg_uow = DispatchMessageUowImpl(
        session=async_session,
        dispatch_message_repository_factory=lambda sess: DispatchMessageRepositoryDB(
            sess
        ),
    )
    msg_cmd_service = DispatchMessageCommandServiceImpl(message_uow=msg_uow)
    msg_query_service = DispatchMessageQueryServiceImpl(message_repository=msg_repo)

    # user 메시지 생성
    msg1 = await msg_cmd_service.create_message(
        thread_id=thread.id_,
        role="user",
        content="1001 공장 출하 내역 취합해줘",
    )
    assert msg1.thread_id == thread.id_
    assert msg1.role == "user"
    assert msg1.content == "1001 공장 출하 내역 취합해줘"

    # assistant 메시지 생성
    msg2 = await msg_cmd_service.create_message(
        thread_id=thread.id_,
        role="assistant",
        content="1001 공장의 총 출하량은 80입니다.",
    )
    assert msg2.role == "assistant"

    # thread_id로 메시지 이력 조회
    messages = await msg_query_service.get_messages_by_thread_id(thread_id=thread.id_)
    assert len(messages) == 2
    assert messages[0].content == "1001 공장 출하 내역 취합해줘"
    assert messages[1].content == "1001 공장의 총 출하량은 80입니다."


@pytest.mark.asyncio
async def test_dispatch_agent_service_with_thread_persistence(async_session):
    # Thread 서비스 설정
    thread_uow = ThreadUowImpl(
        session=async_session,
        thread_repository_factory=lambda sess: ThreadRepositoryDB(sess),
    )
    thread_cmd_service = ThreadCommandServiceImpl(thread_uow=thread_uow)

    # Dispatch 및 Message 서비스 설정
    dispatch_repo = ReMiConDispatchRepositoryDB(session=async_session)
    dispatch_query_service = ReMiConDispatchQueryServiceImpl(
        dispatch_repository=dispatch_repo
    )

    msg_repo = DispatchMessageRepositoryDB(session=async_session)
    msg_uow = DispatchMessageUowImpl(
        session=async_session,
        dispatch_message_repository_factory=lambda sess: DispatchMessageRepositoryDB(
            sess
        ),
    )
    msg_cmd_service = DispatchMessageCommandServiceImpl(message_uow=msg_uow)
    msg_query_service = DispatchMessageQueryServiceImpl(message_repository=msg_repo)

    agent_service = DispatchAgentServiceImpl(
        query_service=dispatch_query_service,
        message_command_service=msg_cmd_service,
        message_query_service=msg_query_service,
        thread_command_service=thread_cmd_service,
    )

    # Runner.run 모킹하여 OpenAI API 호출 대체
    class MockResult:
        final_output = "1001 공장 총 출하량은 80입니다."

    with patch("agents.Runner.run", new_callable=AsyncMock) as mock_runner:
        mock_runner.return_value = MockResult()

        # 1. thread_id 없이 첫 대화 요청 -> 새 Thread 생성 및 메시지 2건(user, assistant) DB 저장 확인
        result1 = await agent_service.chat(message="1001 공장 출하량 알려줘")
        assert result1.thread_id is not None
        assert result1.reply == "1001 공장 총 출하량은 80입니다."

        created_thread_id = UUID(result1.thread_id)

        # DB에 저장된 메시지 확인
        msgs_after_turn1 = await msg_query_service.get_messages_by_thread_id(
            created_thread_id
        )
        assert len(msgs_after_turn1) == 2
        assert msgs_after_turn1[0].role == "user"
        assert msgs_after_turn1[0].content == "1001 공장 출하량 알려줘"
        assert msgs_after_turn1[1].role == "assistant"
        assert msgs_after_turn1[1].content == "1001 공장 총 출하량은 80입니다."

        # 2. 동일한 thread_id로 2번째 턴 대화 요청 -> 이전 대화 내역이 Runner.run의 input에 포함되는지 확인
        mock_runner.return_value.final_output = (
            "1001 공장의 어제 출하량도 동일합니다."
        )
        result2 = await agent_service.chat(
            message="어제는 어땠어?",
            thread_id=result1.thread_id,
        )
        assert result2.thread_id == result1.thread_id

        # Runner.run에 전달된 input 검증: 과거 2건 + 현재 1건 = 총 3건
        call_args = mock_runner.call_args
        passed_input = call_args[1].get("input") or call_args[0][1]
        assert len(passed_input) == 3
        assert passed_input[0]["role"] == "user"
        assert passed_input[0]["content"] == "1001 공장 출하량 알려줘"
        assert passed_input[1]["role"] == "assistant"
        assert passed_input[1]["content"] == "1001 공장 총 출하량은 80입니다."
        assert passed_input[2]["role"] == "user"
        assert passed_input[2]["content"] == "어제는 어땠어?"

        # DB에 누적된 메시지 확인: 총 4건
        msgs_after_turn2 = await msg_query_service.get_messages_by_thread_id(
            created_thread_id
        )
        assert len(msgs_after_turn2) == 4
        assert msgs_after_turn2[2].role == "user"
        assert msgs_after_turn2[2].content == "어제는 어땠어?"
        assert msgs_after_turn2[3].role == "assistant"
        assert (
            msgs_after_turn2[3].content == "1001 공장의 어제 출하량도 동일합니다."
        )
