from pathlib import Path

import cv2

from backend.ocr.entity_extractor import extract_entities
from backend.ocr.language_normalizer import detect_languages, normalize_keywords
from backend.ocr.ocr_service import OCRService
from backend.ocr.pipeline import analyze_product_label


SAMPLE_TEXT = """MRP Rs. 120
Net Wt 500g
Packed Aug 2026
Made in India"""
import unittest
from unittest.mock import patch

class PacksureOCRTests(unittest.TestCase):
    def test_entities_from_english_label(self):
        entities = extract_entities(SAMPLE_TEXT)
        self.assertEqual(entities["mrp"], "120 INR")
        self.assertEqual(entities["net_quantity"], "500 g")
        self.assertEqual(entities["packing_date"], "08/2026")
        self.assertEqual(entities["country_of_origin"], "India")
        self.assertEqual(len(entities), 13)

    def test_multilingual_keyword_normalization(self):
        normalized = normalize_keywords("MRP शुद्ध मात्रा 500g தமிழில் தயாரிக்கப்பட்ட நாடு")
        self.assertIn("MRP", normalized)
        self.assertIn("NET_QUANTITY", normalized)
        self.assertIn("COUNTRY_OF_ORIGIN", normalized)
        self.assertEqual(
            detect_languages("MRP भारत தமிழில்")["detected_languages"],
            ["English", "Hindi", "Tamil"],
        )

    @patch("pytesseract.image_to_data")
    def test_empty_ocr_result_is_safe(self, image_to_data):
        image_to_data.return_value = {
            key: [] for key in (
                "text", "conf", "left", "top", "width", "height",
                "block_num", "par_num", "line_num",
            )
        }
        image = cv2.imread(str(Path(__file__).parent / "images" / "product1.jpeg"))
        result = OCRService().extract_text(image)
        self.assertEqual(result["full_text"], "")
        self.assertEqual(result["lines"], [])
        self.assertEqual(result["average_confidence"], 0)

    def test_pipeline_on_real_image(self):
        image_path = Path(__file__).parent / "images" / "product1.jpeg"
        result = analyze_product_label(image_path)
        self.assertIn("ocr", result)
        self.assertIn("entities", result)
        self.assertIsInstance(result["ocr"]["average_confidence"], float)


if __name__ == "__main__":
    unittest.main()


def test_entities_from_english_label():
    entities = extract_entities(SAMPLE_TEXT)
    assert entities["mrp"] == "120 INR"
    assert entities["net_quantity"] == "500 g"
    assert entities["packing_date"] == "08/2026"
    assert entities["country_of_origin"] == "India"
    assert set(entities) == {
        "product_name", "mrp", "net_quantity", "manufacturer", "packer", "address",
        "country_of_origin", "customer_care_phone", "customer_care_email",
        "manufacturing_date", "packing_date", "best_before", "expiry_date",
    }


def test_multilingual_keyword_normalization():
    normalized = normalize_keywords("MRP शुद्ध मात्रा 500g தமிழில் தயாரிக்கப்பட்ட நாடு")
    assert "MRP" in normalized
    assert "NET_QUANTITY" in normalized
    assert "COUNTRY_OF_ORIGIN" in normalized
    assert detect_languages("MRP भारत தமிழில்")["detected_languages"] == ["English", "Hindi", "Tamil"]


def test_empty_ocr_result_is_safe(monkeypatch):
    monkeypatch.setattr(
        "pytesseract.image_to_data",
        lambda *args, **kwargs: {"text": [], "conf": [], "left": [], "top": [], "width": [], "height": [], "block_num": [], "par_num": [], "line_num": []},
    )
    result = OCRService().extract_text(cv2.imread(str(Path("images/product1.jpeg"))))
    assert result["full_text"] == ""
    assert result["lines"] == []
    assert result["average_confidence"] == 0


def test_pipeline_on_real_image():
    image_path = Path(__file__).parent / "images" / "product1.jpeg"
    result = analyze_product_label(image_path)
    assert "ocr" in result
    assert "entities" in result
    assert isinstance(result["ocr"]["average_confidence"], float)
