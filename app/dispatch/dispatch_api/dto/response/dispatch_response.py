from pydantic import BaseModel, Field


class DispatchResponse(BaseModel):
    """레미콘 출하 상세 응답 DTO"""

    id: str = Field(..., description="출하 ID")
    invoice_no: str = Field(..., description="송장 번호")
    ship_date: str = Field(..., description="출하 일자")
    plant_code: str = Field(..., description="플랜트 코드")
    quantity: int = Field(..., description="수량")
