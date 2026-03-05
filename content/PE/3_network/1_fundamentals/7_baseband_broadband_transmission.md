+++
title = "7. 기저대역 전송 / 대역통과 전송 (Baseband / Broadband Transmission)"
description = "기저대역 전송과 대역통과 전송의 원리, 장단점, 그리고 LAN/WAN 환경에서의 적용 기술 심층 분석"
date = "2026-03-04"
[taxonomies]
tags = ["Baseband", "Broadband", "Transmission", "Ethernet", "Modulation", "데이터통신"]
categories = ["studynotes-3_network"]
+++

# 7. 기저대역 전송 / 대역통과 전송 (Baseband / Broadband Transmission)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 기저대역(Baseband) 전송은 디지털 신호를 변조 없이 원래의 주파수 대역(0Hz~최고 주파수) 그대로 전송하는 방식이며, 대역통과(Broadband/Passband) 전송은 신호를 높은 반송파 주파수대로 변조하여 전송하는 방식입니다. 핵심 차이는 '변조 유무'와 '주파수 대역 위치'에 있습니다.
> 2. **가치**: 기저대역 전송은 구현이 단순하고 지연이 적어 LAN(Ethernet), USB, SATA 등 단거리 고속 전송에 유리합니다. 대역통과 전송은 주파수 분할 다중화(FDM)로 여러 신호를 한 매체에 동시 전송 가능하여 케이블 TV, 무선 통신, 광통신(WDM)에 필수적입니다.
> 3. **융합**: 현대 통신 시스템은 두 방식을 결합합니다. 이더넷은 기저대역이지만, 1000BASE-T는 PAM-5 변조를 사용하고, 10GBASE-T는 4차원 PAM-16을 사용하여 사실상 대역통과 특성을 띱니다. DSL, DOCSIS, 5G는 완전한 대역통과 시스템입니다.

---

### Ⅰ. 개요 (Context & Background) - [최소 500자]

#### 개념 정의

**기저대역 전송(Baseband Transmission)**은 정보 신호를 변조(Modulation) 과정 없이, 원래의 주파수 성분 그대로 전송 매체에 실어 보내는 방식입니다. 디지털 신호의 경우 0과 1을 나타내는 전압 펄스(NRZ, Manchester 등)가 직접 케이블을 통해 전송됩니다. 신호의 에너지는 DC(0Hz)부터 신호 대역폭의 최고 주파수까지 분포합니다.

**대역통과 전송(Broadband/Passband Transmission)**은 정보 신호를 반송파(Carrier)라는 높은 주파수에 실어 변조한 후 전송하는 방식입니다. 신호의 에너지는 반송파 주파수(fc)를 중심으로 특정 대역폭(B) 내에 집중됩니다. 여러 신호를 서로 다른 반송파 주파수에 실어 한 매체로 동시 전송(FDM)할 수 있습니다.

#### 💡 비유

기저대역 전송과 대역통과 전송은 **'말하기'** 방식에 비유할 수 있습니다:

- **기저대역 전송**은 **'보통 목소리로 말하기'**입니다. 내 목소리의 원래 주파수(남자 기준 85~180Hz, 여자 165~255Hz) 그대로 말합니다. 한 번에 한 사람만 말할 수 있고, 멀리 들리지 않습니다. 하지만 간단하고 자연스럽습니다.

- **대역통과 전송**은 **'라디오 방송국을 통해 말하기'**입니다. 내 목소리를 특정 라디오 주파수(예: FM 95.9MHz)에 실어 보냅니다. 여러 방송국이 각자 다른 주파수(92.1MHz, 95.9MHz, 101.3MHz)로 동시에 방송할 수 있습니다. 멀리까지 전달되지만, 송신기와 수신기가 필요합니다.

#### 등장 배경 및 발전 과정

1. **기저대역 전송의 등장 (1960~70년대)**:
   초기 컴퓨터 네트워크는 단거리 연결이 주목적이었습니다. 1973년 Xerox PARC의 Robert Metcalfe가 개발한 Ethernet(10BASE5)은 기저대역 전송을 사용하여 동축 케이블에 디지털 펄스를 직접 전송했습니다. 구현이 간단하고 비용이 저렴하여 LAN 표준으로 자리잡았습니다.

