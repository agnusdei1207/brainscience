+++
weight = 13
title = "13. TDD & BDD"
date = "2026-05-17"
[extra]
categories = "gisulsa-sw-engineering"
+++

# 🎯 TDD (테스트 주도 개발) & BDD (행위 주도 개발)

> **별점**: ★★★★☆ | 기본 필수

## 1. TDD (Test Driven Development)

```
[Red-Green-Refactor 사이클]
① Red: 실패하는 테스트 작성 (코드 없음)
② Green: 테스트를 통과하는 최소 코드 작성
③ Refactor: 코드 개선 (테스트는 통과 유지)

원칙:
- 실패 테스트 없이는 운영 코드 금지
- 컴파일 에러도 하나씩 해결
- 리팩토링은 모든 테스트 통과 후

효과:
- 설계 개선 (테스트 가능성 = 좋은 설계)
- 회귀 방지 (자동화된 회귀 테스트)
- 문서화 (테스트 = 살아있는 명세)
```

## 2. BDD (Behavior Driven Development)

```
Given-When-Then 시나리오:
"주문 시나리오"
Given: 사용자가 로그인되어 있고 상품이 재고에 있을 때
When: 사용자가 상품을 장바구니에 담고 결제하면
Then: 주문이 생성되고 재고가 감소해야 한다

도구: Cucumber (Java), Behave (Python), SpecFlow (.NET)
효과: 비기술 이해관계자도 시나리오 검토 가능
```

## 3. 비교

| 항목 | TDD | BDD |
|------|-----|-----|
| 관점 | 개발자 | 비즈니스/사용자 |
| 언어 | 코드 | 자연어(Given-When-Then) |
| 협업 | 개발 팀 내 | 개발+비즈니스 전체 |
| 도구 | JUnit, pytest | Cucumber, Behave |

## 4. 답안 포인트

**3단락**: ① TDD 사이클 & 원칙 → ② BDD 시나리오 작성 방법 → ③ Agile/CI에서 TDD/BDD 실천 효과

## 5. 관련 개념

`뮤테이션테스팅(★133회)` → TDD 테스트 품질 검증 | `CI/CD` → 자동화 테스트 파이프라인 | `MSA` → 서비스별 독립 테스트
