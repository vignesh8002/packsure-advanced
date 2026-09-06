# PackSure AI backend

## Setup

From the project directory:

```powershell
uv sync --dev
```

## Run the API

```powershell
uv run uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

Health check:

```text
GET http://127.0.0.1:8000/health
```

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Integration contract foundation

Versioned API routes use the `/api/v1` prefix. The generic Pydantic envelopes are
available in `app/models/envelopes.py` for use when the frontend and processing
schemas are finalized.

Requests may provide an `X-Request-ID` header. If omitted, the API generates a
request ID. The value is returned in the `X-Request-ID` response header and is
available for standardized success and error responses.

The processing boundary is defined by the simple `Processor` protocol in
`app/services/processor.py`. No processing endpoint is implemented yet.

## Scan upload

Upload one image using the `file` multipart/form-data field:

```text
POST /api/scan
Content-Type: multipart/form-data
```

Only JPG, JPEG, and PNG files up to 10 MB are accepted. The image is saved
temporarily in `uploads/`, and the response contains a generated `scan_id`.
No image processing is performed yet.

## Mock scan processing

An existing scan can be sent to the mock processing boundary:

```text
POST /api/v1/scan/{scan_id}/process
```

This verifies that the uploaded scan exists and returns a generic mock result.
No image processing, OCR, entity extraction, or compliance logic is performed.

## Run tests

```powershell
uv run pytest
```