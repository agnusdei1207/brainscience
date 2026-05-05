+++
weight = 304
title = "304. TLS 암호 스위트 (TLS Cipher Suite)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: TLS (Transport Layer Security) 암호 스위트는 키 교환·인증·대칭 암호화·MAC (Message Authentication Code) 네 가지 알고리즘을 하나의 패키지로 묶은 "보안 레시피"다.
> 2. **가치**: 서버와 클라이언트가 협상을 통해 공통 지원 스위트를 선택함으로써 하위 호환성과 최신 보안 강도를 동시에 유지한다.
> 3. **판단 포인트**: TLS 1.3은 취약한 키 교환 방식을 제거하고 5개 스위트만 허용해 협상 복잡도를 줄이는 대신, 반드시 PFS (Perfect Forward Secrecy)를 보장한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

TLS 핸드셰이크는 두 당사자가 서로 이해할 수 있는 암호화 방법을 선택하는 '메뉴판 주문' 과정이다. 클라이언트는 자신이 지원하는 스위트 목록을 `ClientHello` 메시지로 전송하고, 서버는 그 중 선호도가 가장 높은 스위트를 골라 `ServerHello`로 응답한다. 이 협상이 끝나야 실제 데이터 암호화가 시작된다.

암호 스위트가 중요한 이유는 알고리즘의 수명이 다르기 때문이다. DES (Data Encryption Standard)처럼 56비트에 불과했던 오래된 알고리즘은 현대 컴퓨터로 수시간 내에 브루트 포스가 가능하다. 반면 AES-256-GCM (Advanced Encryption Standard 256-bit Galois/Counter Mode)은 현재 양자 컴퓨터 이전까지 사실상 해독 불가로 평가된다. 따라서 서버 관리자는 취약한 스위트를 비활성화하고 강력한 스위트만 허용하는 설정이 필수다.

기업 환경에서는 규정 준수(PCI-DSS, NIST SP 800-52)에 따라 특정 스위트 이하의 버전이나 알고리즘을 금지한다. 기술사 시험에서도 "왜 TLS 1.0/1.1이 비활성화되어야 하는가"는 단골 질문인데, 그 핵심 답변이 바로 구식 암호 스위트의 강제 사용이다.

📢 **섹션 요약 비유**: 암호 스위트는 식당 세트 메뉴다. 메뉴판(ClientHello)을 보고 주방(서버)이 "오늘은 이 세트로 드시겠습니까?"라고 확정하는 것이 핸드셰이크 협상이다.

---

## 2. 구성요소

### 암호 스위트의 4가지 구성 요소

| 구성 요소 | 역할 | TLS 1.2 예시 | TLS 1.3 예시 |
|:---|:---|:---|:---|
| 키 교환 (Key Exchange) | 세션 키를 안전하게 합의 | RSA, DHE, ECDHE | ECDHE (필수) |
| 인증 (Authentication) | 서버/클라이언트 신원 확인 | RSA, ECDSA | RSA, ECDSA (인증서) |
| 대칭 암호화 (Bulk Cipher) | 실제 데이터 암호화 | AES-128-CBC, AES-256-GCM | AES-256-GCM, ChaCha20-Poly1305 |
| MAC/해시 (Hash/PRF) | 데이터 무결성·PRF 기반 | SHA-256, SHA-384 | SHA-256, SHA-384 |

TLS 1.3에서는 키 교환과 인증이 분리돼 스위트 이름이 짧아졌다. 인증 방식은 인증서 협상에서 별도 처리하므로 스위트 내에 포함되지 않는다.

```
TLS 1.2 Cipher Suite 협상 흐름

ClientHello ──────────────────────────────────►
  cipher_suites: [
    TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
    TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
    TLS_RSA_WITH_AES_256_CBC_SHA256,   ← 취약(PFS 없음)
    ...
  ]
                                ServerHello ◄──
                                  selected:
                              TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384

       [Certificate] ◄──────────────────────────
       [ServerKeyExchange (ECDHE params)] ◄──────
       [ServerHelloDone] ◄─────────────────────
[ClientKeyExchange] ──────────────────────────►
[ChangeCipherSpec] ──────────────────────────►
[Finished] ──────────────────────────────────►
                             [ChangeCipherSpec] ◄
                                  [Finished] ◄──
              ▼
     암호화 데이터 교환 시작
```

### TLS 1.2 vs TLS 1.3 스위트 비교

| 항목 | TLS 1.2 | TLS 1.3 |
|:---|:---|:---|
| 허용 스위트 수 | 수십 개 | 5개 |
| PFS 의무화 | 선택적 | 필수 |
| 0-RTT 지원 | 미지원 | 지원(재접속) |
| 취약 스위트 포함 가능 | 예 (RC4, NULL 등) | 불가 |
| 권장 스위트 | ECDHE + AES-256-GCM + SHA384 | TLS_AES_256_GCM_SHA384 |

### TLS 1.3 5대 스위트

