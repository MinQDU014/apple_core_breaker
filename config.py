# ✅ Fruit Box 실제 보드는 가로 17, 세로 10 입니다.
GRID_WIDTH = 17    # columns
GRID_HEIGHT = 10   # rows

CONF_START = 0.95
CONF_FLOOR = 0.75
CONF_STEP = 0.02
SCALES = [1.00, 0.98, 1.02, 0.96, 1.04, 0.94, 1.06]
DEBUG_DIR = "debug"

# ==========================================
# ⚙️ 자동화 봇 통합 설정 (Configuration)
# ==========================================

# 1. 마우스 조작 속도 (GLOBAL_SPEED)
# 1.0 = 기본 속도
# 1.5 = 사람과 비슷한 여유로운 속도
# 0.3 = 안정적인 최고 속도
GLOBAL_SPEED = 0.3

# 2. AI 병렬 연산 제한 시간 (단위: 초)
# 시간이 길수록 수백 판을 더 플레이하여 완벽한 점수를 찾지만 대기 시간이 길어집니다.
MAX_SIMULATION_TIME = 5.0