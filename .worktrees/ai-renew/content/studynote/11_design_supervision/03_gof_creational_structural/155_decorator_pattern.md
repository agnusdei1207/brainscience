+++
weight = 155
title = "데코레이터 패턴 (Decorator Pattern)"
date = "2026-03-04"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
1. **동적 책임 추가**: 상속 대신 합성(Composition)을 사용하여 객체에 기능을 런타임에 동적으로 추가할 수 있게 해주는 구조 패턴입니다.
2. **유연한 확장성**: 상속을 통한 확장은 정적이고 클래스 수가 폭발적으로 늘어나지만, 데코레이터는 여러 장식자를 조합하여 무수히 많은 조합을 생성할 수 있습니다.
3. **투명한 래핑**: 데코레이터와 실제 객체는 동일한 인터페이스를 가지므로, 클라이언트는 객체가 장식되었는지 여부를 알 필요가 없습니다.

### Ⅰ. 개요 (Context & Background)
데코레이터 패턴은 "객체의 서브클래싱을 통한 기능 확장"의 한계를 극복하기 위해 제안되었습니다. 상속은 클래스 설계 시점에 결정되지만(Compile-time), 데코레이터는 객체 생성 시점에 결정됩니다(Run-time). 주로 스트림 처리(Java I/O), GUI 위젯 장식, 커피 메뉴 조합 등 부가적인 책임을 유연하게 추가해야 할 때 사용됩니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
데코레이터 패턴은 공통 인터페이스(Component), 구체적 컴포넌트(Concrete Component), 장식자(Decorator), 구체적 장식자(Concrete Decorator)로 구성됩니다.

```text
       [ Component ] (공통 인터페이스)
      /             \
[ Concrete ]     [ Decorator ] (장식자 베이스)
[ Component ]    - component: Component
      ^                 /            \
      |        [ Concrete ]      [ Concrete ]
      |        [ Decorator A ]   [ Decorator B ]
      |        (기능 추가 로직)     (기능 추가 로직)

  <Bilingual Execution Flow>
  1. Client calls Decorator.operation(). -> 클라이언트가 장식자 호출
  2. Decorator calls wrapped Component.operation(). -> 감싸진 객체 기능 수행
  3. Decorator adds extra behavior. -> 장식자가 추가 기능 수행 (앞/뒤)
```

- **Component**: 기본 객체와 장식자가 공통으로 구현해야 할 인터페이스입니다.
- **Decorator**: 감쌀 객체(Component)의 참조를 유지하며, 인터페이스의 연산을 감싸진 객체에게 위임합니다.
- **Concrete Decorator**: 실제 부가 기능을 구현합니다. (예: 로깅, 데이터 압축, UI 테두리 추가)

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
데코레이터 패턴은 프록시 및 전략 패턴과 구조적으로 유사하지만 목적이 다릅니다.

| 구분 | 데코레이터 패턴 (Decorator) | 프록시 패턴 (Proxy) | 전략 패턴 (Strategy) |
| :--- | :--- | :--- | :--- |
| **핵심 목적** | 객체에 새로운 책임(기능) 추가 | 객체에 대한 접근 제어 | 객체의 행위(알고리즘) 변경 |
| **객체 관계** | 1:1 재귀적 래핑 가능 | 1:1 대리 관계 | Context - Strategy 위임 |
| **투명성** | 매우 높음 (인터페이스 동일) | 높음 (인터페이스 동일) | 낮음 (컨텍스트가 전략을 앎) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **적용 케이스**: 
    - Java I/O 스트림: `new BufferedInputStream(new FileInputStream(file))`
    - 웹 필터/인터셉터: 서블릿 필터 체인 구조
    - UI 프레임워크: 스크롤바, 테두리, 그림자 효과를 동적으로 추가
- **기술사적 판단**: 데코레이터 패턴은 **단일 책임 원칙(SRP)**을 지키는 데 매우 효과적입니다. 핵심 로직과 부가 기능을 분리하여 관리할 수 있기 때문입니다. 다만, 너무 많은 데코레이터를 중첩하면 코드가 복잡해지고(Deep Stack), 작은 객체들이 많이 생성되어 메모리 관리에 주의해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
데코레이터 패턴을 적용하면 클래스의 폭발적인 증가를 막고, **변경에는 닫혀 있고 확장에는 열려 있는(OCP)** 이상적인 설계를 달성할 수 있습니다. 이는 특히 요구사항이 수시로 변하는 기민한(Agile) 개발 환경에서 유지보수 효율을 높이는 핵심 도구로 작용합니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **부모 개념**: 구조 패턴 (Structural Patterns), 합성 (Composition)
- **핵심 원칙**: 개방-폐쇄 원칙 (OCP), 상속보다 합성 선호
- **융합 기술**: 어스펙트 지향 프로그래밍 (AOP), 필터 체인 (Filter Chain)

### 👶 어린이를 위한 3줄 비유 설명
1. **아이스크림 한 스쿱(Component)**에 **초코 시럽(Decorator A)**과 **스프링클(Decorator B)**을 뿌리는 것과 같아요.
2. 어떤 토핑을 뿌려도 여전히 "아이스크림"이라는 사실은 변하지 않아요.
3. 토핑을 하나씩 더 얹을 때마다 맛이 더 풍부해지는 것처럼, 객체에 기능을 하나씩 더해주는 방법이에요.
