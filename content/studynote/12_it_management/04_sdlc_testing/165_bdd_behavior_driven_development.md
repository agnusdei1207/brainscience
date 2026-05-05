+++
weight = 165
title = "165. BDD (Behavior Driven Development, 행위 주도 개발)"
date = "2026-04-21"
[extra]
categories = "studynote-it-management"
+++
## 0. 핵심 인사이트

> **핵심**: BDD (Behavior Driven Development, 행위 주도 개발)는 Given/When/Then 자연어 명세로 소프트웨어의 기대 행위를 정의해, 비즈니스와 개발을 연결하는 TDD의 진화형이다.
> 2. **가치**: BDD의 핵심 가치는 "공통 언어"—기획자, QA, 개발자가 동일한 시나리오(Gherkin 문법)를 함께 작성하면, "무엇을 만들어야 하는가"에 대한 의사소통 비용이 크게 줄어든다.
> 3. **판단 포인트**: BDD는 TDD를 대체하지 않는다—BDD는 비즈니스 행위 수준의 인수 테스트(Acceptance Test)이고, TDD는 구현 수준의 단위 테스트다. 두 기법은 다른 추상화 레벨에서 서로를 보완한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

BDD (Behavior Driven Development, 행위 주도 개발)는 2006년 댄 노스 (Dan North)가 TDD의 의사소통 문제를 해결하기 위해 제안했다. TDD는 개발자 관점의 기술 테스트를 주도하지만, 비즈니스 관계자(기획자, PO)와 소통하기 어렵다는 한계가 있었다.

BDD는 "테스트"라는 단어 대신 "시나리오"와 "행위"를 사용하고, 자연어에 가까운 Given/When/Then 문법(Gherkin)으로 명세를 작성한다. 이 명세는 비기술자도 이해할 수 있으면서 동시에 자동화 테스트로 직접 실행 가능하다.

BDD가 실무에서 중요한 이유는 **요구사항 명확화**다. 개발자가 기획서를 읽고 추측하는 대신, 구체적인 시나리오(Given/When/Then)를 작성해 모호함을 제거한다. 시나리오 작성 과정에서 발견되는 엣지 케이스(Edge Case)와 정책 불명확이 실제 구현 전에 해결된다.

📢 **섹션 요약 비유**: BDD는 법률 계약서처럼, "어떤 상황(Given)에서 무슨 행동(When)을 하면 어떤 결과(Then)가 나와야 하는가"를 모든 관계자가 서명한 명세서다—개발자, 기획자, QA가 동일한 문서를 보고 일한다.

---

## 2. 구성요소

### Given/When/Then 구조

```text
Gherkin 문법:

Feature: 로그인 기능
  사용자가 계정으로 로그인할 수 있어야 한다.

  Scenario: 올바른 자격 증명으로 로그인 성공
    Given 사용자 "alice"가 등록되어 있고 비밀번호는 "secret"
    When 사용자가 "alice"와 "secret"으로 로그인을 시도할 때
    Then 로그인이 성공하고 홈 화면이 표시된다

  Scenario: 잘못된 비밀번호로 로그인 실패
    Given 사용자 "alice"가 등록되어 있고 비밀번호는 "secret"
    When 사용자가 "alice"와 "wrong"으로 로그인을 시도할 때
    Then 로그인이 실패하고 "비밀번호가 틀렸습니다" 메시지가 표시된다

각 요소:
  Given: 초기 컨텍스트 / 사전 조건
  When:  사용자의 행위 / 이벤트
  Then:  기대되는 결과 / 검증

  And, But: 복합 조건 연결
```

### BDD 전체 워크플로우

```text
┌──────────────────────────────────────────────────────────────┐
│                   BDD 워크플로우                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 발견 (Discovery)                                         │
│     → 비즈니스팀 + 개발팀 + QA 함께                         │
│     → "무엇을 만들어야 하는가" 시나리오 도출                 │
│     → Three Amigos Meeting                                   │
│                                                              │
│  2. 공식화 (Formulation)                                     │
│     → Given/When/Then Gherkin 문법으로 작성                  │
│     → 구체적 예시(Concrete Examples)로 명세화               │
│                                                              │
│  3. 자동화 (Automation)                                      │
│     → Step Definitions 코드로 연결                          │
│     → Cucumber/SpecFlow 실행                                 │
│     → CI/CD 파이프라인 통합                                  │
│                                                              │
│  4. 검증 (Validation)                                        │
│     → 자동화된 시나리오 실행                                 │
│     → 생존 문서(Living Documentation) 생성                  │
└──────────────────────────────────────────────────────────────┘
```

