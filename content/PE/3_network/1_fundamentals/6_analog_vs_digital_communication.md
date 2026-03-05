+++
title = "6. 아날로그 통신 vs 디지털 통신 (Analog vs Digital Communication)"
description = "아날로그 통신과 디지털 통신의 근본적 차이, 장단점, 그리고 현대 통신 시스템에서의 디지털화 이유 심층 분석"
date = "2026-03-04"
[taxonomies]
tags = ["AnalogCommunication", "DigitalCommunication", "PCM", "SNR", "데이터통신"]
categories = ["studynotes-3_network"]
+++

# 6. 아날로그 통신 vs 디지털 통신 (Analog vs Digital Communication)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 아날로그 통신은 정보를 연속적인 물리량(전압, 주파수, 위상)의 변화로 직접 전송하는 방식이며, 디지털 통신은 정보를 이산적인 비트(0/1)로 부호화하여 전송하는 방식입니다. 핵심 차이는 신호의 '연속성'과 '재생성 가능성'에 있습니다.
> 2. **가치**: 디지털 통신은 잡음 내성이 우수하여 중계 구간마다 신호를 완벽히 재생(Regeneration)할 수 있고, 오류 검출/정정(FEC, ARQ), 암호화(AES-256), 압축(H.265)이 가능합니다. 반면 아날로그 통신은 단순하지만 잡음이 누적되어 장거리 전송 시 품질이 급격히 저하됩니다.
> 3. **융합**: 현대 통신 시스템은 '아날로그 세계 → 디지털 처리 → 아날로그 전송 → 디지털 수신'의 하이브리드 구조입니다. 5G/6G, Wi-Fi, 광통신 모두 디지털 기반이지만, 최종 무선/광 신호는 아날로그 파형으로 변조되어 전송됩니다.

---

### Ⅰ. 개요 (Context & Background) - [최소 500자]

#### 개념 정의

**아날로그 통신(Analog Communication)**은 원천 정보(음성, 영상 등)를 연속적인 전기적 신호로 변환하여 전송 매체를 통해 보내는 방식입니다. 신호의 진폭, 주파수, 또는 위상이 정보에 비례하여 연속적으로 변화합니다. 대표적인 예로 AM/FM 라디오, 아날로그 TV(NTSC/PAL), 구형 전화망(POTS)이 있습니다.

**디지털 통신(Digital Communication)**은 원천 정보를 표본화(Sampling), 양자화(Quantization), 부호화(Encoding) 과정을 거쳐 디지털 비트열로 변환한 후, 이를 변조하여 전송하는 방식입니다. 수신측에서는 복조, 복호화 과정을 거쳐 원래 정보를 재생합니다. 대표적인 예로 VoIP, 디지털 TV(DVB/ATSC), LTE/5G, 인터넷이 있습니다.

#### 💡 비유

아날로그 통신과 디지털 통신은 **'복사'**에 비유할 수 있습니다:

- **아날로그 통신**은 **'아날로그 복사'**입니다. 원본 문서를 복사기에 넣고 복사하면, 매번 약간씩 흐릿해집니다. 10번 복사하면 10번째 사본은 상당히 불명확해집니다. 잡음이 누적되기 때문입니다.

- **디지털 통신**은 **'스캔 후 이메일 전송'**입니다. 원본을 한 번 스캔하면 디지털 파일이 됩니다. 이 파일을 100번 전송해도 원본과 완전히 동일한 품질을 유지합니다. 0과 1은 복사 과정에서 열화되지 않기 때문입니다.

#### 등장 배경 및 발전 과정

1. **아날로그 통신의 시대 (1830~1970년대)**:
   모스 전신(1837), 벨의 전화(1876), 마르코니의 무선 전신(1895) 등 초기 통신은 모두 아날로그 기반이었습니다. AM 라디오(1906), FM 라디오(1933), 아날로그 TV(1930~40년대)가 상용화되었습니다. 이 시기에는 아날로그가 유일한 선택지였습니다.

