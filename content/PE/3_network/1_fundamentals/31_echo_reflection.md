+++
title = "031. 에코 (Echo, 반향)"
description = "통신 시스템에서 신호 반사로 인해 발생하는 에코(Echo)의 원리, 통신 품질에 미치는 영향, 에코 제거 기술(EC, AEC)을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["Echo", "EchoCanceller", "Hybrid", "Reflection", "VoIP", "TLE", "AEC"]
categories = ["studynotes-3_network"]
+++

# 031. 에코 (Echo, 반향)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 에코는 통신 신호가 임피던스 불일치 지점에서 반사되어 송신자에게 돌아오는 현상으로, 음성 통신에서는 Hybrid의 4-wire/2-wire 변환 지점이, 패킷 네트워크에서는 지연과 결합하여 심각한 품질 저하를 유발합니다.
> 2. **가치**: 에코 제거기(Echo Canceller)는 현대 통신 시스템의 필수 구성요소로, VoIP 품질의 핵심 결정 요소이며 ITU-T G.168/G.167 표준으로 규정된 성능 요구사항을 충족해야 합니다.
> 3. **융합**: 음성 인식 AI의 전처리 단계, 화상 회의 시스템, 헤드폰/스피커의 음향 피드백 제거, 레이더/초음파 센서의 클러터 필터링 등 다양한 신호 처리 분야의 근간이 되는 기술입니다.

---

## Ⅰ. 개요 (Context & Background)

**에코(Echo)**는 송신된 신호가 어떤 경로를 거쳐 지연된 후 송신자에게 되돌아오는 현상입니다. 통신 시스템에서는 주로 두 가지 형태로 나타납니다:

1. **통신 회선 에코(Network Echo)**: 임피던스 불일치 지점(주로 Hybrid)에서 반사
2. **음향 에코(Acoustic Echo)**: 스피커에서 출력된 소리가 마이크로 다시 입력

에코는 지연이 클수록, 반사 계수가 높을수록 통신 품질에 악영향을 미칩니다. 특히 VoIP와 같은 패킷 네트워크에서는 코덱 지연+네트워크 지연이 더해져 에코가 매우 성가신 문제가 됩니다.

**💡 비유**: 에코는 **'산속에서의 메아리'**와 같습니다.
- 산을 향해 "안녕!"하고 외치면, 잠시 후 "안녕~"하고 돌아오는 소리가 들립니다.
- 산(반사체)이 가까우면 에코가 빨리 돌아오고, 멀리 있으면 늦게 돌아옵니다.
- 내 목소리가 컸을수록(높은 반사율), 에코도 크게 들립니다.
- 통화 중에 내 목소리가 지연되어 들리면, 대화가 매우 어색해집니다.

**등장 배경 및 발전 과정**:
1. **전화망 초기 (1900년대)**: 장거리 전화에서 하이브리드 변압기를 통한 4선/2선 변환 시 임피던스 불일치로 에코 발생
2. **에코 억제기 (1960년대)**: 에코 감지 시 수신 경로 차단 (Half-duplex 유사 동작)
3. **에코 제거기 (1970년대~)**: 적응 필터로 에코 성분 추정 후 제거 (Full-duplex 유지)
4. **VoIP 시대 (2000년대~)**: 지연 증가로 에코 문제 심화, G.168 표준 에코 제거기 필수화

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석: 에코 유형과 원인

| 에코 유형 | 발생 위치 | 원인 | 지연 범위 | 대응 기술 |
|----------|----------|------|----------|----------|
| **Hybrid Echo** | 4-wire/2-wire 경계 | 임피던스 불일치 | 0~30ms | Line Echo Canceller (LEC) |
| **Acoustic Echo** | 스피커-마이크 경로 | 음향 결합 | 10~500ms | Acoustic Echo Canceller (AEC) |
| **Network Echo** | 네트워크 경로 | 지연+반사 | 가변적 | NLP, Comfort Noise |
| **Room Echo** | 실내 환경 | 벽/천장 반사 | 10~200ms | Room Correction, AEC |

### 정교한 구조 다이어그램: Hybrid와 에코 발생

