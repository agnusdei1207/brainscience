+++
title = "377. LSM-Tree (Log-Structured Merge-Tree)"
date = "2026-03-05"
[extra]
categories = "studynotes-database"
+++

# 377. LSM-Tree (Log-Structured Merge-Tree) - 빅데이터의 폭발적인 쓰기 속도를 감당하는 마법

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 랜덤 쓰기(Random Write)를 순차 쓰기(Sequential Write)로 변환하여 **쓰기 성능(Throughput)을 극대화**하기 위해, 메모리에 데이터를 모았다가 정렬된 파일(SSTable) 형태로 디스크에 한꺼번에 내려쓰는 저장 엔진 구조다.
> 2. **혁신**: B-Tree가 디스크의 임의 위치를 찾아다니며 수정하는 오버헤드를 없애고, **MemTable(메모리), Commit Log(WAL), 그리고 다층 구조의 SSTable(디스크)**을 통해 쓰기 병목을 원천 차단한다.
> 3. **가치**: 카산드라(Cassandra), RocksDB, Bigtable 등 현대적인 NoSQL과 분산 DB의 표준 저장 엔진으로 쓰이며, 쓰기 요청이 읽기보다 압도적으로 많은 센서 데이터나 로그 수집 시스템의 핵심 인프라다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
LSM-Tree는 "디스크는 순차적으로 쓸 때 가장 빠르다"는 물리적 진리에 기반한다. 데이터를 바로 디스크에 쓰지 않고 일단 메모리(MemTable)에 정렬해서 모아둔다. 메모리가 차면 이를 통째로 디스크에 순차적으로 '부어버리는' 방식을 반복하여 쓰기 속도를 극한으로 높인다.

### 💡 비유
- **B-Tree (도서관 사서)**: 책이 한 권 들어올 때마다 서가로 달려가 가나다순 위치를 정확히 찾아 꽂는다. 책이 수천 권 들어오면 사서는 지쳐서 쓰러진다. (랜덤 I/O 부하).
- **LSM-Tree (택배 분류소)**: 물건이 오면 일단 바닥에 가나다순으로 차곡차곡 쌓아둔다(MemTable). 바닥이 꽉 차면 상자 하나에 담아 창고에 넣는다(SSTable). 나중에 상자가 많아지면(Compaction) 상자 여러 개를 열어 한 번에 큰 상자로 정리한다. 분류소 직원(CPU)은 제자리에서 정리만 하면 되니 엄청나게 많은 물건을 빨리 처리할 수 있다.

### 등장 배경: 'Write-Heavy' 워크로드
전통적인 B-Tree는 읽기는 빠르지만 쓰기 시 인덱스 페이지를 계속 갱신해야 하므로 디스크 헤더가 바쁘게 움직여야 했다. 소셜 미디어의 포스팅이나 IoT 센서 로그처럼 "읽기보다 쓰기가 100배 많은" 환경에서는 B-Tree가 한계를 보였고, 이를 극복하기 위해 1996년 패트릭 오닐에 의해 LSM-Tree가 제안되었다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### LSM-Tree 다층 구조 및 데이터 흐름 (ASCII Diagram)

```ascii
[ Write Request ] ───▶ [ WAL (Write Ahead Log) ] (장애 복구용)
          │
          ▼
[ MemTable (In-Memory) ] ── (Sort & SkipList)
          │
          │ (Flush when Full)
          ▼
[ Level 0 SSTable ] [ Level 0 SSTable ] (Overlap 존재)
          │
          │ (Compaction: Merge Sort)
          ▼
[ Level 1 SSTable ] ───────────────────▶ [ Level 2 SSTable ]
(정렬됨, No Overlap)                      (더 큰 용량)

* 핵심 과정:
1. Write: 메모리(MemTable)에 즉시 저장 (초고속).
2. Flush: 메모리가 차면 디스크에 SSTable(Sorted String Table)로 기록.
3. Compaction: 디스크의 작은 파일들을 병합하여 검색 효율 증대 및 중복 제거.
```

### 3대 핵심 구성 요소

#### ① MemTable & WAL
모든 데이터는 먼저 메모리 내의 **MemTable**(주로 SkipList나 Red-Black Tree)에 저장된다. 이때 전원 차단 시 데이터 유실을 막기 위해 디스크의 **WAL**(Commit Log)에 순차 기록을 병행한다.

#### ② SSTable (Sorted String Table)
메모리에서 내려온 불변(Immutable)의 파일이다. 데이터가 키(Key) 순서로 정렬되어 있어 검색과 병합이 매우 용이하다.

#### ③ 콤팩션 (Compaction) - [별도 주제 378번에서 상세]
여러 SSTable 파일들을 읽어 합치고, 정렬하고, 불필요한 데이터(Tombstone)를 지우는 과정이다. LSM-Tree의 읽기 성능을 보장하는 핵심 뒤처리 작업이다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### B-Tree vs LSM-Tree 상세 비교

