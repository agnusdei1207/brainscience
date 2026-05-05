+++
weight = 305
title = "305. 암호 스위트 명명 규칙 (Cipher Suite Naming Convention)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: 암호 스위트 이름은 `키교환_인증_WITH_암호화알고리즘_해시` 형식으로 해독 가능한 설계 의도가 그대로 담긴 "알고리즘 명세서"다.
> 2. **가치**: 이름만 읽어도 PFS (Perfect Forward Secrecy) 지원 여부·인증 방식·암호 강도를 한 번에 파악할 수 있어 보안 감사와 설정 검토에서 바로 활용된다.
> 3. **판단 포인트**: IANA (Internet Assigned Numbers Authority) 표준 명명과 OpenSSL 내부 명명은 동일한 알고리즘을 다른 문자열로 표기하므로, 설정 파일에 어느 형식을 써야 하는지를 혼동하지 않는 것이 실무 핵심이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

TLS (Transport Layer Security) 암호 스위트 이름은 처음 접하면 암호처럼 보이지만, 규칙을 알면 즉시 해독된다. 예를 들어 `TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384`는 다섯 파트로 나뉘어 각각 어떤 키 교환, 인증, 암호화, 해시 알고리즘을 사용하는지 명시한다.

표준화된 명명 규칙이 필요한 이유는 두 가지다. 첫째, 클라이언트와 서버가 `ClientHello`/`ServerHello`에서 2바이트 숫자 코드(예: `0xC0,0x2C`)로 스위트를 교환하는데, 이 숫자를 사람이 읽으려면 공식 이름이 반드시 필요하다. 둘째, Nginx·Apache·Java JSSE (Java Secure Socket Extension) 등 구현체마다 사용하는 이름 체계가 미묘하게 다르기 때문에 혼용 시 "지원하지 않는 스위트" 오류가 발생한다.

기술사 시험에서 명명 규칙은 "스위트 이름을 보고 취약점을 지적하라"는 형태로 자주 출제된다. 이름을 분석하면 PFS 부재, CBC 모드 사용, SHA-1 해시 사용 등 보안 결함을 바로 식별할 수 있다.

📢 **섹션 요약 비유**: 암호 스위트 이름은 자동차 모델명(예: K5 2.0T AWD Premium)처럼 엔진·구동계·옵션을 압축한 설명서다. 이름만 봐도 사양을 알 수 있다.

---

## 2. 구성요소

### 이름 파싱 구조

```
TLS _ ECDHE _ RSA _ WITH _ AES _ 256 _ GCM _ SHA384
 ①      ②     ③    구분자   ④    ⑤    ⑥      ⑦

① 프로토콜 접두사  : TLS  (SSL 시대에는 SSL_)
② 키 교환 알고리즘 : ECDHE (Ephemeral Elliptic Curve DH)
③ 인증 알고리즘    : RSA
④ 대칭 암호화      : AES (Advanced Encryption Standard)
⑤ 키 길이          : 256 bit
⑥ 운용 모드        : GCM (Galois/Counter Mode)
⑦ 해시/PRF         : SHA384

──────────────────────────────────────────────────
┌────────────────────────────────────────────────┐
│  TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384         │
│  ├─ PFS 여부  : ✅ (ECDHE → Ephemeral)         │
│  ├─ 인증 방식 : RSA 인증서                      │
│  ├─ 암호 강도 : 256 bit (고보안)               │
│  ├─ 암호 모드 : GCM = AEAD (취약점 없음)        │
│  └─ 해시 강도 : SHA-384 (강력)                  │
└────────────────────────────────────────────────┘
```

### 각 파트별 알고리즘 옵션

| 파트 | 옵션 | 보안 등급 |
|:---|:---|:---|
| 키 교환 | RSA | ⚠️ PFS 없음, 비권장 |
| 키 교환 | DHE (Ephemeral DH) | ✅ PFS 있음 |
| 키 교환 | ECDHE (Ephemeral ECDH) | ✅✅ PFS + 성능 |
| 인증 | RSA | ✅ 범용 |
| 인증 | ECDSA (Elliptic Curve DSA) | ✅✅ 성능 우수 |
| 암호화 | AES-128-CBC | ⚠️ 패딩 오라클 주의 |
| 암호화 | AES-256-GCM | ✅✅ AEAD |
| 암호화 | ChaCha20-Poly1305 | ✅✅ AEAD, 저전력 |
| 해시 | MD5, SHA-1 | ❌ 폐기 |
| 해시 | SHA-256, SHA-384 | ✅ 현용 |

### TLS 1.3 명명의 변화

TLS 1.3에서는 키 교환과 인증이 스위트 이름에서 분리되어 이름이 대폭 짧아졌다:

```
TLS 1.2 : TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
TLS 1.3 : TLS_AES_256_GCM_SHA384
           ↑
           키 교환·인증 파트 삭제
           (항상 ECDHE·인증서 방식이므로 불필요)
```

📢 **섹션 요약 비유**: TLS 1.3 이름은 "세트 메뉴 A"처럼 간단하다. 재료가 이미 최고급으로 고정되어 있어 구구절절 설명이 필요 없다.