```ascii
================================================================================
[ Telephone Hybrid and Echo Generation ]
================================================================================

                              Hybrid Transformer
    4-Wire Side (Digital)           (4-to-2 Wire Conversion)
    +------------------+           +------------------------+
    |                  |           |          ┌───────┐    |
    |  Remote Party    |           |   Rx ────┤       │    |
    |  (Far End)       |  ─────────────────> │       │    |
    |                  |           |          │ Hybrid│────┼──> 2-Wire
    |                  |           |          │       │    │    (Local
    |                  |           |   Tx <───┤       │<───┼──> Loop)
    |                  |  <───────────────── │       │    |
    |  Local Party     |           |          └───────┘    |
    |  (Near End)      |           +------------------------+
    +------------------+
           ^    |
           |    |        IMPEDANCE MISMATCH
           |    v           ┌──────────────┐
        ECHO!  <────────────│  Reflection  │
                           │  Point        │
                           └──────────────┘
                                  │
                                  v
                              Echo Path

    Problem: Hybrid cannot perfectly match all line impedances
             → Some transmitted signal leaks into received path
             → ECHO returns to the speaker!

================================================================================
[ Echo Canceller Operation Principle ]
================================================================================

                              Echo Canceller
    Rx Signal                        +---------------------+
    (Far End)                        |                     |
    ─────────────────────────────>──┤  Reference Input    |
                                     |                     |
    Near End Signal                 │  Adaptive Filter    │
    (Local Mic)                     │  h(n) ≈ Echo Path   │
    ─────────────────────>──(+)─────┤                     │
                               |    |                     │
                               |    |  Estimated Echo     │
                               |    |  ē(n) = r(n) * h(n) |
                               |    |                     │
                               v    +----------│----------+
                              (+) <─────────────┘  Subtraction
                               |
                               |  Error Signal e(n)
                               |  = Near End - Estimated Echo
                               v
                          [ Clean Output ]

    Adaptive Algorithm (LMS/NLS):
        h(n+1) = h(n) + μ × e(n) × r(n)

    Where:
        μ = step size (convergence speed vs steady-state error tradeoff)
        r(n) = far-end reference signal
        e(n) = error signal (output)

================================================================================
[ Echo Path Impulse Response ]
================================================================================

Amplitude
    |
    |     *         *    *
    |    * *   *   * *  * *
    |   *   * * * *   **   *
    |  *     *   *         *
    | *                    *
    |*_________________________*__________ Time (samples)
    0   5  10  15  20  25  30  35

    |← Echo Tail Length →|
       (convergence time)

    - First peak: Direct reflection at hybrid
    - Following peaks: Multiple reflections in the line
    - Echo tail: Duration of echo impulse response
```

### 심층 동작 원리

**1. Hybrid 임피던스 불일치와 반사 계수**:
```
반사 계수 (Reflection Coefficient):
        Γ = (Z_L - Z_0) / (Z_L + Z_0)

여기서:
        Z_L = 부하 임피던스 (가입자선)
        Z_0 = Hybrid 기준 임피던스 (보통 600Ω 또는 900Ω)

반사 손실 (Return Loss):
        RL = -20 log₁₀|Γ| [dB]

예시:
        Z_L = 700Ω, Z_0 = 600Ω
        Γ = (700-600)/(700+600) = 100/1300 ≈ 0.077
        RL = -20 log₁₀(0.077) ≈ 22.3 dB

일반적 요구사항:
        ERL (Echo Return Loss) > 6 dB (저품질)
        ERL > 15 dB (양호)
        ERL > 25 dB (우수)
```

**2. 적응 필터를 이용한 에코 제거**:
```
LMS (Least Mean Square) 알고리즘:

필터 출력 (추정 에코):
        ŷ(n) = Σ w_k(n) × x(n-k)
               k=0 to N-1

오차 신호:
        e(n) = d(n) - ŷ(n)

필터 계수 갱신:
        w_k(n+1) = w_k(n) + μ × e(n) × x(n-k)

여기서:
        x(n) = 원신호 (Far-end)
        d(n) = 수신 신호 (Near-end + Echo)
        ŷ(n) = 추정 에코
        e(n) = 에코가 제거된 신호
        μ = 스텝 사이즈 (수렴 속도 조절)
        N = 필터 길이 (에코 테일 커버)

수렴 조건:
        0 < μ < 2/(N × P_x)
        P_x = 입력 신호 전력
```

**3. 에코 테일 길이(Echo Tail Length)**:
```
에코 테일 길이 = 에코 지속 시간 (샘플 수)

필요한 필터 길이:
        N = (에코 테일 길이) / (샘플링 주기)

예시 (8kHz 샘플링):
        에코 테일 32ms → N = 32ms × 8 = 256 샘플
        에코 테일 128ms → N = 128ms × 8 = 1024 샘플

일반적 요구사항:
        PSTN Hybrid Echo: 8-32ms 테일
        VoIP Gateway: 64-128ms 테일
        AEC (음향): 200-500ms 테일
```

### 핵심 코드: LMS 에코 제거기 구현

