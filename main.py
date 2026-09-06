"""
main.py
-------
PACKSURE AI - Member 2 (Computer Vision) integration layer.

A small FastAPI service that sits between Member 1 (frontend) and
Member 3 (OCR):

    Member 1  --(upload raw photo)-->  THIS SERVICE  --(enhanced image)-->  Member 3

Endpoints
---------
POST /process-image
    Member 1 uploads a raw product image (multipart/form-data, field
    name "image" - matches the frontend guide's api.js contract).
    Runs the unchanged quality_checker + image_processor pipeline and
    returns:
        - the quality report (JSON)
        - the enhanced image, base64-encoded (so a same-process or
          separate-process Member 3 can decode it immediately)
        - a processed_image_id + processed_image_url, so Member 3 can
          alternatively fetch the raw JPEG bytes over HTTP instead of
          decoding base64.

GET /processed-image/{image_id}
    Returns the raw enhanced image as image/jpeg bytes. Lets Member 3's
    OCR service (PaddleOCR) load the enhanced image directly with e.g.
    `cv2.imdecode` on the response bytes, if it is running as its own
    process/service rather than importing this module directly.

GET /health
    Basic liveness check.

Note: the existing pipeline (image_processing/quality_checker.py and
image_processing/image_processor.py) is untouched - this file only
wires HTTP around it.
"""

import base64
import uuid
from typing import Dict

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from image_processing.quality_checker import check_image_quality
from image_processing.image_processor import process_image

app = FastAPI(
    title="PACKSURE AI - Member 2: Image Processing Service",
    description=(
        "Receives a raw product image from the frontend, runs quality "
        "checks + enhancement, and hands off the processed image for OCR."
    ),
    version="1.0.0",
)

# Allow the frontend (running on a different port during development) to
# call this service directly from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Matches Member 1's guide: "Allow JPG, JPEG, PNG, WEBP" / "Maximum size: 10 MB"
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

# In-memory store so GET /processed-image/{id} can serve the enhanced
# image by id. Fine for a hackathon demo; not persisted across restarts,
# and bounded so a long demo session doesn't grow memory unbounded.
_PROCESSED_IMAGE_STORE: Dict[str, bytes] = {}
_STORE_MAX_ITEMS = 50


def _remember_processed_image(image_bytes: bytes) -> str:
    image_id = uuid.uuid4().hex
    _PROCESSED_IMAGE_STORE[image_id] = image_bytes
    if len(_PROCESSED_IMAGE_STORE) > _STORE_MAX_ITEMS:
        oldest_key = next(iter(_PROCESSED_IMAGE_STORE))
        _PROCESSED_IMAGE_STORE.pop(oldest_key, None)
    return image_id


@app.get("/health")
def health_check():
    """Basic liveness check for the demo / load balancer."""
    return {"status": "ok", "service": "packsure-image-processing"}


@app.post("/process-image")
async def process_image_endpoint(image: UploadFile = File(...)):
    """
    Accepts a raw product image, runs the quality + enhancement
    pipeline, and returns the quality report plus the enhanced image.
    """
    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Please upload a JPG, PNG, or WEBP image.",
        )

    raw_bytes = await image.read()

    if len(raw_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail="Image size must be below 10 MB.",
        )

    if not raw_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file was empty.")

    np_arr = np.frombuffer(raw_bytes, np.uint8)
    original_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if original_image is None:
        raise HTTPException(
            status_code=400,
            detail="Could not decode image. Please upload a valid JPG, PNG, or WEBP file.",
        )

    try:
        quality_report = check_image_quality(original_image)
        enhanced_image = process_image(original_image)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:  # noqa: BLE001 - never let this crash the request
        raise HTTPException(
            status_code=500,
            detail=f"Image processing failed unexpectedly: {exc}",
        )

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


@app.get("/processed-image/{image_id}")
def get_processed_image(image_id: str):
    """Returns the raw enhanced image bytes (image/jpeg) for a given id."""
    image_bytes = _PROCESSED_IMAGE_STORE.get(image_id)
    if image_bytes is None:
        raise HTTPException(
            status_code=404,
            detail="Processed image not found (it may have expired, or the id is invalid).",
        )
    return Response(content=image_bytes, media_type="image/jpeg")
