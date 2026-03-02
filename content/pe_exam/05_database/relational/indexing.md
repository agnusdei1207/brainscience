+++
title = "데이터베이스 인덱싱 (Database Indexing)"
date = 2025-03-02

[extra]
categories = "pe_exam-database"
+++

# 데이터베이스 인덱싱 (Database Indexing)

## 핵심 인사이트 (3줄 요약)
> **데이터 검색 속도를 획기적으로 향상시키는 별도 정렬 자료구조**. B+Tree가 RDBMS 표준으로 범위 검색에 최적화. 읽기 성능 100~1000배 향상 vs 쓰기 오버헤드 발생이라는 트레이드오프.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 데이터베이스 인덱스(Index)는 **테이블의 특정 컬럼(들)에 대해 빠른 검색을 위해 별도로 유지하는 정렬된 자료구조**로, 책의 색인(Index)처럼 원본 데이터를 직접 스캔하지 않고도 원하는 레코드의 위치를 신속히 찾을 수 있게 한다.

> 💡 **비유**: 인덱스는 **"백과사전의 찾아보기"** 같아요. "컴퓨터"를 찾고 싶을 때 1,000페이지를 다 읽지 않고, 찾아보기에서 "컴퓨터: 234페이지"를 확인하면 바로 찾을 수 있죠.

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 풀 테이블 스캔(Full Table Scan)**: 100만 행 테이블에서 1건을 찾기 위해 100만 번 읽기 수행 (O(n))
2. **기술적 필요성 - 디스크 I/O 최소화**: 디스크 접근은 메모리보다 10만 배 느려 효율적 탐색 필수
3. **시장/산업 요구 - 실시간 응답**: 웹/모바일 서비스에서 100ms 이내 응답 요구사항 충족

**핵심 목적**: **검색 성능 최적화**를 통한 디스크 I/O 최소화와 사용자 응답 시간 단축

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **루트 노드** | 트리 진입점 | 모든 검색의 시작점 | 건물 1층 안내데스크 |
| **브랜치 노드** | 중간 분기점 | 범위에 따른 경로 안내 | 층별 안내판 |
| **리프 노드** | 실제 데이터 위치 | 키값 + ROWID 저장 | 각 방 문 |
| **ROWID** | 물리적 주소 | 블록 번호 + 슬롯 번호 | 방 번호 |
| **엔트리** | 인덱스 레코드 | 키값 + ROWID 쌍 | 명찰 |

**구조 다이어그램** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────┐
│                    B+Tree 인덱스 구조                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [루트 노드 - Level 2]                                             │
│   ┌───────────────────────────────────────────────┐                │
│   │  [50]          │          [80]                │                │
│   └─────┬──────────┴──────────┬──────────────────┘                │
│         │                     │                                    │
│   [브랜치 노드 - Level 1]                                          │
│   ┌─────────────────┐    ┌─────────────────┐                      │
│   │ [20│40] │ [60│70] │    │ [90│100]       │                      │
│   └───┬─────┴────┬───┘    └────┬────────────┘                      │
│       │          │             │                                    │
│   [리프 노드 - Level 0] ────────────────────→ [다음 리프 링크]      │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐                 │
│   │10│ROWID │20│ROWID │50│ROWID │80│ROWID │                      │
│   │   ·    │ │   ·    │ │   ·    │ │   ·    │                      │
│   └────┬───┘ └────┬───┘ └────┬───┘ └────┬───┘                      │
│        │          │          │          │                          │
│        ▼          ▼          ▼          ▼                          │
│   ┌─────────────────────────────────────────────────┐              │
│   │              [데이터 블록 (테이블)]               │              │
│   │   행1 │ 행2 │ 행3 │ ... │ 행N                   │              │
│   └─────────────────────────────────────────────────┘              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    인덱스 스캔 vs 테이블 스캔                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   [인덱스 없음 - Full Table Scan]                                   │
│   블록1 → 블록2 → 블록3 → ... → 블록1000                            │
│   I/O: 1000회, 시간복잡도: O(n)                                     │
│                                                                     │
│   [인덱스 사용 - Index Range Scan]                                  │
│   루트 → 브랜치 → 리프 → 데이터블록                                  │
│   I/O: 3~5회, 시간복잡도: O(log n)                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):
```
① 쿼리 파싱 → ② 옵티마이저 인덱스 선택 → ③ B+Tree 탐색 → ④ ROWID로 데이터 접근 → ⑤ 결과 반환
```

