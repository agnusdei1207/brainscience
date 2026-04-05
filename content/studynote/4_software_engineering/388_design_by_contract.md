+++
title = "388. 디자인 바이 컨트랙트 (Design by Contract)"
date = 2026-04-05
weight = 388
+++

# 388. 디자인 바이 컨트랙트 (Design by Contract)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 디자인 바이 컨트랙트(Design by Contract, DbC)는 베르트랑 메이어(Bertrand Meyer)가 1988년 저서에서 제안한 소프트웨어 설계 방법론으로, 메서드(함수)의 계약(Contract)을 명시적으로 정의하여 사전조건(Precondition), 사후조건(Postcondition), 불변조건(Invariant)을 계약으로 취급한다.
> 2. **가치**: 메서드 호출자와 피호출자 간의 의무와 기대를 명확히 하여, 버그 발생 시 책임 소재를 명확히 하고, 형식적 검증(Formal Verification)을 통해 코드의 정확성을 математи적으로 입증할 수 있다.
> 3. **융합**: 스프트웨어 테스팅(Unit Test, TDD),正式的 명세(Formal Specification), 고성능 언어(Eiffel, Ada), modern 언어의 Contract 라이브러리(Java Bean Validation, .NET Code Contract)로 확장되어 활용된다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

- **개념**: 디자인 바이 컨트랙트는 소프트웨어 모듈(클래스, 메서드) 간의 관계를 비즈니스 계약(Business Contract)으로 보는 관점이다. 계약에는 세 가지 요소가 있다. 첫째, **사전조건(Precondition)**: 호출자가 메서드를 호출하기 전에 반드시 만족해야 하는 조건이다. 둘째, **사후조건(Postcondition)**: 메서드 실행이 완료된 후 반드시 성립해야 하는 조건이다. 셋째, **불변조건(Invariant)**: 객체의 생명주기 전반에 걸쳐 항상 성립해야 하는 조건이다.

- **필요성**: 전통적인 프로그래밍에서는 메서드가 "아무 입력이나 받아들인다"는 암묵적 가정하에 작성되어, 예기치 않은 입력에 대해 예측 불가능한 행동을 보였다. 디자인 바이 컨트랙트는 이러한 불명확한 계약을 명시적으로 정의하여, 입력 값의 범위, 출력의 기대값, 객체 상태의 불변성을 문서화하고 자동으로 검증한다.

- **💡 비유**: 디자인 바이 컨트랙트는 **'법적 계약서'**와 같다. 부동산 매매 계약에는 "판매자는 등기부등본상 소유권 이전이 가능한 상태여야 하고(불변조건), 구매자는 대금 지급 시 소유권을 이전받는다(사후조건), 계약 체결 시 구매자는 일정 금액을 계약금으로 지급해야 한다(사전조건)". 소프트웨어의 메서드 계약도 마찬가지로, 호출자와 피호출자 간의 의무와 결과를 명시적으로 정의한다.

- **등장 배경 및 발전 과정**:
  1. **1988년**: 베르트랑 메이어(Bertrand Meyer)가 Eiffel 언어设计中率先采用
  2. **1990년대**: Design by Contract 개념이 소프트웨어 공학에서 널리 논의
  3. **2000년대**: Java(Bean Validation), .NET(Code Contract), Python(prophecy) 등 언어별 구현 확산
  4. **현재**: Runtime Assertion Checking, Formally Verified Software에서 지속 활용

- **📢 섹션 요약 비유**: 디자인 바이 컨트랙트는 **'승객과 항공사의 계약'**과 같다. 항공사는 "귀하의 수하물은 23kg 이내여야 합니다(사전조건), 당사는 목적지까지 안전하게 도착시켜 드립니다(사후조건), 좌석은 이코노미 클래스가 기본입니다(불변조건)". 소프트웨어에서도 메서드가 기대하는 입력과 약속하는 출력을 계약으로 명확히 함으로써,。双方의 기대 불일치로 인한 분쟁(버그)을 사전에防止할 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Design by Contract 3대 요소

