+++
title = "73. XP (eXtreme Programming)"
date = "2026-03-05"
[extra]
categories = "studynotes-se"
+++

# XP (eXtreme Programming)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: XP(eXtreme Programming)는 켄트 벡(Kent Beck)이 1996년 개발한 애자일 방법론으로, 좋은 실천 방법을 극단(extreme)까지 밀어붙여 소프트웨어 품질과 고객 만족을 동시에 달성하는, 기술적 탁월함을 강조하는 개발 방법론이다.
> 2. **가치**: XP 적용 시 결함 밀도를 40-60% 감소시키고, 생산성을 25-50% 향상시키며, 프로젝트 성공률을 80% 이상으로 끌어올리는 것으로 입증되었다.
> 3. **융합**: XP는 TDD(테스트 주도 개발), CI(지속적 통합), 리팩토링, 짝 프로그래밍을 융합하여 코드 품질을 보장하고, 스크럼의 프로젝트 관리 프레임워크와 결합하여 하이브리드 애자일을 구현한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의
XP(eXtreme Programming)는 소프트웨어 개발의 불확실성을 관리하기 위해 고안된 경량급 방법론으로, **5가지 가치**(용기, 존중, 의사소통, 단순성, 피드백)와 **12가지 실천 방법**(Primary Practices)을 통해 고품질 소프트웨어를 빠르게 개발한다. XP의 핵심 철학은 "좋은 것을 극단까지 밀어붙이는 것"으로, 예를 들어 코드 리뷰가 좋다면 **짝 프로그래밍**으로 극단화하고, 테스트가 좋다면 **TDD**로 극단화한다.

### 💡 비유
XP는 **"스포츠 팀의 집중 훈련 캠프"**에 비유할 수 있다. 모든 선수가 같은 공간에서(전체 팀 같은 방), 서로 코칭하며(짝 프로그래밍), 실전에서 바로 써먹을 수 있는 기술만 연습하고(단순 설계), 매 경기 후 즉시 피드백을 받아(짧은 릴리즈), 실수를 두려워하지 않고 도전한다(용기). 혼자서 몰래 연습하는 것보다 함께 집중적으로 훈련할 때 실력이 빨리 는다.

### 등장 배경 및 발전 과정

**1. 기존 방법론의 치명적 한계점**
- Heavyweight 방법론(RUP, CMM)의 과도한 문서화와 프로세스
- 요구사항 변경에 대한 높은 비용과 저항
- 결함이 개발 후반에 발견되어 수정 비용 급증
- 고객-개발팀 간 거리로 인한 커뮤니케이션 단절

**2. 혁신적 패러다임 변화**
- 1996년 켄트 벡이 크라이슬러 C3 프로젝트에서 XP 창안
- 1999년 "Extreme Programming Explained" 출판으로 대중화
- 2000년대 TDD, CI의 표준화와 도구 발전
- 2010년대 DevOps, SRE의 기술적 기반 제공

**3. 비즈니스적 요구사항**
- 변화하는 요구사항에 대한 민첩한 대응
- 고품질 소프트웨어의 지속적 인도
- 개발팀의 번아웃 방지와 지속 가능한 속도

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/도구 | 비유 |
|-----------|-----------|---------------------|----------------|------|
| **짝 프로그래밍** | 실시간 코드 리뷰 | 드라이버-내비게이터 교대 | VS Code Live Share | 듀엣 피아노 |
| **TDD** | 테스트 우선 개발 | Red-Green-Refactor 사이클 | JUnit, pytest, Jest | 레시피 검증 |
| **지속적 통합** | 빈번한 통합 | 자동화 빌드/테스트 | Jenkins, GitHub Actions | 오케스트라 조율 |
| **리팩토링** | 코드 구조 개선 | 작은 단계, 안전한 변경 | IDE, 정적 분석 | 방 정리 |
| **단순 설계** | 필요한 만큼만 | YAGNI, KISS 원칙 | Architecture Katas | 미니멀리즘 |
| **메타포** | 시스템 공통 언어 | 비즈니스-기술 용어 매핑 | Domain Language | 건축 설계도 |

