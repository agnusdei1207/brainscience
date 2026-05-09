+++
weight = 318
title = "318. SQL 인젝션 동적 바인딩 파서 방화벽 설계 (SQL Injection Defense)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: SQL Injection (SQL 인젝션)은 사용자 입력이 SQL 구문으로 해석될 때 발생하며, PreparedStatement (파라미터 바인딩)가 가장 효과적인 근본 방어다.
> 2. **가치**: Parameterized Query는 입력값을 절대 SQL 코드로 해석하지 않아 공격을 원천 차단하고, WAF (Web Application Firewall)는 알려진 패턴의 2차 방어선을 형성한다.
> 3. **판단 포인트**: 방어 심층 구조(Defense in Depth)는 앱 레벨(바인딩), WAF(웹 방화벽), DB 방화벽(화이트리스트), 최소 권한 원칙(Least Privilege) 4계층을 모두 갖춰야 한다.

## Ⅰ. 개요 및 필요성

SQL Injection은 OWASP (Open Web Application Security Project) Top 10 목록에서 2021년 기준 3위를 기록한 가장 오래되고 치명적인 웹 취약점이다.

기본 공격 예시:
```sql
-- 정상 쿼리
SELECT * FROM users WHERE username = 'alice' AND password = 'secret';

-- 공격 입력: username = "admin'--"
SELECT * FROM users WHERE username = 'admin'--' AND password = '...';
-- → 주석(--) 이후 무시, admin으로 인증 우회
```

공격 유형:
- Classic (고전): WHERE 1=1로 전체 데이터 추출
- Blind (블라인드): 참/거짓으로 데이터 비트 추론
- Time-based: SLEEP(5)로 조건 참/거짓 판별
- Out-of-band: DNS 쿼리로 데이터 외부 전송

피해 범위: 전체 DB 탈취, 인증 우회, 관리자 권한 획득, 데이터 삭제

📢 **섹션 요약 비유**: SQL Injection은 주문서에 "모든 음식 무료 제공"이라고 적어 넣는 것이다. 주방이 주문서를 검증 없이 그대로 처리하면 피해가 발생한다.

## Ⅱ. 아키텍처 및 핵심 원리

### PreparedStatement (파라미터 바인딩) 원리

```java
// 취약한 코드 (동적 쿼리 - SQL Injection 가능)
String query = "SELECT * FROM users WHERE id = " + userId; // 위험!

// 안전한 코드 (PreparedStatement - SQL Injection 불가)
PreparedStatement stmt = conn.prepareStatement(
    "SELECT * FROM users WHERE id = ?"
);
stmt.setString(1, userId); // userId가 SQL 코드가 아닌 데이터로만 처리
```

바인딩 메커니즘:
1. SQL 구문을 먼저 DB 서버에서 파싱·컴파일
2. 파라미터는 데이터로만 전달 (코드 실행 불가)
3. `admin'--` 입력 시 그냥 문자열 `admin'--` 로만 취급

### ORM 파라미터화

```python
# Django ORM - 자동 파라미터화
User.objects.filter(username=request.GET['username'])

# SQLAlchemy (Raw SQL도 안전하게)
session.execute(
    text("SELECT * FROM users WHERE id = :user_id"),
    {"user_id": user_id}
)
```

### ASCII 다이어그램: Defense-in-Depth 계층

```
  사용자 요청
       │
       ▼
  ┌────────────────────────────────────────────────────────┐
  │  Layer 1: 입력 유효성 검사 (Input Validation)           │
  │  - 허용 문자 화이트리스트 (영숫자, 특수문자 제한)          │
  │  - 길이 제한, 타입 검사                                 │
  └────────────────────────────┬───────────────────────────┘
                               ▼
  ┌────────────────────────────────────────────────────────┐
  │  Layer 2: WAF (Web Application Firewall)               │
  │  - SQL 키워드 패턴 탐지 (UNION, SELECT, DROP 등)        │
  │  - 알려진 공격 시그니처 차단                            │
  │  - Mod_Security, AWS WAF, Cloudflare                   │
  └────────────────────────────┬───────────────────────────┘
                               ▼
  ┌────────────────────────────────────────────────────────┐
  │  Layer 3: 앱 레벨 (PreparedStatement / ORM)            │
  │  - 파라미터 바인딩으로 SQL 인젝션 원천 차단 ✅ (핵심)   │
  │  - 동적 쿼리 금지, 저장 프로시저 활용                  │
  └────────────────────────────┬───────────────────────────┘
                               ▼
  ┌────────────────────────────────────────────────────────┐
  │  Layer 4: DB 방화벽 + 최소 권한                        │
  │  - DB 방화벽: 쿼리 화이트리스트 (Imperva, McAfee DAM)  │
  │  - App 계정: SELECT/INSERT/UPDATE 권한만, DROP 불가     │
  │  - 민감 테이블 조회 시도 알람                          │
  └────────────────────────────────────────────────────────┘
```

