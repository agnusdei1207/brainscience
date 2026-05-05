+++
weight = 190
title = "190. 시큐어 코딩 가이드라인 (Secure Coding Guideline)"
date = "2026-04-21"
[extra]
categories = "studynote-it-management"
+++
## 0. 핵심 인사이트

> **핵심**: 시큐어 코딩(Secure Coding)은 소프트웨어 개발 단계에서 보안 취약점의 원인이 되는 코드 패턴을 사전 차단하는 것으로, 사후 패치보다 10~100배 비용 효율적이다.
> 2. **가치**: 행정안전부 47개 SW 보안 약점과 OWASP (Open Web Application Security Project) Top 10은 공공·민간 양쪽의 법적 준수 기준으로 작동하여 보안 사고 시 법적 책임의 분수령이 된다.
> 3. **판단 포인트**: 기술사 답안에서는 "입력값 검증(Input Validation) → 인코딩(Encoding) → 파라미터화 쿼리(Parameterized Query) → 최소 권한(Least Privilege)"의 4단 방어 체계를 구조화하면 고득점이다.

> 📝 모범 답안

## 1. 개요 및 필요성

대부분의 사이버 침해 사고는 취약한 코드에서 비롯된다. NIST (National Institute of Standards and Technology) 연구에 따르면 보안 취약점의 60% 이상이 코딩 단계에서 발생하고, 운영 단계에서 수정하면 설계 단계의 30배 비용이 든다. 이를 '결함 비용 증폭(Defect Cost Amplification)' 효과라 한다.

행정안전부는 「전자정부 SW 개발·운영자를 위한 소프트웨어 개발 보안 가이드」를 통해 47개 보안 약점(Security Weakness) 목록을 정의하고, 공공 소프트웨어 개발 사업에서 이를 의무 준수하도록 규정하였다. 보안 약점은 입력 데이터 검증 및 표현, 보안 기능, 시간 및 상태, 에러 처리, 코드 품질, 캡슐화, API 오용 등 7개 범주로 분류된다.

OWASP Top 10은 글로벌 표준으로, 2021년 기준 인젝션(Injection), 취약한 인증(Broken Authentication), 민감 데이터 노출, XXE (XML External Entity), 취약한 접근통제, 보안 구성 오류, XSS (Cross-Site Scripting), 안전하지 않은 역직렬화, 알려진 취약점 포함 컴포넌트 사용, 불충분한 로깅·모니터링이 포함된다.

📢 **섹션 요약 비유**: 시큐어 코딩은 집을 지을 때 문과 창문에 자물쇠를 달고 방화재를 쓰는 것처럼, 건물을 짓는 과정에서 보안을 내재화하는 것이다.

## 2. 구성요소

### 다층 방어 체계

```text
┌──────────────────────────────────────────────────────────────┐
│         시큐어 코딩 다층 방어 아키텍처                        │
├──────────────────────────────────────────────────────────────┤
│  [외부 입력]                                                  │
│      │                                                        │
│      ▼                                                        │
│  ┌──────────────────────────────┐                            │
│  │  1단: 입력값 검증             │  ← 화이트리스트, 정규식   │
│  │  (Input Validation)          │     길이·형식·범위 체크    │
│  └──────────────┬───────────────┘                            │
│                 │                                             │
│                 ▼                                             │
│  ┌──────────────────────────────┐                            │
│  │  2단: 출력 인코딩             │  ← HTML Escape, URL       │
│  │  (Output Encoding)           │     Encode, JSON Encode    │
│  └──────────────┬───────────────┘                            │
│                 │                                             │
│                 ▼                                             │
│  ┌──────────────────────────────┐                            │
│  │  3단: 파라미터화 쿼리        │  ← PreparedStatement,      │
│  │  (Parameterized Query)       │     ORM 사용, 동적 SQL 금지│
│  └──────────────┬───────────────┘                            │
│                 │                                             │
│                 ▼                                             │
│  ┌──────────────────────────────┐                            │
│  │  4단: 최소 권한 원칙         │  ← DB 계정 권한 최소화,    │
│  │  (Least Privilege)           │     OS 권한 분리           │
│  └──────────────┬───────────────┘                            │
│                 │                                             │
│                 ▼                                             │
│            [안전한 처리 결과]                                  │
└──────────────────────────────────────────────────────────────┘
```

