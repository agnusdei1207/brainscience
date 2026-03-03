+++
title = "백트래킹 (Backtracking)"
date = 2025-03-02

[extra]
categories = "pe_exam-algorithm_stats"
+++

# 백트래킹 (Backtracking)

## 핵심 인사이트 (3줄 요약)
> **DFS 기반으로 가능한 경우를 탐색하며 실패 시 되돌아가는 알고리즘**. 가지치기(Pruning)로 탐색 공간 축소. N-Queen, 스도쿠, 조합 최적화에 필수.

---

## 📝 기술사 모의답안 (2.5페이지 분량)

### 📌 예상 문제
> **"백트래킹의 원리와 동작 과정을 설명하고, 유사 알고리즘과 비교하여 적합한 활용 시나리오를 기술하시오."**

---

### Ⅰ. 개요

#### 1. 개념
백트래킹(Backtracking)은 **해를 찾는 과정에서 막다른 길에 도달하면 이전 상태로 되돌아가 다른 경로를 탐색하는 알고리즘 기법**이다. 모든 가능한 경우를 체계적으로 탐색하며, 불가능한 경로는 조기에 포기(Pruning)하여 탐색 효율을 높인다.

> 💡 **비유**: "미로 찾기" - 막다른 길을 만나면 분기점으로 돌아와 다른 길을 선택하는 방식

**등장 배경**:
1. **기존 문제점**: 브루트 포스는 모든 경우를 탐색하여 지수 시간 소요
2. **기술적 필요성**: 제약 충족 문제(CSP)에서 불가능한 경로 조기 제거 필요
3. **시장 요구**: 스도쿠, 일정 관리, 자원 배분 등 NP-Complete 문제 해결 수요

**핵심 목적**: 유망하지 않은 경로를 조기에 배제하여 탐색 공간 축소

---

### Ⅱ. 구성 요소 및 핵심 원리

#### 2. 백트래킹 핵심 구성 요소

| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| 상태 공간 (State Space) | 가능한 모든 해의 집합 | 트리 구조로 표현 | 미로의 전체 경로 |
| 선택 (Choose) | 현재 단계에서 가능한 선택지 | 제약 조건 필터링 | 갈림길 선택 |
| 제약 검사 (Constraint Check) | 선택이 유효한지 확인 | O(1) 또는 O(n) | 벽/통로 확인 |
| 목표 검사 (Goal Check) | 완전한 해인지 확인 | 종료 조건 | 출구 도달 |
| 백트랙 (Backtrack) | 실패 시 이전 상태 복구 | 상태 되돌리기 | 분기점으로 복귀 |

#### 3. 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────┐
│               백트래킹 상태 공간 트리                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                         [루트]                              │
│                        /  |  \                              │
│                      A1   A2   A3                           │
│                     /|\   |   /|\                           │
│                   B1 B2 B3  X  B4 B5 B6  ← X: 가지치기      │
│                   |  |  |       |  |  |                     │
│                   C1 C2 C3      C4 C5 C6                    │
│                   ✓  X  ✓      X  ✓  X  ← ✓: 해, X: 실패   │
│                                                             │
│  ✂️ 가지치기 (Pruning):                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  • 유망하지 않은 노드의 자식은 탐색하지 않음         │   │
│  │  • 탐색 공간 대폭 감소                               │   │
│  │  • "promising()" 함수로 판단                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│               N-Queen 예시 (4×4)                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Row 0: [Q][.][.][.]  → Queen 배치 시도                    │
│  Row 1: [.][.][Q][.]  → 제약 검사 (대각선 충돌?)           │
│  Row 2: [.][.][.][.]  → 불가능하면 백트랙                  │
│  Row 3: [.][Q][.][.]  → 다음 위치 시도                     │
│                                                             │
│  제약: 같은 행, 열, 대각선에 다른 퀸 없어야 함              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 4. 동작 원리 단계별 설명

```
① 상태 초기화 → ② 선택 (Choose) → ③ 제약 검사 → ④ 재귀 탐색 → ⑤ 백트랙
```

- **1단계**: 현재 상태에서 가능한 모든 선택지 확인
- **2단계**: 선택지 중 하나를 선택하여 상태 갱신
- **3단계**: 선택이 제약 조건을 만족하는지 검사
- **4단계**: 유망하면 다음 단계로 재귀 호출
- **5단계**: 실패 시 이전 상태로 복구 (상태 되돌리기)

#### 5. Python 코드 예시

