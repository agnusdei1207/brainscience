+++
weight = 44
title = "044. TDD & BDD — 테스트 주도 개발"
date = "2026-04-05"
[extra]
categories = "studynote-devops-sre"
+++

## 0. 핵심 인사이트

> **핵심**: TDD & BDD — 테스트 주도 개발은(는) DevOps/SRE 문맥에서 반복 실행과 운영 일관성을 높이기 위한 핵심 개념이다.
> **비유**: TDD는 미래의 나에게 편지 먼저 쓰기 — "이 기능은 이렇게 동작해야 해"를 테스트로 먼저 정의하고, 그 편지 내용에 맞는 코드를 만들어가요.

---

> 📝 모범 답안

## 1. 개요 및 필요성

```
TDD (Test-Driven Development):
  Kent Beck 창안, XP(eXtreme Programming) 핵심 실천법

Red-Green-Refactor 사이클:

  1. RED: 실패하는 테스트 작성
     아직 구현이 없으니 당연히 실패
     → 테스트가 요구사항을 정의

  2. GREEN: 최소 코드로 테스트 통과
     통과만 하면 됨, 완벽하지 않아도 OK

  3. REFACTOR: 코드 개선
     테스트는 그린 상태 유지하며 코드 정리
     중복 제거, 가독성 향상

TDD 사이클 예시 (Python):

  def test_add():
      assert add(2, 3) == 5  # add 함수 없음 → 실패

  def add(a, b):
      return a + b  # 테스트 통과

TDD의 3 규칙 (Uncle Bob):
  1. 실패하는 유닛 테스트 없이 프로덕션 코드 작성 금지
  2. 실패를 확인하기에 충분한 테스트만 작성
  3. 현재 실패 테스트를 통과하기에 충분한 코드만 작성

테스트 유형:
  단위 테스트 (Unit): 함수/클래스 개별
  통합 테스트 (Integration): 모듈 간 연동
  E2E 테스트 (End-to-End): 사용자 시나리오 전체

  TDD: 주로 단위 테스트 중심
```

---

## 2. 구성요소

```
BDD (Behavior-Driven Development):
  Dan North, 2003년 제안
  TDD 확장: 비즈니스 행동 중심

문제 의식:
  TDD: "무엇을 테스트해야 하는가?" 불명확
  BDD: 비즈니스 시나리오로 테스트 범위 정의

Gherkin 언어 (자연어 테스트 시나리오):
  Feature: 쇼핑 카트
    Scenario: 상품 추가
      Given 빈 쇼핑 카트가 있다
      When 사용자가 상품 A를 카트에 추가한다
      Then 카트에 상품 A가 1개 있다
      And 카트 합계 금액이 10,000원이다

  Scenario: 재고 없는 상품 추가 시도
      Given 재고가 0인 상품 B가 있다
      When 사용자가 상품 B를 카트에 추가한다
      Then "품절" 오류 메시지가 표시된다

  Given: 사전 조건 (Pre-condition)
  When: 행동 (Action)
  Then: 기대 결과 (Expected Outcome)

BDD 도구:
  Cucumber (Java, Ruby, JavaScript):
    Gherkin 파일 → 자동 테스트 실행

  Behave (Python):
    given, when, then 데코레이터

  SpecFlow (.NET):
    C# 통합

BDD의 가치:
  비개발자(PM, 기획자) 시나리오 작성 가능
  살아있는 문서 (Living Documentation)
  테스트 = 명세 = 문서
```

---

## 3. 구조 및 원리

**핵심 조건**: 공유된 목표, 자동화된 피드백 루프, 측정 가능한 성과 지표가 동시에 작동해야 문화가 실행력으로 전환된다.

동작 순서:
1. 공동 목표를 정의해 개발·운영·보안의 KPI를 고객 가치 중심으로 정렬한다.
2. 작업 흐름을 시각화해 병목과 대기 시간을 식별하고 제거한다.
3. 자동화와 표준화를 도입해 사람 의존 절차를 축소한다.
4. 운영 데이터와 회고 결과를 다시 개발 계획에 반영해 학습 루프를 닫는다.

```text
문제 인식
   ↓
공유 목표·협업 구조
   ↓
자동화 파이프라인
   ↓
측정·피드백
   ↓
지속 개선
```

```
TDD 실천 패턴:

테스트 더블 (Test Double):
  실제 의존성 대신 테스트용 대체물

  Mock: 호출 기대값 설정 + 검증
    mock_repo.find_by_id.return_value = user
    mock_repo.find_by_id.assert_called_once_with(123)

  Stub: 정해진 값만 반환
    stub_repo.find_by_id = lambda id: User(id=id, name="test")

  Spy: 실제 동작 + 호출 기록
  Fake: 간단한 실제 구현 (메모리 DB 등)

Python pytest 예시:
  import pytest
  from unittest.mock import Mock

  class UserService:
      def __init__(self, repo):
          self.repo = repo
      def get_user(self, user_id):
          return self.repo.find_by_id(user_id)

  def test_get_user_returns_user():
      mock_repo = Mock()
      mock_repo.find_by_id.return_value = {"id": 1, "name": "Alice"}
      service = UserService(mock_repo)

      result = service.get_user(1)

      assert result["name"] == "Alice"
      mock_repo.find_by_id.assert_called_once_with(1)

AAA 패턴 (Arrange-Act-Assert):
  Arrange: 테스트 환경 설정
  Act: 테스트 대상 실행
  Assert: 결과 검증

  = Given-When-Then의 코드 버전

테스트 커버리지:
  목표: 80% 이상 (단위 테스트 기준)
  100%는 오히려 과도할 수 있음 (Getter/Setter)

  도구: Istanbul (JS), Coverage.py, JaCoCo (Java)
```

