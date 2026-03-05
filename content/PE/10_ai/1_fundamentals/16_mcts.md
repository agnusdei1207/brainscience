+++
title = "몬테카를로 트리 탐색 (MCTS, Monte Carlo Tree Search)"
date = "2026-03-05"
[extra]
categories = "studynotes-ai"
+++

# 몬테카를로 트리 탐색 (MCTS, Monte Carlo Tree Search)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MCTS는 무작위 시뮬레이션(롤아웃)을 통해 게임 트리를 점진적으로 구축하는 휴리스틱 탐색 알고리즘으로, 선택(Selection) → 확장(Expansion) → 시뮬레이션(Simulation) → 역전파(Backpropagation)의 4단계를 반복하며 최적의 수를 찾는다.
> 2. **가치**: 상태 공간이 방대한 게임(바둑: 10^170)에서 완전 탐색 대신 통계적 샘플링으로 근사 최적해를 찾으며, AlphaGo가 이세돌 9단을 격파한 핵심 기술이다.
> 3. **융합**: UCT(Upper Confidence Bound) 밴딧 알고리즘, 신경망 평가(AlphaZero), 가치/정책 네트워크와 결합하여 바둑, 체스, 장기, 비디오 게임, 조합 최적화 등 다양한 분야에서 활용된다.

---

## I. 개요 (Context & Background)

### 개념 정의

몬테카를로 트리 탐색(Monte Carlo Tree Search, MCTS)은 **무작위 샘플링(몬테카를로 방법)을 기반으로 게임 트리를 점진적으로 구축하고 탐색하는 알고리즘**으로, 다음 4단계를 반복한다:

1. **선택(Selection)**: 루트에서 시작하여 UCT 등의 기준으로 자식 선택, 리프 노드까지 하강
2. **확장(Expansion)**: 리프 노드에서 하나 이상의 자식 노드 추가
3. **시뮬레이션(Simulation/Playout)**: 새 노드에서 무작위 플레이로 게임 종료까지 진행
4. **역전파(Backpropagation)**: 시뮬레이션 결과를 경로상의 모든 노드에 전파

### 💡 비유: "경험 많은 바둑 기사의 직관"

MCTS를 **"수만 번의 대국 경험을 가진 기사가 직관으로 수를 읽는 방식"**에 비유할 수 있다.

**전통적 미니맥스**: "이 수를 두면 상대는 이렇게 응수하고, 그러면 나는 이렇게... (모든 경우의 수 계산)"

**MCTS 방식**:
1. "지금까지 경험상 이 쪽이 승률이 높았어" (선택)
2. "아직 안 가본 길인데 한번 시도해보자" (확장)
3. "빠르게 끝까지 진행해보니까 이길 것 같아" (시뮬레이션)
4. "기억해두자, 이 길은 승률이 70%네" (역전파)

**핵심 차이**: 모든 경우의 수를 완벽히 계산하는 게 아니라, "경험(시뮬레이션)"을 통해 통계적으로 좋은 수를 찾는다.

### 등장 배경 및 발전 과정

#### 1. 미니맥스의 한계

```
바둑의 상태 공간:
- 가능한 바둑판 상태: 약 10^170개
- 우주의 원자 수: 약 10^80개
- 완전 탐색: 불가능

체스의 상태 공간:
- 약 10^120개
- Deep Blue는 미니맥스 + 알파-베타로 12수 앞 탐색
- 바둑은 12수로 터무니없이 부족
```

#### 2. MCTS의 등장