### 공격 유형별 방어 매핑

| 공격 유형 | 방어 방법 |
|:---|:---|
| Classic Injection | PreparedStatement (바인딩) |
| Blind Injection | 에러 메시지 숨김, 응답 시간 표준화 |
| Time-based | DB 쿼리 타임아웃 설정 (<5초) |
| Second-order | 저장 시에도 바인딩, 조회 시 재이스케이프 |
| Stored Procedure | SP 내부에서도 동적 SQL 금지 |

📢 **섹션 요약 비유**: PreparedStatement는 주문서 양식을 미리 인쇄해두는 것이다. 손님이 어떤 내용을 적어도 미리 정해진 칸에만 들어가고, 주방 지시문을 수정할 수 없다.

## Ⅲ. 비교 및 연결

### WAF vs DB 방화벽

| 항목 | WAF | DB 방화벽 |
|:---|:---|:---|
| 위치 | 웹 서버 앞 | DB 서버 앞 |
| 분석 대상 | HTTP 요청 페이로드 | SQL 쿼리 |
| 탐지 방법 | 패턴 매칭 시그니처 | 쿼리 화이트리스트 |
| 우회 가능성 | 인코딩 우회 가능 | 쿼리 레벨 정밀 |
| 대표 제품 | AWS WAF, Cloudflare, ModSecurity | Imperva SecureSphere, McAfee DAM |

📢 **섹션 요약 비유**: WAF는 건물 입구 보안 요원, DB 방화벽은 금고실 앞 전담 경비원이다. 입구를 통과했더라도 금고실은 따로 검사한다.

## Ⅳ. 실무 적용 및 기술사 판단

### SQL Injection 방어 체크리스트

- [ ] 모든 DB 쿼리에 PreparedStatement / ORM 파라미터화 적용
- [ ] 에러 메시지에 DB 정보 미포함 (테이블명, 스키마 노출 금지)
- [ ] App DB 계정: 최소 권한 원칙 (DROP, TRUNCATE 권한 제거)
- [ ] WAF 규칙 설정 및 주기적 업데이트
- [ ] 정기 침투 테스트 (분기 1회, sqlmap 등 자동화 도구 활용)

### 안티패턴

| 안티패턴 | 문제 | 해결 방법 |
|:---|:---|:---|
| 동적 쿼리 문자열 연결 | SQL Injection 직접 노출 | PreparedStatement 필수 |
| WAF만 믿고 바인딩 미적용 | 인코딩 우회 시 방어 없음 | 다중 계층 방어 |
| SA/root 권한으로 앱 실행 | 공격 성공 시 전체 DB 삭제 가능 | 최소 권한 계정 사용 |

📢 **섹션 요약 비유**: WAF만 믿는 건 현관 잠금장치만 믿고 창문은 열어두는 것이다. 다중 방어선이 필수다.

## Ⅴ. 기대효과 및 결론

| 항목 | 미방어 | 방어 후 |
|:---|:---|:---|
| SQL Injection 성공률 | 취약 코드 100% 공격 가능 | PreparedStatement = 0% |
| 데이터 유출 피해 | 전체 DB 탈취 가능 | 암호화 + 최소 권한으로 피해 최소화 |
| 규정 준수 | OWASP 위반 | OWASP Top 10 A03 충족 |

📢 **섹션 요약 비유**: SQL Injection 방어는 자동차 안전벨트다. 하지 않아도 평소엔 멀쩡하지만, 사고 시 결과가 치명적으로 달라진다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| PreparedStatement | 핵심 방어 | 파라미터 바인딩으로 코드 분리 |
| WAF | 2차 방어 | HTTP 패턴 기반 공격 탐지 |
| DB 방화벽 | 3차 방어 | 쿼리 화이트리스트 |
| 최소 권한 | 피해 최소화 | DROP/TRUNCATE 권한 제거 |
| OWASP Top 10 | 기준 | 웹 보안 상위 10대 취약점 |

### 👶 어린이를 위한 3줄 비유 설명

1. SQL Injection은 주문서에 몰래 "전부 공짜로 해줘"라고 써넣는 것이에요.
2. PreparedStatement는 주문서 양식이 이미 인쇄돼 있어서 손님이 내용을 추가할 수 없는 것이에요.
3. 방어 심층 구조는 문 잠금, 보안 카메라, 금고를 모두 갖춘 은행처럼 여러 층의 보호가 있는 것이에요.
