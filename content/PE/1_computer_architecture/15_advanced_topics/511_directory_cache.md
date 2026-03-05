+++
title = "511. 디렉터리 캐시"
date = "2026-03-05"
[extra]
categories = "studynotes-computer-architecture"
+++

# 디렉터리 캐시 (Directory Cache)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 멀티코어 시스템에서 캐시 일관성 프로토콜의 오버헤드를 줄이기 위해 공유 정보를 캐싱하는 하드웨어 구조로, 메인 디렉터리 접근 지연시간과 전력 소모를 크게 감소시킨다.
> 2. **가치**: 디렉터리 캐시 적중 시 일관성 트랜잭션 지연시간을 30-50% 감소시키며, 대규모 시스템에서 전체 시스템 성능을 15-25% 향상시킬 수 있다.
> 3. **융합**: 디렉터리 기반 캐시 일관성 프로토콜, 분산 공유 메모리, NUMA 아키텍처와 밀접하게 연동되며, 확장 가능한 병렬 컴퓨팅의 핵심 최적화 기법이다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
디렉터리 캐시(Directory Cache)는 대규모 멀티프로세서 시스템에서 캐시 일관성 유지를 위한 디렉터리 정보를 고속으로 접근할 수 있도록 저장하는 하드웨어 캐시 구조이다. 메인 디렉터리는 메모리에 위치하여 접근 지연시간이 길지만, 디렉터리 캐시는 프로세서 가까이 배치하여 자주 참조되는 디렉터리 엔트리를 빠르게 제공한다. 이는 스누핑 방식의 확장성 한계를 극복하고 대규모 시스템에서 효율적인 캐시 일관성을 가능하게 한다.

### 💡 비유
디렉터리 캐시는 "도서관의 인기 도서 코너"와 같다. 전체 도서 목록(메인 디렉터리)은 큰 창고에 있어 찾는데 시간이 오래 걸린다. 하지만 자주 빌려보는 책들은 입구 근처 인기 도서 코너(디렉터리 캐시)에 비치해두어 빠르게 찾을 수 있다. 누군가 책을 빌리면 인기 코너의 기록을 업데이트하고, 오래 안 쓰인 책은 다시 창고로 보낸다.

### 등장 배경 및 발전 과정

#### 1. 기존 기술의 치명적 한계점
- **메인 디렉터리 지연**: 메모리에 위치한 디렉터리 접근에 100+ 사이클 소요
- **직렬화 병목**: 디렉터리가 단일 포인트가 되어 동시 접근 제한
- **전력 소모**: 모든 일관성 트랜잭션마다 메인 디렉터리 접근

#### 2. 패러다임 변화의 역사
- **1990년대**: SGI Origin 2000에서 초기 디렉터리 캐시 개념
- **2000년대**: AMD HyperTransport with directory caching
- **2010년대**: Intel QuickPath Architecture, distributed directories
- **2020년대**: Mesh-based directory caches, CXL coherence

#### 3. 비즈니스적 요구사항
- 데이터센터: 수천 코어 확장성
- HPC: 낮은 지연시간과 높은 대역폭
- 클라우드: 멀티테넌트 격리

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|--------|----------|-------------------|-----------|------|
| **디렉터리 태그** | 캐시된 디렉터리 엔트리 식별 | 메모리 블록 주소 → 디렉터리 캐시 인덱스 매핑 | Set-Associative, CAM | 도서 색인 |
| **공유 벡터** | 해당 블록을 캐시한 프로세서 목록 | 비트맵 (N비트, N=프로세서 수) | Bit Vector, Compressed | 대출자 명단 |
| **상태 정보** | 디렉터리 엔트리의 일관성 상태 | Uncached, Shared, Modified, Exclusive | State Machine | 도서 상태 |
| **교체 정책** | 캐시 엔트리 교체 결정 | LRU, LFU, Random | Replacement Logic | 정리 주기 |
| **일관성 로직** | 캐시된 디렉터리와 메인 디렉터리 동기화 | Write-through, Write-back | Coherence Protocol | 기록 갱신 |
| **프리페처** | 미리 디렉터리 정보 로드 | 접근 패턴 기반 예측 | HW/SW Prefetching | 미리 준비 |

