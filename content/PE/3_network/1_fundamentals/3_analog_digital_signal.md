+++
title = "003. 아날로그 신호 vs 디지털 신호 (Analog vs Digital Signal)"
description = "아날로그 신호와 디지털 신호의 특성, 변환 방식, 장단점 및 통신 시스템에서의 적용을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["AnalogSignal", "DigitalSignal", "Modulation", "Sampling", "Quantization", "ADC", "DAC"]
categories = ["studynotes-3_network"]
+++

# 003. 아날로그 신호 vs 디지털 신호

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 아날로그 신호는 시간과 진폭이 연속적인 물리량으로, 자연계의 정보를 그대로 표현하는 반면, 디지털 신호는 이산적인 0과 1의 이진값으로 구성되어 컴퓨터 처리와 오류 정정에 최적화되어 있습니다.
> 2. **가치**: 디지털 신호는 재생 증폭이 가능하여 장거리 전송에서 신호 품질 열화가 없으며, 암호화·압축·오류정정 등의 디지털 신호 처리를 통해 대역폭 효율을 30~50% 향상시킬 수 있습니다.
> 3. **융합**: 현대 통신 시스템은 아날로그-디지털 하이브리드 방식으로, 자연계의 아날로그 정보를 ADC로 디지털화하여 전송하고 수신측에서 DAC로 복원하는 구조를 채택합니다.

---

## Ⅰ. 개요 (Context & Background)

신호(Signal)는 정보를 전달하는 매개체로, 시간에 따라 변화하는 물리량으로 표현됩니다. 통신 시스템에서 가장 기본이 되는 신호의 분류는 **아날로그 신호(Analog Signal)**와 **디지털 신호(Digital Signal)**입니다. 이 두 가지 신호 형태는 현대 통신의 근간을 이루며, 각각의 특성에 따라 적용 분야와 장단점이 명확히 구분됩니다.

**💡 비유**: 아날로그 신호와 디지털 신호의 차이를 **'음악 감상'**에 비유할 수 있습니다.
- **아날로그 신호**는 **LP 레코드**와 같습니다. 바늘이 레코드 홈의 물리적 굴곡을 따라 움직이며 연속적인 소리를 재생합니다. 미세한 떨림까지 그대로 표현하지만, 먼지나 긁힘에 취약합니다.
- **디지털 신호**는 **CD나 MP3**와 같습니다. 소리를 0과 1의 숫자로 변환하여 저장합니다. 약간의 오류가 있어도 원래 소리를 거의 완벽하게 복원할 수 있고, 복사를 해도 품질이 떨어지지 않습니다.

**등장 배경 및 발전 과정**:
1. **아날로그 통신의 시작 (19세기)**: 전신(Telegraph)과 전화(Telephone)는 본질적으로 아날로그 신호를 사용했습니다. 인간의 음성은 연속적인 파동이므로, 이를 전기 신호로 직접 변환하는 것이 가장 자연스러웠습니다.
2. **디지털 통신의 탄생 (1948년)**: Claude Shannon의 "A Mathematical Theory of Communication" 논문에서 디지털 통신의 이론적 기반이 확립되었습니다. 샤논의 정보이론은 모든 정보를 비트(Bit)로 표현할 수 있음을 증명했습니다.
3. **디지털 혁명 (1980년대~현재)**: 반도체 기술의 발전으로 ADC(Analog-to-Digital Converter)와 DAC(Digital-to-Analog Converter)의 가격이 급격히 하락하면서, 아날로그 통신이 디지털 통신으로 대체되는 패러다임 시프트가 발생했습니다. 오늘날 대부분의 통신 시스템은 디지털 방식을 사용합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 아날로그 신호와 디지털 신호의 특성 비교

