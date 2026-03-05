+++
title = "053. 파서 (Parser)"
date = "2026-03-05"
weight = 53
[extra]
categories = "studynotes-database"
tags = ["database", "parser", "sql", "syntax-analysis", "parse-tree"]
+++

# 053. 파서 (Parser)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 파서는 SQL 문을 구문 분석하여 파스 트리(Parse Tree)를 생성하는 모듈로, 문법 오류를 감지하고 의미 분석의 입력을 제공한다.
> 2. **가치**: SQL 문법 검증, 키워드 식별, 구조 분해를 통해 옵티마이저가 이해할 수 있는 내부 표현으로 변환한다.
> 3. **융합**: 파서는 옵티마이저, 실행 엔진 앞단에 위치하며, Prepared Statement의 파싱 결과 캐싱으로 성능을 최적화한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의
**파서(Parser)**는 SQL 문을 토큰 단위로 분해하고, 문법 규칙에 따라 구조화된 파스 트리(Parse Tree)를 생성하는 컴파일러 모듈이다. SQL의 구문적 정확성을 검증한다.

### 💡 비유
파서를 **문법 검사기**에 비유할 수 있다:
- "나는 학교에 갔다" → 올바른 문장 ✓
- "나는 학교 갔다를" → 잘못된 문장 ✗

### 처리 단계
```text
SQL: SELECT name FROM users WHERE id = 1

    ↓ [Lexer/Tokenizer]

Tokens: SELECT, name, FROM, users, WHERE, id, =, 1

    ↓ [Parser]

Parse Tree:
       SELECT
      /      \
   name     FROM
             /    \
          users   WHERE
                  /     \
                id       =
                        /   \
                       =     1
```

---

## Ⅱ. 아키텍처 및 핵심 원리
### 1. 파싱 파이프라인
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SQL PARSING PIPELINE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   SQL String                                                                │
│   "SELECT name FROM users WHERE id = 1"                                    │
│      │                                                                       │
│      ▼                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │  LEXER (Tokenizer, Scanner)                                        │  │
│   │  • 문자열을 토큰으로 분해                                            │  │
│   │  • 키워드, 식별자, 리터럴 분류                                       │  │
│   │                                                                     │  │
│   │  Tokens: [SELECT][name][FROM][users][WHERE][id][=][1]              │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│      │                                                                       │
│      ▼                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │  PARSER (Syntax Analyzer)                                          │  │
│   │  • 문법 규칙 적용                                                    │  │
│   │  • 파스 트리 생성                                                    │  │
│   │  • 구문 오류 감지                                                    │  │
│   │                                                                     │  │
│   │  Parse Tree / AST                                                    │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│      │                                                                       │
│      ▼                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │  SEMANTIC ANALYZER                                                  │  │
│   │  • 테이블/컬럼 존재 확인                                              │  │
│   │  • 타입 검사                                                         │  │
│   │  • 권한 검사                                                         │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2. 토큰 유형
| 토큰 유형 | 예시 |
|:---|:---|
| **키워드** | SELECT, FROM, WHERE, JOIN |
| **식별자** | table_name, column_name |
| **리터럴** | 123, 'string', NULL |
| **연산자** | =, <>, AND, OR |
| **구분자** | (, ), ,, ; |

---

## Ⅲ. 융합 비교 및 다각도 분석
### 1. Hard Parse vs Soft Parse
| 구분 | Hard Parse | Soft Parse |
|:---|:---|:---|
| **설명** | 전체 파싱 수행 | 캐시된 파싱 결과 재사용 |
| **비용** | 높음 | 낮음 |
| **발생 시점** | 첫 실행 | 동일 SQL 재실행 |
| **해결책** | 바인드 변수 사용 | - |

### 2. Prepared Statement
```sql
-- Hard Parse (매번 파싱)
SELECT * FROM users WHERE id = 1;
SELECT * FROM users WHERE id = 2;

-- Soft Parse (파싱 1회)
PREPARE stmt FROM 'SELECT * FROM users WHERE id = ?';
EXECUTE stmt USING 1;
EXECUTE stmt USING 2;
```

---

## Ⅳ. 실무 적용
### 성능 최적화
```java
// JDBC Prepared Statement
PreparedStatement pstmt = conn.prepareStatement(
    "SELECT * FROM users WHERE id = ?"
);
pstmt.setInt(1, 100);  // 파싱 없이 바인드만 교체
ResultSet rs = pstmt.executeQuery();
```

---

## 📌 관련 개념 맵
- [[052_옵티마이저]](./52_optimizer.md): 파싱 후 최적화
- [[190_바인드_변수]](./190_bind_variable.md): 파싱 최적화
- [[131_SQL_표준]](../2_sql/131_sql_standard.md): SQL 문법

---

## 👶 어린이를 위한 3줄 비유
1. **문법 검사**: 영어 문장이 문법에 맞는지 확인하는 것과 같아요. "I am a boy"는 맞지만 "I am boy a"는 틀렸죠!

2. **단어 분리**: 문장을 단어별로 쪼개서 뜻을 파악해요. "사과가 먹고 싶다" → "사과가", "먹고", "싶다"로 나누는 거예요.

3. **암기 vs 이해**: 처음 보는 문장은 꼼꼼히 읽지만(하드 파스), 두 번째는 기억나서 빨리 읽죠(소프트 파스).
