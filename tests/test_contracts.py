from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient

from app.main import RequestIdMiddleware, app, validation_exception_handler
from app.models.envelopes import ErrorResponse, RequestEnvelope, SuccessResponse


client = TestClient(app)


def test_versioned_router_is_registered() -> None:
    paths = set(app.openapi()["paths"])

    assert "/api/v1" in paths


def test_request_id_is_generated_and_returned() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["X-Request-ID"]


def test_request_id_is_propagated() -> None:
    request_id = "integration-test-request"

    response = client.get("/health", headers={"X-Request-ID": request_id})

    assert response.headers["X-Request-ID"] == request_id


def test_generic_envelopes_validate() -> None:
    request = RequestEnvelope(payload={"future": "data"})
    success = SuccessResponse(request_id="request-1", data={"result": "value"})
    error = ErrorResponse(
        request_id="request-1",
        error={"code": "validation_error", "message": "Request validation failed"},
    )

    assert request.payload == {"future": "data"}
    assert success.status == "success"
    assert error.status == "error"


def test_validation_error_uses_standard_envelope() -> None:
    validation_app = FastAPI()
    validation_app.add_middleware(RequestIdMiddleware)
    validation_app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )

    @validation_app.post("/validate")
    def validate(request: RequestEnvelope, _: Request) -> SuccessResponse:
        return SuccessResponse(request_id="request-1", data=request.payload)

    validation_client = TestClient(validation_app)
    response = validation_client.post("/validate", json={"payload": "not-an-object"})

    assert response.status_code == 422
    assert response.json()["status"] == "error"
    assert response.json()["error"]["code"] == "validation_error"
    assert response.headers["X-Request-ID"]
