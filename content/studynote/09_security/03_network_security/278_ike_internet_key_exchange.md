+++
weight = 278
title = "278. IKE (Internet Key Exchange)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: IKE (Internet Key Exchange)는 IPsec SA (Security Association)를 자동으로 협상·생성·갱신·삭제하는 프로토콜로, ISAKMP (Internet Security Association and Key Management Protocol) 프레임워크 위에서 동작한다.
> 2. **가치**: 수동으로 SA를 관리(Manual Keying)하면 키가 정적으로 고정돼 탈취 시 복구가 불가능하지만, IKE는 DH (Diffie-Hellman) 키 교환으로 동적 세션 키를 생성하고 주기적으로 재협상해 PFS (Perfect Forward Secrecy)를 실현한다.
> 3. **판단 포인트**: IKEv1의 Phase 1/Phase 2 구조와 IKEv2의 단순화된 교환 구조(IKE_SA_INIT + IKE_AUTH)를 구별하고, 각각의 취약점과 개선 사항을 설명해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

IPsec이 보안 통신을 제공하려면 두 피어 간에 "어떤 알고리즘과 키를 사용할 것인가"를 사전에 합의해야 한다. 이 합의의 결과물이 SA (Security Association)이며, SA를 수동으로 생성하는 것은 규모에 맞지 않는다. 수천 개의 VPN 터널을 가진 기업에서 모든 SA를 수동 관리하는 것은 실질적으로 불가능하다.

IKE는 이 문제를 해결하는 자동화된 SA 협상 프로토콜이다. RFC 2409(IKEv1)과 RFC 7296(IKEv2)으로 표준화됐으며, UDP 포트 500(기본), 4500(NAT-T)에서 동작한다.

IKE의 핵심 기능:
1. **상호 인증(Mutual Authentication)**: 두 피어가 서로를 검증 (PSK, 인증서, EAP 방식)
2. **키 교환(Key Exchange)**: DH를 통한 세션 키 생성, 비밀키를 전송하지 않음
3. **SA 협상(SA Negotiation)**: 암호 알고리즘, 해시 함수, DH 그룹 합의
4. **SA 갱신(SA Renewal)**: 수명 만료 전 자동 재협상

ISAKMP는 SA 관리의 일반적 프레임워크(구문, 상태, 프로토콜 구조)를 정의하고, IKE는 그 위에서 실제 키 교환 메커니즘(DH, 인증 방식)을 구현한다.

📢 **섹션 요약 비유**: IKE는 두 은행 지점이 매일 아침 당일 암호 규칙을 자동으로 교환하는 시스템이다. 사람이 직접 전화로 "오늘은 이 키 쓰세요"라고 할 필요가 없다.

---

## 2. 구성요소

### IKEv1 vs IKEv2 구조 비교

```
[IKEv1 구조]
┌────────────────────────────────────┐
│  Phase 1: IKE SA 협상              │
│  (ISAKMP SA 수립)                  │
│  Main Mode: 6 메시지               │
│  Aggressive Mode: 3 메시지         │
│  결과: IKE SA (양방향 보안 채널)   │
└────────────────┬───────────────────┘
                 │
┌────────────────▼───────────────────┐
│  Phase 2: IPsec SA 협상            │
│  Quick Mode: 3 메시지              │
│  결과: IPsec SA 쌍 (AH 또는 ESP)  │
│  (단방향 × 2)                      │
└────────────────────────────────────┘
총 메시지 수: 9개 (Main) 또는 6개 (Aggressive)

[IKEv2 구조]
┌────────────────────────────────────┐
│  IKE_SA_INIT (2 메시지 왕복)       │
│  DH 교환, 넌스, 알고리즘 협상      │
├────────────────────────────────────┤
│  IKE_AUTH (2 메시지 왕복)          │
│  신원 인증, 첫 번째 Child SA 수립  │
└────────────────────────────────────┘
총 메시지 수: 4개 (기본 케이스)
추가 Child SA: CREATE_CHILD_SA 교환
```

### IKEv1 vs IKEv2 핵심 비교

| 특성 | IKEv1 | IKEv2 |
|:---|:---|:---|
| **표준** | RFC 2409 (1998) | RFC 7296 (2014) |
| **메시지 수** | 9개 (Main Mode) | 4개 (기본) |
| **NAT-T** | 별도 확장 (RFC 3947) | 기본 내장 |
| **EAP 지원** | 제한적 | 기본 내장 |
| **DoS 방지** | 없음 | Cookie 챌린지 |
| **MOBIKE** | 없음 | RFC 4555 기본 |
| **재키잉** | 복잡 | 단순화 |
| **에러 처리** | 불명확 | 명확한 응답 코드 |
| **현황** | 레거시 | 권장 표준 |

📢 **섹션 요약 비유**: IKEv1은 9단계 절차서가 필요한 협약서이고, IKEv2는 전자서명 4단계로 완성되는 디지털 계약이다. 같은 목적이지만 훨씬 효율적이다.

---

## 3. 구조 및 동작 원리

### IKE DH (Diffie-Hellman) 키 교환 원리