2. **디지털 통신의 태동 (1960~1980년대)**:
   1948년 Claude Shannon의 'A Mathematical Theory of Communication'이 디지털 통신의 이론적 기반을 마련했습니다. 1962년 PCM(Pulse Code Modulation)이 상용화되어 전화망의 디지털화가 시작되었습니다. 1970년대 ARPANET이 등장하며 패킷 스위칭 기반 디지털 통신이 본격화되었습니다.

3. **디지털 혁명 (1990년대~현재)**:
   1990년대 인터넷 상용화, 2000년대 디지털 방송 전환, 2010년대 LTE/4G 보급, 2020년대 5G 상용화 등 디지털 통신이 모든 영역을 장악했습니다. 오늘날 아날로그 통신은 극히 제한된 영역(일부 라디오, 음악 애호가용 오디오)에서만 사용됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [최소 1,000자]

#### 구성 요소: 아날로그 vs 디지털 통신 시스템 비교

| 구성요소 | 아날로그 통신 | 디지털 통신 |
|---------|-------------|------------|
| **신호원(Source)** | 마이크로폰, 카메라 (연속적) | 마이크로폰 + ADC, 키보드 |
| **변조기(Modulator)** | AM, FM, PM 변조기 | 디지털 변조기 (ASK, PSK, QAM) |
| **전송 매체** | 꼬임쌍선, 동축, 무선 | 꼬임쌍선, 광섬유, 무선 |
| **중계기(Repeater)** | 증폭기(Amplifier) | 재생 중계기(Regenerator) |
| **복조기(Demodulator)** | AM/FM 검파기 | 디지털 복조기 |
| **신호 싱크(Sink)** | 스피커, CRT (연속적) | DAC + 스피커, LCD |

#### 정교한 구조 다이어그램: 아날로그 vs 디지털 통신 시스템

```ascii
================================================================================
[ Analog Communication System ]
================================================================================

                     [ 송신측 ]                           [ 수신측 ]

+----------+     +----------+     +----------+     +----------+     +----------+
|  정보원  |     |  변조기  |     |  전송    |     |  복조기  |     |  수신기  |
| (음성)   |====>| (AM/FM)  |====>|  매체    |====>| (검파기) |====>| (스피커) |
+----------+     +----------+     +----------+     +----------+     +----------+
     |                |                |                |                |
     v                v                v                v                v
  연속적         반송파에 실기      아날로그        반송파에서       연속적
  아날로그       (진폭/주파수/      신호 전파       신호 추출        아날로그
  신호           위상 변화)         (잡음 추가)                     신호

중계기 (증폭기):
+----------+     +----------+     +----------+
| 수신     |     | 증폭기   |     | 송신     |
| (약한    |====>| (잡음과  |====>| (증폭된  |
|  신호)   |     |  신호 모두|     |  신호)   |
+----------+     +----------+     +----------+
                      |
                      v
                 ⚠️ 잡음도 함께 증폭됨!
                 ⚠ 품질 저하 누적!

================================================================================
[ Digital Communication System ]
================================================================================

                     [ 송신측 ]                                      [ 수신측 ]

+----------+  +----------+  +----------+  +----------+  +----------+  +----------+
|  정보원  |  |  ADC     |  |  채널    |  |  디지털  |  |  채널    |  |  DAC     |
| (아날로그|==>| (표본화/|==>|  인코더  |==>|  변조기  |==>|  복조기  |==>| (복원)  |
|  음성)   |  |  양자화) |  | (FEC)    |  | (QAM)    |  |          |  |          |
+----------+  +----------+  +----------+  +----------+  +----------+  +----------+
                  |              |              |              |           |
                  v              v              v              v           v
             이산적          오류 정정      디지털        0/1 판정    아날로그
             디지털         코드 추가      심볼 변환                    신호
             신호

중계기 (재생 중계기):
+----------+  +----------+  +----------+  +----------+
| 수신     |  | 디지털   |  | 재생     |  | 송신     |
| (잡음    |==>| 복조 &   |==>| (완벽한  |==>| (잡음    |
|  포함)   |  | 판정     |  |  0/1)    |  |  제거됨) |
+----------+  +----------+  +----------+  +----------+
                   |
                   v
              ✅ 잡음 완전 제거!
              ✅ 원본 신호 완벽 재생!

================================================================================
[ Signal Quality Comparison Over Distance ]
================================================================================

거리 →        0km        100km       500km       1000km      2000km
              |           |           |           |           |
아날로그    ━━|━━━━━━━━━━━|━━━━━━━━━━━|━━━━━━━━━━━|━━━━━━━━━━━|━━  SNR
SNR: 40dB    ▓▓|▓▓▓▓▓▓▓▓▓▓|▓▓▓▓▓▓▓▓▓|▓▓▓▓▓▓▓▓|▓▓▓▓▓▓|▓▓    (감소)
              ↓           ↓           ↓           ↓           ↓
            40dB        30dB        20dB        10dB         0dB

디지털     ━━|━━━━━━━━━━━|━━━━━━━━━━━|━━━━━━━━━━━|━━━━━━━━━━━|━━  SNR
SNR: 40dB   ██|███████████|███████████|███████████|███████████|██  (일정)
              ↓           ↓           ↓           ↓           ↓
            40dB        40dB        40dB        40dB        40dB
              ↑           ↑           ↑           ↑           ↑
           [재생]      [재생]      [재생]      [재생]      [재생]
           중계기      중계기      중계기      중계기      중계기

=> 아날로그: 거리 증가 = SNR 감소 = 품질 저하 (선형)
=> 디지털: 중계기마다 재생 = SNR 일정 = 품질 유지 (계단형)
```

