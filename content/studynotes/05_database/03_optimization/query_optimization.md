+++
title = "데이터베이스 질의 최적화 (Query Optimization) 및 실행 계획 분석"
description = "RBO와 CBO의 아키텍처 비교, SQL 실행 계획(Execution Plan) 생성 원리, 그리고 Hash/Merge/Nested Loop 조인 알고리즘 심층 분석"
date = 2024-05-18
updated = 2024-05-18
weight = 10
categories = ["studynotes-05_database"]
+++

# [데이터베이스 질의 최적화 및 실행 계획]
#### ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 사용자가 작성한 선언적 언어(SQL)를 DBMS가 물리적인 디스크 I/O와 CPU 연산을 통해 데이터를 추출할 수 있는 **가장 비용이 적게 드는 절차적 실행 경로(Execution Plan)로 변환하는 지능형 컴파일 과정**입니다.
> 2. **가치**: 대용량 데이터 환경에서 최적화기(Optimizer)의 똑똑한 경로 선택 하나가 수 시간 걸릴 쿼리를 수 밀리초(ms) 단위로 단축시켜, 전체 시스템의 처리량(Throughput)과 응답성(Latency)을 결정짓는 핵심 엔진 역할을 합니다.
> 3. **융합**: 최신 옵티마이저는 단순한 통계 정보 기반의 비용 기반 최적화(CBO)를 넘어, 머신러닝(ML)을 도입하여 쿼리 실행 중 통계를 동적으로 보정(Adaptive Query Optimization)하고, 운영체제의 디스크 블록 캐싱 전략(LRU)과 긴밀하게 연계되어 동작합니다.

---

### Ⅰ. 개요 (Context & Background)

- **개념**: 
  - **옵티마이저 (Optimizer)**: SQL 문장의 문법/의미를 분석한 후, 테이블의 데이터 분포도(Statistics), 인덱스 유무, 시스템의 물리적 자원(I/O 속도, CPU)을 종합적으로 고려하여 가장 효율적인 데이터 검색 경로(실행 계획, Execution Plan)를 결정하는 DBMS의 핵심 두뇌입니다.
  - **실행 계획 (Execution Plan)**: 옵티마이저가 생성한 '데이터베이스 엔진의 작업 지시서'로, 어떤 테이블을 먼저 읽을지(Join Order), 인덱스를 탈지 풀 스캔을 할지(Access Path), 조인 방식은 무엇을 쓸지(Join Method)를 명시한 트리(Tree) 구조의 절차서입니다.
- **💡 비유**: 서울에서 부산으로 가는 길찾기(내비게이션)와 같습니다. SQL이 "부산으로 가자"라는 목적지(결과)를 말하는 것이라면, 옵티마이저는 내비게이션 앱입니다. 과거의 내비게이션(RBO)은 무조건 "고속도로 우선"이라는 정해진 규칙만 따랐다면, 현대의 내비게이션(CBO)은 실시간 교통 체증, 톨게이트 비용, 주유비(통계 정보)를 모두 계산해 가장 빨리 도착하는 길(실행 계획)을 안내합니다.
- **등장 배경 및 발전 과정**: 
  1. **휴리스틱 최적화의 한계 (RBO)**: 초기의 관계형 데이터베이스는 개발자가 정해놓은 일련의 우선순위 규칙(Rule-Based Optimizer)에 따라 실행 계획을 생성했습니다. 예를 들어 "인덱스가 있으면 무조건 탄다"라는 식이었으나, 데이터가 수천만 건일 때 인덱스를 타는 것이 오히려 디스크 Random I/O를 발생시켜 Full Table Scan(Sequential I/O)보다 훨씬 느려지는 치명적 한계가 존재했습니다.
  2. **패러다임의 변화 (CBO의 등장)**: 이를 극복하기 위해 테이블의 레코드 수, 블록 수, 컬럼의 데이터 분포(Histogram) 등의 메타데이터를 수집하고, 이를 바탕으로 수학적인 비용(Cost: I/O + CPU 연산량)을 계산하여 최적의 경로를 찾는 비용 기반 최적화(Cost-Based Optimizer)가 표준으로 자리 잡았습니다.
  3. **비즈니스적 요구사항**: 복잡한 조인과 서브쿼리가 난무하는 데이터 웨어하우스(DW) 환경 및 트랜잭션이 폭주하는 OLTP 환경에서 개발자의 SQL 작성 역량에 의존하지 않고 시스템 스스로 최적의 성능을 보장해야 하는 요구가 커졌습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 옵티마이저 파싱 및 최적화 아키텍처 구성 요소

