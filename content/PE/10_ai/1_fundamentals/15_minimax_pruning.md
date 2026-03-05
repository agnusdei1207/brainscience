+++
title = "미니맥스 알고리즘 (Minimax) & 알파-베타 가지치기"
date = "2026-03-05"
[extra]
categories = "studynotes-ai"
+++

# 미니맥스 알고리즘 (Minimax) & 알파-베타 가지치기 (Alpha-Beta Pruning)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 미니맥스는 2인 제로섬 게임(체스, 바둑, 틱택토 등)에서 플레이어가 자신의 이익을 최대화(MAX)하고 상대의 이익을 최소화(MIN)한다고 가정하여 게임 트리를 탐색하는 최적 전략 알고리즘이다.
> 2. **가치**: 완전한 게임 트리 탐색 시 최적의 수를 보장하며, 알파-베타 가지치기를 적용하면 탐색 노드 수를 최대 50%까지 감소시켜 더 깊은 수를 미리 계산할 수 있다.
> 3. **융합**: 체스 엔진(Deep Blue), 오델로, 체커스 등에서 핵심 알고리즘으로 활용되며, 현대에는 MCTS, 딥러닝(AlphaZero)과 결합하여 더 강력한 게임 AI를 구현한다.

---

## I. 개요 (Context & Background)

### 개념 정의

**미니맥스(Minimax) 알고리즘**은 **2인 제로섬 게임(Two-player Zero-sum Game)에서 완벽한 정보 하에 최적의 전략을 찾기 위한 결정론적 알고리즘**이다. 핵심 가정은:
- 두 플레이어가 모두 완벽하게 이성적으로 플레이함
- 한 플레이어의 이익 = 다른 플레이어의 손실 (제로섬)
- MAX 플레이어: 점수 최대화 시도 (내 차례)
- MIN 플레이어: 점수 최소화 시도 (상대 차례)

**알파-베타 가지치기(Alpha-Beta Pruning)**는 **미니맥스 탐색에서 탐색할 필요가 없는 가지를 미리 잘라내어(pruning) 탐색 효율을 높이는 최적화 기법**이다.

### 💡 비유: "완벽한 체스 플레이어의 생각 과정"

미니맥스를 **"모든 가능성을 완벽하게 계산하는 체스 그랜드마스터"**에 비유할 수 있다.

**상황**: 당신이 체스를 두고 있다. 이제 당신 차례다.

**미니맥스 사고 과정**:
1. "내가 이 말을 여기로 움직이면..."
2. "상대는 그에 대응해서 가장 나를 괴롭히는 수를 둘 거야..."
3. "그러면 나는 또 최선의 수로 대응하고..."
4. "결국 이 수를 두면 5수 뒤에 내가 이기네!"

**MAX (나)**: "내 점수를 최대로 만들자!"
**MIN (상대)**: "상대는 내 점수를 최소로 만들려고 할 거야!"

**알파-베타 가지치기**:
"이미 더 좋은 수를 찾았는데, 지금 검토하는 수는 최악의 경우가 너무 나빠. 더 볼 필요 없어!" → 즉시 가지치기

### 등장 배경 및 발전 과정

#### 1. 게임 이론의 기초

1928년 존 폰 노이만(John von Neumann)이 미니맥스 정리 증명:
- 2인 제로섬 게임에서 항상 최적의 혼합 전략이 존재
- 이것이 게임 이론(Game Theory)의 시초

#### 2. 컴퓨터 게임 AI

