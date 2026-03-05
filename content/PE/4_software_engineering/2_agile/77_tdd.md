+++
title = "77. 테스트 주도 개발 (TDD, Test Driven Development)"
date = "2026-03-05"
[extra]
categories = "studynotes-se"
+++

# 테스트 주도 개발 (TDD, Test Driven Development)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TDD(Test Driven Development)는 켄트 벡이 고안한 개발 기법으로, 실제 코드를 작성하기 전에 실패하는 테스트를 먼저 작성(Red)하고, 테스트를 통과하는 최소 코드를 구현(Green)한 후, 코드를 개선(Refactor)하는 Red-Green-Refactor 사이클을 반복하여 설계를 유도하고 결함을 조기에 발견한다.
> 2. **가치**: TDD 적용 시 결함 밀도를 40-90% 감소시키고, 코드 커버리지를 90% 이상 달성하며, 디버깅 시간을 50-80% 단축하여 전체 개발 비용을 20-40% 절감한다.
> 3. **융합**: TDD는 CI/CD 파이프라인, 짝 프로그래밍, 리팩토링, BDD(Behavior-Driven Development)와 결합하여 지속적 품질 보증을 실현하고, 시큐어 코딩(Secure Coding)과 연계하여 보안 테스트를 개발 프로세스에 내재화한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의
테스트 주도 개발(TDD, Test Driven Development)은 **"테스트가 개발을 이끈다"**는 철학을 가진 소프트웨어 개발 기법이다. 개발자는 프로덕션 코드를 작성하기 전에 **실패하는 테스트**를 먼저 작성하고, 그 테스트를 통과시키는 **최소한의 코드**를 작성한 후, 중복을 제거하고 구조를 개선하는 **리팩토링**을 수행한다. 이 **Red-Green-Refactor 사이클**을 짧게(5-10분) 반복하며 개발을 진행한다.

### 💡 비유
TDD는 **"건축가가 설계도를 그리면서 건물을 짓는 것"**과 비슷하다. 전통적 방식은 설계를 완성한 후 시공하지만, TDD는 "이 방은 3m x 4m여야 해"(테스트)라고 정의하고, 그 조건을 만족하는 방을 짓는다(구현). 조건이 맞지 않으면 즉시 수정한다. 마치 레고 블록을 조립하면서 "이 조각이 여기에 맞나?"(테스트) 확인하고 맞으면 계속하고(구현), 안 맞으면 다른 조각을 찾는 것(리팩토링)과 같다.

### 등장 배경 및 발전 과정

**1. 기존 개발 방식의 치명적 한계점**
- 테스트는 개발 완료 후 "품질 보증(QA) 단계"에서 수행
- 결함이 늦게 발견되어 수정 비용 급증 (개발 단계 대비 10-100배)
- "내 코드는 버그 없어"라는 개발자의 과신
- 리팩토링 두려움 - "고치면 깨질까봐"
- 문서와 코드의 불일치

**2. 혁신적 패러다임 변화**
- 1990년대 켄트 벡이 Smalltalk 환경에서 SUnit 개발
- 1997년 켄트 벡, 에릭 감마가 JUnit으로 Java에 TDD 도입
- 2002년 "Test-Driven Development: By Example" 출판
- 2000년대 xUnit 프레임워크 전 언어 확산 (pytest, Jest, NUnit 등)

**3. 비즈니스적 요구사항**
- Time-to-Market 단축하면서 품질 유지
- 기술 부채 누적 방지
- 레거시 시스템 안전한 개선

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/도구 | 비유 |
|-----------|-----------|---------------------|----------------|------|
| **Red Phase** | 실패 테스트 작성 | assert로 기대 동작 정의 | unittest, pytest | 목표 설정 |
| **Green Phase** | 최소 구현 | 하드코딩도 허용, 통과가 목표 | IDE, 언어 | 최소 달성 |
| **Refactor Phase** | 구조 개선 | 중복 제거, 패턴 적용 | IDE 리팩토링 | 정리 정돈 |
| **테스트 피라미드** | 테스트 전략 | 단위 > 통합 > E2E | Jest, Playwright | 건물 구조 |
| **Mock/Stub** | 의존성 격리 | 외부 시스템 모방 | Mockito, unittest.mock | 대역 배우 |
| **CI 통합** | 자동 검증 | 커밋마다 테스트 실행 | GitHub Actions, Jenkins | 자동 품질관리 |