```python
from typing import List, Set, Tuple, Optional

# ==================== N-Queen 문제 ====================

def solve_n_queens(n: int) -> List[List[str]]:
    """
    N-Queen 문제 해결

    N×N 체스판에 N개의 퀸을 서로 공격하지 않게 배치

    Args:
        n: 체스판 크기 및 퀸 개수

    Returns:
        모든 유효한 배치 (각 배치는 문자열 리스트)
    """
    def is_safe(board: List[int], row: int, col: int) -> bool:
        """현재 위치에 퀸 배치 가능한지 확인"""
        for prev_row in range(row):
            prev_col = board[prev_row]
            # 같은 열 또는 대각선 충돌 확인
            if (prev_col == col or
                abs(prev_col - col) == row - prev_row):
                return False
        return True

    def backtrack(board: List[int], row: int) -> None:
        """백트래킹으로 퀸 배치"""
        if row == n:  # 모든 행에 배치 완료
            # 결과 변환
            solution = []
            for r in range(n):
                row_str = ['.'] * n
                row_str[board[r]] = 'Q'
                solution.append(''.join(row_str))
            solutions.append(solution)
            return

        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col  # 선택
                backtrack(board, row + 1)  # 재귀
                # board[row] = -1  # 백트랙 (명시적 복구 불필요 - 덮어쓰기)

    solutions = []
    board = [-1] * n  # board[row] = col (퀸의 열 위치)
    backtrack(board, 0)
    return solutions


# ==================== 부분 집합 생성 ====================

def subsets(nums: List[int]) -> List[List[int]]:
    """
    모든 부분 집합 생성 (Power Set)

    시간복잡도: O(2^n × n)
    """
    def backtrack(start: int, path: List[int]) -> None:
        # 현재 부분 집합 추가
        result.append(path[:])

        for i in range(start, len(nums)):
            path.append(nums[i])  # 선택
            backtrack(i + 1, path)  # 다음 인덱스부터
            path.pop()  # 백트랙

    result = []
    backtrack(0, [])
    return result


# ==================== 순열 생성 ====================

def permutations(nums: List[int]) -> List[List[int]]:
    """
    모든 순열 생성

    시간복잡도: O(n! × n)
    """
    def backtrack(path: List[int], used: List[bool]) -> None:
        if len(path) == len(nums):
            result.append(path[:])
            return

        for i in range(len(nums)):
            if used[i]:
                continue

            used[i] = True
            path.append(nums[i])  # 선택

            backtrack(path, used)  # 재귀

            path.pop()  # 백트랙
            used[i] = False

    result = []
    backtrack([], [False] * len(nums))
    return result


# ==================== 조합 생성 ====================

def combinations(n: int, k: int) -> List[List[int]]:
    """
    n개 중 k개를 선택하는 모든 조합

    시간복잡도: O(C(n,k) × k)
    """
    def backtrack(start: int, path: List[int]) -> None:
        if len(path) == k:
            result.append(path[:])
            return

        for i in range(start, n + 1):
            path.append(i)  # 선택
            backtrack(i + 1, path)  # 다음 수부터
            path.pop()  # 백트랙

    result = []
    backtrack(1, [])
    return result


# ==================== 스도쿠 해결 ====================

def solve_sudoku(board: List[List[str]]) -> bool:
    """
    스도쿠 퍼즐 해결 (in-place)

    Args:
        board: 9×9 스도쿠 보드 ('.'은 빈 칸)

    Returns:
        해결 가능 여부
    """
    def is_valid(row: int, col: int, num: str) -> bool:
        """숫자 배치 유효성 검사"""
        # 행 확인
        if num in board[row]:
            return False

        # 열 확인
        if num in [board[r][col] for r in range(9)]:
            return False

        # 3×3 박스 확인
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if board[r][c] == num:
                    return False

        return True

    def find_empty() -> Optional[Tuple[int, int]]:
        """빈 칸 찾기"""
        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    return (r, c)
        return None

    def backtrack() -> bool:
        """백트래킹으로 스도쿠 해결"""
        empty = find_empty()
        if not empty:
            return True  # 모든 칸 채움

        row, col = empty

        for num in map(str, range(1, 10)):
            if is_valid(row, col, num):
                board[row][col] = num  # 선택

                if backtrack():  # 재귀
                    return True

                board[row][col] = '.'  # 백트랙

        return False  # 이 경로로는 해결 불가

    return backtrack()


# ==================== 미로 찾기 ====================

def solve_maze(maze: List[List[int]],
               start: Tuple[int, int],
               end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    미로 경로 찾기

    Args:
        maze: 0은 통로, 1은 벽
        start: 시작 위치
        end: 도착 위치

    Returns:
        경로 리스트 또는 None
    """
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 우, 하, 좌, 상

    def is_valid(r: int, c: int) -> bool:
        return (0 <= r < rows and 0 <= c < cols and
                maze[r][c] == 0 and (r, c) not in visited)

    def backtrack(r: int, c: int, path: List[Tuple[int, int]]) -> Optional[List[Tuple[int, int]]]:
        if (r, c) == end:
            return path[:]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if is_valid(nr, nc):
                visited.add((nr, nc))
                path.append((nr, nc))

                result = backtrack(nr, nc, path)
                if result:
                    return result

                path.pop()  # 백트랙
                visited.remove((nr, nc))

        return None

    visited = {start}
    return backtrack(start[0], start[1], [start])


# ==================== 테스트 및 검증 ====================

if __name__ == "__main__":
    print("=" * 50)
    print("백트래킹 알고리즘 테스트")
    print("=" * 50)

    # N-Queen (4×4)
    print("\n[N-Queen 4×4]")
    solutions = solve_n_queens(4)
    print(f"해의 개수: {len(solutions)}")
    for i, sol in enumerate(solutions[:2]):  # 처음 2개만 출력
        print(f"\n해 {i+1}:")
        for row in sol:
            print(f"  {row}")

    # 부분 집합
    print("\n[부분 집합]")
    print(f"{{1, 2, 3}}의 부분 집합: {subsets([1, 2, 3])}")

    # 순열
    print("\n[순열]")
    print(f"{{1, 2, 3}}의 순열: {permutations([1, 2, 3])}")

    # 조합
    print("\n[조합]")
    print(f"4C2: {combinations(4, 2)}")

    # 스도쿠
    print("\n[스도쿠]")
    sudoku = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    if solve_sudoku(sudoku):
        print("해결 성공!")
        for row in sudoku[:3]:
            print(f"  {row}")
        print("  ...")
```