2. **대역통과 전송의 필요성 (1970~80년대)**:
   케이블 TV(CATV) 산업이 성장하면서 한 케이블에 여러 TV 채널을 동시 전송해야 했습니다. 이를 위해 FDM 기반 대역통과 전송이 도입되었습니다. 전화망의 디지털화를 위해 DSL(Digital Subscriber Line)도 대역통과 변조(DMT)를 사용합니다.

3. **현대적 융합 (1990년대~현재)**:
   고속 이더넷(1Gbps, 10Gbps)은 대역폭 효율을 높이기 위해 다단 변조(PAM)를 사용하며, 이는 대역통과와 유사한 특성을 갖습니다. 광통신의 WDM, 무선의 OFDM은 완전한 대역통과 시스템입니다. 두 방식의 경계가 모호해지고 있습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive) - [최소 1,000자]

#### 구성 요소: 기저대역 vs 대역통과 전송 시스템

| 구성요소 | 기저대역 전송 (Baseband) | 대역통과 전송 (Broadband) |
|---------|------------------------|-------------------------|
| **신호 형태** | 디지털 펄스 (NRZ, Manchester) | 변조된 아날로그 파형 (AM, FM, QAM) |
| **주파수 범위** | 0 Hz ~ B Hz (DC 포함) | fc - B/2 ~ fc + B/2 (DC 제외) |
| **변조 과정** | 없음 (Line Coding만) | 반송파 변조 (Modulation) 필수 |
| **다중화 방식** | TDM (시분할) | FDM (주파수 분할) 가능 |
| **전송 매체** | 꼬임쌍선(UTP), 동축, 광섬유 | 동축, 광섬유, 무선 |
| **증폭/중계** | 리피터 (재생) | 증폭기 (Amplifier) 또는 재생기 |
| **대표 표준** | Ethernet (10BASE-T), USB, SATA | DOCSIS, DSL, DVB-C, LTE/5G |

#### 정교한 구조 다이어그램: 기저대역 vs 대역통과 전송

```ascii
================================================================================
[ Baseband Transmission System ]
================================================================================

[ 송신기 ]                              [ 수신기 ]

+----------+     +----------+     +----------+     +----------+
| 디지털   |     | Line     |     | 전송     |     | Line     |
| 데이터   |====>| Encoder  |====>| 매체     |====>| Decoder  |
| (0,1)    |     | (NRZ/    |     | (UTP/    |     | (복원)   |
+----------+     | Manchester)    |  광섬유) |     +----------+
                 +----------+     +----------+
                      |                |
                      v                v
                 펄스 파형         아날로그
                 ┌─┐ ┌─┐         펄스
                 │ │ │ │         (감쇠+잡음)
                 └─┘ └─┘

                 신호 스펙트럼:
                 |
            전력 |████████████
                 |            ████
                 |                ████
                 +---------------------> 주파수
                 0      B(Hz)
                 (DC 성분 포함)

특징:
- 단순한 구조 (변조기 불필요)
- 단일 채널만 전송 가능
- DC 성분 처리 중요

================================================================================
[ Broadband (Passband) Transmission System ]
================================================================================

[ 송신기 ]                                      [ 수신기 ]

+----------+  +----------+  +----------+  +----------+  +----------+
| 디지털   |  | 디지털   |  | 믹서     |  | 전송     |  | 복조기   |
| 데이터   |==>| 변조기   |==>| (Up-     |==>| 매체     |==>| (Demod)  |
| (0,1)    |  | (QAM)    |  | convert) |  | (동축/   |  |          |
+----------+  +----------+  +----------+  |  무선)   |  +----------+
                    |             |       +----------+
                    v             v
               디지털 심볼    반송파와
               (I, Q 좌표)    혼합
                                 |
                                 v
                 변조된 신호:
                      __      __
                 ____/  \____/  \____
                 (반송파 fc 위에 신호 실림)

                 신호 스펙트럼:
                 |
            전력 |      ███████████
                 |     ██          ██
                 |    █              █
                 +---------------------> 주파수
                      fc-B/2  fc  fc+B/2
                      (DC 성분 없음)

특징:
- FDM으로 다중 채널 전송 가능
- 주파수 선택적 필터링 가능
- 변조/복조기 복잡도 증가

================================================================================
[ FDM (Frequency Division Multiplexing) - Broadband Only ]
================================================================================

주파수 축:
   채널 1        채널 2        채널 3        채널 4
|███████████|███████████|███████████|███████████|
0            B           2B          3B          4B

   ↓ fc1        ↓ fc2       ↓ fc3       ↓ fc4
  변조         변조        변조        변조
   ↓            ↓           ↓           ↓
  ┌────────────────────────────────────────────┐
  │  합성기 (Combiner)                          │
  └────────────────────────────────────────────┘
                       ↓
               ┌───────────────┐
               │  전송 매체    │
               │  (동축/광섬유)│
               └───────────────┘
                       ↓
  ┌────────────────────────────────────────────┐
  │  분리기 (Splitter) + 필터                  │
  └────────────────────────────────────────────┘
       ↓            ↓           ↓           ↓
    채널 1       채널 2      채널 3      채널 4
    복조        복조        복조        복조

=> 기저대역 전송은 이러한 FDM이 불가능함 (주파수 충돌)
```

