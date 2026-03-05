+++
title = "071. 다중화 (Multiplexing) 개념 및 특징"
description = "다중화의 기본 원리, FDM/TDM/WDM/CDM 방식, 효율성 분석, 현대적 응용을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["Multiplexing", "FDM", "TDM", "WDM", "CDM", "OFDM", "ChannelCapacity"]
categories = ["studynotes-3_network"]
+++

# 071. 다중화 (Multiplexing) 개념 및 특징

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 다중화는 하나의 전송 매체에 여러 신호를 동시에 전송하여 매체 활용 효율을 극대화하는 기술로, 주파수, 시간, 파장, 코드 도메인에서 신호를 분리합니다.
> 2. **가치**: 통신 인프라 비용 절감(단일 고속 링크 vs 다중 저속 링크), 스펙트럼 효율 향상, 대역폭 확장성 확보의 핵심 기술입니다.
> 3. **융합**: 현대 통신은 OFDM(4G/5G/Wi-Fi), DWDM(광백본), CDMA(3G) 등 복합 다중화 기술을 스택 형태로 적용하여 Tbps급 전송을 실현합니다.

---

## I. 개요 (Context & Background)

다중화(Multiplexing)는 **하나의 물리적 전송 매체(채널)를 통해 여러 개의 독립적인 신호를 동시에 전송**하는 기술입니다. 이를 통해 통신 자원(대역폭, 케이블, 광섬유 등)의 활용 효율을 극대화하고, 인프라 구축 비용을 절감할 수 있습니다.

**다중화의 핵심 구성요소**:
1. **Mux (Multiplexer, 다중화기)**: 여러 입력 신호를 하나로 결합
2. **공유 매체**: 결합된 신호가 전송되는 채널
3. **Demux (Demultiplexer, 역다중화기)**: 결합된 신호를 다시 분리

**비유**: 다중화는 **"하나의 고속도로에 여러 차선이 있는 것"**과 같습니다.
- **FDM**: 각 차선이 서로 다른 목적지로 가는 차들로 할당됨
- **TDM**: 시간대별로 다른 차들이 같은 차선을 사용함 (교차로 신호등)
- **CDM**: 모든 차가 같은 도로를 쓰지만, 각각 다른 암호로 구별됨

**등장 배경 및 발전 과정**:
1. **전신 시대 (1850년대)**: 단일 전신선으로 여러 메시지 전송 시도
2. **전화 다중화 (1910년대)**: 캐리어 전화(Carrier Telephony)로 FDM 도입
3. **디지털 다중화 (1960년대)**: T1(1.544 Mbps)으로 TDM 표준화
4. **광 다중화 (1990년대~)**: WDM, DWDM으로 Tbps 시대 개막
5. **현대**: OFDM(무선), λ-Grid(광) 등 정밀 다중화 기술

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 다중화 방식별 특성 비교

| 방식 | 분리 도메인 | 원리 | 장점 | 단점 | 적용 |
|------|------------|------|------|------|------|
| **FDM** | 주파수 | 주파수 대역 분할 | 연속 전송, 단순 | 보호대역 손실 | 라디오, 아날로그 TV |
| **TDM** | 시간 | 타임 슬롯 분할 | 디지털 친화적 | 동기화 필요 | T1/E1, SONET/SDH |
| **WDM** | 파장 | 광 파장 분할 | 초대역폭 | 광부품 고가 | 광백본, FTTH |
| **CDM** | 코드 | 직교 코드 분배 | 보안, 간섭 내성 | 전력 제어 복잡 | CDMA, GPS |
| **OFDM** | 직교 주파수 | 직교 서브캐리어 | 대역폭 효율, ISI 강함 | PAPR 문제 | Wi-Fi, LTE, 5G |
| **SDM** | 공간 | 물리적 경로 분리 | 단순 | 공간 제약 | MIMO, 다중 광섬유 |

### 정교한 구조 다이어그램: 다중화 아키텍처

