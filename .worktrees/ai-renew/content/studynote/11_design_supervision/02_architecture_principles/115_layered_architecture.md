+++
weight = 115
title = "계층형 아키텍처 (Layered Architecture)"
date = "2024-03-24"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
- **계층형 아키텍처**는 시스템의 기능을 수직적 관심사(Concern)에 따라 분할하여 관리하는 가장 보편적인 구조임.
- 각 계층은 하위 계층에만 의존하며, **계층의 격리(Layer Isolation)**를 통해 유지보수성과 테스트 용이성을 확보함.
- 수평적 확장이 용이하고 구조가 명확하여 엔터프라이즈 애플리케이션의 기본 모델로 널리 사용됨.

### Ⅰ. 개요 (Context & Background)
- '관심사의 분리(Separation of Concerns)'를 실현하기 위해 사용자 인터페이스, 비즈니스 로직, 데이터 접근 기능을 각 층으로 나눔.
- 상위 계층은 하위 계층이 제공하는 서비스를 호출하며, 하위 계층의 구체적인 구현 방식은 알 필요가 없음.
- 주로 3계층(3-Tier) 또는 4계층(4-Layer) 구조가 표준적으로 사용됨.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- 표준적인 4계층 구조는 Presentation, Application, Domain, Infrastructure로 나뉘며, 각 계층의 역할이 엄격히 규정됨.

```text
[ Standard 4-Layer Architecture ]
+---------------------------------------+
|  Presentation Layer (UI / API)        | <--- User/Device
+---------------------------------------+
|  Application Layer (Service Orchestr.)| <--- Logic/Flow
+---------------------------------------+
|  Domain Layer (Business Logic / Model)| <--- Pure Domain
+---------------------------------------+
|  Infrastructure Layer (DB / External) | <--- DB/FileSystem
+---------------------------------------+

[ BILINGUAL FLOW: Access Rules ]
(O) Valid : Upper Layer -> Lower Layer
(X) Invalid : Lower Layer -> Upper Layer (Strictly Prohibited)
(X) Invalid : Skip Layer (Generally Prohibited for Isolation)

+-------------------+       +-------------------+
|   Presentation    | ----> |    Application    |
| [Controller]      |       | [Service Manager] |
+-------------------+       +-------------------+
                                      |
                                      V
+-------------------+       +-------------------+
|   Infrastructure  | <---- |      Domain       |
| [Repository]      |       | [Entity / Logic]  |
+-------------------+       +-------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 항목 | 폐쇄형 계층 구조 (Closed) | 개방형 계층 구조 (Open) |
| :--- | :--- | :--- |
| **의존 방식** | 바로 아래 계층만 호출 가능 | 모든 하위 계층 호출 가능 |
| **격리 수준** | 높음 (격리 원칙 준수) | 낮음 (유연성 중시) |
| **유지보수성** | 우수 (영향 범위 제한) | 보통 (결합도 상승 위험) |
| **성능** | 불필요한 위임 가능성 존재 | 직통 호출로 오버헤드 감소 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **엄격한 격리 유지**: 하위 계층의 변화가 상위 계층에 영향을 주지 않도록 DTO(Data Transfer Object)를 사용하여 데이터를 변환 전달함.
- **안티패턴 주의**: 도메인 계층이 비어 있고 애플리케이션 계층에만 로직이 쏠리는 '빈약한 도메인 모델(Anemic Domain Model)'을 경계해야 함.
- **단점 극복**: 계층이 너무 많아지면 단순한 기능 구현에도 많은 코드가 필요(Overhead)하므로, 서비스 규모에 맞게 계층을 최적화함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- 계층형 구조는 팀 단위의 병렬 개발(계층별 담당)을 가능케 하여 대규모 프로젝트 관리에 최적화됨.
- 현대적인 헥사고날(Hexagonal)이나 클린 아키텍처는 사실 계층형 아키텍처에서 '의존성 역전'을 통해 도메인을 중앙으로 옮긴 진화된 형태임.
- 결론적으로 계층형 아키텍처는 **검증된 안정성**을 바탕으로 시스템의 복잡도를 제어하는 핵심 무기임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 아키텍처 스타일, 관심사의 분리 (SoC)
- **하위 개념**: 3-Tier, n-Tier 아키텍처, 계층의 격리 (Isolation)
- **연관 개념**: 헥사고날 아키텍처, 의존성 역전 원칙 (DIP), DTO 패턴

### 👶 어린이를 위한 3줄 비유 설명
- 햄버거처럼 빵, 패티, 야채가 층층이 쌓여 있는 모양이에요.
- 빵(UI)을 먹을 때 패티(DB)가 어떻게 만들어졌는지 몰라도 맛있게 먹을 수 있어요.
- 각 층이 자기 역할만 잘하면 아주 맛있는 햄버거가 완성되는 것과 같아요.