### 정교한 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    디렉터리 캐시 계층 구조 (64-Core 시스템 예시)                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │                    프로세서 노드들 (Processor Nodes)                       │ │
│  │                                                                           │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       ┌─────────┐       │ │
│  │  │ Node 0  │ │ Node 1  │ │ Node 2  │ │ Node 3  │  ...  │ Node 15 │       │ │
│  │  │ 4 Cores │ │ 4 Cores │ │ 4 Cores │ │ 4 Cores │       │ 4 Cores │       │ │
│  │  │ L1/L2   │ │ L1/L2   │ │ L1/L2   │ │ L1/L2   │       │ L1/L2   │       │ │
│  │  │ L3($Dir)│ │ L3($Dir)│ │ L3($Dir)│ │ L3($Dir)│       │ L3($Dir)│       │ │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘       └────┬────┘       │ │
│  │       │           │           │           │                  │             │ │
│  └───────┼───────────┼───────────┼───────────┼──────────────────┼─────────────┘ │
│          │           │           │           │                  │               │
│          └───────────┴───────────┴─────┬─────┴──────────────────┘               │
│                                        │                                        │
│                         ┌──────────────▼──────────────┐                        │
│                         │     인터커넥트 (Mesh/Ring)    │                        │
│                         └──────────────┬──────────────┘                        │
│                                        │                                        │
│  ══════════════════════════════════════╪══════════════════════════════════════ │
│                    디렉터리 캐시 상세 구조                           │
│  ══════════════════════════════════════╪══════════════════════════════════════ │
│                                        │                                        │
│  ┌─────────────────────────────────────▼─────────────────────────────────────┐ │
│  │                        디렉터리 캐시 (Directory Cache)                      │ │
│  │  ┌───────────────────────────────────────────────────────────────────────┐│ │
│  │  │  크기: 4KB - 64KB (설계에 따라)                                       ││ │
│  │  │  구조: 4-way Set Associative                                          ││ │
│  │  │  엔트리 수: 256 - 4096개                                              ││ │
│  │  └───────────────────────────────────────────────────────────────────────┘│ │
│  │                                                                           │ │
│  │  ┌─────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                    디렉터리 캐시 엔트리 구조                          │ │ │
│  │  │  ┌─────────────────────────────────────────────────────────────────┐ │ │ │
│  │  │  │ Tag (26-bit) │ State (3-bit) │ Shared Vector (16-bit) │ Valid  │ │ │ │
│  │  │  │              │               │ [각 비트 = 노드 소유 여부] │ (1-bit)│ │ │ │
│  │  │  └─────────────────────────────────────────────────────────────────┘ │ │ │
│  │  │                                                                       │ │ │
│  │  │  상태 필드:                                                           │ │ │
│  │  │  • 000: UNCACHED - 어떤 노드도 캐시하지 않음                          │ │ │
│  │  │  • 001: SHARED   - 여러 노드가 읽기 전용으로 캐시                      │ │ │
│  │  │  • 010: MODIFIED - 한 노드가 배타적 쓰기 권한 보유                     │ │ │
│  │  │  • 011: EXCLUSIVE - 한 노드만 캐시, 아직 수정 안 함                   │ │ │
│  │  │  • 100: OWNER    - 수정됨 + 공유 중 (MOESI)                          │ │ │
│  │  └─────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                           │ │
│  │  ┌─────────────────────────────────────────────────────────────────────┐ │ │
│  │  │                      압축된 공유 벡터 (Coarse Vector)                │ │ │
│  │  │                                                                       │ │ │
│  │  │  전체 비트맵 (64-core): 64-bit                                        │ │ │
│  │  │  압축 방식:                                                           │ │ │
│  │  │  • Limited Pointer: 최근 4개 노드만 추적 (8-bit)                     │ │ │
│  │  │  • Coarse Bitmap: 4노드당 1비트 (16-bit)                             │ │ │
│  │  │  • Region-based: 메모리 영역별 추적                                  │ │ │
│  │  └─────────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                        │                                        │
│                                        ▼                                        │
│  ┌───────────────────────────────────────────────────────────────────────────┐ │
│  │                        메인 디렉터리 (Main Directory)                      │ │
│  │                                                                           │ │
│  │  위치: 메모리 컨트롤러 내 또는 별도 DRAM                                   │ │
│  │  크기: 메모리 블록당 1 엔트리 (수 GB)                                      │ │
│  │  접근 지연: 100-300 사이클                                                │ │
│  │                                                                           │ │
│  │  엔트리 구조:                                                             │ │
│  │  ┌─────────────────────────────────────────────────────────────────────┐ │ │
│  │  │ Memory Tag │ State │ Full Sharing Vector (64-bit) │ Statistics     │ │ │
│  │  └─────────────────────────────────────────────────────────────────────┘ │ │
│  └───────────────────────────────────────────────────────────────────────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리

