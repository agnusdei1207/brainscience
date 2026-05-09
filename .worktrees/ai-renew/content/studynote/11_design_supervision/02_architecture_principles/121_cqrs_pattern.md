+++
weight = 121
title = "CQRS (Command Query Responsibility Segregation)"
date = "2026-03-04"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
- **책임 분리**: 데이터의 상태를 변경하는 명령(Command)과 데이터를 읽는 조회(Query)를 완전히 독립된 모델로 분리하는 아키텍처 패턴이다.
- **성능 최적화**: 조회용 데이터베이스(Read-DB)를 별도로 구축하여, 대규모 읽기 트래픽에 최적화된 스키마(Denormalization)를 사용할 수 있다.
- **확장성 극대화**: 읽기와 쓰기의 성능 요구사항이 서로 다른 시스템에서 각 계층을 독립적으로 스케일링할 수 있다.

### Ⅰ. 개요 (Context & Background)
전통적인 CRUD 모델에서는 동일한 도메인 객체를 사용하여 데이터의 변경과 조회를 수행한다. 그러나 비즈니스 로직이 복잡해질수록 단일 모델은 읽기와 쓰기 양쪽의 성능 저하를 초래한다. CQRS는 이를 해결하기 위해 "상태를 변경하는 메서드는 값을 반환하지 않고, 값을 반환하는 메서드는 상태를 변경하지 않는다"는 원칙을 아키텍처 레벨로 확장한 것이다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
CQRS는 일반적으로 메시지 브로커를 통해 명령 측과 조회 측의 데이터를 동기화한다.

```text
[ User Interface ]
     |           |
 (Command)    (Query)
     v           v
[ Write Model ] [ Read Model ]
     |           |
 (Event Store) --(Sync)--> (Materialized View)

<Bilingual ASCII Diagram: CQRS Logic>
- Command (Write): 비즈니스 유효성 검사 및 상태 변경 (Update/Delete/Insert)
- Query (Read): 조회 전용 스키마/캐시에서 빠른 데이터 반환 (Select)
- Sync (Event): 메시지 큐를 통한 비동기 데이터 동기화 (Eventual Consistency)
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | 전통적 CRUD 모델 | CQRS 패턴 |
| :--- | :--- | :--- |
| **모델 구조** | 읽기/쓰기 단일 모델 (Unified) | 읽기/쓰기 모델 분리 (Segregated) |
| **데이터 정합성** | 즉시 일관성 (Immediate) | 결과적 일관성 (Eventual) |
| **DB 스키마** | 정규화 (Normalization) | 반정규화 (Denormalization/View) |
| **유지보수성** | 단순하지만 모델 비대화 우려 | 복잡하지만 계층별 전문화 가능 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **기술사적 판단**: CQRS는 시스템 전반에 적용하기보다, 복잡한 비즈니스 규칙이 있는 핵심 도메인(Core Domain)이나 조회 트래픽이 비정상적으로 높은 영역(예: 쇼핑몰 상품 상세/검색)에 부분적으로 적용하는 것이 비용 대비 효율적이다.
- **실무 전략**: 데이터 동기화 지연(Latency)을 고려하여, UI 레벨에서 낙관적 업데이트(Optimistic Update)나 폴링 기법을 적절히 혼용해야 한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
CQRS는 이벤트 소싱(Event Sourcing)과 결합될 때 최상의 시너지를 발휘한다. 복잡한 마이크로서비스 환경에서 시스템의 유연성을 확보하고, 각 서비스의 기술 독립성(Polyglot Persistence)을 보장하는 표준 아키텍처로 자리 잡고 있다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 마이크로서비스 아키텍처(MSA), 아키텍처 스타일
- **하위 개념**: Read Model, Write Model, Materialized View
- **연관 개념**: 이벤트 소싱, EDA, 결과적 일관성, DDD

### 👶 어린이를 위한 3줄 비유 설명
- **전통적 식당**: 요리사가 요리도 하고 서빙도 하고 계산도 다 혼자 하는 거예요. 바빠지면 정신이 없겠죠?
- **CQRS 식당**: 요리는 요리사가 전담하고, 서빙은 서버가 전담해서 각자 잘하는 일에만 집중하는 거예요.
- **장점**: 손님이 갑자기 많이 와도 주문받는 사람과 요리하는 사람이 따로 있어서 훨씬 빨라요!