- **2006년**: Rémi Coulom, "Efficient Selectivity and Backup Operators in Monte-Carlo Tree Search"
- **2006년**: Kocsis & Szepesvári, UCT 알고리즘 제안
- **2016년**: AlphaGo, MCTS + 딥러닝으로 이세돌 9단 격파

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|----------|------|
| **노드** | 게임 상태 | 상태, 방문 횟수, 승리 횟수 | (s, N, W) | 바둑판 |
| **선택** | 탐색 경로 결정 | UCT = W/N + c√(ln Np/N) | Bandit | 방향 선택 |
| **확장** | 새 노드 생성 | 미탐색 자식 추가 | Expand | 새 길 |
| **시뮬레이션** | 무작위 플레이 | 랜덤 수로 종료까지 | Playout | 빠른 대국 |
| **역전파** | 결과 전파 | 승/패 카운트 갱신 | Update | 경험 축적 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          MCTS 4단계 프로세스                                              │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    [1] 선택 (Selection)              [2] 확장 (Expansion)

         Root                             Root
        /    \                           /    \
      [3/5]  [2/3]                     [3/5]  [2/3]
       ↑        \                       |       |
    UCT 최대    ...                  Selected   ...
    자식 선택                         노드
       │                               │
       ▼                               ▼
    ┌──────┐                      ┌──────┐
    │ Leaf │                      │ Leaf │──▶ [0/0] (새 노드 추가)
    │ 노드  │                      │ 노드  │
    └──────┘                      └──────┘

    [3] 시뮬레이션 (Simulation)        [4] 역전파 (Backpropagation)

    무작위 플레이                      결과 전파
    ┌─────────────────┐               ┌─────────────────┐
    │ R → B → W → ... │               │                 │
    │     ↓           │               │    [4/6]        │
    │   승/패 결정     │               │   /     \       │
    │     ↓           │      ───▶     │ [3/5]  [1/4]    │
    │   결과: 승리    │               │   |             │
    └─────────────────┘               │ [1/1] (갱신)    │
                                      └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                          UCT (Upper Confidence Bound) 공식                                 │
└─────────────────────────────────────────────────────────────────────────────────────────┘

    UCT(s, a) = Q(s,a)/N(s,a) + c × √(ln N(s) / N(s,a))

    where:
    - Q(s,a): 상태 s에서 행동 a의 누적 보상
    - N(s,a): 상태 s에서 행동 a의 방문 횟수
    - N(s): 상태 s의 총 방문 횟수
    - c: 탐색 상수 (보통 √2 ≈ 1.414)

    첫 번째 항: Exploitation (이익 극대화)
    - 많이 방문하고 승률이 높은 노드 선호

    두 번째 항: Exploration (미지 탐색)
    - 적게 방문한 노드 선호 (불확실성 해소)

    트레이드오프: Exploitation vs Exploration

    ┌────────────────────────────────────────────────────────────────────────────────────┐
    │  노드    │  승/방문  │  승률   │  UCT (c=1.4, 부모=100) │  선택 우선순위        │
    ├────────────────────────────────────────────────────────────────────────────────────┤
    │  A      │  60/80   │  0.75   │  0.75 + 0.35 = 1.10   │  2위                 │
    │  B      │  10/12   │  0.83   │  0.83 + 0.91 = 1.74   │  1위 (높은 불확실성) │
    │  C      │  5/8     │  0.625  │  0.625 + 1.14 = 1.77  │  최고 (더 탐색 필요) │
    └────────────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

**① 기본 MCTS 구현**

