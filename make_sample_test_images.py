"""
make_sample_test_images.py
---------------------------
Generates a handful of synthetic product-label-like test images so you
can exercise the pipeline (blur/brightness/deskew) before you have real
photos from Member 1's camera capture flow. Not a deliverable itself -
just a convenience for local testing.

Usage:
    python make_sample_test_images.py
"""

import os
import cv2
import numpy as np

OUTPUT_ROOT = "test_images"


def _make_base_label():
    img = np.full((900, 1200, 3), 235, dtype=np.uint8)
    lines = [
        "PRODUCT NAME SAMPLE",
        "MRP Rs.120/-",
        "Net Wt 500 g",
        "Packed Aug 2026",
        "Made in India",
    ]
    for i, line in enumerate(lines):
        y = 150 + i * 130
        cv2.putText(
            img, line, (60, y), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (20, 20, 20), 3
        )
    return img


def main():
    base = _make_base_label()

    clear_dir = os.path.join(OUTPUT_ROOT, "clear")
    blurry_dir = os.path.join(OUTPUT_ROOT, "blurry")
    dark_dir = os.path.join(OUTPUT_ROOT, "dark")
    rotated_dir = os.path.join(OUTPUT_ROOT, "rotated")

    for d in (clear_dir, blurry_dir, dark_dir, rotated_dir):
        os.makedirs(d, exist_ok=True)

    cv2.imwrite(os.path.join(clear_dir, "clear_sample.jpg"), base)

    blurry = cv2.GaussianBlur(base, (25, 25), 10)
    cv2.imwrite(os.path.join(blurry_dir, "blurry_sample.jpg"), blurry)

    dark = (base.astype(np.float32) * 0.25).astype(np.uint8)
    cv2.imwrite(os.path.join(dark_dir, "dark_sample.jpg"), dark)

    center = (base.shape[1] // 2, base.shape[0] // 2)
    matrix = cv2.getRotationMatrix2D(center, 8, 1.0)
    rotated = cv2.warpAffine(
        base, matrix, (base.shape[1], base.shape[0]), borderValue=(235, 235, 235)
    )
    cv2.imwrite(os.path.join(rotated_dir, "rotated_sample.jpg"), rotated)

    print("Sample test images created under test_images/:")
    print("  clear/clear_sample.jpg")
    print("  blurry/blurry_sample.jpg")
    print("  dark/dark_sample.jpg")
    print("  rotated/rotated_sample.jpg")


if __name__ == "__main__":
    main()