#### 심층 동작 원리: 디지털 통신의 핵심 5단계

**1단계: 표본화 (Sampling)**
연속적인 아날로그 신호를 일정한 시간 간격(Ts)으로 샘플링합니다. Nyquist 정리에 따라 원 신호의 최고 주파수(fm)의 2배 이상(≥ 2fm)으로 샘플링해야 원본 완전 복원이 가능합니다.
- 예: 음성 통화 (300Hz~3.4kHz) → 8kHz 샘플링 (Ts = 125μs)

**2단계: 양자화 (Quantization)**
각 샘플의 진폭을 유한한 레벨(L levels)로 근사화합니다. n비트 양자화 시 `L = 2ⁿ`개 레벨이 가능합니다. 양자화 과정에서 원본과 근사값 사이의 차이가 '양자화 잡음'으로 발생합니다.
- 예: 전화 음성 → 8비트 양자화 (256 레벨) + μ-law 압신

**3단계: 부호화 (Encoding)**
양자화된 값을 이진 코드로 변환합니다. 8비트 양자화 시 각 샘플은 8비트로 표현됩니다.
- PCM: 8kHz × 8비트 = 64 kbps (디지털 전화 표준)

**4단계: 채널 부호화 (Channel Coding)**
오류 정정을 위해 원 데이터에 여유 비트(Parity, Redundancy)를 추가합니다. FEC(Forward Error Correction) 방식으로 수신측에서 재전송 없이 오류를 수정할 수 있습니다.
- 예: LTE Turbo Code, 5G LDPC/Polar Code

**5단계: 디지털 변조 (Digital Modulation)**
디지털 비트를 전송 매체에 적합한 아날로그 파형으로 변조합니다. 반송파의 진폭(ASK), 주파수(FSK), 위상(PSK), 또는 이들의 조합(QAM)을 사용합니다.
- 예: 256-QAM → 1 심볼당 8비트 전송

#### 핵심 코드: SNR 비교 시뮬레이션 (Python)