| 구성 요소 (Module) | 상세 역할 | 내부 동작 메커니즘 | 관련 알고리즘/자료구조 |
|---|---|---|---|
| **SQL Parser** | 구문 분석 및 트리 생성 | SQL의 문법적 오류(Syntax)와 객체 존재 여부(Semantic)를 확인하고 파스 트리(Parse Tree) 생성 | Lexical Analysis, AST |
| **Query Transformer** | 쿼리 변환 및 재작성 | 뷰 병합(View Merging), 서브쿼리 언네스팅(Subquery Unnesting) 등 옵티마이저가 처리하기 쉬운 형태로 SQL을 동치 변환 | 휴리스틱 룰 기반 변환 |
| **Estimator (비용 산정기)** | 통계 기반 비용 계산 | 딕셔너리에 저장된 테이블/인덱스 통계 정보를 읽어 각 실행 경로의 예상 비용(Cost), 선택도(Selectivity), 카디널리티(Cardinality) 산출 | Histogram 분석, 확률 모델 |
| **Plan Generator (계획 생성기)** | 최적 경로 탐색 | 가능한 모든 조인 순서와 접근 경로를 조합하여 수많은 실행 계획 후보군(Search Space)을 생성하고 최소 비용의 트리를 선택 | Dynamic Programming, Greedy 알고리즘 |
| **Row Source Generator** | 실행 엔진 코드 생성 | 선택된 논리적 실행 계획을 DB 엔진이 실제로 실행할 수 있는 물리적 코드(Iterators) 포맷으로 변환 | Volcano Iterator Model |

#### 2. SQL 실행 계획(Execution Plan) 트리 다이어그램

```text
[ CBO 기반 SQL 파싱 및 실행 계획 생성 과정 (A JOIN B JOIN C) ]

[SQL Query] : SELECT * FROM EMP e JOIN DEPT d ON e.deptno = d.deptno WHERE e.sal > 3000;

1. Parser & Transformer ---> [ Standardized Parse Tree ]
                                       |
2. Estimator & Plan Generator (CBO Search Space Exploration)
   +---------------------------------------------------------------------------------+
   |  [ 통계 정보 (Data Dictionary) ]                                                  |
   |   - EMP: 1,000,000 rows, sal 컬럼 Histogram (Selectivity: 0.05)                 |
   |   - DEPT: 100 rows, deptno (PK Index)                                           |
   +---------------------------------------------------------------------------------+
                                       |
   (수백 개의 후보 플랜 중 최소 Cost 선택 과정)
   Plan A: Hash Join (Cost: 500)   vs   Plan B: Nested Loop Join (Cost: 1500)
                                       |
3. Selected Optimal Execution Plan (Tree Structure)
   
        [ SELECT STATEMENT ]  (Cost=505, Rows=50,000)
                 |
        [ HASH JOIN ]  (Cost=505, Rows=50,000, Bytes=...)  <-- (Row Source Iterator)
             /       \
           /           \
 [ TABLE ACCESS ]   [ TABLE ACCESS ]
 [  FULL (DEPT) ]   [ BY INDEX ROWID (EMP) ] <-- (Index Range Scan 후 Table Access)
  (Cost=3, Rows=100)        |
                    [ INDEX RANGE SCAN ]
                    [  (EMP_SAL_IDX)   ]
                    (Condition: sal > 3000)
                    (Cost=150, Rows=50,000)
```

#### 3. 심층 동작 원리: 3대 물리적 조인(Join) 알고리즘 메커니즘
옵티마이저가 두 테이블을 조인할 때 선택하는 핵심 물리 알고리즘입니다.

1. **Nested Loop Join (NL Join)**
   - **동작 방식**: 외부 테이블(Driving Table)에서 조건을 만족하는 첫 번째 행을 찾은 후, 내부 테이블(Driven Table)에서 조인 키를 이용해 매칭되는 행을 찾는 과정을 이중 FOR 루프처럼 반복합니다.
   - **핵심 조건**: 내부 테이블의 조인 컬럼에 **반드시 인덱스**가 있어야 성능이 보장됩니다.
   - **적합성**: OLTP 환경에서 조회되는 데이터 양이 적을 때(좁은 범위의 스캔) 가장 빠르고, 첫 번째 결과(First Row)를 즉시 반환(응답성 최고)합니다.