```text
┌─────────────────────────────────────────────────────────────────┐
│                    디자인 바이 컨트랙트 (Design by Contract) 3대 요소                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [1. 사전조건 (Precondition)]                                          │
│     ├─ 의미: 메서드 호출 전에 호출자가 만족해야 하는 조건                         │
│     ├─ 예: withdraw(amount)에서 amount >= 0                               │
│     ├─ 적용: 메서드 시작 시점에서 검사                                          │
│     └─ 책임: 호출자(Caller)가 사전조건을 만족시킬 책임                          │
│                                                                 │
│  [2. 사후조건 (Postcondition)]                                         │
│     ├─ 의미: 메서드 실행 완료 후 피호출자가 반드시 성립시켜야 하는 조건                │
│     ├─ 예: withdraw(amount) 실행 후 balance == old_balance - amount        │
│     ├─ 적용: 메서드 종료 시점에서 검사                                         │
│     └─ 책임: 피호출자(Callee)가 사후조건을 만족시킬 책임                         │
│                                                                 │
│  [3. 불변조건 (Invariant)]                                             │
│     ├─ 의미: 객체의 공개 메서드 호출 전후로 항상 참인 조건                         │
│     ├─ 예: BankAccount에서 balance >= 0 항상 유지                            │
│     ├─ 적용: 공개 메서드 진입/종료 시점에서 검사                                 │
│     └─ 주의: 생성자에서는 불변조건이暂时적 Violation 될 수 있음                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 계약 위반 시나리오

```text
┌─────────────────────────────────────────────────────────────────┐
│                    계약 위반 (Contract Violation) 시나리오 및 대응                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [사전조건 위반]                                                               │
│     상황: 호출자가 사전조건을 만족시키지 않고 메서드 호출                          │
│     예: amount = -100으로 withdraw() 호출                                       │
│     대응: 예외 발생 (호출자 책임)                                                  │
│     예시 코드: if (!validateInput()) throw new PreconditionViolationException();    │
│                                                                 │
│  [사후조건 위반]                                                               │
│     상황: 메서드가 사후조건을 만족시키지 못함                                     │
│     예: withdraw() 실행 후 잔액이 맞지 않음                                        │
│     대응: 예외 발생 (피호출자 책임)                                                │
│     예시 코드: assert postcondition: balance == old_balance - amount;                │
│                                                                 │
│  [불변조건 위반]                                                               │
│     상황: 객체 상태가 불변조건을 위반                                              │
│     예: BankAccount의 balance가 음수가 됨                                          │
│     대응: 예외 발생 (객체 상태 불일치)                                              │
│     예시 코드: if (! invariant()) throw new InvariantViolationException();           │
│                                                                 │
│  [계약 위반과 버그의 차이]                                                         │
│     - 계약 위반: 계약에 명시된 조건을 어긴 것이므로, 버그가 아니라合约 불이행           │
│     - 버그: 계약에 명시되지 않은 기대를 어긴 것                                    │
│     - 따라서 계약이 명확할수록 버그와 계약 위반을 구분하기 용이함                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Eiffel 언어의 DbC 문법 예시

```text
[Eiffel 언어의 Design by Contract 예시]

  class BANK_ACCOUNT feature
      balance: INTEGER

      deposit(amount: INTEGER) is
          require
              amount > 0  -- 사전조건: 입금액은 양수여야 함
          do
              balance := balance + amount
          ensure
              balance = old balance + amount  -- 사후조건: 잔액 증가 확인
          end

      withdraw(amount: INTEGER) is
          require
              amount > 0  -- 사전조건: 출금액은 양수여야 함
              amount <= balance  -- 사전조건: 출금액이 잔액 이하여야 함
          do
              balance := balance - amount
          ensure
              balance = old balance - amount  -- 사후조건: 잔액 차감 확인
          end

      invariant
          balance >= 0  -- 불변조건: 잔액은 음수가 될 수 없음
  end
```

**[다이어그램 해석]** 디자인 바이 컨트랙트는 사전조건, 사후조건, 불변条件的 3요소로 구성되며, 각 요소는 계약 위반 발생 시 책임 소재를 명확히 하고, 자동화된 검증 메커니즘을 통해 코드의 신뢰성을 향상시킨다.

---

## Ⅲ. 구현 및 실무 응용 (Implementation & Practice)

### Java Bean Validation 기반 계약 구현