- **1950년**: 클로드 섀넌, 체스 프로그래밍 논문 발표
- **1997년**: IBM Deep Blue, 세계 체스 챔피언 카스파로프 격파
- **2016년**: AlphaGo, 이세돌 9단 격파 (MCTS + 딥러닝)

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|----------|------|
| **게임 트리** | 가능한 모든 상태 | 노드=상태, 엣지=수 | Tree | 경우의 수 |
| **평가 함수** | 상태의 가치 | 말 점수, 위치 가치 | f(state) | 점수 계산 |
| **MAX 노드** | 내 차례 | 자식 중 최댓값 선택 | max() | 공격 |
| **MIN 노드** | 상대 차례 | 자식 중 최솟값 선택 | min() | 방어 |
| **알파(α)** | MAX 확정 최솟값 | 하한선 | max score | 최소 보장 |
| **베타(β)** | MIN 확정 최댓값 | 상한선 | min score | 최대 허용 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          미니맥스 게임 트리 구조                                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    틱택토 예시 (X = MAX, O = MIN):

                    ┌─────────────┐
                    │   MAX (X)   │  ← 현재 상태 (X 차례)
                    │   ? ? ?    │
                    │   ? ? ?    │
                    │   ? ? ?    │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────┴────┐       ┌────┴────┐       ┌────┴────┐
    │ MIN (O) │       │ MIN (O) │       │ MIN (O) │  ← O의 응수
    │ X ? ?  │       │ ? X ?  │       │ ? ? X  │
    │ ? ? ?  │       │ ? ? ?  │       │ ? ? ?  │
    │ ? ? ?  │       │ ? ? ?  │       │ ? ? ?  │
    └────┬────┘       └────┬────┘       └────┬────┘
         │                 │                 │
    ┌────┴────┐       ┌────┴────┐       ┌────┴────┐
    │ MAX (X) │       │ MAX (X) │       │ MAX (X) │  ← X의 응수
    │ X O ?  │       │ X ? ?  │       │ ? X O  │
    │ ? ? ?  │       │ ? O ?  │       │ ? ? ?  │
    │ ? ? ?  │       │ ? ? ?  │       │ ? ? ?  │
    └────┬────┘       └────┬────┘       └────┬────┘
         │                 │                 │
        ...               ...               ...

    말단 노드(Leaf): 평가 함수로 점수 계산
    내부 노드: 자식 점수의 max 또는 min

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          미니맥스 값 전파 (Value Backpropagation)                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    Leaf 점수 → 루트로 역전파:

                    ┌─────────────┐
                    │  MAX = 3    │  ← 자식 중 최댓값
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────┴────┐       ┌────┴────┐       ┌────┴────┐
    │ MIN = 3 │       │ MIN = 2 │       │ MIN = 5 │  ← 자식 중 최솟값
    └────┬────┘       └────┬────┘       └────┬────┘
         │                 │                 │
    ┌────┴────┐       ┌────┴────┐       ┌────┴────┐
    │3│5│7│  │       │2│4│8│  │       │5│9│6│  │  ← Leaf 노드 점수
    └─────────┘       └─────────┘       └─────────┘

    최적 수: MIN=3인 왼쪽 가지 선택 (보장된 최솟값이 가장 높음)

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          알파-베타 가지치기 (Alpha-Beta Pruning)                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    α: MAX 노드에서 보장된 최소 점수 (하한)
    β: MIN 노드에서 보장된 최대 점수 (상한)

    가지치기 조건: α ≥ β 이면 탐색 중단

    예시:

                    ┌─────────────┐
                    │  MAX        │  α = -∞, β = +∞
                    │  (루트)     │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────┴────┐       ┌────┴────┐       ┌────┴────┐
    │ MIN     │       │ MIN     │       │ PRUNED! │  ← 탐색 안 함
    │ α=-∞   │       │ α=-∞   │       │         │
    │ β=+∞   │       │ β=3    │       │         │
    └────┬────┘       └────┬────┘       └─────────┘
         │                 │
    ┌────┴────┐       ┌────┴────┐
    │ 3 │ 5 │ │       │ 2 │ ? │ │  ← 2를 보는 순간
    └─────────┘       └─────────┘    β=3이고, 다음 자식이 2보다
    → MIN=3                          클 필요 없음 (가지치기)

    탐색 순서가 중요! 좋은 수부터 탐색하면 더 많이 가지치기
```

### 심층 동작 원리

**① 기본 미니맥스 알고리즘**

```python
from typing import List, Optional, Tuple
from copy import deepcopy

class TicTacToe:
    """틱택토 게임 상태"""

    def __init__(self, board=None, player='X'):
        self.board = board if board else [[' ']*3 for _ in range(3)]
        self.player = player  # 'X' = MAX, 'O' = MIN

    def is_terminal(self) -> bool:
        """게임 종료 여부"""
        return self.winner() is not None or self.is_full()

    def winner(self) -> Optional[str]:
        """승자 반환 ('X', 'O', 'Draw', None)"""
        # 행, 열, 대각선 확인
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]

        if self.is_full():
            return 'Draw'
        return None

    def is_full(self) -> bool:
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3))

    def get_moves(self) -> List[Tuple[int, int]]:
        """가능한 수 반환"""
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']

    def make_move(self, move: Tuple[int, int]) -> 'TicTacToe':
        """수를 두어 새 상태 반환"""
        i, j = move
        new_board = deepcopy(self.board)
        new_board[i][j] = self.player
        next_player = 'O' if self.player == 'X' else 'X'
        return TicTacToe(new_board, next_player)

    def evaluate(self) -> int:
        """평가 함수 (X 기준)"""
        w = self.winner()
        if w == 'X': return 10
        if w == 'O': return -10
        return 0


