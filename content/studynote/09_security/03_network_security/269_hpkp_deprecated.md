+++
weight = 269
title = "269. HTTP Public Key Pinning (HPKP, Deprecated)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: HPKP (HTTP Public Key Pinning)는 서버가 브라우저에게 "앞으로 이 공개키만 신뢰하라"고 강제하는 헤더였으나, 잘못 설정 시 사이트가 영구 차단되는 치명적 위험으로 Chrome 68+ 이후 완전 제거됐다.
> 2. **가치**: HPKP가 해결하려 했던 불법 CA (Certification Authority) 발급 인증서 문제는 이제 CAA (Certification Authority Authorization) DNS 레코드와 CT (Certificate Transparency)로 더 안전하게 대체된다.
> 3. **판단 포인트**: 기술사 시험에서 HPKP 언급 시 "왜 실패했나"와 "무엇으로 대체됐나" 두 축을 반드시 서술해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

SSL/TLS (Secure Sockets Layer / Transport Layer Security) 생태계는 수백 개의 CA가 존재하며, 그 중 하나라도 침해되면 공격자가 임의 도메인에 대한 유효한 인증서를 발급받을 수 있다. 2011년 DigiNotar 해킹 사건이 대표적으로, 공격자는 *.google.com 인증서를 획득해 이란 사용자를 중간자 공격(MITM, Man-In-The-Middle Attack)으로 감청했다.

이런 위협에 대응하기 위해 RFC 7469로 표준화된 HPKP는 서버가 HTTP 응답 헤더 `Public-Key-Pins`를 통해 허용된 공개키 해시(SPKI Fingerprint, Subject Public Key Info Fingerprint) 목록을 브라우저에 캐싱시키는 메커니즘이다. 브라우저는 이후 연결 시 서버 인증서 체인 내에 핀된 공개키가 없으면 연결 자체를 차단한다.

문제는 HPKP가 양날의 검이었다는 점이다. 핀 유효 기간(`max-age`) 동안 인증서를 갱신하면서 공개키를 교체하거나, 백업 핀을 잃어버리면 브라우저는 해당 도메인에 **아무도 접근할 수 없는** 상태(Key Pinning Suicide)가 된다. Google, GitHub 등 대형 업체 외에는 운영 리스크가 너무 커 실질적 채택률이 0.1% 이하에 머물렀고, Chrome은 2018년(Chrome 68) HPKP 지원을 완전히 제거했다.

📢 **섹션 요약 비유**: HPKP는 "이 열쇠 외에는 절대 문을 열지 마"라는 자물쇠였지만, 열쇠를 잃어버리면 집주인도 못 들어가는 설계 결함이 있었다.

---

## 2. 구성요소

### HPKP 동작 흐름

```
브라우저 (Browser)              서버 (Server)
      │                               │
      │─── HTTPS 요청 ──────────────►│
      │                               │
      │◄── HTTP 응답 헤더 ────────────│
      │  Public-Key-Pins:             │
      │    pin-sha256="BASE64_A";     │
      │    pin-sha256="BASE64_B";     │
      │    max-age=2592000;           │
      │    includeSubDomains          │
      │                               │
      │  [브라우저가 핀 캐싱]         │
      │                               │
      │─── 다음 요청 (30일 이내) ───►│
      │  인증서 공개키 해시 비교      │
      │  핀 목록에 없으면 → 차단!     │
```

### HPKP 핵심 파라미터

| 파라미터 | 설명 | 권장값 |
|:---|:---|:---|
| `pin-sha256` | 공개키 SHA-256 해시 (Base64) | 현재 키 + 백업 키 최소 2개 |
| `max-age` | 핀 캐싱 유효 기간 (초) | 초기 60초, 검증 후 2592000 |
| `includeSubDomains` | 하위 도메인 적용 여부 | 신중하게 설정 |
| `report-uri` | 핀 실패 시 보고 엔드포인트 | 별도 서버 필요 |
| `Public-Key-Pins-Report-Only` | 차단 없이 보고만 | 테스트 단계 권장 |

SPKI Fingerprint 생성: `openssl x509 -pubkey -noout | openssl pkey -pubin -outform DER | openssl dgst -sha256 -binary | base64`

📢 **섹션 요약 비유**: HPKP 설정은 마치 금고 조합을 미리 공증해두는 것과 같아서, 조합을 바꾸려면 공증 만료 전에 새 조합도 함께 등록해야 한다.

---

## 3. 구조 및 동작 원리

### HPKP vs 대체 기술 비교