#### ① 디렉터리 캐시 동작 흐름
```
일관성 트랜잭션 처리:

1. Read Request (노드 A → 메모리 블록 X)
   a) 디렉터리 캐시 조회
      - Hit: 캐시된 상태 정보 사용
      - Miss: 메인 디렉터리 접근 → 캐시에 적재

   b) 상태에 따른 처리:
      - UNCACHED: 데이터 반환, 상태 → EXCLUSIVE, Sharers = {A}
      - SHARED: 데이터 반환, Sharers += {A}
      - EXCLUSIVE/MODIFIED: 소유자에게 Flush 요청 → 데이터 전달

2. Write Request (노드 A → 메모리 블록 X)
   a) 디렉터리 캐시 조회

   b) 상태에 따른 처리:
      - UNCACHED: 데이터 반환, 상태 → MODIFIED, Sharers = {A}
      - SHARED: 모든 Sharers에 Invalid 전송 → 상태 → MODIFIED
      - EXCLUSIVE: 상태만 → MODIFIED (메시지 없음)
      - MODIFIED (다른 노드): 소유자에게 Flush+Invalid → 상태 이전

3. 캐시 교체 (노드 A에서 블록 X 제거)
   - 디렉터리 캐시의 Sharers 벡터에서 A 제거
   - Sharers가 비면 상태 → UNCACHED
```

#### ② 디렉터리 캐시 교체 정책
```
LRU 기반 교체:

1. 새로운 디렉터리 엔트리 접근
   - 캐시 미스 시 새 엔트리 할당

2. 교체 후보 선택
   - LRU 위치의 엔트리 선택

3. 교체 전 처리
   - Dirty 상태면 메인 디렉터리에 Write-back
   - SHARED/MODIFIED 상태면 소유자 정보 정리

4. 새 엔트리 로드
   - 메인 디렉터리에서 정보 읽어옴

최적화 기법:
- Write-through: 매번 메인 디렉터리 동기화
- Write-back: 교체 시에만 동기화 (지연, 더 효율적)
- Selective Write-back: MODIFIED 상태만 동기화
```

#### ③ 디렉터리 캐시 일관성
```
문제: 디렉터리 캐시 자체의 일관성 유지

해결 방안:

1. Invalidation-based:
   - 메인 디렉터리 변경 시 관련 캐시 엔트리 무효화
   - 장점: 단순함
   - 단점: 캐시 효율 저하

2. Update-based:
   - 메인 디렉터리 변경 시 캐시 엔트리 갱신
   - 장점: 캐시 적중률 유지
   - 단점: 복잡한 업데이트 로직

3. Hybrid:
   - 자주 변경되는 정보는 무효화
   - 안정적인 정보는 갱신

구현 예시:
- Sharers 추가: 캐시 엔트리 갱신
- Sharers 제거: 갱신 (0이면 상태도 변경)
- 상태 전이: 갱신
```

### 핵심 알고리즘 & 실무 코드 예시