2. **Sort Merge Join**
   - **동작 방식**: 두 테이블을 각각 조인 컬럼 기준으로 정렬(Sort)한 후, 스캔해가며(Merge) 조인을 수행합니다.
   - **핵심 조건**: 정렬을 위한 메모리(Sort Area) 공간이 필요합니다.
   - **적합성**: 조인 컬럼에 인덱스가 없으면서 대량의 데이터를 조인할 때, 혹은 비동등 조인(`<`, `>`, `BETWEEN`)이 필요할 때 Hash Join의 대안으로 사용됩니다.

3. **Hash Join**
   - **동작 방식**: 크기가 작은 테이블(Build Input)을 먼저 읽어 메모리(Hash Area)에 조인 키를 해시 함수로 돌려 **해시 테이블(Hash Map)**을 생성합니다. 그 후 큰 테이블(Probe Input)을 Full Scan 하면서 조인 키를 동일한 해시 함수에 넣어 해시 테이블을 탐색(Probe)하며 조인합니다.
   - **핵심 조건**: 메모리 내에 해시 테이블을 올릴 수 있는 충분한 PGA(PGA in Oracle, work_mem in PostgreSQL) 공간이 필요하며, 동등 조인(`=`)에서만 사용 가능합니다.
   - **적합성**: 대용량 데이터 웨어하우스(DW) 환경이나 통계 분석 쿼리에서 가장 강력한 성능을 발휘합니다. 인덱스 여부와 무관하게 대량의 데이터를 Sequential I/O로 빠르게 처리합니다.

#### 4. 핵심 수학적 모델: CBO 비용(Cost) 산정 및 선택도(Selectivity) 공식
옵티마이저는 조건절이 반환할 데이터의 비율인 **선택도(Selectivity)**를 계산하여 카디널리티(결과 건수)를 추정합니다.
$$ \text{Selectivity} = \frac{1}{\text{NDV (Number of Distinct Values)}} $$
예: `WHERE gender = 'M'`일 때, `gender` 컬럼의 NDV가 2('M', 'F')라면 선택도는 $1/2 = 0.5$ (50%)입니다.

**카디널리티(Cardinality) 산출 공식:**
$$ \text{Cardinality} = \text{Total Rows in Table} \times \text{Selectivity} $$

**Index Scan Cost 모델 (단순화):**
$$ \text{Cost}_{Index} = \text{BTree Level} + (\text{Index Leaf Blocks} \times \text{Selectivity}) + (\text{Table Clustering Factor} \times \text{Selectivity}) $$
- **Clustering Factor (군집도)**: 인덱스의 순서와 테이블의 물리적 데이터 저장 순서가 얼마나 일치하는지를 나타내는 지표. CF가 나쁘면(테이블 블록 랜덤 I/O 급증), 옵티마이저는 인덱스 스캔을 포기하고 Full Table Scan을 선택하게 됩니다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 옵티마이저 아키텍처 비교 (RBO vs CBO)

| 평가 지표 | RBO (Rule-Based Optimizer) | CBO (Cost-Based Optimizer) |
|---|---|---|
| **의사 결정 기준** | 하드코딩된 규칙의 우선순위 (예: ROWID > PK > Index > Full Scan) | I/O, CPU, 메모리 자원 소모의 수학적 예상 **비용(Cost)** |
| **통계 정보 활용** | 전혀 사용하지 않음 | 테이블 로우 수, 블록 수, 인덱스 높이, 데이터 히스토그램 필수 |
| **데이터 분포 대응** | 불가능 (데이터가 1건이든 1억 건이든 인덱스가 있으면 탐) | 매우 유연함 (데이터가 많아 임계점을 넘으면 스스로 Full Scan 선택) |
| **관리 포인트** | 쿼리 작성 시 힌트(Hint)나 문법적 순서에 크게 의존 | 통계 정보의 주기적인 갱신(Analyze, Gather Stats)이 필수 |

