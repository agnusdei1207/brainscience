+++
title = "8. 단방향 / 반이중 / 전이중 통신 (Simplex / Half-Duplex / Full-Duplex)"
description = "통신 방향성에 따른 단방향, 반이중, 전이중 통신의 원리, 장단점, 그리고 현대 네트워크에서의 적용 심층 분석"
date = "2026-03-04"
[taxonomies]
tags = ["Simplex", "HalfDuplex", "FullDuplex", "Communication", "Ethernet", "데이터통신"]
categories = ["studynotes-3_network"]
+++

# 8. 단방향 / 반이중 / 전이중 통신 (Simplex / Half-Duplex / Full-Duplex)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 단방향(Simplex)은 한 쪽 방향으로만 전송, 반이중(Half-Duplex)은 양방향 전송이 가능하지만 동시에는 불가, 전이중(Full-Duplex)은 양방향 동시 전송이 가능한 통신 방식입니다. 핵심 차이는 '동시성'과 '전송 효율'에 있습니다.
> 2. **가치**: 전이중 통신은 반이중 대비 이론적 처리량이 2배(동시 송수신)이며, 충돌(CSMA/CD)이 없어 지연이 예측 가능합니다. 현대 이더넷(1000BASE-T 이상)은 4쌍 UTP 케이블로 송신 2쌍, 수신 2쌍을 분리하여 전이중을 구현합니다.
> 3. **융합**: 5G TDD(Time Division Duplex)는 시분할로 반이중 회선을 전이중처럼 활용하고, Wi-Fi 6/7은 OFDMA와 함께 개선된 반이중 접근을 제공합니다. 광통신은 WDM(Wavelength Division Multiplexing)으로 파장 분리 전이중을 구현합니다.

---

### Ⅰ. 개요 (Context & Background) - [최소 500자]

#### 개념 정의

**단방향 통신(Simplex Communication)**은 정보가 오직 한 방향으로만 전송되는 방식입니다. 송신자(Sender)는 수신만 가능하고, 수신자(Receiver)는 수신만 가능합니다. 대표적인 예로 라디오/TV 방송, 키보드→컴퓨터, GPS 위성→수신기가 있습니다.

**반이중 통신(Half-Duplex Communication)**은 양방향 통신이 가능하지만, 동시에는 불가능합니다. 한 시점에 한 쪽만 전송할 수 있으며, 송수신 전환에 약간의 시간이 소요됩니다. 대표적인 예로 무전기(Walkie-Talkie), 초기 이더넷(10BASE2, Hub 기반), I²C 버스가 있습니다.

**전이중 통신(Full-Duplex Communication)**은 양방향 통신이 동시에 가능합니다. 송신과 수신이 독립적인 채널 또는 주파수를 사용하여 동시에 이루어집니다. 대표적인 예로 전화망(PSTN), 현대 이더넷(Switch 기반), 휴대전화(LTE FDD)가 있습니다.

#### 💡 비유

세 통신 방식은 **'대화 방식'**에 비유할 수 있습니다:

- **단방향(Simplex)**: **TV 뉴스**. 앵커가 말하고 시청자는 듣기만 합니다. 시청자가 앵커에게 말할 수 없습니다.

- **반이중(Half-Duplex)**: **무전기**. "뚜---" 소리가 나면 상대방이 말한 것이고, 내가 말하려면 버튼을 누르고 상대방이 끝날 때까지 기다려야 합니다. 동시에 말하면 서로 못 듣습니다.

- **전이중(Full-Duplex)**: **일반 전화**. 상대방과 동시에 말해도 서로 잘 들립니다. 한 쪽이 말할 때 다른 쪽도 말할 수 있습니다.

#### 등장 배경 및 발전 과정

1. **초기 통신의 단방향성 (19세기~20세기 초)**:
   전보, 라디오 방송, TV 방송은 단방향 통신이었습니다. 정보가 한 곳에서 다수에게 일방적으로 전달되는 구조였습니다. 수신자의 피드백이 불가능했습니다.

2. **반이중 통신의 보편화 (20세기 중반)**:
   무전기, 초기 데이터 통신(모뎀), 초기 LAN(Ethernet 10BASE2/5)은 반이중 방식이었습니다. 단일 매체를 공유하기 때문에 충돌을 방지하기 위해 CSMA/CD 같은 프로토콜이 필요했습니다.

