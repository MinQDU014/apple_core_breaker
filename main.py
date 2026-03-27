import ctypes
import logging
import time
import os
import threading
from typing import Tuple, Optional
from pynput import mouse, keyboard

from core.grid_builder import compute_region_and_cell_from_corners, build_grid_from_templates, save_region_png
from core.strategy_adapter import find_strategy
from core.mouse_actions import drag_box

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    pass

tl_center: Optional[Tuple[int, int]] = None
br_center: Optional[Tuple[int, int]] = None
board_region: Optional[tuple] = None
cell_size: Optional[Tuple[int, int]] = None


def wait_for_center_click(prompt: str) -> Tuple[int, int]:
    print(prompt)
    clicked = []

    def on_click(x, y, button, pressed):
        if pressed:
            print(f"클릭됨: ({x}, {y})")
            logging.info(f"clicked {x},{y}")
            clicked.append((x, y))
            return False

    with mouse.Listener(on_click=on_click) as L:
        L.join()
    return clicked[0]


def action_set_tl():
    global tl_center, board_region, cell_size
    tl_center = wait_for_center_click("[F3] 최상단 최좌측(첫 칸)의 중심을 클릭하세요.")
    print(f"TL set: {tl_center}")
    board_region = None;
    cell_size = None


def action_set_br():
    global br_center, board_region, cell_size
    if not tl_center:
        print("먼저 F3으로 최상단 최좌측(첫 칸) 중심을 설정하세요.")
        return
    br_center = wait_for_center_click("[F4] 최하단 최우측(마지막 칸)의 중심을 클릭하세요.")
    print(f"BR set: {br_center}")
    board_region, cell_size = compute_region_and_cell_from_corners(tl_center, br_center)
    print(f"→ 계산된 CELL_SIZE: {cell_size}, 보드 영역: {board_region}")
    logging.info(f"region={board_region}, cell={cell_size}")
    save_region_png(board_region, "capture_region_manual.png")
    print("📸 debug/capture_region_manual.png 저장 완료")


def action_solve_once():
    if not board_region or not cell_size:
        print("보드 영역이 설정되지 않았습니다. F3, F4 순서로 먼저 지정하세요.")
        return
    left, top, width, height = board_region
    print("[F8] 분석/풀이 시작... (멈추려면 F9 또는 F12 연타!)")
    logging.info("Solve started")
    board, total, hits, digit_hits = build_grid_from_templates(board_region, cell_size)
    print(f"인식 성공 수(hits): {hits}, 합계: {total}, per-digit: {digit_hits}")
    logging.debug(f"Board={board}")
    if hits == 0:
        print("⚠️ 매칭 0건. 템플릿/배율/CELL_SIZE 재점검 필요.")
        return
    strategy = find_strategy([row[:] for row in board])
    score = getattr(strategy, 'score', 0)
    boxes = getattr(strategy, 'boxes', [])
    print(f"선택 박스 수: {len(boxes)}, 예상 점수: {score}")
    for i, box in enumerate(boxes):
        logging.info(f"Drag box #{i}: ({box.x},{box.y},{box.width},{box.height})")
        drag_box(left, top, box, cell_size)
        time.sleep(0.12)
    print("✅ 풀이 완료")


def main():
    print("\n[사용법]")
    print("F3       : 최상단 최좌측(첫 칸) 중심 클릭")
    print("F4       : 최하단 최우측(마지막 칸) 중심 클릭 → 자동으로 셀 크기 계산")
    print("F8       : 분석 및 풀이 1회 실행")
    print("F9 / F12 : 🚨 긴급 강제 종료 (언제든지 즉시 멈춤)")
    print("ESC      : 프로그램 정상 종료")
    print("브라우저 줌 100%로 맞춰주세요.\n")

    def on_press(key):
        try:
            if key == keyboard.Key.f3:
                action_set_tl()
            elif key == keyboard.Key.f4:
                action_set_br()
            elif key == keyboard.Key.f8:
                # 💡 핵심 해결책: F8 작업(마우스 움직임)을 별도의 백그라운드 스레드로 실행합니다!
                # 이렇게 하면 마우스가 미친듯이 움직이는 와중에도 키보드 감지가 멈추지 않습니다.
                threading.Thread(target=action_solve_once, daemon=True).start()

            elif key in (keyboard.Key.f9, keyboard.Key.f12):
                print("\n🚨 [긴급 정지] F9 또는 F12 입력됨! 즉시 시스템을 종료합니다!")
                os._exit(0)  # 무조건 묻지도 따지지도 않고 바로 킬!

            elif key == keyboard.Key.esc:
                print("종료합니다.")
                os._exit(0)
        except Exception as e:
            logging.exception("핫키 처리 중 오류")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == '__main__':
    main()