```ascii
================================================================================
[ Multiplexing System Architecture ]
================================================================================

[ 송신측: Multiplexer (Mux) ]                [ 수신측: Demultiplexer (Demux) ]

  입력 채널들                                    출력 채널들
  =========                                     =========

  Ch 1 ----+                              +----> Ch 1
           |                              |
  Ch 2 ----+    +------------------+      +----> Ch 2
           |    |                  |      |
  Ch 3 ----+--->|   Multiplexer    |===========>|  Demultiplexer  |--+----> Ch 3
           |    |                  |      ^      |                 |  |
  Ch 4 ----+    +------------------+      |      +------------------+  +----> Ch 4
           |             |                |              ^
           |             v                |              |
           |      공유 전송 매체           +---- 분리된 신호들
           |    (Shared Medium)          (Recovered Signals)
           |
           +--- 결합된 신호 (Composite Signal)

================================================================================
[ FDM: Frequency Division Multiplexing ]
================================================================================

주파수 (Frequency)
    ^
    |  Ch 1      보호    Ch 2      보호    Ch 3      보호    Ch 4
    |   |<------> 대역 <-------> 대역 <-------> 대역 <------->|
    |   |   f₁   | B_g |   f₂   | B_g |   f₃   | B_g |   f₄   |
    |   |        |     |        |     |        |     |        |
    |   |   ___  |     |   ___  |     |   ___  |     |   ___  |
    |   |  |   | |     |  |   | |     |  |   | |     |  |   | |
    |   |  |   | |     |  |   | |     |  |   | |     |  |   | |
    |   |  |   | |     |  |   | |     |  |   | |     |  |   | |
    +---+--+---+-+-----+--+---+-+-----+--+---+-+-----+--+---+-+------> f
        f₁-B/2 f₁+B/2  f₂-B/2 f₂+B/2 f₃-B/2 f₃+B/2 f₄-B/2 f₄+B/2

    특징:
    - 각 채널이 고유 주파수 대역 할당
    - 동시에 모든 채널 전송 (병렬)
    - 보호 대역(Guard Band) 필요 → 대역폭 낭비
    - 아날로그 신호에 적합

    총 대역폭: B_total = N × (B_ch + B_guard)
             ≈ N × B_ch × (1 + α), α = B_guard/B_ch

================================================================================
[ TDM: Time Division Multiplexing ]
================================================================================

시간 (Time)
    ^
    |          Frame 1              Frame 2              Frame 3
    |  |----------------------||----------------------||-----------------...
    |  |    |    |    |    |  ||    |    |    |    |  ||
    |  | Ch | Ch | Ch | Ch |  || Ch | Ch | Ch | Ch |  ||
    |  |  1 |  2 |  3 |  4 |  ||  1 |  2 |  3 |  4 |  ||
    |  |    |    |    |    |  ||    |    |    |    |  ||
    +--+----+----+----+----+--++----+----+----+----+--++-------------> t
       |----|----|----|----|
            하나의 프레임

    특징:
    - 각 채널이 고유 타임 슬롯 할당
    - 순차적 전송 (직렬)
    - 동기화 필수 (프레임 동기)
    - 디지털 신호에 적합

    프레임 구조:
    +--------+--------+--------+--------+--------+
    | 프레임 | Slot 1 | Slot 2 | Slot 3 | Slot 4 |
    | 동기화 | (Ch 1) | (Ch 2) | (Ch 3) | (Ch 4) |
    +--------+--------+--------+--------+--------+
       (Framing bits for synchronization)

    비트 레이트: R_total = N × R_ch (이상적, 오버헤드 무시 시)

================================================================================
[ WDM: Wavelength Division Multiplexing (광 다중화) ]
================================================================================

파장 (Wavelength) - 광섬유 투과율
    ^
    |    λ₁   λ₂   λ₃   λ₄   λ₅   λ₆   λ₇   λ₈
    |    |    |    |    |    |    |    |    |
    |    |    |    |    |    |    |    |    |
100%|....|....|....|....|....|....|....|....|.... 저손실 윈도우
    |    | 1540nm                        1560nm
    |    |    |    |    |    |    |    |    |
    +----+----+----+----+----+----+----+----+----+---> λ
        1530                            1565 nm (C-band)

    CWDM (Coarse WDM):   8~18 채널, 20nm 간격, 저비용
    DWDM (Dense WDM):    40~160+ 채널, 0.8nm(100GHz) 간격, 고용량

    단일 광섬유 용량:
    - 100 채널 × 100 Gbps/채널 = 10 Tbps (양방향 20 Tbps)

================================================================================
[ CDM: Code Division Multiplexing ]
================================================================================

직교 코드 예시 (Walsh Code, 4채널)

    Ch 1: [+1 +1 +1 +1]  (코드 C₁)
    Ch 2: [+1 -1 +1 -1]  (코드 C₂)
    Ch 3: [+1 +1 -1 -1]  (코드 C₃)
    Ch 4: [+1 -1 -1 +1]  (코드 C₄)

    직교성: Cᵢ · Cⱼ = 0 (i ≠ j), Cᵢ · Cᵢ = N

    송신:
    신호 = Ch1_data×C₁ + Ch2_data×C₂ + Ch3_data×C₃ + Ch4_data×C₄

    수신 (Ch 1 복원):
    Rx_Ch1 = 신호 · C₁ / 4 = Ch1_data (다른 채널 성분은 0)

    특징:
    - 모든 채널이 동일 주파수, 동일 시간 사용
    - 코드로만 분리
    - 전력 제어 중요 (Near-Far 문제)

================================================================================
```