```python
"""
LMS 기반 에코 제거기 (Echo Canceller) 구현
Hybrid Echo 및 Acoustic Echo 제거 시뮬레이션
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve
from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class EchoCancellerConfig:
    """에코 제거기 설정"""
    filter_length: int = 256      # 필터 길이 (샘플)
    step_size: float = 0.01       # LMS 스텝 사이즈
    sample_rate: int = 8000       # 샘플링 레이트 (Hz)
    echo_tail_ms: float = 32      # 에코 테일 길이 (ms)


class LMSEchoCanceller:
    """
    LMS 알고리즘 기반 에코 제거기
    """

    def __init__(self, config: EchoCancellerConfig):
        self.config = config
        self.filter_length = config.filter_length
        self.step_size = config.step_size

        # 적응 필터 계수 (0으로 초기화)
        self.weights = np.zeros(self.filter_length)

        # 입력 버퍼 (지연 라인)
        self.buffer = np.zeros(self.filter_length)

        # 통계
        self.error_history = []
        self.weight_history = []

    def process_sample(self, far_end: float, near_end: float) -> Tuple[float, float]:
        """
        단일 샘플 처리

        Args:
            far_end: 원격 신호 (에코 원본)
            near_end: 근단 신호 (에코 포함)

        Returns:
            error: 에코 제거된 신호
            echo_estimate: 추정된 에코
        """
        # 버퍼 업데이트 (shift right, new sample at front)
        self.buffer = np.roll(self.buffer, 1)
        self.buffer[0] = far_end

        # 에코 추정 (필터 출력)
        echo_estimate = np.dot(self.weights, self.buffer)

        # 오차 계산 (에코 제거된 신호)
        error = near_end - echo_estimate

        # 필터 계수 갱신 (LMS)
        self.weights += self.step_size * error * self.buffer

        return error, echo_estimate

    def process(self, far_end: np.ndarray, near_end: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        전체 신호 처리

        Returns:
            error: 에코 제거된 신호
            echo_estimates: 추정된 에코
        """
        num_samples = len(far_end)
        error = np.zeros(num_samples)
        echo_estimates = np.zeros(num_samples)

        for i in range(num_samples):
            error[i], echo_estimates[i] = self.process_sample(far_end[i], near_end[i])

        return error, echo_estimates

    def get_erle(self, near_end: np.ndarray, error: np.ndarray) -> float:
        """
        ERLE (Echo Return Loss Enhancement) 계산
        에코 제거 성능 지표
        """
        echo_power = np.var(near_end)
        residual_power = np.var(error)

        if residual_power > 0:
            erle = 10 * np.log10(echo_power / residual_power)
        else:
            erle = float('inf')

        return erle


def create_echo_path(tail_length: int, sample_rate: int) -> np.ndarray:
    """
    에코 경로 임펄스 응답 생성
    실제 환경을 시뮬레이션하기 위한 에코 특성
    """
    # 지연 (첫 반사까지의 시간)
    delay_samples = int(0.005 * sample_rate)  # 5ms 지연

    # 감쇠 계수
    attenuation = 0.3

    # 임펄스 응답 생성 (지수 감쇠)
    t = np.arange(tail_length)
    decay_rate = 0.02  # 감쇠율

    impulse_response = attenuation * np.exp(-decay_rate * t)
    impulse_response[:delay_samples] = 0  # 지연 구간

    return impulse_response


def simulate_echo_scenario():
    """
    에코 시나리오 시뮬레이션
    """
    # 설정
    sample_rate = 8000
    duration = 5.0  # 5초
    num_samples = int(duration * sample_rate)
    echo_tail_ms = 32
    filter_length = int(echo_tail_ms * sample_rate / 1000)

    config = EchoCancellerConfig(
        filter_length=filter_length,
        step_size=0.005,
        sample_rate=sample_rate,
        echo_tail_ms=echo_tail_ms
    )

    # 신호 생성
    t = np.linspace(0, duration, num_samples)

    # 원격 신호 (Far-end): 음성 대역 잡음
    far_end = np.random.randn(num_samples) * 0.5

    # 일부 구간에만 신호 (음성과 유사)
    far_end[:num_samples//4] *= 0.1
    far_end[num_samples//2:3*num_samples//4] *= 0.1

    # 에코 경로
    echo_path = create_echo_path(filter_length, sample_rate)

    # 에코 생성 (콘볼루션)
    echo = convolve(far_end, echo_path, mode='same')

    # 근단 신호 (Near-end): 에코 + 약간의 배경 잡음
    near_end_speech = np.random.randn(num_samples) * 0.05  # 작은 배경 잡음
    near_end = echo + near_end_speech

    # 에코 제거기 동작
    ec = LMSEchoCanceller(config)
    error, echo_estimates = ec.process(far_end, near_end)

    # ERLE 계산
    erle = ec.get_erle(near_end, error)

    print(f"에코 테일 길이: {echo_tail_ms} ms")
    print(f"필터 길이: {filter_length} 샘플")
    print(f"ERLE (Echo Return Loss Enhancement): {erle:.2f} dB")

    # 시각화
    fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)

    time_ms = np.arange(num_samples) / sample_rate * 1000

    # 원격 신호
    axes[0].plot(time_ms, far_end, 'b', linewidth=0.5)
    axes[0].set_ylabel('Far-end Signal')
    axes[0].set_title('Far-end Signal (Original)')
    axes[0].grid(True, alpha=0.3)

    # 에코가 포함된 근단 신호
    axes[1].plot(time_ms, near_end, 'r', linewidth=0.5)
    axes[1].set_ylabel('Near-end Signal')
    axes[1].set_title('Near-end Signal (with Echo)')
    axes[1].grid(True, alpha=0.3)

    # 추정된 에코
    axes[2].plot(time_ms, echo_estimates, 'g', linewidth=0.5)
    axes[2].set_ylabel('Estimated Echo')
    axes[2].set_title('Estimated Echo (Filter Output)')
    axes[2].grid(True, alpha=0.3)

    # 에코 제거된 신호
    axes[3].plot(time_ms, error, 'purple', linewidth=0.5)
    axes[3].set_ylabel('Error Signal')
    axes[3].set_xlabel('Time (ms)')
    axes[3].set_title('Error Signal (Echo Cancelled Output)')
    axes[3].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('echo_cancellation.png', dpi=150)
    plt.show()

    # 필터 수렴 시각화
    plt.figure(figsize=(10, 4))
    plt.plot(ec.weights, 'b-', linewidth=1.5)
    plt.plot(echo_path, 'r--', linewidth=1.5, label='True Echo Path')
    plt.xlabel('Filter Tap')
    plt.ylabel('Coefficient Value')
    plt.title('Adaptive Filter Coefficients vs True Echo Path')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('filter_convergence.png', dpi=150)
    plt.show()

    return ec, far_end, near_end, error


def calculate_erle_vs_time():
    """
    시간에 따른 ERLE 변화 분석 (수렴 특성)
    """
    sample_rate = 8000
    num_samples = sample_rate * 3  # 3초
    filter_length = 256

    # 신호 생성
    far_end = np.random.randn(num_samples)
    echo_path = create_echo_path(filter_length, sample_rate)
    echo = convolve(far_end, echo_path, mode='same')
    near_end = echo + np.random.randn(num_samples) * 0.01

    # 다양한 스텝 사이즈로 테스트
    step_sizes = [0.001, 0.005, 0.01, 0.02]
    colors = ['b', 'g', 'r', 'm']

    plt.figure(figsize=(12, 6))

    for step_size, color in zip(step_sizes, colors):
        config = EchoCancellerConfig(filter_length=filter_length, step_size=step_size)
        ec = LMSEchoCanceller(config)
        error, _ = ec.process(far_end, near_end)

        # 구간별 ERLE 계산 (100ms 윈도우)
        window_size = int(0.1 * sample_rate)
        erle_values = []

        for i in range(0, num_samples - window_size, window_size // 2):
            window_near = near_end[i:i+window_size]
            window_error = error[i:i+window_size]

            echo_power = np.var(window_near)
            residual_power = np.var(window_error)

            if residual_power > 1e-10:
                erle = 10 * np.log10(echo_power / residual_power)
            else:
                erle = 60  # 상한

            erle_values.append(erle)

        time_axis = np.arange(len(erle_values)) * (window_size / 2) / sample_rate * 1000
        plt.plot(time_axis, erle_values, color=color, label=f'μ={step_size}')

    plt.xlabel('Time (ms)')
    plt.ylabel('ERLE (dB)')
    plt.title('ERLE Convergence vs Step Size')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim([0, 40])
    plt.tight_layout()
    plt.savefig('erle_convergence.png', dpi=150)
    plt.show()


if __name__ == "__main__":
    print("=== 에코 제거기 시뮬레이션 ===\n")

    # 기본 시뮬레이션
    ec, far_end, near_end, error = simulate_echo_scenario()

    # 수렴 특성 분석
    print("\n수렴 특성 분석 중...")
    calculate_erle_vs_time()

    # VoIP 요구사항
    print("\n=== ITU-T G.168 요구사항 ===")
    print("ERLE 요구사항:")
    print("  - 최소 20 dB (NLP 비활성)")
    print("  - 최소 24 dB (NLP 활성)")
    print("  - 수렴 시간: < 500ms")
    print("  - 에코 테일: 최대 128ms 지원")