| 특성 | 아날로그 신호 (Analog Signal) | 디지털 신호 (Digital Signal) |
|------|------------------------------|------------------------------|
| **정의** | 시간과 진폭이 연속적인 신호 | 시간과 진폭이 이산적인 신호 |
| **표현** | 사인파, 복합파형 | 구형파(Pulse), 2진 비트 열 |
| **수학적 표현** | x(t) = A·sin(2πft + φ) | x[n] = {0, 1}의 이산 시퀀스 |
| **값의 범위** | 무한한 연속값 (-∞ ~ +∞) | 유한한 이산값 (0, 1 또는 정해진 레벨) |
| **대역폭** | 신호 주파수 범위에 의해 결정 | 비트 전송률과 부호화 방식에 의해 결정 |
| **전송 매체** | 꼬임쌍선, 동축케이블, 무선 | 모든 매체 (광섬유 포함) |
| **증폭 방식** | 아날로그 증폭기 (Amplifier) | 디지털 재생 중계기 (Repeater) |
| **오류 처리** | 오류 검출/정정 불가능 | 오류 검출(CRC), 정정(FEC, ARQ) 가능 |
| **암호화** | 어렵고 비효율적 | 용이하고 강력함 (AES, RSA 등) |
| **저장 매체** | LP, 카세트테이프, VHS | CD, DVD, HDD, SSD, Flash Memory |

### 정교한 구조 다이어그램: 아날로그-디지털 변환 체계

```ascii
================================================================================
[ Analog-Digital Signal Conversion Architecture ]
================================================================================

                    [ ANALOG WORLD ]                [ DIGITAL WORLD ]

+------------------+                              +------------------+
|  자연계 정보      |                              |  컴퓨터/디지털   |
|  (음성, 영상,    |                              |  처리 시스템     |
|   온도, 압력 등) |                              +--------|---------+
+--------|---------+                                       |
         | 연속적                                           | 이산적
         v                                                 v
+------------------+          +------------------+   +------------------+
|   아날로그 신호   |          |      ADC         |   |   디지털 신호    |
|   x(t)           |=========>| (Analog-to-      |==>|   x[n]           |
|                  |          |  Digital Conv.)  |   |   (0, 1 비트열)  |
+--------|---------+          +--------|---------+   +--------|---------+
         |                             |                      |
         |                             v                      |
         |                    +------------------+            |
         |                    | 1. Sampling      |            |
         |                    |   (표본화)       |            |
         |                    |   Fs ≥ 2Fmax     |            |
         |                    +--------|---------+            |
         |                             |                      |
         |                             v                      |
         |                    +------------------+            |
         |                    | 2. Quantization  |            |
         |                    |   (양자화)       |            |
         |                    |   n-bit 해상도   |            |
         |                    +--------|---------+            |
         |                             |                      |
         |                             v                      |
         |                    +------------------+            |
         |                    | 3. Encoding      |            |
         |                    |   (부호화)       |            |
         |                    |   PCM, ADPCM 등  |            |
         |                    +--------|---------+            |
         |                             |                      |
         |                             v                      v
         |                    +------------------+   +------------------+
         |                    |   디지털 전송    |   | 디지털 신호 처리 |
         |                    |   (암호화, 압축) |   | (DSP, AI/ML)     |
         |                    +--------|---------+   +--------|---------+
         |                             |                      |
         |                             v                      |
         |                    +------------------+            |
         |                    |      DAC         |            |
         |                    | (Digital-to-     |            |
         |                    |  Analog Conv.)   |            |
         |                    +--------|---------+            |
         |                             |                      |
         v                             v                      v
+------------------+          +------------------+   +------------------+
|  아날로그 출력   |<=========|  필터링 (LPF)    |<--|  디지털 데이터   |
|  (스피커, 모니터)|          |  평활화          |   |  복원            |
+------------------+          +------------------+   +------------------+

================================================================================
[ Signal Waveform Comparison ]
================================================================================

아날로그 신호 (Analog Signal):           디지털 신호 (Digital Signal):
연속적인 파형                            이산적인 레벨

    /\/\/\                                  ___    ___    ___
   /      \                                |   |  |   |  |   |
  /        \              ──────           |   |__|   |__|   |
 /          \            (0 Volt)          0    1  0    1  0
/            \

+Vmax                                          +V
 |    /\      /\                              |      ___     ___
 |   /  \    /  \                             |     |   |   |   |
-+--/----\--/----\-- 0V                      -+-----+---+---+---+- 0V
 |                                                0   1   0   1
-Vmax

[ 특징: 무한한 중간값 ]                    [ 특징: 유한한 레벨만 존재 ]
```

