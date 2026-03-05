+++
title = "554. CQRS (명령과 조회 책임 분리)"
date = "2026-03-05"
[extra]
categories = "studynotes-software-engineering"
+++

# 554. CQRS (명령과 조회 책임 분리)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터베이스의 쓰기 모델(Command)과 읽기 모델(Query)을 완전히 분리하여, 복잡한 비즈니스 로직 연산과 대규모 조회 트래픽이 서로 간섭하지 않도록 아키텍처를 이원화하는 설계 패턴이다.
> 2. **가치**: 마이크로서비스(MSA) 환경에서 데이터가 여러 서비스에 찢어져 있을 때 발생하는 '조회(Join)의 극악한 성능'을 해결해주며, 읽기/쓰기 각각에 최적화된 이기종 데이터베이스(예: 쓰기는 MySQL, 읽기는 Elasticsearch)를 사용할 수 있게 해 준다.
> 3. **융합**: 이벤트 브로커(Kafka)를 매개로 한 비동기 데이터 동기화, 그리고 쓰기 데이터의 이력을 100% 저장하는 **이벤트 소싱(Event Sourcing)** 패턴과 완벽하게 융합되어 현대 클라우드 네이티브의 고성능 데이터 파이프라인을 이룬다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
CQRS(Command and Query Responsibility Segregation)는 시스템이 수행하는 작업을 두 가지로 엄격히 나눈다.
- **Command (명령)**: 시스템의 상태를 변경하는 작업 (Create, Update, Delete). 부작용(Side-effect)을 동반하며, 강력한 정합성(ACID)과 복잡한 비즈니스 룰 검증이 필요하다.
- **Query (조회)**: 시스템의 상태를 반환하는 작업 (Read). 부작용이 없으며, 빠르고 유연한 데이터 반환이 최우선 목표다.
이 두 책임을 소프트웨어 코드 레벨(클래스 분리)을 넘어, 물리적인 데이터베이스(쓰기용 DB, 읽기용 DB)까지 완전히 분리하는 것이 CQRS의 핵심이다.

### 💡 비유
CQRS는 **"대형 도서관의 책 입고와 검색 시스템"**과 같다.
- **기존 방식(CRUD)**: 사서가 새 책을 사 와서(Command) 분류 기호에 맞게 서가에 꽂고 있는데, 동시에 100명의 학생이 와서(Query) 그 서가 앞에서 책을 찾겠다고 아우성친다. 사서는 책을 꽂을 수도 없고, 학생은 책을 찾을 수도 없다(병목과 락).
- **CQRS 방식**: 사서는 뒷방의 '비밀 창고(쓰기 DB)'에서 새 책을 꼼꼼히 검수하고 정리한다(Command). 정리가 끝나면 "A책 들어왔음!" 하고 방송(Event)을 한다. 도서관 앞데스크 직원은 그 방송을 듣고 '스마트 검색기(읽기 DB)'에 데이터만 쓱 업데이트한다. 학생들 1만 명이 검색기(Query)를 미친 듯이 두드려도, 뒷방에서 책을 정리하는 사서의 일에는 0.1%의 방해도 주지 않는다.

### 등장 배경 및 발전 과정

#### 1. CRUD 모델의 한계와 Impedance Mismatch
전통적인 CRUD(Create, Read, Update, Delete) 아키텍처는 하나의 도메인 모델(Entity)과 하나의 DB(RDBMS)를 공유했다. 트래픽이 커지면서 쓰기(Insert/Update) 시 걸리는 락(Lock)이 조회(Select)를 방해했다. 더 심각한 것은, 쓰기를 위한 정규화된 테이블 구조가 복잡한 화면(View)을 그리기 위한 JOIN 위주의 조회 쿼리와 전혀 맞지 않는 '임피던스 불일치(Impedance Mismatch)' 현상이었다.

#### 2. CQS에서 CQRS로의 확장 (Bertrand Meyer -> Greg Young)
객체 지향의 거장 버트란드 마이어(Bertrand Meyer)가 "상태를 변경하는 함수는 값을 반환하면 안 되고, 값을 반환하는 함수는 상태를 변경하면 안 된다"는 CQS(Command Query Separation) 원칙을 세웠다. 이를 그렉 영(Greg Young)과 우디 디한(Udi Dahan)이 아키텍처 레벨로 끌어올려 물리적 모델까지 분리하는 **CQRS** 패턴으로 발전시켰다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 (표)

| 요소명 | 상세 역할 | 적용 기술 / 특성 | 비유 |
|--------|----------|------------------|------|
| **Command Model**| 복잡한 도메인 로직 처리 및 상태 변경. 완벽한 정합성 요구 | 정규화된 RDBMS, JPA/Hibernate | 정밀한 설계도 |
| **Command DB** | 쓰기 전용 데이터베이스 | Write-heavy에 강한 스토리지 (MySQL, Oracle) | 장인들의 공방 |
| **Event Bus** | 쓰기 DB의 변경 사항을 읽기 DB로 전송 | 비동기 브로커 (Kafka, RabbitMQ, CDC 도구) | 배달 트럭 |
| **Query Model** | 클라이언트 화면(UI)에 최적화된 DTO 반환 | 복잡한 JOIN이 없는 단순 SELECT (MyBatis, SQL Mapper) | 조립 완성품 |
| **Query DB (View)**| 읽기 전용 데이터베이스 | 비정규화된 NoSQL, 검색 엔진 (MongoDB, Elasticsearch, Redis) | 쇼룸(Showroom) 진열대 |