---

## 3. 구조 및 동작 원리

### IANA 명명 vs OpenSSL 명명

동일한 암호 스위트를 IANA와 OpenSSL이 다르게 표기한다. 설정 파일에서 혼동하면 `no shared cipher` 오류가 발생한다.

| IANA 표준 이름 | OpenSSL 이름 | IANA 코드 |
|:---|:---|:---|
| TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 | ECDHE-RSA-AES256-GCM-SHA384 | 0xC0,0x30 |
| TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 | ECDHE-RSA-AES128-GCM-SHA256 | 0xC0,0x2C |
| TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 | ECDHE-ECDSA-AES256-GCM-SHA384 | 0xC0,0x2C |
| TLS_RSA_WITH_AES_256_CBC_SHA256 | AES256-SHA256 | 0x00,0x3D |
| TLS_AES_256_GCM_SHA384 (1.3) | TLS_AES_256_GCM_SHA384 | 0x13,0x02 |

**주요 차이점**:
- IANA: `TLS_` 접두사, `WITH` 구분자, 언더스코어(`_`)
- OpenSSL: 접두사 없음, `-` 구분자, `TLS 1.3`은 IANA와 동일
- Java JSSE: IANA 명명 사용하지만 `TLS_` 대신 `SSL_`을 쓰는 레거시 잔재 존재

📢 **섹션 요약 비유**: 같은 노래를 한국어 제목, 영어 제목, 일본어 제목으로 부르는 것과 같다. 멜로디(알고리즘)는 같지만 표기가 다르다.

---

## 4. 비교 및 트레이드오프

**OpenSSL로 스위트 목록 확인**

```bash
# 현재 지원 스위트 나열
openssl ciphers -v 'ALL:!aNULL'

# TLS 1.3 스위트만 확인
openssl ciphers -v -s -tls1_3

# 특정 서버의 협상된 스위트 확인
openssl s_client -connect example.com:443 2>/dev/null | grep "Cipher is"
```

**Nginx 스위트 설정 — OpenSSL 명명 사용**

```nginx
ssl_ciphers 'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:!aNULL:!MD5';
```

**Java 애플리케이션 — IANA 명명 사용**

```java
SSLContext ctx = SSLContext.getInstance("TLSv1.3");
SSLParameters params = new SSLParameters();
params.setCipherSuites(new String[]{
    "TLS_AES_256_GCM_SHA384",
    "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"
});
```

**취약 스위트 식별 체크리스트**:
- 이름에 `RC4`, `DES`, `3DES`, `NULL`, `EXPORT`, `anon` 포함 → 즉시 비활성화
- 이름에 `MD5`, `SHA` (SHA-1) 해시 → SHA-256 이상으로 교체
- 키 교환이 `RSA`만 → PFS 없음, `ECDHE`로 교체

📢 **섹션 요약 비유**: 스위트 이름 분석은 식품 영양 성분표 읽기다. 나트륨(취약 알고리즘) 함량을 보고 구매 여부를 결정한다.

---

## 5. 실무 적용 및 최적화 기법

명명 규칙을 정확히 이해하면 보안 감사 시 수십 개의 스위트를 빠르게 분류할 수 있다. 특히 레거시 시스템 점검에서 `grep -i "RC4\|NULL\|EXPORT\|DES"` 한 줄로 비허용 스위트를 필터링하는 것이 가능하다.

기술사 시험 관점에서는 "주어진 스위트 이름에서 보안 문제점을 찾아라"라는 문제에 명명 규칙 지식이 직접 적용된다. TLS 1.3 전환 시 이름이 짧아진 이유, OpenSSL 설정에서 IANA 이름을 사용하면 발생하는 오류 등이 논술 및 단답 주제로 활용된다.

📢 **섹션 요약 비유**: 명명 규칙 숙지는 지도 읽는 법을 배우는 것이다. 지도를 읽을 줄 알면 어떤 지형이든 빠르게 파악할 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| TLS 암호 스위트 | 상위 | 명명 규칙의 적용 대상 |
| IANA | 표준화 기관 | 공식 스위트 번호와 이름 등록 |
| OpenSSL | 구현체 | 자체 명명 체계 사용 |
| PFS (Perfect Forward Secrecy) | 관련 기능 | 이름에서 ECDHE/DHE로 확인 가능 |
| AEAD | 관련 개념 | GCM, CCM, Poly1305 → 이름에 명시 |
| TLS 핸드셰이크 | 사용 시점 | ClientHello에서 스위트 이름 목록 전송 |

### 👶 어린이를 위한 3줄 비유 설명
1. 암호 스위트 이름은 레고 설명서처럼 "어떤 블록을 어떤 순서로 쓸지" 적혀 있어요.
2. TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384은 "튼튼한 열쇠로 문 열고, 강력한 금고에 넣고, 지문으로 확인"하는 방법이에요.
3. 이름만 읽어도 "이 자물쇠가 낡은 건지 새것인지" 바로 알 수 있어요.