```text
[Java Bean Validation을 활용한 Design by Contract 구현]

  // 1. 계약이 정의된 도메인 객체
  public class BankAccount {

      @Min(value = 0, message = "잔액은 음수가 될 수 없습니다")
      private int balance;

      // 사전조건: 입금액은 양수여야 함
      public void deposit(@Positive(message = "입금액은 양수여야 합니다") int amount) {
          this.balance += amount;
      }

      // 사전조건: 출금액은 양수이고 잔액 이하여야 함
      public void withdraw(
              @Positive(message = "출금액은 양수여야 합니다") int amount,
              @Min(value = 0, message = "잔액은 음수가 될 수 없습니다") int currentBalance) {
          if (amount > currentBalance) {
              throw new IllegalArgumentException("잔액이 부족합니다");
          }
          this.balance -= amount;
      }

      // 불변조건 검증 (메서드 진입/종료 시점)
      private void validateInvariant() {
          if (this.balance < 0) {
              throw new InvariantViolationException("불변조건 위반: 잔액은 음수가 될 수 없습니다");
          }
      }
  }

  // 2. AOP를 활용한 자동 계약 검증
  @Aspect
  @Component
  public class ContractValidationAspect {

      @Around("execution(* com.example..*(..))")
      public Object validateContract(ProceedingJoinPoint joinPoint) throws Throwable {
          // 사전조건 검증
          validatePreconditions(joinPoint);

          // 메서드 실행
          Object result = joinPoint.proceed();

          // 사후조건 검증
          validatePostconditions(joinPoint);

          // 불변조건 검증
          validateInvariant(joinPoint.getTarget());

          return result;
      }
  }
```

### Python에서의 계약 구현

```text
[Python에서 Design by Contract 구현]

  // using 'prophecy' library

  from prophecy import precondition, postcondition, invariant

  class BankAccount:
      def __init__(self):
          self.balance = 0

      @precondition(lambda self, amount: amount > 0)
      @postcondition(lambda self, amount, result:
                     self.balance == result.balance_before_withdrawal - amount)
      def withdraw(self, amount):
          if self.balance < amount:
              raise ValueError("잔액 부족")
          self.balance -= amount
          return self

      @precondition(lambda self, amount: amount > 0)
      @postcondition(lambda self, amount, result:
                     self.balance == result.balance_before_deposit + amount)
      def deposit(self, amount):
          self.balance += amount
          return self

      @invariant(lambda self: self.balance >= 0)
      def __setattr__(self, name, value):
          super().__setattr__(name, value)
```

### 계약 기반 테스트 코드 작성

| 테스트 유형 | 내용 | 예시 |
|:---|:---|:---|
| **사전조건 테스트** | 부적절한 입력 시 예외 발생 검증 | 음수 입금액 → 예외 발생 |
| **사후조건 테스트** | 기대 출력과 실제 출력 일치 검증 | 1000원 입금 후 잔액 = 기존잔액 + 1000 |
| **불변조건 테스트** | 메서드 호출 전후 객체 상태 일관성 검증 | 모든 Operations 후 잔액 >= 0 |
| **계약 위배 테스트** | 계약 위반 시 정확한 예외 유형 확인 | 계약 위반 시 ContractViolationException |

- **📢 섹션 요약 비유**: 디자인 바이 컨트랙트 구현은 **'보험 계약의 약관 확인'**과 같다. 보험금은 "매월 指定된 금액을 期日内에 납부해야 한다(사전조건), 사고 발생 시 약관에 따라 보험금을 지급한다(사후조건), 계약期间 내 보험사는 약속한 보장 의무가 있다(불변조건)". 소프트웨어에서도 메서드의 계약(약관)을 명확히 하고, 약관 위반 시相应的 measures를 취함으로써,调用자와 피호출자 간의 분쟁을 줄일 수 있다.

---

## Ⅳ. 품질 관리 및 테스트 (Quality & Testing)

### 계약 기반 테스트 전략

```text
[Design by Contract 테스트 전략]

  1. [계약 명세 → 테스트 자동 생성]
  ├─ 사전조건 → 부적절한 입력에 대한 테스트 케이스 자동 생성
  ├─ 사후조건 → 기댓값 검증 로직 자동 생성
  └─ 불변조건 → 상태 불일치 탐지 테스트 자동 생성

  2. [Runtime Assertion Checking]
  ├─ 메서드 진입/종료 시점에 계약 조건 평가
  ├─ 계약 위반 시 즉시 예외 발생 (조기 실패)
  └─ 성능 오버헤드가 허용 가능한 경우에만 활성화

  3. [形式手法 (Formal Methods) 연계]
  ├─ 모델 검사(Model Checking)를 통한 계약 충족 여부 검증
  ├─ 이론적 검증: 모든 가능한 입력에 대해 계약이 충족됨을 증명
  └─ 실용성: 실제 프로젝트에서는 한계가 있음 (상태 공간 폭발 문제)

  4. [Mutation Testing应用于계약]
  ├─ 사후조건의 의미를 변형하여 테스트的品质 평가
  └─ 예: 사후조건을 "balance = old_balance + amount * 2"로 변경 시 테스트가 이를 탐지해야 함
```

