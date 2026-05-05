+++
weight = 167
title = "167. 추상 팩토리 팩토리 클래스 도출 (Abstract Factory Derivation)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: 추상 팩토리(Abstract Factory) 패턴은 '제품군(Product Family) 전체를 일관되게 교체해야 한다'는 설계 요구에서 출발한다.
> 2. **가치**: 클라이언트 코드는 구체 팩토리를 몰라도 되고, 팩토리만 갈아끼우면 UI 테마·환경·플랫폼이 통째로 바뀐다.
> 3. **판단 포인트**: 연관된 제품들이 항상 함께 교체되어야 한다면 팩토리 메서드(Factory Method)가 아닌 추상 팩토리를 선택해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 팩토리 클래스 도출의 배경

소프트웨어 설계에서 "어떤 객체를 만들지"를 결정하는 책임을 분리하는 과정이 팩토리 패턴 계열이다. 가장 단순한 정적 팩토리에서 시작해, 단일 제품 생성을 담당하는 팩토리 메서드(Factory Method), 그리고 **관련 제품군(Product Family) 전체를 책임지는 추상 팩토리(Abstract Factory)**로 발전한다.

추상 팩토리 도출의 핵심 트리거는 다음 질문이다.

> "시스템이 복수의 관련 객체를 생성하며, 이 객체들은 항상 같은 계열로 묶여 교체되어야 하는가?"

예를 들어 UI 테마를 다크(Dark) ↔ 라이트(Light)로 전환할 때 `Button`, `TextField`, `Dialog` 세 위젯이 모두 같은 테마를 가져야 한다. 버튼만 다크, 다이얼로그만 라이트가 섞이면 UX 일관성이 깨진다. 이 일관성을 강제하는 구조적 장치가 추상 팩토리다.

### 리팩토링 경로: Factory Method → Abstract Factory

1. **팩토리 메서드 단계**: `createButton()` 하나만 추상화. 테마별로 `LightButtonFactory`, `DarkButtonFactory` 존재.
2. **확장 압력**: TextField, Dialog 등 추가 제품이 등장하며 "이 셋을 묶어서 관리하자"는 요구 발생.
3. **추상 팩토리 도출**: 공통 인터페이스 `ThemeFactory` 안에 `createButton()`, `createTextField()`, `createDialog()` 메서드를 정의. 구체 팩토리 `LightThemeFactory`, `DarkThemeFactory`가 각각 구현.

📢 **섹션 요약 비유**: 공장 하나가 "의자"만 만들다가, 의자·테이블·소파를 세트로 맞춰야 하는 주문이 들어와 "가구 세트 공장"으로 업그레이드되는 것과 같다.

---

## 2. 구성요소

### 추상 팩토리 구조도

```
┌─────────────────────────────────────────────────────────────┐
│                  <<interface>>                               │
│                  ThemeFactory                                │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ + createButton()  : Button                             │ │
│  │ + createTextField(): TextField                         │ │
│  │ + createDialog()  : Dialog                             │ │
│  └────────────────────────────────────────────────────────┘ │
└───────────────────┬─────────────────────┬───────────────────┘
                    │                     │
       ┌────────────▼──────────┐ ┌────────▼──────────────┐
       │  LightThemeFactory    │ │  DarkThemeFactory      │
       │ createButton()        │ │ createButton()         │
       │  → LightButton        │ │  → DarkButton          │
       │ createTextField()     │ │ createTextField()      │
       │  → LightTextField     │ │  → DarkTextField       │
       │ createDialog()        │ │ createDialog()         │
       │  → LightDialog        │ │  → DarkDialog          │
       └───────────────────────┘ └────────────────────────┘
```

### 제품 계층 구조

```
Button (Abstract)
  ├── LightButton
  └── DarkButton

TextField (Abstract)
  ├── LightTextField
  └── DarkTextField

Dialog (Abstract)
  ├── LightDialog
  └── DarkDialog
```

### OCP (Open-Closed Principle, 개방-폐쇄 원칙) 달성

클라이언트 코드는 `ThemeFactory` 인터페이스만 의존한다. 새로운 `HighContrastThemeFactory`를 추가할 때 기존 코드는 **변경 없이** 새 팩토리를 주입받기만 하면 된다. 즉, **확장에는 열려 있고, 변경에는 닫혀 있다.**

### 제품군 일관성 강제 메커니즘

| 수단 | 설명 |
|:---|:---|
| 팩토리 인터페이스 | 어떤 제품을 만들지 계약 강제 |
| 구체 팩토리 단위 교체 | 팩토리 하나만 교체하면 전체 제품군이 동시에 교체 |
| 컴파일 타임 타입 체크 | 추상 타입만 반환하므로 잘못된 제품 혼용 방지 |

📢 **섹션 요약 비유**: 팩토리는 "같은 공장 라인에서 나온 부품만 조립"을 규칙으로 삼는 자동차 조립 공장과 같다. 엔진은 A 공장, 내장재는 B 공장에서 가져오면 맞지 않는다.

---

## 3. 구조 및 동작 원리

### Factory Method vs Abstract Factory

| 비교 항목 | Factory Method (팩토리 메서드) | Abstract Factory (추상 팩토리) |
|:---|:---|:---|
| **생성 대상** | 단일 제품(Single Product) | 제품군(Product Family) |
| **변형 수단** | 서브클래스(Subclass) 오버라이드 | 다른 팩토리 객체로 교체 |
| **관계 패턴** | 상속(Inheritance) 중심 | 합성(Composition) 중심 |
| **일관성 보장** | 제품 1개 | 관련 제품 전체 동시 보장 |
| **클래스 수** | 적음 | 제품 수 × 계열 수만큼 증가 |
| **확장 비용** | 새 제품 추가 쉬움 | 새 제품 추가 시 모든 팩토리 수정 |
| **사용 예시** | 단일 DB 커넥션 생성 | DB + 캐시 + 로거를 환경별 세트 교체 |