```
피어 A                           피어 B
   │                                │
   │  공개 파라미터 합의            │
   │  (g: 생성원, p: 소수)          │
   │                                │
   │  a (비밀수) 생성               │  b (비밀수) 생성
   │  A = g^a mod p                 │  B = g^b mod p
   │                                │
   │─── A 전송 ────────────────────►│
   │◄── B 전송 ─────────────────────│
   │                                │
   │  K = B^a mod p                 │  K = A^b mod p
   │  = (g^b)^a mod p               │  = (g^a)^b mod p
   │  = g^(ab) mod p  ←──── 동일 ──│  = g^(ab) mod p
   │                                │
   │     K: 공유 비밀 (전송 안됨)   │
```

DH의 핵심: a, b는 절대 전송되지 않는다. K를 계산하는 데 a, b 없이는 이산로그 문제를 풀어야 하므로 계산적으로 불가능하다.

### IKE 인증 방식 비교

| 방식 | 설명 | 적합 시나리오 |
|:---|:---|:---|
| PSK (Pre-Shared Key) | 사전 공유 비밀키 | 소규모, 단순 설정 |
| RSA 서명 | X.509 인증서 서명 | 대규모 PKI 환경 |
| ECDSA | 타원곡선 디지털 서명 | 고성능, 모바일 |
| EAP (Extensible Authentication Protocol) | 외부 인증 서버 위임 | RADIUS, 기업 원격접속 |
| EAP-TLS | 인증서 기반 EAP | 최고 보안 수준 |

📢 **섹션 요약 비유**: DH 키 교환은 두 사람이 공개 장소에서 각자 물감을 섞는 것이다. 개별 물감 비율(a, b)을 알지 못하면 최종 색상(K)을 재현할 수 없다.

---

## 4. 비교 및 트레이드오프

**IKEv2 설정 예시 (strongSwan)**

```
# ike 파라미터: aes256-sha256-ecp256
# 해석: AES-256-CBC + HMAC-SHA-256 + ECDH P-256
#
# esp 파라미터: aes256gcm16
# 해석: AES-256-GCM (AEAD, 16바이트 ICV)
#
# keyingtries=%forever   : SA 협상 재시도 무한
# dpdaction=restart      : Dead Peer Detection 후 자동 재연결
# closeaction=restart    : 연결 종료 시 자동 재시작

conn vpn-to-aws
    keyexchange=ikev2
    ike=aes256-sha256-ecp256!
    esp=aes256gcm16!
    left=203.0.113.1
    leftid=@hq.example.com
    leftcert=hq-cert.pem
    right=52.x.x.x
    rightid=@aws.example.com
    rightca=rootca.pem
    auto=start
    dpddelay=30s
    dpdtimeout=120s
    dpdaction=restart
```

**IKEv2 MOBIKE (RFC 4555)**:
- 모바일 디바이스의 IP 주소 변경(Wi-Fi ↔ LTE) 시 VPN 터널을 재설정 없이 유지
- 디바이스가 새 IP를 서버에 알리고, SA는 유지된 채 주소만 업데이트
- iOS, Android VPN 클라이언트에서 기본 활성화

**PFS 설정 중요성**: `keyingtries`와 `rekey` 설정을 통해 주기적으로 새 DH 키 교환을 수행하면, 과거 세션 키가 탈취되더라도 현재 세션은 안전하다.

📢 **섹션 요약 비유**: IKEv2는 매 통화마다 자동으로 암호 코드를 바꾸는 군용 무전기와 같다. 한 번 코드가 노출돼도 다음 통화는 이미 새 코드로 바뀌어 있다(PFS).

---

## 5. 실무 적용 및 최적화 기법

IKE는 IPsec 생태계를 실용적으로 만든 핵심 컴포넌트다. IKEv2로의 전환은 메시지 수 감소, NAT 내장 지원, EAP 통합, 강화된 DoS 방지 등 운영 편의성과 보안성을 동시에 개선했다. 현재 대부분의 기업 VPN, 클라우드 VPN 서비스가 IKEv2를 기본값으로 채택한다.

앞으로의 방향은 포스트-양자 암호(PQC, Post-Quantum Cryptography) 통합이다. IKEv2의 모듈화 설계는 기존 DH를 ML-KEM (Module Lattice Key Encapsulation Mechanism) 등 양자 내성 알고리즘으로 교체하거나 조합(Hybrid KEM)하는 것을 비교적 용이하게 한다.

📢 **섹션 요약 비유**: IKE는 VPN의 "자동 열쇠 교환 로봇"이다. 사람이 일일이 열쇠를 전달하지 않아도, 두 건물의 로봇이 매일 아침 새 열쇠를 스스로 만들고 교환한다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| ISAKMP | 기반 프레임워크 | IKE가 구현하는 SA 관리 구조 |
| SA (Security Association) | 결과물 | IKE 협상의 최종 산출물 |
| DH (Diffie-Hellman) | 핵심 기술 | 비밀 전송 없는 공유 키 생성 |
| PFS (Perfect Forward Secrecy) | 보안 속성 | 세션마다 새 DH 키 교환 |
| IKEv1 | 이전 버전 | Phase 1/2, 취약점 있음 |
| MOBIKE | IKEv2 확장 | 모바일 IP 변경 시 터널 유지 |

### 👶 어린이를 위한 3줄 비유 설명
IKE는 두 친구가 처음 만날 때 서로 비밀 암호를 정하는 방법인데, 암호 자체는 인터넷에 보내지 않아요!
대신 각자 숫자를 계산해서 똑같은 결론에 도달해요 (마법 같은 수학!).
그리고 주기적으로 새 암호로 바꿔서, 예전 암호가 노출돼도 지금 대화는 안전해요 (PFS).