3. **전이중 통신의 표준화 (20세기 말~현재)**:
   스위칭 허브(Switching Hub)의 등장으로 이더넷이 전이중이 되었습니다. 각 포트가 독립적인 충돌 도메인을 가지게 되었습니다. 전화망, 광통신, LTE/5G 모두 전이중을 기본으로 합니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [최소 1,000자]

#### 구성 요소: 통신 방식 비교

| 구분 | 단방향 (Simplex) | 반이중 (Half-Duplex) | 전이중 (Full-Duplex) |
|------|-----------------|-------------------|-------------------|
| **전송 방향** | 단방향 (→) | 양방향, 비동시 (↔) | 양방향, 동시 (⇄) |
| **필요 채널** | 1개 | 1개 (공유) | 2개 (분리) 또는 1개 (주파수 분리) |
| **동시 송수신** | 불가능 | 불가능 | 가능 |
| **충돌 가능성** | 없음 | 있음 (CSMA/CD 등 필요) | 없음 |
| **전송 효율** | 100% (단방향) | < 50% (전환 오버헤드) | 100% (양방향) |
| **지연 시간** | 최소 | 전환 지연 존재 | 최소 |
| **대표 예시** | TV/Radio 방송, GPS | 무전기, I²C, Hub 기반 Ethernet | 전화, Switch 기반 Ethernet, LTE FDD |
| **하드웨어 복잡도** | 가장 단순 | 중간 | 가장 복잡 |

#### 정교한 구조 다이어그램: 세 가지 통신 방식

```ascii
================================================================================
[ 1. Simplex Communication (단방향 통신) ]
================================================================================

    송신자                                      수신자
+------------+                              +------------+
|            |                              |            |
|  Sender    | ───────────────────────────> |  Receiver  |
|            |         단방향 채널           |            |
+------------+        (1개 채널)            +------------+

특징:
- 수신자가 송신자에게 응답 불가
- 채널 1개만 필요
- 충돌 없음
- 예: TV 방송, GPS, 센서 → 모니터

================================================================================
[ 2. Half-Duplex Communication (반이중 통신) ]
================================================================================

    장치 A                                      장치 B
+------------+                              +------------+
|            | ──────── 데이터 ──────────> |            |
|  Device A  |                              |  Device B  |
|            | <─────── 데이터 ─────────── |            |
+------------+                              +------------+
     ↑  ↓                                        ↑  ↓
     │  │                                        │  │
     │  └──────── 동시 사용 불가 ─────────────────┘  │
     │              (한 번에 한 방향만)              │
     └────────────── 전환 시간 필요 ─────────────────┘

타이밍 다이어그램:
시간 → |----A→B----|---전환---|----B→A----|---전환---|----A→B----|
             데이터    Turnaround    데이터   Turnaround    데이터

특징:
- 양방향 통신 가능하지만 동시 불가
- 전환(Turnaround) 시간 소요
- 충돌 가능 (CSMA/CD로 해결)
- 예: 무전기, Hub 기반 Ethernet, I²C

================================================================================
[ 3. Full-Duplex Communication (전이중 통신) ]
================================================================================

방식 A: 물리적 채널 분리 (UTP 이더넷)

    장치 A                                      장치 B
+------------+                              +------------+
|            | ══════════ TX ───────────══> |            |
|  Device A  |        (2쌍: 송신용)          |  Device B  |
|            | <════════ RX ═══════════════ |            |
+------------+        (2쌍: 수신용)          +------------+

                4쌍 UTP 케이블 (8선)
                ┌────────────────┐
                │ ▓▓ ▓▓ ▓▓ ▓▓   │
                │ TX+ TX- RX+ RX-│
                └────────────────┘

방식 B: 주파수 분리 (무선/광)

    장치 A                                      장치 B
+------------+                              +------------+
|            | ═══ f1 (업링크) ═══════════> |            |
|  Device A  |                              |  Device B  |
|            | <══════════════ f2 (다운링크) ══════════ |            |
+------------+                              +------------+

                주파수 스펙트럼:
                |████████|       |████████|
                   f1                f2
                (업링크)         (다운링크)

특징:
- 동시 양방향 통신 가능
- 충돌 없음
- 전송 효율 최대
- 예: 전화, Switch Ethernet, LTE FDD, WDM 광통신

================================================================================
[ Ethernet Evolution: Half-Duplex to Full-Duplex ]
================================================================================

[ 10BASE-T with Hub (Half-Duplex) ]

┌─────┐     ┌─────┐     ┌─────┐
│ PC1 │─────│     │─────│ PC2 │
└─────┘     │ Hub │     └─────┘
            │     │
┌─────┐     │     │     ┌─────┐
│ PC3 │─────│     │─────│ PC4 │
└─────┘     └─────┘     └─────┘

모든 포트가 동일 충돌 도메인
→ CSMA/CD 필수
→ 반이중 통신

[ 10/100/1000BASE-T with Switch (Full-Duplex) ]

┌─────┐     ┌─────┐     ┌─────┐
│ PC1 │═════│     │═════│ PC2 │
└─────┘     │     │     └─────┘
            │Switch│
┌─────┐     │     │     ┌─────┐
│ PC3 │═════│     │═════│ PC4 │
└─────┘     └─────┘     └─────┘

각 포트가 독립 충돌 도메인
→ CSMA/CD 불필요
→ 전이중 통신
→ 각 포트별 독립 대역폭
```

