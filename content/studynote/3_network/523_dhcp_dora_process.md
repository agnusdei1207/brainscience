+++
title = "523. DHCP 과정 4단계 (DORA)"
weight = 523
+++
# 523. DHCP 과정 4단계 (DORA)

> **핵심 인사이트**: IP 주소가 없는 폰이 어떻게 서버를 찾아서 IP를 받아올까? 그 과정은 'DORA'라는 4단계의 깔끔한 대화로 이루어진다. "누구 IP 줄 사람?"(D) ➔ "내가 하나 줄게!"(O) ➔ "진짜 쓴다?"(R) ➔ "응, 확실히 네 거야!"(A)의 유쾌한 거래 과정이다.

## Ⅰ. DHCP의 4단계 통신 과정 (DORA)
DHCP 클라이언트(PC, 스마트폰)가 네트워크에 처음 연결되어 IP 주소를 성공적으로 할당받기까지는 **Discover, Offer, Request, Acknowledge**의 4단계(DORA)를 거칩니다.

## Ⅱ. DORA 단계별 세부 동작

```text
[ Client ]                                  [ DHCP Server ]
(IP 없음)                                    (IP Pool 관리)
   │     1. DHCP Discover (Broadcast) ────────────▶│
   │                                               │
   │◀─────────── 2. DHCP Offer (Broadcast/Unicast) │
   │                                               │
   │     3. DHCP Request (Broadcast) ─────────────▶│
   │                                               │
   │◀─────────── 4. DHCP Ack (Broadcast/Unicast)   │
   │                                               │
(IP 할당 완료!)
```

### 1. DHCP Discover (발견)
- **방향**: Client ➔ Server (Broadcast)
- **내용**: 클라이언트가 네트워크에 처음 들어왔지만 서버가 누군지 모르므로, 네트워크 전체에 `255.255.255.255` 주소로 "여기 DHCP 서버 있으면 응답 좀 해주세요!"라고 소리칩니다.

### 2. DHCP Offer (제안)
- **방향**: Server ➔ Client (Broadcast 또는 Unicast)
- **내용**: Discover 메시지를 들은 DHCP 서버가 자신의 IP 풀(Pool)에서 남는 IP 주소 하나(예: `192.168.1.10`)를 골라 "이 IP 주소 쓸래?"라고 제안(Offer)합니다.

### 3. DHCP Request (요청)
- **방향**: Client ➔ Server (Broadcast)
- **내용**: 클라이언트는 제안받은 IP를 쓰겠다고 서버에 확정 요청(Request)을 보냅니다. 이때 여러 대의 서버가 동시에 Offer를 보냈을 수도 있으므로, **"나는 A 서버가 준 IP를 쓸 거야!"** 라고 네트워크 전체에 알리기 위해 다시 브로드캐스트로 보냅니다. (선택받지 못한 다른 서버들은 자기가 제안했던 IP를 풀로 회수함)

### 4. DHCP Acknowledge (승인, ACK)
- **방향**: Server ➔ Client (Broadcast 또는 Unicast)
- **내용**: 최종적으로 서버가 "그래, 그 IP는 이제 네 거야. 임대 시간은 24시간이야"라고 확정(Ack) 지어줍니다. 이 메시지를 받은 직후부터 클라이언트는 해당 IP를 통신에 사용합니다.

## Ⅲ. 만약 IP 할당을 거절당한다면? (NACK)
클라이언트가 이전에 쓰던 IP를 다시 달라고 Request를 보냈는데, 그사이에 다른 사람이 그 IP를 가져가 버렸다면 서버는 **DHCP NAK (Negative Acknowledge)** 를 보냅니다. 클라이언트는 즉시 포기하고 처음(Discover)부터 다시 시작해야 합니다.

> 📢 **섹션 요약 비유**: 식당에 들어가서 "빈자리 있어요?"(Discover) 외치면, 종업원이 "저쪽 창가 자리 앉으실래요?"(Offer) 합니다. 그럼 손님이 "네, 저기 앉을게요!"(Request) 하고 크게 대답하면, 종업원이 "네, 테이블 세팅해 드릴게요!"(Ack) 하고 최종 확정되는 과정과 완벽히 똑같습니다.
