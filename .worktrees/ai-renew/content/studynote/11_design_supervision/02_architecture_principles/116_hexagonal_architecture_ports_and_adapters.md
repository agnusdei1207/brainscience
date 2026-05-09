+++
weight = 116
title = "헥사고날 아키텍처 (Hexagonal Architecture / Ports and Adapters)"
date = "2025-05-14"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
1. **도메인 중심 설계**: 비즈니스 로직(Core)을 외부 기술(DB, UI, 외부 API)로부터 완전히 격리하여 기술 종속성을 제거함.
2. **포트와 어댑터 구조**: 내부 도메인은 '포트(Interface)'를 제공하고, 외부 기술은 '어댑터(Implementation)'를 통해 이를 구현하거나 호출함.
3. **테스트 용이성 및 유연성**: 외부 인프라 없이도 도메인 로직 단독 테스트가 가능하며, 인프라 교체 시 도메인 코드 수정이 불필요함.

---

### Ⅰ. 개요 (Context & Background)
- **정의**: 앨리스테어 코번(Alistair Cockburn)이 제안한 아키텍처로, 애플리케이션의 핵심 비즈니스 로직을 외부의 다양한 입출력 장치로부터 독립시키기 위해 고안됨.
- **등장 배경**: 계층형 아키텍처(Layered Architecture)에서 발생하기 쉬운 상위 계층의 하위 계층(DB 등) 의존성 문제를 해결하고, 도메인 모델을 보호하기 위해 등장함.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- **핵심 원리**: 의존성은 항상 외부에서 내부(도메인)로 향하며, 내부 도메인은 외부를 알지 못함.

```text
[ Hexagonal Architecture / Ports and Adapters ]

     User / UI           +---------------------------+          Database
    (Driving App)        |      Inside (Domain)      |       (Driven App)
         |               |                           |              ^
         v               |      +-------------+      |              |
   +-----------+         |      |             |      |        +-----------+
   |  Adapter  | ------> | [Port]   Core      | [Port] <----- |  Adapter  |
   | (Web/CLI) | (Input) |      |  Business   |      | (Output) (JPA/SQL) |
   +-----------+         |      |   Logic     |      |        +-----------+
                         |      +-------------+      |
         ^               |                           |              |
         |               +---------------------------+              v
   External API                                                  Messaging
```

- **구성 요소**:
    1. **Core Domain**: 비즈니스 규칙과 엔티티가 포함된 핵심 영역.
    2. **Ports (Input/Output)**: 도메인과 외부 세계 사이의 명세(Interface).
    3. **Adapters**: 특정 기술(Spring Web, JPA, Kafka 등)을 사용해 포트를 구현하거나 연결하는 구현체.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구분 | 계층형 아키텍처 (Layered) | 헥사고날 아키텍처 (Hexagonal) |
| :--- | :--- | :--- |
| **의존성 방향** | 상위 -> 하위 (UI -> Service -> DB) | 외부 -> 내부 (Adapter -> Port -> Core) |
| **핵심 가치** | 관심사의 분리 | 도메인 모델의 고립 및 기술 독립성 |
| **DB 종속성** | 높음 (Persistence 계층에 의존) | 낮음 (어댑터로 분리) |
| **적합한 규모** | 소규모, 단순 CRUD | MSA, 복잡한 비즈니스 도메인, DDD |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **적용 전략**: 도메인 복잡도가 높고 외부 연동(다양한 클라이언트, 여러 저장소)이 빈번한 MSA 환경에서 도입 권장.
- **기술사적 판단**: 단순한 데이터 CRUD 시스템에 도입하는 것은 오버엔지니어링일 수 있으나, 비즈니스 로직의 영속성을 보장하고 클라우드 네이티브 환경의 유연성을 확보하기 위해서는 필수적인 선택지임.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- **기대효과**: 기술 스택(DB, 메시지 브로커 등)의 변화에도 비즈니스 핵심 코드를 안전하게 유지하며 유지보수 비용을 장기적으로 절감함.
- **결론**: 헥사고날 아키텍처는 '포트와 어댑터'라는 명확한 인터페이스 기반 설계를 통해 클린 아키텍처의 실무적 구현 가이드를 제시함.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 소프트웨어 아키텍처 스타일, 클린 아키텍처.
- **하위 개념**: Inbound Port, Outbound Adapter, Dependency Inversion Principle (DIP).
- **연관 개념**: DDD (Domain Driven Design), Microservices.

### 👶 어린이를 위한 3줄 비유 설명
1. 게임기 본체(도메인)는 그대로 두고, 조이스틱이나 핸들(어댑터)만 갈아 끼우는 것과 같아요.
2. TV(UI)가 바뀌어도 게임기 안의 게임 내용(비즈니스 로직)은 변하지 않아요.
3. 구멍(포트)에 맞는 플러그(어댑터)만 있으면 무엇이든 연결할 수 있는 '만능 로봇' 같은 아키텍처예요.
