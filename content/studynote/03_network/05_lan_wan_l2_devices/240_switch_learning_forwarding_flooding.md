+++
weight = 240
title = "240. 수신/학습 (Learning) / 전달 (Forwarding) / 플러딩 (Flooding) - Unknown Unicast Flooding"
date = "2026-05-05"
[extra]
categories = "studynote-network"
+++

## 0. 핵심 인사이트

> **핵심**: L2 스위치가 텅 빈 깡통 상태에서 훌륭한 교통경찰로 진화하는 과정은 프레임을 처리하는 5대 동작 알고리즘인 **Learning(학습), Forwarding(전달), Filtering(여과), Flooding(플러딩), Aging(노화)**의 유기적인 결합 덕분이다.
> **비유**: 수신/학습 (Learning) / 전달 (Forwarding) / 플러딩 (Flooding) - Unknown Unicast Flooding은(는) LAN/WAN 구조와 2계층 장비 안에서 데이터와 제어 규칙을 질서 있게 맞춰 주는 교통 체계와 같다.

> 📝 모범 답안

## 1. 개요 및 필요성

- **개념**: 스위치가 데이터를 올바르게 보내기 위해 수행하는 일련의 자율적 논리 프로세스다. 스위치 전원을 막 켜면 MAC 주소 테이블은 텅 비어있다. 스위치는 네트워크 트래픽을 관찰하며 스스로 학습하고, 적절히 버리거나 전달한다.
- **필요성**: 만약 스위치가 IP 라우터처럼 관리자가 일일이 "1번 포트에 무슨 PC, 2번 포트에 무슨 PC"를 수동으로 입력(Static Routing)해줘야 한다면, 사무실에서 직원이 자리를 옮기거나 노트북을 껐다 켤 때마다 네트워크 관리자는 퇴근을 못 할 것이다. 이더넷 스위치의 위대함은 **전원만 꽂으면 스스로 네트워크 지형을 학습하는 "Plug and Play"** 기능에 있다.

---

스위치 포트에 프레임이 들어오면, 스위치는 가장 먼저 프레임 헤더의 **출발지(Source) MAC 주소**를 까본다.
- "1번 포트에서 `MAC A`가 보낸 편지가 들어왔네? 그럼 1번 포트 끝에는 `MAC A`라는 PC가 매달려 있구나!"
- 이를 즉시 MAC 주소 테이블에 `[MAC A - Port 1]`이라고 기록한다.

## 2. 구성요소

스위치가 이제 목적지 MAC 주소를 보고 어디로 보낼지 결정해야 한다. 목적지가 `MAC B`인데, 아직 테이블에 `MAC B`가 어디 있는지 정보가 없다.
- 스위치는 **"모르는 유니캐스트(Unknown Unicast)"** 또는 아예 전체 방송용인 **"브로드캐스트(FF:FF...)"** 프레임을 받으면, 편지가 들어온 포트를 제외한 **나머지 모든 포트로 편지를 복사해서 쏟아낸다**. 이것이 플러딩이다.

## 3. 구조 및 원리

**핵심 조건**: 수신/학습 (Learning) / 전달 (Forwarding) / 플러딩 (Flooding) - Unknown Unicast Flooding은(는) Ethernet, MAC 주소, 스위칭 조건을 함께 만족할 때 안정적으로 동작한다.

동작 순서:

만약 스위치가 테이블을 뒤졌는데 목적지 `MAC B`가 3번 포트에 있다는 것을 이미 학습(Learning)한 상태라면?
- 플러딩하지 않고, **오직 3번 포트로만 프레임을 조용히 전달**한다. 이것이 스위치의 진면목인 포워딩이다.

## 4. 비교 및 연결

테이블에 `[MAC A - Port 1]`, `[MAC B - Port 1]`이라고 적혀있다고 가정하자. (1번 포트에 작은 허브가 달려있는 상황)
- A가 B에게 편지를 보냈다. 스위치가 1번 포트에서 편지를 받아보니, 목적지 B도 1번 포트에 있다.
- "어? 어차피 1번 포트(허브) 안에서 너희들끼리 주고받았겠네? 내가 굳이 다른 포트로 이걸 넘겨줄 필요가 없지!" 하고 스위치는 이 프레임을 즉시 **폐기(버림)**한다. 이것이 필터링이다. 덕분에 다른 포트의 대역폭 낭비를 막는다.

## 5. 실무 적용 및 판단