def minimax(state: TicTacToe, depth: int, is_maximizing: bool) -> int:
    """
    미니맥스 알고리즘

    Args:
        state: 현재 게임 상태
        depth: 탐색 깊이
        is_maximizing: True면 MAX 플레이어, False면 MIN

    Returns:
        최적의 평가 점수
    """
    # 종료 조건
    if state.is_terminal() or depth == 0:
        return state.evaluate()

    if is_maximizing:
        # MAX: 자식 중 최댓값 선택
        max_eval = float('-inf')
        for move in state.get_moves():
            child = state.make_move(move)
            eval_score = minimax(child, depth - 1, False)
            max_eval = max(max_eval, eval_score)
        return max_eval
    else:
        # MIN: 자식 중 최솟값 선택
        min_eval = float('inf')
        for move in state.get_moves():
            child = state.make_move(move)
            eval_score = minimax(child, depth - 1, True)
            min_eval = min(min_eval, eval_score)
        return min_eval


def find_best_move(state: TicTacToe) -> Tuple[int, int]:
    """최적의 수 찾기"""
    best_move = None
    best_value = float('-inf') if state.player == 'X' else float('inf')

    for move in state.get_moves():
        child = state.make_move(move)
        # 다음 플레이어 관점에서 평가
        value = minimax(child, 9, state.player == 'O')

        if state.player == 'X':
            if value > best_value:
                best_value = value
                best_move = move
        else:
            if value < best_value:
                best_value = value
                best_move = move

    return best_move
```

**② 알파-베타 가지치기**

```python
def minimax_alpha_beta(
    state: TicTacToe,
    depth: int,
    alpha: float,
    beta: float,
    is_maximizing: bool
) -> int:
    """
    알파-베타 가지치기를 적용한 미니맥스

    Args:
        alpha: MAX가 보장받는 최소 점수 (하한)
        beta: MIN이 허용하는 최대 점수 (상한)

    Returns:
        최적의 평가 점수
    """
    # 종료 조건
    if state.is_terminal() or depth == 0:
        return state.evaluate()

    if is_maximizing:
        max_eval = float('-inf')
        for move in state.get_moves():
            child = state.make_move(move)
            eval_score = minimax_alpha_beta(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval_score)

            # 알파 갱신
            alpha = max(alpha, eval_score)

            # 가지치기: 알파 >= 베타이면 더 볼 필요 없음
            if beta <= alpha:
                break  # β-cut

        return max_eval
    else:
        min_eval = float('inf')
        for move in state.get_moves():
            child = state.make_move(move)
            eval_score = minimax_alpha_beta(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval_score)

            # 베타 갱신
            beta = min(beta, eval_score)

            # 가지치기
            if beta <= alpha:
                break  # α-cut

        return min_eval


def find_best_move_ab(state: TicTacToe) -> Tuple[int, int]:
    """알파-베타를 사용한 최적 수 찾기"""
    best_move = None

    if state.player == 'X':
        best_value = float('-inf')
        alpha, beta = float('-inf'), float('inf')

        for move in state.get_moves():
            child = state.make_move(move)
            value = minimax_alpha_beta(child, 9, alpha, beta, True)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, value)
    else:
        best_value = float('inf')
        alpha, beta = float('-inf'), float('inf')

        for move in state.get_moves():
            child = state.make_move(move)
            value = minimax_alpha_beta(child, 9, alpha, beta, False)
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, value)

    return best_move
```

**③ 성능 비교**

```python
# 노드 수 카운트
node_count = 0

def minimax_with_count(state, depth, is_max):
    global node_count
    node_count += 1

    if state.is_terminal() or depth == 0:
        return state.evaluate()

    if is_max:
        return max(minimax_with_count(state.make_move(m), depth-1, False)
                   for m in state.get_moves())
    else:
        return min(minimax_with_count(state.make_move(m), depth-1, True)
                   for m in state.get_moves())