### 다중화 효율 분석

| 방식 | 대역폭 효율 | 스펙트럼 효율 (bps/Hz) | 오버헤드 | 복잡도 |
|------|-----------|----------------------|---------|--------|
| **FDM** | 70-85% | 낮음 | 보호 대역 | 낮음 |
| **TDM (Sync)** | 90-95% | 중간 | 프레임 동기 | 중간 |
| **TDM (Stat)** | 95-99% | 높음 | 헤더 | 중간 |
| **WDM** | 90-98% | 최고 | EDFA 레인 | 중간 |
| **CDM** | 50-80% | 중간 | 코드 길이 | 높음 |
| **OFDM** | 85-95% | 높음 | CP | 높음 |

### 심층 동작 원리: 동기식 TDM vs 통계적 TDM

**동기식 TDM (Synchronous TDM)**:
```
- 고정 슬롯 할당 (각 채널에 정해진 슬롯)
- 유휴 슬롯도 전송 (데이터 없어도 슬롯 유지)
- 구현 단순, 지연 일정

예: T1 (24채널 음성 + 1프레이밍 비트)
프레임 = 24 × 8비트 + 1비트 = 193비트
8000 프레임/초 → 1.544 Mbps
각 채널 = 64 kbps
```

**통계적 TDM (Statistical/Asynchronous TDM)**:
```
- 동적 슬롯 할당 (데이터 있는 채널만)
- 주소/식별자 포함 필요
- 버퍼링 필요, 지연 변동

프레임 구조:
+----------+------+----------+------+----------+
|  헤더    | 데이터|  헤더    | 데이터|  헤더    | ...
| Ch ID   | Ch 3 | Ch ID   | Ch 1 | Ch ID   |
+----------+------+----------+------+----------+

효율 = 활성 채널 수 / 전체 채널 수 (버스트 트래픽에서 높음)
```

### 핵심 코드: 다중화 시뮬레이션 (Python)

