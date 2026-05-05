+++
weight = 488
title = "488. Nikto (웹 서버 취약점 스캐너)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: Nikto는 웹 서버의 알려진 취약점·위험한 파일·구성 오류를 빠르게 스캔하는 오픈소스 CLI (Command Line Interface) 도구로, 6,700개 이상의 잠재적 위험 항목을 데이터베이스로 관리한다.
> 2. **가치**: 초기 정보 수집(Reconnaissance) 단계에서 빠른 공격 표면(Attack Surface) 파악에 유용하며, 서버 헤더·쿠키 설정·디렉토리 노출 등을 자동으로 점검한다.
> 3. **판단 포인트**: Nikto는 스텔스 기능이 없어 IDS (Intrusion Detection System)/WAF에 즉시 탐지되므로, 은밀한 테스트보다는 빠른 기본 점검에 적합하다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

Nikto는 2001년 CIRT.net에서 개발한 웹 서버 취약점 스캐너이다. Apache·Nginx·IIS (Internet Information Services) 등 모든 웹 서버를 대상으로 취약한 파일·디렉토리(예: `/admin`, `/.git`, `/phpinfo.php`), 서버 헤더 정보 노출, 구형 소프트웨어 버전 등을 탐지한다.

Kali Linux에 기본 탑재되어 있으며, Perl로 작성되어 크로스 플랫폼 동작이 가능하다.

📢 **섹션 요약 비유**: 건물 외관을 빠르게 돌아다니며 열린 문·깨진 창문·경고 표지판을 체크하는 빠른 사전 점검이다.

---

## 2. 구성요소

| 스캔 항목 | 예시 | 위험 |
|:---|:---|:---|
| 위험한 파일 | `/phpinfo.php`, `/.git` | 정보 노출 |
| 구형 소프트웨어 | Apache 2.2.x | CVE (Common Vulnerabilities Exposures) 취약점 |
| 보안 헤더 누락 | X-Frame-Options, CSP 없음 | Clickjacking, XSS |
| 기본 자격증명 | `admin:admin` 기본값 | 무단 접근 |
| 취약한 CGI | 오래된 CGI (Common Gateway Interface) 스크립트 | RCE (Remote Code Execution) |

```
[Nikto 스캔 흐름]

nikto -h https://target.com -o report.html
  │
  ▼
대상 서버 연결
  │
  ▼
6,700+ 항목 점검
  ├─ 서버 버전 확인
  ├─ 위험 파일 경로 확인
  ├─ 보안 헤더 확인
  ├─ 쿠키 속성 확인
  └─ 디렉토리 리스팅 확인
  │
  ▼
결과 보고서 (HTML/CSV/XML)
```

📢 **섹션 요약 비유**: 점검관이 체크리스트(6,700항목)를 들고 건물 외관을 빠르게 순회하는 것이다.

---

## 3. 구조 및 동작 원리

| 도구 | 특징 | 탐지 난이도 |
|:---|:---|:---|
| Nikto | 빠른 기본 스캔, 노이즈 많음 | IDS에 즉시 탐지 |
| OWASP ZAP | 심층 스캔, CI/CD 통합 | 중간 |
| Burp Suite | 수동 심층 분석 | 설정에 따라 다름 |
| Nmap | 포트·서비스 스캔 | 낮음 |

📢 **섹션 요약 비유**: Nikto는 빠르지만 시끄러운 점검, Burp는 느리지만 조용한 정밀 분석이다.

---

## 4. 비교 및 트레이드오프

**기본 사용법**:
```
nikto -h https://target.com          # 기본 스캔
nikto -h https://target.com -Tuning 1  # SQL 인젝션 집중
nikto -h https://target.com -ssl      # HTTPS 강제
nikto -h https://target.com -useragent "Custom"  # UA 변경
```

방어자 관점: Nikto가 발견하는 항목들을 사전에 수정하면 공격자의 초기 정보 수집을 무력화할 수 있다. 특히 `X-Powered-By`, `Server` 헤더 제거와 보안 헤더 추가가 핵심이다.

📢 **섹션 요약 비유**: 점검관이 발견하는 문제들을 미리 고쳐두면 공격자가 찾을 것이 없어진다.

---

## 5. 실무 적용 및 최적화 기법

Nikto를 통한 기초 보안 점검으로 서버 구성 오류·정보 노출·레거시 취약점을 빠르게 파악할 수 있다. 정기적인 Nikto 스캔 결과를 기반으로 서버 하드닝(Hardening) 작업을 수행하면 공격 표면을 효과적으로 줄일 수 있다.

📢 **섹션 요약 비유**: 빠른 점검(Nikto)으로 쉬운 취약점을 먼저 제거하면 고급 공격자도 시작점을 잃는다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| CVE | 탐지 기반 | 알려진 취약점 데이터베이스 |
| 정보 수집 | 단계 | Nikto의 주요 활용 단계 |
| 서버 하드닝 | 방어 | Nikto 결과 기반 보안 강화 |
| IDS | 탐지됨 | Nikto 트래픽 즉시 탐지 |

### 👶 어린이를 위한 3줄 비유 설명
Nikto는 건물(웹 서버)을 빠르게 돌아다니며 열린 문·깨진 창문을 찾는 점검관이에요.
체크리스트(6,700항목)에 있는 문제들을 자동으로 확인해줘요.
점검관이 발견한 문제를 미리 고치면 나쁜 사람이 들어올 구멍이 없어져요.
