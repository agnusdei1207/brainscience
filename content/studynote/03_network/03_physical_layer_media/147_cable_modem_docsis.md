+++
weight = 147
title = "147. 케이블 모뎀 (Cable Modem) / DOCSIS 표준"
date = "2026-04-19"
[extra]
categories = "studynote-network"
+++

## 0. 핵심 인사이트

> **핵심**: 케이블 모뎀(Cable Modem)은 기존 케이블 TV(CATV, Community Antenna Television) 동축 케이블 인프라를 재활용해 광대역 인터넷을 제공하는 장치이며, DOCSIS(Data Over Cable Service Interface Specification) 표준이 데이터 전송 방식을 정의한다.
> **비유**: 케이블 모뎀 (Cable Modem) / DOCSIS 표준은(는) 전송 매체와 물리 계층 안에서 데이터와 제어 규칙을 질서 있게 맞춰 주는 교통 체계와 같다.

> 📝 모범 답안

## 1. 개요 및 필요성

케이블 모뎀은 CATV 인프라를 데이터 통신에 재활용하는 기술이다. 1990년대 중반, 전화선 기반 DSL(Digital Subscriber Line)이 좁은 대역폭으로 한계를 보이던 시절, CATV 사업자들은 이미 가정까지 구축된 동축 케이블(Coaxial Cable)망을 인터넷 서비스에 활용하는 방안을 모색했다.

케이블 TV 신호는 MHz 단위의 넓은 주파수 대역을 사용한다. 이 중 데이터 통신에 일부 채널을 할당하면 기존 인프라 투자 없이도 광대역 인터넷을 제공할 수 있다. 이를 표준화한 것이 CableLabs가 개발한 **DOCSIS(Data Over Cable Service Interface Specification)** 이다.

**케이블 모뎀 없으면 발생하는 문제**:
- 가정마다 새로운 광섬유 직결(FTTH) 배선 필요 → 막대한 비용
- 기존 CATV 인프라 유휴화 → 투자 손실
- 도심 외곽 광대역 인터넷 공급 공백

---

```text
인터넷
  │
  ▼
헤드엔드 (Headend)
  │ 광섬유 (Fiber)          ← 높은 대역폭, 간선망
  ▼
광 노드 (Optical Node / CMTS 연결점)
  │ 동축 케이블 (Coaxial)   ← 라스트 마일, 가정까지
  ├── 가정 A: [Cable Modem] ─ [Router] ─ [PC]
  ├── 가정 B: [Cable Modem] ─ [Router] ─ [PC]
  └── 가정 C: [Cable Modem] ─ [TV]
```

- **CMTS (Cable Modem Termination System)**: 헤드엔드에 위치하는 장비로, 여러 케이블 모뎀과의 통신을 집선하고 인터넷과 연결함
- **HFC (Hybrid Fiber-Coaxial)**: 헤드엔드 ~ 광 노드는 광섬유, 광 노드 ~ 가정은 동축 케이블로 구성된 혼합 망

## 2. 구성요소

```text
동축 케이블 주파수 대역 (DOCSIS 3.1 기준)

  5 MHz                       85 MHz              1,218 MHz
  │◄──── 업스트림 (Upstream) ────►│◄──── 다운스트림 (Downstream) ────►│
  │  가정 → CMTS               │      CMTS → 가정                  │
  │  OFDMA 다중 접속             │      OFDM 고속 다운로드             │
  │  최대 ~1 Gbps 이론           │      최대 ~10 Gbps 이론            │
```

- 다운스트림이 더 넓은 주파수를 차지: 인터넷 사용 패턴이 다운로드 중심이기 때문
- DOCSIS 3.1은 OFDM(Orthogonal Frequency-Division Multiplexing) 도입으로 기존 SC-QAM 대비 효율 대폭 향상

## 3. 구조 및 원리

**핵심 조건**: 케이블 모뎀 (Cable Modem) / DOCSIS 표준은(는) 매체 특성, 감쇠, 간섭 조건을 함께 만족할 때 안정적으로 동작한다.

동작 순서:

| 버전 | 발표년도 | 다운스트림 이론 최대 | 업스트림 이론 최대 | 주요 기술 |
|:---:|:---:|:---:|:---:|:---|
| DOCSIS 1.0 | 1997 | 42 Mbps | 10 Mbps | SC-QAM |
| DOCSIS 2.0 | 2001 | 42 Mbps | 30 Mbps | 업스트림 개선 |
| DOCSIS 3.0 | 2006 | 1.2 Gbps | 200 Mbps | 채널 본딩(Channel Bonding) |
| DOCSIS 3.1 | 2013 | ~10 Gbps | ~1 Gbps | OFDM/OFDMA |
| DOCSIS 4.0 | 2020 | ~10 Gbps | ~6 Gbps | Full Duplex + ESD |

---

### 케이블 모뎀 vs. DSL vs. FTTH

