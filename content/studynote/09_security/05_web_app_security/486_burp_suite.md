+++
weight = 486
title = "486. Burp Suite (웹 취약점 진단 도구)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: Burp Suite는 PortSwigger사의 웹 애플리케이션 보안 테스트 통합 플랫폼으로, 인터셉팅 프록시를 중심으로 스캐너·인트루더·리피터 등 다양한 모듈을 제공한다.
> 2. **가치**: 수동 침투 테스트에서 가장 강력한 도구이며, 전문 모의해킹(Penetration Testing) 시장에서 사실상 표준 도구로 사용된다.
> 3. **판단 포인트**: Community Edition은 무료지만 자동 스캐너가 없고, Professional Edition($449/년)에서 Active Scanner, Burp Collaborator가 제공된다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

Burp Suite는 2003년 처음 출시되어 현재 버전 2.x까지 발전했다. 인터셉팅 프록시를 통해 HTTP/HTTPS (Hypertext Transfer Protocol Secure) 트래픽을 실시간으로 캡처하고 수정할 수 있어, 웹 애플리케이션의 모든 요청·응답을 완전히 제어할 수 있다.

주요 모듈: Proxy(인터셉팅), Scanner(자동 취약점 탐지), Intruder(자동화 공격), Repeater(요청 수동 반복), Decoder(인코딩 변환), Comparer(응답 비교), Collaborator(Out-of-Band 공격), DOM Invader(DOM XSS 탐지).

📢 **섹션 요약 비유**: 웹 보안 스위스 아미 나이프—하나의 도구에 모든 기능이 담긴 전문 해킹 도구 세트이다.

---

## 2. 구성요소

| 모듈 | 기능 | 용도 |
|:---|:---|:---|
| Proxy | HTTP 인터셉팅 | 트래픽 분석 |
| Scanner | 자동 취약점 탐지 | DAST 자동화 |
| Intruder | 자동화 페이로드 주입 | Brute Force, Fuzzing |
| Repeater | 단일 요청 반복 수정 | 수동 취약점 검증 |
| Collaborator | Out-of-Band 서버 | Blind XXE/SSRF 탐지 |

```
[Burp Suite 프록시 구조]

브라우저
  (Proxy 설정: 127.0.0.1:8080)
  │
  ▼
Burp Proxy
  ├─ Intercept: 요청 일시 정지·수정
  ├─ HTTP History: 모든 요청 로그
  └─ WebSockets: WS 트래픽 캡처
  │
  ▼
대상 웹 서버

[Intruder 공격 유형]
  Sniper: 단일 파라미터 퍼징
  Battering Ram: 모든 파라미터 동일 페이로드
  Pitchfork: 파라미터별 다른 페이로드 리스트
  Cluster Bomb: 모든 조합
```

📢 **섹션 요약 비유**: 탐정(침투 테스터)의 도구 가방—현미경(Proxy), 자물쇠 따개(Intruder), 기록장(Repeater)이 모두 들어있다.

---

## 3. 구조 및 동작 원리

| 항목 | Burp Community | Burp Professional |
|:---|:---|:---|
| 가격 | 무료 | $449/년 |
| 자동 스캐너 | 없음 | 있음 |
| Intruder 속도 | 제한적 | 무제한 |
| Collaborator | 없음 | 있음 |

📢 **섹션 요약 비유**: 커뮤니티(무료)는 기본 도구, 프로(유료)는 완전한 해킹 실험실이다.

---

## 4. 비교 및 트레이드오프

**SQL 인젝션 테스트 워크플로우**:
1. Proxy로 로그인 요청 캡처
2. Repeater로 전송, 파라미터에 `'` 입력 후 오류 확인
3. Intruder로 Union-based SQLi 페이로드 자동화

**Burp Collaborator 활용**: DNS·HTTP Out-of-Band 서버로 Blind SSRF (Server-Side Request Forgery), Blind XXE (XML External Entity) 탐지에 필수적이다.

📢 **섹션 요약 비유**: Collaborator는 범죄 현장에 마련한 비밀 수신함—직접 보이지 않는 공격도 증거를 남긴다.

---

## 5. 실무 적용 및 최적화 기법

Burp Suite를 활용한 수동 침투 테스트는 자동화 스캐너가 놓치는 복잡한 비즈니스 로직 취약점을 발견하는 데 탁월하다. 기술사 시험에서 모의해킹 도구 관련 논술 시 ZAP(무료, CI/CD)과 Burp(전문, 수동)의 용도 차이를 명확히 설명하는 것이 중요하다.

📢 **섹션 요약 비유**: 자동화 로봇(ZAP)은 빠르지만 섬세한 범죄는 전문 형사(Burp)가 찾아낸다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| DAST | 분류 | 동적 보안 테스트 유형 |
| Intruder | 핵심 모듈 | 자동화 페이로드 공격 |
| Collaborator | 고급 기능 | Out-of-Band 공격 탐지 |
| OWASP ZAP | 비교 도구 | 무료 DAST 대안 |

### 👶 어린이를 위한 3줄 비유 설명
Burp Suite는 웹사이트(건물)의 모든 구석을 탐색할 수 있는 탐정 도구 세트예요.
모든 대화(HTTP 요청)를 엿듣고(Proxy), 반복해보고(Repeater), 자동으로 시험해볼(Intruder) 수 있어요.
전문 탐정(침투 테스터)이 사용하는 도구라서 올바른 목적으로만 써야 해요.