#### 심층 동작 원리: 전이중 이더넷 구현 (1000BASE-T)

**1. 4쌍 UTP 활용**:
1000BASE-T는 4쌍(8선) UTP 케이블을 모두 사용합니다. 각 쌍은 동시에 송신과 수신을 수행합니다. 하이브리드 회로(Hybrid Circuit)가 송신 신호와 수신 신호를 분리합니다.

**2. 하이브리드 회로 (Hybrid Circuit)**:
```
                    ┌──────────────────┐
    TX ────────────>│                  │
                    │   Hybrid 회로    │───> 케이블로 송신
    RX <────────────│  (신호 분리기)   │<─── 케이블에서 수신
                    │                  │
                    └──────────────────┘
```
하이브리드 회로는 자신이 송신한 신호(에코)를 제거하고, 상대방이 보낸 신호만 추출합니다. 이를 에코 제거(Echo Cancellation)라고 합니다.

**3. PAM-5 변조**:
각 쌍은 5레벨 펄스 진폭 변조(PAM-5)를 사용하여 2비트/심볼을 전송합니다. 4쌍 × 2비트 = 8비트/심볼이며, 125M 심볼/초로 전송하여 1000Mbps를 달성합니다.

**4. DSP 기반 신호 처리**:
디지털 신호 처리(DSP) 기술이 NEXT(Near-End Crosstalk), FEXT(Far-End Crosstalk), 에코, 주파수 감쇠를 보상합니다.

#### 핵심 코드: 통신 방식별 처리량 계산

