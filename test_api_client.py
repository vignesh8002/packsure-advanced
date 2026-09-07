"""
test_api_client.py
-------------------
End-to-end test client for the FastAPI service (main.py).

This does NOT import the pipeline directly - it makes real HTTP
requests, exactly like Member 1's frontend (or Member 3's OCR
service) would. Use it after starting the API with:

    uvicorn main:app --reload

Usage:
    python test_api_client.py
    python test_api_client.py http://localhost:8000
    python test_api_client.py http://localhost:8000 path/to/your_photo.jpg
"""

import sys
import os
import glob

import requests

DEFAULT_BASE_URL = "http://localhost:8000"

DEFAULT_TEST_IMAGES = [
    "test_images/clear/clear_sample.jpg",
    "test_images/blurry/blurry_sample.jpg",
    "test_images/dark/dark_sample.jpg",
    "test_images/rotated/rotated_sample.jpg",
]


def _content_type_for(path):
    ext = os.path.splitext(path)[1].lower()
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }.get(ext, "application/octet-stream")


def test_health(base_url):
    response = requests.get(f"{base_url}/health", timeout=10)
    response.raise_for_status()
    print(f"[health] {response.status_code} -> {response.json()}")


def test_process_image(base_url, image_path):
    if not os.path.exists(image_path):
        print(f"  Skipping (file not found): {image_path}")
        return

    filename = os.path.basename(image_path)
    with open(image_path, "rb") as f:
        files = {"image": (filename, f, _content_type_for(image_path))}
        response = requests.post(f"{base_url}/process-image", files=files, timeout=60)

    print(f"\n[process-image] {image_path} -> HTTP {response.status_code}")

    if response.status_code != 200:
        print(f"  Error response: {response.text}")
        return

    payload = response.json()
    print(f"  quality: {payload['quality']}")
    print(f"  processed_image_id: {payload['processed_image_id']}")

    # Fetch the enhanced image back via the retrieval endpoint (this is
    # how Member 3's OCR service could pull it if running separately).
    fetch_url = f"{base_url}{payload['processed_image_url']}"
    fetch_response = requests.get(fetch_url, timeout=30)
    fetch_response.raise_for_status()

    root, ext = os.path.splitext(image_path)
    out_path = f"{root}_api_processed.jpg"
    with open(out_path, "wb") as out_file:
        out_file.write(fetch_response.content)

    print(f"  Saved API-processed image to: {out_path}")
    print(f"  ({len(fetch_response.content)} bytes fetched from {fetch_url})")


def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BASE_URL
    image_paths = sys.argv[2:] if len(sys.argv) > 2 else DEFAULT_TEST_IMAGES

    print(f"Testing PACKSURE AI image-processing API at: {base_url}\n")

    try:
        test_health(base_url)
    except requests.exceptions.ConnectionError:
        print(
            f"Could not connect to {base_url}. "
            "Make sure the API is running: uvicorn main:app --reload"
        )
        sys.exit(1)

    for path in image_paths:
        test_process_image(base_url, path)

    print("\nDone.")


if __name__ == "__main__":
    main()