#### 심층 동작 원리: 기저대역 vs 대역통과 전송 7단계 비교

**기저대역 전송 (Ethernet 10BASE-T 예시)**:

1. **데이터 인코딩**: MAC 계층에서 전달받은 바이트를 Manchester 부호화합니다. 0은 Low→High, 1은 High→Low 전이로 표현합니다. 이를 통해 DC 성분을 제거하고 클럭 복원을 용이하게 합니다.

2. **펄스 성형**: 인코딩된 디지털 신호를 전송 라인의 특성에 맞게 성형합니다. 상승/하강 시간을 제어하여 고조파(Harmonics)를 억제하고 EMI를 최소화합니다.

3. **라인 구동**: 라인 드라이버가 UTP 케이블의 두 쌍(Tx+, Tx-)에 차동 신호로 출력합니다. 10BASE-T는 ±2.5V 피크 전압을 사용합니다.

4. **케이블 전파**: 신호는 UTP Cat 3 이상 케이블을 통해 전파됩니다. 100m 전파 지연은 약 500ns이며, 감쇠는 100m당 약 11.5dB(@10MHz)입니다.

5. **수신 및 등화**: 수신측에서 신호를 받아 등화기(Equalizer)가 케이블 감쇠를 보상합니다. 자동 이득 조정(AGC)이 신호 레벨을 정상화합니다.

6. **클럭 복원**: Manchester 부호의 천이점에서 클럭을 복원합니다. PLL(Phase-Locked Loop)이 송신측 클럭과 동기화합니다.

7. **디코딩**: Manchester 부호를 원래 NRZ 비트로 복원하고 MAC 계층으로 전달합니다.

**대역통과 전송 (DOCSIS 케이블 모뎀 예시)**:

1. **데이터 인코딩**: 데이터를 Reed-Solomon FEC, 인터리빙, 스크램블링하여 오류 정정 능력을 추가합니다.

2. **디지털 변조**: 데이터를 64-QAM 또는 256-QAM으로 변조합니다. 6비트(64-QAM) 또는 8비트(256-QAM)가 하나의 심볼(I/Q 좌표)로 매핑됩니다.

3. **업변환 (Upconversion)**: 기저대역 I/Q 신호를 믹서에서 반송파와 혼합하여 91~857MHz 대역으로 변환합니다.

4. **증폭 및 결합**: 변조된 신호를 증폭하고, 다른 채널(다른 반송파)과 결합하여 케이블로 보냅니다.

5. **케이블 전파**: 동축 케이블을 통해 신호가 전파됩니다. 다수의 채널이 FDM으로 공존합니다.

6. **튜닝 및 필터링**: 수신측 튜너가 원하는 채널의 반송파 주파수로 튜닝하고, 대역통과 필터로 해당 채널만 통과시킵니다.

7. **하향변환 및 복조**: 신호를 기저대역으로 하향변환(Downconversion)하고, QAM 복조기를 통해 원래 비트를 복원합니다.

#### 핵심 코드: 기저대역/대역통과 신호 스펙트럼 분석