#### 디렉터리 캐시 시뮬레이터
```python
from dataclasses import dataclass, field
from typing import List, Set, Optional, Dict
from enum import Enum
import random

class DirectoryState(Enum):
    UNCACHED = 0
    SHARED = 1
    MODIFIED = 2
    EXCLUSIVE = 3
    OWNER = 4  # For MOESI

@dataclass
class DirectoryCacheEntry:
    tag: int
    state: DirectoryState
    sharers: Set[int]  # Node IDs that have this block cached
    owner: Optional[int] = None  # For MODIFIED/OWNER state
    valid: bool = True
    dirty: bool = False  # Needs write-back to main directory

@dataclass
class MainDirectoryEntry:
    state: DirectoryState
    sharers: Set[int]
    owner: Optional[int] = None

class DirectoryCache:
    def __init__(self,
                 num_sets: int = 64,
                 ways: int = 4,
                 num_nodes: int = 16):
        self.num_sets = num_sets
        self.ways = ways
        self.num_nodes = num_nodes

        # Cache storage: set -> list of entries (LRU order)
        self.cache: Dict[int, List[DirectoryCacheEntry]] = {
            i: [] for i in range(num_sets)
        }

        # Main directory (simulated as slow memory)
        self.main_directory: Dict[int, MainDirectoryEntry] = {}

        # Statistics
        self.stats = {
            'accesses': 0,
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'write_backs': 0,
            'invalidations_sent': 0,
            'data_provided': 0
        }

    def _get_set_index(self, block_addr: int) -> int:
        return block_addr % self.num_sets

    def _find_entry(self, block_addr: int) -> Optional[DirectoryCacheEntry]:
        """Find entry in cache, update LRU on hit"""
        set_idx = self._get_set_index(block_addr)
        entries = self.cache[set_idx]

        for i, entry in enumerate(entries):
            if entry.valid and entry.tag == block_addr:
                # Move to MRU position
                entries.pop(i)
                entries.append(entry)
                return entry

        return None

    def lookup(self, block_addr: int) -> DirectoryCacheEntry:
        """Look up directory info, fetch from main directory on miss"""
        self.stats['accesses'] += 1

        # Check cache
        entry = self._find_entry(block_addr)
        if entry:
            self.stats['hits'] += 1
            return entry

        # Cache miss
        self.stats['misses'] += 1
        return self._fetch_from_main_directory(block_addr)

    def _fetch_from_main_directory(self, block_addr: int) -> DirectoryCacheEntry:
        """Fetch directory info from main memory and cache it"""
        set_idx = self._get_set_index(block_addr)

        # Get or create main directory entry
        if block_addr not in self.main_directory:
            self.main_directory[block_addr] = MainDirectoryEntry(
                DirectoryState.UNCACHED, set()
            )

        main_entry = self.main_directory[block_addr]

        # Create cache entry
        cache_entry = DirectoryCacheEntry(
            tag=block_addr,
            state=main_entry.state,
            sharers=main_entry.sharers.copy(),
            owner=main_entry.owner
        )

        # Evict if necessary
        if len(self.cache[set_idx]) >= self.ways:
            self._evict(set_idx)

        self.cache[set_idx].append(cache_entry)
        return cache_entry

    def _evict(self, set_idx: int):
        """Evict LRU entry"""
        entries = self.cache[set_idx]
        if not entries:
            return

        victim = entries.pop(0)  # Remove LRU
        self.stats['evictions'] += 1

        if victim.dirty:
            self._write_back_to_main_directory(victim)

    def _write_back_to_main_directory(self, entry: DirectoryCacheEntry):
        """Write dirty entry back to main directory"""
        if entry.tag not in self.main_directory:
            self.main_directory[entry.tag] = MainDirectoryEntry(
                entry.state, entry.sharers, entry.owner
            )
        else:
            main_entry = self.main_directory[entry.tag]
            main_entry.state = entry.state
            main_entry.sharers = entry.sharers
            main_entry.owner = entry.owner

        self.stats['write_backs'] += 1

    def process_read_request(self, block_addr: int,
                             requesting_node: int) -> Dict:
        """
        Process read request and return necessary actions
        """
        entry = self.lookup(block_addr)
        entry.dirty = True  # Will need to update main directory eventually

        result = {
            'data_source': None,  # 'memory', 'owner_node', or None
            'invalidations_needed': [],
            'new_state': None
        }

        if entry.state == DirectoryState.UNCACHED:
            # No one has it, get from memory
            entry.state = DirectoryState.EXCLUSIVE
            entry.sharers = {requesting_node}
            result['data_source'] = 'memory'
            result['new_state'] = DirectoryState.EXCLUSIVE

        elif entry.state == DirectoryState.SHARED:
            # Add to sharers, get from memory (or any sharer)
            entry.sharers.add(requesting_node)
            result['data_source'] = 'memory'
            result['new_state'] = DirectoryState.SHARED

        elif entry.state in [DirectoryState.EXCLUSIVE, DirectoryState.MODIFIED]:
            # Current owner has latest data
            if entry.owner != requesting_node:
                result['data_source'] = f'owner_node_{entry.owner}'

                if entry.state == DirectoryState.MODIFIED:
                    # Owner needs to flush data
                    pass

                entry.state = DirectoryState.SHARED
                entry.sharers = {entry.owner, requesting_node}
                result['new_state'] = DirectoryState.SHARED

        return result

    def process_write_request(self, block_addr: int,
                               requesting_node: int) -> Dict:
        """
        Process write request - invalidate other copies
        """
        entry = self.lookup(block_addr)
        entry.dirty = True

        result = {
            'data_source': None,
            'invalidations_needed': [],
            'new_state': DirectoryState.MODIFIED
        }

        # Collect nodes to invalidate
        nodes_to_invalidate = []

        if entry.state == DirectoryState.SHARED:
            nodes_to_invalidate = [n for n in entry.sharers
                                   if n != requesting_node]

        elif entry.state in [DirectoryState.EXCLUSIVE, DirectoryState.MODIFIED]:
            if entry.owner and entry.owner != requesting_node:
                nodes_to_invalidate = [entry.owner]
                result['data_source'] = f'owner_node_{entry.owner}'

        elif entry.state == DirectoryState.UNCACHED:
            result['data_source'] = 'memory'

        # Update directory
        entry.state = DirectoryState.MODIFIED
        entry.owner = requesting_node
        entry.sharers = {requesting_node}

        result['invalidations_needed'] = nodes_to_invalidate
        self.stats['invalidations_sent'] += len(nodes_to_invalidate)

        return result

    def get_hit_rate(self) -> float:
        if self.stats['accesses'] == 0:
            return 0.0
        return self.stats['hits'] / self.stats['accesses']

    def print_stats(self):
        print(f"\n=== 디렉터리 캐시 통계 ===")
        print(f"총 접근: {self.stats['accesses']}")
        print(f"적중: {self.stats['hits']}")
        print(f"미스: {self.stats['misses']}")
        print(f"적중률: {self.get_hit_rate():.2%}")
        print(f"교체: {self.stats['evictions']}")
        print(f"Write-back: {self.stats['write_backs']}")
        print(f"무효화 전송: {self.stats['invalidations_sent']}")

# 성능 시뮬레이션
def simulate_directory_cache_performance():
    """Simulate directory cache with varying sizes"""
    print("=" * 60)
    print("디렉터리 캐시 성능 시뮬레이션")
    print("=" * 60)

    for cache_size in [16, 64, 256, 1024]:
        num_sets = cache_size // 4  # 4-way
        dir_cache = DirectoryCache(num_sets=num_sets, ways=4, num_nodes=16)

        # Simulate random access pattern
        num_accesses = 10000
        working_set = 2000  # Memory blocks being accessed

        for _ in range(num_accesses):
            addr = random.randint(0, working_set - 1)
            node = random.randint(0, 15)

            if random.random() < 0.7:  # 70% reads
                dir_cache.process_read_request(addr, node)
            else:
                dir_cache.process_write_request(addr, node)

        print(f"\n캐시 크기: {cache_size} 엔트리")
        dir_cache.print_stats()

if __name__ == "__main__":
    simulate_directory_cache_performance()
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 디렉터리 캐시 구성 방식

| 구성 방식 | 적중률 | 지연시간 | 면적 | 전력 | 복잡도 |
|-----------|--------|----------|------|------|--------|
| **No Cache** | 0% | 100% | 최소 | 최소 | 낮음 |
| **Small (256-entry)** | 40-60% | -40% | 작음 | 낮음 | 낮음 |
| **Medium (1K-entry)** | 70-85% | -50% | 중간 | 중간 | 중간 |
| **Large (4K-entry)** | 85-95% | -55% | 큼 | 높음 | 높음 |
| **Multi-level** | 95%+ | -60% | 매우 큼 | 매우 높음 | 높음 |

### 디렉터리 캐시 vs 다른 일관성 최적화 기법

| 기법 | 추가 면적 | 지연 감소 | 확장성 | 적용 난이도 |
|------|-----------|-----------|--------|-------------|
| **Directory Cache** | +5-10% | 30-50% | 높음 | 중간 |
| **Snoop Filter** | +3-5% | 20-30% | 중간 | 낮음 |
| **Speculative Read** | 0% | 10-20% | 낮음 | 낮음 |
| **Migration** | 0% | 20-40% | 중간 | 높음 |

### 과목 융합 관점 분석

#### [컴퓨터구조 + OS] OS가 디렉터리 캐시에 미치는 영향
```
페이지 할당 정책과 디렉터리 캐시:

