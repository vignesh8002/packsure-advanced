import pytesseract
from PIL import Image

# If Windows cannot find Tesseract automatically,
# uncomment and modify this line:
#
# pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Mohnishraj\tesseract.exe"

image_path = "test_images/english/product.jpg"

image = Image.open(image_path)

text = pytesseract.image_to_string(image)

print("========== OCR OUTPUT ==========")
print(text)