### 실무 단점: 제품 추가의 어려움

추상 팩토리의 치명적 단점은 **새 제품 종류를 추가할 때 모든 구체 팩토리를 수정해야** 한다는 점이다. 예를 들어 `createScrollbar()`를 추가하면 `LightThemeFactory`, `DarkThemeFactory` 모두 구현을 추가해야 한다. 이는 OCP를 **팩토리 인터페이스 자체 변경** 관점에서는 위반한다.

📢 **섹션 요약 비유**: 세트 메뉴를 운영하는 식당에서 메뉴 하나(신제품)를 추가하면 모든 세트 메뉴 구성을 전부 업데이트해야 한다는 부담과 같다.

---

## 4. 비교 및 트레이드오프

### 도출 사고 흐름 (설계 면접·기술사 답변 틀)

1. **요구 분석**: "여러 제품이 항상 한 묶음으로 교체되어야 한다" → 추상 팩토리 신호.
2. **추상 제품 정의**: `Button`, `TextField`, `Dialog` 각각 인터페이스 도출.
3. **공통 팩토리 인터페이스 도출**: 각 제품 생성 메서드를 팩토리 인터페이스에 집약.
4. **구체 팩토리 구현**: `LightThemeFactory`, `DarkThemeFactory`.
5. **클라이언트 연결**: DI (Dependency Injection, 의존성 주입) 또는 설정 파일로 팩토리 주입.

### 실무 코드 스케치 (의사 코드)

```java
// Abstract Factory Interface
interface ThemeFactory {
    Button createButton();
    TextField createTextField();
    Dialog createDialog();
}

// Concrete Factory
class DarkThemeFactory implements ThemeFactory {
    public Button createButton()         { return new DarkButton(); }
    public TextField createTextField()   { return new DarkTextField(); }
    public Dialog createDialog()         { return new DarkDialog(); }
}

// Client - 팩토리 교체만으로 테마 전체 변경
class UIRenderer {
    private ThemeFactory factory;  // DI로 주입
    void render() {
        Button  btn  = factory.createButton();
        Dialog  dlg  = factory.createDialog();
        // 테마 일관성 자동 보장
    }
}
```

### 적용 판단 기준

| 상황 | 권장 패턴 |
|:---|:---|
| 단일 제품, 생성 로직 분리만 필요 | Factory Method |
| 관련 제품군, 일관성 있는 교체 필요 | Abstract Factory |
| 런타임에 생성 방식 변경 필요 | Abstract Factory + DI |
| 제품 종류가 자주 추가됨 | Factory Method (Abstract Factory는 수정 비용 발생) |

📢 **섹션 요약 비유**: 기술사는 "요구사항에 제품군 교체가 명시되어 있는지"를 확인한 뒤 추상 팩토리를 꺼내 드는 외과의사처럼, 진단 후 처방해야 한다.

---

## 5. 실무 적용 및 최적화 기법

추상 팩토리 패턴을 올바르게 적용하면:

- **교체 용이성**: 팩토리 하나 교체로 시스템 전체 테마·플랫폼·환경 전환 가능.
- **일관성 보장**: 잘못된 제품 혼용을 구조적으로 차단.
- **테스트 용이성**: `MockThemeFactory`를 주입하면 UI 단위 테스트에서 실제 렌더링 없이 테스트 가능.
- **OCP 달성**: 새 계열 추가 시 기존 코드 무수정.

단, 제품 종류 추가에는 비용이 발생하므로, **요구사항 변화 방향**을 예측해 설계에 반영해야 한다. 계열이 자주 추가될 것으로 예상되면 추상 팩토리가 유리하고, 제품 종류가 자주 추가될 것으로 예상되면 팩토리 메서드가 더 유연하다.

📢 **섹션 요약 비유**: 추상 팩토리는 "층별 교체 가능한 모듈형 건물" 설계다. 층 전체(팩토리)를 교체하면 내부 가구(제품군)가 모두 바뀌지만, 새로운 종류의 방(신제품)을 추가하려면 설계도 자체를 수정해야 한다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | Creational Pattern (생성 패턴) | GoF 5대 생성 패턴 중 하나 |
| 하위 개념 | ConcreteFactory (구체 팩토리) | ThemeFactory를 구현하는 실제 클래스 |
| 연관 개념 | Factory Method (팩토리 메서드) | 단일 제품 생성 추상화, 추상 팩토리의 구성 요소 |
| 연관 개념 | OCP (Open-Closed Principle) | 새 팩토리 추가 시 기존 코드 무변경 |
| 연관 개념 | DI (Dependency Injection) | 구체 팩토리를 외부에서 주입하는 기법 |
| 연관 개념 | Product Family (제품군) | 함께 사용되는 관련 객체 집합 |

---

### 👶 어린이를 위한 3줄 비유 설명

- 레고 세트에는 "우주 테마"와 "성 테마"가 있어요. 같은 테마 세트 안에서만 블록이 딱 맞게 어울려요.
- 추상 팩토리는 "테마 박스 공장"이에요. 박스를 통째로 다른 테마 박스로 교체하면 안에 든 블록이 전부 바뀌어요.
- 우주 테마 박스 안에 성 테마 블록이 섞이지 않도록, 공장이 항상 같은 테마 블록만 넣어줘요.
