from typing import Any

from pydantic import BaseModel, Field


class RequestEnvelope(BaseModel):
    request_id: str | None = Field(default=None)
    payload: dict[str, Any] = Field(default_factory=dict)


class SuccessResponse(BaseModel):
    request_id: str
    status: str = "success"
    data: dict[str, Any] = Field(default_factory=dict)


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    request_id: str
    status: str = "error"
    error: ErrorDetail