### XP 5가지 가치

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                         XP FIVE VALUES (XP 5가지 가치)                         │
│                                                                                │
│                          ┌─────────────────────┐                              │
│                          │    COMMUNICATION    │                              │
│                          │    (의사소통)        │                              │
│                          │                     │                              │
│                          │  • 전체 팀 같은 방   │                              │
│                          │  • 짝 프로그래밍     │                              │
│                          │  • 실제 고객 참여    │                              │
│                          └──────────┬──────────┘                              │
│                                     │                                          │
│          ┌──────────────────────────┼──────────────────────────┐              │
│          │                          │                          │              │
│          ▼                          ▼                          ▼              │
│   ┌─────────────┐           ┌─────────────┐           ┌─────────────┐        │
│   │  SIMPLICITY │           │   FEEDBACK  │           │    COURAGE  │        │
│   │  (단순성)   │           │   (피드백)   │           │    (용기)   │        │
│   │             │           │             │           │             │        │
│   │ • YAGNI     │           │ • 짧은 릴리즈│           │ • 코드 폐기 │        │
│   │ • 최선 설계 │           │ • TDD       │           │ • 리팩토링  │        │
│   │ • 리팩토링  │           │ • 고객 피드백│           │ • 진실 말하기│        │
│   └─────────────┘           └─────────────┘           └─────────────┘        │
│          │                          ▲                          │              │
│          │                          │                          │              │
│          └──────────────────────────┼──────────────────────────┘              │
│                                     │                                          │
│                          ┌──────────┴──────────┐                              │
│                          │     RESPECT         │                              │
│                          │     (존중)          │                              │
│                          │                     │                              │
│                          │ • 팀원 신뢰         │                              │
│                          │ • 집단 코드 소유    │                              │
│                          │ • 지속 가능한 속도  │                              │
│                          └─────────────────────┘                              │
│                                                                                │
└───────────────────────────────────────────────────────────────────────────────┘
```

### 정교한 구조 다이어그램: XP 12가지 실천 방법

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    XP 12 PRIMARY PRACTICES (12가지 실천 방법)                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                     PROGRAMMING PRACTICES (프로그래밍 실천)               │   │
│  │                                                                          │   │
│  │   ┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐  │   │
│  │   │  Pair Programming │   │       TDD         │   │   Refactoring     │  │   │
│  │   │   (짝 프로그래밍)  │   │  (테스트 주도 개발)│   │    (리팩토링)     │  │   │
│  │   │                   │   │                   │   │                   │  │   │
│  │   │  Driver ↔ Navigator│   │  Red → Green →    │   │  작은 단계로      │  │   │
│  │   │                   │   │  Refactor         │   │  안전하게 변경     │  │   │
│  │   │  • 실시간 리뷰    │   │                   │   │                   │  │   │
│  │   │  • 지식 공유      │   │  • 테스트 먼저    │   │  • 중복 제거      │  │   │
│  │   │  • 결함 감소      │   │  • 설계 유도      │   │  • 복잡도 감소    │  │   │
│  │   └───────────────────┘   └───────────────────┘   └───────────────────┘  │   │
│  │                                                                          │   │
│  │   ┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐  │   │
│  │   │  Simple Design    │   │ Collective Code   │   │ Coding Standards  │  │   │
│  │   │   (단순 설계)     │   │  Ownership        │   │  (코딩 표준)      │  │   │
│  │   │                   │   │  (공동 코드 소유) │   │                   │  │   │
│  │   │  • 현재 요구 충족 │   │                   │   │  • 일관된 스타일  │  │   │
│  │   │  • 불필요 복잡성  │   │  • 누구나 수정    │   │  • 가독성 향상    │  │   │
│  │   │    제거           │   │  • 페어로 안전성  │   │  • 리팩토링 용이  │  │   │
│  │   │  • YAGNI 원칙     │   │                   │   │                   │  │   │
│  │   └───────────────────┘   └───────────────────┘   └───────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    INTEGRATION PRACTICES (통합 실천)                      │   │
│  │                                                                          │   │
│  │   ┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐  │   │
│  │   │ Continuous        │   │ Small Releases    │   │ Sustainable Pace  │  │   │
│  │   │ Integration (CI)  │   │  (작은 릴리즈)    │   │ (지속 가능한 속도)│  │   │
│  │   │ (지속적 통합)     │   │                   │   │                   │  │   │
│  │   │                   │   │  • 잦은 배포      │   │  • 40시간/주      │  │   │
│  │   │  • 자동화 빌드    │   │  • 빠른 피드백    │   │  • 오버타임 금지  │  │   │
│  │   │  • 즉시 테스트    │   │  • 리스크 감소    │   │  • 번아웃 방지    │  │   │
│  │   │  • 통합 문제 조기 │   │  • 가치 조기 전달 │   │  • 일관된 속도    │  │   │
│  │   │    발견           │   │                   │   │                   │  │   │
│  │   └───────────────────┘   └───────────────────┘   └───────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                      TEAM PRACTICES (팀 실천)                            │   │
│  │                                                                          │   │
│  │   ┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐  │   │
│  │   │  Whole Team       │   │ On-Site Customer  │   │     Metaphor      │  │   │
│  │   │   (전체 팀)       │   │ (현장 고객)       │   │    (메타포)       │  │   │
│  │   │                   │   │                   │   │                   │  │   │
│  │   │  • 같은 공간      │   │  • 실제 사용자    │   │  • 공통 언어      │  │   │
│  │   │  • 교차 기능팀    │   │  • 즉각적 피드백  │   │  • 시스템 비유    │  │   │
│  │   │  • 자기 조직화    │   │  • 우선순위 결정  │   │  • 이해 증진      │  │   │
│  │   └───────────────────┘   └───────────────────┘   └───────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: TDD 사이클

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                           TDD CYCLE (Red-Green-Refactor)                       │
│                                                                                │
│                              ┌─────────────┐                                  │
│                              │   REFACTOR  │                                  │
│                              │   (리팩토링) │                                  │
│                              │             │                                  │
│                              │ • 중복 제거 │                                  │
│                              │ • 코드 정리 │                                  │
│                              │ • 설계 개선 │                                  │
│                              └──────┬──────┘                                  │
│                                     │                                          │
│                                     ▼                                          │
│          ┌──────────────────────────────────────────────────────────┐         │
│          │                                                          │         │
│          │     ┌─────────────┐              ┌─────────────┐         │         │
│          │     │             │              │             │         │         │
│          │     │    RED      │──────────────│   GREEN     │         │         │
│          │     │   (실패)    │              │   (통과)    │         │         │
│          │     │             │              │             │         │         │
│          │     │ 1. 테스트   │              │ 3. 최소     │         │         │
│          │     │    작성     │              │    구현     │         │         │
│          │     │             │              │             │         │         │
│          │     │ 2. 실패    │              │ 4. 통과     │         │         │
│          │     │    확인     │              │    확인     │         │         │
│          │     │             │              │             │         │         │
│          │     └─────────────┘              └─────────────┘         │         │
│          │                                                          │         │
│          │         🔴 FAIL                   🟢 PASS                │         │
│          │                                                          │         │
│          └──────────────────────────────────────────────────────────┘         │
│                                                                                │
│   Example: 로그인 기능 TDD                                                     │
│   ┌───────────────────────────────────────────────────────────────────────┐  │
│   │                                                                       │  │
│   │   Cycle 1: 기본 로그인                                                │  │
│   │   ┌────────────────────────────────────────────────────────────────┐ │  │
│   │   │ RED:                                                           │ │  │
│   │   │ def test_login_success():                                      │ │  │
│   │   │     user = User("alice", "password123")                        │ │  │
│   │   │     assert login(user.email, user.password) == True            │ │  │
│   │   │ # AssertionError: login() not defined                          │ │  │
│   │   │                                                                │ │  │
│   │   │ GREEN:                                                         │ │  │
│   │   │ def login(email, password):                                    │ │  │
│   │   │     return True  # Minimum implementation                     │ │  │
│   │   │                                                                │ │  │
│   │   │ REFACTOR:                                                      │ │  │
│   │   │ # Extract user validation logic                                │ │  │
│   │   └────────────────────────────────────────────────────────────────┘ │  │
│   │                                                                       │  │
│   │   Cycle 2: 잘못된 비밀번호                                            │  │
│   │   ┌────────────────────────────────────────────────────────────────┐ │  │
│   │   │ RED:                                                           │ │  │
│   │   │ def test_login_wrong_password():                               │ │  │
│   │   │     assert login("alice@test.com", "wrong") == False           │ │  │
│   │   │                                                                │ │  │
│   │   │ GREEN:                                                         │ │  │
│   │   │ def login(email, password):                                    │ │  │
│   │   │     user = find_user(email)                                    │ │  │
│   │   │     return user and user.password == password                  │ │  │
│   │   └────────────────────────────────────────────────────────────────┘ │  │
│   │                                                                       │  │
│   └───────────────────────────────────────────────────────────────────────┘  │
│                                                                                │
└───────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 알고리즘: TDD 예시 코드

```python
"""
TDD로 구현하는 계좌 이체 기능 예시
"""

