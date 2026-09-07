import os
import re
from dataclasses import asdict
from pathlib import Path
from typing import Any, Protocol

import cv2
import pytesseract

from backend.ocr.pipeline import analyze_product_label
from app.services.compliance import LegalMetrologyRuleEngine
from image_processing.image_processor import process_image
from image_processing.quality_checker import check_image_quality


class Processor(Protocol):
    def process(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Process a validated generic payload."""


class MockProcessor:
    def process(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {
            "processor": "mock",
            "message": "Mock processing completed",
        }


class ProcessingError(Exception):
    """Base error for failures while processing an uploaded scan."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


class InvalidImageError(ProcessingError):
    def __init__(self, message: str = "Uploaded scan is not a valid image") -> None:
        super().__init__("invalid_image", message)


class OCRProcessingError(ProcessingError):
    def __init__(self, message: str = "OCR processing failed") -> None:
        super().__init__("ocr_processing_failed", message)


class TesseractRuntimeError(ProcessingError):
    def __init__(self) -> None:
        super().__init__(
            "tesseract_unavailable",
            "Tesseract OCR is unavailable. Configure PACKSURE_TESSERACT_CMD.",
        )


class OCRProcessor:
    """Application adapter for image preprocessing and the canonical OCR pipeline."""

    def __init__(self) -> None:
        self.compliance_engine = LegalMetrologyRuleEngine()

    @staticmethod
    def _compliance_product(analysis: dict[str, Any], quality: dict[str, Any]) -> dict[str, Any]:
        entities = analysis["entities"]
        quantity = entities.get("net_quantity")
        quantity_value = None
        quantity_unit = None
        if isinstance(quantity, str):
            match = re.match(r"^\s*([\d.]+)\s*([A-Za-z]+)", quantity)
            if match:
                quantity_value = match.group(1)
                quantity_unit = match.group(2).lower()

        return {
            **entities,
            "date_of_manufacture": entities.get("manufacturing_date"),
            "consumer_care": entities.get("customer_care_phone")
            or entities.get("customer_care_email"),
            "net_quantity": quantity_value or quantity,
            "quantity_unit": quantity_unit,
            "readable": not quality.get("low_confidence", False),
            "pdp_visible": True,
        }

    def process(self, payload: dict[str, Any]) -> dict[str, Any]:
        file_path = Path(str(payload["file_path"]))
        image = cv2.imread(str(file_path), cv2.IMREAD_COLOR)
        if image is None:
            raise InvalidImageError()

        try:
            quality = check_image_quality(image)
            enhanced_image = process_image(image)
            tesseract_cmd = os.getenv("PACKSURE_TESSERACT_CMD")
            default_tesseract = Path(
                r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            )
            if not tesseract_cmd and default_tesseract.is_file():
                tesseract_cmd = str(default_tesseract)
            analysis = analyze_product_label(
                enhanced_image,
                tesseract_cmd=tesseract_cmd,
            )
            compliance_results = self.compliance_engine.check_product(
                self._compliance_product(analysis, quality)
            )
        except pytesseract.TesseractNotFoundError as error:
            raise TesseractRuntimeError() from error
        except pytesseract.TesseractError as error:
            raise OCRProcessingError("Tesseract could not process the image") from error
        except (FileNotFoundError, TypeError, ValueError) as error:
            raise InvalidImageError(str(error)) from error
        except RuntimeError as error:
            raise OCRProcessingError() from error

        return {
            "processor": "ocr",
            "quality": quality,
            **analysis,
            "compliance": {
                "summary": self.compliance_engine.calculate_summary(compliance_results),
                "rules": [asdict(result) for result in compliance_results],
            },
        }
