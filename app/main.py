from uuid import uuid4

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.api.router import router
from app.models.envelopes import ErrorDetail, ErrorResponse

app = FastAPI()
app.include_router(router)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


app.add_middleware(RequestIdMiddleware)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", str(uuid4()))
    error = ErrorResponse(
        request_id=request_id,
        error=ErrorDetail(
            code="validation_error",
            message="Request validation failed",
        ),
    )
    return JSONResponse(status_code=422, content=error.model_dump())