import unittest
from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

# === RED Phase: 먼저 테스트 작성 ===

class TestAccountTransfer(unittest.TestCase):
    """계좌 이체 테스트"""

    def test_simple_transfer(self):
        """기본 이체 성공 테스트"""
        # Given
        source = Account("111-222", Decimal("1000.00"))
        target = Account("333-444", Decimal("500.00"))

        # When
        source.transfer_to(target, Decimal("300.00"))

        # Then
        self.assertEqual(source.balance, Decimal("700.00"))
        self.assertEqual(target.balance, Decimal("800.00"))

    def test_transfer_insufficient_balance(self):
        """잔액 부족 테스트"""
        source = Account("111-222", Decimal("100.00"))
        target = Account("333-444", Decimal("500.00"))

        with self.assertRaises(InsufficientBalanceError):
            source.transfer_to(target, Decimal("200.00"))

    def test_transfer_negative_amount(self):
        """음수 금액 이체 방지 테스트"""
        source = Account("111-222", Decimal("1000.00"))
        target = Account("333-444", Decimal("500.00"))

        with self.assertRaises(InvalidAmountError):
            source.transfer_to(target, Decimal("-100.00"))

    def test_transfer_to_same_account(self):
        """동일 계좌 이체 방지 테스트"""
        account = Account("111-222", Decimal("1000.00"))

        with self.assertRaises(SameAccountError):
            account.transfer_to(account, Decimal("100.00"))


