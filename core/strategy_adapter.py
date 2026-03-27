import random
import time
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from typing import List

from config import MAX_SIMULATION_TIME

try:
    import fruit_box_bot
    HAS_EXT = True
except Exception:
    HAS_EXT = False


class BoxSel:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Strategy:
    def __init__(self, boxes: List[BoxSel], score: int):
        self.boxes = boxes
        self.score = score


def _simulation_worker(original_board: List[List[int]], max_time: float, seed_val: int):
    random.seed(seed_val)
    h, w = len(original_board), len(original_board[0])
    best_strategy = Strategy([], -1)

    start_time = time.time()
    iteration_count = 0

    while True:
        if time.time() - start_time >= max_time:
            break

        iteration_count += 1
        board = [row[:] for row in original_board]
        boxes = []
        score = 0  # 💡 여기서 score는 '없앤 사과의 총개수'를 의미하게 됩니다.

        while True:
            valid_rects = []
            for r1 in range(h):
                for r2 in range(r1 + 1, h + 1):
                    for c1 in range(w):
                        current_sum = 0
                        for c2 in range(c1 + 1, w + 1):
                            for r in range(r1, r2):
                                current_sum += board[r][c2 - 1]

                            if current_sum == 10:
                                area = (r2 - r1) * (c2 - c1)
                                valid_rects.append((area, r1, c1, r2, c2))
                            elif current_sum > 10:
                                break

            if not valid_rects:
                break

            valid_rects.sort(key=lambda x: x[0])

            if iteration_count == 1:
                chosen = valid_rects[0]
            else:
                top_n = min(4, len(valid_rects))
                chosen = random.choice(valid_rects[:top_n])

            area, r1, c1, r2, c2 = chosen
            boxes.append(BoxSel(c1, r1, c2 - c1, r2 - r1))

            # 💡 수정된 부분: 드래그한 상자 안의 실제 사과 개수를 세고 지웁니다.
            removed_apples = 0
            for rr in range(r1, r2):
                for cc in range(c1, c2):
                    if board[rr][cc] > 0:
                        removed_apples += 1
                    board[rr][cc] = 0

            # 실제 없앤 사과 개수를 점수(score)로 더합니다.
            score += removed_apples

        # 이 우주에서 없앤 총 사과 개수가 기존 최고 기록보다 많으면 갱신!
        if score > best_strategy.score:
            best_strategy = Strategy(boxes, score)

    return best_strategy, iteration_count


def _multicore_ultimate_strategy(original_board: List[List[int]], max_time: float = MAX_SIMULATION_TIME) -> Strategy:
    cores = multiprocessing.cpu_count()
    print(f"🔥 {cores}개의 CPU 코어를 100% 풀가동하여 {max_time}초 동안 초병렬 탐색을 시작합니다!")

    start_total = time.time()
    best_overall_strategy = Strategy([], -1)
    total_iterations = 0

    with ProcessPoolExecutor(max_workers=cores) as executor:
        futures = []
        for i in range(cores):
            futures.append(executor.submit(_simulation_worker, original_board, max_time, int(time.time() * 1000) + i))

        for future in futures:
            strategy, iters = future.result()
            total_iterations += iters
            if strategy.score > best_overall_strategy.score:
                best_overall_strategy = strategy

    elapsed = time.time() - start_total
    print(f"✅ 연산 완료! ({elapsed:.2f}초 동안 총 {total_iterations}판 가상 플레이)")
    print(f"🏆 가장 완벽한 루트 발견: [사과 {best_overall_strategy.score}개 제거 / {len(best_overall_strategy.boxes)}회 드래그]")
    return best_overall_strategy


def find_strategy(board: List[List[int]]):
    if HAS_EXT:
        return fruit_box_bot.find_strategy(board)
    else:
        return _multicore_ultimate_strategy([row[:] for row in board])