---

### Ⅲ. 기술 비교 분석

#### 6. 백트래킹 vs 브루트포스 vs 분할정복

| 구분 | 브루트포스 | 백트래킹 | 분할정복 |
|-----|-----------|----------|----------|
| 탐색 방식 | 모든 경우 | 유망한 경우만 | 독립적 부분 문제 |
| 가지치기 | 없음 | **있음 (핵심)** | 없음 |
| 재귀 구조 | 선택적 | **필수** | 필수 |
| 최적해 보장 | 항상 | 항상 | 항상 |
| 효율성 | 낮음 | **중간** | 높음 (문제에 따라) |
| 적용 문제 | 모든 문제 | 제약 충족, 최적화 | 분해 가능 문제 |

#### 7. 장단점 분석

| 장점 | 단점 |
|-----|------|
| 모든 해 탐색 가능 | 지수 시간 복잡도 (최악) |
| 최적해 보장 | 문제 크기에 민감 |
| 구조적이고 체계적 탐색 | 재귀로 인한 스택 오버플로우 가능 |
| 구현 직관적 | 가지치기 설계가 핵심/어려움 |
| 제약 문제에 강력 | 휴리스틱 없으면 느림 |

#### 8. 대안 기술 비교

| 비교 항목 | 백트래킹 | 분기한정 (B&B) | 힐 클라이밍 | 유전알고리즘 |
|---------|---------|---------------|------------|--------------|
| 완전성 | ★ 완전 | ★ 완전 | 불완전 | 불완전 |
| 최적해 | 보장 | 보장 | 미보장 | 미보장 |
| 효율성 | 중간 | 중간~높음 | 높음 | 중간 |
| 구현 난이도 | 낮음 | 중간 | 낮음 | 높음 |
| 적합 문제 | CSP | 최적화 | 근사 해 | 대규모 최적화 |

> **★ 선택 기준**:
> - 완전한 해 탐색 필요 → **백트래킹**
> - 최적화 + 하한/상한 계산 가능 → **분기한정 (Branch and Bound)**
> - 빠른 근사해만 필요 → **힐 클라이밍, 시뮬레이티드 어닐링**
> - 대규모 조합 최적화 → **유전 알고리즘, 메타휴리스틱**

---

### Ⅳ. 실무 적용 방안

#### 9. 실무 적용 시나리오

| 적용 분야 | 구체적 적용 방법 | 기대 효과 |
|---------|----------------|----------|
| **일정 관리** | 회의/작업 배치에서 충돌 없는 스케줄 탐색 | 충돌 0% 일정 생성 |
| **자원 배분** | 제약 조건 하에서 최적 자원 분배 | 자원 활용률 30% 향상 |
| **퍼즐 게임** | 스도쿠, 퍼즐 자동 해결기 | 즉시 해법 제공 |
| **컴파일러** | 레지스터 할당, 명령어 스케줄링 | 컴파일 최적화 |
| **AI 게임** | 체스, 바둑 등에서 가능한 수 탐색 | 승률 향상 |

#### 10. 실제 기업/서비스 사례

