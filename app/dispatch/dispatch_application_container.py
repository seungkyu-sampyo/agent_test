from fastapi import Depends

from app.thread.thread_core import ThreadCommandService
from app.thread.thread_application_container import get_thread_command_service
from .dispatch_core import (
    ReMiConDispatchQueryService,
    ReMiConDispatchCommandService,
    DispatchAgentService,
    ReMiConDispatchRepository,
    ReMiConDispatchUow,
    DispatchMessageRepository,
    DispatchMessageUow,
    DispatchMessageCommandService,
    DispatchMessageQueryService,
)
from .dispatch_application import (
    ReMiConDispatchQueryServiceImpl,
    ReMiConDispatchCommandServiceImpl,
    DispatchMessageCommandServiceImpl,
    DispatchMessageQueryServiceImpl,
    DispatchAgentServiceImpl,
)
from .dispatch_infra_container import (
    get_re_mi_con_dispatch_repository,
    get_re_mi_con_dispatch_uow,
    get_dispatch_message_repository,
    get_dispatch_message_uow,
)


def get_re_mi_con_dispatch_query_service(
    dispatch_repository: ReMiConDispatchRepository = Depends(
        get_re_mi_con_dispatch_repository
    ),
) -> ReMiConDispatchQueryService:
    return ReMiConDispatchQueryServiceImpl(dispatch_repository=dispatch_repository)


def get_re_mi_con_dispatch_command_service(
    dispatch_uow: ReMiConDispatchUow = Depends(get_re_mi_con_dispatch_uow),
) -> ReMiConDispatchCommandService:
    return ReMiConDispatchCommandServiceImpl(dispatch_uow=dispatch_uow)


def get_dispatch_message_command_service(
    message_uow: DispatchMessageUow = Depends(get_dispatch_message_uow),
) -> DispatchMessageCommandService:
    return DispatchMessageCommandServiceImpl(message_uow=message_uow)


def get_dispatch_message_query_service(
    message_repository: DispatchMessageRepository = Depends(
        get_dispatch_message_repository
    ),
) -> DispatchMessageQueryService:
    return DispatchMessageQueryServiceImpl(message_repository=message_repository)


def get_dispatch_agent_service(
    query_service: ReMiConDispatchQueryService = Depends(
        get_re_mi_con_dispatch_query_service
    ),
    message_command_service: DispatchMessageCommandService = Depends(
        get_dispatch_message_command_service
    ),
    message_query_service: DispatchMessageQueryService = Depends(
        get_dispatch_message_query_service
    ),
    thread_command_service: ThreadCommandService = Depends(
        get_thread_command_service
    ),
    dispatch_command_service: ReMiConDispatchCommandService = Depends(
        get_re_mi_con_dispatch_command_service
    ),
) -> DispatchAgentService:
    return DispatchAgentServiceImpl(
        query_service=query_service,
        message_command_service=message_command_service,
        message_query_service=message_query_service,
        thread_command_service=thread_command_service,
        dispatch_command_service=dispatch_command_service,
    )