# === GREEN Phase: 최소 구현 ===

@dataclass
class Account:
    """은행 계좌"""
    account_number: str
    balance: Decimal

    def transfer_to(self, target: 'Account', amount: Decimal) -> None:
        """다른 계좌로 이체"""
        # 유효성 검사
        if amount <= 0:
            raise InvalidAmountError("이체 금액은 양수여야 합니다")

        if self.account_number == target.account_number:
            raise SameAccountError("동일 계좌로 이체할 수 없습니다")

        if self.balance < amount:
            raise InsufficientBalanceError("잔액이 부족합니다")

        # 이체 실행
        self.balance -= amount
        target.balance += amount


class InsufficientBalanceError(Exception):
    """잔액 부족 예외"""
    pass


class InvalidAmountError(Exception):
    """잘못된 금액 예외"""
    pass


class SameAccountError(Exception):
    """동일 계좌 예외"""
    pass


# === REFACTOR Phase: 개선 ===

class AccountService:
    """계좌 서비스 (리팩토링된 버전)"""

    MIN_TRANSFER_AMOUNT = Decimal("0.01")

    def __init__(self, account_repository):
        self.account_repository = account_repository

    def transfer(self, source_number: str, target_number: str,
                 amount: Decimal) -> TransferResult:
        """
        계좌 이체 (개선된 버전)
        - 트랜잭션 관리
        - 이력 기록
        - 알림 발송
        """
        # 1. 유효성 검사
        self._validate_transfer(source_number, target_number, amount)

        # 2. 계좌 조회
        source = self.account_repository.find_by_number(source_number)
        target = self.account_repository.find_by_number(target_number)

        if not source or not target:
            raise AccountNotFoundError("계좌를 찾을 수 없습니다")

        # 3. 이체 실행 (트랜잭션)
        with self.account_repository.transaction():
            source.balance -= amount
            target.balance += amount

            self.account_repository.save(source)
            self.account_repository.save(target)

            # 이력 기록
            self._record_transfer(source, target, amount)

        return TransferResult(
            source_number=source_number,
            target_number=target_number,
            amount=amount,
            source_balance=source.balance,
            status="SUCCESS"
        )

    def _validate_transfer(self, source: str, target: str,
                           amount: Decimal) -> None:
        """이체 유효성 검사"""
        if source == target:
            raise SameAccountError("동일 계좌로 이체할 수 없습니다")

        if amount < self.MIN_TRANSFER_AMOUNT:
            raise InvalidAmountError(
                f"최소 이체 금액은 {self.MIN_TRANSFER_AMOUNT}입니다"
            )

    def _record_transfer(self, source, target, amount) -> None:
        """이체 이력 기록"""
        pass  # 구현 생략


