from PIL import ImageGrab
import pytesseract

img = ImageGrab.grab(bbox=(1423, 402, 1423+40, 402+40))  # 사과 첫 칸
img.show()

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
print(pytesseract.image_to_string(img, config='--psm 10 -c tessedit_char_whitelist=123456789'))
