def find_valid_rectangles(board):
    h, w = len(board), len(board[0])
    best = None
    for r1 in range(h):
        for r2 in range(r1+1, h+1):
            for c1 in range(w):
                for c2 in range(c1+1, w+1):
                    flat = [board[r][c] for r in range(r1, r2) for c in range(c1, c2)]
                    if 0 in flat or sum(flat) != 10:
                        continue
                    area = (r2 - r1) * (c2 - c1)
                    if best is None or area < best[1]:
                        best = ((r1, c1, r2, c2), area)
    return best[0] if best else None