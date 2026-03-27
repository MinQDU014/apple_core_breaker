import mss
from PIL import Image
from config import GRID_TOP_LEFT, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT

def capture_board():
    x0, y0 = GRID_TOP_LEFT
    w, h = CELL_SIZE
    images = []
    with mss.mss() as sct:
        for row in range(GRID_HEIGHT):
            line = []
            for col in range(GRID_WIDTH):
                x = x0 + col * w
                y = y0 + row * h
                monitor = {"top": y, "left": x, "width": w, "height": h}
                img = sct.grab(monitor)
                pil_img = Image.frombytes("RGB", img.size, img.rgb)
                line.append(pil_img)
            images.append(line)
    return images