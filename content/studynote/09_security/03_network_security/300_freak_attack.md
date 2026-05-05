+++
weight = 300
title = "300. FREAK — RSA_EXPORT 키 다운그레이드 (Factoring RSA Export Keys)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: FREAK(Factoring RSA Export Keys)는 미국 수출 규제 시대의 유물인 512비트 RSA_EXPORT 암호 스위트로 클라이언트를 다운그레이드한 뒤, RSA 팩토링(Factoring)으로 약한 키를 수 시간 내에 크래킹하여 TLS 세션을 복호화하는 공격이다.
> 2. **가치**: 2015년 발표 당시 OpenSSL·Apple SecureTransport·NSS 등 주요 TLS 라이브러리가 서버가 RSA_EXPORT를 요청하면 클라이언트도 수용하는 버그를 갖고 있어, 수백만 대의 Android·iOS 기기가 즉시 취약 상태였다.
> 3. **판단 포인트**: 서버 측에서 RSA_EXPORT 암호 스위트를 완전히 비활성화하고, 클라이언트 라이브러리를 패치하면 FREAK는 완전히 차단된다. 근본 원인은 Logjam과 마찬가지로 1990년대 수출 규제 정책이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

2015년 3월 INRIA(Institut National de Recherche en Informatique et en Automatique) 등 공동 연구팀이 공개한 FREAK은 SSL/TLS 역사의 가장 오랜 구조적 유산 중 하나를 공격한다.

1990년대 미국 정부는 NSA(National Security Agency)의 요청으로 수출용 암호 제품에 "EXPORT 등급"을 적용했다 — RSA는 512비트, DH는 512비트 이하로 제한됐다. 민주주의 국가 내수용은 1024비트 이상을 허용하면서, 해외에 수출하는 제품에만 약한 암호를 탑재했다.

규제가 완화된 후(1999년 이후) 개발자들은 내수용·수출용 코드를 통합하면서 EXPORT 암호 스위트를 단순히 "비추천"으로 표시했지만 제거하지는 않았다. 이 결정이 15년 후 FREAK의 공격 경로가 됐다.

발표 당시 상위 100만 HTTPS 서버의 36.7%가 RSA_EXPORT를 허용했고, Apple 기기 전체(iOS·macOS)와 OpenSSL 기반 Android가 클라이언트 측 버그로 인해 즉시 취약한 상태였다.

📢 **섹션 요약 비유**: 해외에 파는 금고는 "수출용이니 3자리 비밀번호로 해주세요"라는 규제가 있었는데, 국내용 금고에도 그 3자리 비밀번호 잠금장치가 뒷면에 그대로 붙어 있었다. 도둑이 뒷면을 발견하자마자 모든 금고를 3자리로 열 수 있었다.

---

## 2. 구성요소

### RSA 팩토링 공격 원리

RSA는 두 큰 소수 p, q의 곱 n = p×q의 인수분해 어려움에 의존한다. 512비트 RSA에서 n은 약 155자리 10진수이며, GNFS(General Number Field Sieve) 알고리즘과 현대 클라우드 자원으로 **7.5시간, 비용 약 $100** 만에 분해할 수 있다.

```
RSA_EXPORT 공격 흐름:

[1단계] 다운그레이드 강제
클라이언트           공격자 (MITM)         서버
    │                    │                   │
    │─ ClientHello ───────────────────────▶  │
    │  (RSA + DHE 등 포함)                   │
    │      [ServerHello 변조]                │
    │◀─ ServerHello (RSA_EXPORT 512비트) ────┤
    │◀─ ServerKeyExchange (512비트 RSA 임시키)│
    │                                        │
[2단계] 클라이언트 버그
    클라이언트 라이브러리가 서버 요청대로
    512비트 RSA_EXPORT 수락 (패치 전 버그)

[3단계] 팩토링
    공격자: 512비트 RSA 임시 공개키 캡처
    → GNFS로 p, q 인수분해 → 개인 키 복원
    → 소요 시간: 약 7.5시간 / 비용: ~$100

[4단계] 세션 복호화
    복원된 개인 키로 PreMasterSecret 복호화
    → 모든 TLS 레코드 복호화
```

### 취약 컴포넌트

| 컴포넌트 | 취약 버전 | CVE |
|:---|:---|:---|
| OpenSSL | 1.0.1k 이전 | CVE-2015-0204 |
| Apple SecureTransport | iOS 8.1 미만, macOS 10.10 미만 | CVE-2015-1067 |
| NSS (Network Security Services) | 일부 버전 | CVE-2015-0205 |
| Microsoft SChannel | Windows 서버 일부 | CVE-2015-1637 |

```
클라이언트 버그 (패치 전):
서버가 RSA_EXPORT를 요청하면 클라이언트가
"내가 지원한다고 광고하지 않았어도" 수락함

→ ClientHello에 RSA_EXPORT를 포함하지 않았어도
  서버의 강요에 응하는 구현 오류
```

📢 **섹션 요약 비유**: 방문객이 "저는 3자리 비밀번호 자물쇠는 사용 안 합니다"라고 이미 선언했는데, 관리인이 억지로 3자리 자물쇠를 달아두고 "이걸 써주세요"라고 하면, 방문객이 그냥 따르는 버그가 클라이언트 측 결함이다.

---

## 3. 구조 및 동작 원리

### EXPORT 계열 취약점 비교

