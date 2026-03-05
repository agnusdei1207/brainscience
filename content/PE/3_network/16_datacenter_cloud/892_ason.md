+++
title = "892. ASON (Automatically Switched Optical Network)"
date = "2026-03-05"
[extra]
categories = "studynotes-03_network"
+++

# 892. ASON (Automatically Switched Optical Network) - 지능형 광교환 네트워크

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기존의 수동적인 광전송망에 **지능형 제어 평면(Control Plane)**을 결합하여, 네트워크 스스로가 경로를 계산하고 광 스위치를 자동 제어하여 연결을 설정하는 기술이다.
> 2. **혁신**: 장애 발생 시 수 밀리초(ms) 내에 우회 경로를 자동으로 찾아 복구하는 **'자가 치유(Self-healing)'** 능력과, 필요에 따라 대역폭을 즉시 할당하는 동적 서비스(BoD)를 제공한다.
> 3. **가치**: 대규모 클라우드 트래픽 변동에 유연하게 대응하며, 복잡한 광 네트워크 관리 비용(OPEX)을 획기적으로 낮추는 차세대 광 전송 아키텍처이다.

---

## Ⅰ. 개요 (Context & Background)

### 개념
ASON은 ITU-T에서 표준화한 지능형 광 네트워크 아키텍처이다. 과거의 광망은 사람이 직접 광패치 코드를 꽂거나 관리 시스템에서 수동으로 경로를 지정해야 했으나, ASON은 라우터처럼 스스로 네트워크 상태를 파악하고 빛의 길을 만들어낸다.

### 💡 비유
- **전통적 광망 (Static)**: 기차 선로와 같다. 한 번 깔린 선로는 바꿀 수 없으며, 선로가 끊어지면 사람이 직접 가서 수리할 때까지 기차가 멈춰야 한다.
- **ASON (Dynamic)**: 내비게이션이 달린 자율주행 자동차 시스템과 같다. 목적지만 입력하면 도로 상황을 보고 가장 빠른 길을 스스로 찾아간다. 만약 사고로 길이 막히면 내비게이션이 즉시 골목길(우회 경로)을 안내해 멈추지 않고 가게 해준다.

### 등장 배경: 'Traffic Unpredictability'
데이터센터 간 트래픽(East-West Traffic)은 예측이 매우 어렵고 변동성이 크다. 고정된 광 전송로(Static Provisioning) 방식으로는 급격한 트래픽 증가에 대응하기 위해 몇 주씩 기다려야 했고, 이는 클라우드 시대의 민첩성에 걸림돌이 되었다. 이를 해결하기 위해 광학 계층의 자동화가 필요해졌다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### ASON 3면체 아키텍처 (ASCII Diagram)

ASON은 기능적으로 세 가지 평면으로 나뉜다.

```ascii
[ Management Plane ]  <--- (Configuration & Billing)
         │
┌────────▼────────┐  1. Request  ┌────────────────────┐
│  Control Plane  │ <──────────> │  Other ASON Nodes  │
│  (GMPLS / PCE)  │  2. Signaling│  (Intelligence)    │
└────────┬────────┘              └────────────────────┘
         │ 3. Switch Command
┌────────▼────────┐
│ Transport Plane │ <──────────> [ Actual Data (Light) ]
│ (OXC / ROADM)   │
└─────────────────┘

* 핵심 원리: '전송'과 '제어'를 분리하고, 제어 평면이 스스로 경로를 결정함.
```

### 3대 핵심 평면 (Planes)

#### ① 전송 평면 (Transport Plane)
실제 데이터(빛)가 흐르는 물리적 계층이다. **OXC(Optical Cross-Connect)**나 **ROADM(Reconfigurable Optical Add-Drop Multiplexer)** 장비가 위치하여 빛의 방향을 물리적으로 바꾼다.

#### ② 제어 평면 (Control Plane) - ASON의 핵심
네트워크의 두뇌에 해당한다. **GMPLS(Generalized Multi-Protocol Label Switching)** 프로토콜을 사용하여 토폴로지를 발견하고, 최적 경로를 계산(Constraint-based Routing)하며, 장비 간에 신호를 주고받아 경로를 설정한다.

#### ③ 관리 평면 (Management Plane)
네트워크 운영자가 전체 상태를 모니터링하고 가이드라인을 설정하는 곳이다. 장애 발생 시 리포트를 받고 과금 정보를 관리한다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 전통적 광망 vs ASON 심층 비교

