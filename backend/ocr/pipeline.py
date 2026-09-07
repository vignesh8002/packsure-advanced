"""High-level image-to-structured-product pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .entity_extractor import extract_entities
from .language_normalizer import detect_languages, normalize_keywords
from .ocr_service import OCRService


def analyze_product_label(
    image: Any,
    language: str = "eng",
    psm: int = 6,
    tesseract_cmd: str | Path | None = None,
) -> dict[str, Any]:
    """Run OCR, keyword normalization, language detection, and entity extraction."""
    ocr_result = OCRService(
        language=language,
        psm=psm,
        tesseract_cmd=tesseract_cmd,
    ).extract_text(image)
    raw_text = ocr_result["full_text"]
    normalized_text = normalize_keywords(raw_text)
    return {
        "ocr": ocr_result,
        "normalized_text": normalized_text,
        "detected_languages": detect_languages(raw_text)["detected_languages"],
        "entities": extract_entities(normalized_text),
    }


def analyze_product_batch(
    images: list[Any],
    language: str = "eng",
    psm: int = 6,
    tesseract_cmd: str | Path | None = None,
    max_images: int = 10,
) -> list[dict[str, Any]]:
    """Analyze up to ten images and return one result per input image."""
    if max_images < 1:
        raise ValueError("max_images must be at least 1")

    results = []
    for image in images[:max_images]:
        try:
            result = analyze_product_label(
                image,
                language=language,
                psm=psm,
                tesseract_cmd=tesseract_cmd,
            )
            results.append({"image": str(image), "success": True, **result})
        except (FileNotFoundError, TypeError, ValueError, RuntimeError) as error:
            results.append({
                "image": str(image),
                "success": False,
                "error": str(error),
            })
    return results
