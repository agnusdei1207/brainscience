+++
weight = 434
title = "434. NoSQL Injection"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: NoSQL Injection (NoSQL 인젝션)은 MongoDB, Redis, Elasticsearch 등 비관계형 DB (Database)에서 JSON (JavaScript Object Notation)/BSON 쿼리 구조나 쿼리 연산자를 악용해 인증 우회, 데이터 탈취를 유발하는 공격이다.
> 2. **가치**: "SQL을 안 쓰면 SQL 인젝션이 없다"는 잘못된 인식과 달리, MongoDB의 `$where`, `$regex`, `$gt` 연산자가 새로운 인젝션 공격 벡터가 된다.
> 3. **판단 포인트**: 쿼리 파라미터의 타입 검증(JSON 객체를 문자열로 강제), MongoDB 쿼리 연산자 화이트리스트, 최신 드라이버 사용이 핵심 방어책이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

NoSQL 데이터베이스는 SQL을 사용하지 않지만, 사용자 입력을 쿼리에 직접 포함하면 동일한 인젝션 위험에 노출된다. 특히 MongoDB에서 HTTP 요청 바디의 JSON이 쿼리 객체로 직접 변환될 때 공격자가 쿼리 연산자(`$gt`, `$ne`, `$where`, `$regex`)를 주입할 수 있다.

**MongoDB 인젝션 예시**:
```javascript
// 취약한 로그인 코드 (Node.js)
db.users.find({ username: req.body.username, password: req.body.password })

// 공격 입력 (JSON): {"username": "admin", "password": {"$gt": ""}}
// 실행 쿼리: {username: "admin", password: {$gt: ""}}
// password 값이 빈 문자열보다 크면 → 모든 비밀번호 통과 → 인증 우회
```

이 공격은 비밀번호를 모르고도 `$gt`, `$ne`, `$regex` 등으로 조건을 항상 참으로 만들어 인증을 우회한다.

📢 **섹션 요약 비유**: SQL 인젝션이 레스토랑 주문서에 명령을 쓰는 것이라면, NoSQL 인젝션은 주문 앱의 JSON 필드에 "가격이 0보다 크면"이라는 조건을 몰래 삽입하는 것이다.

---

## 2. 구성요소

MongoDB 주요 인젝션 연산자:

| 연산자 | 의미 | 공격 예시 |
|:---|:---|:---|
| `$gt` | 초과 | `{"password": {"$gt": ""}}` — 항상 참 |
| `$ne` | 불일치 | `{"username": {"$ne": null}}` — 모든 사용자 |
| `$where` | JS 표현식 | `{"$where": "sleep(5000)"}` — 시간 기반 공격 |
| `$regex` | 정규식 | `{"password": {"$regex": ".*"}}` — 항상 참 |

```
┌──────────────────────────────────────────────────────────┐
│           NoSQL 인젝션 공격 흐름                         │
├──────────────────────────────────────────────────────────┤
│  HTTP 요청:                                              │
│  POST /login                                             │
│  {"username":"admin", "password":{"$gt":""}}             │
│       │                                                  │
│       ▼                                                  │
│  MongoDB 쿼리: find({username:"admin",                   │
│                       password:{$gt:""}})                │
│       │                                                  │
│       ▼                                                  │
│  비밀번호 조건 항상 참 → 인증 우회 성공                  │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: NoSQL 인젝션은 "비밀번호가 뭐든 상관없이, 뭔가 있으면 통과"라는 새 규칙을 쿼리에 몰래 집어넣는 것이다.

---

## 3. 구조 및 동작 원리

| 구분 | SQL 인젝션 | NoSQL 인젝션 |
|:---|:---|:---|
| 대상 | 관계형 DB | MongoDB, Redis 등 |
| 공격 문자 | `'`, `;`, `--` | `{$gt:`, `$where` 등 |
| 인증 우회 | `' OR 1=1--` | `{"password": {"$gt": ""}}` |
| 방어 | 파라미터화 쿼리 | 타입 검증, 연산자 화이트리스트 |

📢 **섹션 요약 비유**: SQL은 구두 주문을 조작하고, NoSQL은 앱 주문 양식의 필드 타입을 바꿔 시스템을 속인다.

---

## 4. 비교 및 트레이드오프

**대응 전략**:
1. **타입 강제 검증**: 비밀번호 필드는 반드시 string 타입만 허용, 객체 수신 시 거부
2. **쿼리 연산자 화이트리스트**: 허용되지 않은 MongoDB 연산자 포함 시 요청 거부
3. **`$where` 연산자 비활성화**: 서버에서 JavaScript 실행 기능 비활성화
4. **ODM (Object Document Mapping) 사용**: Mongoose 등으로 스키마 타입 강제
5. **최소 권한**: DB 계정에 애플리케이션에 필요한 최소 읽기/쓰기 권한만 부여

```javascript
// 안전한 코드: 타입 검증 추가
const username = String(req.body.username);
const password = String(req.body.password);
db.users.find({ username: username, password: password });
```

📢 **섹션 요약 비유**: 타입 검증은 "주문서에 음식 이름만 적을 수 있고, 코드나 명령은 적을 수 없다"는 규칙을 적용하는 것이다.

---

## 5. 실무 적용 및 최적화 기법

타입 강제 검증과 ODM 스키마를 활용하면 NoSQL 인젝션을 구조적으로 방어할 수 있다. 특히 Express.js 환경에서 `express-validator`와 Mongoose를 조합하면 입력 타입 검증과 쿼리 안전성을 동시에 확보할 수 있다.

기술사 관점에서 NoSQL 인젝션은 데이터 타입 혼용이라는 JavaScript의 동적 타입 특성에서 비롯된다. 이를 인식하고 정적 타입 검사(TypeScript)와 입력 검증 라이브러리를 병행 사용하는 아키텍처가 필요하다.

📢 **섹션 요약 비유**: NoSQL 인젝션 방어는 주문 양식에서 "음식 이름" 칸에는 문자만, "수량" 칸에는 숫자만 입력받도록 강제하는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| $gt/$ne/$where | 공격 연산자 | MongoDB 쿼리 연산자 악용 |
| Mongoose ODM | 방어 도구 | 스키마 타입 강제 |
| Type Coercion | 취약 원인 | JavaScript 동적 타입 |
| Input Sanitization | 방어 방법 | 타입·형식 강제 검증 |
| SQL Injection | 유사 공격 | 관계형 DB 인젝션 |

### 👶 어린이를 위한 3줄 비유 설명
- NoSQL 인젝션은 SQL을 안 써도 비슷한 방식으로 DB를 속이는 공격이야.
- MongoDB 같은 DB는 JSON 형식으로 질문하는데, "비밀번호가 뭐든 상관없어"라는 조건을 몰래 넣을 수 있어.
- 그래서 사용자 입력이 항상 문자(string)인지 확인하고, 다른 타입이 들어오면 거부해야 해!