```python
import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class TransmissionParameters:
    """전송 시스템 파라미터"""
    bit_rate: int           # 비트레이트 (bps)
    samples_per_bit: int    # 비트당 샘플 수
    carrier_freq: float     # 반송파 주파수 (Hz) - 대역통과용

class BasebandTransmission:
    """기저대역 전송 시뮬레이션"""

    def __init__(self, params: TransmissionParameters):
        self.params = params
        self.bit_duration = 1.0 / params.bit_rate
        self.sample_rate = params.bit_rate * params.samples_per_bit

    def generate_nrz_signal(self, bits: np.ndarray) -> np.ndarray:
        """NRZ (Non-Return-to-Zero) 부호화"""
        signal = np.array([])
        for bit in bits:
            # 1은 +V, 0은 -V
            level = 1.0 if bit == 1 else -1.0
            signal = np.concatenate([signal, np.full(self.params.samples_per_bit, level)])
        return signal

    def generate_manchester_signal(self, bits: np.ndarray) -> np.ndarray:
        """Manchester 부호화 (IEEE 802.3 표준)"""
        signal = np.array([])
        half_samples = self.params.samples_per_bit // 2

        for bit in bits:
            if bit == 1:
                # 1: High → Low
                signal = np.concatenate([
                    signal,
                    np.full(half_samples, 1.0),
                    np.full(half_samples, -1.0)
                ])
            else:
                # 0: Low → High
                signal = np.concatenate([
                    signal,
                    np.full(half_samples, -1.0),
                    np.full(half_samples, 1.0)
                ])
        return signal

    def compute_spectrum(self, sig: np.ndarray) -> tuple:
        """신호 스펙트럼 계산"""
        n = len(sig)
        yf = np.abs(fft(sig))[:n//2]
        xf = fftfreq(n, 1/self.sample_rate)[:n//2]
        return xf, yf

class BroadbandTransmission:
    """대역통과 전송 시뮬레이션"""

    def __init__(self, params: TransmissionParameters):
        self.params = params
        self.bit_duration = 1.0 / params.bit_rate
        self.sample_rate = params.bit_rate * params.samples_per_bit
        self.baseband = BasebandTransmission(params)

    def modulate_bpsk(self, bits: np.ndarray) -> np.ndarray:
        """BPSK 변조 (반송파에 실기)"""
        # 기저대역 NRZ 신호 생성
        baseband_signal = self.baseband.generate_nrz_signal(bits)

        # 반송파 생성
        t = np.arange(len(baseband_signal)) / self.sample_rate
        carrier = np.cos(2 * np.pi * self.params.carrier_freq * t)

        # 변조 (DSB-SC: Double Sideband Suppressed Carrier)
        modulated = baseband_signal * carrier
        return modulated

    def modulate_ask(self, bits: np.ndarray) -> np.ndarray:
        """ASK (Amplitude Shift Keying) 변조"""
        # 기저대역 신호 (0~1 범위)
        baseband_signal = np.array([])
        for bit in bits:
            level = 1.0 if bit == 1 else 0.0
            baseband_signal = np.concatenate([
                baseband_signal,
                np.full(self.params.samples_per_bit, level)
            ])

        # 반송파 생성 및 변조
        t = np.arange(len(baseband_signal)) / self.sample_rate
        carrier = np.cos(2 * np.pi * self.params.carrier_freq * t)

        modulated = baseband_signal * carrier
        return modulated

    def compute_spectrum(self, sig: np.ndarray) -> tuple:
        """신호 스펙트럼 계산"""
        n = len(sig)
        yf = np.abs(fft(sig))[:n//2]
        xf = fftfreq(n, 1/self.sample_rate)[:n//2]
        return xf, yf

def compare_transmissions():
    """기저대역 vs 대역통과 전송 비교"""

    # 파라미터 설정
    params = TransmissionParameters(
        bit_rate=10_000_000,      # 10 Mbps
        samples_per_bit=100,
        carrier_freq=50_000_000   # 50 MHz 반송파
    )

    # 테스트 데이터
    bits = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1])

    # 시스템 생성
    baseband = BasebandTransmission(params)
    broadband = BroadbandTransmission(params)

    # 신호 생성
    nrz_signal = baseband.generate_nrz_signal(bits)
    manchester_signal = baseband.generate_manchester_signal(bits)
    bpsk_signal = broadband.modulate_bpsk(bits)

    # 스펙트럼 계산
    freq_nrz, spec_nrz = baseband.compute_spectrum(nrz_signal)
    freq_manch, spec_manch = baseband.compute_spectrum(manchester_signal)
    freq_bpsk, spec_bpsk = broadband.compute_spectrum(bpsk_signal)

    # 결과 출력
    print("=" * 70)
    print("[ 기저대역 vs 대역통과 전송 비교 ]")
    print("=" * 70)
    print(f"비트레이트: {params.bit_rate/1e6} Mbps")
    print(f"샘플링 속도: {params.sample_rate/1e6} MHz")
    print(f"반송파 주파수 (대역통과): {params.carrier_freq/1e6} MHz")
    print("-" * 70)

    # 대역폭 분석
    def find_bandwidth(freq, spec, threshold_db=-3):
        """-3dB 대역폭 찾기"""
        spec_db = 20 * np.log10(spec + 1e-10)
        max_db = np.max(spec_db)
        threshold = max_db + threshold_db
        indices = np.where(spec_db >= threshold)[0]
        if len(indices) > 0:
            return freq[indices[0]], freq[indices[-1]]
        return 0, 0

    bw_nrz = find_bandwidth(freq_nrz, spec_nrz)
    bw_manch = find_bandwidth(freq_manch, spec_manch)
    bw_bpsk = find_bandwidth(freq_bpsk, spec_bpsk)

    print("\n[ 대역폭 분석 (-3dB 기준) ]")
    print(f"NRZ (기저대역):     {bw_nrz[0]/1e6:.2f} ~ {bw_nrz[1]/1e6:.2f} MHz")
    print(f"Manchester (기저):  {bw_manch[0]/1e6:.2f} ~ {bw_manch[1]/1e6:.2f} MHz")
    print(f"BPSK (대역통과):    {bw_bpsk[0]/1e6:.2f} ~ {bw_bpsk[1]/1e6:.2f} MHz")
    print("-" * 70)

    print("\n[ 주요 차이점 ]")
    print("기저대역 전송:")
    print("  - 신호 에너지가 0Hz(DC)부터 시작")
    print("  - 단일 채널만 전송 가능")
    print("  - 구현 단순, 지연 시간 낮음")
    print("")
    print("대역통과 전송:")
    print("  - 신호 에너지가 반송파 주파수(fc) 중심에 집중")
    print("  - FDM으로 다중 채널 전송 가능")
    print("  - 변조/복조기 필요, 복잡도 증가")
    print("=" * 70)

if __name__ == "__main__":
    compare_transmissions()
```