### 심층 동작 원리: ADC 변환 3단계 프로세스

**1. 표본화 (Sampling)**:
- 연속적인 아날로그 신호를 일정한 시간 간격(Ts)으로 샘플링합니다.
- **나이퀴스트 정리(Nyquist Theorem)**: 원 신호의 최대 주파수를 Fmax라 할 때, 표본화 주파수 Fs는 Fs ≥ 2Fmax를 만족해야 에일리어싱(Aliasing) 없이 원 신호를 완벽히 복원할 수 있습니다.
- 예: 음성 통신(전화)은 3.4kHz까지의 주파수를 전송하므로, Fs = 8kHz로 샘플링합니다.

**2. 양자화 (Quantization)**:
- 각 샘플의 진폭을 미리 정의된 유한 개의 레벨 중 가장 가까운 값으로 근사합니다.
- **양자화 오차(Quantization Error)**: 실제 값과 양자화된 값 사이의 차이로, 이것이 양자화 잡음(Quantization Noise)이 됩니다.
- **SNR(신호 대 잡음비)**: n비트 양자화의 이론적 SNR은 약 6.02n + 1.76 dB입니다. 16비트 CD 오디오의 경우 약 98dB의 SNR을 가집니다.

**3. 부호화 (Encoding)**:
- 양자화된 각 레벨을 이진 코드(Binary Code)로 변환합니다.
- **PCM(Pulse Code Modulation)**: 가장 기본적인 디지털 부호화 방식으로, 각 샘플을 고정 길이의 이진수로 표현합니다.
- 예: 8비트 PCM은 256개(2^8)의 레벨을 표현할 수 있습니다.

### 핵심 코드: ADC/DAC 시뮬레이션 (Python)

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

