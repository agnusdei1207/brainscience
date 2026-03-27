+++
title = "생성 패턴"
description = "Creational Design Patterns"
category = "4_software_engineering"
+++

# 생성 패턴 (Creational Design Patterns)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 생성 패턴 (Creational Patterns)은 객체의 생성 방식 (How)을 그 사용 방식 (What)과 분리하여, 결합도를 낮추고 시스템의 유연성을 높이는 GoF 디자인 패턴의 한 분류로, Factory Method, Abstract Factory, Builder, Prototype, Singleton의 5개 패턴이 포함된다.
> 2. **가치**: 생성 패턴을 적용하면 객체 생성 로직의 변경이 객체 사용 코드에 영향을 미치지 않게 되어, 새로운 제품 타입 추가 시 기존 코드를 修改하지 않고 확장할 수 있다 (OCP 준수).
> 3. **융합**: 생성 패턴은 Dependency Injection (DI), IoC Container (Spring, Dagger), Microservices의 Service Locator 등 현대적 설계 기술의 이론적 기반이며, 특히 Factory 패턴은 API Gateway, Service Discovery 등의 구현에서 핵심 역할을 한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

- **개념**: 생성 패턴은"객체를 만드는 방법"을 추상화하여 클라이언트 코드와 객체 생성 로직을 분리한다. 만약 객체 생성 로직이 클라이언트 코드에直接 구현되어 있으면, 새로운 객체 타입 추가 시 클라이언트 코드를 모두 수정해야 한다. 생성 패턴은"객체 생성"을 별도의 책임으로 분리함으로써 이 문제를 해결한다.

- **필요성**: 객체지향 시스템에서"객체 생성"은 가장 빈번한 작업 중 하나이며, 잘못된 생성 방식은 결합도를 높이고 테스트를 어렵게 한다. 예컨대"new Car()"라고直接 호출하면 Car의 구체적 구현에 결합되지만,"CarFactory.create()"를 호출하면工厂实现切换可能해진다.

- **💡 비유**: 생성 패턴은"餐巾factory"와 같다. 요리사가 직접 재료를 사러 장을 보면 (new 연산자 직접 호출) 시간이浪费되고, 재료 purchase 로직이 바뀌면 요리사도 다시 교육해야 한다. 반면采购담당자(Factory)가 있으면, 요리사는"재료가 필요합니다"만 말하면 되고, 구매 로직이 바뀌어도 요리사는 신경 쓸 필요가 없다.

- **등장 배경**: 1994년 GoF (Gang of Four)의"Design Patterns: Elements of Reusable Object-Oriented Software"에서 생성 패턴 5가지를 체계화했다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 5가지 생성 패턴

| 패턴 | 핵심 아이디어 | 사용 시점 | 예시 |
|:---|:---|:---|:---|
| **Factory Method** | 하위 클래스에서 생성할 객체를 결정 | 서브클래스가 생성할 객체 타입을 결정 | Dialog → ButtonDialog |
| **Abstract Factory** | 관련된 객체들을 families로 생성 | 여러 관련 객체群을 함께 생성 | UI Theme (Button+Input+Menu) |
| **Builder** | 복잡한 객체를 단계별로 생성 | 생성 과정이 복잡할 때 (파라미터 많음) | DocumentBuilder, StringBuilder |
| **Prototype** | 기존 객체를 복제하여 생성 | 생성 비용이 높을 때 (DB 조회 등) | Clone(), copy constructor |
| **Singleton** | 클래스의 인스턴스가 하나만 존재 | 하나의 인스턴스만 필요 | Configuration, Logger |

### Factory Method vs Abstract Factory