| 항목 | FREAK | Logjam |
|:---|:---|:---|
| 약화된 알고리즘 | RSA_EXPORT (512비트) | DHE_EXPORT (512비트 DH) |
| 크래킹 방법 | RSA 팩토링 (GNFS) | 이산 로그 사전 계산 (SNFS) |
| 클라이언트 버그 | ✅ 있음 (수락 버그) | ❌ 없음 (프로토콜 수준) |
| 크래킹 시간 | ~7.5시간 (단일 세션) | 사전 계산 후 수 분 |
| 사전 계산 | ❌ 불필요 | ✅ 필요 |
| 영향 범위 | 클라이언트 라이브러리 의존 | 서버 DH 파라미터 의존 |
| 방어 | RSA_EXPORT 비활성화 + 라이브러리 패치 | DHE_EXPORT 비활성화 + 2048비트 DH |

📢 **섹션 요약 비유**: FREAK와 Logjam은 같은 수출 규제법으로 만들어진 두 자물쇠의 약점이다. FREAK는 자물쇠 번호 자체를 추측하고(팩토링), Logjam은 자물쇠 설계 도면을 미리 외워두는(사전 계산) 방식의 차이가 있다.

---

## 4. 비교 및 트레이드오프

**서버 측 방어**

```nginx
# nginx - EXPORT 암호 스위트 명시적 제외
ssl_ciphers 'HIGH:!EXPORT:!NULL:!eNULL:!aNULL:!RC4:!DES:!3DES:!MD5:!PSK';
ssl_protocols TLSv1.2 TLSv1.3;
```

```apache
# Apache
SSLCipherSuite HIGH:!EXPORT:!NULL:!eNULL:!aNULL:!RC4:!MD5
SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
```

**클라이언트 측 방어**

- OpenSSL 1.0.1k 이상으로 업그레이드
- Apple 보안 패치 적용 (iOS 8.2+, macOS 10.10.2+)
- Android: Google Play Services 업데이트

**취약점 스캔**

```bash
# openssl로 서버의 EXPORT 지원 여부 확인
openssl s_client -connect example.com:443 -cipher EXPORT 2>&1 | grep -E "Cipher|Alert"
# "handshake failure" → 안전, "Cipher is ..." → 취약
```

**기술사 논술 포인트**: FREAK 분석 시 ① 미국 수출 규제 배경(정책), ② RSA 512비트 팩토링 가능성(기술), ③ 클라이언트 버그 + 서버 EXPORT 활성화 조합(공격 조건), ④ EXPORT 비활성화 + 라이브러리 패치(방어) 순으로 4단계 구성을 권장한다.

📢 **섹션 요약 비유**: 자동차 회사가 "해외용에만 약한 에어백을 넣었는데, 국내용에도 같은 에어백이 숨어 있었다"는 리콜 상황이다. 에어백을 완전히 제거하거나(EXPORT 비활성화), 강한 에어백으로 교체하는(최신 라이브러리 패치) 것이 해결책이다.

---

## 5. 실무 적용 및 최적화 기법

FREAK는 보안 정책이 기술적 레거시로 변환되는 과정의 전형적인 사례다. 1990년대 규제 목적의 "의도적 약화"가 규제 해제 후에도 코드베이스에 잔류하여 취약점으로 부활했다. 이는 정책 변경 시 해당 정책을 구현한 **모든 코드를 함께 정리해야 한다**는 교훈을 준다.

또한 클라이언트 라이브러리의 버그(협상 안 된 암호 스위트 수락)가 없었다면 공격이 훨씬 어려웠을 것이다. 이는 방어 심층화(Defense in Depth) 원칙에서 클라이언트와 서버 양측 모두를 강화해야 한다는 근거가 된다.

TLS 1.3은 EXPORT 암호 스위트 자체를 프로토콜 명세에서 삭제했으므로, TLS 1.3 전용 환경에서 FREAK는 불가능하다.

📢 **섹션 요약 비유**: 법이 바뀌어 "3자리 비밀번호 금지"가 해제됐는데, 창고 뒤편에 여전히 3자리 자물쇠가 달린 쪽문이 있었다. 법 담당자는 규제를 해제했지만, 창고 관리인은 그 쪽문을 잊고 있었다. FREAK는 그 잊혀진 쪽문 이야기다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| RSA_EXPORT | 취약 암호 스위트 | 512비트 RSA, 수출 규제 레거시 |
| GNFS (General Number Field Sieve) | 공격 알고리즘 | 512비트 RSA 팩토링 |
| EAR (Export Administration Regulations) | 역사적 원인 | 미국 암호 수출 규제 |
| Logjam | 유사 취약점 | DHE_EXPORT DH 다운그레이드 |
| DROWN | 유사 취약점 | SSLv2 RSA 크로스 프로토콜 |
| TLS_FALLBACK_SCSV | 다운그레이드 방어 | 폴백 시도 탐지 |
| Defense in Depth | 방어 원칙 | 클라이언트·서버 양측 강화 필요 |

### 👶 어린이를 위한 3줄 비유 설명

1. FREAK는 "해외에 파는 자물쇠는 쉽게 열려야 한다"는 오래된 법 때문에 만들어진 약한 자물쇠가 국내 금고에도 숨어 있었던 이야기예요.
2. 도둑이 그 숨겨진 약한 자물쇠를 강제로 사용하게 만든 뒤, 7.5시간 만에 비밀번호를 맞춰서 금고를 열었어요.
3. 해결책은 그 낡은 자물쇠를 완전히 없애거나(EXPORT 비활성화), 새 자물쇠를 제대로 설치하는(라이브러리 패치) 거예요.