### BDD 도구 생태계

| 도구 | 언어 | 특징 |
|:---|:---|:---|
| Cucumber | Java, Ruby, JS, Python | 가장 널리 사용, Gherkin 지원 |
| SpecFlow | C# (.NET) | .NET 표준 BDD 도구 |
| Behave | Python | Python 생태계 |
| JBehave | Java | Cucumber 이전 세대 |
| Behat | PHP | PHP 생태계 |
| Playwright + BDD | JS/TS | E2E BDD |

```text
Cucumber Step Definitions 예시 (Java):
@Given("사용자 {string}가 등록되어 있고 비밀번호는 {string}")
public void givenUserRegistered(String username, String password) {
    userService.register(username, password);
}

@When("사용자가 {string}와 {string}으로 로그인을 시도할 때")
public void whenUserLogin(String username, String password) {
    result = authService.login(username, password);
}

@Then("로그인이 성공하고 홈 화면이 표시된다")
public void thenLoginSuccess() {
    assertThat(result.isSuccess()).isTrue();
}
```

📢 **섹션 요약 비유**: BDD의 Given/When/Then은 "안전 매뉴얼"과 같다. "화재가 발생했을 때(Given), 비상구 버튼을 누르면(When), 스프링클러가 작동해야 한다(Then)"—이 명세가 있어야 소방 시스템이 기대대로 동작하는지 테스트할 수 있다.

---

## 3. 구조 및 동작 원리

### TDD vs BDD vs ATDD

| 구분 | TDD | BDD | ATDD |
|:---|:---|:---|:---|
| 제안자 | Kent Beck | Dan North | Brian Marick |
| 관점 | 개발자 (구현) | 전체 팀 (행위) | QA (인수) |
| 언어 | 코드 | 자연어+코드 | 자연어 |
| 추상화 레벨 | 함수/메서드 | 기능/시나리오 | 비즈니스 가치 |
| 테스트 유형 | 단위 테스트 | 기능/행위 테스트 | 인수 테스트 |
| 도구 | JUnit, pytest | Cucumber, SpecFlow | FitNesse |

### Three Amigos Meeting

```text
BDD의 핵심 협업: Three Amigos

  🎩 비즈니스 (PO/기획자): "무엇을 만들어야 하는가"
  💻 개발자:               "어떻게 만들 것인가"
  🔍 QA:                  "어떻게 테스트할 것인가"

  세 관점이 모여 시나리오 작성 → 요구사항 모호성 제거
  → "왜 이 기능이 필요한가"까지 이해한 시나리오 도출
  
  산출물:
  - Gherkin 시나리오 명세
  - 엣지 케이스 목록
  - 완료 기준(Definition of Done)
```

📢 **섹션 요약 비유**: Three Amigos Meeting은 법률 문서 작성과 같다. 의뢰인(비즈니스), 변호사(개발자), 공증인(QA)이 함께 계약서를 작성해야 나중에 "이 조항이 무슨 뜻이야?" 분쟁이 없다.

---

## 4. 비교 및 트레이드오프

### BDD 시나리오 작성 모범 사례

```text
좋은 시나리오:
  ✅ 구체적인 예시 사용 (숫자, 이름, 날짜)
  ✅ 한 시나리오 = 하나의 행위 검증
  ✅ 비즈니스 관계자가 이해할 수 있는 언어
  ✅ UI 상세(버튼 클릭 등)보다 행위(로그인 시도) 중심

나쁜 시나리오:
  ❌ "로그인 버튼을 클릭한다" (UI 레벨)
  ✅ "사용자가 로그인을 시도한다" (행위 레벨)
  
  ❌ 모든 엣지 케이스를 하나의 시나리오에 담음
  ✅ 시나리오 아웃라인(Scenario Outline)으로 분리

  Scenario Outline: 다양한 자격 증명 테스트
    Given 사용자 <username>이 등록되어 있다
    When <username>과 <password>로 로그인을 시도한다
    Then <result>가 표시된다
    
    Examples:
      | username | password | result  |
      | alice    | secret   | 홈 화면 |
      | alice    | wrong    | 오류 메시지 |
      | unknown  | secret   | 오류 메시지 |
```

