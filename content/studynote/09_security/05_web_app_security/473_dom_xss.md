+++
weight = 473
title = "473. DOM-based XSS"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: DOM-based XSS (Document Object Model 기반 XSS)는 서버를 거치지 않고 클라이언트 사이드 JavaScript가 DOM을 조작하는 과정에서 공격자 제공 데이터가 실행되는 XSS 유형이다.
> 2. **가치**: 서버 로그에 흔적이 없고 WAF (Web Application Firewall)가 탐지하기 어려워 가장 은밀한 XSS 유형이다.
> 3. **판단 포인트**: Source(데이터 출처)가 Sink(위험한 DOM API)로 흐르는 경로를 추적하는 것이 취약점 분석의 핵심이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

DOM-based XSS는 클라이언트 측 JavaScript가 `location.hash`, `document.referrer`, `window.name` 등 Source에서 데이터를 읽어 `innerHTML`, `eval()`, `document.write()` 등 Sink에 그대로 출력할 때 발생한다.

서버는 스크립트가 포함되지 않은 정상 응답을 보내므로, 서버 사이드 필터링이나 WAF로는 탐지할 수 없다. 특히 SPA (Single Page Application)에서 URL 해시값(`#`)을 사용한 클라이언트 라우팅이 일반화되면서 공격 표면이 넓어졌다.

📢 **섹션 요약 비유**: 서버(우체국)를 거치지 않고 직접 집 안(브라우저) 이곳저곳에 독을 뿌리는 공격이다.

---

## 2. 구성요소

| Source (입력원) | Sink (위험 API) | 결과 |
|:---|:---|:---|
| `location.hash` | `innerHTML` | XSS 실행 |
| `document.referrer` | `eval()` | 코드 실행 |
| `URLSearchParams` | `document.write()` | DOM 조작 |
| `postMessage` data | `dangerouslySetInnerHTML` | React XSS |

```
[DOM XSS 흐름]

URL: https://site.com/#<img src=x onerror=alert(1)>
          │
          ▼
      브라우저 JavaScript
          │
          │ var hash = location.hash.substr(1);
          │ document.getElementById('x').innerHTML = hash;  ← Sink
          ▼
      DOM 조작
          │
          ▼
  onerror 이벤트 실행 → alert(1) → 공격 성공
  (서버에는 # 이후 값 전송 안됨)
```

📢 **섹션 요약 비유**: 집 안(브라우저) 청소부(JavaScript)가 바깥(URL)의 쓰레기를 직접 실내에 가져다 놓는 것과 같다.

---

## 3. 구조 및 동작 원리

| 항목 | DOM XSS | Reflected XSS |
|:---|:---|:---|
| 서버 처리 | 없음 | 있음 |
| 로그 흔적 | 없음(해시는 서버 비전송) | 있음 |
| WAF 탐지 | 매우 어려움 | 가능 |
| 원인 | 클라이언트 JS 취약 코드 | 서버 출력 검증 부재 |

탐지 도구: DOM Invader (Burp Suite 내장), Semgrep JavaScript 규칙, ESLint 보안 플러그인으로 Source→Sink 흐름을 정적 분석할 수 있다.

📢 **섹션 요약 비유**: 서버(우체부)가 관여하지 않으니 CCTV(서버 로그·WAF)로는 볼 수 없다.

---

## 4. 비교 및 트레이드오프

**방어**:
1. `innerHTML` 대신 `textContent`·`createTextNode` 사용
2. `eval()`, `setTimeout(string)`, `setInterval(string)` 금지 (ESLint no-eval)
3. Trusted Types API (Chrome 정책) 적용으로 Sink 화이트리스트 관리
4. CSP `require-trusted-types-for 'script'`

**정적 분석**: CodeQL JavaScript 쿼리 `js/xss-through-dom`으로 자동 탐지 가능

📢 **섹션 요약 비유**: 청소부(JS)에게 쓰레기(외부 데이터)를 절대 실내로 가져오지 말라고 규칙(Trusted Types)을 정해두는 것이다.

---

## 5. 실무 적용 및 최적화 기법

Trusted Types API와 CSP를 결합하면 DOM XSS를 근본적으로 차단할 수 있다. CI/CD 파이프라인에 정적 분석 도구를 통합하면 코드 커밋 단계에서 취약 패턴을 사전 차단할 수 있다.

📢 **섹션 요약 비유**: 집 안 청소 규칙을 법으로 정해두면 어떤 청소부도 쓰레기를 실내로 들일 수 없다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| innerHTML | Sink | DOM 조작 위험 API |
| location.hash | Source | 클라이언트 입력 출처 |
| Trusted Types | 방어 | Sink 화이트리스트 API |
| CodeQL | 탐지 | 정적 Source→Sink 분석 |

### 👶 어린이를 위한 3줄 비유 설명
집 안(브라우저) 청소부(JavaScript)가 바깥(URL)에서 쓰레기를 직접 방 안에 뿌리는 게 DOM XSS예요.
우체부(서버)를 거치지 않으니 CCTV(WAF)에도 안 찍혀요.
청소 규칙(Trusted Types)을 만들면 쓰레기를 실내로 못 가져오게 할 수 있어요.