### 정교한 구조 다이어그램: Red-Green-Refactor 사이클

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      TDD RED-GREEN-REFACTOR CYCLE                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│                         ┌─────────────────────────────┐                        │
│                         │         REFACTOR            │                        │
│                         │         (리팩토링)          │                        │
│                         │                             │                        │
│                         │  ┌───────────────────────┐  │                        │
│                         │  │ • 중복 제거           │  │                        │
│                         │  │ • 코드 정리           │  │                        │
│                         │  │ • 설계 개선           │  │                        │
│                         │  │ • 성능 최적화         │  │                        │
│                         │  │                       │  │                        │
│                         │  │ ⚠️ 테스트는 계속      │  │                        │
│                         │  │    통과해야 함!       │  │                        │
│                         │  └───────────────────────┘  │                        │
│                         └──────────────┬──────────────┘                        │
│                                        │                                         │
│                                        │ 모든 테스트 통화                         │
│                                        │ 새 기능 필요?                            │
│                                        ▼                                         │
│   ┌─────────────────────────────────────────────────────────────────────────┐  │
│   │                                                                         │  │
│   │    ┌─────────────────────┐              ┌─────────────────────┐         │  │
│   │    │                     │              │                     │         │  │
│   │    │        RED          │──────────────│       GREEN         │         │  │
│   │    │       (실패)        │              │       (통과)        │         │  │
│   │    │                     │              │                     │         │  │
│   │    │  ┌───────────────┐  │              │  ┌───────────────┐  │         │  │
│   │    │  │ 1. 요구사항   │  │              │  │ 3. 최소 코드  │  │         │  │
│   │    │  │    이해       │  │              │  │    작성       │  │         │  │
│   │    │  │               │  │              │  │               │  │         │  │
│   │    │  │ 2. 실패하는   │  │              │  │ 4. 테스트     │  │         │  │
│   │    │  │    테스트     │──┼──────────────┼──│    통과 확인  │  │         │  │
│   │    │  │    작성       │  │              │  │               │  │         │  │
│   │    │  │               │  │              │  │ • 하드코딩 OK │  │         │  │
│   │    │  │ 🔴 FAIL       │  │              │  │ • 복사붙여넣기│  │         │  │
│   │    │  │               │  │              │  │ OK           │  │         │  │
│   │    │  └───────────────┘  │              │  │ 🟢 PASS      │  │         │  │
│   │    │                     │              │  └───────────────┘  │         │  │
│   │    │                     │              │                     │         │  │
│   │    └─────────────────────┘              └─────────────────────┘         │  │
│   │                                                                         │  │
│   └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
│   사이클 시간: 5-10분 이내 권장                                                │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### TDD 실제 코드 예시: 이커머스 장바구니