#### 2. 과목 융합 관점 분석 (컴퓨터 구조 및 운영체제)
- **메모리 계층 및 I/O 융합**: 옵티마이저가 Hash Join을 선택했을 때, 해시 테이블이 작아 L1/L2 Cache에 적재될 수 있다면 CPU 사이클은 극단적으로 단축됩니다. 반면 해시 테이블이 DB에 할당된 메모리(PGA)를 초과하면, OS의 가상 메모리 스왑(Swap) 대신 DB 엔진이 임시 테이블스페이스(디스크)로 데이터를 쏟아내는 **Spill-to-Disk** 현상이 발생하여 성능이 수십 배 하락합니다. 옵티마이저는 이 메모리 임계값을 사전에 계산(Costing)하여 플랜을 결정합니다.
- **디스크 블록 스캔 및 OS 파일 시스템**: Full Table Scan은 언뜻 느려 보이나, OS와 스토리지가 제공하는 **다중 블록 읽기(Multi-Block Read, Read-Ahead)** 및 순차적 I/O(Sequential I/O) 하드웨어 가속을 최대한 활용합니다. CBO는 디스크의 단일 블록을 읽는 Random I/O(Index Scan) 비용과 멀티 블록 단위로 읽는 Sequential I/O(Full Scan) 비용을 디스크 스펙 기반으로 저울질합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오: 대용량 결제 데이터 통계 쿼리 타임아웃 장애)
- **문제 상황 (Scenario)**: 매일 밤 12시에 실행되는 '일일 결제 내역 통계 배치 배치 쿼리(결제 테이블 5천만 건 JOIN 유저 테이블 1천만 건)'가 기존에는 10분 만에 끝났으나, 특정일 이후 2시간이 넘게 걸리며 시스템 장애를 유발했습니다.
- **아키텍트의 전략적 의사결정**:
  1. **실행 계획(Execution Plan) 분석 및 병목 도출**: `EXPLAIN PLAN`을 확인한 결과, 기존에 `Hash Join`으로 동작하던 플랜이 `Nested Loop Join`으로 변형되어, 5천만 번의 Random I/O를 발생시키고 있음을 확인했습니다.
  2. **원인 파악 (통계 정보 누락)**: 일주일 전 대량의 데이터 마이그레이션이 있었으나, CBO를 위한 통계 정보 갱신(Gather Statistics) 작업이 수행되지 않아, 옵티마이저가 결제 테이블의 로우 수를 100건으로 잘못 인지(Estimation Error)하여 NL Join이 유리하다고 판단한 것이 원인이었습니다.
  3. **조치 및 최적화**: 
     - **단기 조치**: 쿼리에 `/*+ USE_HASH(pay user) */` 힌트를 강제로 주입하여 즉각적으로 Hash Join으로 유도해 장애를 해소합니다.
     - **근본 조치**: DB 스케줄러에 데이터 대량 변동 시 즉시 통계 정보를 재수집하는 작업을 등록하고, 히스토그램(Histogram) 버킷 수를 늘려 데이터 편향(Data Skew)에 CBO가 적절히 대응할 수 있도록 아키텍처를 보강합니다.

#### 2. 도입 시 고려사항 및 안티패턴 (Anti-patterns)
- **Bind Variable Peeking 결함**: 애플리케이션에서 하드파싱을 줄이기 위해 바인드 변수(`WHERE age = :v`)를 사용합니다. 이때 CBO는 쿼리 최초 실행 시 들어온 바인드 변수의 값을 슬쩍 훔쳐보고(Peeking) 실행 계획을 세워버립니다. 만약 첫 변수가 선택도가 1%인 값이었고 나중에 들어온 값이 99%인 값이라면, 1%에 맞춰진 잘못된 Index Scan 계획이 캐싱되어 전체 시스템이 마비될 수 있습니다. 이를 방지하기 위해 `Adaptive Cursor Sharing` 기능을 활용하거나, 데이터 분포가 극단적인 컬럼에는 바인드 변수 대신 리터럴 값을 사용하는 예외 원칙을 세워야 합니다.
- **의미 없는 인덱스 떡칠(Anti-pattern)**: 조회 성능을 높이겠다며 테이블의 거의 모든 컬럼에 인덱스를 생성하는 것은 최악의 안티패턴입니다. 이는 INSERT/UPDATE/DELETE 시 트랜잭션 오버헤드를 유발할 뿐만 아니라, 옵티마이저가 경로를 탐색(Search Space)할 때 경우의 수가 기하급수적으로 늘어나 SQL 파싱 타임(CPU 소모) 자체를 크게 지연시킵니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과 (ROI)
| 구분 | 튜닝 전 (비효율적 실행 계획) | 최적화 후 (CBO 및 인덱스 튜닝) | 개선 효과 (ROI) |
|---|---|---|---|
| **배치 처리 시간** | 1억 건 NL Join (수 시간 소요) | Hash Join & 병렬 처리 (수 분 내 완료) | 배치 윈도우(Batch Window) **90% 단축** |
| **디스크 I/O (Buffer Gets)** | 인덱스 랜덤 액세스로 수백만 블록 읽기 | 클러스터링 팩터 개선 및 Index Only Scan | 블록 읽기 횟수 **1/1000 수준으로 감소** |
| **CPU 자원 소모** | 잘못된 암시적 형변환으로 지속적 CPU 스파이크 | 조건절 재작성을 통한 인덱스 정상 사용 | DB 서버 CPU 사용률 평균 **40% 안정화** |

