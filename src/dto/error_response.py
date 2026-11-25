from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str = Field(description="What went wrong", examples=["Warehouse with id 5 was not found"])