1. First-Touch Policy
   - 페이지를 처음 접근한 노드에 할당
   - 디렉터리 캐시의 지역성 향상

2. Page Coloring
   - 물리 페이지 색상과 디렉터리 캐시 인덱스 정렬
   - 캐시 충돌 감소

3. Page Migration
   - 접근 패턴 변화 시 페이지 이동
   - 디렉터리 캐시 갱신 필요

OS-하드웨어 협력:
- TLB shootdown 시 디렉터리 캐시 flush
- NUMA balancing과 디렉터리 부하 분산
```

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

#### 시나리오 1: 64코어 서버 CPU 설계
```
상황: 데이터센터용 64코어 ARM 서버
요구: 높은 메모리 일관성 성능

분석:
- 64코어에서 디렉터리 접근 빈도 높음
- 메인 디렉터리 지연이 전체 성능 제한

설계 결정:
1. 2-level 디렉터리 캐시
   - L1: 각 코어 클러스터 (256-entry)
   - L2: 메모리 컨트롤러 근처 (4K-entry)

2. 압축 공유 벡터
   - 64비트 전체 대신 Limited Pointer 사용
   - 평균 공유자 수 < 4이므로 효율적

3. Write-back 정책
   - dirty 엔트리만 교체 시 write-back
   - 전력 절감

