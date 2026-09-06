from pydantic import BaseModel


class ScanResponse(BaseModel):
    request_id: str
    scan_id: str
    status: str = "accepted"
    message: str = "Image uploaded successfully"
