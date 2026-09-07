
import pytesseract
from pytesseract import Output
from PIL import Image
import cv2


class OCRService:

    def __init__(self):

        # ==========================================================
        # TESSERACT CONFIGURATION
        # ==========================================================

        # Your actual Tesseract installation
        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Users\Mohnishraj\tesseract.exe"
        )

    # ==============================================================
    # IMAGE PREPROCESSING
    # ==============================================================

    def preprocess_image(self, image):

        """
        Preprocess product/package image before OCR.

        Steps:
        1. Read image
        2. Convert to grayscale
        3. Resize
        4. Remove noise
        5. Apply thresholding
        """

        # ----------------------------------------------------------
        # If image is a file path
        # ----------------------------------------------------------

        if isinstance(image, str):

            image = cv2.imread(image)

            if image is None:
                raise FileNotFoundError(
                    f"Could not open image: {image}"
                )

        # ----------------------------------------------------------
        # If image is already an OpenCV image
        # ----------------------------------------------------------

        elif hasattr(image, "shape"):

            pass

        else:

            raise TypeError(
                "Image must be a file path or OpenCV image."
            )

        # ----------------------------------------------------------
        # Convert to grayscale
        # ----------------------------------------------------------

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        # ----------------------------------------------------------
        # Increase image size
        # ----------------------------------------------------------

        gray = cv2.resize(
            gray,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC
        )

        # ----------------------------------------------------------
        # Reduce noise
        # ----------------------------------------------------------

        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )

        # ----------------------------------------------------------
        # Convert to black and white
        # ----------------------------------------------------------

        processed = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

        return processed

    # ==============================================================
    # OCR TEXT EXTRACTION
    # ==============================================================

    def extract_text(self, image):

        """
        Extract raw text from a product/package image.

        Returns:
            {
                "full_text": "...",
                "lines": [...],
                "average_confidence": 0.0
            }
        """

        # ----------------------------------------------------------
        # Preprocess image
        # ----------------------------------------------------------

        processed_image = self.preprocess_image(
            image
        )

        # ----------------------------------------------------------
        # Tesseract configuration
        # ----------------------------------------------------------

        config = "--oem 3 --psm 6"

        # ----------------------------------------------------------
        # Get OCR text
        # ----------------------------------------------------------

        full_text = pytesseract.image_to_string(
            processed_image,
            config=config
        ).strip()

        # ----------------------------------------------------------
        # Get confidence information
        # ----------------------------------------------------------

        data = pytesseract.image_to_data(
            processed_image,
            output_type=Output.DICT,
            config=config
        )

        lines = []

        current_words = []
        current_confidences = []

        previous_block = None
        previous_paragraph = None
        previous_line = None

        # ----------------------------------------------------------
        # Process OCR words
        # ----------------------------------------------------------

        for i in range(len(data["text"])):

            word = data["text"][i].strip()

            try:
                confidence = float(
                    data["conf"][i]
                )
            except (ValueError, TypeError):
                confidence = -1

            # Ignore empty/invalid OCR results
            if not word or confidence < 0:
                continue

            block = data["block_num"][i]
            paragraph = data["par_num"][i]
            line = data["line_num"][i]

            # ------------------------------------------------------
            # Detect new OCR line
            # ------------------------------------------------------

            if (
                previous_block is not None
                and (
                    block != previous_block
                    or paragraph != previous_paragraph
                    or line != previous_line
                )
            ):

                if current_words:

                    line_text = " ".join(
                        current_words
                    )

                    line_confidence = (
                        sum(current_confidences)
                        / len(current_confidences)
                    )

                    lines.append({
                        "text": line_text,
                        "confidence": round(
                            line_confidence,
                            2
                        )
                    })

                current_words = []
                current_confidences = []

            current_words.append(word)
            current_confidences.append(
                confidence
            )

            previous_block = block
            previous_paragraph = paragraph
            previous_line = line

        # ----------------------------------------------------------
        # Add final line
        # ----------------------------------------------------------

        if current_words:

            line_text = " ".join(
                current_words
            )

            line_confidence = (
                sum(current_confidences)
                / len(current_confidences)
            )

            lines.append({
                "text": line_text,
                "confidence": round(
                    line_confidence,
                    2
                )
            })

        # ----------------------------------------------------------
        # Calculate average confidence
        # ----------------------------------------------------------

        if lines:

            average_confidence = (
                sum(
                    line["confidence"]
                    for line in lines
                )
                / len(lines)
            )

        else:

            average_confidence = 0

        # ----------------------------------------------------------
        # Return complete OCR result
        # ----------------------------------------------------------

        return {
            "full_text": full_text,
            "lines": lines,
            "average_confidence": round(
                average_confidence,
                2
            )
        }


# ==================================================================
# DIRECT TEST
# ==================================================================

if __name__ == "__main__":

    # Create OCR service
    ocr = OCRService()

    # Your actual test image
    image_path = (
        r"C:\Users\Mohnishraj\.vscode"
        r"\packsure\images\product1.jpeg"
    )

    print("Reading product image...")

    # Run OCR
    result = ocr.extract_text(
        image_path
    )

    # --------------------------------------------------------------
    # Display raw OCR
    # --------------------------------------------------------------

    print("\n==============================")
    print("        RAW OCR TEXT")
    print("==============================\n")

    print(
        result["full_text"]
    )

    # --------------------------------------------------------------
    # Display confidence
    # --------------------------------------------------------------

    print("\n==============================")
    print("       OCR CONFIDENCE")
    print("==============================\n")

    print(
        f"Average Confidence: "
        f"{result['average_confidence']}%"
    )

    # --------------------------------------------------------------
    # Display individual lines
    # --------------------------------------------------------------

    print("\n==============================")
    print("       OCR LINES")
    print("==============================\n")

    for line in result["lines"]:

        print(
            f"{line['text']} "
            f"→ {line['confidence']}%"
        )