@dataclass
class TransferResult:
    """이체 결과"""
    source_number: str
    target_number: str
    amount: Decimal
    source_balance: Decimal
    status: str


class AccountNotFoundError(Exception):
    """계좌 미발견 예외"""
    pass


if __name__ == "__main__":
    # 테스트 실행
    unittest.main(verbosity=2)
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: XP vs 스크럼 vs 칸반

| 비교 항목 | XP | 스크럼 | 칸반 |
|-----------|-----|--------|------|
| **초점** | 기술적 탁월성 | 프로젝트 관리 | 흐름 최적화 |
| **이터레이션** | 1-2주 | 1-4주 스프린트 | 연속적 흐름 |
| **역할** | 코치, 고객 | PO, SM, 개발팀 | 서비스 딜리버리 매니저 |
| **실천 방법** | 12가지 엄격 | 프레임워크 중심 | 원칙 중심 |
| **변경** | 즉시 수용 | 스프린트 내 고정 | 언제든 가능 |
| **추정** | 스토리 포인트 | 스토리 포인트 | 리드 타임 |
| **강점** | 코드 품질 | 예측 가능성 | 유연성 |
| **약점** | 적용 난이도 | 경직성 | 예측 어려움 |

### 과목 융합 관점 분석

#### 1. 소프트웨어 공학 × 품질 관리 융합
XP의 TDD와 리팩토링은 소프트웨어 품질 메트릭(결함 밀도, 코드 커버리지, 사이클로매틱 복잡도)을 직접 개선한다. CI는 품질 게이트(Quality Gate)를 자동화하여 지속적 품질 보증을 실현한다.