class ADConverter:
    """
    아날로그-디지털 변환기(ADC) 시뮬레이션 클래스
    표본화, 양자화, 부호화 과정을 구현
    """

    def __init__(self, sampling_rate: int, bit_depth: int, v_ref: float = 1.0):
        """
        Args:
            sampling_rate: 초당 샘플링 횟수 (Hz)
            bit_depth: 양자화 비트 수 (예: 8, 16, 24비트)
            v_ref: 기준 전압 (진폭 범위: -v_ref ~ +v_ref)
        """
        self.fs = sampling_rate
        self.bit_depth = bit_depth
        self.v_ref = v_ref
        self.num_levels = 2 ** bit_depth
        self.quantization_step = (2 * v_ref) / self.num_levels

    def sampling(self, analog_signal: np.ndarray, original_fs: int) -> np.ndarray:
        """
        표본화(Sampling): 연속 신호를 이산 시간 신호로 변환

        Args:
            analog_signal: 원본 아날로그 신호 배열
            original_fs: 원본 신호의 샘플링 레이트
        """
        # 다운샘플링 비율 계산
        downsampling_ratio = original_fs / self.fs
        sampled_indices = np.arange(0, len(analog_signal), downsampling_ratio).astype(int)
        sampled_signal = analog_signal[sampled_indices]

        return sampled_signal, sampled_indices

    def quantization(self, sampled_signal: np.ndarray) -> tuple:
        """
        양자화(Quantization): 연속 진폭을 이산 레벨로 근사

        Returns:
            quantized_signal: 양자화된 신호
            quantization_error: 양자화 오차
            digital_codes: 디지털 코드 (정수 인덱스)
        """
        # 클리핑: 범위를 -v_ref ~ +v_ref로 제한
        clipped_signal = np.clip(sampled_signal, -self.v_ref, self.v_ref)

        # 양자화 레벨 계산
        # -v_ref → 코드 0, +v_ref → 코드 (num_levels - 1)
        normalized = (clipped_signal + self.v_ref) / (2 * self.v_ref)
        digital_codes = np.floor(normalized * self.num_levels).astype(int)
        digital_codes = np.clip(digital_codes, 0, self.num_levels - 1)

        # 양자화된 신호 복원 (DAC 과정의 일부)
        quantized_signal = (digital_codes / self.num_levels) * (2 * self.v_ref) - self.v_ref

        # 양자화 오차 계산
        quantization_error = clipped_signal - quantized_signal

        return quantized_signal, quantization_error, digital_codes

    def encoding(self, digital_codes: np.ndarray) -> list:
        """
        부호화(Encoding): 정수 코드를 이진 문자열로 변환
        """
        binary_codes = [format(code, f'0{self.bit_depth}b') for code in digital_codes]
        return binary_codes

    def adc_process(self, analog_signal: np.ndarray, original_fs: int) -> dict:
        """
        전체 ADC 과정 수행
        """
        # 1. 표본화
        sampled_signal, sampled_indices = self.sampling(analog_signal, original_fs)

        # 2. 양자화
        quantized_signal, quant_error, digital_codes = self.quantization(sampled_signal)

        # 3. 부호화
        binary_codes = self.encoding(digital_codes)

        return {
            'sampled_signal': sampled_signal,
            'sampled_indices': sampled_indices,
            'quantized_signal': quantized_signal,
            'quantization_error': quant_error,
            'digital_codes': digital_codes,
            'binary_codes': binary_codes,
            'snr_db': self._calculate_snr(quant_error)
        }

    def _calculate_snr(self, quantization_error: np.ndarray) -> float:
        """
        신호 대 양자화 잡음비(SNR) 계산
        이론값: SNR ≈ 6.02n + 1.76 dB
        """
        signal_power = np.var(quantization_error)  # 잡음 전력
        # 전체 신호 전력 추정
        total_power = (self.v_ref ** 2) / 3  # 균일 분포 가정
        noise_power = np.var(quantization_error)

        if noise_power > 0:
            snr_db = 10 * np.log10(total_power / noise_power)
        else:
            snr_db = float('inf')

        return snr_db


class DAConverter:
    """
    디지털-아날로그 변환기(DAC) 시뮬레이션 클래스
    """

    def __init__(self, original_fs: int, v_ref: float = 1.0):
        self.original_fs = original_fs
        self.v_ref = v_ref

    def dac_process(self, digital_codes: np.ndarray, bit_depth: int,
                    num_output_samples: int) -> np.ndarray:
        """
        DAC 과정: 디지털 코드를 아날로그 신호로 변환
        Zero-Order Hold 방식 사용
        """
        num_levels = 2 ** bit_depth

        # 디지털 코드를 전압 레벨로 변환
        voltage_levels = (digital_codes / num_levels) * (2 * self.v_ref) - self.v_ref

        # Zero-Order Hold: 각 샘플을 다음 샘플까지 유지
        samples_per_bit = num_output_samples // len(digital_codes)
        analog_output = np.repeat(voltage_levels, samples_per_bit)

        # 길이 맞춤
        if len(analog_output) < num_output_samples:
            analog_output = np.pad(analog_output,
                                   (0, num_output_samples - len(analog_output)),
                                   mode='edge')

        return analog_output

    def low_pass_filter(self, signal: np.ndarray, cutoff_freq: float) -> np.ndarray:
        """
        저역 통과 필터(LPF): 계단 현상 제거 및 평활화
        """
        nyquist = self.original_fs / 2
        normalized_cutoff = cutoff_freq / nyquist

        # Butterworth 저역 통과 필터 설계
        b, a = signal.butter(4, normalized_cutoff, btype='low')
        filtered_signal = signal.filtfilt(b, a, signal)

        return filtered_signal