def minimax_ab_with_count(state, depth, alpha, beta, is_max):
    global node_count
    node_count += 1

    if state.is_terminal() or depth == 0:
        return state.evaluate()

    if is_max:
        value = float('-inf')
        for m in state.get_moves():
            value = max(value, minimax_ab_with_count(state.make_move(m), depth-1, alpha, beta, False))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value
    else:
        value = float('inf')
        for m in state.get_moves():
            value = min(value, minimax_ab_with_count(state.make_move(m), depth-1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

# 결과 (빈 보드에서 depth 6):
# 기본 미니맥스: ~500,000 노드
# 알파-베타: ~20,000 노드 (96% 감소!)
```

---

## III. 융합 비교 및 다각도 분석

### 미니맥스 변종 비교

| 알고리즘 | 특징 | 탐색 노드 | 용도 |
|---------|------|----------|------|
| **기본 Minimax** | 완전 탐색 | O(b^d) | 작은 게임 |
| **Alpha-Beta** | 가지치기 | O(b^(d/2)) ~ O(b^d) | 범용 |
| **Negamax** | 코드 단순화 | 동일 | 구현 편의 |
| **NegaScout** | null-window 탐색 | 더 적음 | 체스 |
| **MTD(f)** | Memory-enhanced | 더 적음 | 최적화 |

### 과목 융합 관점

#### 미니맥스 × 알고리즘

- **동적 계획법**: Transposition Table로 중복 계산 방지
- **메모이제이션**: 이미 계산된 상태 저장

#### 미니맥스 × 머신러닝

- **평가 함수 학습**: 신경망으로 f(state) 학습
- **AlphaZero**: 뉴럴 네트워크 + MCTS로 미니맥스 대체

---

## IV. 실무 적용 및 기술사적 판단

### 실무 시나리오

#### 시나리오 1: 체스 엔진

**전략**:
1. **Iterative Deepening**: 시간 내 최대 깊이
2. **Transposition Table**: 중복 상태 캐시
3. **휴리스틱 평가**: 말 가치 + 위치 가치
4. **결과**: 초당 수백만 노드 탐색

#### 시나리오 2: 실시간 게임 AI

**전략**:
1. **깊이 제한**: 시간 예산 내 탐색
2. **퀴어센스 탐색**: 불안정 상태 심층 탐색
3. **결과**: 60 FPS 유지, 자연스러운 플레이

### 안티패턴

1. **지나친 깊이**: 시간 초과
2. **평가 함수 편향**: 특정 상황에 취약
3. **수순 무시**: 좋은 수부터 탐색 안 함

---

## V. 기대효과 및 결론

### 정량적 효과

| 기법 | 탐색 노드 | 상대적 효율 |
|------|----------|-----------|
| 기본 Minimax | 1,000,000 | 1x |
| Alpha-Beta (평균) | 100,000 | 10x |
| Alpha-Beta (최적 순서) | 31,623 | 31.6x |
| + Transposition Table | 10,000 | 100x |

### 미래 전망

1. **딥러닝 평가**: 신경망 기반 평가 함수
2. **AlphaZero 방식**: 미니맥스 없이 MCTS + RL
3. **실시간 적응**: 상대 플레이 스타일 학습

---

## 👶 어린이를 위한 3줄 비유

**1. 미니맥스는 체스 둘 때 "상대는 똑똑할 거야"라고 가정하는 거예요.** "내가 이 수를 두면, 상대는 가장 나를 괴롭히는 수로 대응할 거야. 그러면 나는 또 최선으로 대응하고..."

**2. 알파-베타 가지치기는 "이미 더 좋은 수를 찾았으면 더 볼 필요 없어!"하는 거예요.** 이미 이길 수 있는 수를 발견했는데, 다른 수가 얼마나 나쁜지 굳이 확인할 필요 없겠죠?

**3. 이렇게 컴퓨터는 수십, 수백 수 앞을 내다봐요.** 우리가 "음, 이게 좋아 보이네" 하고 두는 것과 달리, 컴퓨터는 모든 가능성을 완벽하게 계산해요. 그래서 체스 챔피언도 이기는 거랍니다!