기대 효과:
- 일관성 트랜잭션 지연 40% 감소
- 전체 성능 20% 향상
```

### 도입 시 고려사항 (체크리스트)

#### 기술적 고려사항
- [ ] 시스템 규모에 따른 디렉터리 캐시 크기
- [ ] 공유 벡터 표현 방식
- [ ] 교체 정책 선택
- [ ] 일관성 유지 방식

#### 운영/보안적 고려사항
- [ ] 디렉터리 캐시 오버플로우 대응
- [ ] 모니터링 및 성능 튜닝

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 개선 전 | 개선 후 | 향상률 |
|------|---------|---------|--------|
| 일관성 트랜잭션 지연 | 150ns | 80ns | -47% |
| 디렉터리 접근 전력 | 100mW | 60mW | -40% |
| 전체 시스템 성능 | 기준 | +20% | +20% |

### 미래 전망 및 진화 방향

1. **ML 기반 프리페칭**: 접근 패턴 학습으로 디렉터리 캐시 프리로드
2. **CXL 확장**: 분산 디렉터리 캐시
3. **3D 적층**: 메모리 근처 디렉터리 캐시 고속 연결

---

## 📌 관련 개념 맵 (Knowledge Graph)

1. [디렉터리 기반 프로토콜](../11_synchronization/404_directory_based_protocol.md) - 디렉터리 캐시가 최적화하는 대상
2. [캐시 일관성](../11_synchronization/402_cache_coherence.md) - 전체 시스템 일관성
3. [스누핑 버스 병목](./510_snooping_bus_bottleneck.md) - 디렉터리 방식이 해결하는 문제
4. [NUMA](../10_parallel/380_numa.md) - 분산 메모리 아키텍처
5. [MESI 프로토콜](../11_synchronization/407_mesi_protocol.md) - 기반 일관성 프로토콜

---

## 👶 어린이를 위한 3줄 비유 설명

1. **디렉터리 캐시가 뭐야?**: 학교에서 누가 어떤 책을 빌렸는지 적어둔 목록표예요. 큰 목록은 도서실에 있어서 보러 가기 멀어요.

2. **왜 캐시가 필요해요?**: 선생님 책상 위에 자주 빌리는 책들의 작은 목록을 적어두면, 매번 도서실까지 안 가도 돼요!

3. **어떻게 써요?**: 누가 책을 빌리면 작은 목록에도 적어두고, 나중에 큰 목록이랑 같아지게 해요. 그래서 빠르고 정확하게 누가 책을 가졌는지 알 수 있어요!
