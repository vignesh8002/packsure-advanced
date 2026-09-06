"""
test_pipeline.py
-----------------
Quick manual test script for Member 2's deliverables.

Usage:
    python test_pipeline.py path/to/test_product.jpg

This will:
  1. Print the quality report for the original image.
  2. Run the enhancement pipeline.
  3. Save the enhanced image next to the original as
     "<name>_processed.jpg" so you can visually compare before/after
     (useful for the hackathon demo + slides).

If you don't have real product photos yet, run:
    python make_sample_test_images.py
first to generate a few synthetic ones under test_images/.
"""

import sys
import os
import cv2

from image_processing.quality_checker import check_image_quality
from image_processing.image_processor import process_image


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_pipeline.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    image = cv2.imread(image_path)

    if image is None:
        print(f"Could not read image: {image_path}")
        sys.exit(1)

    print(f"\n--- Quality report for: {image_path} ---")
    quality = check_image_quality(image)
    for key, value in quality.items():
        print(f"  {key}: {value}")

    print("\n--- Running enhancement pipeline ---")
    processed = process_image(image)

    root, ext = os.path.splitext(image_path)
    output_path = f"{root}_processed{ext or '.jpg'}"
    cv2.imwrite(output_path, processed)
    print(f"Saved enhanced image to: {output_path}")


if __name__ == "__main__":
    main()
