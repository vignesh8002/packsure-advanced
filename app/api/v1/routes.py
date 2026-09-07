from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import JSONResponse

from app.models.envelopes import ErrorDetail, ErrorResponse
from app.models.processing import ProcessingResponse
from app.services.processor import MockProcessor
from app.services.scan import (
    InvalidScanIdError,
    ScanNotFoundError,
    find_scan_file,
)
from app.models.envelopes import SuccessResponse

router = APIRouter()
processor = MockProcessor()


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

    result = processor.process({"scan_id": scan_id, "file_path": str(scan_file)})
    return ProcessingResponse(
        request_id=request.state.request_id,
        scan_id=scan_id,
        result=result,
    )