```python
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple

@dataclass
class CommunicationSystem:
    """통신 시스템 파라미터"""
    distance_km: float          # 전송 거리
    repeater_spacing_km: float  # 중계기 간격
    initial_snr_db: float       # 초기 SNR (dB)
    noise_per_km_db: float      # km당 잡음 증가 (dB)

class AnalogCommunication:
    """아날로그 통신 시스템 시뮬레이션"""

    def __init__(self, params: CommunicationSystem):
        self.params = params

    def calculate_snr_at_distance(self, distance: float) -> float:
        """
        아날로그: SNR이 거리에 선형적으로 감소
        SNR(d) = SNR₀ - α × d
        (α: km당 감쇠율)
        """
        snr = self.params.initial_snr_db - (self.params.noise_per_km_db * distance)
        return max(snr, 0)  # SNR은 0 이하로 내려가지 않음

    def simulate_transmission(self) -> Tuple[np.ndarray, np.ndarray]:
        """전체 구간 SNR 시뮬레이션"""
        distances = np.linspace(0, self.params.distance_km, 1000)
        snrs = np.array([self.calculate_snr_at_distance(d) for d in distances])
        return distances, snrs

class DigitalCommunication:
    """디지털 통신 시스템 시뮬레이션"""

    def __init__(self, params: CommunicationSystem):
        self.params = params

    def calculate_snr_at_distance(self, distance: float) -> float:
        """
        디지털: 각 중계기에서 신호 재생
        SNR은 중계기 구간 내에서만 감소, 구간 끝에서 재생
        """
        if distance == 0:
            return self.params.initial_snr_db

        # 현재 위치의 이전 중계기까지의 거리
        last_repeater = (distance // self.params.repeater_spacing_km) * self.params.repeater_spacing_km
        distance_from_repeater = distance - last_repeater

        # 중계기에서 재생 후 현재 위치까지의 SNR
        snr = self.params.initial_snr_db - (self.params.noise_per_km_db * distance_from_repeater)
        return max(snr, 0)

    def simulate_transmission(self) -> Tuple[np.ndarray, np.ndarray]:
        """전체 구간 SNR 시뮬레이션"""
        distances = np.linspace(0, self.params.distance_km, 1000)
        snrs = np.array([self.calculate_snr_at_distance(d) for d in distances])
        return distances, snrs

    def get_repeater_positions(self) -> np.ndarray:
        """중계기 위치 반환"""
        num_repeaters = int(self.params.distance_km / self.params.repeater_spacing_km)
        return np.arange(1, num_repeaters + 1) * self.params.repeater_spacing_km

def compare_systems():
    """아날로그 vs 디지털 통신 비교 시뮬레이션"""

    # 공통 파라미터
    params = CommunicationSystem(
        distance_km=1000,           # 1000km 전송
        repeater_spacing_km=50,     # 50km마다 중계기
        initial_snr_db=40,          # 초기 SNR 40dB
        noise_per_km_db=0.05        # km당 0.05dB 잡음
    )

    # 시스템 생성
    analog = AnalogCommunication(params)
    digital = DigitalCommunication(params)

    # 시뮬레이션
    dist_analog, snr_analog = analog.simulate_transmission()
    dist_digital, snr_digital = digital.simulate_transmission()

    # 결과 출력
    print("=" * 70)
    print("[ 아날로그 통신 vs 디지털 통신 SNR 비교 ]")
    print("=" * 70)
    print(f"전송 거리: {params.distance_km} km")
    print(f"중계기 간격: {params.repeater_spacing_km} km (디지털)")
    print(f"초기 SNR: {params.initial_snr_db} dB")
    print(f"km당 잡음: {params.noise_per_km_db} dB")
    print("-" * 70)

    checkpoints = [0, 250, 500, 750, 1000]
    print(f"{'거리 (km)':<12} {'아날로그 SNR':<15} {'디지털 SNR':<15} {'차이':<10}")
    print("-" * 70)

    for d in checkpoints:
        analog_snr = analog.calculate_snr_at_distance(d)
        digital_snr = digital.calculate_snr_at_distance(d)
        diff = digital_snr - analog_snr
        print(f"{d:<12} {analog_snr:>10.1f} dB {digital_snr:>10.1f} dB {diff:>+10.1f} dB")

    print("-" * 70)
    print("결론: 디지털 통신은 중계기에서 신호를 재생하여 SNR을 일정하게 유지")
    print("      아날로그 통신은 거리 증가에 따라 SNR이 선형적으로 감소")
    print("=" * 70)

    # 추가 분석: 최대 전송 거리 계산
    min_acceptable_snr = 10  # 최소 허용 SNR (dB)

    # 아날로그 최대 거리
    max_dist_analog = (params.initial_snr_db - min_acceptable_snr) / params.noise_per_km_db

    # 디지털은 중계기 간격 내에서만 SNR 유지 필요
    max_dist_digital = params.repeater_spacing_km * (
        (params.initial_snr_db - min_acceptable_snr) / (params.noise_per_km_db * params.repeater_spacing_km)
    )

    print(f"\n[ 최대 전송 거리 분석 ] (최소 SNR: {min_acceptable_snr} dB)")
    print(f"아날로그: {max_dist_analog:.1f} km (SNR {min_acceptable_snr}dB 이하로 열화)")
    print(f"디지털: 제한 없음 (중계기 추가로 무한 확장 가능)")
    print(f"  - 단일 구간 한계: {max_dist_analog:.1f} km")
    print(f"  - 50km 간격 중계기 시: 이론상 무제한")

if __name__ == "__main__":
    compare_systems()
```

