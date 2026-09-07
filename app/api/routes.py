from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import JSONResponse

from app.models.envelopes import ErrorDetail, ErrorResponse
from app.models.scan import ScanResponse
from app.services.scan import ScanUploadError, save_scan_upload

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/api/scan", response_model=ScanResponse)
async def create_scan(
    request: Request,
    file: UploadFile = File(...),
) -> ScanResponse | JSONResponse:
    try:
        scan_id = await save_scan_upload(file)
    except ScanUploadError as error:
        response = ErrorResponse(
            request_id=request.state.request_id,
            error=ErrorDetail(code=error.code, message=error.message),
        )
        return JSONResponse(status_code=400, content=response.model_dump())

    return ScanResponse(
        request_id=request.state.request_id,
        scan_id=scan_id,
    )
