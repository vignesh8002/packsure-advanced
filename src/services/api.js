async function readResponse(response) {
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(
      body?.error?.message || body?.detail || "The backend request failed."
    );
  }
  return body;
}

export async function uploadScan(file) {
  const formData = new FormData();
  formData.append("file", file, file.name || "product.jpg");

  const response = await fetch("/api/scan", {
    method: "POST",
    body: formData,
  });
  return readResponse(response);
}

export async function processScan(scanId) {
  const response = await fetch(`/api/v1/scan/${encodeURIComponent(scanId)}/process`, {
    method: "POST",
  });
  return readResponse(response);
}