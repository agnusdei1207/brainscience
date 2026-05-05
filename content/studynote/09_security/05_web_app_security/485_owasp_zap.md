+++
weight = 485
title = "485. OWASP ZAP (Zed Attack Proxy)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: OWASP ZAP (Zed Attack Proxy)는 OWASP (Open Web Application Security Project)에서 개발한 무료 오픈소스 웹 취약점 스캐너로, 수동·자동 취약점 탐지를 모두 지원하는 통합 웹 보안 테스트 도구이다.
> 2. **가치**: CI/CD (Continuous Integration/Continuous Delivery) 파이프라인에 통합하여 DAST (Dynamic Application Security Testing) 자동화가 가능하며, API 보안 테스트에도 활용된다.
> 3. **판단 포인트**: Active Scan은 실제 공격 페이로드를 전송하므로 운영 환경이 아닌 스테이징 환경에서만 사용해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

ZAP은 2010년 오픈소스로 공개되어 현재 가장 널리 사용되는 웹 보안 테스트 도구 중 하나이다. 인터셉팅 프록시로 동작하며, 브라우저와 웹 서버 사이에서 HTTP (Hypertext Transfer Protocol) 트래픽을 캡처·수정·재전송할 수 있다.

주요 기능: Spider(자동 URL 수집), Active Scan(취약점 자동 탐지), Passive Scan(트래픽 분석), Fuzzer, 인증 관리, API 스캔.

📢 **섹션 요약 비유**: 건물 보안 점검관(ZAP)이 문·창문·배관(HTTP 트래픽)을 직접 흔들어보며 취약점을 찾는 것이다.

---

## 2. 구성요소

| 스캔 유형 | 동작 | 위험 수준 |
|:---|:---|:---|
| Passive Scan | 트래픽 관찰만 | 무해 |
| Spider | URL 자동 크롤링 | 낮음 |
| Ajax Spider | SPA JavaScript 렌더링 | 낮음 |
| Active Scan | 취약점 페이로드 전송 | 높음(운영 금지) |
| Fuzzer | 커스텀 페이로드 | 높음 |

```
[ZAP 동작 아키텍처]

브라우저
  │ HTTP 요청
  ▼
ZAP 프록시 (8080포트)
  ├─ Passive Scan: 트래픽 분석
  ├─ Spider: 링크 자동 수집
  ├─ Active Scan: 취약점 페이로드 주입
  │    ├─ SQLi 테스트
  │    ├─ XSS 테스트
  │    └─ Path Traversal 테스트
  ▼
대상 웹 서버
  │ 응답
  ▼
ZAP 결과 보고서
  Alert: High/Medium/Low/Informational
```

📢 **섹션 요약 비유**: 건물 점검관이 실제로 문을 두드리고(Active) 유리창을 들여다보며(Passive) 취약점을 기록하는 것이다.

---

## 3. 구조 및 동작 원리

| 도구 | 특징 | 유형 |
|:---|:---|:---|
| OWASP ZAP | 무료, CI/CD 통합 | DAST |
| Burp Suite | 강력한 수동 테스트 | DAST(유료 Pro) |
| Nikto | 빠른 서버 취약점 스캔 | DAST |
| Nessus | 네트워크+웹 통합 | 취약점 스캐너 |

📢 **섹션 요약 비유**: ZAP은 무료 건물 안전 검사관, Burp Suite는 전문 보안 엔지니어—용도에 따라 선택한다.

---

## 4. 비교 및 트레이드오프

**CI/CD ZAP 통합 예시 (GitHub Actions)**:
```yaml
- name: ZAP Baseline Scan
  uses: zaproxy/action-baseline@v0.10.0
  with:
    target: 'https://staging.example.com'
```

**Baseline Scan**: Passive 스캔만 수행하여 CI/CD에서 안전하게 실행 가능. Full Scan은 Active 포함하여 스테이징 전용.

📢 **섹션 요약 비유**: 배포 전 검사관(ZAP)이 자동으로 건물을 점검하고 이상 있으면 배포를 막는 것이다.

---

## 5. 실무 적용 및 최적화 기법

ZAP을 CI/CD에 통합하면 웹 취약점을 배포 전에 자동으로 탐지하여 Shift-Left 보안을 실현할 수 있다. Baseline Scan은 Passive 모드이므로 운영 환경에도 적용 가능하다.

📢 **섹션 요약 비유**: 건물을 짓는 과정(CI/CD)에서 매번 검사관이 확인하면 완공 후 수리비(보안 사고 비용)가 줄어든다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| DAST | 분류 | 동적 애플리케이션 보안 테스트 |
| CI/CD | 통합 환경 | 자동화 파이프라인 보안 테스트 |
| Active Scan | 기능 | 취약점 페이로드 자동 전송 |
| Burp Suite | 비교 도구 | 전문 수동 테스트 도구 |

### 👶 어린이를 위한 3줄 비유 설명
ZAP은 웹사이트(건물)의 약한 곳을 찾아주는 무료 보안 점검관이에요.
문을 두드려보고(Active Scan) 눈으로 살펴보며(Passive Scan) 취약점을 기록해요.
건물을 지을 때마다(배포마다) 자동으로 점검하면 나중에 큰 수리를 안 해도 돼요.