### 행안부 47개 보안 약점 주요 범주

| 범주 | 개수 | 대표 약점 | 방어 기법 |
|:---|:---:|:---|:---|
| 입력 데이터 검증 및 표현 | 13개 | SQL 인젝션, XSS, 경로 순회 | 화이트리스트 검증, PreparedStatement |
| 보안 기능 | 16개 | 취약한 암호화 알고리즘, 하드코딩 패스워드 | AES-256, 키 관리 정책 |
| 시간 및 상태 | 2개 | TOCTOU (Time-of-Check-to-Time-of-Use) 경쟁 조건 | 원자적 연산, 잠금 메커니즘 |
| 에러 처리 | 4개 | 민감 정보 에러 메시지 노출 | 일반화된 에러 메시지 반환 |
| 코드 품질 | 5개 | 초기화되지 않은 변수 사용 | 정적 분석 도구 활용 |
| 캡슐화 | 4개 | 잘못된 세션 데이터 공유 | 범위 최소화, Private 선언 |
| API 오용 | 3개 | DNS Lookup 결과 신뢰, 취약 함수 사용 | 보안 API 매핑 테이블 준수 |

### SQL 인젝션(SQL Injection) 방어 예시

**취약 코드 (Bad)**:
```sql
-- 동적 쿼리 직접 연결 → SQL Injection 가능
String query = "SELECT * FROM user WHERE id='" + userId + "'";
```

**안전 코드 (Good)**:
```sql
-- PreparedStatement로 파라미터 분리
PreparedStatement ps = conn.prepareStatement(
    "SELECT * FROM user WHERE id = ?");
ps.setString(1, userId);
```

📢 **섹션 요약 비유**: 파라미터화 쿼리는 식당 주문서에 고객이 직접 쓰지 못하게 하고, 직원이 정해진 항목만 체크하도록 양식을 고정하는 것과 같다.

## 3. 구조 및 동작 원리

| 구분 | 행안부 47개 보안 약점 | OWASP Top 10 |
|:---|:---|:---|
| 적용 범위 | 공공기관 SW 개발 (국내 법적 의무) | 글로벌 웹 애플리케이션 |
| 갱신 주기 | 필요 시 수시 개정 | 3~4년 주기 (2013, 2017, 2021) |
| 분류 기준 | 코드 취약 패턴(Weakness) | 리스크 기반 위협(Risk) |
| 활용 방식 | SAST 도구 룰셋 매핑 | 보안 테스트 체크리스트 |
| 주요 항목 | SQL 인젝션, XSS, 경로 순회 등 | A01:인젝션, A07:XSS 포함 |
| 법적 효력 | 전자정부법 기반 강제 | 자율 권고 (사실상 표준) |

### XSS (Cross-Site Scripting) 유형별 비교

| 유형 | 메커니즘 | 지속성 | 방어 방법 |
|:---|:---|:---:|:---|
| Stored XSS | 악성 스크립트를 DB에 저장 → 피해자가 조회 시 실행 | 영구 | 저장 시 HTML 인코딩 |
| Reflected XSS | 악성 URL 파라미터 → 서버가 즉시 반사 출력 | 임시 | 출력 시 HTML Escape |
| DOM-based XSS | 클라이언트 JavaScript가 DOM 직접 조작 | 임시 | innerHTML 대신 textContent 사용 |

📢 **섹션 요약 비유**: 행안부 기준은 국내 교통법규이고 OWASP는 국제 교통 안전 기준이다 — 국내에서는 둘 다 지켜야 진짜 안전하다.

