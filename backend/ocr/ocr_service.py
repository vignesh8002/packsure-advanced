"""Tesseract OCR service for product labels."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pytesseract
from pytesseract import Output


class OCRService:
    """Extract text, word confidence, and line confidence from an image."""

    def __init__(
        self,
        language: str = "eng",
        psm: int = 6,
        tesseract_cmd: str | Path | None = None,
    ) -> None:
        self.language = language
        self.psm = psm
        command = tesseract_cmd or os.getenv("PACKSURE_TESSERACT_CMD")
        if not command:
            command = shutil.which("tesseract")
        if not command:
            user_tesseract = Path.home() / "tesseract.exe"
            if user_tesseract.is_file():
                command = user_tesseract
        if command:
            pytesseract.pytesseract.tesseract_cmd = str(command)

    @property
    def config(self) -> str:
        return f"--oem 3 --psm {self.psm}"

    def _load_image(self, image: str | Path | np.ndarray) -> np.ndarray:
        if isinstance(image, (str, Path)):
            image_path = Path(image)
            if not image_path.is_file():
                raise FileNotFoundError(f"Image file does not exist: {image_path}")
            loaded = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
            if loaded is None:
                raise ValueError(f"Could not read image file: {image_path}")
            image = loaded

        if not isinstance(image, np.ndarray) or image.size == 0:
            raise ValueError("image must be a non-empty OpenCV/NumPy image or file path")

        if image.ndim == 2:
            return cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        if image.ndim == 3 and image.shape[2] == 3:
            return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if image.ndim == 3 and image.shape[2] == 4:
            return cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
        raise ValueError("image must be grayscale, BGR, or BGRA")

    def extract_text(self, image: str | Path | np.ndarray) -> dict[str, Any]:
        """Return raw OCR text, words, grouped lines, and 0-1 confidence values."""
        rgb_image = self._load_image(image)
        data = pytesseract.image_to_data(
            rgb_image,
            lang=self.language,
            config=self.config,
            output_type=Output.DICT,
        )

        grouped: dict[tuple[int, int, int], list[dict[str, Any]]] = {}
        words: list[dict[str, Any]] = []
        confidences: list[float] = []
        for index, raw_text in enumerate(data.get("text", [])):
            text = str(raw_text).strip()
            try:
                raw_confidence = float(data["conf"][index])
            except (KeyError, IndexError, TypeError, ValueError):
                raw_confidence = -1
            if not text or raw_confidence < 0:
                continue

            confidence = round(max(0.0, min(raw_confidence / 100.0, 1.0)), 4)
            word = {
                "text": text,
                "confidence": confidence,
                "bbox": {
                    "left": int(data["left"][index]),
                    "top": int(data["top"][index]),
                    "width": int(data["width"][index]),
                    "height": int(data["height"][index]),
                },
            }
            words.append(word)
            confidences.append(confidence)
            key = (
                int(data["block_num"][index]),
                int(data["par_num"][index]),
                int(data["line_num"][index]),
            )
            grouped.setdefault(key, []).append(word)

        lines = []
        for line_words in grouped.values():
            line_confidences = [word["confidence"] for word in line_words]
            lines.append(
                {
                    "text": " ".join(word["text"] for word in line_words),
                    "confidence": round(sum(line_confidences) / len(line_confidences), 4),
                }
            )

        return {
            "full_text": "\n".join(line["text"] for line in lines),
            "lines": lines,
            "words": words,
            "average_confidence": round(sum(confidences) / len(confidences), 4)
            if confidences
            else 0,
        }
