from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app
from app.services.scan import MAX_UPLOAD_SIZE, UPLOAD_DIRECTORY

client = TestClient(app)


def test_scan_accepts_png_and_saves_it_temporarily() -> None:
    response = client.post(
        "/api/scan",
        files={"file": ("label.png", BytesIO(b"png-data"), "image/png")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["scan_id"].startswith("scan_")
    assert len(body["scan_id"]) == 13
    assert body["status"] == "accepted"
    assert body["message"] == "Image uploaded successfully"
    assert (UPLOAD_DIRECTORY / f"{body['scan_id']}.png").exists()


def test_scan_rejects_unsupported_file_type() -> None:
    response = client.post(
        "/api/scan",
        files={"file": ("label.gif", BytesIO(b"gif-data"), "image/gif")},
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "unsupported_file_type"


def test_scan_rejects_files_over_10_mb() -> None:
    response = client.post(
        "/api/scan",
        files={
            "file": (
                "large.png",
                BytesIO(b"x" * (MAX_UPLOAD_SIZE + 1)),
                "image/png",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "file_too_large"


def test_scan_propagates_request_id() -> None:
    request_id = "scan-integration-test"

    response = client.post(
        "/api/scan",
        headers={"X-Request-ID": request_id},
        files={"file": ("label.jpg", BytesIO(b"jpeg-data"), "image/jpeg")},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == request_id
    assert response.json()["request_id"] == request_id