- **1단계 - 쿼리 파싱**: WHERE 절의 검색 조건 분석
- **2단계 - 옵티마이저 판단**: 비용 기반(CBO)으로 인덱스 사용 여부 결정
- **3단계 - B+Tree 탐색**: 루트→브랜치→리프 순으로 이진 탐색 수행
- **4단계 - 랜덤 액세스**: ROWID로 테이블 블록 직접 접근
- **5단계 - 결과 반환**: 조건에 맞는 행들을 결과 집합으로 반환

**핵심 알고리즘/공식** (해당 시 필수):

```
[B+Tree 높이 계산]
h = ⌈log_f(n)⌉
f = 팬아웃 (한 노드의 자식 수, 보통 100~1000)
n = 레코드 수

예: 100만 행, 팬아웃 100 → h = ⌈log_100(1,000,000)⌉ = 3
→ 단 3번의 디스크 I/O로 검색 완료!

[인덱스 선택도 (Selectivity)]
선택도 = 선택된 행 수 / 전체 행 수
카디널리티 = 1 / 선택도

높은 선택도 (≈ 1): 대부분의 행 선택 → 인덱스 비효율
낮은 선택도 (< 0.1): 소수 행 선택 → ★ 인덱스 효율적

[비용 계산 공식]
Full Scan Cost = 페이지 수 × 1 I/O
Index Scan Cost = (트리높이 + 선택행수) × 랜덤 I/O

Index Scan 유리 조건: 선택행수 < 전체행수 × 5~20%
```