---

## 4. 비교 및 연결

```
TDD/BDD + CI/CD 파이프라인:

완전 자동화 흐름:
  1. 개발자: 로컬에서 TDD 사이클
     Red → Green → Refactor

  2. git push → PR 생성

  3. CI 파이프라인 자동 실행:
     단위 테스트 → 통합 테스트 → E2E 테스트

  4. BDD 시나리오 자동 검증:
     Cucumber: .feature 파일 실행

  5. 테스트 커버리지 리포트 생성

  6. 품질 게이트: 커버리지 < 80% → 머지 차단

  7. 모든 테스트 통과 → 프로덕션 자동 배포

GitHub Actions 예시:
  name: Test
  on: [push, pull_request]
  jobs:
    test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Run tests
          run: pytest --cov=. --cov-fail-under=80
        - name: BDD
          run: behave features/

테스트 피라미드:
       /E2E\          ← 적게 (느림, 비용)
      /통합테스트\     ← 중간
     /단위테스트/      ← 많이 (빠름, 저렴)

  단위 70% + 통합 20% + E2E 10% 권장

TDD 도입 장벽과 극복:
  "시간이 없어요": 테스트 작성 시간 = 디버깅 시간 감소
  "테스트 작성 어려워요": 레거시는 테스트 가능 설계 먼저
  "100% 커버리지 요구": 80%로 시작, 점진적 개선

  XP의 실천: "테스트 없는 코드는 레거시 코드"
```

---

## 5. 실무 적용 및 판단

```
결제 API TDD+BDD 개발:

요구사항:
  POST /payments
  성공: 결제 완료, 주문 상태 업데이트
  실패: 잔액 부족 시 400 오류

BDD 시나리오 (Gherkin):
  Feature: 결제 처리

    Scenario: 정상 결제
      Given 사용자 A가 잔액 50,000원을 보유한다
      And 주문 금액이 30,000원이다
      When 사용자가 결제를 요청한다
      Then 결제가 성공한다
      And 사용자 잔액이 20,000원이 된다
      And 주문 상태가 "결제 완료"로 변경된다

    Scenario: 잔액 부족
      Given 사용자 B가 잔액 10,000원을 보유한다
      And 주문 금액이 30,000원이다
      When 사용자가 결제를 요청한다
      Then 400 오류가 반환된다
      And "잔액 부족" 메시지가 포함된다
      And 주문 상태는 변경되지 않는다

TDD 구현:
  def test_process_payment_success():
      mock_user = Mock(balance=50000)
      mock_order = Mock(amount=30000)

      result = payment_service.process(mock_user, mock_order)

      assert result.success == True
      assert mock_user.balance == 20000

  def test_process_payment_insufficient_balance():
      mock_user = Mock(balance=10000)
      mock_order = Mock(amount=30000)

      with pytest.raises(InsufficientBalanceError):
          payment_service.process(mock_user, mock_order)

결과:
  TDD 비용: 테스트 작성 +30% 시간
  효과:
    프로덕션 버그: 70% 감소
    디버깅 시간: 60% 감소
    리팩토링 안전성: 대폭 향상

  ROI: 6개월 후 개발 속도 20% 향상
  (초기 속도 저하 후 리팩토링 가속)
```

---

## 6. 기대효과 및 결론

TDD & BDD — 테스트 주도 개발을(를) 도입하면 자동화와 표준화를 통해 속도·안정성·가시성의 균형을 높일 수 있다. 다만 효과를 얻으려면 공유된 목표, 자동화된 피드백 루프, 측정 가능한 성과 지표가 동시에 작동해야 문화가 실행력으로 전환된다는 전제가 충족되어야 하며, 도구만 도입하고 운영 원칙을 바꾸지 않으면 기대 효과가 빠르게 한계에 부딪힌다.

결론적으로 TDD & BDD — 테스트 주도 개발은(는) 개별 기능이 아니라 운영 체계 전체의 품질을 재정렬하는 방식이며, 향후에는 플랫폼화·정책화·AI 기반 최적화와 결합해 더 높은 수준의 자동 운영으로 확장된다.

---

## 7. 발전 흐름도

```
[TDD 탄생 (1999)]
Kent Beck: XP 실천법으로 체계화
Red-Green-Refactor 사이클
      |
      v
[BDD 제안 (2003)]
Dan North: TDD + 비즈니스 언어
Gherkin/Cucumber 도구 탄생
      |
      v
[CI/CD 통합 (2010s)]
Jenkins → Travis → GitHub Actions
테스트 자동화 파이프라인 표준화
      |
      v
[테스트 문화 확산 (2015~)]
DevOps 운동과 결합
팀 전체 품질 책임 문화
      |
      v
[현재: AI 테스트 생성]
GitHub Copilot 테스트 코드 생성
AI 기반 엣지 케이스 자동 탐지
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| CALMS | 문화·자동화·측정·공유를 아우르는 DevOps 기본 프레임워크 |
| DORA 메트릭스 | 변화 속도와 안정성을 함께 측정하는 성과 지표 |
| 피드백 루프 | 운영 경험을 개발 계획으로 되돌리는 핵심 메커니즘 |
| 플랫폼 엔지니어링 | 표준화된 셀프서비스로 DevOps 실천을 조직화 |
| 심리적 안전감 | 실패 학습과 무비난 회고를 가능하게 하는 문화 기반 |