| 구분 | B-Tree (전통적 RDBMS) | **LSM-Tree (현대적 NoSQL)** |
|:---:|:---|:---|
| **핵심 철학** | 제자리 업데이트 (Update-in-place) | **추가 전용 (Append-only)** |
| **쓰기 성능** | 보통 (랜덤 I/O 병목) | **극도로 우수 (순차 I/O)** |
| **읽기 성능** | **매우 우수 (단일 파일 탐색)** | 상대적으로 느림 (여러 계층 확인) |
| **디스크 효율** | 높음 (공간 즉시 재사용) | 낮음 (중복 데이터 존재, 콤팩션 필요) |
| **주 사용처** | Oracle, MySQL, PostgreSQL | **Cassandra, HBase, RocksDB** |
| **비유** | **정밀 조각** | **블록 쌓기** |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 로그 분석 플랫폼 엔진 선정 전략)

**상황**: 초당 100만 건의 웹 접속 로그를 실시간 수집하여 침입 탐지 AI를 돌려야 한다. DB 서버의 쓰기 대기(I/O Wait)가 너무 높아 데이터가 유실되고 있다.
**판단 및 저장 엔진 교체 전략**:
1. **엔진 전환**: 기존 B-Tree 기반 DB를 **LSM-Tree 엔진을 사용하는 Cassandra나 RocksDB**로 교체한다.
2. **읽기 최적화**: LSM-Tree의 약점인 읽기 지연을 줄이기 위해 **블룸 필터(Bloom Filter)**를 적극 활용한다. (파일을 열어보지 않고도 데이터 존재 여부 판단).
3. **콤팩션 전략 수립**: 쓰기가 너무 많으면 콤팩션이 밀려 시스템이 느려질 수 있다. **Size-Tiered** 또는 **Leveled Compaction** 옵션을 워크로드에 맞게 튜닝한다.
4. **결과**: I/O 병목 제거로 로그 유실율 0% 달성, 하드웨어 증설 없이 처리량 5배 향상.

### 안티패턴 및 고려사항
- **쓰기 증폭 (Write Amplification)**: LSM-Tree는 콤팩션 과정에서 데이터를 계속 다시 읽고 쓴다. SSD의 수명을 갉아먹는 주범이 될 수 있으므로, **SSD의 수명과 콤팩션 주기** 사이의 타협점을 잘 찾아야 한다.
- **읽기 증폭 (Read Amplification)**: 찾으려는 데이터가 최신 계층에 없으면 모든 레벨의 SSTable을 다 뒤져야 한다. 인덱스와 블룸 필터 관리가 부실하면 읽기 성능이 처참해진다.

---

## Ⅴ. 미래 전망 및 결론

### 결론: 빅데이터 시대를 연 물리적 통찰
LSM-Tree는 소프트웨어 아키텍처가 하드웨어의 물리적 특성(Sequential > Random)을 얼마나 영리하게 이용할 수 있는지 보여주는 모범 사례다. 데이터가 폭증할수록 LSM-Tree의 가치는 더욱 빛을 발한다.

### 미래 전망
앞으로는 **'NVM(비휘발성 메모리) 최적화 LSM-Tree'**가 등장할 것이다. WAL과 MemTable을 초고속 NVM에 직접 배치하여, Flush 과정조차 필요 없는 초저지연 저장 구조로 진화할 것이다. 또한, **ZNS(Zoned Namespace) SSD**와 결합하여, 하드웨어 레벨의 순차 쓰기 구역과 LSM-Tree의 SSTable 배치를 1:1로 매핑함으로써 쓰기 증폭을 제로화하는 진정한 소프트웨어-하드웨어 협력 설계가 표준이 될 전망이다.

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [콤팩션 (Compaction)](./378_compaction.md) - LSM-Tree의 집 청소 기술
- [SSTable (Sorted String Table)](../../5_database/6_nosql/sstable_detail.md) - 디스크에 저장되는 데이터의 물리적 형태
- [블룸 필터 (Bloom Filter)](../../8_algorithm_stats/bloom_filter.md) - LSM-Tree 검색 속도를 100배 높여주는 확률적 자료구조
- [B-Tree 인덱스](../../5_database/5_indexing/200_b_tree.md) - LSM-Tree와 영원히 비교되는 전통의 강자

---

## 👶 어린이를 위한 3줄 비유 설명
1. **LSM-Tree가 뭔가요?**: 일기장에 글을 쓸 때, 매번 첫 페이지부터 빈틈을 찾아 쓰는 게 아니라 무조건 맨 뒷장에 이어서 쭉쭉 써 내려가는 방법이에요.
2. **왜 그렇게 하나요?**: 빈틈을 찾는 시간보다 그냥 뒤에 붙여 쓰는 게 훨씬 빠르기 때문이에요.
3. **나중에 찾을 때는요?**: 일기장이 꽉 차면 비슷한 내용끼리 모아서 예쁘게 정리(콤팩션)해 두기 때문에, 나중에 찾는 것도 어렵지 않답니다!
