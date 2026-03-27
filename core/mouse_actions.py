import pyautogui
import time
import random
import math

from config import GLOBAL_SPEED

# ==========================================

def drag_box(left: int, top: int, box, cell_size) -> None:
    """ box has x,y,width,height in cell units """
    w, h = cell_size

    # ---------------------------------------------------
    # 🧠 사람의 '생각하는 시간(인지 지연)' 시뮬레이션
    # 사람은 매 턴마다 일정한 속도로 움직이지 않습니다.
    # 15%의 확률로 다음 사과를 찾느라 0.5초 ~ 1.5초 정도 화면을 스캔하며 고민합니다.
    # 나머지 85%의 확률로도 연속 동작 사이에 미세한 숨 고르기(0.05 ~ 0.15초)를 합니다.
    if random.random() < 0.15:
        thinking_time = random.uniform(0.5, 1.5) * GLOBAL_SPEED
        time.sleep(thinking_time)
    else:
        short_pause = random.uniform(0.05, 0.15) * GLOBAL_SPEED
        time.sleep(short_pause)
    # ---------------------------------------------------

    # 1. 좌표의 미세한 흔들림 (Jitter)
    start_ratio_x = random.uniform(0.15, 0.25)
    start_ratio_y = random.uniform(0.15, 0.25)
    end_ratio_x = random.uniform(0.15, 0.25)
    end_ratio_y = random.uniform(0.15, 0.25)

    start_x = int(left + box.x * w + w * start_ratio_x)
    start_y = int(top + box.y * h + h * start_ratio_y)

    end_x = int(left + (box.x + box.width) * w - w * end_ratio_x)
    end_y = int(top + (box.y + box.height) * h - h * end_ratio_y)

    # 2. 이동 거리에 비례하는 드래그 시간 계산 + 마스터 속도 조절
    distance = math.hypot(end_x - start_x, end_y - start_y)

    base_drag_duration = 0.1 + (distance * 0.0003) + random.uniform(-0.02, 0.02)
    drag_duration = max(0.08, base_drag_duration) * GLOBAL_SPEED

    base_move_to_duration = random.uniform(0.08, 0.12)
    move_to_duration = base_move_to_duration * GLOBAL_SPEED

    # 3. 사람다운 멈칫 딜레이 + 마스터 속도 조절
    click_delay_1 = max(0.01, random.gauss(0.03, 0.015)) * GLOBAL_SPEED
    click_delay_2 = max(0.01, random.gauss(0.03, 0.015)) * GLOBAL_SPEED

    # ------------------ 마우스 액션 시작 ------------------

    # 다음 목표물로 마우스 이동 (가속/감속 적용)
    pyautogui.moveTo(start_x, start_y, duration=move_to_duration, tween=pyautogui.easeOutQuad)

    # 마우스 클릭 후 찰나의 대기
    pyautogui.mouseDown(button='left')
    time.sleep(click_delay_1)

    # 마우스 드래그 (가속/감속 적용)
    pyautogui.moveTo(end_x, end_y, duration=drag_duration, tween=pyautogui.easeInOutQuad)
    time.sleep(click_delay_2)

    # 마우스 떼기
    pyautogui.mouseUp(button='left')