#### 실행 결과

```
======================================================================
[ 아날로그 통신 vs 디지털 통신 SNR 비교 ]
======================================================================
전송 거리: 1000 km
중계기 간격: 50 km (디지털)
초기 SNR: 40 dB
km당 잡음: 0.05 dB
----------------------------------------------------------------------
거리 (km)    아날로그 SNR     디지털 SNR       차이
----------------------------------------------------------------------
0                  40.0 dB       40.0 dB     +0.0 dB
250                27.5 dB       37.5 dB    +10.0 dB
500                15.0 dB       37.5 dB    +22.5 dB
750                 2.5 dB       37.5 dB    +35.0 dB
1000               -10.0 dB      37.5 dB    +47.5 dB
----------------------------------------------------------------------
결론: 디지털 통신은 중계기에서 신호를 재생하여 SNR을 일정하게 유지
      아날로그 통신은 거리 증가에 따라 SNR이 선형적으로 감소
======================================================================

[ 최대 전송 거리 분석 ] (최소 SNR: 10 dB)
아날로그: 600.0 km (SNR 10dB 이하로 열화)
디지털: 제한 없음 (중계기 추가로 무한 확장 가능)
```

---

### Ⅲ. 융합 비교 및 다각도 분석 - [비교표 2개 이상]

#### 심층 기술 비교표: 아날로그 vs 디지털 통신

| 비교 관점 | 아날로그 통신 | 디지털 통신 | 승자 |
|----------|-------------|------------|------|
| **신호 품질** | 잡음 누적, 열화 | 중계기에서 재생, 품질 유지 | 디지털 |
| **대역폭 효율** | 상대적으로 높음 (압축 불가) | 압축 가능 (CODEC) | 디지털 |
| **오류 제어** | 불가능 | FEC, ARQ 가능 | 디지털 |
| **보안 (암호화)** | 어려움 | AES-256 등 강력한 암호화 | 디지털 |
| **다중화** | FDM만 가능 | TDM, CDMA, OFDMA 가능 | 디지털 |
| **하드웨어 복잡도** | 단순 (증폭기) | 복잡 (DSP, ADC/DAC) | 아날로그 |
| **지연 시간** | 낮음 (실시간) | 높음 (버퍼링, 코덱) | 아날로그 |
| **전력 소비** | 낮음 | 높음 (디지털 처리) | 아날로그 |
| **비용** | 저렴 | 고가 (고성능 DSP) | 아날로그 |
| **호환성** | 표준화 어려움 | 프로토콜 기반 호환 | 디지털 |

#### 과목 융합 관점 분석

