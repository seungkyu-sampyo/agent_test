from typing import Optional
from pydantic import BaseModel, Field


class DispatchChatRequest(BaseModel):
    """레미콘 출하 상담 에이전트 대화 요청 DTO"""

    message: str = Field(
        ...,
        description="사용자 질문 또는 지시사항 (예: '1001 공장 출하 내역 취합해줘')",
        examples=["1001 공장 오늘 출하 수량 취합해줘", "플랜트별 전체 출하량 알려줘"],
    )
    thread_id: Optional[str] = Field(
        None,
        description="대화 맥락 유지를 위한 스레드 ID (생략 시 새로 생성됨)",
    )
