+++
title = "328. OLAP (On-Line Analytical Processing) - 대용량 다차원 분석, 비정규화(스타 스키마), 읽기 위주"
weight = 328
+++
## 0. 핵심 인사이트

> **💡 핵심 인사이트**
> LSM-Tree(Log-Structured Merge-Tree)는 **"쓰기 성능을 극대화하기 위해 데이터를 먼저 메모리(MemTable)에 저장하고, 일정 크기가 되면 디스크(SSTable)로_FLUSH_한 후,Background에서 병합(Compaction)하는 쓰기 최적화 자료구조"**입니다.
> 전통적 B-Tree가 읽기 우선(Read-Optimized)이라면, LSM-Tree는 쓰기 우선(Write-Optimized)입니다. Cassandra, RocksDB, LevelDB, MongoDB의 WiredTiger 등이 LSM-Tree를採用しており、**쓰기放量 обработка에 강한noSQL의 핵심 저장 엔진**입니다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

```
[B-Tree의 쓰기 동작]

  B-Tree에서 UPDATE 발생 시:
  1. 해당 leaf 노드를 디스크에서 읽음 (Random I/O)
  2. 메모리에서 값 수정
  3. 해당 leaf 노드를 디스크에 다시 기록 (Random I/O)
  → 같은 위치를 읽고 쓰기를 반복 (Read-Modify-Write)

  문제점:
  - Random I/O가 연속 I/O보다数百倍 느림
  - 쓰기 시 마다 디스크 탐색(seek) 필요
  - SSDs도 Random 쓰기 오버헤드는 존재
```

**LSM-Tree의 혁신:** 모든 쓰기를 **순차적(sequential)으로만 처리**하자!

---

## II. LSM-Tree의 핵심 자료구조: MemTable + SSTable

```
[LSM-Tree 아키텍처]

  쓰기 요청 (Write)
        │
        ▼
  ┌─────────────────────────────────┐
  │       MemTable (메모리)          │
  │  - 건건이 메모리에 기록 (순차)     │
  │  - 내부: Red-Black Tree 또는     │
  │    Skip List                    │
  │  - L0: 임계치 도달 시            │
  │    → Immutable MemTable로 전환   │
  │    → 새 MemTable 생성            │
  └─────────────────────────────────┘
        │ (임계치 도달 시)
        ▼
  ┌─────────────────────────────────┐
  │      L0: Level 0 (SSTable)       │
  │  - Immutable MemTable를         │
  │    디스크에Flush                │
  │  - 아직 정렬되지 않은 상태        │
  └─────────────────────────────────┘
        │ (Compaction 시)
        ▼
  ┌─────────────────────────────────┐
  │      L1: Level 1 (SSTable)      │
  │  - L0 파일들 병합 + 정렬         │
  │  - 키 기준 정렬된 상태            │
  └─────────────────────────────────┘
        │
        ▼
  ┌─────────────────────────────────┐
  │      L2: Level 2 (SSTable)      │
  │  - L1과 병합, 더 큰 파일로        │
  └─────────────────────────────────┘
        │
        ...
```

### MemTable (메모리 계층)

```python
# MemTable 구현 예시 (Skip List)
import random

class SkipList:
    """멀티레벨 연결 리스트로 O(log n) 검색"""
    def __init__(self, max_level=16):
        self.max_level = max_level
        self.header = Node(key=None, value=None, level=max_level)
        self.level = 0

    def insert(self, key, value):
        # 1. 해당 위치를 찾음 (수평으로 가로-scan)
        # 2. 새 노드를 위에서 아래로 수평插入
        # 3. Random 레벨 선택 (역사적 비율: 1/2^level)
        pass

    def flush_to_disk(self):
        # 메모리의 Skip List를 정렬된 형태로 SSTable로 변환
        pass
```

### SSTable (Static Sorted String Table)

```
[SSTable 구조]

  ┌──────────────────────────────────────────────────────┐
  │                    SSTable File                       │
  │  ┌────────────┐                                       │
  │  │ Data Block │  [key1:value1][key2:value2]...       │
  │  │ (실제 데이  │  - 키로 정렬된 상태                   │
  │  │  타 저장)   │  - 블럭 단위 압축 (Snappy, Zstd)     │
  │  └────────────┘                                       │
  │  ┌────────────┐                                       │
  │  │ Index Block│  [key: 오프셋] 들의集合               │
  │  │ (색인)      │  - 특정 키 빠르게 검색 가능           │
  │  └────────────┘                                       │
  │  ┌────────────┐                                       │
  │  │ Bloom Filter│ - 키 존재 여부 bloom filter로高速 판별│
  │  │             │  - 없으면 디스크 I/O 불필요         │
  │  └────────────┘                                       │
  │  ┌────────────┐                                       │
  │  │  Footer     │  - 메타데이터 (인덱스, 필터 위치 등)  │
  │  └────────────┘                                       │
  └──────────────────────────────────────────────────────┘
```

---

## III. Compaction (콤팩션): 쓰레기 수집의艺术

### 콤팩션의 종류

**1. Size-Tiered Compaction (STCS) - Cassandra 기본:**

```
[Size-Tiered Compaction]

  Level 0: SSTable 1 (4MB)
  Level 1: SSTable A, B (8MB each)   ← 크기 유사
  Level 2: SSTable C, D, E, F (16MB each)
  Level 3: SSTable G~N (32MB each)

  Trigger: 각 레벨이 N개 파일이 되면 → 상위 레벨로 병합
  → 항상 모든 레벨의 파일이 유사한 크기로 유지
```

