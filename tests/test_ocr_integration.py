from io import BytesIO
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.services.processor import InvalidImageError, OCRProcessingError


client = TestClient(app)


def _upload_valid_image() -> str:
    response = client.post(
        "/api/scan",
        files={"file": ("label.png", BytesIO(b"png-data"), "image/png")},
    )
    assert response.status_code == 200
    return response.json()["scan_id"]


def test_scan_processing_returns_structured_ocr_result() -> None:
    scan_id = _upload_valid_image()
    result = {
        "processor": "ocr",
        "quality": {"quality_score": 82},
        "ocr": {"full_text": "MRP 120", "average_confidence": 0.91},
        "normalized_text": "MRP 120",
        "detected_languages": ["English"],
        "entities": {"mrp": "120 INR"},
    }

    with patch("app.api.v1.routes.processor.process", return_value=result):
        response = client.post(f"/api/v1/scan/{scan_id}/process")

    assert response.status_code == 200
    assert response.json()["result"] == result


def test_scan_processing_rejects_invalid_image() -> None:
    scan_id = _upload_valid_image()

    with patch(
        "app.api.v1.routes.processor.process",
        side_effect=InvalidImageError(),
    ):
        response = client.post(f"/api/v1/scan/{scan_id}/process")

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_image"


def test_scan_processing_returns_ocr_failure() -> None:
    scan_id = _upload_valid_image()

    with patch(
        "app.api.v1.routes.processor.process",
        side_effect=OCRProcessingError("OCR processing failed"),
    ):
        response = client.post(f"/api/v1/scan/{scan_id}/process")

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "ocr_processing_failed"


def test_scan_processing_returns_ocr_failure_without_internal_details() -> None:
    scan_id = _upload_valid_image()

    with patch(
        "app.api.v1.routes.processor.process",
        side_effect=RuntimeError("secret internal detail"),
    ):
        response = client.post(f"/api/v1/scan/{scan_id}/process")

    assert response.status_code == 500
    assert response.json()["error"]["code"] == "processing_failed"
    assert "secret internal detail" not in response.text