- **Google OR-Tools**: 제약 프로그래밍(CP)으로 스케줄링/배송 최적화
- **일정 관리 앱(Calendly)**: 백트래킹으로 충돌 없는 시간대 탐색
- **퍼즐 게임**: Candy Crush 등 매치-3 게임의 유효 이동 탐색
- **항공사 스케줄링**: 승무원 배정, 항로 최적화에 제약 기반 탐색

#### 11. 도입 시 고려사항

1. **기술적**:
   - 제약 조건 명확히 정의 (is_safe 함수)
   - 가지치기 최적화로 탐색 공간 축소
   - 반복적 구현으로 스택 오버플로우 방지

2. **운영적**:
   - 문제 크기에 따른 시간 제한 설정
   - 메모이제이션 활용 가능 여부 검토

3. **보안적**:
   - 입력 크기 제한으로 DoS 방지
   - 무한 루프 방지를 위한 깊이 제한

4. **경제적**:
   - NP-Complete 문제의 경우 근사 알고리즘 고려
   - 실시간 요구사항 시 휴리스틱 병행

#### 12. 주의사항 / 흔한 실수

- ❌ 상태 복구 누락 (pop/remove 호출 안 함)
- ❌ 가지치기 조건 미흡 → 불필요한 탐색 증가
- ❌ 깊은 재귀로 스택 오버플로우
- ❌ 전역 변수로 인한 상태 오염

#### 13. 관련 개념

```
📌 백트래킹 핵심 연관 개념 맵

┌─────────────────────────────────────────────────────────────────┐
│  [DFS] ←──→ [백트래킹] ←──→ [제약충족문제(CSP)]               │
│       ↓           ↓                ↓                           │
│  [그래프]    [분기한정]       [스도쿠/N-Queen]                 │
│                   ↓                                             │
│              [최적화문제]                                       │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| DFS (깊이우선탐색) | 기반 기법 | 백트래킹의 탐색 방식 | `[DFS](./graph.md)` |
| 동적계획법 | 대안 | 메모이제이션으로 최적화 | `[DP](./dynamic_programming.md)` |
| 분할정복 | 대안 | 독립 부분 문제 해결 | `[분할정복](./divide_conquer.md)` |
| 탐욕 알고리즘 | 대안 | 빠른 근사해 | `[탐욕](./greedy.md)` |
| 분기한정 | 확장 | 최적화 문제에 특화 | CLRS 참조 |

---

### Ⅴ. 기대 효과 및 결론

#### 14. 정량적 기대 효과

| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| 문제 해결 | 모든 가능한 해 탐색 | 100% 완전성 보장 |
| 탐색 효율 | 가지치기로 공간 축소 | 탐색 노드 50~90% 감소 |
| 최적해 | 전역 최적해 보장 | 근사 알고리즘 대비 정확도 100% |
| 확장성 | 다양한 CSP 문제 적용 | 범용 알고리즘 |

#### 15. 미래 전망

1. **기술 발전 방향**:
   - 병렬 백트래킹 (분산 탐색)
   - 기계학습 기반 가지치기 휴리스틱

2. **시장 트렌드**:
   - 자동 스케줄링/최적화 수요 증가
   - 클라우드 기반 최적화 서비스

3. **후속 기술**:
   - 양자 백트래킹 (Grover 알고리즘 활용)
   - 제약 프로그래밍(CP) 솔버 고도화

> **결론**: 백트래킹은 제약 충족 문제와 조합 최적화의 핵심 기법으로, 적절한 가지치기 설계가 성능을 결정한다. 완전성이 필요한 문제에서는 필수적이며, 분기한정, 메타휴리스틱과 결합하여 실무에 적용된다.

> **※ 참고 표준**: CLRS 'Introduction to Algorithms', ACM Computing Surveys (Backtracking Survey)

---

## 어린이를 위한 종합 설명

**백트래킹을 쉽게 이해해보자!**

백트래킹은 마치 **미로 찾기**와 같아요. 한 길로 계속 가다가 막다른 곳에 다다르면, 갈림길이 있던 곳까지 되돌아가서 다른 길을 시도해보는 거예요.

첫째, **선택하고 확인하기**예요. 갈림길에서 한 길을 선택하고, 그 길이 막다른 곳인지 출구인지 확인해요. 만약 막다른 곳이면 되돌아가야죠.

둘째, **똑똑하게 포기하기**예요. "이 길은 절대 출구가 없겠다!"라고 미리 알면 그 길은 아예 가지도 않아요. 이걸 '가지치기'라고 해요. 나무에서 죽은 가지를 치는 것처럼, 확인할 필요 없는 길은 미리 없애는 거예요.

---