### 정교한 구조 다이어그램 (ASCII Art)

```ascii
================================================================================
[ Advanced CQRS Architecture with Event Synchronization ]
================================================================================

  [ Client (Web/App) ]
      │          ▲
   (1)│ POST     │ (4) GET 
      ▼          │
  ┌────────┐  ┌───────┐
  │Command │  │ Query │  <-- API 컨트롤러부터 분리됨
  │  API   │  │  API  │
  └───┬────┘  └───┬───┘
      │           │
 (도메인로직)   (단순조회)
      ▼           │
 ┌─────────┐      │
 │Command  │      │
 │ Model   │      │
 └────┬────┘      │
      │(2) Insert │
      ▼           │
  [(RDBMS) Command DB]
   - Order Table
   - User Table
      │
      │ (3) Event Publish (e.g. CDC - Change Data Capture)
      ▼
  [ Event Bus (Kafka) ] ── "Order_Created" ──┐
                                             │
                                             ▼ (Subscribe & Update)
                                   [(NoSQL) Query DB (Materialized View)]
                                    - Order_View_Document (JSON)
                                      (Order와 User 정보가 이미 합쳐져 있음)
                                             ▲
                                             │ (Fast Read!)
                                             └────────────────────────────┘
```

### 심층 동작 원리

#### ① 비정규화된 읽기 전용 뷰 (Materialized View) 구축
Query DB(예: Elasticsearch)에는 RDBMS처럼 쪼개진 테이블이 없다. 오직 프론트엔드 화면 1장을 그리기 위해 필요한 모든 정보(주문자 이름, 상품명, 가격, 배송 상태 등)가 **이미 하나로 조립된(JOIN된) JSON 문서 1개**로 통째로 저장되어 있다. 
클라이언트가 조회를 요청하면 Query API는 어떤 연산이나 JOIN도 하지 않고, 이 JSON 문서 1개를 O(1) 속도로 꺼내서 바로 반환한다. (극강의 조회 성능).

#### ② 이벤트 브로커를 통한 상태 동기화 (Synchronization)
Command DB에 새로운 주문이 들어오면(Insert), 이 변경 사항을 Query DB에 어떻게 전달할 것인가?
1. **Application Level**: Command API 코드가 DB에 저장함과 동시에 Kafka에 `OrderCreated` 이벤트를 쏜다.
2. **Database Level (CDC)**: 코드를 건드리지 않고, Debezium 같은 CDC(Change Data Capture) 툴이 Command DB의 트랜잭션 로그(Binlog)를 몰래 읽어다가 Kafka로 쏴준다. (더 안정적인 최신 방식).
Query DB 업데이트를 담당하는 스레드는 Kafka에서 이벤트를 꺼내어 JSON 문서를 예쁘게 조립한 뒤 Query DB를 갱신한다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### CQRS 적용 단계별 아키텍처 비교

CQRS는 한 번에 물리적 DB를 쪼개는 것이 아니라, 조직의 성숙도에 따라 3단계로 진화한다.

| 진화 단계 | 아키텍처 특성 | 장점 | 단점 / 한계 |
|-----------|---------------|------|-------------|
| **Level 1: 코드 레벨 분리** | 단일 DB 사용. 클래스만 Command Service와 Query Service로 나눔 | 구현이 매우 쉽고, ACID 트랜잭션이 100% 보장됨 | 트래픽 폭주 시 단일 DB 병목은 여전함 |
| **Level 2: DB 레플리케이션 분리**| Master DB(Write)와 Slave DB(Read)로 물리적 분리 후 조회는 Slave에서 함 | 데이터베이스 I/O 부하가 분산됨 | 읽기와 쓰기의 데이터 모델(테이블 구조)이 똑같아 복잡한 JOIN 성능 문제는 미해결 |
| **Level 3: 이기종 DB 완벽 분리** | Write는 RDBMS, Read는 NoSQL/Elasticsearch. 비동기 이벤트로 동기화 | **CQRS의 완성**. 조회 속도 극대화, 읽기 스키마 완전 독립 | 동기화 지연(Eventual Consistency) 발생. 아키텍처 복잡도 지옥 |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 시나리오)