**2. Level-Tiered Compaction (LTCS) - Cassandra 3.0+:**

```
[Level-Tiered Compaction]

  Level 0: 최대 4개 파일 (4MB)   ← 수평 확장
  Level 1: 최대 10개 파일 (40MB)   ← 10배 크기
  Level 2: 최대 100개 파일 (400MB)  ← 10배 크기
  Level 3: 최대 1000개 파일 (4GB)

  Trigger: 각 레벨의 모든 파일을 상위 레벨의 파일과정밀히 병합
  → 상위 레벨로 갈수록 파일 수 10배 증가
```

### 콤팩션 과정

```
[Compaction 상세 과정]

  상황: Level N에서 병합 시작

  Step 1: 병합 대상 파일 선택
  ┌──────────────────────────────────────┐
  │ Level N: [A, B, C, D] 파일들        │
  │ (모두 키 범위가 重複)                 │
  └──────────────────────────────────────┘

  Step 2: K-way 병합 정렬 (N=4 → 4-웨이 머지)
  ┌──────────────────────────────────────┐
  │  A: key1=X, key3=Y, key5=Z           │
  │  B: key1=X'(삭제 표시), key4=W      │
  │  C: key2=P, key3=Y'(업데이트)       │
  │  D: key5=Z'                         │
  │                                    │
  │  ↓ 4-웨이 머지 소트                 │
  │  key1=X' → X' (삭제가 최신)          │
  │  key2=P                              │
  │  key3=Y' → Y' (업데이트가 최신)       │
  │  key4=W                              │
  │  key5=Z' → Z' (업데이트가 최신)       │
  └──────────────────────────────────────┘

  Step 3: 결과 파일 생성 (Level N+1)
  ┌──────────────────────────────────────┐
  │ 새 SSTable: [key2:P, key3:Y', key4:W, key5:Z'] │
  │ ( Tombstone: 삭제된 key1은 기록 안 함) │
  └──────────────────────────────────────┘
```

---

## IV. 쓰기 성능 vs 읽기 성능의 트레이드오프

```
[LSM-Tree의 성능 특성]

  쓰기 (Write):
  ✅ 장점:
  - 모든 쓰기가 MemTable에만 순차 기록 (Random I/O 없음)
  - 디스크 Flush도 순차적
  - 쓰기 성능: B-Tree 比 10~100배 향상

  ⚠️ 단점:
  - 삭제도 쓰기(Tombstone)로 처리 → 내부碎片 발생
  - Compaction 시 I/O 오버헤드 발생 (Write Amplification)
  - 너무 많은 Compact가 발생하면 쓰기rate 저하

  읽기 (Read):
  ⚠️ 단점:
  - 읽을 때 MemTable → L0 → L1 → ... 순으로 탐색
  - 여러 레벨에 같은 키가 존재 → 最新 값 찾을 때까지 全 레벨 확인
  - (Bloom Filter로 해결)

  ✅ 장점:
  - Bloom Filter로 존재하지 않는 키는快速排除
  - Compaction으로 레벨이 깊어져도 메모리/IO 효율改善
```

**Write Amplification:**
- 원본 데이터 1MB를写入해도, Compaction 과정에서 수 MB의 디스크 쓰기 발생
- 일반적으로 10~50배 (저장 미디어 수명 영향)

---

## 5. 실무 적용 및 최적화 기법

**LSM-Tree를 采用하는 시스템:**
- **Apache Cassandra**: STCS/LTCS 선택 가능
- **RocksDB**: Level-티어드 (Facebook الأصل)
- **LevelDB**: Google의原始 구현
- **MongoDB (WiredTiger)**: LSM-Tree 지원 (SNappy 압축)
- **InfluxDB**: 시계열 데이터용 LSM-Tree 변형

**B-Tree vs LSM-Tree 선택:**

| 시나리오 | 추천 |
|---------|------|
| 쓰기 많은ワーク로드 (IoT, 로그) | LSM-Tree |
| 읽기 많은ワーク로드 (Web 서비스) | B-Tree |
| 순차 쓰기가 많은 경우 (analytics) | LSM-Tree |
| 임의 접근 읽기가 많은 경우 | B-Tree |
| 짧은 TTL (데이터很快就过期) | LSM-Tree |

> 📢 **섹션 요약 비유:** LSM-Tree는 **"편의점 진열대"**와 같습니다. 새 물건이 들어오면 진열대에 바로 올리는 것이 아니라, **"먼저 창고(메모리)에 쌓아두었다가, 창고가 차면 진열대(SSTable)로 한 꺼내음"**으로 효율적으로管理합니다. 진열대가 다 차면 (Compaction) **"모든 물건을 한 꺼내어新しい날부터 순서대로 다시 진열"**합니다. 이때 先入れ先出し(FIFO)처럼 오래된 것을 뒤로 미뤄두고 새로운 것을 앞에 둡니다. B-Tree가 **"客人을 위해 물건을 찾을 때 진열대 어딜 가도 바로 찾을 수 있다"**는 장점이 있지만, **"새 물건 올릴 때마다 어딘가 비워야 하는"** 번거로움이 있습니다. LSM-Tree는 **"일단 창고에 차곡차곡 쌓아두고, 정기적으로 정리整列하는"** 것으로 쓰기 효율을 극대화합니다. **"정리하는 시간(Compaction)은 들지만,平日里货物摆放(쓰기)는 빠른"** 것이 핵심입니다.
