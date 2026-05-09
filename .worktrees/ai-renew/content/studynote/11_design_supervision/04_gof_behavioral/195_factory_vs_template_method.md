+++
weight = 195
title = "팩토리 메서드 vs 템플릿 메서드 관계 (Relationship between Factory & Template Method)"
date = "2026-03-04"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
- **제어의 역전(IoC) 구현:** 부모 클래스가 흐름을 정의하고 자식 클래스가 세부 구현을 담당하는 '할리우드 원칙'의 결정체이다.
- **객체 생성과 알고리즘 분리:** 팩토리 메서드는 '객체 생성'에 집중하고, 템플릿 메서드는 '알고리즘의 뼈대'에 집중한다.
- **융합 설계:** 템플릿 메서드 내부에서 팩토리 메서드를 호출하여 복잡한 로직 내의 객체 생성을 유연하게 처리한다.

### Ⅰ. 개요 (Context & Background)
- 두 패턴은 모두 상속(Inheritance)을 통해 다형성을 구현하는 대표적인 기법이다. 특히 프레임워크 설계 시 공통적인 실행 흐름과 객체 생성 인터페이스를 정의하는 데 필수적으로 활용된다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

```text
+----------------------------+
|      AbstractClass         |
|----------------------------|
| + TemplateMethod()         | -- [Algorithm Skeleton]
| # PrimitiveOperation()     |
| # FactoryMethod():Product  | -- [Creation Interface]
+----------------------------+
             ^
             |
+----------------------------+
|      ConcreteClass         |
|----------------------------|
| # PrimitiveOperation()     | -- [Detail Implementation]
| # FactoryMethod():Product  | -- [Concrete Product]
+----------------------------+

<Bilingual ASCII Diagram: 팩토리/템플릿 메서드 융합 구조 / Combined Factory & Template Method Structure>
```

- **핵심 연관성:** 팩토리 메서드는 종종 템플릿 메서드 내부에서 호출된다. 즉, 템플릿 메서드가 '언제' 객체를 만들지 결정하고, 팩토리 메서드가 '무엇을' 만들지 결정한다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 구분 | 팩토리 메서드 (Factory Method) | 템플릿 메서드 (Template Method) |
| :--- | :--- | :--- |
| **패턴 분류** | 생성 패턴 (Creational) | 행위 패턴 (Behavioral) |
| **주요 목적** | 객체 생성의 서브클래싱 위임 | 알고리즘 구조의 고정과 세부 위임 |
| **관심사** | **Who**: 어떤 객체를 생성할 것인가? | **How**: 어떤 절차로 실행할 것인가? |
| **구현 방식** | 리턴 타입이 객체인 추상 메서드 | 호출 순서가 고정된 Final 메서드 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **프레임워크 설계:** Spring의 `ApplicationContext` 초기화 과정이나 Java의 `AbstractList` 등에서 흔히 발견된다.
- **판단 지점:** 중복되는 코드(Boilerplate)를 부모 클래스로 끌어올리고(Refactoring), 변하는 부분만 메서드로 추출(Extract Method)하여 추상화한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
- 상속의 한계를 극복하기 위해 두 패턴은 긴밀히 협력한다. 이를 통해 변하지 않는 '전략적 가이드라인'과 변하는 '전술적 구현'을 명확히 분리함으로써 코드의 견고함을 확보한다.

### 📌 관련 개념 맵 (Knowledge Graph)
- GoF 디자인 패턴 -> (Template Method, Factory Method) -> 할리우드 원칙 -> IoC (Inversion of Control)

### 👶 어린이를 위한 3줄 비유 설명
- **템플릿 메서드**는 "요리 레시피(재료 준비->굽기->담기)"를 정해놓은 거예요. 굽는 방법만 자식이 정해요.
- **팩토리 메서드**는 요리사가 쓸 "도구(뒤집개, 냄비)"를 그때그때 골라주는 창고지기 같은 역할이에요.
- 레시피 도중에 "자, 이제 창고에서 알맞은 도구를 가져오렴!" 하고 시키는 게 두 패턴의 만남이랍니다.
