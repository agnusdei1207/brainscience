+++
weight = 430
title = "430. Error-based SQL Injection"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: Error-based SQL Injection (에러 기반 SQL 인젝션)은 DB (Database) 에러 메시지에 데이터를 포함시켜 반환하게 하는 공격으로, 에러 메시지를 그대로 사용자에게 노출하는 취약한 애플리케이션에서 유효하다.
> 2. **가치**: 에러 메시지에서 DB 유형, 버전, 테이블 구조, 심지어 데이터 값까지 추출할 수 있어 공격 속도와 정보 획득량이 Blind 방식보다 빠르다.
> 3. **판단 포인트**: `extractvalue()`, `updatexml()`, `floor()` 등 MySQL 전용 함수와 MS SQL의 `convert()` 에러를 이용한 공격이 대표적이며, 에러 메시지 숨김이 핵심 방어다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

에러 기반 인젝션은 의도적으로 DB에서 에러를 발생시키고, 그 에러 메시지 안에 원하는 데이터를 포함시키는 기법이다. DB가 에러 발생 시 실행 중이던 쿼리나 함수 인수를 에러 메시지에 포함해 반환하는 특성을 악용한다.

MySQL (My Structured Query Language) Error-based 대표 기법:
```sql
-- extractvalue() 악용: XPath 에러에 데이터 포함
' AND extractvalue(1, concat(0x7e, (SELECT version())))--
-- 에러 메시지: XPATH syntax error: '~8.0.26' (버전 노출)

-- updatexml() 악용
' AND updatexml(1, concat(0x7e, (SELECT user())), 1)--
-- 에러 메시지: XPATH syntax error: '~root@localhost'
```

이 기법이 위험한 이유는 에러 메시지만 확인하면 DB의 모든 정보를 순서대로 추출할 수 있기 때문이다.

📢 **섹션 요약 비유**: DB가 에러가 날 때 "지금 이런 걸 처리하다가 실패했어요"라고 상세히 알려주면, 공격자는 그 설명에서 비밀 정보를 꺼낸다.

---

## 2. 구성요소

Error-based 인젝션 주요 기법:

| DB 유형 | 기법 | 특징 |
|:---|:---|:---|
| MySQL | `extractvalue()`, `updatexml()` | XPath 에러에 데이터 포함 |
| MySQL | `floor(rand(0)*2)` GROUP BY | 중복 에러로 데이터 노출 |
| MS SQL | `CONVERT(int, user)` | 타입 변환 에러 |
| Oracle | `ctxsys.drithsx.sn()` | 패키지 에러 |
| PostgreSQL | CAST 에러 | 타입 오류 |

```
┌──────────────────────────────────────────────────────────┐
│           Error-based SQLi 데이터 추출 흐름              │
├──────────────────────────────────────────────────────────┤
│  공격자 입력: ' AND extractvalue(1,                      │
│             concat(0x7e,(SELECT pw FROM admin)))--       │
│       │                                                  │
│       ▼                                                  │
│  DB 에러 발생                                            │
│  에러 메시지: XPATH syntax error: '~P@ssw0rd!'           │
│       │                                                  │
│       ▼                                                  │
│  공격자: 에러 메시지에서 비밀번호 추출 성공              │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: DB가 에러 설명서에 "이 비밀번호를 처리하다 실패함: P@ssw0rd!"라고 적어 돌려주는 것과 같다.

---

## 3. 구조 및 동작 원리

| 구분 | Error-based | Boolean Blind | Time-based |
|:---|:---|:---|:---|
| 출력 필요 여부 | 에러 메시지 필요 | 참/거짓 차이 필요 | 응답 시간 차이 |
| 공격 속도 | 빠름 | 느림 | 가장 느림 |
| 방어 | 에러 메시지 숨김 | 응답 균일화 | SLEEP 함수 제한 |

📢 **섹션 요약 비유**: Error-based는 잡힌 사람이 실수로 비밀을 말하는 것이고, Blind는 침묵하는 사람에게서 예/아니오만 뽑아내는 것이다.

---

## 4. 비교 및 트레이드오프

**핵심 방어책**:
1. **에러 메시지 일반화**: DB 에러를 "오류가 발생했습니다"로 교체, 스택 트레이스 숨김
2. **커스텀 에러 페이지**: 500 에러 전용 페이지 설정
3. **로깅 분리**: 에러 상세 정보는 서버 로그에만 기록
4. **파라미터화 쿼리**: 근본 해결책 — SQL 구조를 변경하는 입력 자체를 방지

```python
# 취약한 패턴 (에러 노출)
try:
    cursor.execute("SELECT * FROM users WHERE id=" + uid)
except Exception as e:
    return str(e)   # DB 에러 메시지 직접 반환

# 안전한 패턴 (에러 숨김 + 파라미터화)
try:
    cursor.execute("SELECT * FROM users WHERE id=%s", (uid,))
except Exception:
    return "처리 중 오류가 발생했습니다."
```

📢 **섹션 요약 비유**: 에러 메시지 숨김은 "지금 어떤 작업을 했다가 실패했는지"를 공격자에게 알려주지 않는 것이다.

---

## 5. 실무 적용 및 최적화 기법

에러 메시지 일반화만으로 Error-based SQLi를 완전 차단할 수 있다. 그러나 이것은 공격을 "더 어렵게" 만드는 것이지, 취약점 자체를 제거하는 것이 아니다. 파라미터화 쿼리 적용이 근본 해결책이며, 에러 메시지 숨김은 그에 더해지는 심층 방어 레이어다.

📢 **섹션 요약 비유**: 에러 메시지 숨김은 비밀 창고 지도를 찢어버리는 것이다. 창고 자물쇠(파라미터화)는 여전히 필요하다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| extractvalue() | 공격 함수 | MySQL XPath 에러 유발 |
| updatexml() | 공격 함수 | MySQL XML 에러 유발 |
| Custom Error Page | 방어 | DB 에러 노출 차단 |
| Parameterized Query | 근본 방어 | SQL 구조 변경 방지 |
| WAF | 보완 방어 | 알려진 패턴 차단 |

### 👶 어린이를 위한 3줄 비유 설명
- Error-based SQLi는 컴퓨터가 실수를 설명하다가 비밀을 말해버리는 것이야.
- "이 비밀번호를 처리하다 실패했어요: admin123"처럼 에러 메시지에 비밀이 새어나와.
- 그래서 에러가 나면 "오류가 발생했습니다"라고만 말하고 자세한 내용은 숨겨야 해!
