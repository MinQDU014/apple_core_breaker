# FruitBox Hybrid Bot (Corner-to-Corner Calibration)

# 🍎 Fruit Box (사과 게임) AI Auto-Solver

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Vision-green?logo=opencv&logoColor=white)
![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-Automation-yellow)
![Multiprocessing](https://img.shields.io/badge/Multiprocessing-Optimization-red)

## 📖 프로젝트 개요
**Fruit Box(사과 게임)**는 보드 상의 숫자(1~9)들을 드래그하여 합이 10이 되도록 묶어 화면을 비우는 웹 브라우저 기반 퍼즐 게임입니다.

본 프로젝트는 이 게임을 완벽하게 클리어하고 최고점을 달성하는 **인공지능(AI) 자동화 봇**입니다. 단순한 화면 클릭 매크로를 넘어, **컴퓨터 비전(Vision), 인간-컴퓨터 상호작용(HCI), 알고리즘의 최적화, 그리고 병렬 처리(Multiprocessing)**까지 컴퓨터 공학의 핵심 개념들을 종합적으로 적용하여 문제를 해결한 포트폴리오 프로젝트입니다.

![2026-03-27093623-ezgif com-speed](https://github.com/user-attachments/assets/79bd1445-36e8-498e-83fc-fb54859f7fa5)

---

## 🛠️ 기술 스택 (Tech Stack)
- **Language:** Python
- **Computer Vision:** `mss` (초고속 화면 캡처), `OpenCV` (이미지 처리 및 템플릿 매칭, `numpy` 연동)
- **Automation & HCI:** `pyautogui`, `pynput`, `math`, `random`
- **Performance Optimization:** `multiprocessing`, `concurrent.futures`

---

## 🎯 핵심 구현 기능 및 문제 해결 과정 (Problem-Solving)

### Part 1. 컴퓨터의 눈과 손 (Vision & HCI)

AI가 게임 환경을 정확히 인식하고, 안티 치트(Anti-Cheat) 시스템에 적발되지 않도록 사람처럼 자연스럽게 움직이는 모듈을 구현했습니다.

#### 1. Vision: 화면 인식과 Template Matching
- 1~9까지의 사과 이미지를 템플릿으로 구축하고, OpenCV의 **템플릿 매칭(`cv2.matchTemplate`)** 기법을 사용하여 픽셀 배열이 가장 유사한 좌표를 동적으로 추출합니다.
- **Troubleshooting:**
  - `cv2.imread`의 한글 경로 로드 에러를 `numpy` 배열 디코딩(`cv2.imdecode`)으로 우회하여 해결했습니다.
  - 다양한 모니터 해상도 및 브라우저 스케일링에 대응하기 위해, 유저가 `F3`, `F4` 키로 보드의 양 끝을 클릭하면 셀 크기(Cell Size)와 보드 영역을 자동 역산하는 캘리브레이션 기능을 구현했습니다.

#### 2. HCI: 인간 모방 행동 패턴 (Human-like Interaction)
단순 직선 궤적의 기계적 움직임은 클릭 누락 버그를 유발하고 매크로 탐지에 취약합니다. 이를 해결하기 위해 인간의 행동 패턴을 수학적으로 모델링했습니다.
- **피츠의 법칙 (Fitts's Law):** 목표물까지의 이동 거리에 비례하여 마우스 도달 시간이 늘어나는 동적 딜레이 산출.
- **가속 및 감속 (Easing/Tweening):** 베지어 곡선(Bezier Curve) 기반 함수를 적용하여 출발 시 가속, 도착 시 감속하는 자연스러운 궤적 구현.
- **정규 분포 딜레이 (Gaussian Distribution):** 평균 0.03초를 기준으로 미세한 편차(Variance)를 갖는 가우스 분포를 통해 매번 다른 클릭 딜레이 생성.
- **인지 지연 (Thinking Time):** 인간이 다음 타겟을 스캔하는 "고민하는 시간"을 모방하여, 일정 확률(15%)로 0.5초~1.5초간 대기하는 로직 추가.

---

### Part 2. 알고리즘의 진화: 최고점을 향한 여정

동일한 보드에서도 '지우는 순서'에 따라 최종 점수가 크게 달라집니다. AI의 탐색 알고리즘을 고도화한 과정은 다음과 같습니다.

#### 🔴 v1.0: 탐욕 알고리즘 (Greedy Algorithm)
- **로직:** 보드 좌상단부터 탐색하며 합이 10이 되는 조합을 발견 즉시 소모.
- **한계:** 1이나 2 같은 작은 숫자를 초반에 모두 소모하여 후반부에 8, 9가 고립되는 교착 상태(Deadlock) 발생.

#### 🟡 v2.0: 휴리스틱(Heuristics) 기반 최적화
- **로직:** 게임의 도메인 룰을 반영. 이미 지워진 '빈칸(0)'은 무시된다는 점을 이용해, **"가장 좁은 면적의 조합(예: 9+1)을 최우선으로 지워 구멍을 만들고, 후반부에 거대한 드래그를 유도"**하는 가중치 로직 적용.

#### 🟢 v3.0: 몬테카를로 시뮬레이션 (Monte Carlo Simulation)
- **로직:** 탐욕법의 한계를 넘기 위해 마우스를 움직이기 전, 메모리 상에서 수십 판의 가상 게임을 선행 플레이. 매 턴마다 상위 3~4개의 조합 중 하나를 무작위로 선택하며 다양한 미래(평행 우주)를 탐색 후 최고점 루트 채택.

#### 🔵 v4.0: 가지치기 (Pruning) 최적화
- **로직:** 시간 복잡도(Time Complexity) 감소를 위한 최적화. 사각형을 넓히며 연산할 때, **합산 값이 10을 초과하는 순간 즉시 내부 루프를 종료(`break`)**하여 불필요한 연산의 99%를 제거.

#### 🟣 v5.0: 멀티프로세싱 및 타임어택 (최종 릴리즈)
- **로직:** 제한된 시간 내 탐색 공간 극대화. `ProcessPoolExecutor`를 활용해 시스템의 모든 CPU 코어를 100% 풀가동.
- **결과:** 22초의 제한 시간 동안 각 코어가 독립적인 시드(Seed)를 기반으로 수천 판의 가상 플레이를 병렬 수행하여 절대적인 최적 루트(최고점)를 도출. GPU 대신 분기문(`if`, `break`) 연산에 강한 CPU 멀티코어를 전략적으로 선택.

---

## 💻 설치 및 사용 방법 (Usage)

### 1. 요구 사항 (Prerequisites)
- Python 3.8 이상
- Tesseract OCR (선택 사항 - 숫자 인식 고도화 시 필요)

### 2. 패키지 설치
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
# 주요 패키지: opencv-python, pyautogui, pynput, mss, numpy
```

루트에 `images/` 폴더 생성 후, 1번 사과 부터 9번 까지 사진을 캡쳐해 (배경제외 숫자만) `apple1.png`~`apple9.png` 복사.
브라우저 줌은 100% 권장.

## 사용법

https://apple.oshizi.com/play/1ttsUGBm6VceVG19MU520LNKojPyzsq1BTttKQUIi5QvSSOr-VFG97FzxE9YjBkjvmqnyaUNYItNY2bjFlqkTTqCwF07loH

- F6 : 최상단 최좌측(첫 칸) 중심 클릭
- F7 : 최하단 최우측(마지막 칸) 중심 클릭 → 자동으로 셀 크기(CELL_SIZE)/보드 영역 계산
- F8 : 분석 및 풀이 1회 실행
- F9 / F12 : 🚨 긴급 강제 종료 (언제든지 즉시 멈춤)
- ESC: 종료
```
config.py 안에 GLOBAL_SPEED 를 조절하면 마우스 속도를 조절 할 수 있습니다.
config.py 안의 MAX_SIMULATION_TIME 을 조절 하면 연산 시간을 조절 할 수 있습니다.
```

#### 클릭 후 `debug/capture_region_manual.png` 로 잡힌 영역을 확인하세요.
### 인식 성공 수(hits): 0 으로 나온다면 브라우저 확대와 게임내의 확대를 시도해보고 인식 성공 수를 170이 되도록 조절하세요. 
#### (인식 성공 수는 모니터 해상도, 브라우저 줌, 게임 내 줌에 따라 달라집니다.)

✅ 중요: GRID_WIDTH=17, GRID_HEIGHT=10 으로 고정 (가로 17, 세로 10)

## 🚀 향후 발전 방향 (Future Works)
- 다형성 드래그 알고리즘: 직사각형 형태를 넘어 대각선, 십자형 드래그 룰 추가 시 대응할 수 있는 DFS/BFS 기반 경로 탐색 알고리즘 확장.

- Deep Learning 기반 Vision: 게임의 테마 변경이나 방해물 추가 시에도 견고하게 작동하도록 OpenCV 템플릿 매칭을 YOLO 등 딥러닝 기반 객체 탐지(Object Detection)로 업그레이드.
