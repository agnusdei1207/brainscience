+++
title = "SYN 플러딩 (SYN Flood)"
weight = 255
date = "2024-03-21"
[extra]
categories = ["Security", "Network"]
+++
## 0. 핵심 인사이트

>|                        |---SYN--->| (Half-Open)

> 📝 모범 답안

- **TCP 3-Way Handshake 취약점 악용**: 클라이언트가 SYN 패킷을 보낸 후 서버의 SYN-ACK에 응답하지 않아 서버의 백로그 큐(Backlog Queue)를 반열림(Half-Open) 상태로 가득 채우는 공격임.
- **가용성 저하 및 서비스 거부**: 서버가 새로운 연결 요청을 수락하지 못하게 함으로써 정상적인 사용자의 접속을 차단하는 대표적인 L4 프로토콜 수준의 DDoS 공격임.
- **하이브리드 대응 체계**: TCP 스택 최적화(Timeout 단축)와 더불어 SYN Cookie, 임계치 기반 차단 등 하드웨어 장비 및 OS 레벨의 병행 대응이 필수적임.

### 1. 개요 및 필요성
- **정의**: TCP 연결 설정 과정 중 3-way handshake의 약점을 이용하여 서버 자원을 고갈시키는 공격임.
- **공격 원리**: 공격자는 IP 주소를 위조(Spoofing)하여 대량의 SYN 패킷을 전송함. 서버는 존재하지 않는 IP로 SYN-ACK를 보내고 ACK를 기다리며 TCB(Transmission Control Block)를 점유함.
- **위협 수준**: 소량의 트래픽으로도 서버 전체를 마비시킬 수 있어 저비용 고효율 공격으로 간주됨.

### 2. 구성요소
```text
[ Normal TCP Handshake ]          [ SYN Flood Attack ]
   Client      Server                 Attacker      Server
     |---SYN---     |<--SYN/ACK|                        |---SYN--->| (Half-Open)
     |---ACK--->| (Established)          |---SYN--->| (Half-Open)
                                         |   ...    | [ Queue Full ]
                                         X (No ACK) X (Wait...)

[ SYN Cookie Mechanism ]
1. Server receives SYN.
2. Instead of allocating TCB, server generates a 'Cookie' (Sequence Number).
3. Server sends SYN-ACK with this Cookie.
4. Server only allocates resources IF it receives an ACK with valid Cookie.
```
- **백로그 큐(Backlog Queue)**: 연결이 완전히 수립되기 전의 상태를 저장하는 메모리 공간으로, 크기가 제한되어 있어 공격에 취약함.
- **SYN Cookie**: 서버의 상태를 저장하지 않고 일정한 규칙으로 생성된 시퀀스 번호를 활용하여 유효한 연결만 수락하는 방어 기법임.
- **TCP 정렬(TCP Intercept)**: 방화벽이나 IPS가 서버 대신 Handshake를 대행하여 검증된 세션만 서버로 넘기는 프록시 방식임.

### 3. 구조 및 동작 원리

| 구분 | SYN Flood | UDP Flood | HTTP Flood (L7) |
| :--- | :--- | :--- | :--- |
| **공격 대상** | TCP 연결 테이블 (TCB) | 네트워크 대역폭 | 서버 로직/DB 자원 |
| **주요 기법** | Half-Open 세션 생성 | 대량 UDP 패킷 전송 | 정상 GET/POST 요청 |
| **방어 난이도** | 중간 (SYN Cookie로 대응 가능) | 낮음 (ACL/Rate Limit) | 높음 (정상/악성 구분 난해) |
| **탐지 지표** | SYN_RECV 상태 급증 | bps/pps 급증 | RPS(Request Per Second) 급증 |

### 4. 비교 및 트레이드오프
- **OS 커널 튜닝**: `tcp_max_syn_backlog` 크기를 상향하고 `tcp_synack_retries` 횟수를 줄여 Half-Open 세션의 유지 시간을 최소화해야 함.
- **전용 보안 장비**: 대규모 공격 상황에서는 OS 레벨의 대응에 한계가 있으므로, 가속 칩(ASIC/FPGA)이 탑재된 DDoS 전용 방어 장비를 전단에 배치해야 함.
- **기술사적 판단**: 단순 차단은 위조된 IP에 의한 오차단 위험이 있으므로, First SYN에 대해 Drop 후 재전송을 유도하는 'Anti-Spoofing' 기술을 우선 적용해야 함.

### 5. 실무 적용 및 최적화 기법
- **차세대 방어 기술**: 머신러닝을 활용하여 트래픽 패턴을 학습하고, 공격자의 평판 점수(Reputation)를 기반으로 동적 차단 정책을 적용하는 방향으로 발전 중임.
- **표준 가이드**: KISA 및 NIST의 DDoS 대응 가이드라인을 준수하여 정기적인 모의 훈련과 대응 절차 숙달이 필요함.
- **결론**: SYN Flood는 고전적이지만 여전히 강력한 위협임. 시스템 가용성을 보장하기 위해 네트워크 인프라와 OS 스택 전반에 걸친 심층 방어(Defense in Depth)가 필수적임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **3-Way Handshake**: 공격의 기술적 기반
- **SYN Cookie**: 핵심 방어 기술
- **IP Spoofing**: 공격의 은닉 수단
- **Backlog Queue**: 자원 고갈 지점

### 👶 어린이를 위한 3줄 비유 설명
1. 장난꾸러기 친구가 피자가게에 전화를 걸어 "피자 100판 배달해 주세요!" 하고는 전화를 끊어버려요.
2. 피자가게 아저씨는 주소를 확인하려고 전화를 기다리느라 다른 진짜 주문 전화를 못 받게 돼요.
3. 이럴 땐 주문을 받을 때 진짜 손님인지 먼저 확인하는 규칙을 정해서 해결한답니다!