# 사용 예시
if __name__ == "__main__":
    # 테스트 신호 생성 (1kHz 사인파 + 3kHz 고조파)
    original_fs = 44100  # CD 품질
    duration = 0.01  # 10ms
    t = np.linspace(0, duration, int(original_fs * duration), endpoint=False)

    # 아날로그 신호: 1kHz 기본파 + 3kHz 고조파
    analog_signal = 0.7 * np.sin(2 * np.pi * 1000 * t) + \
                    0.3 * np.sin(2 * np.pi * 3000 * t)

    # ADC 수행 (8kHz 샘플링, 8비트 양자화 - 전화 품질)
    adc = ADConverter(sampling_rate=8000, bit_depth=8, v_ref=1.0)
    result = adc.adc_process(analog_signal, original_fs)

    print(f"샘플링 레이트: {adc.fs} Hz")
    print(f"양자화 비트: {adc.bit_depth} bits")
    print(f"양자화 레벨: {adc.num_levels}")
    print(f"양자화 스텝: {adc.quantization_step:.6f} V")
    print(f"측정 SNR: {result['snr_db']:.2f} dB")
    print(f"이론 SNR: {6.02 * adc.bit_depth + 1.76:.2f} dB")
    print(f"첫 5개 샘플의 디지털 코드: {result['digital_codes'][:5]}")
    print(f"첫 5개 샘플의 이진 코드: {result['binary_codes'][:5]}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 아날로그 vs 디지털 통신 시스템 종합 비교

| 비교 항목 | 아날로그 통신 | 디지털 통신 | 승자 |
|----------|--------------|-------------|------|
| **신호 품질** | 전송 거리 증가시 품질 저하 | 재생 중계로 품질 유지 | 디지털 |
| **오류 제어** | 불가능 | CRC, FEC, ARQ 가능 | 디지털 |
| **암호화** | 어렵고 비효율적 | 강력한 암호화 가능 | 디지털 |
| **대역폭 효율** | 단순 신호에 유리 | 압축으로 효율 증가 | 경우에 따라 다름 |
| **하드웨어 복잡도** | 단순함 | 복잡함 (ADC/DAC, DSP) | 아날로그 |
| **전력 소모** | 일반적으로 낮음 | 높음 (디지털 처리) | 아날로그 |
| **전송 거리** | 증폭시 잡음 증폭 | 재생 중계로 무제한 | 디지털 |
| **다중화** | FDM 위주 | TDM, CDM, WDM 다양 | 디지털 |
| **저장 및 복사** | 품질 저하 | 무손실 복사 가능 | 디지털 |
| **비용** | 저렴 (단순 시스템) | 고가 (복잡한 시스템) | 아날로그 |

### 적용 분야별 최적 신호 방식

| 적용 분야 | 권장 방식 | 이유 |
|----------|----------|------|
| **음성 통신 (전화)** | 디지털 | 압축(PCM→ADPCM), 암호화, 교환 기능 |
| **음악 저장 (CD, 스트리밍)** | 디지털 | 무손실 복사, 오류 정정, 메타데이터 |
| **라디오 방송** | 혼합 (AM/FM→DAB) | 아날로그는 단순, 디지털은 품질/효율 |
| **TV 방송** | 디지털 | HD/UHD, 멀티채널, 데이터 방송 |
| **센서 데이터** | 아날로그 (근거리) / 디지털 (원거리) | 근거리는 단순성, 원거리는 노이즈 내성 |
| **RF 통신 (5G, Wi-Fi)** | 디지털 (베이스밴드) + 아날로그 (RF) | 하이브리드 방식 |
| **오디오 앰프** | 아날로그 (Class A/AB) / 디지털 (Class D) | 음질 vs 효율 트레이드오프 |

### 과목 융합 관점 분석

1. **컴퓨터구조와의 융합**:
   - **ADC/DAC 인터페이스**: 마이크로컨트롤러(MCU)와 센서 간의 인터페이스에서 ADC가 핵심 역할을 합니다. 10비트 ADC는 0~1023의 디지털 값을 출력합니다.
   - **DSP(Digital Signal Processor)**: 디지털 신호 처리를 위한 전용 프로세서가 실시간 오디오/비디오 처리에 사용됩니다.

2. **운영체제와의 융합**:
   - **오디오 서브시스템**: ALSA(Advanced Linux Sound Architecture)는 ADC/DAC 하드웨어를 추상화하여 애플리케이션에 오디오 서비스를 제공합니다.
   - **버퍼링과 지터 제어**: 디지털 오디오 스트리밍에서 커널이 버퍼를 관리하여 지터(Jitter)를 최소화합니다.

3. **보안과의 융합**:
   - **디지털 워터마킹**: 아날로그 신호를 디지털화한 후 저작권 정보를 삽입하여 불법 복제를 방지합니다.
   - **암호화**: 디지털 신호만 강력한 암호화가 가능하므로, 보안 통신에서는 필수적으로 디지털 방식이 사용됩니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오 1: 스마트팩토리 센서 네트워크 설계

**문제 상황**: 공장의 온도, 압력, 진동 센서 1,000개를 중앙 서버에 연결해야 합니다. 센서는 아날로그 출력(0~10V)을 생성하며, 공장 환경은 전자기 노이즈가 심합니다.

**기술사의 전략적 의사결정**:

1. **전송 방식 결정**:
   - **분석**: 아날로그 전송은 노이즈에 취약하여 긴 케이블에서 신호 왜곡이 심합니다.
   - **결정**: 센서 근처에 **분산형 ADC 모듈**을 설치하여 디지털화 후 전송합니다. RS-485 또는 이더넷을 사용하여 노이즈 내성을 확보합니다.

2. **샘플링 레이트 결정**:
   - **분석**: 온도는 천천히 변하므로 1Hz, 진동은 빠르게 변하므로 1kHz 이상의 샘플링이 필요합니다.
   - **결정**: **가변 샘플링** 방식을 채택하여 센서 유형별로 최적화합니다. 이를 통해 대역폭을 50% 절감합니다.

3. **양자화 비트 수 결정**:
   - **분석**: 12비트(4096레벨)는 0.1% 정밀도를 제공하며, 대부분의 산업용 센서에 충분합니다.
   - **결정**: 12비트 ADC를 표준으로 채택하되, 고정밀이 필요한 압력 센서에만 16비트 ADC를 사용합니다.

### 실무 시나리오 2: 오디오 스트리밍 서비스 품질 설계

**문제 상황**: 음악 스트리밍 서비스를 위한 오디오 코덱과 비트레이트를 결정해야 합니다.

**결정 요소 분석**:

| 코덱 | 비트레이트 | 품질 | 대역폭 | 배터리 소모 |
|------|-----------|------|--------|------------|
| **MP3** | 128~320 kbps | 양호 | 낮음 | 낮음 |
| **AAC** | 96~256 kbps | 우수 | 낮음 | 중간 |
| **FLAC** | 800~1500 kbps | 무손실 | 높음 | 높음 |
| **Opus** | 64~510 kbps | 우수 | 매우 낮음 | 낮음 |

**기술사의 결정**:
- 모바일 네트워크: **Opus 128 kbps** (높은 효율, 낮은 지연)
- Wi-Fi/유선: **FLAC** (무손실, 오디오파일 대상)
- 적응형 스트리밍: 네트워크 상태에 따라 자동 전환

### 안티패턴 (Anti-patterns)

- **안티패턴 1 - 과도한 양자화 비트**:
  오디오에서 24비트 이상의 양자화는 인간의 청각 한계를 넘어섭니다. 16비트(96dB SNR)면 충분하며, 24비트는 마케팅 목적으로 과장됩니다.

- **안티패턴 2 - 나이퀴스트 위반 샘플링**:
  20kHz까지의 오디오를 32kHz로 샘플링하면 에일리어싱이 발생합니다. 반드시 40kHz 이상(일반적으로 44.1kHz 또는 48kHz)을 사용해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 영역 | 아날로그 | 디지털 | 개선 효과 |
|----------|----------|--------|----------|
| **전송 품질** | 거리당 3dB 감쇠 | 재생 중계로 무손실 | 품질 균일성 100% |
| **오류율** | 측정 불가 | 10^-9 이하 달성 | 신뢰성 대폭 향상 |
| **대역폭 효율** | 기본 | 압축 시 50~80% 절감 | 비용 30% 이상 절감 |
| **보안성** | 취약 | 강력한 암호화 | 데이터 유출 0% |

### 미래 전망 및 진화 방향

- **소프트웨어 정의 라디오(SDR)**: 아날로그 RF 프론트엔드를 제외한 모든 처리를 디지털로 수행하여, 펌웨어 업데이트만으로 새로운 통신 표준을 지원합니다.

- **AI 기반 신호 처리**: 딥러닝을 활용한 노이즈 제거, 신호 복원, 자동 변조 식별이 가능해져, 열악한 채널 환경에서도 통신 품질을 획기적으로 개선합니다.

- **양자 신호 처리**: 양자 비트(Qubit)를 활용한 양자 통신은 아날로그와 디지털의 경계를 넘어서는 새로운 패러다임을 제시합니다. 양자 얽힘을 이용한 무해킹 통신이 상용화될 것입니다.

### 참고 표준/가이드

| 표준 | 기관 | 내용 |
|------|------|------|
| **ITU-T G.711** | ITU-T | PCM 음성 부호화 표준 (64 kbps) |
| **ITU-T G.729** | ITU-T | 음성 압축 표준 (8 kbps) |
| **IEEE 1241** | IEEE | ADC 테스트 및 성능 측정 표준 |
| **AES3 (AES/EBU)** | AES | 디지털 오디오 인터페이스 표준 |
| **HDMI 2.1** | HDMI Forum | 디지털 비디오/오디오 인터페이스 |

---

## 관련 개념 맵 (Knowledge Graph)
- [샤논 채널 용량](./shannon_hartley_capacity.md) - 디지털 통신의 이론적 한계
- [변조 기술](./modulation_ask_fsk_psk_qam.md) - 디지털 데이터의 아날로그 반송파 실림
- [PCM 부호화](./pcm_sampling_quantization.md) - 아날로그 신호의 디지털 변환 표준
- [전송 모드](./transmission_modes_duplex.md) - 단방향/양방향 통신 방식
- [오류 제어](./error_detection_parity_crc.md) - 디지털 통신의 오류 검출 및 정정

---

## 어린이를 위한 3줄 비유 설명
1. **아날로그 신호**는 **물이 호스를 통해 흐르는 것**과 같아요. 물의 양이 조금씩 계속 변하듯이, 신호도 아주 부드럽게 변합니다.
2. **디지털 신호**는 **스위치를 켰다 껐다 하는 것**과 같아요. 불이 켜져 있거나 꺼져 있거나 둘 중 하나만 있죠. 컴퓨터는 이렇게 0과 1만으로 모든 정보를 처리합니다.
3. **ADC**는 **음악을 악보로 적는 것**과 같아요. 연주되는 소리(아날로그)를 기호로 적어서(디지털) 저장하고, 나중에 다시 연주할 수 있게 해줍니다!