**상황**: 대형 쇼핑몰의 '마이페이지 - 내 주문 내역' 화면. 이 화면을 그리려면 `주문 MSA`, `회원 MSA`, `상품 MSA`, `배송 MSA`, `리뷰 MSA` 등 무려 5개의 마이크로서비스 API를 호출해서 데이터를 조합(API Composition)해야 한다. 로딩에 3초가 걸려 고객 이탈률이 급증함.
**판단 및 Level 3 CQRS 도입 전략**:
1. **Query 모델(뷰) 전용 DB 구축**: 읽기 전용 NoSQL(MongoDB)에 `MyPage_View` 컬렉션을 만든다.
2. **이벤트 구독 및 조립(Projection)**: 5개의 MSA에서 발생하는 모든 이벤트(결제 완료, 배송 출발, 리뷰 작성 등)를 Kafka로 모은다. **프로젝터(Projector)**라는 백그라운드 앱이 이 이벤트들을 족족 주워 담아 `MyPage_View` JSON 문서 하나를 계속해서 실시간 업데이트(조립)해 둔다.
3. **조회 전환**: 프론트엔드가 5개의 API를 부르던 코드를 지우고, 오직 NoSQL을 바라보는 `GET /mypage/view` 하나만 호출하도록 바꾼다.
4. **결과**: 로딩 속도가 3초에서 **0.05초(50ms)**로 60배 빨라졌다. 5개의 마이크로서비스 중 배송 MSA가 서버 점검으로 다운되어 있어도, 고객은 MongoDB에 미리 캐싱된 내역을 통해 안전하게 마이페이지를 볼 수 있다 (장애 격리 완벽 달성).

### 주의사항 및 안티패턴 (Anti-patterns)
- **최종적 일관성(Eventual Consistency)의 비즈니스 충돌**: Command DB에 글을 쓰고 나서 Query DB에 데이터가 동기화되기까지 카프카를 거치며 약 0.1초~1초의 틈(지연)이 발생한다. 사용자가 게시글을 등록하고 화면이 새로고침(리다이렉트) 되었을 때, Query DB가 아직 갱신되지 않아 방금 쓴 글이 안 보이면 사용자는 "오류 난 줄 알고 등록 버튼을 여러 번 누르는" 대형 사고가 터진다.
*해결책*: 등록 직후 1~2초 동안은 프론트엔드 단(React, Vue)에서 캐싱한 임시 데이터를 보여주거나(Optimistic UI), 커맨드 응답으로 생성된 ID를 받아 짧은 시간 폴링(Polling)을 하는 등 **UI/UX 적인 타협과 기만(?)**이 반드시 병행되어야 한다.

---

## Ⅴ. 기대효과 및 결론

### 정량적/정성적 기대효과
- **읽기 성능(Read Latency) 극대화**: 다중 JOIN 연산을 `Select *` 1번으로 치환하여, 대규모 B2C 서비스(상품 카탈로그, 피드)의 응답 속도를 $O(1)$에 가깝게 최적화.
- **도메인 모델의 순수성 보장**: Command(쓰기) 쪽 도메인 객체(Entity)가 억지로 화면(View)을 그리기 위한 잡다한 필드들을 떠안지 않고 순수한 비즈니스 규칙만 품을 수 있게 됨.

### 미래 전망 및 진화 방향
CQRS는 그 자체로도 훌륭하지만, 최근에는 모든 상태 변경을 이벤트의 누적으로 저장하는 **이벤트 소싱(Event Sourcing)** 패턴과 사실상 한 몸(CQRS/ES)처럼 융합되어 사용된다. 이벤트 소싱으로 저장된 수억 개의 과거 이벤트들을 재생(Replay)하기만 하면, 언제든 새로운 형태의 Query DB(예: Elasticsearch에서 Redis로 교체)를 0에서부터 완벽하게 100% 다시 찍어낼 수 있는 **궁극의 불변 데이터 아키텍처**로 발전하고 있다.

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [이벤트 소싱 (Event Sourcing)](./555_event_sourcing.md) - CQRS의 Command DB를 대체하여 완벽한 시너지를 내는 영혼의 단짝 아키텍처
- [이벤트 기반 아키텍처 (EDA)](./538_event_driven_architecture.md) - Command DB와 Query DB 사이의 간극을 비동기로 메워주는 사상
- [API 게이트웨이 및 BFF](./543_bff_backend_for_frontend.md) - CQRS의 Query 모델이 응답하는 형태가 결국 BFF가 원하는 형태와 완벽히 일치함
- [NoSQL 데이터 모델 (Document DB)](../../5_database/6_nosql/277_document_store.md) - 복잡한 조인 결과를 하나의 덩어리로 저장하기 좋은 CQRS의 1순위 Query DB

---

## 👶 어린이를 위한 3줄 비유 설명
1. **CQRS가 뭔가요?**: 요리사(쓰기)가 요리하는 좁고 복잡한 주방과, 손님(읽기)이 음식을 꺼내가는 넓고 깔끔한 뷔페 진열대를 아예 벽으로 분리해 버리는 식당 구조예요.
2. **왜 분리하나요?**: 손님 수천 명이 밥을 푸고 있는데 요리사가 그 틈을 비집고 들어가서 새 요리를 놓으려면 너무 복잡하고 다치기 쉽잖아요.
3. **어떻게 돌아가나요?**: 주방에서 요리를 완성하면 작은 뒷문을 통해 진열대에 쓱 밀어 넣어둬요. 손님들은 요리사가 어떻게 요리했는지는 전혀 알 필요 없이, 진열대에 놓인 완성품만 1초 만에 쏙쏙 집어가면 된답니다!