```text
  ┌─────────────────────────────────────────────────────────────────┐
  │              Factory Method vs Abstract Factory                          │
  ├─────────────────────────────────────────────────────────────────┤
  │
  │  [Factory Method: 제품 하나 생성]                                  │
  │
  │       ┌──────────────────┐                                      │
  │       │  Dialog          │                                      │
  │       │ (Creator)        │                                      │
  │       ├──────────────────┤                                      │
  │       │ +createButton()  │                                      │
  │       │ (Factory Method) │                                      │
  │       └────────┬─────────┘                                      │
  │                │ extends                                        │
  │     ┌─────────┴──────────┐                                    │
  │     ▼                     ▼                                    │
  │  ┌────────┐           ┌────────┐                               │
  │  │Windows │           │  Mac   │                               │
  │  │ Dialog │           │  Dialog │                               │
  │  ├────────┤           ├────────┤                               │
  │  │+create │           │+create │                               │
  │  │Button()│           │Button()│                               │
  │  │ →Win  │           │ →Mac   │                               │
  │  │Button │           │Button  │                               │
  │  └────────┘           └────────┘                               │
  │
  │  [Abstract Factory: 관련 객체群 함께 생성]                          │
  │
  │       ┌──────────────────┐                                      │
  │       │  GUIFactory      │                                      │
  │       │ (Abstract Factory)│                                      │
  │       ├──────────────────┤                                      │
  │       │ +createButton() │                                      │
  │       │ +createMenu()   │                                      │
  │       │ +createInput()   │                                      │
  │       └────────┬─────────┘                                      │
  │                │ implements                                     │
  │     ┌─────────┴──────────┐                                    │
  │     ▼                     ▼                                    │
  │  ┌────────┐           ┌────────┐                               │
  │  │ Win    │           │  Mac   │                               │
  │  │Factory │           │Factory │                               │
  │  └────────┘           └────────┘                               │
  │  ※ 한 Factory에서 Button+Menu+Input을 함께 생성                   │
  │
  └─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Factory Method는"하나의 제품"만 생성하며, 어떤具体的な製品を生成するかはサブクラスで決定する。 Dialog.createButton()을 호출하면 Windows 환경에서는 WindowsButton을, Mac 환경에서는 MacButton을 생성한다. Abstract Factory는"관련 객체群"을 함께 생성한다. GUIFactory는 Button+Menu+Input을 함께 생성하며, WinFactory는 Windows 스타일의 Button+Menu+Input을, MacFactory는 Mac 스타일의它们を一緒に生成する。 이를 통해"관련 객체들의 family"를 한 번에 교체할 수 있어, UI Theme 전체를 통째로 변경하는 것이 가능하다.

---

## Ⅲ. Singleton 패턴의 쟁점

Singleton은 가장 단순하지만 오남용 시 문제가 발생하는 패턴이다.

| 장점 | 문제점 |
|:---|:---|
| 하나의 인스턴스만 존재 보장 | 전역 상태 문제, 테스트 어려움 |
| 지연 초기화 (Lazy Init) 가능 | 명시적 의존성 숨김 |
| 리소스 절약 | 다중 스레드 환경에서 복잡성 ↑ |

**대안**: Dependency Injection을 통해Singleton 효과를 얻는 것이 일반적으로 더 좋은 설계다.

- **📢 섹션 요약 비유**: Singleton은"학교의 교장선생님"과 같다. 교장선생님은 학교에 하나뿐이어서 어느 선생님이든"저는 교장선생님과 상의했습니다"라고 말하지만, 실제로 교장선생님이 바쁘면 업무가堵下がり、교장선생님問題가 全校에 영향이 간다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 패턴 선택 가이드

| 상황 | 적합한 패턴 | 대안 |
|:---|:---|:---|
| 객체 생성 로직이 복잡할 때 | Builder | telescopic constructor 회피 |
| 동일한 객체 여러 개 필요할 때 | Prototype | clone() 활용 |
| 객체 인스턴스 하나만 필요 | Singleton | DI Container의 Singleton Scope |
| 제품 family 전체 교체 필요 | Abstract Factory | Plugin 시스템 |

### 안티패턴

- **Singleton 오남용**: 어디서든 접근 가능한 Singleton会导致"숨겨진 의존성"이 되어 테스트와 유연성을 해침
- **Factory 과잉**: 단순한 객체 생성에까지 Factory 적용 → 과도한抽象化

- **📢 섹션 요약 비유**: 생성 패턴은"餐巾供应链管理"와 같다. 식당에 재료가 직접 들어오는 것이 아니라 (new 직접 호출), 전문 유통업체 (Factory)를 통해 들어오면, 식당은 재료 purchase 방법이 바뀌어도 recipe에만 집중할 수 있다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망

- **DI Container의 표준화**: Spring, Dagger 등의 DI Container가 생성 패턴을 자동으로 처리하는方向发展

### 참고 표준

- **GoF - Design Patterns**: 생성 패턴의 원천 출처
- **Martin Fowler - PoEAA**: 엔터프라이즈 앱에서의 생성 패턴 적용 가이드

- **📢 섹션 요약 비유**: 생성 패턴은"construction 전문施工管理模式"과 같다. 직접 施工하면 工務店 costs가 들지만, 施工 manager(Builder)를 두면 施工プロセス全体を监督管理하고, 각 공種(Prototype)를 복제해서 쓸 수 있다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **Dependency Injection (DI)** | Factory 패턴을 대체하는 의존성 해결 방법으로, 객체 생성 responsibility를外部 Container에 위임한다. |
| **Factory Method** | 생성 패턴의 하나로, 하위 클래스에서 생성할 객체를 결정하게 함으로써 객체를 사용하는 코드와 생성 코드를 분리한다. |
| **Builder Pattern** | 복잡한 객체의 생성 과정을 단계별로 분리하여, 같은 생성 공정으로 다른 표현의 객체를 생성할 수 있게 한다. |
| **Prototype Pattern** | 기존 객체를 복제함으로써 생성 비용 (DB 조회, 네트워크 호출 등)을 절감하는 패턴이다. |
| **Singleton Pattern** | 하나의 인스턴스만 생성하도록 보장하지만, 전역 상태 문제로 인해 DI 패턴 사용이 권장된다. |
| **OCP (개방-폐쇄 원칙)** | 생성 패턴은 OCP를 준수하는 데 핵심적인 역할을 하며, 새로운 객체 타입 추가 시 기존 코드를 수정하지 않아도 된다. |
| **IoC Container** | Spring, Dagger 등의 DI Container가 Factory, Singleton 등의 패턴을 내부적으로 활용하여 객체 생성과 의존성 주입을 자동화한다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. 생성 패턴은"장난감 자동販売機"와 같아. 직접 공장에서 장난감을 가져오려면 (new 직접 호출) 시간과 노력이 들지만, 판매기 (Factory)에 동전을 넣으면 (Factory Method 호출) 원하는 장난감이 나옴. 만약 장난감이 여러 개인 경우 (Abstract Factory) 묶음으로 나올 수 있어.
2. Builder 패턴은"피자 만들기"와 같아.반죽-토핑-굽기 단계로 만들면 같은 레시피로 다양한 피자를 만들 수 있잖아.
3. Prototype 패턴은"클론 장난감"과 같아. 하나를 만들고 그것을 복제하면 새로운 장난감을 만들기 위해 시간을 들이지 않아도 돼. Singleton은"우리 반 게시판"과 같아. 게시판은 하나뿐이어서 모두가 같은 정보를 볼 수 있지만, 게시판에 문제가 생기면 반 전체에 영향이 간다.