- 한 번 학습된 정보가 평생 남으면, 노트북을 뽑아서 다른 자리로 갔을 때 스위치는 계속 옛날 포트로 데이터를 보낼 것이다.
- 그래서 스위치는 테이블에 적힌 정보가 기본값 300초(Aging Time) 동안 사용되지 않으면(데이터가 안 들어오면) **테이블에서 쿨하게 삭제**해 버리고, 다음번에 다시 Learning을 수행한다.

```text
 ┌─────────────────────────────────────────────────────────────┐
 │                스위치의 Learning과 Flooding 과정                │
 ├─────────────────────────────────────────────────────────────┤
 │                                                             │
 │   1. PC A가 PC B로 핑(Ping) 전송                             │
 │   [ PC A ] ────▶(Port 1) [ 스위치 ] (Port 3)──── [ PC B ]   │
 │   (MAC A)                  테이블 비어있음          (MAC B)   │
 │                                                             │
 │   2. Learning (학습)                                         │
 │   스위치: "출발지가 MAC A네? Port 1에 MAC A 등록!"               │
 │   CAM Table: [ MAC A : Port 1 ]                             │
 │                                                             │
 │   3. Flooding (플러딩)                                       │
 │   스위치: "목적지 MAC B는 어딨는지 모르겠네? 1번 빼고 다 뿌려!"      │
 │   스위치 ──▶ Port 2, Port 3, Port 4... 전송                   │
 │                                                             │
 │   4. PC B의 응답 및 재학습                                     │
 │   PC B가 응답 프레임 보냄 ──▶ 스위치 (Port 3로 들어옴)            │
 │   스위치: "출발지가 MAC B네? Port 3에 MAC B 등록!"               │
 │   CAM Table: [ MAC A : Port 1 ]                             │
 │              [ MAC B : Port 3 ]                             │
 │                                                             │
 │   5. Forwarding (포워딩)                                     │
 │   스위치: "이제 목적지 MAC A 위치(Port 1) 아니까 조용히 전송!"      │
 │                                                             │
 └─────────────────────────────────────────────────────────────┘
```

## 6. 기대효과 및 결론

수신/학습 (Learning) / 전달 (Forwarding) / 플러딩 (Flooding) - Unknown Unicast Flooding을 적용하면 Ethernet과 MAC 주소에 대한 통제력이 높아지고, 운영 일관성과 성능 예측 가능성을 확보할 수 있다. 반면 설정 복잡도, 표준 호환성, 장비 비용, 운영 숙련도라는 전제가 뒤따르므로 무조건적인 도입이 정답은 아니다. 결론적으로 이 주제는 LAN/WAN 구조와 2계층 장비를 이해하는 기준점이며, 최근에는 자동화·가상화·지능형 제어와 결합해 더 세밀한 최적화 방향으로 진화하고 있다.

## 7. 발전 흐름도

```text
기초 LAN/WAN 구조와 2계층 장비 이해
    ↓
수신/학습 (Learning) / 전달 (Forwarding) / 플러딩 (Flooding) - Unknown Unicast Flooding 개념 정립
    ↓
표준화·상용화 적용
    ↓
자동화·가상화 연계
    ↓
지능형 최적화·차세대 확장
```

수신/학습 (Learning) / 전달 (Forwarding) / 플러딩 (Flooding) - Unknown Unicast Flooding은(는) 단일 기능으로 끝나지 않고 표준화, 운영 자동화, 고속화·지능화 단계로 확장된다.

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Ethernet | 수신/학습 (Learning) / 전달 (Forwarding) / 플러딩 (Flooding) - Unknown Unicast Flooding를 이해할 때 함께 봐야 하는 LAN/WAN 구조와 2계층 장비 핵심 개념 |
| MAC 주소 | 수신/학습 (Learning) / 전달 (Forwarding) / 플러딩 (Flooding) - Unknown Unicast Flooding를 이해할 때 함께 봐야 하는 LAN/WAN 구조와 2계층 장비 핵심 개념 |
| 스위칭 | 수신/학습 (Learning) / 전달 (Forwarding) / 플러딩 (Flooding) - Unknown Unicast Flooding를 이해할 때 함께 봐야 하는 LAN/WAN 구조와 2계층 장비 핵심 개념 |
| VLAN | 수신/학습 (Learning) / 전달 (Forwarding) / 플러딩 (Flooding) - Unknown Unicast Flooding를 이해할 때 함께 봐야 하는 LAN/WAN 구조와 2계층 장비 핵심 개념 |
| 브리지/STP | 수신/학습 (Learning) / 전달 (Forwarding) / 플러딩 (Flooding) - Unknown Unicast Flooding를 이해할 때 함께 봐야 하는 LAN/WAN 구조와 2계층 장비 핵심 개념 |