```python
import math
import random
from typing import List, Optional, Tuple
from copy import deepcopy
from dataclasses import dataclass, field

@dataclass
class MCTSNode:
    """MCTS 노드"""
    state: any
    parent: Optional['MCTSNode'] = None
    children: List['MCTSNode'] = field(default_factory=list)
    visits: int = 0
    wins: float = 0.0
    untried_moves: List = field(default_factory=list)

    def uct_value(self, c: float = 1.414) -> float:
        """UCT 값 계산"""
        if self.visits == 0:
            return float('inf')

        exploitation = self.wins / self.visits
        exploration = c * math.sqrt(math.log(self.parent.visits) / self.visits)
        return exploitation + exploration

    def best_child(self, c: float = 1.414) -> 'MCTSNode':
        """UCT 값이 가장 높은 자식 선택"""
        return max(self.children, key=lambda child: child.uct_value(c))

    def most_visited_child(self) -> 'MCTSNode':
        """가장 많이 방문한 자식 (최종 선택용)"""
        return max(self.children, key=lambda child: child.visits)


class MCTS:
    """몬테카를로 트리 탐색"""

    def __init__(
        self,
        initial_state,
        get_legal_moves,
        make_move,
        is_terminal,
        get_result,
        exploration_weight: float = 1.414
    ):
        """
        Args:
            initial_state: 초기 게임 상태
            get_legal_moves: state -> 가능한 수 리스트
            make_move: (state, move) -> 새 상태
            is_terminal: state -> 게임 종료 여부
            get_result: state -> 결과 (1=승, 0=패, 0.5=무승부)
            exploration_weight: UCT 탐색 상수 c
        """
        self.root = MCTSNode(
            state=initial_state,
            untried_moves=get_legal_moves(initial_state)
        )
        self.get_legal_moves = get_legal_moves
        self.make_move = make_move
        self.is_terminal = is_terminal
        self.get_result = get_result
        self.c = exploration_weight

    def select(self) -> MCTSNode:
        """Selection: UCT 기반으로 리프 노드까지 하강"""
        node = self.root

        while node.children:
            # 모든 자식이 확장되었으면 UCT로 선택
            if not node.untried_moves:
                node = node.best_child(self.c)
            else:
                # 아직 확장 안 된 자식이 있으면 중단
                break

        return node

    def expand(self, node: MCTSNode) -> MCTSNode:
        """Expansion: 새 자식 노드 추가"""
        if not node.untried_moves:
            return node

        # 무작위 미시도 수 선택
        move = random.choice(node.untried_moves)
        node.untried_moves.remove(move)

        # 새 상태 생성
        new_state = self.make_move(node.state, move)
        child = MCTSNode(
            state=new_state,
            parent=node,
            untried_moves=self.get_legal_moves(new_state)
        )
        node.children.append(child)

        return child

    def simulate(self, node: MCTSNode) -> float:
        """Simulation: 무작위 플레이로 결과 획득"""
        state = node.state
        player = self._get_current_player(state)

        while not self.is_terminal(state):
            moves = self.get_legal_moves(state)
            if not moves:
                break
            move = random.choice(moves)
            state = self.make_move(state, move)

        return self.get_result(state, player)

    def backpropagate(self, node: MCTSNode, result: float):
        """Backpropagation: 결과를 루트까지 전파"""
        while node:
            node.visits += 1
            node.wins += result
            result = 1 - result  # 상대방 관점으로 전환
            node = node.parent

    def run_iteration(self):
        """한 번의 MCTS 반복 수행"""
        # 1. Selection
        node = self.select()

        # 2. Expansion (종료 상태가 아니면)
        if not self.is_terminal(node.state) and node.untried_moves:
            node = self.expand(node)

        # 3. Simulation
        result = self.simulate(node)

        # 4. Backpropagation
        self.backpropagate(node, result)

    def get_best_move(self, num_iterations: int = 1000):
        """최적의 수 반환"""
        for _ in range(num_iterations):
            self.run_iteration()

        return self.root.most_visited_child()

    def _get_current_player(self, state):
        """현재 플레이어 반환 (게임별 구현 필요)"""
        # 간단히 상태에서 추출 (실제로는 게임에 따라 다름)
        return getattr(state, 'current_player', 1)


# 틱택토 예시
class TicTacToeState:
    def __init__(self, board=None, player=1):
        self.board = board if board else [[0]*3 for _ in range(3)]
        self.current_player = player

    def get_winner(self):
        # 행, 열, 대각선 확인
        for i in range(3):
            if abs(sum(self.board[i])) == 3:
                return sum(self.board[i]) // 3
            if abs(sum(self.board[j][i] for j in range(3))) == 3:
                return self.board[0][i] // abs(self.board[0][i]) if self.board[0][i] else 0

        if abs(self.board[0][0] + self.board[1][1] + self.board[2][2]) == 3:
            return self.board[1][1]
        if abs(self.board[0][2] + self.board[1][1] + self.board[2][0]) == 3:
            return self.board[1][1]

        return 0

    def is_full(self):
        return all(self.board[i][j] != 0 for i in range(3) for j in range(3))


def tic_tac_toe_mcts():
    """틱택토 MCTS 예시"""

    def get_legal_moves(state):
        return [(i, j) for i in range(3) for j in range(3) if state.board[i][j] == 0]

    def make_move(state, move):
        i, j = move
        new_board = [row[:] for row in state.board]
        new_board[i][j] = state.current_player
        return TicTacToeState(new_board, -state.current_player)

    def is_terminal(state):
        return state.get_winner() != 0 or state.is_full()

    def get_result(state, player):
        winner = state.get_winner()
        if winner == player:
            return 1.0
        elif winner == -player:
            return 0.0
        else:
            return 0.5

    initial_state = TicTacToeState()
    mcts = MCTS(initial_state, get_legal_moves, make_move, is_terminal, get_result)

    best_child = mcts.get_best_move(1000)
    print(f"최적의 수: {best_child.state.board}")
    print(f"방문 횟수: {best_child.visits}")
```