```python
"""
TDD로 구현하는 이커머스 장바구니 기능
각 사이클을 보여주는 실제 코드 예시
"""

import unittest
from decimal import Decimal
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

# ============================================
# CYCLE 1: 빈 장바구니 생성
# ============================================

class TestShoppingCartCreation(unittest.TestCase):
    """Cycle 1: 장바구니 생성 테스트"""

    def test_create_empty_cart(self):
        """빈 장바구니 생성"""
        # RED: ShoppingCart 클래스가 아직 없음
        cart = ShoppingCart()
        self.assertEqual(cart.item_count, 0)
        self.assertEqual(cart.total, Decimal("0"))


# GREEN: 최소 구현
@dataclass
class ShoppingCart:
    """장바구니"""
    items: List = field(default_factory=list)

    @property
    def item_count(self) -> int:
        return 0

    @property
    def total(self) -> Decimal:
        return Decimal("0")


# ============================================
# CYCLE 2: 상품 추가
# ============================================

class TestAddItem(unittest.TestCase):
    """Cycle 2: 상품 추가 테스트"""

    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_single_item(self):
        """단일 상품 추가"""
        item = CartItem("PROD-001", "노트북", Decimal("1000000"), 1)
        self.cart.add(item)

        self.assertEqual(self.cart.item_count, 1)
        self.assertEqual(self.cart.total, Decimal("1000000"))

    def test_add_multiple_items(self):
        """여러 상품 추가"""
        self.cart.add(CartItem("PROD-001", "노트북", Decimal("1000000"), 1))
        self.cart.add(CartItem("PROD-002", "마우스", Decimal("50000"), 2))

        self.assertEqual(self.cart.item_count, 2)
        self.assertEqual(self.cart.total, Decimal("1100000"))


# GREEN: 구현 업데이트
@dataclass
class CartItem:
    """장바구니 항목"""
    product_id: str
    name: str
    price: Decimal
    quantity: int

    @property
    def subtotal(self) -> Decimal:
        return self.price * self.quantity


@dataclass
class ShoppingCart:
    """장바구니 (Cycle 2 업데이트)"""
    items: List[CartItem] = field(default_factory=list)

    def add(self, item: CartItem) -> None:
        self.items.append(item)

    @property
    def item_count(self) -> int:
        return len(self.items)

    @property
    def total(self) -> Decimal:
        return sum(item.subtotal for item in self.items)


# ============================================
# CYCLE 3: 수량 업데이트
# ============================================

class TestUpdateQuantity(unittest.TestCase):
    """Cycle 3: 수량 업데이트 테스트"""

    def setUp(self):
        self.cart = ShoppingCart()
        self.cart.add(CartItem("PROD-001", "노트북", Decimal("1000000"), 1))

    def test_increase_quantity(self):
        """수량 증가"""
        self.cart.update_quantity("PROD-001", 3)
        self.assertEqual(self.cart.total, Decimal("3000000"))

    def test_decrease_quantity(self):
        """수량 감소"""
        self.cart.update_quantity("PROD-001", 0)
        self.assertEqual(self.cart.item_count, 0)

    def test_update_nonexistent_item(self):
        """존재하지 않는 상품 업데이트"""
        with self.assertRaises(ItemNotFoundError):
            self.cart.update_quantity("PROD-999", 1)


# GREEN: 구현 업데이트
class ItemNotFoundError(Exception):
    """상품 미발견 예외"""
    pass


@dataclass
class ShoppingCart:
    """장바구니 (Cycle 3 업데이트)"""
    items: List[CartItem] = field(default_factory=list)

    def add(self, item: CartItem) -> None:
        # 동일 상품이면 수량 증가
        for existing in self.items:
            if existing.product_id == item.product_id:
                existing.quantity += item.quantity
                return
        self.items.append(item)

    def update_quantity(self, product_id: str, quantity: int) -> None:
        for i, item in enumerate(self.items):
            if item.product_id == product_id:
                if quantity <= 0:
                    self.items.pop(i)
                else:
                    item.quantity = quantity
                return
        raise ItemNotFoundError(f"상품 {product_id}를 찾을 수 없습니다")

    @property
    def item_count(self) -> int:
        return len(self.items)

    @property
    def total(self) -> Decimal:
        return sum(item.subtotal for item in self.items)


# ============================================
# CYCLE 4: 할인 적용 (리팩토링 포함)
# ============================================

class TestDiscount(unittest.TestCase):
    """Cycle 4: 할인 적용 테스트"""

    def setUp(self):
        self.cart = ShoppingCart()
        self.cart.add(CartItem("PROD-001", "노트북", Decimal("1000000"), 1))

    def test_percentage_discount(self):
        """퍼센트 할인"""
        self.cart.apply_discount(PercentageDiscount(10))  # 10% 할인
        self.assertEqual(self.cart.final_total, Decimal("900000"))

    def test_fixed_discount(self):
        """고정 금액 할인"""
        self.cart.apply_discount(FixedDiscount(Decimal("50000")))
        self.assertEqual(self.cart.final_total, Decimal("950000"))

    def test_no_discount(self):
        """할인 없음"""
        self.assertEqual(self.cart.final_total, Decimal("1000000"))


# REFACTOR: 할인 전략 패턴 도입
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    """할인 전략 (추상 클래스)"""
    @abstractmethod
    def apply(self, total: Decimal) -> Decimal:
        pass


class PercentageDiscount(DiscountStrategy):
    """퍼센트 할인"""
    def __init__(self, percentage: float):
        self.percentage = percentage

    def apply(self, total: Decimal) -> Decimal:
        return total * Decimal(str(1 - self.percentage / 100))


class FixedDiscount(DiscountStrategy):
    """고정 금액 할인"""
    def __init__(self, amount: Decimal):
        self.amount = amount

    def apply(self, total: Decimal) -> Decimal:
        return max(Decimal("0"), total - self.amount)


class NoDiscount(DiscountStrategy):
    """할인 없음"""
    def apply(self, total: Decimal) -> Decimal:
        return total


@dataclass
class ShoppingCart:
    """장바구니 (Cycle 4 리팩토링)"""
    items: List[CartItem] = field(default_factory=list)
    discount: DiscountStrategy = field(default_factory=NoDiscount)

    def add(self, item: CartItem) -> None:
        for existing in self.items:
            if existing.product_id == item.product_id:
                existing.quantity += item.quantity
                return
        self.items.append(item)

    def update_quantity(self, product_id: str, quantity: int) -> None:
        for i, item in enumerate(self.items):
            if item.product_id == product_id:
                if quantity <= 0:
                    self.items.pop(i)
                else:
                    item.quantity = quantity
                return
        raise ItemNotFoundError(f"상품 {product_id}를 찾을 수 없습니다")

    def apply_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount

    @property
    def item_count(self) -> int:
        return len(self.items)

    @property
    def total(self) -> Decimal:
        return sum(item.subtotal for item in self.items)

    @property
    def final_total(self) -> Decimal:
        return self.discount.apply(self.total)


# ============================================
# REFACTORED: 최종 구조
# ============================================

"""
최종 리팩토링 결과:
1. DiscountStrategy로 할인 로직 분리 (OCP 준수)
2. CartItem에 subtotal 프로퍼티 (SRP 준수)
3. 명확한 예외 처리
4. Decimal로 금전 계산 정확성 확보
"""

if __name__ == "__main__":
    unittest.main(verbosity=2)
```