#### 2. 객체지향 설계 × 리팩토링 융합
XP의 리팩토링은 SOLID 원칙, 디자인 패턴, 코드 스멜 제거와 밀접하게 연관된다. 단순 설계(Simple Design)는 YAGNI(You Aren't Gonna Need It)와 KISS(Keep It Simple, Stupid) 원칙을 실현한다.

#### 3. 보안 × 시큐어 코딩 융합
XP의 TDD는 보안 테스트 케이스를 포함할 수 있다. 짝 프로그래밍은 "4-eyes principle"을 실시간으로 구현하여 보안 결함을 조기 발견한다. CI 파이프라인에 SAST/DAST를 통합하여 보안 품질을 자동화한다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단: 실무 시나리오 3가지

#### 시나리오 1: XP 실천 방법 선택적 도입
**상황**: 스타트업에서 XP 전체 도입이 어려움

**기술사적 의사결정 과정**:
1. **우선순위 선정**: TDD, CI, 짝 프로그래밍을 1단계로 선정
2. **점진적 도입**: 주 1회 짝 프로그래밍 데부터 시작
3. **측정**: 도입 전후 결함 밀도, 생산성 비교
4. **피드백**: 회고에서 도입 효과 평가 및 조정

#### 시나리오 2: 레거시 시스템에 TDD 도입
**상황**: 테스트 없는 레거시 코드에 TDD 적용 난항

**기술사적 의사결정 과정**:
1. **스트랭글러 패턴**: 새 기능은 TDD로, 기존 코드는 점진적
2. **특성 테스트**: 기존 동작을 포착하는 테스트 먼저 작성
3. **승인 테스트**: 블랙박스 테스트로 외부 동작 검증
4. **리팩토링 창구**: 테스트 추가 후 안전하게 리팩토링

#### 시나리오 3: 원격 팀에서 짝 프로그래밍
**상황**: 분산 팀에서 짝 프로그래밍 효과 감소

**기술사적 의사결정 과정**:
1. **도구 활용**: VS Code Live Share, Tuple 등 실시간 협업 도구
2. **시간대 고려**: 오버랩 시간에 짝 프로그래밍 집중
3. **비동기 리뷰**: PR 기반 코드 리뷰로 보완
4. **모빌리티 세션**: 정기적 온라인 모빌 프로그래밍

### 도입 시 고려사항 체크리스트

#### 기술적 고려사항
- [ ] CI/CD 파이프라인 구축
- [ ] 테스트 프레임워크 선정 (JUnit, pytest, Jest)
- [ ] 코드 커버리지 측정 도구 (JaCoCo, Coverage.py)
- [ ] 정적 분석 도구 (SonarQube, ESLint)

#### 운영/보안적 고려사항
- [ ] 팀의 XP 가치 이해도 및 동의
- [ ] 짝 프로그래밍을 위한 물리적/기술적 환경
- [ ] 지속 가능한 속도 준수 문화
- [ ] 보안 테스트를 TDD에 포함

### 주의사항 및 안티패턴

1. **Cargo Cult XP**: 형식만 따라하고 본질 무시
2. **No Tests TDD**: 테스트 없이 리팩토링만 반복
3. **Big Design Upfront**: 단순 설계 원칙 위배
4. **Hero Pairing**: 동일 파트너만 고수하여 지식 격리

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 도입 전 | 도입 후 | 개선율 |
|------|---------|---------|--------|
| 결함 밀도 | 15/KLOC | 5/KLOC | **67% 감소** |
| 코드 커버리지 | 30% | 85% | **183% 향상** |
| 평균 결함 수정 시간 | 4시간 | 1시간 | **75% 단축** |
| 팀 만족도 | 65% | 85% | **31% 향상** |
| 기술 부채 비율 | 25% | 8% | **68% 감소** |

### 미래 전망 및 진화 방향

1. **AI 페어 프로그래밍**: GitHub Copilot 등 AI와의 짝 프로그래밍
2. **AI 기반 리팩토링**: 자동화된 코드 개선 제안
3. **실시간 품질 모니터링**: 프로덕션에서의 지속적 품질 측정
4. **하이브리드 XP-DevOps**: SRE와 XP의 융합

### ※ 참고 표준/가이드
- **Extreme Programming Explained (Kent Beck, 1999)**: XP 원전
- **Test-Driven Development (Kent Beck, 2002)**: TDD 가이드
- **Refactoring (Martin Fowler, 1999)**: 리팩토링 카탈로그
- **Clean Code (Robert C. Martin, 2008)**: 코딩 표준 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)

1. [테스트 주도 개발](./77_tdd.md) - XP의 핵심 실천 방법
2. [지속적 통합](./76_continuous_integration.md) - XP의 통합 실천
3. [리팩토링](./78_refactoring.md) - XP의 품질 개선 기법
4. [짝 프로그래밍](./74_pair_programming.md) - XP의 협업 실천
5. [애자일 선언문](./61_agile_manifesto.md) - XP의 철학적 기반
6. [스크럼 프레임워크](./62_scrum_framework.md) - XP와 자주 결합되는 프레임워크

---

## 👶 어린이를 위한 3줄 비유 설명

**비유: 축구 팀 연습**

1. **함께 연습해요**: 혼자서 공을 차는 것보다 친구랑 같이 연습하면 실수를 금방 알 수 있어요. 한 명은 공을 차고, 한 명은 "거기 말고 여기가 더 좋아!"라고 알려줘요.

2. **시험부터 시작해요**: "공을 문에 넣을 수 있을까?" 먼저 시험해보고, 넣을 수 없으면 어떻게 넣을지 연습해요. 시험에 통과하면 더 멋지게 넣는 방법을 찾아요.

3. **매일 조금씩 발전해요**: 한 번에 모든 걸 다 하려고 하지 않고, 매일 조금씩 더 나아져요. 지치지 않게 적당히 쉬면서 오래 할 수 있어요.
