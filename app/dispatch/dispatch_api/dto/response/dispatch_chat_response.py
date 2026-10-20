from pydantic import BaseModel, Field


class DispatchChatResponse(BaseModel):
    """레미콘 출하 상담 에이전트 대화 응답 DTO"""

    reply: str = Field(..., description="에이전트 답변 내용")
    thread_id: str = Field(..., description="스레드 ID")
