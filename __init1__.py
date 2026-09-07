import pytesseract
from PIL import Image
import cv2
from pathlib import Path


class OCRService:

    def __init__(self):

        # Your actual Tesseract installation
        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Users\Mohnishraj\tesseract.exe"
        )

    def preprocess_image(self, image):
        """
        Preprocess the image to improve OCR accuracy.

        image can be:
        - image file path
        - OpenCV image
        """

        # If image is a file path
        if isinstance(image, (str, Path)):
            image_path = Path(image)
            image = cv2.imread(str(image_path))

            if image is None:
                raise FileNotFoundError(
                    f"Could not find or open image: {image_path}"
                )

        # If image is already an OpenCV image
        elif hasattr(image, "shape"):
            pass

        else:
            raise TypeError(
                "Image must be a file path or OpenCV image."
            )

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Increase image size
        gray = cv2.resize(
            gray,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC
        )

        # Remove small noise
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        # Convert to black and white
        processed = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        return processed

    def extract_text(self, image):
        """
        Extract text from an image using Tesseract OCR.
        """

        # Preprocess the image
        processed_image = self.preprocess_image(image)

        # Tesseract OCR configuration
        config = "--oem 3 --psm 6"

        text = pytesseract.image_to_string(
            processed_image,
            config=config
        )

        return text.strip()


if __name__ == "__main__":

    # Create OCR service
    ocr = OCRService()

    # Your product image
    image_path = Path(__file__).parent / "images" / "product1.jpeg"

    print("Reading product image...")

    # Extract text
    text = ocr.extract_text(image_path)

    print("\n----- OCR RESULT -----")
    print(text)
    print("----------------------")