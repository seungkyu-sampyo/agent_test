from pydantic import BaseModel, Field


class DispatchMessageResponse(BaseModel):
    """레미콘 출하 상담 대화 메시지 응답 DTO"""

    id: str = Field(..., description="메시지 ID")
    thread_id: str = Field(..., description="스레드 ID")
    role: str = Field(..., description="역할 (user, assistant 등)")
    content: str = Field(..., description="메시지 내용")
    created_at: int = Field(..., description="생성 일시 (UNIX 타임스탬프)")