| 구분 | HPKP | CAA 레코드 | CT (Certificate Transparency) |
|:---|:---|:---|:---|
| **레이어** | HTTP 응답 헤더 | DNS (Domain Name System) | 로그 서버 기반 |
| **차단 주체** | 브라우저 | CA 발급 거부 | 브라우저/감사 도구 |
| **오설정 위험** | 사이트 완전 차단 | 없음 | 없음 |
| **적용 난이도** | 매우 높음 | 낮음 | 자동(브라우저 내장) |
| **현황** | Deprecated (Chrome 68+) | 권장 | Chrome/Firefox 강제 |
| **표준** | RFC 7469 | RFC 6844 | RFC 9162 |

CAA DNS 레코드 예시:
```
example.com. CAA 0 issue "letsencrypt.org"
example.com. CAA 0 issuewild ";"
example.com. CAA 0 iodef "mailto:security@example.com"
```
이 설정은 Let's Encrypt 외에는 발급 불가능하게 만들어, DigiNotar형 공격을 DNS 레벨에서 차단한다.

📢 **섹션 요약 비유**: HPKP가 "특정 열쇠만 허용"이라면, CAA는 "특정 열쇠 제조소만 허용"이다. 후자가 훨씬 유연하고 실수해도 돌이킬 수 있다.

---

## 4. 비교 및 트레이드오프

**HPKP 폐기 교훈 3가지**

1. **보안 메커니즘의 복잡성 vs 운영 가능성**: 아무리 강력해도 운영자가 올바르게 쓸 수 없으면 보안이 오히려 가용성 위협이 된다. HPKP는 이 원칙을 위반한 교과서적 사례다.

2. **백업 플랜 필수**: RFC 7469도 "백업 핀 2개 이상 필수"를 명시했지만 현실적으로 키 관리 절차 없이 적용하면 재앙이다.

3. **Preloading의 위험**: Chromium이 관리하는 HPKP preload 목록에 잘못 등록된 도메인은 소프트웨어 업데이트 없이는 복구가 불가능하다.

**현재 권장 대안 스택**

```
CAA DNS 레코드            → CA 무단 발급 방지
Certificate Transparency  → 불법 발급 감지/감사
DANE (DNS-based Authentication of Named Entities) + DNSSEC → DNS 기반 인증서 검증
MTA-STS (Mail Transfer Agent Strict Transport Security)     → 이메일 채널 보안
```

기술사 시험에서 HPKP를 논할 때는 "기술의 우수성보다 채택 가능성과 운영 안전성이 더 중요하다"는 교훈을 중심으로 서술하면 고득점을 기대할 수 있다.

📢 **섹션 요약 비유**: 좋은 자물쇠라도 잠그는 법이 너무 어려우면 아무도 안 쓰고 문을 열어두게 된다. 보안 설계는 최악의 사용자도 안전하게 쓸 수 있어야 한다.

---

## 5. 실무 적용 및 최적화 기법

HPKP의 실패는 보안 기술 설계에서 **"오류 허용성(Fault Tolerance)"과 "운영 복잡성(Operational Complexity)"을 함께 고려해야 한다**는 중요한 교훈을 남겼다. PKI (Public Key Infrastructure) 생태계의 신뢰 문제는 여전히 진화 중이며, CAA + CT + DANE의 조합이 현재 최선의 답에 가깝다.

보안 아키텍처 설계 시 "이 메커니즘이 실수를 용납하는가"를 먼저 질문해야 한다. 복잡한 키 관리가 필요한 메커니즘은 자동화 도구(예: Let's Encrypt의 ACME 프로토콜)와 결합될 때만 현실적 보안성이 보장된다.

📢 **섹션 요약 비유**: HPKP는 훌륭한 개념이었지만 "인간 오류"를 설계에 포함하지 않았다. 좋은 보안은 실수해도 집에 들어갈 수 있는 여분 열쇠를 갖추고 있다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| CT (Certificate Transparency) | 대체/보완 | 모든 인증서 공개 로그로 불법 발급 탐지 |
| CAA DNS 레코드 | 대체 | DNS로 허용 CA 지정, 오설정 위험 없음 |
| DANE (DNS-based Authentication) | 보완 | DNSSEC 기반 인증서 바인딩 |
| HSTS (HTTP Strict Transport Security) | 유사/생존 | HTTPS 강제, HPKP와 달리 폐기 안됨 |
| MITM 공격 | 위협 | HPKP가 방어하려 했던 공격 유형 |
| Preload List | 관련 | 크로미움 사전 로드 목록, HSTS/HPKP 적용 |

### 👶 어린이를 위한 3줄 비유 설명
학교 문에 "이 열쇠 외엔 절대 안 열려" 스티커를 붙였더니, 선생님이 열쇠를 잃어버려서 학교 문이 영원히 잠겼어요.
그래서 사람들은 "어느 열쇠 회사가 열쇠를 만들어도 되는지" 목록만 관리하기로 했어요 (CAA).
실수해도 다시 고칠 수 있는 방법이 훨씬 안전한 방법이에요!