1. `TLS_AES_128_GCM_SHA256` — 범용·성능 균형
2. `TLS_AES_256_GCM_SHA384` — 고보안 권장
3. `TLS_CHACHA20_POLY1305_SHA256` — 모바일·IoT 저전력
4. `TLS_AES_128_CCM_SHA256` — 임베디드 환경
5. `TLS_AES_128_CCM_8_SHA256` — 초경량 태그 (IoT)

📢 **섹션 요약 비유**: TLS 1.3은 음식 알레르기 유발 재료를 메뉴에서 아예 삭제한 신메뉴판이다. 고르는 항목이 줄었지만 모든 항목이 안전하다.

---

## 3. 구조 및 동작 원리

| 비교 항목 | 취약 구성 | 권장 구성 |
|:---|:---|:---|
| 키 교환 | RSA (정적) | ECDHE (임시, PFS) |
| 암호화 | AES-128-CBC | AES-256-GCM (AEAD) |
| 해시 | MD5, SHA-1 | SHA-256 이상 |
| TLS 버전 | 1.0, 1.1 | 1.3 (차선 1.2) |
| 인증서 서명 | SHA1WithRSA | SHA256WithECDSA |

AEAD (Authenticated Encryption with Associated Data) 방식(GCM, ChaCha20-Poly1305)은 암호화와 MAC을 동시에 처리하여 별도의 MAC 단계가 불필요하다. CBC (Cipher Block Chaining) 모드는 패딩 오라클 공격(POODLE, BEAST)에 취약하므로 현대 환경에서 사용을 지양한다.

📢 **섹션 요약 비유**: CBC 모드는 맥주 한 캔 + 안주 따로 주문, GCM은 일체형 세트다. 따로 주문하면 잘못 조합될 위험이 있다.

---

## 4. 비교 및 트레이드오프

**Nginx 권장 설정 예시**

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers on;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:10m;
```

**점검 시나리오**: `openssl s_client -connect example.com:443` 실행 후 `Cipher is` 행을 확인한다. `RC4`, `DES`, `NULL`, `EXPORT` 문자열이 보이면 즉시 비활성화 필요다.

**기술사 판단 포인트**:
- 서버가 `RSA` 키 교환을 유일하게 지원한다면 → PFS 부재 → 장기 키 유출 시 과거 트래픽 복호화 가능
- `CBC` 계열이 최우선 협상 → 패딩 오라클 위험 → `ssl_prefer_server_ciphers on`으로 서버 측 순서 강제 필요
- PCI-DSS 3.2.1 요건 6.5.4는 TLS 1.0 비활성화를 명시적으로 요구

📢 **섹션 요약 비유**: 서버가 스위트를 협상하는 것은 은행 금고의 자물쇠 등급을 고르는 것이다. 최신 등급 자물쇠가 있어도 낡은 자물쇠도 같이 두면 범인은 낡은 자물쇠를 공략한다.

---

## 5. 실무 적용 및 최적화 기법

강력한 TLS 암호 스위트 정책을 적용하면 세 가지 효과가 동시에 달성된다. 첫째, 도청(스니핑) 공격에서 기밀성이 확보된다. 둘째, 데이터 위·변조 시도를 AEAD MAC이 즉시 탐지해 무결성이 보장된다. 셋째, ECDHE를 통한 PFS로 서버 인증서가 나중에 탈취되더라도 과거 세션 데이터를 해독할 수 없다.

기술사 논술에서는 "암호 스위트 취약점 진단 → 권장 스위트로의 마이그레이션 절차 → 하위 호환성 고려 방안"을 세 단계로 전개하면 완성도 높은 답안이 된다. 특히 레거시 IE 지원 문제로 TLS 1.2를 완전히 포기할 수 없는 환경에서 `ssl_ciphers` 제한이 사실상의 보안 수문 역할을 한다는 점을 강조한다.

📢 **섹션 요약 비유**: 강력한 암호 스위트 정책은 수영장에 설치한 여러 겹의 방어망이다. 한 겹이 뚫려도 나머지가 이물질을 막는다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| TLS 핸드셰이크 | 상위 | 스위트 협상이 핸드셰이크 첫 단계 |
| PFS (Perfect Forward Secrecy) | 포함 | ECDHE 키 교환 선택 시 자동 달성 |
| AEAD | 포함 | GCM, ChaCha20-Poly1305 암호화 방식 |
| X.509 인증서 | 연동 | 인증 알고리즘(RSA/ECDSA) 결정 |
| HSTS (HTTP Strict Transport Security) | 보완 | TLS 강제 사용으로 다운그레이드 방지 |
| OpenSSL | 도구 | 스위트 설정·점검 주요 라이브러리 |

### 👶 어린이를 위한 3줄 비유 설명
1. 암호 스위트는 친구와 비밀 편지를 쓰기 전에 "어떤 비밀 코드를 쓸까?" 정하는 것이에요.
2. 오래된 코드(TLS 1.0)는 나쁜 사람이 이미 풀 수 있어서 새 코드(TLS 1.3)로 바꿔야 해요.
3. 제일 좋은 코드는 매번 새 열쇠를 만들어 써서(PFS), 예전 편지는 절대 읽을 수 없어요.