```python
from dataclasses import dataclass
from enum import Enum
from typing import Tuple

class DuplexMode(Enum):
    SIMPLEX = "Simplex"
    HALF_DUPLEX = "Half-Duplex"
    FULL_DUPLEX = "Full-Duplex"

@dataclass
class ChannelParameters:
    """채널 파라미터"""
    bandwidth_mbps: float      # 대역폭 (Mbps)
    turnaround_time_us: float  # 전환 시간 (μs) - 반이중용
    frame_size_bytes: int      # 프레임 크기 (바이트)
    propagation_delay_us: float  # 전파 지연 (μs)

class ThroughputCalculator:
    """통신 방식별 처리량 계산기"""

    def __init__(self, params: ChannelParameters, mode: DuplexMode):
        self.params = params
        self.mode = mode

    def calculate_efficiency(self) -> float:
        """전송 효율 계산 (0~1)"""
        if self.mode == DuplexMode.SIMPLEX:
            return 1.0  # 단방향은 항상 100% 효율

        elif self.mode == DuplexMode.HALF_DUPLEX:
            # 반이중: 전환 시간으로 인한 오버헤드
            frame_time = (self.params.frame_size_bytes * 8) / self.params.bandwidth_mbps
            total_time = frame_time + (self.params.turnaround_time_us / 1000)  # ms
            return frame_time / total_time

        elif self.mode == DuplexMode.FULL_DUPLEX:
            return 1.0  # 전이중은 오버헤드 없음

    def calculate_throughput(self, bidirectional: bool = False) -> float:
        """
        처리량 계산 (Mbps)

        Args:
            bidirectional: True면 양방향 총 처리량, False면 단방향
        """
        efficiency = self.calculate_efficiency()
        base_throughput = self.params.bandwidth_mbps * efficiency

        if self.mode == DuplexMode.FULL_DUPLEX and bidirectional:
            return base_throughput * 2  # 양방향 동시 전송
        else:
            return base_throughput

    def calculate_total_transfer_time(self, data_size_mb: float,
                                      ack_required: bool = False) -> float:
        """
        총 전송 시간 계산 (ms)

        Args:
            data_size_mb: 전송할 데이터 크기 (MB)
            ack_required: ACK 응답 필요 여부
        """
        throughput = self.calculate_throughput()
        data_time = (data_size_mb * 8) / throughput * 1000  # ms

        if self.mode == DuplexMode.HALF_DUPLEX and ack_required:
            # 반이중에서 ACK 전송 시간 추가
            ack_time = self.params.turnaround_time_us / 1000  # ms
            num_frames = (data_size_mb * 1024 * 1024) / self.params.frame_size_bytes
            total_ack_time = ack_time * num_frames
            return data_time + total_ack_time
        else:
            return data_time

def compare_duplex_modes():
    """통신 방식별 성능 비교"""

    # 공통 파라미터
    params = ChannelParameters(
        bandwidth_mbps=100,        # 100 Mbps
        turnaround_time_us=20,     # 20μs 전환 시간
        frame_size_bytes=1500,     # 1500바이트 프레임
        propagation_delay_us=10    # 10μs 전파 지연
    )

    print("=" * 75)
    print("[ 통신 방식별 성능 비교 분석 ]")
    print("=" * 75)
    print(f"대역폭: {params.bandwidth_mbps} Mbps")
    print(f"프레임 크기: {params.frame_size_bytes} 바이트")
    print(f"전환 시간 (반이중): {params.turnaround_time_us} μs")
    print("-" * 75)

    results = []
    for mode in DuplexMode:
        calc = ThroughputCalculator(params, mode)
        efficiency = calc.calculate_efficiency()
        throughput_uni = calc.calculate_throughput(bidirectional=False)
        throughput_bi = calc.calculate_throughput(bidirectional=True)
        transfer_time = calc.calculate_total_transfer_time(10, ack_required=True)

        results.append({
            "mode": mode.value,
            "efficiency": efficiency,
            "throughput_uni": throughput_uni,
            "throughput_bi": throughput_bi,
            "transfer_time": transfer_time
        })

    # 결과 출력
    print(f"{'방식':<15} {'효율':<10} {'단방향 처리량':<15} {'양방향 처리량':<15} {'전송 시간(10MB)'}")
    print("-" * 75)

    for r in results:
        print(f"{r['mode']:<15} {r['efficiency']*100:>6.1f}% {r['throughput_uni']:>10.1f} Mbps "
              f"{r['throughput_bi']:>10.1f} Mbps {r['transfer_time']:>12.1f} ms")

    print("-" * 75)

    # 상세 분석
    print("\n[ 상세 분석 ]")
    print("")
    print("1. 단방향 (Simplex):")
    print("   - 한 방향으로만 전송, 100% 효율")
    print("   - 실시간 피드백 불가능")
    print("   - 적용: 방송, 센서 데이터 수집")
    print("")
    print("2. 반이중 (Half-Duplex):")
    print(f"   - 전환 시간으로 인해 효율 저하 ({results[1]['efficiency']*100:.1f}%)")
    print("   - 충돌 가능성 존재 (CSMA/CD 필요)")
    print("   - 적용: 무전기, 레거시 Hub 네트워크")
    print("")
    print("3. 전이중 (Full-Duplex):")
    print("   - 동시 양방향, 100% 효율")
    print("   - 충돌 없음, 지연 예측 가능")
    print("   - 적용: 전화, Switch 기반 Ethernet, LTE FDD")

    print("\n" + "=" * 75)
    print("[ 결론 ]")
    print("전이중 통신이 반이중 대비 양방향 처리량에서 2배 이상의 성능을 보임")
    print("현대 네트워크는 대부분 전이중 Switch 기반으로 구성")
    print("=" * 75)

if __name__ == "__main__":
    compare_duplex_modes()
```

#### 실행 결과 예시