### 기술사 시험 판단 포인트

1. **BDD = TDD 확장**: TDD의 의사소통 문제를 해결하기 위한 진화—같은 철학(먼저 명세, 나중 구현)이지만 추상화 레벨이 다름.

2. **Given = 초기 상태, When = 행위, Then = 검증**: 이 구조가 핵심.

3. **Gherkin**: BDD 시나리오 작성 언어—Feature, Scenario, Given/When/Then, And, But, Examples.

4. **생존 문서 (Living Documentation)**: BDD 테스트가 곧 최신 요구사항 문서—코드와 문서가 항상 동기화.

📢 **섹션 요약 비유**: BDD의 생존 문서(Living Documentation)는 살아있는 교과서와 같다. 교과서(시나리오)가 실제 테스트와 연결되어 있어, 코드가 변경될 때마다 교과서가 자동으로 최신화된다.

---

## 5. 실무 적용 및 최적화 기법

BDD를 체계적으로 적용하면:

1. **요구사항-구현-테스트 일치**: 세 관점의 시나리오가 일치해 갭(Gap)이 없는 개발이 가능하다.
2. **회귀 방지**: 자동화된 시나리오가 CI/CD에서 실행되어 기존 기능 보호.
3. **의사소통 비용 감소**: 자연어 시나리오로 개발팀과 비즈니스팀 간 "번역 손실" 제거.
4. **생존 문서**: 항상 최신 상태의 기능 명세가 자동 생성된다.

BDD의 가장 흔한 실패 패턴은 **형식만 도입하고 협업 문화를 놓치는 것**이다. Given/When/Then을 개발자 혼자 쓰면 BDD의 가장 중요한 가치—Three Amigos의 공통 이해—가 사라진다. BDD는 도구가 아닌 **협업 방식**이다.

📢 **섹션 요약 비유**: BDD를 형식만 따르는 것은 영어를 공부하면서 번역기만 쓰는 것과 같다. 형식(Given/When/Then)은 있지만 실제 소통(Three Amigos)이 없으면 BDD의 핵심 가치를 얻지 못한다.

---

### 📌 관련 개념 맵

| 개념 | 설명 | 연관 키워드 |
|:---|:---|:---|
| BDD (Behavior Driven Development) | Given/When/Then 기반 행위 주도 개발 | Dan North, TDD |
| Gherkin | BDD 시나리오 작성 DSL | Feature, Scenario |
| Given/When/Then | 초기 상태/행위/기대 결과 구조 | 시나리오 명세 |
| Cucumber | 대표적 BDD 프레임워크 | Step Definitions |
| Three Amigos | PO+개발자+QA 협업 세션 | 요구사항 명확화 |
| Living Documentation | 시나리오=항상 최신 명세 문서 | 문서 자동화 |
| ATDD (Acceptance Test Driven Development) | 인수 테스트 주도 개발 | BDD 관련 기법 |
| Step Definitions | Gherkin 시나리오와 코드 연결 | Cucumber |

---

### 👶 어린이를 위한 3줄 비유 설명

1. BDD는 "이 게임에서 어떻게 이길 수 있는가"를 미리 약속하는 것이에요 — "특정 아이템을 얻으면(Given), 보스를 공격하면(When), 100점을 얻어야 한다(Then)"처럼요.
2. 기획자, 개발자, 테스터가 함께 약속을 만들어요(Three Amigos) — 서로 다른 말을 하지 않으려고요.
3. 약속이 코드로 자동 테스트되어서, 게임이 업데이트될 때마다 약속대로 동작하는지 자동으로 확인돼요.
