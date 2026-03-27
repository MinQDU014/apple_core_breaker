import pyautogui
from config import GRID_TOP_LEFT, CELL_SIZE

def drag_rectangle(r1, c1, r2, c2):
    x0, y0 = GRID_TOP_LEFT
    w, h = CELL_SIZE
    start_x = x0 + c1 * w + w // 2
    start_y = y0 + r1 * h + h // 2
    end_x = x0 + (c2 - 1) * w + w // 2
    end_y = y0 + (r2 - 1) * h + h // 2
    pyautogui.moveTo(start_x, start_y, duration=0.1)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=0.2)
    pyautogui.mouseUp()