+++
title = "499. SQL 인젝션 방어 - Prepared Statement, ORM"
date = 2026-04-21
weight = 499
description = "Prepared Statement와 ORM 프레임워크로 SQL 인젝션을 방어하는 방법"
taxonomy = ""
tags = ["Software Engineering", "Security", "SQL Injection", "Prepared Statement", "ORM"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: SQL Injection은 쿼리와 데이터를 분리하면 크게 줄일 수 있다.
> 2. **가치**: Prepared Statement (파라미터화된 쿼리)가 핵심 방어다.
> 3. **판단 포인트**: ORM (Object-Relational Mapping)도 안전하게 써야 한다.

---

## Ⅰ. 개요 및 필요성

SQL Injection은 입력이 SQL 문법으로 해석될 때 발생한다. 가장 기본적인 방어는 파라미터 분리다.

Prepared Statement와 ORM은 많이 쓰이지만, 사용법이 잘못되면 여전히 위험하다.

- **📢 섹션 요약 비유**: 메모 내용과 봉투 주소를 따로 써야 하는 것과 같다.

---

## Ⅱ. 아키텍처 및 핵심 원리

Prepared Statement는 쿼리 템플릿과 값 바인딩을 분리한다.

```text
SQL 템플릿 + 파라미터 -> DB 실행
```

| 방법 | 의미 |
|:---|:---|
| Prepared Statement | 값 분리 |
| Parameter Binding | 안전한 전달 |
| ORM | 추상화된 DB 접근 |

- **📢 섹션 요약 비유**: 요리법과 재료를 따로 준비하면 실수가 줄어든다.

---

## Ⅲ. 비교 및 연결

ORM은 SQL을 직접 쓰지 않게 도와주지만, 동적 쿼리 문자열을 만들면 여전히 위험하다.

| 구분 | 안전한 방식 | 위험한 방식 |
|:---|:---|:---|
| SQL | 바인딩 변수 | 문자열 결합 |
| ORM | 파라미터 사용 | raw query 남용 |
| 검증 | 입력 제한 | 신뢰 |

Input Validation과 함께 적용해야 효과가 크다.

- **📢 섹션 요약 비유**: 자동문이 있어도 옆문을 열어 두면 소용이 없다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 검색, 로그인, 필터링, 관리자 기능에서 특히 주의한다.

점검 포인트는 다음과 같다.
1. 문자열 연결로 SQL을 만들지 않는가?
2. ORM의 raw query를 제한하는가?
3. 예외 메시지에 쿼리 정보가 노출되지 않는가?

- **📢 섹션 요약 비유**: 레시피는 읽되, 재료를 마음대로 문장으로 바꾸면 안 된다.

---

## Ⅴ. 기대효과 및 결론

Prepared Statement와 ORM의 올바른 사용은 SQL Injection 방어의 핵심이다.

결론적으로 이 항목은 "SQL과 데이터를 분리하는 방어"다.

- **📢 섹션 요약 비유**: 주문서와 메뉴판을 섞지 않으면 식당이 안전해진다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Prepared Statement | 핵심 방어 |
| ORM | 추상화 도구 |
| Input Validation | 보완 방어 |

### 👶 어린이를 위한 3줄 비유 설명

1. SQL과 숫자, 문자를 따로 넣어야 해요.
2. 문장처럼 붙이면 위험해요.
3. 그러면 나쁜 명령이 못 들어와요.

