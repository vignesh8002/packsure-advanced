import re
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

UPLOAD_DIRECTORY = Path(__file__).resolve().parents[2] / "uploads"
MAX_UPLOAD_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
CHUNK_SIZE = 1024 * 1024
SCAN_ID_PATTERN = re.compile(r"^scan_[0-9a-f]{8}$")


class ScanUploadError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


class ScanNotFoundError(Exception):
    pass


class InvalidScanIdError(Exception):
    pass


async def save_scan_upload(file: UploadFile) -> str:
    extension = Path(file.filename or "").suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ScanUploadError(
            "unsupported_file_type",
            "Only JPG, JPEG, and PNG files are supported",
        )

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise ScanUploadError(
            "unsupported_file_type",
            "Only JPG, JPEG, and PNG files are supported",
        )

    scan_id = f"scan_{uuid4().hex[:8]}"
    destination = UPLOAD_DIRECTORY / f"{scan_id}{extension}"
    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

    total_size = 0
    try:
        with destination.open("wb") as output:
            while chunk := await file.read(CHUNK_SIZE):
                total_size += len(chunk)
                if total_size > MAX_UPLOAD_SIZE:
                    raise ScanUploadError(
                        "file_too_large",
                        "Image size must not exceed 10 MB",
                    )
                output.write(chunk)
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    finally:
        await file.close()

    return scan_id


def find_scan_file(scan_id: str) -> Path:
    if not SCAN_ID_PATTERN.fullmatch(scan_id):
        raise InvalidScanIdError("Scan ID must match scan_<8 hex characters>")

    for extension in ALLOWED_EXTENSIONS:
        scan_file = UPLOAD_DIRECTORY / f"{scan_id}{extension}"
        if scan_file.is_file():
            return scan_file

    raise ScanNotFoundError(f"No upload found for scan ID: {scan_id}")