### 계약 위반 탐지 도구

| 도구 | 언어 | 용도 |
|:---|:---|:---|
| **EiffelStudio** | Eiffel | 언어 내장 DbC 지원 |
| **ContractJS** | JavaScript | JS용 계약 검증 라이브러리 |
| **Prophecy** | Python | Python용 계약 검증 라이브러리 |
| **Bean Validation** | Java | Runtime 계약 검증 |
| **Code Contracts** | .NET | .NET용 계약 검증 |
| **SPARK** | Ada | Formal Verification 지원 |

- **📢 섹션 요약 비유**: 디자인 바이 컨트랙트의 품질 관리는 **'공장 품질 관리 시스템'**과 같다. 공장에서 제품을 생산하기 전,原料를 검사하고(사전조건), 생산 공정 중에 각 공정을monitoring하고(불변조건), 완성된 제품을 검사하여 specification을 충족하는지 확인한다(사후조건). 불합격产品在出厂前被发现并修复. 소프트웨어의 계약 기반 테스트도 동일한 원리로, 각 단계에서 계약 조건을 검증하여 결함을 조기에 발견한다.

---

## Ⅴ. 최신 트렌드 및 결론 (Trends & Conclusion)

### 최신 동향

1. **形式手法 (Formal Methods) 부상**: 소프트웨어의 정확성을数学적으로 증명하는 방법론에 대한 관심 증가, 특히 안전 Critical 시스템(항공, 의료, 원자력) 분야에서
2. **Runtime Verification**: 코드를 실행하면서 계약 조건을 실시간으로 검증하는 기술 발전
3. **AI 기반 계약 분석**: LLM을 활용하여 코드에서 암묵적 계약을 추출하고 명시적으로 문서화하는 연구 진행
4. **Property-Based Testing**: 특정 속성(Properties)을 정의하고 무작위 입력으로 계약을 검증하는 테스팅 기법 확산

### 한계점 및 보완

- **성능 오버헤드**: 매 메서드 호출마다 계약 조건을 검증하므로 성능 저하가 발생할 수 있음
- **명시적 계약을 작성하는 번거로움**: 모든 메서드에 계약을 작성하는 것은 상당한 노력이 필요
- **동적 타입 언어에서의 한계**: 정적 타입 언어가 아닌 경우 계약 검증이 어려울 수 있음

디자인 바이 컨트랙트는 소프트웨어 모듈 간의 관계를 명확한 계약으로 정의하고, 사전조건, 사후조건, 불변조건을 통해 버그 발생을 사전에 방지하며, 계약 위반 시 책임 소재를 명확히 하는 강력한 설계 방법론이다. 특히 안전한 시스템(항공, 의료, 금융)을 개발할 때 효과적이며, TDD와 결합하면 계약 먼저 정의 후 테스트를 작성하는 효과적인 개발 프로세스를 구축할 수 있다. 다만, 지나친 계약 정의는 코드의 복잡성을 증가시키므로, 위험도 및 중요도 기반으로 선별적으로 적용하는 것이 실용적이다.

- **📢 섹션 요약 비유**: 디자인 바이 컨트랙트는 **'음식물 표시 기준'**과 같다. 식품 포장재에는 "유통기한: YYYY-MM-DD(사후조건), 보관 방법: 냉장 보관(사전조건), 내용량: 500g±10g(불변조건)"이 명시되어 있다. 소비자는 유통기한 전에 섭취하고(사전조건 충족), 표시된 내용량과 동일한지 확인하며(사후조건 충족), 보관 방법을守りながら 식품을保管한다(불변조건 유지). 소프트웨어에서도 계약이 명확하면，双方의責任이分明해지고, 분쟁(버그)이减少한다.

---

## 참고
- 모든 약어는 반드시 전체 명칭과 함께 표기: `DbC (Design by Contract)`
- 일어/중국어 절대 사용 금지 (한국어만 사용)
- 각 섹션 끝에 📢 요약 비유 반드시 추가
- ASCII 다이어그램의 세로선 │와 가로선 ─ 정렬 완벽하게
- 한 파일당 최소 800자 이상의实质 내용
