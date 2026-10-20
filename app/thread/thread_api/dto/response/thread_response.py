from pydantic import BaseModel, Field


class ThreadResponse(BaseModel):
    id: str = Field(
        ...,
        description="unit of grouped messages",
    )

    created_at: int = Field(
        ...,
        description="creation timestamp",
    )
