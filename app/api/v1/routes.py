from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import JSONResponse

from app.models.envelopes import ErrorDetail, ErrorResponse
from app.models.processing import ProcessingResponse
from app.services.processor import (
    OCRProcessor,
    ProcessingError,
)
from app.services.scan import (
    InvalidScanIdError,
    ScanNotFoundError,
    find_scan_file,
)
from app.models.envelopes import SuccessResponse

router = APIRouter()
processor = OCRProcessor()


@router.get("", response_model=SuccessResponse)
def api_version(request: Request) -> SuccessResponse:
    return SuccessResponse(
        request_id=request.state.request_id,
        data={"version": "v1"},
    )


@router.post(
    "/scan/{scan_id}/process",
    response_model=ProcessingResponse,
)
def process_scan(scan_id: str, request: Request) -> ProcessingResponse | JSONResponse:
    try:
        scan_file = find_scan_file(scan_id)
    except InvalidScanIdError as error:
        response = ErrorResponse(
            request_id=request.state.request_id,
            error=ErrorDetail(code="invalid_scan_id", message=str(error)),
        )
        return JSONResponse(status_code=400, content=response.model_dump())
    except ScanNotFoundError as error:
        response = ErrorResponse(
            request_id=request.state.request_id,
            error=ErrorDetail(code="scan_not_found", message=str(error)),
        )
        return JSONResponse(status_code=404, content=response.model_dump())

    try:
        result = processor.process({"scan_id": scan_id, "file_path": str(scan_file)})
    except ProcessingError as error:
        response = ErrorResponse(
            request_id=request.state.request_id,
            error=ErrorDetail(code=error.code, message=str(error)),
        )
        status_code = 503 if error.code == "tesseract_unavailable" else 400
        return JSONResponse(status_code=status_code, content=response.model_dump())
    except Exception:
        response = ErrorResponse(
            request_id=request.state.request_id,
            error=ErrorDetail(
                code="processing_failed",
                message="Scan processing failed unexpectedly",
            ),
        )
        return JSONResponse(status_code=500, content=response.model_dump())

    return ProcessingResponse(
        request_id=request.state.request_id,
        scan_id=scan_id,
        result=result,
    )
