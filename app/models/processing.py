from typing import Any

from pydantic import BaseModel, Field


class ProcessingResponse(BaseModel):
    request_id: str
    scan_id: str
    status: str = "completed"
    result: dict[str, Any] = Field(default_factory=dict)
