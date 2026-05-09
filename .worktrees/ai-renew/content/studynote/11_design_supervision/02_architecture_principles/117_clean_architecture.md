+++
weight = 117
title = "클린 아키텍처 (Clean Architecture)"
date = "2024-03-20"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
- **의존성 규칙(Dependency Rule)**에 따라 모든 소스코드 의존성이 외부에서 내부(도메인)로만 향하도록 설계하여 비즈니스 로직을 보호함.
- 프레임워크, 데이터베이스, UI 등 외부 요소가 변경되어도 핵심 업무 규칙(Entities/Use Cases)은 영향을 받지 않는 **독립성**을 확보함.
- 테스트하기 쉬운 구조를 제공하며, 기술적 세부사항에 대한 결정을 최대한 늦출 수 있는 **유연성**을 제공함.

### Ⅰ. 개요 (Context & Background)
- 로버트 C. 마틴(Robert C. Martin, Uncle Bob)이 제안한 아키텍처로, 계층형 아키텍처의 고질적인 문제인 '프레임워크 및 DB 결합도'를 해결하기 위해 고안됨.
- 소프트웨어의 진화 과정에서 '관심사의 분리(Separation of Concerns)'를 달성하여 시스템의 수명을 연장하고 유지보수 비용을 절감하는 것이 목적임.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
```text
[ Clean Architecture Structure ]

    /-------------------------------------------\
    |  External Interfaces (UI, DB, Web, ...)   | <--- Frameworks & Drivers
    |  /-------------------------------------\  |
    |  |  Interface Adapters (Controllers)    |  | <--- Adapters
    |  |  /-----------------------------\     |  |
    |  |  |  Application Business Rules |     |  | <--- Use Cases
    |  |  |  /-------------------\      |     |  |
    |  |  |  | Enterprise Rules  |      |     |  | <--- Entities
    |  |  |  |    (Entities)     |      |     |  |
    |  |  |  \-------------------/      |     |  |
    |  |  \-----------------------------/     |  |
    |  \-------------------------------------/  |
    \-------------------------------------------/

* 의존성 방향 (Dependency Direction): Inside <--- Outside (Entities is Core)
```
- **Entities (Enterprise Business Rules)**: 핵심 비즈니스 로직을 담은 객체. 외부의 어떤 변화에도 무관하게 유지됨.
- **Use Cases (Application Business Rules)**: 시스템이 수행해야 할 구체적인 비즈니스 흐름(워크플로우)을 정의함.
- **Interface Adapters**: Use Case와 External Interface 간의 데이터를 변환(DTO, ViewModel 등)하는 계층.
- **Frameworks & Drivers**: 가장 외곽 계층으로 DB, 프레임워크, 도구 등이 위치하며, 언제든 교체 가능한 세부사항(Detail)임.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 계층형 아키텍처 (Layered) | 클린 아키텍처 (Clean) |
| :--- | :--- | :--- |
| **핵심 가치** | 구조적 단순성 및 빠른 개발 | 비즈니스 로직의 격리 및 보호 |
| **의존성 방향** | 상위 -> 하위 (보통 DB에 의존) | 외부 -> 내부 (도메인이 중심) |
| **테스트 용이성** | 모킹(Mocking)이 복잡함 | 순수 비즈니스 로직 단위 테스트 용이 |
| **변경 전파** | DB 변경 시 도메인 영향 가능성 높음 | 프레임워크/DB 변경 영향 제로 지향 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **판단 지표**: 프로젝트의 규모와 복잡도가 높고, 장기적인 유지보수가 필요하며, 기술 스택의 변경 가능성이 있을 때 도입을 적극 권고함.
- **적용 전략**: 인터페이스(Interface)와 의존성 역전 원칙(DIP)을 활용하여 계층 간의 경계를 명확히 하고, 패키지 구조를 아키텍처 뷰와 일치시킴.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- 시스템의 **유지보수성(Maintainability)**과 **테스트 가능성(Testability)**을 극대화하여 기술 부채를 사전에 방지함.
- 현대의 MSA, Serverless 환경에서도 도메인 중심 설계(DDD)와 결합하여 견고한 소프트웨어 생태계를 구축하는 핵심 표준으로 자리 잡음.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 소프트웨어 아키텍처, 관심사의 분리 (SoC)
- **동급 개념**: 헥사고날 아키텍처, 어니언 아키텍처
- **하위 원칙**: SOLID 원칙, 의존성 역전 (DIP)

### 👶 어린이를 위한 3줄 비유 설명
- 양파처럼 여러 겹의 막이 있는 집을 상상해 보세요.
- 가장 안쪽에는 보물이 들어있고, 바깥쪽 막은 도둑을 막거나 비를 막는 역할을 해요.
- 밖의 막이 찢어져서 새 막으로 갈아 끼워도 안쪽의 보물은 변함없이 안전하게 보관되는 것과 같아요.
