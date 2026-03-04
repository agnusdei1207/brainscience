+++
title = "데이터베이스 정규화 (Normalization)"
date = "2026-03-04"
[extra]
categories = "studynotes-database"
+++

# 데이터베이스 정규화 (Database Normalization)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 관계형 데이터베이스(RDBMS) 설계에서 데이터 중복을 제거하고 함수적 종속성(Functional Dependency)을 기반으로 테이블을 무손실 분해(Lossless Decomposition)하여 데이터의 무결성을 보장하는 논리적 프로세스입니다.
> 2. **가치**: 삽입, 삭제, 갱신 시 발생하는 이상 현상(Anomaly)을 근본적으로 차단하고, 저장 공간의 효율적 사용과 데이터 구조의 유연성을 확보하여 엔터프라이즈 시스템의 신뢰성을 극대화합니다.
> 3. **융합**: 고성능 트랜잭션 처리를 위한 정규화와 대규모 데이터 분석을 위한 반정규화(Denormalization) 전략의 적절한 트레이드오프(Trade-off) 관리는 현대 하이브리드 데이터 플랫폼 아키텍처의 핵심 성공 요소입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**데이터베이스 정규화(Normalization)**란 관계형 데이터베이스 설계 과정에서 데이터의 중복을 최소화하고 일관성을 유지하기 위해 테이블(릴레이션)을 논리적으로 구조화하는 체계적인 방법론입니다. 이는 수학적인 집합 이론과 함수적 종속성(Functional Dependency)을 근간으로 하며, 잘못된 데이터 모델링으로 인해 발생할 수 있는 데이터의 불일치와 저장 공간의 낭비를 방지하는 데이터 아키텍처의 핵심 설계 원칙입니다.

#### 2. 💡 비유를 통한 이해
정규화는 **'옷장 정리'**에 비유할 수 있습니다.
- **비정규화된 상태**: 한 서랍에 양말, 티셔츠, 바지, 액세서리를 마구 섞어 넣은 상태입니다. 양말 하나를 찾으려 해도 서랍 전체를 뒤져야 하고(성능 저하), 바지를 버리려다가 같이 껴 있던 소중한 반지를 잃어버릴 수도 있으며(삭제 이상), 똑같은 티셔츠가 여러 벌 있다는 사실을 모르고 또 살 수도 있습니다(중복).
- **정규화된 상태**: 양말 칸, 상의 칸, 하의 칸, 보석함으로 용도별로 서랍을 나누는 것입니다. 이제 양말을 찾을 때는 양말 칸만 열면 되고, 바지를 버려도 반지는 보석함에 안전하게 보관됩니다. 각각의 물건이 '있어야 할 자리'에 하나씩만 존재하게 하는 것, 그것이 정규화의 본질입니다.

#### 3. 등장 배경 및 발전 과정
1.  **기존 기술의 치명적 한계점 (이상 현상, Anomalies)**: 초기 데이터베이스 시스템에서는 모든 데이터를 하나의 거대한 파일이나 테이블에 담으려 했습니다. 이로 인해 특정 부서의 이름을 바꾸려면 수천 명의 사원 데이터를 일일이 고쳐야 했고(갱신 이상), 새로운 부서를 만들려면 아직 뽑지도 않은 사원 정보를 억지로 넣어야 했으며(삽입 이상), 사원을 한 명 해고했는데 그 부서의 유일한 정보까지 사라지는(삭제 이상) 치명적인 데이터 부패 현상이 발생했습니다.
2.  **혁신적 패러다임의 도입**: 1970년 E.F. Codd 박사는 관계형 모델을 발표하며 정규화 이론의 기초인 1NF, 2NF, 3NF를 정립했습니다. 이후 Raymond F. Boyce와 함께 더욱 강력한 BCNF를 발표하며 복잡한 다중 후보키 상황에서의 무결성 문제를 해결했습니다.
3.  **현대적 요구사항**: 클라우드 기반의 대규모 분산 시스템과 MSA(Microservices Architecture) 환경에서도 데이터의 'Single Source of Truth'를 확보하는 것은 시스템 간 정합성 유지의 필수 조건입니다. 이에 따라 정규화는 단순히 DB 설계를 넘어 정보 설계 전체의 표준 가이드라인으로 기능하고 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 정규화의 핵심 개념: 함수적 종속성 (Functional Dependency) (표)

