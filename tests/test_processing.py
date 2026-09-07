from io import BytesIO
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_scan() -> str:
    response = client.post(
        "/api/scan",
        files={"file": ("label.png", BytesIO(b"png-data"), "image/png")},
    )
    assert response.status_code == 200
    return response.json()["scan_id"]


def test_processes_existing_scan_with_ocr_processor() -> None:
    scan_id = create_scan()

    with patch(
        "app.api.v1.routes.processor.process",
        return_value={
            "processor": "ocr",
            "quality": {"quality_score": 80},
            "ocr": {
                "full_text": "MRP 120",
                "lines": [],
                "words": [],
                "average_confidence": 0.9,
            },
            "normalized_text": "MRP 120",
            "detected_languages": ["English"],
            "entities": {"mrp": "120 INR"},
        },
    ):
        response = client.post(f"/api/v1/scan/{scan_id}/process")

    assert response.status_code == 200
    assert response.json()["scan_id"] == scan_id
    assert response.json()["result"]["processor"] == "ocr"


def test_missing_scan_returns_scan_not_found() -> None:
    response = client.post("/api/v1/scan/scan_abcdef12/process")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "scan_not_found"


def test_invalid_scan_id_returns_invalid_scan_id() -> None:
    response = client.post("/api/v1/scan/not-a-scan/process")

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_scan_id"


def test_processing_request_id_is_generated_and_propagated() -> None:
    scan_id = create_scan()

    generated_response = client.post(f"/api/v1/scan/{scan_id}/process")
    assert generated_response.headers["X-Request-ID"]

    request_id = "processing-integration-test"
    response = client.post(
        f"/api/v1/scan/{scan_id}/process",
        headers={"X-Request-ID": request_id},
    )

    assert response.headers["X-Request-ID"] == request_id
    assert response.json()["request_id"] == request_id