## 4. 비교 및 트레이드오프

**시큐어 코딩 개발 프로세스 통합 방안**  
① **요구사항 단계**: 보안 요구사항 명세서(Security Requirements Specification)에 행안부 47개 약점 체크리스트를 포함한다.  
② **설계 단계**: 위협 모델링(Threat Modeling, STRIDE 방법론)을 수행하고 설계 단계에서 인증·인가·암호화 아키텍처를 확정한다.  
③ **구현 단계**: IDE (Integrated Development Environment) 플러그인 형태의 SAST (Static Application Security Testing) 도구(FindBugs, Checkmarx, SonarQube)를 연동하여 실시간 취약점을 탐지한다.  
④ **테스트 단계**: DAST (Dynamic Application Security Testing, OWASP ZAP, Burp Suite)로 런타임 취약점을 검증한다.  
⑤ **운영 단계**: WAF (Web Application Firewall)와 IPS (Intrusion Prevention System)로 방어층을 추가한다.

**DevSecOps 연계**  
CI/CD (Continuous Integration/Continuous Delivery) 파이프라인에 SAST와 DAST를 자동화 게이트로 삽입하여, 취약점이 탐지되면 빌드를 자동 실패시키는 'Security Gate' 방식으로 운영한다.

📢 **섹션 요약 비유**: DevSecOps 보안 게이트는 공장 컨베이어 벨트에 불량품 감지 센서를 달아, 결함품이 라인을 통과하지 못하게 자동 차단하는 것과 같다.

## 5. 실무 적용 및 최적화 기법

시큐어 코딩 가이드라인의 체계적 적용은 **보안 취약점 사전 예방(Shift-Left Security)** 효과를 극대화한다. 행안부 기준 공공 사업에서 시큐어 코딩 준수율이 80% 이상일 때, 사후 패치 비용이 평균 40% 감소하는 효과가 보고된다.

미래 방향으로는 AI 기반 코드 분석 도구(GitHub Copilot Security, Amazon CodeGuru)가 개발자 작성 코드를 실시간으로 취약점 분석하고 수정안을 제안하는 방향으로 발전하고 있다. LLM (Large Language Model) 생성 코드에 대한 보안 검증 가이드라인 수립도 새로운 과제다.

📢 **섹션 요약 비유**: 시큐어 코딩은 백신 접종과 같다 — 아프기 전에 예방하는 것이 훨씬 싸고, 확산을 막아 모두를 보호한다.

### 📌 관련 개념 맵
| 개념 | 설명 | 연관 키워드 |
|:---|:---|:---|
| 행안부 47개 보안 약점 | 국내 공공 SW의 법적 시큐어 코딩 기준 | 전자정부법, 소프트웨어 보안 가이드 |
| OWASP Top 10 | 글로벌 웹 애플리케이션 최대 보안 위협 목록 | SQL Injection, XSS, CSRF |
| SAST | 소스코드 정적 분석 보안 테스트 | SonarQube, Checkmarx, FindBugs |
| DAST | 실행 중 애플리케이션 동적 보안 테스트 | OWASP ZAP, Burp Suite |
| Parameterized Query | SQL 인젝션 방어를 위한 파라미터 분리 쿼리 | PreparedStatement, ORM |

### 👶 어린이를 위한 3줄 비유 설명
1. SQL 인젝션은 주문서에 "공짜로 줘"라고 몰래 써넣는 것처럼 해커가 입력칸에 나쁜 명령어를 넣는 것이에요.
2. 시큐어 코딩은 주문서에 정해진 항목만 선택할 수 있도록 만들어서, 나쁜 내용을 아예 쓸 수 없게 만드는 거예요.
3. OWASP 규칙을 따르면 전 세계가 동의한 가장 위험한 10가지 공격을 미리 막을 수 있어요.
