+++
weight = 433
title = "433. ORM Injection"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: ORM (Object-Relational Mapping) Injection은 ORM 프레임워크를 사용하더라도 동적 쿼리 생성, Raw 쿼리 사용, 안전하지 않은 파라미터 바인딩으로 인해 SQL 인젝션이 발생하는 취약점이다.
> 2. **가치**: "ORM을 쓰면 SQL 인젝션이 없다"는 잘못된 통념을 깨트리며, Hibernate HQL (Hibernate Query Language), JPA JPQL, Django ORM, SQLAlchemy 등 모든 ORM이 잘못 사용되면 취약하다.
> 3. **판단 포인트**: ORM의 파라미터 바인딩 API를 올바르게 사용하고, 불가피한 Raw 쿼리는 반드시 파라미터화해야 하며, HQL/JPQL 인젝션도 SQL 인젝션과 동일한 위험도로 처리해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

ORM은 SQL을 직접 작성하지 않고 객체 지향적 방식으로 DB를 조작해 SQL 인젝션을 방지한다고 알려져 있다. 하지만 이것은 ORM이 올바르게 사용될 때만 성립한다. 개발자가 동적 쿼리 필요성, 성능 최적화, 복잡한 조인 등을 위해 ORM의 Raw 쿼리 기능이나 문자열 연결을 사용하면 취약점이 생긴다.

**Hibernate HQL 인젝션 예시 (Java)**:
```java
// 취약한 코드: 문자열 연결로 HQL 구성
String hql = "FROM User WHERE name = '" + userName + "'";
Query query = session.createQuery(hql);

// 공격 입력: admin' OR '1'='1
// 실행 HQL: FROM User WHERE name = 'admin' OR '1'='1'
// → 전체 사용자 반환
```

**안전한 코드**:
```java
String hql = "FROM User WHERE name = :name";
Query query = session.createQuery(hql);
query.setParameter("name", userName);
```

📢 **섹션 요약 비유**: ORM은 안전한 자동 번역기지만, 번역기를 우회해 원문을 직접 삽입하면 번역기의 보호를 받을 수 없다.

---

## 2. 구성요소

| ORM 프레임워크 | 취약 패턴 | 안전 패턴 |
|:---|:---|:---|
| Hibernate | `createQuery("FROM U WHERE name='"+name+"'")` | `:name` 파라미터 바인딩 |
| JPA/JPQL | 문자열 연결 | `setParameter()` 사용 |
| Django ORM | `raw(f"SELECT * WHERE name='{name}'")` | `filter(name=name)` |
| SQLAlchemy | `text("WHERE name='" + name + "'")` | `text(":name")` + params |

```
┌──────────────────────────────────────────────────────────┐
│           ORM 인젝션 발생 경로                           │
├──────────────────────────────────────────────────────────┤
│  ORM 안전 경로: User.objects.filter(name=input)          │
│  → 자동 파라미터화 → SQL 인젝션 불가                    │
│                                                          │
│  ORM 취약 경로: User.objects.raw(f"WHERE name={input}")  │
│  → 직접 SQL 삽입 → SQL 인젝션 가능                      │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: ORM의 안전한 API는 마치 공항 출국장의 자동 검색대다. 그런데 검색대를 우회하는 VIP 통로(Raw 쿼리)를 아무나 사용하게 두면 의미가 없다.

---

## 3. 구조 및 동작 원리

| 구분 | 일반 SQL 인젝션 | ORM 인젝션 |
|:---|:---|:---|
| 발생 조건 | 모든 SQL 직접 사용 환경 | ORM Raw 쿼리/문자열 연결 사용 시 |
| 위험도 | 동일 | 동일 |
| 탐지 | SAST로 탐지 가능 | ORM 전용 룰 필요 |
| 방어 | Prepared Statement | ORM 파라미터 바인딩 API |

📢 **섹션 요약 비유**: ORM을 쓴다고 자동으로 안전한 것이 아니라, ORM의 안전한 함수를 올바르게 쓸 때 안전해진다.

---

## 4. 비교 및 트레이드오프

**대응 전략**:
1. **ORM 기본 API 우선 사용**: filter(), get(), annotate() 등 ORM 내장 메서드 활용
2. **Raw 쿼리 사용 시 파라미터화 강제**: 코드 리뷰에서 Raw/execute 사용을 반드시 검토
3. **SAST 룰 추가**: 문자열 연결 HQL/JPQL 패턴 탐지 룰 설정
4. **최소 권한**: ORM이 사용하는 DB 계정에 최소 권한만 부여
5. **Lint 규칙**: ORM 안전 API 사용을 강제하는 커스텀 룰 추가

📢 **섹션 요약 비유**: ORM 코드 리뷰는 자동 검색대를 우회하는 통로가 생기지 않았는지 감시하는 것이다.

---

## 5. 실무 적용 및 최적화 기법

ORM의 표준 API를 올바르게 사용하고 Raw 쿼리를 금지 또는 엄격히 통제하면 ORM Injection을 방어할 수 있다. 팀 전체에 "ORM = 자동 안전"이 아니라 "올바른 ORM 사용 = 안전"이라는 인식을 정착시키는 것이 중요하다.

📢 **섹션 요약 비유**: ORM은 안전한 칼을 제공하지만, 칼을 거꾸로 들면 여전히 다친다. 도구가 안전한 것이지 사용법이 안전한 것이 아니다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| HQL/JPQL | 공격 대상 | Hibernate/JPA 쿼리 언어 |
| Parameterized Binding | 방어 방법 | `:name` 바인딩 사용 |
| Raw Query | 취약 패턴 | ORM 우회 SQL 직접 실행 |
| SAST | 탐지 도구 | 취약 패턴 코드 레벨 분석 |
| Django filter() | 안전 API | 자동 이스케이프 제공 |

### 👶 어린이를 위한 3줄 비유 설명
- ORM은 위험한 SQL을 대신 써주는 안전한 번역기야.
- 근데 번역기를 안 쓰고 직접 위험한 SQL을 넣으면 번역기가 도와줄 수 없어.
- 그래서 ORM을 쓸 때도 항상 정해진 안전한 방법만 사용해야 해!