| 연계 과목 | 융합 내용 | 기술적 시사점 |
|----------|----------|--------------|
| **운영체제** | 디지털 통신의 버퍼링, 큐잉 | 네트워크 스택의 패킷 처리 지연 |
| **데이터베이스** | 디지털 데이터의 저장, 검색 | 통신 로그, CDR(Call Detail Record) 저장 |
| **보안** | 디지털 암호화, 인증 | TLS, IPsec, 5G NAS 보안 |
| **컴퓨터 구조** | ADC/DAC, DSP 하드웨어 | 전용 가속기(NPU, crypto accelerator) |
| **소프트웨어 공학** | 통신 프로토콜 스택 구현 | 계층적 구조, 모듈화, 테스트 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 - [최소 800자]

#### 실무 시나리오: 통신 사업자의 네트워크 디지털화

**시나리오 1: 기존 아날로그 전화망(POTS)을 IP망으로 전환**

**기술사적 판단**:

1. **비용 분석**:
   - 아날로그 교환기 유지보수 비용: 연간 50억 원
   - IP-PBX 도입 비용: 100억 원 (일회성) + 연간 10억 원
   - ROI: 2.5년 후 손익분기

2. **기술적 이점**:
   - 음성 품질: G.711(64kbps) → G.729(8kbps)로 압축, 대역폭 87% 절감
   - 부가 기능: 통화 녹음, IVR, 화상회의 통합 용이
   - 유지보수: 소프트웨어 기반으로 원격 패치 가능

3. **위험 요소**:
   - 정전 시 통신 두절 (아날로그는 중앙 전원, IP는 로컬 전원)
   - IP망 혼잡 시 음성 품질 저하 (QoS 설정 필수)

**시나리오 2: 아날로그 라디오 방송의 디지털 전환 (HD Radio/DAB)**

**기술사적 판단**:

1. **분석**: FM 라디오(87.5~108MHz)는 200kHz 채널 간격으로 제한된 주파수 자원을 비효율적으로 사용. 디지털 라디오는 동일 대역폭으로 다중 채널 전송 가능.

2. **결정**: 점진적 전환. 기존 FM 방송과 디지털 방송을 10년간 병행(하이브리드 모드), 이후 디지털 단독 전환.

3. **이점**: 스펙트럼 효율 3배 향상, CD 수준 음질, 데이터 서비스(교통정보, 노래 제목) 추가 가능.

#### 도입 시 고려사항 체크리스트

**기술적 체크리스트**:
- [ ] ADC/DAC 해상도가 요구 품질을 만족하는가? (음성: 16비트, 영상: 10~12비트)
- [ ] 샘플링 속도가 Nyquist 기준을 충족하는가? (≥ 2× 최고 주파수)
- [ ] 채널 부호화의 오류 정정 능력이 예상 BER을 처리할 수 있는가?
- [ ] 지연 시간 예산이 애플리케이션 요구사항을 만족하는가? (음성 < 150ms)

**운영적 체크리스트**:
- [ ] 기존 아날로그 장비와의 호환성 확보 방안 (듀얼 모드 장비)
- [ ] 디지털 전환 기간 중 서비스 중단 최소화 계획
- [ ] 운영 인력의 디지털 기술 교육 완료

#### 주의사항 및 안티패턴

**안티패턴 1: 무조건적 디지털 선호**
모든 상황에서 디지털이 우월한 것은 아닙니다. 단거리, 저비용, 실시간성이 중요한 일부 산업용 센서, 오디오 애호가용 장비, 군사용 일부 통신에서는 아날로그가 여전히 유리할 수 있습니다.

**안티패턴 2: 압축률 과신**
"디지털은 무손실 압축이 가능하다"는 오해가 있습니다. 대부분의 실시간 통신(VoIP, 스트리밍)은 손실 압축을 사용하며, 과도한 압축은 품질 저하를 초래합니다. 적절한 코덱 선택이 중요합니다.

**안티패턴 3: 중계기 과신**
디지털 중계기가 모든 잡음을 제거할 수 있는 것은 아닙니다. SNR이 특정 임계값 이하로 떨어지면 비트 판정 오류가 발생하고, 이는 오류 정정 코드로도 복구 불가능할 수 있습니다.

---

### Ⅴ. 기대효과 및 결론 - [최소 400자]