| 개념 | 상세 역할 | 내부 동작 메커니즘 | 관련 특징 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **결정자 (Determinant)** | 다른 속성을 고유하게 결정하는 속성 | X -> Y 관계에서 X에 해당 | 기본키(PK)의 근간 | 기차의 '열차 번호' |
| **완전 함수 종속 (FFD)** | 기본키 전체에만 종속됨 | 복합키 {A, B} 전체가 있어야 C 결정 | 제2정규형의 판단 기준 | '성명+생년월일'로 사람 특정 |
| **부분 함수 종속 (PFD)** | 기본키의 일부에만 종속됨 | 복합키 {A, B} 중 A만으로도 C 결정 | 중복과 이상 현상의 주범 | '학번'만으로 '이름'이 나옴 |
| **이행적 함수 종속 (TFD)** | 제3의 속성을 매개로 종속됨 | A -> B 이고 B -> C 이면 A -> C | 제3정규형의 제거 대상 | '주소'를 알면 '우편번호'를 앎 |
| **다치 종속 (MVD)** | 하나의 결정자가 여러 값을 가짐 | A ->> B 형태 (독립적인 다중 값) | 제4정규형의 타겟 | '한 사원'이 '여러 취미' 보유 |

#### 2. 정규화 단계별 변환 아키텍처 및 흐름 다이어그램

```text
<<< Database Normalization Step-by-Step Architecture >>>

[ Unnormalized Relation ] (Multi-valued attributes, repeating groups)
          |
          | (1) Remove repeating groups, make attributes atomic
          v
[ 1st Normal Form (1NF) ] (All attributes are atomic)
          |
          | (2) Remove Partial Functional Dependencies (PK is fully determinant)
          v
[ 2nd Normal Form (2NF) ] (No partial functional dependency)
          |
          | (3) Remove Transitive Functional Dependencies (Non-key to Non-key)
          v
[ 3rd Normal Form (3NF) ] (No transitive functional dependency)
          |
          | (4) Every Determinant must be a Candidate Key
          v
[ Boyce-Codd Normal Form (BCNF) ] (Strong 3NF)
          |
          | (5) Remove Multi-valued Dependencies (A ->> B)
          v
[ 4th Normal Form (4NF) ]
          |
          | (6) Remove Join Dependencies
          v
[ 5th Normal Form (5NF) ] (Ultimate normalization state)

<<< Normalization Visualization: 1NF to 3NF >>>

     [ Table: Orders ]
     PK: {OrderID, ProductID}
     ----------------------------------------------------------
     | OrderID | ProductID | Qty | CustName | CustCity |
     ----------------------------------------------------------
          ^           ^       |       |          |
          |           |       |       |          +---- [Z] City
          |           |       |       +--------------- [Y] Name
          |           +-------|----------------------- [X] Product Info
          +-------------------+----------------------- [W] Order Info

     1. Part of PK {OrderID} -> {CustName, CustCity} : Partial Dependency (PFD)
     2. {CustName} -> {CustCity} : Transitive Dependency (TFD)
```

#### 3. 심층 동작 원리: 무손실 분해와 종속성 보존
정규화는 단순히 테이블을 쪼개는 것이 아니라, 두 가지 수학적 조건을 만족해야 합니다.
1.  **무손실 분해 (Lossless Join Decomposition)**: 테이블 R을 R1과 R2로 분해했을 때, R1 ⨝ R2 (Natural Join)의 결과가 원래의 R과 정확히 일치해야 합니다. 만약 분해 후 조인했을 때 '가짜 튜플(Spurious Tuples)'이 생긴다면 이는 잘못된 정규화입니다.
2.  **종속성 보존 (Dependency Preservation)**: 원래 테이블 R에서 존재하던 모든 함수적 종속성이 분해된 결과인 R1, R2, ..., Rn에서도 그대로 유지되어야 합니다. 이는 데이터 무결성 검증을 위한 제약 조건 체크 비용을 최소화하기 위함입니다.

#### 4. 실무 수준의 정규화 구현 및 검증 SQL (PostgreSQL 예시)