**② AlphaZero 스타일 MCTS**

```python
class AlphaZeroMCTS:
    """AlphaZero 스타일 MCTS (신경망 기반)"""

    def __init__(
        self,
        model,  # 정책-가치 네트워크
        initial_state,
        get_legal_moves,
        make_move,
        is_terminal,
        num_simulations: int = 800,
        c_puct: float = 1.0
    ):
        self.model = model
        self.root = self._create_node(initial_state, get_legal_moves(initial_state))
        self.get_legal_moves = get_legal_moves
        self.make_move = make_move
        self.is_terminal = is_terminal
        self.num_simulations = num_simulations
        self.c_puct = c_puct

    def _create_node(self, state, legal_moves):
        """노드 생성 및 신경망 평가"""
        # 신경망에서 정책과 가치 예측
        policy, value = self.model.predict(state)

        # 유효한 수만 필터링
        masked_policy = {move: policy[move] for move in legal_moves}

        return {
            'state': state,
            'prior': masked_policy,
            'visit_count': {},
            'total_value': {},
            'children': {}
        }

    def puct_value(self, node, move):
        """PUCT (Predictor + UCT) 값"""
        q = node['total_value'].get(move, 0) / max(node['visit_count'].get(move, 1), 1)
        p = node['prior'][move]
        n = node['visit_count'].get(move, 0)
        total_n = sum(node['visit_count'].values()) + 1

        u = self.c_puct * p * math.sqrt(total_n) / (1 + n)
        return q + u

    def search(self):
        """MCTS 탐색 수행"""
        for _ in range(self.num_simulations):
            self._simulate(self.root)

        # 방문 횟수 기반 정책 반환
        visits = self.root['visit_count']
        total = sum(visits.values())
        policy = {move: count/total for move, count in visits.items()}

        return policy

    def _simulate(self, node):
        """시뮬레이션 (재귀)"""
        state = node['state']

        # 종료 확인
        if self.is_terminal(state):
            return self._get_result(state)

        # 리프 노드면 신경망 평가
        if not node['children']:
            _, value = self.model.predict(state)
            return -value

        # PUCT로 자식 선택
        best_move = max(
            node['prior'].keys(),
            key=lambda m: self.puct_value(node, m)
        )

        # 자식이 없으면 생성
        if best_move not in node['children']:
            new_state = self.make_move(state, best_move)
            node['children'][best_move] = self._create_node(
                new_state,
                self.get_legal_moves(new_state)
            )

        # 재귀 시뮬레이션
        value = self._simulate(node['children'][best_move])

        # 역전파
        node['visit_count'][best_move] = node['visit_count'].get(best_move, 0) + 1
        node['total_value'][best_move] = node['total_value'].get(best_move, 0) + value

        return -value  # 상대방 관점으로 반환
```

