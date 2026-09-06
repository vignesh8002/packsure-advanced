import base64
import uuid
from typing import Dict

import cv2
import numpy as np
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import Response

from image_processing.image_processor import process_image
from image_processing.quality_checker import check_image_quality

router = APIRouter()

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024
_PROCESSED_IMAGE_STORE: Dict[str, bytes] = {}
_STORE_MAX_ITEMS = 50


def _remember_processed_image(image_bytes: bytes) -> str:
    image_id = uuid.uuid4().hex
    _PROCESSED_IMAGE_STORE[image_id] = image_bytes
    if len(_PROCESSED_IMAGE_STORE) > _STORE_MAX_ITEMS:
        oldest_key = next(iter(_PROCESSED_IMAGE_STORE))
        _PROCESSED_IMAGE_STORE.pop(oldest_key, None)
    return image_id


@router.post("/process-image")
async def process_image_endpoint(image: UploadFile = File(...)):
    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Please upload a JPG, PNG, or WEBP image.",
        )

    raw_bytes = await image.read()
    if len(raw_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="Image size must be below 10 MB.")
    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file was empty.")

    original_image = cv2.imdecode(
        np.frombuffer(raw_bytes, np.uint8),
        cv2.IMREAD_COLOR,
    )
    if original_image is None:
        raise HTTPException(
            status_code=400,
            detail="Could not decode image. Please upload a valid JPG, PNG, or WEBP file.",
        )

    try:
        quality_report = check_image_quality(original_image)
        enhanced_image = process_image(original_image)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Image processing failed unexpectedly: {exc}",
        ) from exc

    success, encoded = cv2.imencode(".jpg", enhanced_image)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to encode processed image.")

    processed_bytes = encoded.tobytes()
    image_id = _remember_processed_image(processed_bytes)
    return {
        "quality": quality_report,
        "processed_image_id": image_id,
        "processed_image_url": f"/processed-image/{image_id}",
        "processed_image_base64": base64.b64encode(processed_bytes).decode("utf-8"),
    }


@router.get("/processed-image/{image_id}")
def get_processed_image(image_id: str):
    image_bytes = _PROCESSED_IMAGE_STORE.get(image_id)
    if image_bytes is None:
        raise HTTPException(
            status_code=404,
            detail="Processed image not found (it may have expired, or the id is invalid).",
        )
    return Response(content=image_bytes, media_type="image/jpeg")