### TDD와 테스트 피라미드

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                           TEST PYRAMID (테스트 피라미드)                        │
│                                                                                │
│                              ┌─────────┐                                      │
│                              │   E2E   │  10%                                │
│                              │  Tests  │  • 느림, 비용 높음                   │
│                              │         │  • 전체 시스템 검증                  │
│                              └────┬────┘                                      │
│                                   │                                            │
│                         ┌─────────┴─────────┐                                 │
│                         │    Integration    │  20%                            │
│                         │      Tests        │  • API, DB 연동                 │
│                         │                   │  • 중간 속도                     │
│                         └─────────┬─────────┘                                 │
│                                   │                                            │
│                    ┌──────────────┴──────────────┐                            │
│                    │       Unit Tests            │  70%                       │
│                    │   (TDD의 핵심 영역)         │  • 빠름, 격리됨             │
│                    │                             │  • 단일 함수/클래스         │
│                    │   Red-Green-Refactor 대상   │  • Mock 활용                │
│                    └─────────────────────────────┘                            │
│                                                                                │
│   TDD 원칙:                                                                    │
│   ┌─────────────────────────────────────────────────────────────────────┐     │
│   │ 1. 단위 테스트는 TDD로 작성 (Red-Green-Refactor)                     │     │
│   │ 2. 통합 테스트는 핵심 경로만 작성                                     │     │
│   │ 3. E2E 테스트는 사용자 시나리오 중심                                  │     │
│   │ 4. 아래에서 위로 갈수록 실행 시간 증가, 유지비용 증가                  │     │
│   └─────────────────────────────────────────────────────────────────────┘     │
│                                                                                │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 테스트 유형별 TDD 적용

| 테스트 유형 | TDD 적용 | 실행 속도 | Mock 사용 | 커버리지 | 용도 |
|------------|----------|----------|-----------|----------|------|
| **단위 테스트** | 핵심 | ms | 필수 | 80%+ | 로직 검증 |
| **통합 테스트** | 선택적 | 초 | 선택적 | 50%+ | API/DB 연동 |
| **E2E 테스트** | 제한적 | 분 | 없음 | 30%+ | 사용자 시나리오 |
| **계약 테스트** | 선택적 | ms-ms | Mock | 60%+ | API 계약 |
| **성능 테스트** | 아님 | 분-시간 | 없음 | N/A | 부하 검증 |

### 과목 융합 관점 분석

#### 1. 소프트웨어 설계 × TDD 융합
TDD는 **자연스럽게 좋은 설계를 유도**한다. 테스트가 어려운 코드는 설계가 나쁜 코드다. TDD를 하다 보면 자연스럽게 의존성 주입(DI), 인터페이스 분리, 단일 책임 원칙(SRP)이 적용된다.

#### 2. 보안 × 시큐어 코딩 융합
TDD에 보안 테스트를 포함하면 **Security by Design**을 실현한다. SQL 인젝션, XSS, 인증 우회 등에 대한 테스트를 Red-Green-Refactor 사이클에 포함한다.

#### 3. DevOps × CI/CD 융합
TDD로 작성된 테스트는 CI/CD 파이프라인의 **품질 게이트(Quality Gate)** 역할을 한다. 커밋마다 자동 실행되어 결함이 배포되는 것을 방지한다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단: 실무 시나리오 3가지

#### 시나리오 1: 레거시 코드에 TDD 도입
**상황**: 테스트 없는 레거시 시스템에 TDD 도입 난항

**기술사적 의사결정 과정**:
1. **특성 테스트(Characterization Test)**: 기존 동작을 포착하는 테스트 먼저 작성
2. **승인 테스트(Acceptance Test)**: 블랙박스 테스트로 외부 동작 검증
3. **스트랭글러 패턴**: 새 기능은 TDD로, 기존 코드는 점진적
4. **테스트 가능한 설계로 리팩토링**: 의존성 주입, 인터페이스 분리