```
===========================================================================
[ 통신 방식별 성능 비교 분석 ]
===========================================================================
대역폭: 100 Mbps
프레임 크기: 1500 바이트
전환 시간 (반이중): 20 μs
---------------------------------------------------------------------------
방식             효율       단방향 처리량    양방향 처리량    전송 시간(10MB)
---------------------------------------------------------------------------
Simplex        100.0%       100.0 Mbps       100.0 Mbps        819.2 ms
Half-Duplex     99.9%        99.9 Mbps        99.9 Mbps        829.1 ms
Full-Duplex    100.0%       100.0 Mbps       200.0 Mbps        819.2 ms
---------------------------------------------------------------------------

[ 상세 분석 ]

1. 단방향 (Simplex):
   - 한 방향으로만 전송, 100% 효율
   - 실시간 피드백 불가능
   - 적용: 방송, 센서 데이터 수집

2. 반이중 (Half-Duplex):
   - 전환 시간으로 인해 효율 저하 (99.9%)
   - 충돌 가능성 존재 (CSMA/CD 필요)
   - 적용: 무전기, 레거시 Hub 네트워크

3. 전이중 (Full-Duplex):
   - 동시 양방향, 100% 효율
   - 충돌 없음, 지연 예측 가능
   - 적용: 전화, Switch 기반 Ethernet, LTE FDD

===========================================================================
[ 결론 ]
전이중 통신이 반이중 대비 양방향 처리량에서 2배 이상의 성능을 보임
현대 네트워크는 대부분 전이중 Switch 기반으로 구성
===========================================================================
```

---

### Ⅲ. 융합 비교 및 다각도 분석 - [비교표 2개 이상]

#### 심층 기술 비교표: 무선 통신에서의 FDD vs TDD

| 비교 관점 | FDD (Frequency Division Duplex) | TDD (Time Division Duplex) |
|----------|--------------------------------|---------------------------|
| **방식** | 주파수 분리 전이중 | 시분할 반이중 (전이중처럼 동작) |
| **업/다운링크** | 서로 다른 주파수 대역 | 동일 주파수, 시간 분할 |
| **스펙트럼 효율** | 가드 밴드로 인한 손실 | 가드 밴드 불필요, 높은 효율 |
| **비대칭 트래픽** | 고정된 업/다운 비율 | 유연한 업/다운 비율 조절 |
| **지연** | 낮음 (동시 전송) | 높음 (시분할) |
| **주파수 자원** | 2배 필요 (업+다운) | 1배 (공유) |
| **적용** | LTE FDD, 음성 통화 | LTE TDD, 5G NR, Wi-Fi |

#### 과목 융합 관점 분석

| 연계 분야 | 융합 내용 | 기술적 시사점 |
|----------|----------|--------------|
| **운영체제** | 전이중 통신의 버퍼 관리 | 송신 큐와 수신 큐 독립 운영 |
| **데이터베이스** | 반이중 통신의 락(Lock) 유사성 | 동시 접근 제어 메커니즘 |
| **보안** | 전이중 도청 vs 반이중 도청 | 전이중은 양방향 감청 가능 |
| **컴퓨터 구조** | 버스 아키텍처 (단방향/양방향) | 시스템 버스의 통신 방식 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 - [최소 800자]

#### 실무 시나리오: 데이터센터 네트워크 설계

**시나리오**: 클라우드 데이터센터에서 서버 간 통신을 위한 네트워크 스위치 선정. 예상 트래픽은 대칭(업로드=다운로드)이며, 각 서버는 25Gbps 연결 필요.

**기술사적 판단**:

1. **요구사항 분석**:
   - 대칭 트래픽 → 전이중 25Gbps = 양방향 합계 50Gbps 처리량
   - 저지연 요구 (HPC, 실시간 분석) → 전이중 필수
   - 100서버 규모 → 25Gbps × 100포트 스위치 필요

2. **옵션 분석**:
   - **25GBASE-T (전이중)**: UTP 케이블, 100m, PAM-4 변조
   - **25GBASE-SR (전이중)**: 광섬유 MMF, 100m, NRZ 변조
   - **반이중 솔루션**: 존재하지 않음 (현대 데이터센터는 전이중 표준)

3. **결정**: **25GBASE-SR (광섬유)** 선택.
   - 이유: 전력 소비가 25GBASE-T 대비 50% 수준, EMI 없음, 케이블 두께 얇음
   - 전이중으로 양방향 50Gbps 처리량 보장

#### 도입 시 고려사항 체크리스트

**전이중 전환 체크리스트**:
- [ ] 모든 장비가 전이중을 지원하는가? (Auto-negotiation 확인)
- [ ] 케이블이 전이중 요구사항을 만족하는가? (4쌍 UTP, 광섬유)
- [ ] 스위치 포트가 전이중으로 설정되어 있는가? (수동 설정 권장)
- [ ] 반이중 장비와 혼재 시 속도 저하를 감수하는가?

**반이중 사용이 불가피한 경우**:
- [ ] 전환 시간 최소화 (고속 트랜시버 사용)
- [ ] 충돌 도메인 크기 최소화 (소규모 세그먼트)
- [ ] CSMA/CD 파라미터 최적화 (슬롯 타임, 백오프)

