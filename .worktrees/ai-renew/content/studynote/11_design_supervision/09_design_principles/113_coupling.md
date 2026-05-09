+++
weight = 113
title = "결합도 (Coupling)"
date = "2024-03-24"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
- **결합도(Coupling)**는 서로 다른 모듈 간의 상호 의존성 정도를 나타내며, 낮을수록 모듈의 독립성이 향상됨.
- 결합도가 낮으면 변경 시 영향 범위가 최소화되어 유지보수성이 극대화되고 재사용성이 높아짐.
- 이상적인 객체지향 설계는 **'강한 응집도(High Cohesion)'**와 **'느슨한 결합(Loose Coupling)'**을 지향함.

### Ⅰ. 개요 (Context & Background)
- 소프트웨어 공학에서 결합도는 한 모듈의 변화가 다른 모듈에 얼마나 영향을 주는지를 측정하는 척도임.
- 모듈 간의 연결 통로가 복잡하고 정보 교환이 많을수록 결합도가 높다고 하며, 이는 시스템의 경직성을 초래함.
- 인터페이스를 통한 추상화와 의존성 주입(DI) 등을 통해 결합도를 낮추는 것이 현대 아키텍처의 핵심 과제임.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
- 결합도는 데이터(Data) 결합도에서 내용(Content) 결합도로 갈수록 강해지며, 설계 품질이 저하됨.

```text
[ Lowest Coupling / Best Quality ]
      |
  (1) Data Coupling (데이터 결합도) : 자료 요소만 전달
      |
  (2) Stamp Coupling (스탬프 결합도) : 데이터 구조(객체) 전달
      |
  (3) Control Coupling (제어 결합도) : 처리 로직 제어 신호 전달
      |
  (4) External Coupling (외부 결합도) : 외부 환경(통신, 프로토콜) 의존
      |
  (5) Common Coupling (공통 결합도) : 전역 변수 공유
      |
  (6) Content Coupling (내용 결합도) : 타 모듈 내부 직접 접근
      |
[ Highest Coupling / Worst Quality ]

[ BILINGUAL DIAGRAM: Coupling Levels ]
+-------------------+       +-------------------+
|   Module A (Caller)| ----> |   Module B (Callee)|
| [Data Only]       | <---- | [Result Only]     |
+-------------------+       +-------------------+
  (Data Coupling: Loose/Good)

+-------------------+       +-------------------+
|   Module C (Direct)| <---> |   Module D (Internal)|
| [Direct Access]   |       | [Code/State]      |
+-------------------+       +-------------------+
  (Content Coupling: Tight/Bad)
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구분 | 결합도 (Coupling) | 응집도 (Cohesion) |
| :--- | :--- | :--- |
| **관점** | 모듈 간 (Inter-module) | 모듈 내 (Intra-module) |
| **추구 방향** | 낮을수록 좋음 (Minimize) | 높을수록 좋음 (Maximize) |
| **목표** | 독립성 확보, 영향 최소화 | 명확한 기능 수행, 책임 분리 |
| **상호 관계** | 결합도가 낮으면 응집도를 높이기 쉬움 | 응집도가 높으면 자연스럽게 결합도가 낮아짐 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **추상화(Abstraction) 활용**: 구체적인 클래스보다는 인터페이스(Interface)나 추상 클래스에 의존하게 하여 결합도를 완화함 (DIP 원칙).
- **의존성 주입(Dependency Injection)**: 객체 생성을 외부 컨테이너에 맡겨 모듈 간의 직접적인 'new' 호출을 제거함.
- **이벤트 기반 통신(EDA)**: 직접 호출 대신 메시지 큐나 이벤트 버스를 사용하여 발행자(Publisher)와 구독자(Subscriber) 간의 결합을 물리적으로 분리함.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- 결합도를 낮춤으로써 개별 모듈의 단위 테스트가 용이해지고, 병렬 개발의 효율성이 증대됨.
- 향후 마이크로서비스 아키텍처(MSA)에서는 네트워크 결합도를 제어하기 위해 API 게이트웨이와 서비스 메시를 활용하는 추세임.
- 결론적으로 낮은 결합도는 급변하는 비즈니스 요구사항에 유연하게 대응할 수 있는 '애자일한 아키텍처'의 근간임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 소프트웨어 설계 품질 (Design Quality), 모듈화 (Modularity)
- **하위 개념**: 인터페이스 분리 (ISP), 제어의 역전 (IoC), 느슨한 결합 (Loose Coupling)
- **연관 개념**: SOLID 원칙, 디자인 패턴, 도메인 주도 설계 (DDD)

### 👶 어린이를 위한 3줄 비유 설명
- 레고 블록처럼 각 조각이 서로 조금만 닿아 있으면 나중에 떼서 다른 곳에 쓰기 쉬워요(낮은 결합도).
- 만약 풀로 끈적하게 다 붙여버리면 하나를 떼려고 할 때 다른 조각까지 다 망가져요(높은 결합도).
- 그래서 우리는 조립하기 쉬운 레고처럼 서로 독립적인 설계를 해야 해요.