```python
import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class MultiplexingType(Enum):
    FDM = "Frequency Division"
    TDM = "Time Division"
    WDM = "Wavelength Division"
    CDM = "Code Division"

@dataclass
class Channel:
    """채널 데이터 클래스"""
    id: int
    data: np.ndarray
    bandwidth_hz: float = 4000.0  # 기본 4kHz (음성)
    sample_rate: float = 8000.0

class FDMMultiplexer:
    """
    주파수 분할 다중화 (FDM) 구현
    """

    def __init__(self, carrier_spacing_hz: float = 10000.0):
        """
        Args:
            carrier_spacing_hz: 반송파 간격 (Hz)
        """
        self.carrier_spacing = carrier_spacing_hz
        self.guard_band_hz = 1000.0  # 보호 대역

    def modulate_channel(
        self,
        channel: Channel,
        carrier_freq: float,
        modulation: str = 'AM'
    ) -> np.ndarray:
        """
        채널 신호를 지정된 반송파로 변조

        Args:
            channel: 채널 데이터
            carrier_freq: 반송파 주파수 (Hz)
            modulation: 변조 방식

        Returns:
            변조된 신호
        """
        t = np.arange(len(channel.data)) / channel.sample_rate
        carrier = np.cos(2 * np.pi * carrier_freq * t)

        if modulation == 'AM':
            # 진폭 변조 (DSB-SC)
            modulated = channel.data * carrier
        elif modulation == 'DSB-LC':
            # 대역 억압 반송파 포함
            modulated = (1 + channel.data) * carrier
        else:
            modulated = channel.data * carrier

        return modulated

    def multiplex(self, channels: List[Channel], base_freq: float = 100000.0) -> np.ndarray:
        """
        FDM 다중화 수행

        Args:
            channels: 채널 리스트
            base_freq: 기준 주파수 (Hz)

        Returns:
            다중화된 신호
        """
        # 모든 채널의 길이를 동일하게 맞춤
        max_len = max(len(ch.data) for ch in channels)
        multiplexed = np.zeros(max_len)

        for i, channel in enumerate(channels):
            # 반송파 주파수 할당 (보호 대역 포함)
            carrier_freq = base_freq + i * (self.carrier_spacing + self.guard_band_hz)

            # 변조
            modulated = self.modulate_channel(channel, carrier_freq)

            # 합성
            if len(modulated) < max_len:
                modulated = np.pad(modulated, (0, max_len - len(modulated)))
            multiplexed += modulated

        return multiplexed

    def demultiplex(
        self,
        multiplexed: np.ndarray,
        num_channels: int,
        base_freq: float,
        sample_rate: float
    ) -> List[np.ndarray]:
        """
        FDM 역다중화

        복조 과정: 대역 통과 필터 → 복조 → 저역 통과 필터
        """
        from scipy import signal

        recovered = []
        t = np.arange(len(multiplexed)) / sample_rate

        for i in range(num_channels):
            carrier_freq = base_freq + i * (self.carrier_spacing + self.guard_band_hz)

            # 대역 통과 필터 설계 (간단화)
            bandwidth = self.carrier_spacing / 2
            nyq = sample_rate / 2

            # 코히어런트 복조
            carrier = np.cos(2 * np.pi * carrier_freq * t)
            demodulated = multiplexed * carrier

            # 저역 통과 필터
            lpf_cutoff = bandwidth / nyq
            b, a = signal.butter(4, lpf_cutoff, btype='low')
            baseband = signal.filtfilt(b, a, demodulated)

            recovered.append(baseband * 2)  # 정규화

        return recovered


class TDMMultiplexer:
    """
    시분할 다중화 (TDM) 구현
    """

    def __init__(self, slot_duration_ms: float = 0.125):
        """
        Args:
            slot_duration_ms: 슬롯 지속 시간 (ms)
        """
        self.slot_duration = slot_duration_ms / 1000  # 초 단위

    def multiplex_synchronous(
        self,
        channels: List[Channel],
        samples_per_slot: int = 8
    ) -> Tuple[np.ndarray, dict]:
        """
        동기식 TDM 다중화

        Args:
            channels: 채널 리스트
            samples_per_slot: 슬롯당 샘플 수

        Returns:
            (다중화된 데이터, 프레임 정보)
        """
        num_channels = len(channels)
        frame_size = num_channels * samples_per_slot

        # 최대 길이 계산
        max_samples = max(len(ch.data) for ch in channels)
        num_frames = int(np.ceil(max_samples / samples_per_slot))

        # 프레임 구조: [동기 비트] + [슬롯 1] + [슬롯 2] + ... + [슬롯 N]
        sync_pattern = np.array([1, 0, 1, 0, 1, 0, 1, 1])  # 프레임 동기 패턴

        multiplexed = []

        for frame_idx in range(num_frames):
            # 동기 패턴 추가
            multiplexed.extend(sync_pattern)

            for channel in channels:
                start = frame_idx * samples_per_slot
                end = start + samples_per_slot

                slot_data = channel.data[start:end] if end <= len(channel.data) else \
                           np.pad(channel.data[start:], (0, end - len(channel.data)))

                multiplexed.extend(slot_data)

        frame_info = {
            'num_channels': num_channels,
            'samples_per_slot': samples_per_slot,
            'sync_pattern_length': len(sync_pattern),
            'frame_size': len(sync_pattern) + frame_size,
            'num_frames': num_frames
        }

        return np.array(multiplexed), frame_info

    def multiplex_statistical(
        self,
        channels: List[Channel],
        address_bits: int = 8
    ) -> Tuple[np.ndarray, dict]:
        """
        통계적 TDM 다중화 (비동기식)

        데이터가 있는 채널만 전송
        """
        multiplexed = []
        total_slots = 0
        active_slots = 0

        # 각 채널의 데이터를 슬롯 단위로 처리
        slot_size = 32  # 바이트

        for channel in channels:
            data = channel.data
            num_slots = int(np.ceil(len(data) / slot_size))

            for slot_idx in range(num_slots):
                start = slot_idx * slot_size
                end = min(start + slot_size, len(data))

                if start < len(data):
                    # 채널 ID (주소) 추가
                    address = channel.id.to_bytes(address_bits // 8, 'big')

                    # 데이터 슬롯
                    slot_data = data[start:end]
                    if len(slot_data) < slot_size:
                        slot_data = np.pad(slot_data, (0, slot_size - len(slot_data)))

                    # 프레임: [주소][데이터]
                    multiplexed.extend(list(address))
                    multiplexed.extend(slot_data)

                    active_slots += 1
                total_slots += 1

        frame_info = {
            'slot_size': slot_size,
            'address_bits': address_bits,
            'total_slots': total_slots,
            'active_slots': active_slots,
            'efficiency': active_slots / total_slots if total_slots > 0 else 0
        }

        return np.array(multiplexed), frame_info

    def demultiplex_synchronous(
        self,
        multiplexed: np.ndarray,
        frame_info: dict
    ) -> List[np.ndarray]:
        """
        동기식 TDM 역다중화
        """
        num_channels = frame_info['num_channels']
        samples_per_slot = frame_info['samples_per_slot']
        sync_len = frame_info['sync_pattern_length']
        frame_size = frame_info['frame_size']

        recovered = [[] for _ in range(num_channels)]

        num_frames = len(multiplexed) // frame_size

        for frame_idx in range(num_frames):
            frame_start = frame_idx * frame_size
            data_start = frame_start + sync_len

            for ch_idx in range(num_channels):
                slot_start = data_start + ch_idx * samples_per_slot
                slot_end = slot_start + samples_per_slot

                slot_data = multiplexed[slot_start:slot_end]
                recovered[ch_idx].extend(slot_data)

        return [np.array(r) for r in recovered]


class CDMMultiplexer:
    """
    코드 분할 다중화 (CDM) 구현
    Walsh 코드 사용
    """

    @staticmethod
    def generate_walsh_code(order: int) -> np.ndarray:
        """
        Walsh 코드 생성 (Hadamard 행렬)

        Args:
            order: 코드 차수 (2^n)

        Returns:
            Walsh 코드 행렬 (order × order)
        """
        if order == 1:
            return np.array([[1]])

        # 재귀적 생성
        h_small = CDMMultiplexer.generate_walsh_code(order // 2)

        h = np.zeros((order, order))
        h[:order//2, :order//2] = h_small
        h[:order//2, order//2:] = h_small
        h[order//2:, :order//2] = h_small
        h[order//2:, order//2:] = -h_small

        return h

    def __init__(self, num_channels: int):
        """
        Args:
            num_channels: 채널 수 (2의 거듭제곱이어야 함)
        """
        # 가장 가까운 2의 거듭제곱으로 올림
        self.code_length = 1
        while self.code_length < num_channels:
            self.code_length *= 2

        self.walsh_matrix = self.generate_walsh_code(self.code_length)
        self.codes = self.walsh_matrix[:num_channels]

    def spread_signal(self, data: np.ndarray, code: np.ndarray) -> np.ndarray:
        """
        스펙트럼 확산

        각 데이터 비트를 코드 길이만큼 확산
        """
        spread = np.zeros(len(data) * len(code))
        for i, bit in enumerate(data):
            spread[i*len(code):(i+1)*len(code)] = bit * code
        return spread

    def multiplex(self, channels: List[Channel]) -> np.ndarray:
        """
        CDM 다중화

        모든 채널의 확산된 신호를 합산
        """
        max_len = max(len(ch.data) for ch in channels)

        # 모든 채널을 같은 길이로 확장
        multiplexed = np.zeros(max_len * self.code_length)

        for i, channel in enumerate(channels):
            if i >= len(self.codes):
                break

            code = self.codes[i]
            data = channel.data

            # 확산
            spread = self.spread_signal(data, code)

            # 길이 맞춤
            if len(spread) < len(multiplexed):
                spread = np.pad(sread, (0, len(multiplexed) - len(spread)))
            elif len(spread) > len(multiplexed):
                multiplexed = np.pad(multiplexed, (0, len(spread) - len(multiplexed)))

            multiplexed += spread

        return multiplexed / len(channels)  # 정규화

    def demultiplex(self, multiplexed: np.ndarray, channel_id: int) -> np.ndarray:
        """
        CDM 역다중화

        상관 연산으로 원하는 채널 복원
        """
        if channel_id >= len(self.codes):
            raise ValueError(f"Invalid channel ID: {channel_id}")

        code = self.codes[channel_id]
        code_len = len(code)

        num_symbols = len(multiplexed) // code_len
        recovered = np.zeros(num_symbols)

        for i in range(num_symbols):
            segment = multiplexed[i*code_len:(i+1)*code_len]
            # 상관 (내적)
            correlation = np.dot(segment, code) / code_len
            recovered[i] = np.sign(correlation) if correlation != 0 else 0

        return recovered


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("다중화 시스템 비교")
    print("=" * 60)

    # 테스트 채널 생성
    np.random.seed(42)
    channels = [
        Channel(id=1, data=np.random.randn(1000)),
        Channel(id=2, data=np.random.randn(1000)),
        Channel(id=3, data=np.random.randn(1000)),
        Channel(id=4, data=np.random.randn(1000)),
    ]

    # 1. FDM
    fdm = FDMMultiplexer(carrier_spacing_hz=10000)
    fdm_signal = fdm.multiplex(channels, base_freq=100000)
    print(f"\nFDM: 다중화된 신호 길이 = {len(fdm_signal)}")

    # 2. TDM (동기식)
    tdm = TDMMultiplexer()
    tdm_signal, tdm_info = tdm.multiplex_synchronous(channels, samples_per_slot=8)
    print(f"TDM (동기식): {tdm_info['num_frames']} 프레임, 프레임 크기 = {tdm_info['frame_size']}")

    # 3. TDM (통계적)
    tdm_stat_signal, tdm_stat_info = tdm.multiplex_statistical(channels)
    print(f"TDM (통계적): 효율 = {tdm_stat_info['efficiency']:.2%}")

    # 4. CDM
    cdm = CDMMultiplexer(num_channels=4)
    print(f"CDM: Walsh 코드 길이 = {cdm.code_length}")
    print(f"Walsh 코드:\n{cdm.codes}")

    cdm_signal = cdm.multiplex(channels)
    print(f"CDM: 다중화된 신호 길이 = {len(cdm_signal)}")

    # 5. 대역폭 효율 비교
    print("\n" + "=" * 60)
    print("대역폭 효율 분석")
    print("=" * 60)

    channel_bw = 4000  # Hz per channel
    num_channels = 4

    fdm_total = num_channels * (channel_bw + 1000)  # 보호 대역 포함
    tdm_total = num_channels * channel_bw  # 이상적

    print(f"FDM 총 대역폭: {fdm_total/1000:.1f} kHz (보호 대역 포함)")
    print(f"TDM 총 대역폭: {tdm_total/1000:.1f} kHz (이상적)")
    print(f"FDM 효율: {num_channels * channel_bw / fdm_total:.1%}")

    print("\n=== 다중화 분석 완료 ===")
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 다중화 기술 스택 (현대 통신 시스템)

| 계층 | 기술 | 예시 |
|------|------|------|
| **전파 접속** | OFDMA, CDMA | 5G NR, Wi-Fi 6 |
| **광 전송** | DWDM | 100채널 × 100G = 10T |
| **전기 전송** | TDM | OTN, SDH |
| **공간** | MIMO, SDM | 8×8 MIMO, 멀티코어 광섬유 |

### 과목 융합 관점 분석

1. **OSI 계층과의 융합**:
   - **물리 계층**: FDM, TDM, WDM
   - **데이터링크 계층**: 통계적 TDM, VLAN 태그
   - **네트워크 계층**: MPLS 레이블, VPN

2. **클라우드와의 융합**:
   - **가상화**: vNIC, SR-IOV
   - **컨테이너**: 네트워크 네임스페이스 분리
   - **NFV**: VNF 간 트래픽 다중화

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 통신 사업자 백본망 용량 확장

**문제 상황**: 기존 10 Gbps × 32파장 DWDM 시스템(320 Gbps)을 1 Tbps로 확장해야 합니다.

**기술사의 전략적 의사결정**:

1. **옵션 분석**:
   | 옵션 | 기술 | 비용 | 확장성 |
   |------|------|------|--------|
   | A | 100G × 10파장 추가 | 중간 | 제한적 |
   | B | 100G × 80파장 교체 | 높음 | 우수 |
   | C | 400G × 3파장 | 낮음 | 최고 |

2. **선택**: 옵션 C (400G QPSK/16QAM 적응형)
   - 기존 섀시 활용
   - 최소 업그레이드
   - 향후 800G 확장 가능

---

## V. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 항목 | 다중화 미적용 | 다중화 적용 | 개선 |
|------|--------------|------------|------|
| **케이블 수** | 100회선 | 1회선 | 99% 절감 |
| **설치 비용** | $100K | $5K | 95% 절감 |
| **대역폭 활용** | 10% | 85% | 8.5배 |
| **관리 복잡도** | 높음 | 낮음 | - |

### 참고 표준/가이드

| 표준 | 기관 | 내용 |
|------|------|------|
| **ITU-T G.694.1** | ITU-T | DWDM 주파수 그리드 |
| **IEEE 802.3** | IEEE | 이더넷 PHY |
| **3GPP TS 38.211** | 3GPP | 5G NR OFDM |

---

## 관련 개념 맵 (Knowledge Graph)
- [주파수 분할 다중화 FDM](./73_fdm_frequency_division.md) - FDM 상세
- [시분할 다중화 TDM](./75_tdm_time_division.md) - TDM 상세
- [광파장 분할 다중화 WDM](./79_wdm_wavelength_division.md) - WDM 상세
- [OFDM 직교 주파수 분할](./84_ofdm_orthogonal_fdm.md) - OFDM 상세
- [다중 접속 기술](./87_multiple_access_concept.md) - MAC 계층 연계

---

## 어린이를 위한 3줄 비유 설명
1. **다중화**는 **하나의 고속도로에서 여러 차선을 쓰는 것**과 같아요. 한 도로로 많은 차가 목적지까지 갈 수 있어요.
2. **FDM**은 **각 차선이 다른 도시로 가는 전용 차선**, **TDM**은 **시간대별로 차가 번갈아 가는 교차로**예요.
3. **다중화기(Mux)**는 **차들을 도로로 합치는 입구**, **역다중화기(Demux)**는 **다시 갈라지는 출구**예요!
