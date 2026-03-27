import os
from typing import List, Tuple
import cv2
import numpy as np
import mss
from config import GRID_WIDTH, GRID_HEIGHT, CONF_START, CONF_FLOOR, CONF_STEP, SCALES, DEBUG_DIR

def _ensure_debug_dir():
    os.makedirs(DEBUG_DIR, exist_ok=True)

def _grab_region_bgr(region):
    left, top, width, height = region
    with mss.mss() as sct:
        mon = {"left": int(left), "top": int(top), "width": int(width), "height": int(height)}
        img = sct.grab(mon)
        arr = np.array(img)  # BGRA
        return arr[:,:,:3]   # BGR

def save_region_png(region, filename):
    _ensure_debug_dir()
    bgr = _grab_region_bgr(region)
    cv2.imwrite(os.path.join(DEBUG_DIR, filename), bgr)

def compute_region_and_cell_from_corners(tl_center: Tuple[int,int], br_center: Tuple[int,int]):
    tlx, tly = tl_center
    brx, bry = br_center
    # 셀 사이 간격으로 셀 크기 산출 (센터→센터)
    cell_w = max(1, int(round((brx - tlx) / (GRID_WIDTH - 1))))
    cell_h = max(1, int(round((bry - tly) / (GRID_HEIGHT - 1))))
    # 좌상단 픽셀 좌표
    left = int(round(tlx - cell_w / 2))
    top  = int(round(tly - cell_h / 2))
    width  = cell_w * GRID_WIDTH
    height = cell_h * GRID_HEIGHT
    return (left, top, width, height), (cell_w, cell_h)

def _match_scaled(screen_bgr, templ_bgr, confidence):
    res_rects = []
    scr_g = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)
    templ0 = templ_bgr
    for scale in SCALES:
        if scale == 1.0:
            templ = templ0
        else:
            new_w = max(1, int(templ0.shape[1]*scale))
            new_h = max(1, int(templ0.shape[0]*scale))
            templ = cv2.resize(templ0, (new_w, new_h), interpolation=cv2.INTER_AREA)
        templ_g = cv2.cvtColor(templ, cv2.COLOR_BGR2GRAY)
        if templ_g.shape[0] >= scr_g.shape[0] or templ_g.shape[1] >= scr_g.shape[1]:
            continue
        res = cv2.matchTemplate(scr_g, templ_g, cv2.TM_CCOEFF_NORMED)
        ys, xs = np.where(res >= confidence)
        h, w = templ_g.shape[:2]
        for (xx, yy) in zip(xs, ys):
            res_rects.append((xx, yy, w, h))
    # 간단 병합
    merged = []
    for (x, y, w, h) in res_rects:
        if not any(abs(x - mx) < w//2 and abs(y - my) < h//2 for (mx, my, mw, mh) in merged):
            merged.append((x, y, w, h))
    return merged

def build_grid_from_templates(region, cell_size) -> Tuple[List[List[int]], int, int, dict]:
    left, top, width, height = region
    w, h = cell_size
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    total = 0
    hits = 0
    digit_hits = {d:0 for d in range(1,10)}

    screen_bgr = _grab_region_bgr(region)
    _ensure_debug_dir()
    cv2.imwrite(os.path.join(DEBUG_DIR, "capture_region.png"), screen_bgr)

    conf = CONF_START
    while conf >= CONF_FLOOR and hits == 0:
        for digit in range(1, 10):
            template_path = os.path.join('assets', 'images', f'apple{digit}.png')

            # 1. 파일이 실제로 있는지 체크해서 터미널에 출력
            if not os.path.exists(template_path):
                print(f"❌ 파일 없음: {template_path}")
                continue

            # 2. 한글 경로에서도 이미지를 읽어올 수 있도록 numpy 활용
            path_array = np.fromfile(template_path, np.uint8)
            templ = cv2.imdecode(path_array, cv2.IMREAD_COLOR)

            if templ is None:
                print(f"❌ 이미지 로드 실패 (손상되거나 읽을 수 없음): {template_path}")
                continue
            matches = _match_scaled(screen_bgr, templ, conf)
            for (lx, ly, lw, lh) in matches:
                r = ly // h
                c = lx // w
                if 0 <= r < GRID_HEIGHT and 0 <= c < GRID_WIDTH and grid[r][c] == 0:
                    grid[r][c] = digit
                    total += digit
                    hits += 1
                    digit_hits[digit] += 1
        conf -= CONF_STEP
        if hits > 0:
            break
    return grid, total, hits, digit_hits