---

### Ⅲ. 융합 비교 및 다각도 분석 - [비교표 2개 이상]

#### 심층 기술 비교표: 전송 방식별 특성

| 비교 관점 | 기저대역 (Baseband) | 대역통과 (Broadband) |
|----------|-------------------|-------------------|
| **변조 필요성** | 없음 (Line Coding만) | 필수 (AM/FM/PM/QAM) |
| **주파수 범위** | 0 ~ B Hz | fc-B/2 ~ fc+B/2 |
| **DC 성분** | 포함 (처리 필요) | 없음 (차단됨) |
| **다중화** | TDM만 가능 | FDM, TDM 모두 가능 |
| **대역폭 효율** | 낮음 (1채널/케이블) | 높음 (다중 채널/케이블) |
| **전송 거리** | 짧음 (~100m UTP) | 김 (~수km 동축, ~수십km 광섬유) |
| **하드웨어 복잡도** | 낮음 | 높음 |
| **지연 시간** | 낮음 (변조 오버헤드 없음) | 높음 (변조/복조 처리) |
| **비용** | 저렴 | 고가 |
| **대표 적용** | Ethernet LAN, USB, SATA | 케이블 TV, DSL, Wi-Fi, 5G |

#### 적용 분야별 전송 방식 선택

| 적용 분야 | 추천 방식 | 이유 |
|----------|----------|------|
| **LAN (사내 네트워크)** | 기저대역 | 단거리, 단순성, 저비용 |
| **WAN (광역망 백본)** | 대역통과 | 장거리, WDM 다중화 |
| **무선 통신** | 대역통과 | 주파수 자원 효율, 다중 접속 |
| **USB/SATA** | 기저대역 | 짧은 케이블, 낮은 지연 |
| **케이블 TV** | 대역통과 | 수십 채널 FDM 전송 |
| **DSL (전화선)** | 대역통과 | 음성(0~4kHz)과 데이터(25kHz~) 분리 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 - [최소 800자]