**코드 예시** (필수: Python 또는 의사코드):
```python
from dataclasses import dataclass
from typing import List, Optional, Tuple
import bisect

@dataclass
class BPlusTreeNode:
    """B+Tree 노드"""
    keys: List[int]
    children: List['BPlusTreeNode']  # 내부 노드용
    values: List[int]                 # 리프 노드용 (ROWID)
    is_leaf: bool
    next_leaf: Optional['BPlusTreeNode'] = None  # 리프 노드 연결

class BPlusTree:
    """B+Tree 인덱스 구현"""
    def __init__(self, order: int = 4):
        self.order = order  # 최대 자식 수
        self.root = BPlusTreeNode(keys=[], children=[], values=[], is_leaf=True)

    def search(self, key: int) -> Optional[int]:
        """키값으로 ROWID 검색 - O(log n)"""
        node = self.root
        while not node.is_leaf:
            idx = bisect.bisect_right(node.keys, key)
            node = node.children[idx]
        # 리프 노드에서 검색
        try:
            idx = node.keys.index(key)
            return node.values[idx]
        except ValueError:
            return None

    def range_search(self, start: int, end: int) -> List[int]:
        """범위 검색 - B+Tree의 장점"""
        results = []
        # 시작 키가 있는 리프 노드 찾기
        node = self._find_leaf(start)
        # 리프 노드 연결 따라가며 범위 내 값 수집
        while node:
            for i, key in enumerate(node.keys):
                if start <= key <= end:
                    results.append(node.values[i])
                elif key > end:
                    return results
            node = node.next_leaf
        return results

    def _find_leaf(self, key: int) -> BPlusTreeNode:
        """키가 있어야 할 리프 노드 찾기"""
        node = self.root
        while not node.is_leaf:
            idx = bisect.bisect_right(node.keys, key)
            node = node.children[idx]
        return node

    def insert(self, key: int, value: int) -> None:
        """키-값 삽입"""
        leaf = self._find_leaf(key)
        idx = bisect.bisect_left(leaf.keys, key)
        leaf.keys.insert(idx, key)
        leaf.values.insert(idx, value)
        # 오버플로우 처리 (분할)
        if len(leaf.keys) > self.order - 1:
            self._split_leaf(leaf)

    def _split_leaf(self, leaf: BPlusTreeNode) -> None:
        """리프 노드 분할"""
        mid = len(leaf.keys) // 2
        new_leaf = BPlusTreeNode(
            keys=leaf.keys[mid:],
            values=leaf.values[mid:],
            is_leaf=True,
            next_leaf=leaf.next_leaf
        )
        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]
        leaf.next_leaf = new_leaf
        # 부모 노드에 키 전파 (구현 생략)

class DatabaseIndex:
    """데이터베이스 인덱스 시뮬레이터"""

    def __init__(self):
        self.btree_index = BPlusTree(order=100)
        self.hash_index = {}  # 해시 인덱스
        self.bitmap_index = {}  # 비트맵 인덱스

    def create_btree_index(self, data: List[Tuple[int, int]]) -> None:
        """B+Tree 인덱스 생성"""
        for key, rowid in data:
            self.btree_index.insert(key, rowid)
        print(f"B+Tree 인덱스 생성 완료: {len(data)}개 엔트리")

    def create_hash_index(self, data: List[Tuple[int, int]]) -> None:
        """해시 인덱스 생성 (등가 검색용)"""
        for key, rowid in data:
            if key not in self.hash_index:
                self.hash_index[key] = []
            self.hash_index[key].append(rowid)
        print(f"해시 인덱스 생성 완료: {len(self.hash_index)}개 버킷")

    def create_bitmap_index(self, data: List[Tuple[str, int]], total_rows: int) -> None:
        """비트맵 인덱스 생성 (저카디널리티용)"""
        for value, rowid in data:
            if value not in self.bitmap_index:
                self.bitmap_index[value] = [0] * total_rows
            self.bitmap_index[value][rowid] = 1
        print(f"비트맵 인덱스 생성 완료: {len(self.bitmap_index)}개 값")

    def btree_point_query(self, key: int) -> int:
        """B+Tree 점 검색"""
        return self.btree_index.search(key)

    def btree_range_query(self, start: int, end: int) -> List[int]:
        """B+Tree 범위 검색"""
        return self.btree_index.range_search(start, end)

    def hash_point_query(self, key: int) -> List[int]:
        """해시 등가 검색 - O(1)"""
        return self.hash_index.get(key, [])

    def bitmap_query(self, conditions: List[str]) -> List[int]:
        """비트맵 인덱스 결합 검색 (비트 연산)"""
        if not conditions:
            return []
        result = self.bitmap_index.get(conditions[0], [])
        import numpy as np
        result = np.array(result)
        for cond in conditions[1:]:
            result = result & np.array(self.bitmap_index.get(cond, result.shape))
        return result.tolist()

# 성능 비교 시뮬레이션
if __name__ == "__main__":
    import time
    import random

    # 100만 건 데이터 생성
    data = [(i, i) for i in range(1, 1000001)]

    db = DatabaseIndex()

    # 인덱스 생성 시간 측정
    start = time.time()
    db.create_btree_index(data)
    print(f"인덱스 생성 시간: {time.time() - start:.3f}초")

    # 점 검색 비교
    target = 500000

    # 인덱스 검색
    start = time.time()
    result = db.btree_point_query(target)
    print(f"B+Tree 검색: {time.time() - start:.6f}초, 결과: {result}")

    # 범위 검색
    start = time.time()
    results = db.btree_range_query(100000, 100100)
    print(f"범위 검색 (100개): {time.time() - start:.6f}초, 결과 수: {len(results)}")
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):
| 장점 | 단점 |
|-----|------|
| **검색 성능 향상**: O(n) → O(log n), 100~1000배 개선 | **저장 공간 증가**: 테이블 크기의 10~30% 추가 필요 |
| **정렬 비용 제거**: 이미 정렬된 상태로 ORDER BY 최적화 | **쓰기 성능 저하**: INSERT/UPDATE/DELETE 시 인덱스 갱신 오버헤드 |
| **JOIN 성능 개선**: FK 컬럼 인덱스로 조인 비용 절감 | **인덱스 관리**: 통계 갱신, 재구성(Rebuild) 필요 |
| **제약조건 검사**: UNIQUE, PK 빠른 중복 확인 | **잘못된 사용 시 악화**: 선택도 높으면 풀 스캔보다 느림 |

**인덱스 유형별 비교** (필수: 최소 2개 대안):
| 비교 항목 | B+Tree | Hash | Bitmap |
|---------|--------|------|--------|
| **핵심 특성** | ★ 범용, 범위 검색 가능 | 등가 검색만 | 저카디널리티 최적 |
| **검색 타입** | 등가, 범위, 정렬 | 등가만 | 등가, 결합 |
| **시간복잡도** | O(log n) | ★ O(1) | O(1) 비트연산 |
| **공간 효율** | 중간 | 좋음 | ★ 압축 시 매우 좋음 |
| **쓰기 비용** | 중간 | 낮음 | 높음 (재구성) |
| **적합 환경** | OLTP 일반 | 메모리 DB, 캐시 | OLAP, DW |

| 비교 항목 | 클러스터형 인덱스 | 비클러스터형 인덱스 |
|---------|----------------|-------------------|
| **데이터 순서** | ★ 물리적 정렬 | 독립적 순서 |
| **리프 노드** | 데이터 페이지 자체 | ROWID 포인터 |
| **개수 제한** | 테이블당 1개 | 테이블당 다수 가능 |
| **범위 검색** | ★ 매우 빠름 | 추가 I/O 필요 |
| **삽입 비용** | 높음 (페이지 분할) | 중간 |

> **★ 선택 기준**:
> - **B+Tree**: 기본 선택, 범위 검색/정렬 필요 시
> - **Hash**: 정확히 일치하는 값 검색만 필요한 경우
> - **Bitmap**: 성별, 지역 등 선택지 적은 컬럼, OLAP 환경
> - **클러스터형**: PK, 범위 검색 빈번한 컬럼

---

### Ⅳ. 실무 적용 방안 (필수: 기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **전자상거래 상품 검색** | 상품명, 카테고리에 복합 인덱스 | 검색 응답시간 500ms → 50ms (90% 단축) |
| **금융 거래 내역 조회** | 계좌번호 + 거래일시 복합 인덱스 | 월별 조회 10초 → 0.5초 |
| **로그 분석 시스템** | 저카디널리티 컬럼에 비트맵 인덱스 | 집계 쿼리 5분 → 10초 |

**실제 도입 사례** (필수: 구체적 기업/서비스):
- **사례 1 - 네이버 쇼핑**: 상품 검색에 B+Tree 복합 인덱스 적용, 카테고리+가격+검색어 조합으로 1억 상품에서 0.1초 내 검색
- **사례 2 - 카카오페이**: 계좌 이력 테이블에 파티셔닝+로컬 인덱스로 월 10억 건 데이터 실시간 조회
- **사례 3 - AWS Aurora**: MySQL 기반 스토리지 엔진 최적화로 인덱스 생성 속도 5배 향상

**도입 시 고려사항** (필수: 4가지 관점):
1. **기술적**:
   - 카디널리티 분석 (높을수록 유리)
   - 선택도 계산 (5~20% 미만이어야 유리)
   - 복합 인덱스 컬럼 순서 (선택도 높은 것 우선)
   - 커버링 인덱스 가능성 검토
2. **운영적**:
   - 인덱스 통계 갱신 주기
   - 인덱스 재구성(Rebuild) 스케줄
   - 모니터링 대시보드 구축
   - 사용되지 않는 인덱스 제거
3. **보안적**:
   - 인덱스 컬럼 민감 정보 노출 주의
   - 인덱스 접근 권한 관리
   - 암호화 컬럼 인덱싱 제약
4. **경제적**:
   - 저장 공간 비용 증가
   - 쓰기 성능 저하 vs 읽기 향상 트레이드오프
   - 인덱스 수 제한 (테이블당 5개 권장)

**주의사항 / 흔한 실수** (필수: 최소 3개):
- ❌ **함수 사용**: `WHERE YEAR(date) = 2024` → 인덱스 무효, 범위 검색으로 변경
- ❌ **암시적 형변환**: `WHERE varchar_col = 123` → 인덱스 미사용
- ❌ **OR 조건**: `WHERE a = 1 OR b = 2` → UNION ALL로 분리
- ❌ **선택도 무시**: 90% 행 선택하는 조건에 인덱스 → 풀 스캔보다 느림

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):
```
📌 인덱싱과 밀접하게 연관된 핵심 개념들