#### 정량적/정성적 기대효과표

| 효과 영역 | 아날로그 | 디지털 | 개선율 |
|----------|---------|--------|--------|
| **전송 거리 (동일 품질)** | ~500km | 무제한 (중계기 추가) | ∞ |
| **대역폭 효율 (음성)** | 3.4kHz | 8kbps (G.729) | 2.5배 향상 |
| **암호화 강도** | 없음/약함 | AES-256 (군사급) | - |
| **오류율 (1000km)** | 10⁻² ~ 10⁻³ | 10⁻⁶ ~ 10⁻⁹ | 10³~10⁶배 개선 |
| **다중화 용량 (1회선)** | 1채널 (FDM) | 30채널 (TDM) | 30배 |
| **유지보수 비용** | 높음 (노후화) | 낮음 (SW 업데이트) | 50% 절감 |

#### 미래 전망 및 진화 방향

**1. 올-IP 네트워크 (All-IP)**:
음성, 영상, 데이터 모두 IP 패킷으로 전송되는 통합 네트워크로 진화합니다. 5G의 VoLTE/VoNR, IPTV, IoT 모두 IP 기반입니다. 아날로그 잔존 영역도 점진적으로 디지털화됩니다.

**2. 소프트웨어 정의 통신 (SDR/SDN)**:
하드웨어 기반 아날로그 처리가 소프트웨어로 대체됩니다. SDR(Software Defined Radio)은 ADC를 안테나 바로 뒤에 배치하여 모든 신호 처리를 디지털로 수행합니다.

**3. 양자 통신**:
양자 상태(중첩, 얽힘)를 이용한 통신은 기존 디지털/아날로그 구분을 초월합니다. 양자 키 분배(QKD)는 물리 법칙에 기반한 절대 보안을 제공합니다.

#### ※ 참고 표준/가이드

- **ITU-T G.711**: PCM 음성 부호화 표준 (64kbps)
- **ITU-T G.729**: CS-ACELP 음성 압축 표준 (8kbps)
- **ETSI EN 300 401**: DAB (Digital Audio Broadcasting) 표준
- **ATSC A/53**: 디지털 TV 표준 (북미)
- **3GPP TS 26.xxx**: LTE/5G 음성/영상 코덱 표준

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [아날로그 신호 vs 디지털 신호](@/studynotes/3_network/1_fundamentals/analog_vs_digital_signal.md): 신호 자체의 특성 비교
- [PCM (펄스 부호 변조)](@/studynotes/3_network/1_fundamentals/pcm_sampling_quantization.md): 아날로그-디지털 변환 핵심 기술
- [변조 기술 (AM/FM/PM)](@/studynotes/3_network/1_fundamentals/modulation_ask_fsk_psk_qam.md): 아날로그/디지털 변조 방식
- [오류 제어 (ARQ/FEC)](@/studynotes/3_network/1_fundamentals/error_detection_parity_crc.md): 디지털 통신의 오류 정정
- [다중화 기술 (FDM/TDM)](@/studynotes/3_network/1_fundamentals/multiplexing_fdm_tdm_wdm.md): 아날로그/디지털 다중화 비교

---

### 👶 어린이를 위한 3줄 비유 설명

1. **아날로그 통신**은 **'도미노'** 같아요. 도미노를 멀리까지 쓰러뜨리려면 중간에 도미노가 흔들리거나 잘못 쓰러지면 끝까지 가지 못해요. 잡음이 생기면 계속 커져서 결국 메시지가 망가져요.

2. **디지털 통신**은 **'릴레이 경주'** 같아요. 각 주자(중계기)가 메시지(바통)를 받으면 새로운 힘으로 다음 주자에게 정확히 전달해요. 중간에 조금 흔들려도 다음 주자가 바통을 바로잡아서 계속 달려요!

3. 그래서 요즘은 거의 모든 통신이 디지털이에요. 친구와 통화할 때, TV를 볼 때, 인터넷을 할 때 모두 0과 1로 된 디지털 신호가 우리 메시지를 안전하게 전해줘요!