| 비교 항목 | 전통적 광망 (SDH/WDM) | **ASON (지능형 광망)** |
|-----------|-----------------------|-------------------------|
| **경로 설정** | 수동 (Manual Provisioning) | **자동 (Auto Provisioning)** |
| **장애 복구** | 단순 이중화 (1+1 Protection) | **다중 경로 복구 (Mesh Restoration)** |
| **자원 효율** | 낮음 (예비 경로 선점 필요) | **높음 (유휴 자원 동적 공유)** |
| **응답 시간** | 수일 ~ 수주 (인력 투입) | **수초 ~ 수분 (즉시 할당)** |
| **주요 기술** | 고정식 하드웨어 | GMPLS, PCE, ROADM |

### ASON의 3단계 연결 서비스 (Table)

| 서비스 유형 | 특징 | 용도 |
|-------------|------|------|
| **Permanent (PC)** | 관리자가 수동으로 영구 설정 | 기본 기간망 |
| **Switched (SC)** | 사용자가 직접 필요할 때 요청 | 주문형 대역폭 (BoD) |
| **Soft Switched (SPC)** | 관리자가 요청하고 시스템이 자동 설정 | 운영 효율화 |

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 (실무 도입 시나리오)

**상황**: 전국 단위의 데이터센터를 운영하는 통신사에서 지진이나 대규모 공사로 인한 광케이블 단선 사고 시 서비스 중단 시간을 최소화해야 한다.
**판단 및 ASON 구축 전략**:
1. **Mesh Topology 구축**: 링(Ring) 구조가 아닌 거미줄(Mesh) 구조로 광 선로를 구성한다.
2. **Restoration 우선순위 설정**: 핵심 데이터(금융 등)는 'Protection+Restoration'으로 50ms 내 복구하게 하고, 일반 데이터는 'Restoration'만 설정하여 비용 효율을 높인다.
3. **PCE (Path Computation Element) 연동**: 복잡한 다차원 경로 계산을 전담하는 서버를 두어 대규모 망에서도 최적의 길을 찾게 한다.
4. **결과**: 케이블이 단선되어도 사용자는 인지하지 못할 속도로 경로가 자동 우회되며, 전용선 개통 시간이 2주에서 5분으로 단축됨.

### 안티패턴 및 고려사항
- **복잡한 제어 로직**: 제어 평면이 너무 복잡해지면 소프트웨어 버그로 인해 망 전체가 마비될 위험(Control Plane Flapping)이 있다. 안정성이 검증된 프로토콜을 사용해야 한다.
- **표준 호환성**: 제조사마다 GMPLS 구현 방식이 미세하게 다를 수 있어, 멀티 벤더 환경에서는 상호 운용성 테스트가 필수적이다.

---

## Ⅴ. 미래 전망 및 결론

### 결론: SDN과 광망의 결합
ASON은 광 네트워크가 단순한 '파이프'에서 '지능형 서비스 플랫폼'으로 진화하는 첫걸음이었다. 이는 현대의 **SD-OTN (Software Defined Optical Transport Network)**의 이론적 기반이 되었으며, 데이터센터의 자동화 흐름에 필수적인 기술이다.

### 미래 전망
앞으로는 인공지능(AI)이 결합된 **AI-ASON**이 등장할 것이다. 트래픽 패턴을 미리 예측하여 트래픽이 몰리기 직전에 광 경로를 미리 확보하거나, 광학 신호의 품질(OSNR) 저하를 미리 감지해 장애가 나기 전에 예방 정비하는 자율 운영 광 네트워크(Autonomous Optical Network)로 발전할 전망이다.

---

## 📌 관련 개념 맵 (Knowledge Graph)
- [ROADM (재구성 가능 광 분기 결합기)](../../3_network/2_multiplexing/90_roadm.md) - ASON의 손과 발이 되는 장비
- [GMPLS (Generalized MPLS)](../../3_network/6_sdn_nfv/520_gmpls.md) - ASON의 언어이자 프로토콜
- [SDN (Software Defined Networking)](../../3_network/6_sdn_nfv/500_sdn_concept.md) - ASON이 지향하는 중앙 제어의 진화형
- [Mesh Topology](../../3_network/5_lan_wan/150_topology.md) - ASON의 장점을 극대화하는 망 구조

---

## 👶 어린이를 위한 3줄 비유 설명
1. **ASON이 뭔가요?**: 인터넷 정보를 실어 나르는 빛의 길을 컴퓨터가 스스로 척척 만들어내는 '똑똑한 지도 시스템'이에요.
2. **왜 똑똑해야 하나요?**: 가끔 바닷속 케이블이 끊어지거나 길이 막힐 때, 사람이 가서 고칠 때까지 기다리지 않고 컴퓨터가 즉시 다른 길을 찾아 정보를 보내야 하기 때문이에요.
3. **뭐가 제일 좋나요?**: 정보를 보내는 길이 막혀서 인터넷이 끊기는 일이 거의 없어지고, 우리가 원할 때 언제든 대용량 동영상을 아주 빨리 볼 수 있게 해준답니다!
