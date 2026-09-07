import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\Mohnishraj\tesseract.exe"
)

print(pytesseract.get_tesseract_version())