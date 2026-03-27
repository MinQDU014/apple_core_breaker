import pytesseract
import cv2
import numpy as np
from PIL import Image
from config import TESSERACT_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def preprocess_image(pil_img):
    img = np.array(pil_img.convert('RGB'))

    # Resize (optional)
    img = cv2.resize(img, (80, 80), interpolation=cv2.INTER_LINEAR)

    # Convert to HSV and mask out red background (apple body)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)

    # Invert mask to keep only non-red (number) part
    mask_inv = cv2.bitwise_not(mask_red)
    result = cv2.bitwise_and(img, img, mask=mask_inv)

    # Convert to grayscale and apply threshold
    gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return binary

def recognize_digit(pil_image):
    processed = preprocess_image(pil_image)
    config = '--psm 10 -c tessedit_char_whitelist=123456789'
    text = pytesseract.image_to_string(processed, config=config)
    try:
        return int(text.strip())
    except ValueError:
        return 0