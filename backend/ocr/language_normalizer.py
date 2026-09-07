"""Lightweight multilingual keyword normalization."""

from __future__ import annotations

import re


ALIASES = {
    "MRP": ["maximum retail price", "mrp", "अधिकतम खुदरा मूल्य", "அதிகபட்ச சில்லறை விலை"],
    "NET_QUANTITY": ["net quantity", "net qty", "net weight", "net wt", "शुद्ध मात्रा", "நிகர அளவு"],
    "PACKING_DATE": ["packing date", "packed", "pkd", "पैक किया गया", "पैकिंग की तारीख", "பேக் செய்யப்பட்ட", "பேக்கிங் தேதி"],
    "COUNTRY_OF_ORIGIN": ["country of origin", "made in", "product of", "मूल देश", "भारत में निर्मित", "தயாரிக்கப்பட்ட நாடு", "இந்தியாவில் தயாரிக்கப்பட்டது"],
}


def normalize_keywords(text: str) -> str:
    """Replace known label keywords while preserving their values and other text."""
    normalized = text or ""
    aliases = sorted(
        ((alias, field) for field, values in ALIASES.items() for alias in values),
        key=lambda item: len(item[0]),
        reverse=True,
    )
    for alias, field in aliases:
        normalized = re.sub(re.escape(alias), field, normalized, flags=re.IGNORECASE)
    return normalized


def detect_languages(text: str) -> dict[str, list[str]]:
    """Detect languages using lightweight Unicode-range checks."""
    languages = []
    if re.search(r"[A-Za-z]", text or ""):
        languages.append("English")
    if re.search(r"[\u0900-\u097F]", text or ""):
        languages.append("Hindi")
    if re.search(r"[\u0B80-\u0BFF]", text or ""):
        languages.append("Tamil")
    return {"detected_languages": languages}