#### 시나리오 2: TDD와 일정 압박
**상황**: "테스트 작성할 시간에 기능 개발하라"는 압박

**기술사적 의사결정 과정**:
1. **ROI 데이터 제시**: TDD는 디버깅 시간 50-80% 감소
2. **파일럿 프로젝트**: 비교군 실험으로 효과 입증
3. **핵심 로직만 TDD**: 모든 코드가 아닌 리스크 높은 영역 우선
4. **테스트 레거시 방지**: 테스트 없는 코드는 기술 부채로 추적

#### 시나리오 3: 테스트 유지보수 부담
**상황**: 테스트가 너무 많아 유지보수 비용 증가

**기술사적 의사결정 과정**:
1. **테스트 피라미드 준수**: 단위 > 통합 > E2E 비율 유지
2. **중복 테스트 제거**: 동일 검증을 여러 계층에서 수행 방지
3. **테스트 리팩토링**: 테스트 코드도 정기적 정리
4. **공통 픽스처**: Given-When-Then 팩토리로 중복 감소

### 도입 시 고려사항 체크리스트

#### 기술적 고려사항
- [ ] 테스트 프레임워크 선정 (pytest, Jest, JUnit)
- [ ] Mock 라이브러리 학습 (unittest.mock, Mockito)
- [ ] CI/CD 파이프라인에 테스트 자동 실행
- [ ] 코드 커버리지 도구 도입 (Coverage.py, JaCoCo)

#### 운영/보안적 고려사항
- [ ] 팀 TDD 교육 및 연습
- [ ] 테스트 코드 품질 기준 정의
- [ ] 보안 테스트 포함 정책
- [ ] 레거시 코드 TDD 도입 전략

### 주의사항 및 안티패턴

1. **Testing After**: 코드 작성 후 테스트 작성 (TDD가 아님)
2. **Overtesting**: 구현 세부사항까지 테스트 (리팩토링 방해)
3. **Flaky Tests**: 비결정적 테스트 (신뢰도 저하)
4. **Mock Overuse**: 모든 의존성 Mock (통합 문제 미발견)

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | TDD 미적용 | TDD 적용 | 개선율 |
|------|-----------|----------|--------|
| 결함 밀도 | 15/KLOC | 3/KLOC | **80% 감소** |
| 코드 커버리지 | 30% | 90%+ | **200% 향상** |
| 디버깅 시간 | 40% | 10% | **75% 감소** |
| 리팩토링 자신감 | 낮음 | 높음 | 질적 향상 |
| 기술 부채 누적률 | 5%/월 | 1%/월 | **80% 감소** |

### 미래 전망 및 진화 방향

1. **AI 기반 테스트 생성**: LLM이 테스트 코드 자동 작성
2. **Mutation Testing 자동화**: 테스트 품질 자동 검증
3. **Property-Based Testing**: 속성 기반 테스트와 TDD 결합
4. **Contract Testing**: 마이크로서비스 간 계약 테스트 표준화

### ※ 참고 표준/가이드
- **TDD: By Example (Kent Beck, 2002)**: TDD 원전
- **Clean Code (Robert C. Martin)**: TDD와 클린 코드
- **xUnit Test Patterns (Gerard Meszaros)**: 테스트 패턴

---

## 📌 관련 개념 맵 (Knowledge Graph)

1. [XP (Extreme Programming)](./73_xp_extreme_programming.md) - TDD의 방법론적 기반
2. [지속적 통합](./76_continuous_integration.md) - TDD 테스트의 자동 실행
3. [리팩토링](./78_refactoring.md) - TDD의 세 번째 단계
4. [짝 프로그래밍](./74_pair_programming.md) - Ping-Pong 페어링의 기반
5. [단위 테스트](../7_testing/397_unit_test.md) - TDD의 핵심 테스트 유형
6. [BDD (행동 주도 개발)](./126_bdd.md) - TDD의 확장

---

## 👶 어린이를 위한 3줄 비유 설명

**비유: 요리 레시피 개발**

1. **맛부터 정해요**: "이 케이크는 달콤해야 해!"라고 먼저 정해요. 그리고 그걸 확인할 방법을 생각해요 - "한 입 먹어서 설탕이 느껴져야 해!"

2. **최소로 만들어요**: 설탕만 넣어서 만들어요. 맛있어 보이지 않아도 괜찮아요. "달콤한지"만 확인하면 돼요.

3. **예쁘게 만들어요**: 이제 크림도 올리고 딸기도 올려요. 그래도 "달콤한지"는 계속 확인해요. 예쁘게 만들다가 단맛이 사라지면 안 되니까요!
