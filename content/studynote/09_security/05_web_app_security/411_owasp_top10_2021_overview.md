+++
weight = 411
title = "411. OWASP Top 10 2021 Overview"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: OWASP (Open Web Application Security Project) Top 10 2021은 전 세계 웹 애플리케이션에서 가장 빈번하고 위험한 보안 취약점 10개를 데이터 기반으로 선정한 업계 표준 가이드다.
> 2. **가치**: 2021년판은 Broken Access Control이 1위로 올라서고 Insecure Design, Software Integrity Failures가 신규 진입하는 등 클라우드·API·공급망 보안의 패러다임 전환을 반영한다.
> 3. **판단 포인트**: OWASP Top 10은 체크리스트가 아니라 리스크 인식 프레임워크다. 각 항목의 발생 빈도, 탐지 난이도, 영향 범위를 교차 분석하여 우선순위를 정해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

OWASP Top 10은 2003년 처음 발표되어 현재까지 웹 보안 분야에서 가장 광범위하게 인용되는 참조 기준이다. 정기적으로 업데이트되며, 전 세계 수백 개 조직의 실제 취약점 데이터와 전문가 설문을 종합해 순위를 결정한다.

2021년판은 특히 중요한 전환점이었다. Broken Access Control (접근 제어 실패)가 5위에서 1위로 급상승했고, Insecure Design (안전하지 않은 설계) 이라는 설계 단계 취약점이 신규 등장했으며, Software and Data Integrity Failures (소프트웨어·데이터 무결성 실패)는 공급망 공격과 CI/CD (Continuous Integration/Continuous Delivery) 파이프라인 보안을 반영한다.

OWASP Top 10은 단독 보안 표준이 아니라 ISO 27001 (정보보안 관리 체계), PCI DSS (Payment Card Industry Data Security Standard), NIST SP 800-53 등 다양한 컴플라이언스 프레임워크의 참조 기준으로도 활용된다.

📢 **섹션 요약 비유**: OWASP Top 10은 의사가 가장 흔한 질병 10개를 미리 알고 진단 체크리스트를 만드는 것과 같다. 100가지 병을 다 알기보다, 실제로 사람을 가장 많이 죽이는 병 10가지를 집중 관리하는 전략이다.

---

## 2. 구성요소

OWASP Top 10 2021 순위는 발생률(Incidence Rate), 탐지 용이성, 기술적 영향, 비즈니스 영향을 종합 점수화하여 결정된다.

| 순위 | 카테고리 (Category) | 핵심 위험 |
|:---:|:---|:---|
| A01 | Broken Access Control (접근 제어 실패) | 권한 초과 접근 |
| A02 | Cryptographic Failures (암호화 실패) | 민감 데이터 노출 |
| A03 | Injection (인젝션) | SQL/OS/LDAP 명령 삽입 |
| A04 | Insecure Design (안전하지 않은 설계) | 설계 단계 결함 |
| A05 | Security Misconfiguration (보안 설정 오류) | 기본값·권한 오설정 |
| A06 | Vulnerable Components (취약한 구성 요소) | 구식 라이브러리 |
| A07 | Authentication Failures (인증 실패) | 크리덴셜 공격 |
| A08 | Software Integrity Failures (무결성 실패) | 공급망·CI/CD 공격 |
| A09 | Logging & Monitoring Failures (로깅 실패) | 침해 탐지 불가 |
| A10 | SSRF (서버 측 요청 위조) | 내부망 침투 |