```sql
-- [Scenario] 주문 시스템의 비정규화 테이블을 3NF로 정규화하는 과정

-- 0. 비정규화된 초기 테이블 (1NF 상태라고 가정하지만 설계 결함 존재)
CREATE TABLE raw_orders (
    order_id INT,
    product_id INT,
    order_date DATE,
    customer_id INT,
    customer_name VARCHAR(100),
    customer_city VARCHAR(50),
    quantity INT,
    unit_price DECIMAL(10, 2),
    PRIMARY KEY (order_id, product_id)
);

-- 1. 제2정규형 (2NF): 부분 함수 종속 제거
-- {order_id, product_id} -> {quantity} (FFD)
-- {order_id} -> {order_date, customer_id, customer_name, customer_city} (PFD)
-- {product_id} -> {unit_price} (PFD)

-- [분리 1] 주문 마스터 (주문에 종속된 정보)
CREATE TABLE orders_m (
    order_id INT PRIMARY KEY,
    order_date DATE,
    customer_id INT,
    customer_name VARCHAR(100),
    customer_city VARCHAR(50)
);

-- [분리 2] 주문 상세 (복합키 전체에 종속된 정보)
CREATE TABLE order_details (
    order_id INT REFERENCES orders_m(order_id),
    product_id INT,
    quantity INT,
    PRIMARY KEY (order_id, product_id)
);

-- 2. 제3정규형 (3NF): 이행적 함수 종속 제거
-- orders_m 테이블에서: order_id -> customer_id -> {customer_name, customer_city}
-- customer_id가 결정자이지만 PK가 아니므로 분리 필요

-- [최종 분리] 고객 테이블
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100),
    customer_city VARCHAR(50)
);

-- [수정] 주문 마스터에서 고객 정보 제거하고 FK만 유지
ALTER TABLE orders_m DROP COLUMN customer_name;
ALTER TABLE orders_m DROP COLUMN customer_city;
ALTER TABLE orders_m ADD CONSTRAINT fk_customer 
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id);

-- [검증 쿼리] 무손실 조인 확인
SELECT *
FROM orders_m o
JOIN order_details d ON o.order_id = d.order_id
JOIN customers c ON o.customer_id = c.customer_id;
-- 결과가 raw_orders와 동일한 행을 반환하는지 확인
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 정규화 vs 반정규화 (Normalization vs Denormalization)

| 비교 항목 | 정규화 (Normalization) | 반정규화 (Denormalization) |
| :--- | :--- | :--- |
| **목표** | 데이터 정합성, 유연성, 중복 제거 | 조회 성능 향상, 시스템 부하 감소 |
| **주요 대상** | OLTP (실시간 트랜잭션 시스템) | OLAP (데이터 웨어하우스, 대용량 분석) |
| **장점** | 이상 현상 방지, 저장 공간 절약, 설계 명확 | JOIN 연산 감소로 응답 속도 비약적 향상 |
| **단점** | JOIN 증가로 인한 복잡한 조회 쿼리 성능 저하 | 데이터 불일치 위험(Update Anomaly), 용량 증가 |
| **데이터 구조** | 좁고 깊은 테이블 (Narrow & Deep) | 넓고 얕은 테이블 (Wide & Shallow) |

#### 2. OS 및 개발 패러다임 융합 관점 분석
- **OS 캐시 및 I/O 효율성**: 정규화된 테이블은 레코드의 길이가 짧아 한 번의 디스크 블록 읽기(Disk Block Read) 시 더 많은 레코드를 메모리(Buffer Pool)에 올릴 수 있습니다. 이는 Full Table Scan 시 OS의 페이지 캐시 히트율을 높이는 효과를 줍니다. 반면, 지나친 정규화로 인한 조인은 랜덤 I/O를 유발할 수 있습니다.
- **객체 지향 프로그래밍 (OOP)과의 매핑**: 정규화 이론은 객체 지향의 **단일 책임 원칙 (SRP)**과 궤를 같이 합니다. 하나의 테이블이 하나의 엔티티(Entity)만 책임지게 하는 것은 애플리케이션 레벨의 ORM(Object-Relational Mapping) 구현 시 객체 그래프의 명확성을 확보해 줍니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)
- **시나리오 1: 뱅킹 시스템의 계좌 및 거래 내역 설계**
  - 상황: 하루 수억 건의 거래가 발생하는 시스템.
  - 판단: 거래 내역은 절대적인 무결성이 필요하므로 BCNF 수준까지 정규화합니다. 하지만 실시간 잔액 조회 성능을 위해 '계좌 마스터' 테이블에 거래가 일어날 때마다 잔액(Balance)을 업데이트하는 **'중복 속성 유지(반정규화)'** 전략을 병행해야 합니다.
- **시나리오 2: 글로벌 소셜 미디어의 좋아요/댓글 기능**
  - 상황: 읽기(Read) 부하가 쓰기(Write)의 1,000배 이상인 환경.
  - 판단: 엄격한 정규화는 조인 부하로 시스템을 붕괴시킵니다. 따라서 쓰기 시점에 미리 데이터를 합쳐두는(Pre-aggregated) 반정규화와, 일관성을 조금 양보하더라도 가용성을 챙기는 **BASE** 모델을 NoSQL과 혼합하여 사용해야 합니다.

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] **성능 벤치마킹**: JOIN이 3개 이상 발생하는 핵심 쿼리가 서비스 응답 목표 시간(SLA)을 만족하는가?
- [ ] **데이터 중복 허용 범위**: 중복 저장된 데이터의 정합성을 보장하기 위한 추가 로직(Trigger, Application Logic)의 비용이 JOIN 비용보다 저렴한가?
- [ ] **쿼리 복잡도**: 개발자들이 이해하고 유지보수하기에 모델이 지나치게 파편화되지는 않았는가?

#### 3. 안티패턴 (Anti-patterns)
- **과도한 정규화 (Over-Normalization)**: 의미 없는 1:1 관계를 남발하여 모든 조회에 5개 이상의 JOIN을 강제하는 설계는 시스템 자원 소모의 주범입니다.
- **정규화 없는 반정규화**: 정규화 단계를 거치지 않고 처음부터 테이블을 크게 설계하는 것은 논리적 설계를 포기하는 행위입니다. 반드시 **'정규화 후 전략적 반정규화'** 순서를 지켜야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과
- **정량적**: 중복 데이터 제거로 스토리지 비용 30~50% 절감, 데이터 수정 시 갱신 대상 범위 축소로 인한 잠금(Lock) 경합 40% 감소.
- **정성적**: 데이터 아키텍처의 논리적 선명도 확보, 신규 비즈니스 요구사항 발생 시 데이터 모델 변경 최소화(확장성).

#### 2. 미래 전망
클라우드 네이티브 데이터베이스 기술이 발전함에 따라, 분산 환경에서의 **NewSQL**은 NoSQL의 확장성과 함께 강력한 정규화 기반의 ACID를 다시 강조하고 있습니다. 또한, AI 모델을 위한 데이터 레이크(Data Lake) 환경에서는 정규화보다는 대규모 스캔에 최적화된 **Columnar Storage** 기반의 비정규화 구조가 주류를 이룰 것이며, 아키텍트는 워크로드의 성격에 따라 두 모델을 조화롭게 운용하는 역량이 더욱 요구될 것입니다.

#### 3. 참고 표준
- **ANSI/ISO/IEC 9075**: SQL 언어 표준 및 관계형 데이터 모델 표준.
- **DAMA-DMBOK**: 데이터 관리 지식 체계 및 데이터 모델링 가이드.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[함수적 종속성 (FD)](@/studynotes/05_database/01_relational/normalization.md)**: 정규화의 수학적 판단 근거가 되는 속성 간의 관계.
- **[반정규화 (Denormalization)](@/studynotes/05_database/01_relational/normalization.md)**: 성능 최적화를 위해 의도적으로 정규화를 포기하는 전략.
- **[무손실 조인 분해](@/studynotes/05_database/01_relational/normalization.md)**: 정규화 과정에서 정보 유실이 없음을 보장하는 증명 과정.
- **[BCNF (Boyce-Codd Normal Form)](@/studynotes/05_database/01_relational/normalization.md)**: 3정규형의 한계를 극복한 강력한 정규형.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **레고 정리함**: 여러 가지 레고 조각이 한 박스에 섞여 있으면 찾기 힘들죠? 모양별, 색깔별로 작은 칸에 나눠 담는 게 정규화예요.
2. **이상한 일 방지**: 칸을 나눠두면, 빨간 조각을 찾으려다 파란 조각을 잃어버리거나 똑같은 조각을 또 사는 실수를 하지 않게 돼요.
3. **똑똑한 사용**: 나중에 조립을 빨리하고 싶을 때는 자주 쓰는 조각들만 모아둔 '특수 상자'를 따로 만들기도 하는데, 그게 반정규화예요.
