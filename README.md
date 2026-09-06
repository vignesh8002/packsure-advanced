# PACKSURE AI — Member 2: Computer Vision / Image Processing + API

This is the complete Member 2 deliverable: a preprocessing pipeline that
takes a raw product-label photo (from Member 1's camera/upload flow),
runs quality checks + enhancement, and now also a small FastAPI wrapper
so Member 1's frontend and Member 3's OCR service can plug in over HTTP.

## What's here

```
backend/
├── main.py                    # FastAPI wrapper (the new integration layer)
├── image_processing/
│   ├── __init__.py            # exposes check_image_quality() and process_image()
│   ├── quality_checker.py     # blur / brightness / resolution / quality score
│   └── image_processor.py     # resize, denoise, CLAHE, deskew, perspective (bonus)
├── test_images/
│   ├── blurry/  dark/  rotated/  clear/
├── test_pipeline.py            # run the pipeline directly (no HTTP) on one image
├── test_api_client.py          # run the pipeline over HTTP against a running server
├── make_sample_test_images.py  # generates synthetic test images if you don't have real photos yet
└── requirements.txt
```

The core pipeline (`quality_checker.py`, `image_processor.py`) is modular and
is wired to the API without changing the OCR integration contract.

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn main:app --reload
```

- Server runs at `http://localhost:8000`
- Interactive docs (Swagger UI) at `http://localhost:8000/docs` — you can
  upload a test image straight from the browser, no frontend needed.

## How to run it in VS Code

1. Open the `backend/` folder in VS Code (`File → Open Folder…`).
2. Open a terminal inside VS Code (`` Ctrl+` ``  /  `` Cmd+` ``).
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```
4. Select that interpreter for the workspace: `Ctrl+Shift+P` →
   **"Python: Select Interpreter"** → choose the one inside `venv/`.
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Start the API (either works):
   - In the same terminal: `uvicorn main:app --reload`
   - Or press `F5` with a `launch.json` configured to run
     `uvicorn` as a module (Run and Debug → "create a launch.json file" →
     choose "Python" → "Module" → enter `uvicorn` as the module and
     `main:app --reload` as args) if you want breakpoints/debugging.
7. Visit `http://localhost:8000/docs` to confirm it's running, or in a
   **second** VS Code terminal (keep the server running in the first one):
   ```bash
   python make_sample_test_images.py   # only needed once
   python test_api_client.py
   ```
   This uploads each sample image to the running server and saves the
   API's enhanced output next to each original as `..._api_processed.jpg`.

## API reference

### `POST /process-image`

Upload a raw product image (multipart/form-data, field name **`image`** —
matches Member 1's `api.js` contract). Accepts JPG, JPEG, PNG, WEBP, up
to 10 MB.

Request (what Member 1's frontend already sends):
```javascript
const formData = new FormData();
formData.append("image", imageFile);

const response = await axios.post(
  "http://localhost:8000/process-image",
  formData,
  { headers: { "Content-Type": "multipart/form-data" } }
);
```

Response `200 OK`:
```json
{
  "quality": {
    "quality_score": 82.0,
    "quality_rating": "EXCELLENT",
    "low_confidence": false,
    "blur_score": 145.2,
    "blur": "LOW",
    "brightness_score": 130.4,
    "brightness": "GOOD",
    "width": 1920,
    "height": 1080,
    "resolution": "GOOD"
  },
  "processed_image_id": "3f9a1c2b7e8d4a6f9b0c1d2e3f4a5b6c",
  "processed_image_url": "/processed-image/3f9a1c2b7e8d4a6f9b0c1d2e3f4a5b6c",
  "processed_image_base64": "<base64-encoded JPEG bytes>"
}
```

Error responses:
| Status | When |
|---|---|
| `400` | Wrong content type, empty file, or the file can't be decoded as an image |
| `413` | File is larger than 10 MB |
| `500` | Unexpected failure inside the CV pipeline |

### `GET /processed-image/{image_id}`

Returns the raw enhanced image as `image/jpeg` bytes. Use this if
Member 3's OCR service runs as its **own process** and would rather
fetch the file over HTTP than decode base64.

```python
import requests, cv2, numpy as np

resp = requests.get(f"http://localhost:8000{processed_image_url}")
np_arr = np.frombuffer(resp.content, np.uint8)
enhanced_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
```

### `GET /health`

Basic liveness check: `{"status": "ok", "service": "packsure-image-processing"}`

## How Member 3 should consume this

**Option A — same process (fastest, recommended if OCR runs in the same backend):**
```python
import cv2
from image_processing.quality_checker import check_image_quality
from image_processing.image_processor import process_image

image = cv2.imread("product.jpg")
quality = check_image_quality(image)
processed_image = process_image(image)   # OpenCV array, straight into PaddleOCR
```

**Option B — separate service, over HTTP (use if OCR runs as its own process):**
```python
import requests, base64, cv2, numpy as np

with open("product.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/process-image",
        files={"image": ("product.jpg", f, "image/jpeg")},
    )
payload = response.json()
quality = payload["quality"]

# Either decode the inline base64...
image_bytes = base64.b64decode(payload["processed_image_base64"])
# ...or fetch it separately:
# image_bytes = requests.get(f"http://localhost:8000{payload['processed_image_url']}").content

np_arr = np.frombuffer(image_bytes, np.uint8)
processed_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
```

## Testing performed

- `test_image_processing.py` — automated tests for clear, blurry, dark, bright,
  rotated, noisy, low-resolution, and invalid images.
- `test_pipeline.py` — direct pipeline demo for one image; it prints the
  quality report and saves a processed image beside the input.
- Endpoint logic (decode → quality check → process → JPEG-encode →
  base64 round-trip → JSON serialization) was verified directly against
  all four sample images — confirmed the response JSON serializes
  cleanly and the base64 image decodes back into a valid OpenCV array
  on the "receiving" side.
- `test_api_client.py` exercises the actual running HTTP server (health
  check, upload, fetch-by-id) — run this yourself after `uvicorn
  main:app --reload` to see it hit the live API end-to-end, since a
  live server needs to be running to test the real HTTP layer.

## Design decisions worth knowing about

- **Quality score formula**: sharpness (Laplacian variance) and
  brightness (mean pixel intensity) are on very different numeric
  scales, so each is normalized to its own 0–100 sub-score before
  being combined with the guide's weights (sharpness 50% / brightness
  30% / resolution 20%). Brightness scores highest near a mid-range
  center and falls off toward both "too dark" and "too bright" — a
  washed-out overexposed image now correctly scores lower, not higher.
- Images with a score below 60 receive `low_confidence: true`, but are still
  enhanced and passed onward so the OCR/compliance layer can decide.
- **Deskew** uses Otsu thresholding before `minAreaRect`, which is more
  robust across different lighting than a fixed manual threshold, and
  only corrects when the detected angle is ≥ 2° so it never nudges an
  already-straight image.
- **Perspective correction** looks for the largest 4-point contour
  covering at least 25% of the frame; if nothing confident is found it
  quietly returns the original image rather than guessing. It stays
  off by default in `process_image()` (bonus feature, per the guide).
- **The API never crashes on a bad image** — CV errors are caught and
  turned into a `500` with a message, decode failures become a clean
  `400`, and oversized uploads become a `413`, matching the guide's
  "never block the pipeline" rule.
- **In-memory image store**: `processed_image_id` → bytes is a plain
  dict, capped at 50 entries. Fine for a hackathon demo; if you need it
  to survive a server restart, swap it for a temp-file directory later.