#### 실무 시나리오: 기업 네트워크 백본 설계

**시나리오**: 대기업이 5개 층(각 층 200명)의 사무실 네트워크를 설계합니다. 각 층의 스위치를 지하 MDF(Main Distribution Frame)의 코어 스위치와 연결해야 합니다. 최대 거리는 80m입니다.

**기술사적 판단**:

1. **옵션 분석**:
   - **기저대역 (10GBASE-T)**: UTP Cat 6a 케이블로 100m까지 10Gbps 전송 가능. 변조 방식은 PAM-16을 사용하므로 사실상 대역통과 특성을 가짐.
   - **대역통과 (10GBASE-LR)**: SMF(단일모드 광섬유)로 10km까지 10Gbps 전송. 1310nm 파장의 광 신호 사용.

2. **결정**: **기저대역/준대역통과 (10GBASE-T)** 선택.
   - 이유: 80m는 UTP 전송 한계(100m) 내이며, 광섬유는 설치 비용이 3~5배 높음. Cat 6a 케이블은 기존 UTP 설치 노하우 활용 가능.

3. **고려사항**:
   - Cat 6a 케이블은 외경이 두꺼워(약 9mm) 케이블 트레이 용량 고려 필요
   - PoE+ (30W) 지원을 위해 전력 예산 계산 필요
   - Alien Crosstalk 방지를 위해 케이블 간격 유지

**시나리오 2: 케이블 TV 사업자의 인터넷 서비스 추가**

**기술사적 판단**:

1. **분석**: 기존 CATV 네트워크는 5~860MHz 대역을 사용. 하향(Downstream)은 54~860MHz, 상향(Upstream)은 5~42MHz 사용. 여유 대역에 인터넷 데이터를 실어야 함.

2. **결정**: **DOCSIS 3.1 (대역통과)** 채택.
   - 64/256-QAM 변조로 하향 최대 10Gbps, 상향 최대 1Gbps 지원
   - OFDM(하향)/OFDMA(상향)로 주파수 효율 극대화
   - 기존 TV 신호와 FDM으로 공존 가능

#### 도입 시 고려사항 체크리스트

**기저대역 전송 체크리스트**:
- [ ] 전송 거리가 매체 한계(UTP 100m, 광섬유 종류별 상이) 내인가?
- [ ] DC 성분 처리(Manchester, 8B/10B 등)가 적절한가?
- [ ] 클럭 복원 메커니즘이 신뢰적인가?
- [ ] 단일 채널만으로 충분한 대역폭이 확보되는가?

**대역통과 전송 체크리스트**:
- [ ] 반송파 주파수가 규제 및 간섭 측면에서 적절한가?
- [ ] 변조 방식의 SNR 요구사항을 채널이 만족하는가?
- [ ] 필터 설계가 인접 채널 간섭을 충분히 억제하는가?
- [ ] 튜너/동기 회로의 복잡도가 예산 내인가?

#### 주의사항 및 안티패턴

**안티패턴 1: 기저대역 전송으로 장거리 시도**
"기저대역이 단순하니 장거리 전송에도 좋을 것"이라는 잘못된 가정입니다. 기저대역 신호는 감쇠와 잡음에 취약하여 리피터가 빈번히 필요합니다. 장거리는 대역통과 + 광섬유 조합이 정석입니다.

**안티패턴 2: 대역통과 전송의 과도한 FDM**
"FDM으로 한 케이블에 수백 채널을 실자"는 접근은 가드밴드(Guard Band)와 필터 비용을 무시한 것입니다. 실제로는 채널 간 간섭 방지를 위해 충분한 여유가 필요합니다.