┌─────────────────────────────────────────────────────────────────┐
│  인덱싱 핵심 연관 개념 맵                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [B+Tree] ←──→ [인덱싱] ←──→ [쿼리최적화]                      │
│       ↓              ↓              ↓                           │
│   [정규화]      [트랜잭션]     [옵티마이저]                      │
│       ↓              ↓              ↓                           │
│   [파티셔닝]    [MVCC]        [실행계획]                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| **쿼리 최적화** | 후속 개념 | 인덱스를 활용한 쿼리 튜닝 | `[쿼리최적화](./query_optimization.md)` |
| **정규화** | 선행 개념 | 정규화 후 인덱스 설계 | `[정규화](./normalization.md)` |
| **B+Tree** | 핵심 자료구조 | 인덱스의 기본 구조 | `[B+Tree](../../08_algorithm_stats/data_structure/btree.md)` |
| **트랜잭션** | 보완 개념 | 인덱스와 ACID 보장 | `[트랜잭션](../transaction.md)` |
| **파티셔닝** | 확장 개념 | 대용량 테이블 분할 + 인덱스 | `[파티셔닝](../distributed_database.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| **검색 성능** | 풀 스캔 → 인덱스 스캔 | 응답시간 90~99% 단축 |
| **디스크 I/O** | 블록 접근 횟수 감소 | I/O 95% 감소 |
| **시스템 부하** | CPU/메모리 사용 효율화 | 리소스 사용 50% 절감 |
| **사용자 경험** | 실시간 응답 가능 | 이탈률 30% 감소 |

**미래 전망** (필수: 3가지 관점):
1. **기술 발전 방향**: AI 기반 자동 인덱스 추천, 학습형 인덱스(Learned Index)로 B+Tree 대체 시도
2. **시장 트렌드**: SSD/NVMe 보편화로 랜덤 I/O 비용 감소, 인메모리 DB 확대로 인덱스 전략 변화
3. **후속 기술**: 벡터 인덱스(IVF, HNSW)로 AI/LLM 시대의 유사도 검색 지원

> **결론**: 인덱싱은 데이터베이스 성능 최적화의 가장 강력한 도구로, 적절한 인덱스 설계는 수백 배의 성능 향상을 가져온다. 다만 "무조건 인덱스"는 위험하며, 선택도 분석과 쓰기 부하 고려 후 신중히 설계해야 한다.

> **※ 참고 표준**: SQL:2023 표준, Oracle Index Internals, MySQL 8.0 Reference Manual

---

## 어린이를 위한 종합 설명 (필수)

**데이터베이스 인덱싱**은(는) 마치 **"책의 찾아보기 페이지"** 같아요.

두꺼운 백과사전에서 "태양계"에 대한 내용을 찾아야 한다고 생각해보세요. 찾아보기가 없다면 1페이지부터 마지막까지 다 읽어야 해요. 하지만 찾아보기 페이지에서 "태양계: 234페이지"라고 적혀 있으면 바로 찾을 수 있죠!

인덱스는 이 찾아보기와 똑같아요. **데이터베이스에서 원하는 정보를 빨리 찾을 수 있게 도와주는 특별한 목록**이에요. 이름, 나이, 주소 같은 것들을 미리 정리해두는 거예요.

하지만 인덱스를 만드는 데도 시간이 걸리고, 공간도 필요해요. 그래서 **자주 찾는 것만 인덱스를 만들어요**. 마치 요리책에서 자주 만드는 레시피만 책갈피를 꽂아두는 것처럼요!

인덱스 덕분에 100만 명의 학생 중에서 "김철수"를 1초 만에 찾을 수 있어요. 정말 빠르죠? 📚🔍