```
┌──────────────────────────────────────────────────────────┐
│             OWASP Top 10 2021 위험 구조                  │
├──────────────────────────────────────────────────────────┤
│  설계 단계  →  A04 Insecure Design                       │
│  구현 단계  →  A03 Injection, A02 Crypto Failures        │
│  구성 단계  →  A05 Misconfig, A06 Vuln. Components       │
│  운영 단계  →  A09 Logging Failures, A10 SSRF            │
│  인증/인가  →  A01 Broken Access, A07 Auth Failures      │
│  공급망     →  A08 Integrity Failures                    │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: OWASP Top 10은 건물 안전 점검표와 같다. 설계 결함부터 배관, 전기, 출입 통제까지 각 단계별로 가장 치명적인 위험을 미리 점검한다.

---

## 3. 구조 및 동작 원리

2017년 대비 2021년의 주요 변화를 비교하면 보안 패러다임의 이동이 뚜렷하게 보인다.

| 변화 | 2017 순위 | 2021 순위 | 의미 |
|:---|:---:|:---:|:---|
| Broken Access Control | A05 | **A01** | 권한 관리 부실 급증 |
| Injection | A01 | A03 | 여전히 핵심이나 상대적 하락 |
| Insecure Design | 신규 | A04 | 설계 보안 중요성 대두 |
| Software Integrity | 신규 | A08 | 공급망 공격 반영 |
| SSRF | 신규 | A10 | 클라우드·API 환경 반영 |

📢 **섹션 요약 비유**: 2017년은 해킹이 주로 "공격자가 문을 부수는" 방식이었다면, 2021년은 "설계 단계에서 문이 없는 건물"과 "공급망 장악"으로 진화했다는 신호다.

---

## 4. 비교 및 트레이드오프

기술사 시험에서 OWASP Top 10은 세 가지 관점으로 출제된다.

1. **취약점 식별**: 시나리오 코드에서 A01~A10 중 어느 항목인지 진단
2. **우선순위 결정**: 제한된 보안 예산 내에서 어느 항목부터 대응할지 판단
3. **대응 아키텍처 설계**: 각 취약점에 맞는 기술 통제와 관리적 통제 제안

실무에서는 OWASP ZAP (Zed Attack Proxy), Burp Suite 같은 DAST (Dynamic Application Security Testing) 도구로 자동 스캔하고, SAST (Static Application Security Testing) 도구로 코드 레벨 검사를 병행한다.

📢 **섹션 요약 비유**: 기술사가 OWASP Top 10을 안다는 것은 의사가 가장 흔한 전염병의 증상과 치료법을 외우는 것과 같다. 진단 속도와 처방 정확도가 모두 달라진다.

---

## 5. 실무 적용 및 최적화 기법

OWASP Top 10 기반 보안 체계를 구축하면 인식 가능한 웹 취약점의 80% 이상을 커버할 수 있다. 특히 SDL (Secure Development Lifecycle)과 결합하면 개발 초기부터 보안을 내재화(Security by Design)할 수 있다.

궁극적으로 OWASP Top 10은 도구가 아니라 **조직 문화** 변화를 촉진하는 커뮤니케이션 수단이다. 개발팀과 보안팀, 경영진이 공통 언어로 리스크를 논의할 수 있게 해준다.

📢 **섹션 요약 비유**: OWASP Top 10은 전 세계 보안 전문가들이 "이것만큼은 반드시 막아야 한다"는 공통 언어로 만든 약속이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SDL (Secure Development Lifecycle) | 통합 프레임워크 | 개발 전 단계 보안 내재화 |
| DAST | 탐지 도구 | 런타임 취약점 스캔 |
| SAST | 탐지 도구 | 코드 레벨 정적 분석 |
| CVE (Common Vulnerabilities and Exposures) | 연계 | A06 취약 구성 요소 |
| PCI DSS | 컴플라이언스 참조 | 금융 보안 표준 |

### 👶 어린이를 위한 3줄 비유 설명
- OWASP Top 10은 전 세계에서 제일 많이 일어나는 10가지 나쁜 해킹 방법을 모아 놓은 목록이야.
- 이걸 알면 프로그램 만드는 사람들이 가장 위험한 구멍을 먼저 막을 수 있어.
- 마치 학교에서 "이 10가지 위험을 조심해!"라고 알려주는 안전 교육 같은 거야!