#### 2. 미래 전망 (AI 기반 자율 최적화, Autonomous Database)
현대의 옵티마이저는 단순히 정적인 통계 정보에 의존하는 것을 넘어섭니다. 오라클의 `Autonomous Database`나 AWS의 무중단 튜닝 기능처럼, 쿼리가 실행되는 도중에 메모리 사용량과 실제 카디널리티를 모니터링하여 실시간으로 실행 계획을 바꾸는 **적응형 질의 최적화(Adaptive Query Optimization)**가 고도화되고 있습니다. 향후에는 머신러닝(딥러닝 강화학습)이 탑재된 옵티마이저가 쿼리 패턴을 스스로 학습하여, DBA의 개입 없이 최적의 인덱스를 자동 생성하고 소멸시키는 'Zero DBA' 시대로 진화할 것입니다.

#### 3. 관련 표준 및 규격
- **SQL:2016 (ISO/IEC 9075)**: 표준 SQL 규격. 옵티마이저의 구현은 벤더(Oracle, MS, PostgreSQL) 고유의 영업 기밀이나, 쿼리 변환 시 지켜야 할 관계 대수 동치성 표준을 따름.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- [`[RAID 아키텍처]`](@/studynotes/01_computer_architecture/08_storage/_index.md): 옵티마이저가 Full Table Scan의 비용을 계산할 때 스토리지의 디스크 스트라이핑(RAID 0)으로 인한 순차 I/O 성능 향상을 고려함.
- [`@/studynotes/02_operating_system/07_virtual_memory/_index.md`](@/studynotes/02_operating_system/07_virtual_memory/_index.md): DB 엔진이 인덱스 블록을 메모리(Buffer Cache)에 적재할 때 사용하는 LRU 알고리즘 원리.
- [`@/studynotes/08_algorithm_stats/01_sorting/_index.md`](@/studynotes/08_algorithm_stats/01_sorting/_index.md): B+Tree 인덱스의 탐색 복잡도(O(log N))와 Hash Join에서의 해시 맵 검색 복잡도(O(1)) 비교.
- [`@/studynotes/05_database/04_dw_olap/data_warehouse_olap.md`](@/studynotes/05_database/04_dw_olap/data_warehouse_olap.md): DW 환경에서의 대량 데이터 분석을 위해 Hash Join이 어떻게 활용되는지 연계.
- [`@/studynotes/10_ai/01_dl/_index.md`](@/studynotes/10_ai/01_dl/_index.md): 향후 머신러닝 기반 쿼리 옵티마이저(Learned Optimizer)로의 발전 방향.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **옵티마이저란?**: 엄마한테 심부름으로 "슈퍼에서 우유랑 계란 사와"라고 듣고(SQL 쿼리), 어떤 길로 가서(경로) 무엇부터 바구니에 담을지 가장 빠르고 덜 힘든 방법을 머릿속으로 계산하는 '똑똑한 내비게이션'이에요.
2. **실행 계획 (Execution Plan)**: 내비게이션이 고민을 끝내고 "1번: 큰길로 나가라 -> 2번: 횡단보도를 건너라 -> 3번: 우유 먼저 집어라"라고 단계별로 적어준 보물지도 같은 설명서랍니다.
3. **조인 알고리즘(Hash Join)**: 두 학교의 학생 명부를 합칠 때, 한 명 한 명 찾아다니며 물어보는 대신(NL Join), 반별로 이름표(Hash)를 만들어 바구니에 던져 넣고 한 번에 짝을 찾는 엄청나게 빠른 마법의 정렬 방법이에요.
