from pathlib import Path

from backend.ocr.pipeline import analyze_product_batch


IMAGE_FOLDER = Path(__file__).parent / "images"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
MAX_IMAGES = 10


def main() -> None:
    image_files = sorted(
        file for file in IMAGE_FOLDER.iterdir()
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
    )[:MAX_IMAGES]

    if not image_files:
        print(f"No supported images found in: {IMAGE_FOLDER}")
        return

    print(f"Scanning {len(image_files)} image(s), maximum {MAX_IMAGES} per run")
    results = analyze_product_batch(image_files, max_images=MAX_IMAGES)

    for index, result in enumerate(results, start=1):
        print(f"\n===== PRODUCT {index}: {Path(result['image']).name} =====")
        if not result["success"]:
            print(f"OCR ERROR: {result['error']}")
            continue

        print(result["ocr"]["full_text"])
        print(f"Confidence: {result['ocr']['average_confidence']:.2f}")
        print("Entities:")
        for field, value in result["entities"].items():
            print(f"  {field}: {value}")


if __name__ == "__main__":
    main()