**안티패턴 3: DC 성분 무시**
기저대역 전송에서 DC 성분이 포함된 부호(NRZ-L)를 사용하면, 긴 0 또는 1 연속 시 베이스라인 드리프트(Baseline Wander)가 발생합니다. Manchester, 8B/10B, 64B/66B 등 DC 밸런스 부호를 사용해야 합니다.

---

### Ⅴ. 기대효과 및 결론 - [최소 400자]

#### 정량적/정성적 기대효과표

| 효과 영역 | 기저대역 | 대역통과 | 비교 |
|----------|---------|---------|------|
| **설치 비용 (100m)** | 50만 원 (UTP) | 200만 원 (광섬유+변환기) | 기저대역 75% 절감 |
| **지연 시간** | < 1μs | 5~20μs (변조/복조) | 기저대역 10~20배 빠름 |
| **전력 소비** | 0.5W/port | 2~5W/port (광 모듈) | 기저대역 4~10배 적음 |
| **주파수 효율** | 1 채널/케이블 | 10+ 채널/케이블 | 대역통과 10배+ 높음 |
| **전송 거리** | ~100m (UTP) | ~80km (SMF) | 대역통과 800배+ 김 |

#### 미래 전망 및 진화 방향

**1. 기저대역/대역통과 경계의 모호화**:
고속 이더넷(25G, 40G, 100G)은 PAM-4 같은 다단 변호를 사용하며, 이는 기술적으로 대역통과 특성을 갖습니다. 400GBASE-R은 16진 PAM(PAM-16)을 사용합니다. 용어의 구분보다 실제 변조 방식에 주목해야 합니다.

**2. 광 인터커넥트의 기저대역화**:
데이터센터 내 서버-스위치 연결에 광 인터커넥트가 늘어나면서, NRZ 기저대역 전송이 광 도메인으로 확장됩니다. Silicon Photonics 기술이 변조 없는 광 기저대역 전송을 가능하게 합니다.

**3. 무선의 초광대역 기저대역화**:
UWB(Ultra-Wideband)와 Impulse Radio는 반송파 없이 기저대역 펄스를 직접 방사합니다. 이는 무선에서 기저대역 전송의 새로운 패러다임입니다.

#### ※ 참고 표준/가이드

- **IEEE 802.3**: Ethernet 표준 (기저대역 및 광대역통과 모두 포함)
- **ITU-T G.992.x (ADSL)**: DMT 기반 대역통과 전송 표준
- **DOCSIS 3.1/4.0**: 케이블 모뎀 대역통과 표준
- **ITU-T G.709 (OTN)**: 광 대역통과 전송 표준

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [Line Coding (NRZ/Manchester)](@/studynotes/3_network/1_fundamentals/line_coding_nrz_rz_manchester.md): 기저대역 부호화 기술
- [변조 기술 (ASK/FSK/PSK/QAM)](@/studynotes/3_network/1_fundamentals/modulation_ask_fsk_psk_qam.md): 대역통과 변조 기술
- [다중화 기술 (FDM/TDM)](@/studynotes/3_network/1_fundamentals/multiplexing_fdm_tdm_wdm.md): 대역통과의 FDM 활용
- [OSI 7계층 - 물리 계층](@/studynotes/3_network/1_fundamentals/osi_7_layer.md): 전송 방식의 계층적 위치
- [전송 매체 (UTP/광섬유)](@/studynotes/3_network/1_fundamentals/_index.md): 매체별 적합한 전송 방식

---

### 👶 어린이를 위한 3줄 비유 설명

1. **기저대역 전송**은 **'친구에게 바로 말하기'**예요. 내 목소리 그대로 말하니까 간단하고 빠르지만, 한 번에 한 명한테만 말할 수 있고 멀리 있는 친구는 못 들어요.

2. **대역통과 전송**은 **'라디오 방송으로 말하기'**예요. 내 목소리를 전파에 실어 보내니까 멀리까지 들리고, 여러 라디오 채널로 여러 사람이 동시에 방송할 수 있어요.

3. 집에서 인터넷할 때는 기저대역(랜선)으로, 핸드폰으로 영상 통화할 때는 대역통과(무선)로 정보가 오가요! 두 방식이 우리 생활 곳곳에서 쓰이고 있어요.