---

## III. 융합 비교 및 다각도 분석

### MCTS vs 다른 탐색 알고리즘

| 알고리즘 | 특징 | 적용 분야 |
|---------|------|----------|
| **Minimax** | 완전 탐색 | 작은 게임 |
| **Alpha-Beta** | 가지치기 | 중간 크기 게임 |
| **MCTS** | 통계적 샘플링 | 대규모 게임 |
| **AlphaZero** | MCTS + 신경망 | 모든 완전 정보 게임 |

### UCT 변종 비교

| 변종 | 탐색 상수 | 특징 |
|------|----------|------|
| **기본 UCT** | c = √2 | Kocsis & Szepesvári |
| **UCB1-Tuned** | 적응적 | 분산 고려 |
| **PUCT** | c_puct | AlphaZero |
| **Bayesian UCT** | 베이지안 | 불확실성 모델링 |

### 과목 융합 관점

#### MCTS × 머신러닝

- **정책 네트워크**: 수 선택 확률 학습
- **가치 네트워크**: 상태 가치 평가
- **자가 대국**: Self-play로 강화학습

#### MCTS × 최적화

- **조합 최적화**: TSP, 스케줄링
- **Hyperparameter**: NAS (Neural Architecture Search)

---

## IV. 실무 적용 및 기술사적 판단

### 실무 시나리오

#### 시나리오 1: 바둑 AI

**전략**:
1. **정책 네트워크**: 361개 착점 확률
2. **가치 네트워크**: 승률 예측
3. **MCTS 1600회**: 최적 수 선택
4. **결과**: 프로 9단 수준

#### 시나리오 2: 비디오 게임 AI

**전략**:
1. **전방 모델**: 게임 상태 예측
2. **MCTS**: 최적 행동 탐색
3. **실시간**: 50ms 예산
4. **결과**: 인간 수준 플레이

### 안티패턴

1. **시뮬레이션 편향**: 나쁜 무작위 플레이
2. **과소 탐색**: 불충분한 시뮬레이션
3. **신경망 오류**: 편향된 평가

---

## V. 기대효과 및 결론

### 장단점

| 장점 | 단점 |
|------|------|
| 대규모 상태 공간 | 시간 소요 |
| 도메인 독립적 | 시뮬레이션 품질 중요 |
| 점진적 개선 | 결정론적 아님 |
| 신경망 결합 가능 | 구현 복잡 |

### 미래 전망

1. **Sample-Efficient MCTS**: 더 적은 시뮬레이션
2. **멀티 에이전트**: 다중 플레이어 게임
3. **실시간 최적화**: 동적 환경 대응

---

## 👶 어린이를 위한 3줄 비유

**1. MCTS는 "빠르게 가상 대국을 많이 해보는 거예요."** "이 수를 두면 어떻게 될까?" 하고 머리로 빠르게 게임을 끝까지 진행해봐요. 마치 머릿속에서 천 번을 둬보는 거죠.

**2. 경험을 쌓으면서 더 똑똑해져요.** "이쪽으로 두면 70번 중 50번 이겼어. 저쪽은 30번 중 10번만 이겼고. 그럼 이쪽이 더 좋은 수네!" 하고 통계를 내요.

**3. 이게 알파고가 이세돌 9단을 이긴 비밀이에요!** 컴퓨터가 인간보다 훨씬 빠르게 수만 번을 시뮬레이션하면서 최고의 수를 찾아낸 거예요. 인간은 한 수 한 수 깊게 생각하지만, 알파고는 엄청나게 많은 경우를 빠르게 시도해봐요!
