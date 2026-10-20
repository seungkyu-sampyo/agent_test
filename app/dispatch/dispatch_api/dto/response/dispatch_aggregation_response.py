from pydantic import BaseModel, Field

from .dispatch_response import DispatchResponse


class DispatchAggregationResponse(BaseModel):
    """플랜트 코드별 출하 취합 응답 DTO"""

    plant_code: str = Field(..., description="플랜트 코드")
    total_quantity: int = Field(..., description="총 출하 수량 합계")
    dispatch_count: int = Field(..., description="총 출하 건수")
    dispatches: list[DispatchResponse] = Field(
        default_factory=list, description="해당 플랜트의 출하 상세 목록"
    )