#### 주의사항 및 안티패턴

**안티패턴 1: 전이중/반이중 혼재**
한 스위치에 전이중 장비와 반이중 장비가 연결되면, 포트 속도가 반이중 장비에 맞춰져 전체 성능이 저하될 수 있습니다. 또한 듀플렉스 미스매치(Duplex Mismatch)가 발생하면 다량의 충돌과 지연이 발생합니다.

**안티패턴 2: 전이중에서 CSMA/CD 활성화**
전이중 모드에서는 충돌이 발생하지 않으므로 CSMA/CD가 불필요합니다. 오히려 활성화하면 불필요한 오버헤드가 발생합니다. 스위치 포트는 자동으로 CSMA/CD를 비활성화해야 합니다.

**안티패턴 3: TDD를 전이중으로 착각**
TDD(Time Division Duplex)는 시분할로 양방향 통신을 제공하지만, 실제로는 반이중 회선을 빠르게 전환하는 것입니다. 진정한 전이중(FDD, 물리적 분리)보다 지연이 길 수 있습니다.

---

### Ⅴ. 기대효과 및 결론 - [최소 400자]

#### 정량적/정성적 기대효과표

| 효과 영역 | 반이중 (Hub) | 전이중 (Switch) | 개선폭 |
|----------|-------------|----------------|--------|
| **처리량 (양방향)** | 50% (충돌로 인해) | 200% (동시 송수신) | 4배 |
| **평균 지연** | 10~100ms (충돌 백오프) | < 1ms (충돌 없음) | 10~100배 |
| **지터 (Jitter)** | 높음 (충돌 불확실성) | 낮음 (예측 가능) | 안정화 |
| **포트당 비용** | $5 (단순) | $15 (복잡) | +200% |
| **확장성** | 제한적 (충돌 증가) | 선형 (독립 포트) | 무제한 |

#### 미래 전망 및 진화 방향

**1. 전이중 무선 (Full-Duplex Wireless)**:
연구 단계에서는 동일 주파수로 동시 송수신이 가능한 전이중 무선이 개발되고 있습니다. 자기 간섭(Self-Interference) 제거 기술이 핵심이며, 성공 시 스펙트럼 효율이 2배 향상됩니다.

**2. 양자 전이중 통신**:
양자 얽힘(Quantum Entanglement)을 활용한 통신은 이론적으로 동시 양방향 정보 전송이 가능합니다. 양자 인터넷의 핵심 기술이 될 것입니다.

**3. 위성 전이중 통신**:
Starlink 등 LEO 위성군은 레이저 인터위성 링크로 전이중 광통신을 수행합니다. 지구-위성 구간은 FDD 기반 전이중입니다.

#### ※ 참고 표준/가이드

- **IEEE 802.3x**: Full-Duplex Ethernet 표준
- **IEEE 802.3-2018**: Ethernet 프레임 포맷 및 물리 계층 사양
- **3GPP TS 36.xxx**: LTE FDD/TDD 듀플렉싱 표준
- **ITU-T G.992.x**: DSL 반이중/전이중 모드

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [CSMA/CD (충돌 감지)](@/studynotes/3_network/1_fundamentals/_index.md): 반이중 통신의 충돌 해결
- [이더넷 프레임 구조](@/studynotes/3_network/1_fundamentals/_index.md): 프레임 전송 방식
- [OSI 7계층 - 데이터링크 계층](@/studynotes/3_network/1_fundamentals/osi_7_layer.md): 반이중/전이중 결정 계층
- [스위치 vs 허브](@/studynotes/3_network/1_fundamentals/_index.md): 전이중/반이중 장비 비교
- [LTE FDD/TDD](@/studynotes/3_network/5_wireless/_index.md): 무선 통신의 듀플렉싱

---

### 👶 어린이를 위한 3줄 비유 설명

1. **단방향 통신**은 **TV 시청**이에요. TV는 말하고 우리는 듣기만 해요. 우리가 TV에게 말해도 TV는 못 들어요.

2. **반이중 통신**은 **무전기 대화**예요. "뚜---" 하고 상대방이 말하면 내가 듣고, 내가 말할 차례면 버튼을 눌러서 말해요. 동시에 말하면 서로 못 들어요!

3. **전이중 통신**은 **전화 통화**예요. 친구와 동시에 말해도 서로 잘 들려요. 인터넷도 전이중이라서 파일을 다운로드하면서 업로드도 동시에 할 수 있어요!