| 구분 | 케이블 모뎀 (HFC) | DSL (전화선) | FTTH (광섬유) |
|:---|:---|:---|:---|
| 매체 | 동축 케이블 | 구리 전화선 | 광섬유 |
| 대역폭 | 최대 ~10 Gbps (DOCSIS 3.1) | 수십~수백 Mbps | 1 Gbps ~ 10 Gbps |
| 거리 영향 | 적음 | 거리↑ → 속도↓ 심각 | 없음 |
| 공유 여부 | 이웃과 대역폭 공유 | 전용 회선 | 전용 회선 |
| 인프라 재활용 | CATV 망 재활용 | 전화망 재활용 | 신규 광섬유 필요 |
| 설치 비용 | 낮음 | 낮음 | 높음 |

**케이블 모뎀의 공유 대역폭 문제**: 같은 광 노드에 연결된 수십~수백 가구가 대역폭을 공유한다. 저녁 피크 시간대에 이웃이 대용량 스트리밍을 사용하면 속도가 저하된다. DOCSIS 3.1의 OFDMA와 스케줄링 알고리즘이 이 문제를 완화한다.

### 연결 개념 흐름

CATV 동축망 → HFC 구조 → CMTS (헤드엔드) → DOCSIS 표준 → 케이블 모뎀 → 가정 라우터 → 최종 사용자

---

## 4. 비교 및 연결

### 의사결정 기준

| 상황 | 권장 선택 | 이유 |
|:---|:---|:---|
| 소규모 가정 인터넷 | 케이블 모뎀 (DOCSIS 3.1) | 비용 대비 충분한 성능 |
| 기가비트 인터넷 필요 (개인) | FTTH 또는 DOCSIS 3.1 | 대역폭 보장 |
| 소규모 오피스 (보장 대역폭 필요) | FTTH 전용 회선 | 공유 대역폭 불확실성 제거 |
| 피크 타임 속도 저하가 심각한 지역 | FTTH 전환 검토 | HFC 공유 대역폭 문제 |

### 안티패턴

**CMTS 용량 초과 수용**: 광 노드 하나에 연결 가구 수가 너무 많으면(Over-subscription 과도) 피크 시간 대역폭이 심각하게 저하된다. ISP는 노드 분할(Node Split)로 가구당 대역폭을 확보해야 한다.

**DOCSIS 3.0 이하 모뎀 유지**: DOCSIS 3.0까지는 SC-QAM 방식으로 효율에 한계가 있다. 기가비트 플랜을 구독해도 구형 모뎀이 병목이 되면 속도 보장이 불가능하다. DOCSIS 3.1 인증 모뎀을 사용해야 한다.

---

## 5. 실무 적용 및 판단

케이블 모뎀과 DOCSIS 표준은 기존 CATV 인프라를 최대한 재활용하면서 광대역 인터넷 보급을 앞당긴 핵심 기술이다. DOCSIS 3.1의 OFDM 도입은 최대 10 Gbps 이론 속도를 가능하게 했으며, DOCSIS 4.0의 풀 듀플렉스(Full Duplex ESD) 기술은 업스트림도 대폭 향상시켜 FTTH와의 격차를 줄이고 있다.

케이블 모뎀은 "기존 인프라를 최대한 쥐어짜는 기술"이라는 점에서, 신규 투자 없이 광대역을 제공하는 **라스트 마일 혁신**의 교과서적 사례다.

---

## 6. 기대효과 및 결론

**한계**: 공유 매체 특성상 가입자 밀도가 높으면 피크 타임 성능이 저하된다. 또한 동축 케이블의 물리적 대역폭은 광섬유에 비해 절대적으로 좁아, 수십 Gbps 이상의 차세대 인터넷에서는 FTTH로의 전환이 불가피하다.

**미래 방향**: ① DOCSIS 4.0의 멀티기가빗 업스트림 지원, ② 원격 PHY(Physical Layer) 분산 아키텍처(R-PHY), ③ DAA(Distributed Access Architecture) 도입으로 광 노드 지능화.

## 7. 발전 흐름도

```text
CATV 동축 케이블 인프라 (기존 TV 배선)
    │
    ▼
HFC (Hybrid Fiber-Coaxial) 망 구축
    │
    ▼
DOCSIS 1.0 / 2.0 (SC-QAM, 수십 Mbps)
    │
    ▼
DOCSIS 3.0 (채널 본딩, 1 Gbps)
    │
    ▼
DOCSIS 3.1 (OFDM/OFDMA, ~10 Gbps)
    │
    ▼
DOCSIS 4.0 (Full Duplex ESD, 멀티기가빗 업스트림)
```

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **HFC (Hybrid Fiber-Coaxial)** | 케이블 모뎀이 사용하는 광+동축 혼합 망 구조 |
| **CMTS (Cable Modem Termination System)** | 헤드엔드에서 다수 케이블 모뎀을 집선·관리하는 장비 |
| **DSL (Digital Subscriber Line)** | 전화선 기반 광대역 접속; 케이블 모뎀의 경쟁 기술 |
| **FTTH (Fiber To The Home)** | 광섬유 직결 방식; 케이블 모뎀의 장기 대안 |
| **OFDM (Orthogonal Frequency-Division Multiplexing)** | DOCSIS 3.1에서 채택한 고효율 다중화 방식 |
