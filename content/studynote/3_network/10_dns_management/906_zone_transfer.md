+++
weight = 2
title = "DNS zone transfer와 DNSSEC"
description = "DNS 존 간의 영역 전송과 DNSSEC의 디지털 서명을 통한 응답 무결성 보장을 다룬다."
date = 2024-02-02

[extra]
categories = ["studynote-software-engineering"]
topics = ["dns", "zone-transfer", "dnssec", "axfr"]
study_section = ["section-10-dns-management"]

number = "906"
core_insight = "DNS zone transfer는 Primary DNS와 Secondary DNS 사이에서 존 파일을 동기화하는 메커니즘이며, DNSSEC는 DNS 응답에 디지털 서명을附加하여 응답의 출처와 무결성을 검증할 수 있게 한다."
key_points = ["Zone transfer (AXFR, IXFR)", "Primary/Secondary DNS 구성", "DNSSEC 디지털 서명 (RRSIG)", "DS 레코드와 사슬 검증"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: DNS zone transfer는 Primary DNS 서버의 존 파일을 Secondary DNS 서버에 동기화하는 메커니즘으로, DNS 서비스의 이중화와可用성을 높인다.
> 2. **가치**: 단일 DNS 서버 장애 시에도 도메인 이름解決이 계속 가능하며, DNSSEC는 DNS 응답의 위조를 방지하여 보안성을 강화한다.
> 3. **융합**: DNSSEC는 DNS 응답에 cryptographic 서명을附加하여, Cache Poisoning, Spoofing 공격을 효과적으로 방어한다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

**개念**: DNS zone transfer는 하나의 DNS 존(Zone)을管理하는 Primary (Master) DNS 서버와 그レコードを복제하는 Secondary (Slave) DNS 서버 사이의 동기화 메커니즘이다. AXFR(동일 계수 전송), IXFR(증분 전송) 등의 프로토콜이 사용되며, TCP 포트 53에서 동작한다. DNSSEC(DNS Security Extensions)는 RFC 4033~4035로 표준화된 확장 기능으로, DNS 응답에 디지털 서명을附加하여 출처 인증과 무결성 검증을 가능하게 한다.

**필요성**: DNS 서버가 하나뿐이라면, 해당 서버 장애 시internet에서 해당 도메인에 접근할 수 없게 된다. 따라서権威 DNS 서버는 Primary-Secondary 구조로 이중화되어 있으며, Primary의 변경 사항이 Secondary에 자동으로 반영되어야 한다. 또한 DNS는 spoofing/poisoning 공격의 대상이 될 수 있어, 응답의 진위를 검증할 수 있는 메커니즘이 필요하다.

**비유**: DNS zone transfer는 **본사와 지사 사이의 문서同步**과 같다. 본사(Primary DNS)에 문서가新增되면, 변경 사항을 지사(Secondary DNS)에 전송하여 동일한 사본을 유지한다. 그래야 본사가 없어도 지사에서文書を 조회할 수 있다. DNSSEC는これらの文書에「공인 인증서 의한 도장」を押して, 위조되지 않았음을証明하는 것과 같다.

**등장 배경**: DNS zone transfer는 원래 BootP의 확장 형태로1986년경 도입되었으며, DNSSEC는2005년 RFC 4033~4035로 표준화되었다. 그러나 DNSSEC의 실제 채택은 느리게 진행되었으며, 2010년대부터 점차 확대되기 시작했다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### DNS Zone Transfer (AXFR/IXFR)

```
┌───────────────────────────────────────────────────────────────────────┐
│                    DNS Zone Transfer 과정                                 │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  【Primary/Secondary DNS架构】                                          │
│                                                                       │
│       [Domain Owner]                                                  │
│              │                                                        │
│              │ Zone 데이터 관리                                         │
│              ▼                                                        │
│  ┌───────────────────┐                                                │
│  │  Primary DNS       │                                                │
│  │  (Master DNS)     │ TCP 53                                         │
│  │  ns1.example.com  │◀────────────┐                                  │
│  └───────┬───────────┘             │                                  │
│          │                           │ AXFR/IXFR                      │
│          │                           │                                  │
│          │                           ▼                                  │
│  ┌───────┴───────────┐                                                │
│  │  Secondary DNS     │                                                │
│  │  (Slave DNS)      │                                                │
│  │  ns2.example.com  │                                                │
│  └───────────────────┘                                                │
│                                                                       │
│  【AXFR (All Zone Transfer)】                                          │
│  • 존 전체를 처음부터 끝까지 전송                                        │
│  • 존 크기가 클수록 네트워크 부하 큼                                     │
│  • TCP 포트 53 사용                                                    │
│                                                                       │
│  ① Secondary가 SOA 레코드의 Serial 확인                                 │
│  ② Serial이 크면 → AXFR 요청                                           │
│  ③ Primary가 존 전체를 순차적으로 전송                                    │
│  ④ Secondary가 존 파일 교체                                             │
│                                                                       │
│  【IXFR (Incremental Zone Transfer)】                                  │
│  • 변경된 부분만 전송 (증분)                                            │
│  • SOA Serial, SOA 레코드たちの IXQR를 활용                             │
│  • AXFR보다 네트워크 부하 적음                                          │
│                                                                       │
│  SOA 레코드 (Serial):                                                  │
│  • 형식: YYYYMMDDNN (날짜 + 버전)                                      │
│  • 예: 2024011501 → 2024년 1월 15일 첫 번째 업데이트                   │
│  • Secondary는 정기적으로(Refresh 시간) Primary의 SOA 확인             │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Zone transfer의 핵심은 SOA(Start of Authority) 레코드의 Serial 번호이다. Primary의 존 파일이更新되면 Serial이 증가하며, Secondary는 정기적으로(Refresh 시간, 일반적으로 수시간~수일) Primary에 SOA를 질의하여 Serial이 증가했는지 확인한다. 증가했으면 AXFR 또는 IXFR을 요청하여 변경 사항을 동기화한다. AXFR은 항상 존 전체를 전송하므로 네트워크 비용이 크지만, IXFR은 변경된 부분만 전송하여 효율적이다. 그러나 IXFR을지원하지 않는 DNS 서버도 있으므로, AXFR이더普遍적으로使用된다.

### DNSSEC (DNS Security Extensions)

DNSSEC는 DNS 응답에 디지털 서명을附加하여 응답의 출처(누가 보냈는가)와 무결성(이进程中 변경되지 않았는가)을 검증한다.

```
┌───────────────────────────────────────────────────────────────────────┐
│                    DNSSEC 디지털 서명 과정                              │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  【서명 과정 (Primary DNS에서)】                                        │
│                                                                       │
│  ① DNS 레코드 생성                                                     │
│     example.com.  IN  A     93.184.216.34                            │
│                                                                       │
│  ② KSK(Zone Signing Key)로 RRSET(레코드 집합)에 서명                  │
│     → RRSIG (Resource Record Signature) 생성                          │
│     example.com.  IN  RRSIG  A 5 3 86400 ... (서명)                  │
│                                                                       │
│  ③ ZSK(Zone Signing Key)로 KSK에 서명                                  │
│     → DNSKEY 레코드 (公开키)                                            │
│                                                                       │
│  ④ Trust Anchor (루트 DNSKEY)를 루트 DNS에 배포                        │
│                                                                       │
│  【검증 과정 (Resolver에서)】                                           │
│                                                                       │
│  ① DNS 응답 + RRSIG 수신                                               │
│  ② DNSKEY (공개키)를 사용하여 RRSIG 검증                               │
│  ③ Chain of Trust 검증:                                               │
│     • 도메인 DNSKEY → TLD DNSKEY → Root DNSKEY                        │
│     • 각 단계에서 상위 키로 서명 검증                                   │
│     • Root DNSKEY는 Trust Anchor에 사전 등록                           │
│                                                                       │
│  ④ 검증 성공 → 응답이 진본 + 무결함                                      │
│  ④ 검증 실패 → 응답 폐기 (보안 문제로 처리)                              │
│                                                                       │
│  DNSSEC 레코드 유형:                                                   │
│  • RRSIG: DNS 레코드 집합의 디지털 서명                                 │
│  • DNSKEY: 공개키 (KSK, Zone Signing Key)                             │
│  • DS: Delegation Signer - 상위 존에 등록된 하위 존의 키 해시           │
│  • NSEC/NSEC3: 다음에 존재하는 레코드 목록 (否定検索結果)               │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** DNSSEC의 핵심 개념은「사슬 모양 신뢰(Chain of Trust)」이다. 각 존의 DNSKEY는 상위 존(예: .com)에 DS 레코드로 등록되어 있다. .com의 DNSKEY는 다시 상위(root)에 DS로 등록되어 있다. Root는 Trust Anchor(사전に登録된ルートDNSKEY)로 신뢰할 수 있다. 따라서example.com의 DNS 응답을 검증하려면, example.com → .com → Root 순서로 Chain을따라 검증해야 한다. 만약 하나라도 검증에 실패하면, 해당 응답은信頼할 수 없다.

### DS 레코드와 위임 검증

```
┌───────────────────────────────────────────────────────────────────────┐
│                    DS 레코드와 위임 검증                                 │
├───────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  【DS 레코드 구조】                                                     │
│                                                                       │
│  example.com의 DNSKEY 해시를 상위 도메인(.com)에 DS로 등록             │
│  example.com.  IN  DS  12345 8 1 ABCDEF...                            │
│                     │    │   │   └─ DNSKEY 해시 (SHA-1)              │
│                     │    │   └─────── DNSKEY 해시 알고리즘           │
│                     │    └──────────── 키 태그 (Key Tag)               │
│                     └──────────────── 키 식별자                          │
│                                                                       │
│  【Chain of Trust 검증】                                               │
│                                                                       │
│  [Root DNSKEY]                                                        │
│       │ 서명                                                          │
│       ▼                                                              │
│  [.com DNSKEY]                                                        │
│       │ 서명                                                          │
│       ▼                                                              │
│  [example.com DNSKEY + RRSIG]                                         │
│       │ 서명                                                          │
│       ▼                                                              │
│  [example.com A 레코드 + RRSIG] ←── 최종 검증 대상                      │
│                                                                       │
│  검증 과정:                                                            │
│  1. example.com의 A 레코드와 RRSIG 수신                               │
│  2. example.com의 DNSKEY로 RRSIG 검증 (내 부서 도장 확인)              │
│  3. example.com의 DNSKEY의 부모(.com)에 DS 레코드 확인                 │
│  4. .com의 DNSKEY로 example.com DNSKEY의 서명 검증 (상관 도장 확인)    │
│  5. .com의 DNSKEY의 부모(Root)에 DS 레코드 확인                        │
│  6. Root DNSKEY로 .com DNSKEY의 서명 검증                              │
│  7. Root DNSKEY는 Trust Anchor로 신뢰                                 │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### DNSSEC 적용 전후 비교

| 항목 | DNSSEC 미적용 | DNSSEC 적용 |
|:---|:---|:---|
| **응답 출처** | 검증 불가 | 상위 도메인 사슬로 검증 |
| **응답 무결성** | 검증 불가 | RRSIG 서명으로 보장 |
| **Cache Poisoning** | 위험 | 효과적 방어 |
| **암호화** | 없음 (단순히 서명) | 없음 (기밀성 없음) |
| **현재 채택률** | 대부분 적용 | 점차 증가中 (루트+ 일부 TLD) |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

**시나리오 1 — DNSSEC 적용**: 도메인 Registrar(Korean Registrar 등)에서 DNSSEC를 활성화하면, Registrar가 자동으로 DS 레코드를 TLD Registry(.com의 경우 Verisign)에 등록한다. DNS Hosting provider(예: AWS Route 53)에서 KSK/ZSK를 자동 생성/관리하고, DNS 레코드에 RRSIG 서명을附加한다. Validator(Resolver)는Chain of Trust를 통해 응답의 진위를 검증한다.

**시나리오 2 — Zone Transfer 보안**: Zone transfer는 아무나 시도할 수 없도록 ACL(Access Control List)으로 제한해야 한다. Secondary DNS의IP만 허용하고, TSIG(Transaction Signature)을 활용하여인증된 서버만 전송할 수 있게 해야 한다. 그래야不正な zone transfer를 방지할 수 있다.

### 도입 체크리스트

- **기술적**: DNSSEC 활성화 전, DNS 서비스 업체 지원 확인, 키 관리 정책 수립
- **운영·보안적**: KSK Rollover 계획 수립, DS 레코드 관리, DNSSEC 검증 모니터링

### 안티패턴

- **DNSSEC 키 관리不善**: KSK/ZSK를 정기적으로 순환하지 않으면 보안이 약화된다.
- **DS 레코드 실수**: DS 레코드가 잘못되면 도메인 전체가 검증 실패하여internet에서 조회 불가해진다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망

DNSSEC의 채택은 점차 확대되고 있다. 2010년 루트 존에 DNSSEC가 적용되었으며, 주요 TLD(.com, .net 등)도 적용되었다. 그러나 모든 도메인registrar가 DNSSEC를サポート하지는 않으며, 설정의 복잡성도普及を妨碍している。 향후는自动化された DNSSEC 管理와 함께, DNS security의 标准이 될 것으로 예상된다.

### 참고 표준

- RFC 1995 — Incremental Zone Transfer (IXFR)
- RFC 1996 — A Mechanism for Prompt Zone Transfer (AXFR)
- RFC 4033 — DNS Security Introduction and Requirements
- RFC 4035 — Protocol Modifications for DNS Security Extensions

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **AXFR** | 존 전체를 전송하는 zone transfer 방식으로, TCP 포트 53을 사용한다. |
| **IXFR** | 변경된 부분만 전송하는 증분 zone transfer 방식이다. |
| **RRSIG** | DNS 레코드 집합에 대한 DNSSEC 디지털 서명이다. |
| **DS 레코드** | 상위 도메인에 등록된 하위 도메인의 DNSKEY 해시로, Chain of Trust의 핵심이다. |
| **KSK/ZSK** | DNSSEC에서 사용하는 두 종류의 키로, KSK는 존의 키를 서명하고, ZSK는 레코드를 서명한다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. DNS 존 전송은 **母公司에서 지사에 매일早上문서를fax로 보내는 것**과 같아요.母公司에 새 문서가 오면 지사로fax로 보내서,母公司가 없어도 지사에서 필요한文書を 찾을 수 있어요.
2. DNSSEC는 **重要 문서에 인증 도장을** 누르는 것과 같아요.母公司가文서에「공인 인증 Bureau 도장」을 찍어서,「이 문서는真正이다」고証明하는 거예요.
3. 그래야!**なりすましが「내 도메인이다」と 提出물을 바꿔도, 도장을 검증하면「위조犯이었다」는 걸 바로 알 수 있어요!
