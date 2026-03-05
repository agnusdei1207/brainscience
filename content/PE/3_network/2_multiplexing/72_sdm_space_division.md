+++
title = "072. 공간 분할 다중화 (SDM - Space Division Multiplexing)"
description = "공간 분할 다중화의 정의, 원리, MIMO 시스템, 그리고 5G/6G Massive MIMO로의 진화를 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["SDM", "SpaceDivisionMultiplexing", "MIMO", "MassiveMIMO", "Beamforming", "5G", "SpatialStreaming"]
categories = ["studynotes-3_network"]
+++

# 072. 공간 분할 다중화 (SDM)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 공간 분할 다중화(SDM)는 물리적으로 분리된 경로(다중 안테나, 다중 광섬유 코어)를 통해 독립적인 데이터 스트림을 동시에 전송하여, 공간적 자원을 활용한 전송 용량 확장 기술입니다.
> 2. **가치**: MIMO(Multiple-Input Multiple-Output) 시스템을 통해 동일 주파수/대역폭으로 다중 데이터 스트림을 전송하여, 스펙트럼 효율을 선형적으로 증가시키고 5G/6G의 핵심 기술인 Massive MIMO의 기반이 됩니다.
> 3. **융합**: WiFi 4/5/6/7의 MIMO, 4G LTE의 다중 안테나, 5G NR의 Massive MIMO(64~256 안테나), 그리고 다중 코어 광섬유(MCF)에 이르기까지 모든 차세대 통신의 용량 확장 기술입니다.

---

## Ⅰ. 개요 (Context & Background)

공간 분할 다중화(Space Division Multiplexing, SDM)는 **공간적으로 분리된 채널을 통해 여러 신호를 동시에 전송**하는 다중화 기법입니다. 이는 물리적 분리(다중 케이블, 다중 안테나)를 통해 이루어지며, 현대 무선 통신에서는 MIMO 기술로 구현됩니다.

### SDM의 기본 정의

```
공간 분할 다중화 (SDM):
- 유선: 다중 광섬유 코어, 다중 케이블
- 무선: 다중 안테나 배열 (MIMO)

핵심 원리:
- 각 안테나/경로는 독립적인 공간 채널
- 동일 주파수/시간/코드를 사용하되 공간으로 분리
- 채널 행렬 H의 랭크(Rank)가 다중화 이득 결정
```

### SDM의 종류 및 발전

| 종류 | 안테나 수 | 다중화 이득 | 응용 분야 |
|------|----------|------------|----------|
| **SISO** | 1×1 | 1 (기준) | 초기 무선 시스템 |
| **SIMO** | 1×N | 1 (다이버시티만) | 수신 다이버시티 |
| **MISO** | N×1 | 1 (빔포밍) | 송신 빔포밍 |
| **SU-MIMO** | M×N | min(M,N) | WiFi, LTE |
| **MU-MIMO** | M×N (다중 사용자) | 사용자 수 × 안테나 | LTE-Advanced, 5G |
| **Massive MIMO** | 64~256×N | 매우 높음 | 5G, 6G |

**💡 비유**: SDM은 **'차선이 여러 개인 고속도로'**와 같습니다.
- 1차선 도로(SISO)에서는 한 번에 한 대만 지나갈 수 있습니다.
- 4차선 도로(4×4 MIMO)에서는 4대가 동시에 지나갈 수 있습니다.
- 차선이 늘어날수록 동시 통행량이 선형적으로 증가합니다.
- Massive MIMO는 64차량, 128차량 고속도로와 같습니다.

**등장 배경 및 발전 과정**:

1. **다중 안테나의 초기 개념 (1980~90년대)**:
   다이버시티(Diversity) 기술로 시작되어, 다중 경로 페이딩을 극복하기 위한 목적으로 연구되었습니다. 이 시기에는 주로 수신측 다중 안테나(SIMO)가 연구되었습니다.

2. **MIMO 이론의 확립 (1990년대 후반)**:
   1998년 Foschini와 Gans, 그리고 1999년 Telatar의 논문에서 MIMO 채널 용량이 안테나 수에 선형적으로 비례함이 증명되었습니다. 이는 통신 이론의 획기적 발전이었습니다.

3. **WiFi MIMO 표준화 (2000년대)**:
   802.11n(2009)에서 최대 4×4 MIMO가 도입되어 600Mbps 전송 속도를 달성했습니다. 이후 802.11ac(WiFi 5), 802.11ax(WiFi 6)에서 8×8 MIMO까지 확장되었습니다.

4. **Massive MIMO의 등장 (2010년대~현재)**:
   Marzetta(2010)가 Massive MIMO 개념을 제안했습니다. 5G에서 64, 128, 256개 안테나 배열이 상용화되어, 6G에서는 하이브리드 빔포밍과 결합한 초대형 안테나 배열로 진화하고 있습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### MIMO 시스템 구조

```ascii
================================================================================
[ MIMO System Architecture ]
================================================================================

   송신측 (Transmitter)                    수신측 (Receiver)
   ==================                    ==================

   데이터 스트림                               복원된 데이터
        |                                          ^
        v                                          |
   +-----------+         무선 채널           +-----------+
   | 공간      |                              | 공간      |
   | 분할      |                              | 합성      |
   | (Precoding)|                             | (Combining)|
   +-----------+                              +-----------+
        |                                          ^
        |     +-----------------------------+      |
        |     |      무선 채널 (Channel)     |      |
        |     |                             |      |
        +---->|  H_11  H_12 ... H_1N       |----->|
        |     |  H_21  H_22 ... H_2N       |      |
        +---->|   .     .         .        |----->|
        |     |   .     .         .        |      |
        +---->|  H_M1  H_M2 ... H_MN       |----->|
              +-----------------------------+

   송신 안테나: M개                         수신 안테나: N개

   채널 행렬 H (N × M):
   y = H·x + n

   다중화 이득 = Rank(H) ≤ min(M, N)

================================================================================
[ Spatial Multiplexing: Data Stream Mapping ]
================================================================================

   직렬 데이터 스트림
   ==================
   b_0 b_1 b_2 b_3 b_4 b_5 b_6 b_7 ...
            |
            v
   +-----------------+
   |  직렬-병렬      |
   |  변환 (S/P)     |
   +-----------------+
            |
            v
   병렬 데이터 스트림 (4×4 MIMO 예시)
   =================================
   스트림 1: b_0 b_4 b_8  ...  -----> [안테나 1]
   스트림 2: b_1 b_5 b_9  ...  -----> [안테나 2]
   스트림 3: b_2 b_6 b_10 ...  -----> [안테나 3]
   스트림 4: b_3 b_7 b_11 ...  -----> [안테나 4]

   각 안테나에서 독립적인 데이터 전송
   → 전송 속도 4배 증가

================================================================================
[ MIMO Channel Matrix and Capacity ]
================================================================================

   채널 모델:
   ┌   ┐   ┌                    ┐   ┌   ┐   ┌   ┐
   │y_1│   │ h_11  h_12  h_13  │   │x_1│   │n_1│
   │y_2│ = │ h_21  h_22  h_23  │ · │x_2│ + │n_2│
   │y_3│   │ h_31  h_32  h_33  │   │x_3│   │n_3│
   │y_4│   │ h_41  h_42  h_43  │   │   │   │n_4│
   └   ┘   └                    ┘   └   ┘   └   ┘

   (4×3 MIMO: 4 수신, 3 송신 안테나)

   MIMO 채널 용량 (Shannon):
   C = B·log₂(det(I + (SNR/M)·H·H^H))  [bits/s]

   특수 케이스 (직교 채널, H^H·H = N·I):
   C = M·B·log₂(1 + SNR/N)  ← M배 용량 증가!

   현실적 이득:
   - 이상적: M배 증가
   - 실제: 0.5M ~ 0.8M (채널 상관, 간섭)

================================================================================
[ SU-MIMO vs MU-MIMO ]
================================================================================

   SU-MIMO (Single-User MIMO)
   ==========================
   - 한 사용자에게 모든 스트림 할당
   - 사용자 장비에 다중 안테나 필요

      기지국
      +--+
      |●●| -----> [사용자 A (4 안테나)]
      |●●|
      +--+

   MU-MIMO (Multi-User MIMO)
   =========================
   - 여러 사용자에게 스트림 분배
   - 각 사용자는 적은 안테나만 있어도 됨

      기지국
      +--+
      |●●| --+---> [사용자 A (2 안테나)]
      |●●|  +---> [사용자 B (2 안테나)]
      +--+   +---> [사용자 C (2 안테나)]

   장점: 스마트폰처럼 작은 기기에서도 MIMO 혜택

================================================================================
```

### MIMO의 핵심 기술

| 기술 | 설명 | 이득 | 복잡도 |
|------|------|------|--------|
| **공간 다중화** | 독립 데이터 스트림 동시 전송 | 용량 증가 | 중간 |
| **빔포밍** | 신호 에너지 집중 | SNR 향상, 간섭 감소 | 높음 |
| **다이버시티** | 다중 경로 신호 결합 | 페이딩 감소 | 낮음 |
| **Precoding** | 송신측 채널 사전 보상 | 간섭 제거 | 매우 높음 |
| **SDMA** | 공간적 사용자 분리 | 다중 접속 용량 | 매우 높음 |

### 심층 동작 원리: MIMO 5단계 프로세스

1. **채널 상태 정보(CSI) 획득**:
   - 수신측에서 파일럿 신호로 채널 행렬 H 추정
   - TDD: 상향링크 측정으로 하향링크 CSI 추정 (상호성)
   - FDD: 수신측에서 CSI 피드백 필요

2. **공간 Precoding**:
   - 송신 신호 x = W·s (W: Precoding 행렬)
   - SVD 기반: H = U·Σ·V^H, W = V
   - 채널을 독립적인 병렬 서브채널로 분해

3. **동시 전송**:
   - 각 안테나에서 독립적인 데이터 전송
   - 동일 주파수, 동일 시간 자원 사용
   - 공간적 직교성으로 분리

4. **수신 신호 처리**:
   - y = H·x + n 수신
   - MMSE, ZF, ML 등으로 검출
   - 각 스트림을 개별적으로 복원

5. **데이터 재조립**:
   - 병렬-직렬 변환
   - 원본 비트 스트림 복원

### 핵심 코드: MIMO 시스템 시뮬레이터 (Python)

```python
import numpy as np
from typing import Tuple, List
from dataclasses import dataclass

@dataclass
class MIMOConfig:
    """MIMO 설정"""
    n_tx: int = 4      # 송신 안테나 수
    n_rx: int = 4      # 수신 안테나 수
    n_streams: int = 4 # 데이터 스트림 수
    modulation: str = "QPSK"
    snr_db: float = 20.0

class MIMOChannel:
    """MIMO 채널 모델"""

    def __init__(self, n_tx: int, n_rx: int, correlation: float = 0.0):
        self.n_tx = n_tx
        self.n_rx = n_rx
        self.correlation = correlation
        self.H = None

    def generate(self) -> np.ndarray:
        """MIMO 채널 행렬 생성"""
        # i.i.d. Rayleigh 페이딩
        H = (np.random.randn(self.n_rx, self.n_tx) +
             1j * np.random.randn(self.n_rx, self.n_tx)) / np.sqrt(2)

        # 공간 상관 적용 (간소화)
        if self.correlation > 0:
            R_tx = self._correlation_matrix(self.n_tx, self.correlation)
            R_rx = self._correlation_matrix(self.n_rx, self.correlation)
            H = np.sqrt(R_rx) @ H @ np.sqrt(R_tx)

        self.H = H
        return H

    def _correlation_matrix(self, n: int, rho: float) -> np.ndarray:
        """지수 상관 행렬"""
        R = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                R[i, j] = rho ** abs(i - j)
        return R

class MIMOPrecoder:
    """MIMO Precoding"""

    @staticmethod
    def svd_precoding(H: np.ndarray, n_streams: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """SVD 기반 Precoding"""
        U, S, Vh = np.linalg.svd(H, full_matrices=False)

        # 상위 n_streams개의 모드 선택
        V = Vh.conj().T[:, :n_streams]
        U_rx = U[:, :n_streams]

        return V, U_rx, S[:n_streams]

    @staticmethod
    def zero_forcing(H: np.ndarray) -> np.ndarray:
        """Zero-Forcing Precoding"""
        # W = H^H (H H^H)^{-1}
        W = np.linalg.pinv(H)
        return W

class MIMODetector:
    """MIMO 검출기"""

    @staticmethod
    def zf_detection(y: np.ndarray, H: np.ndarray) -> np.ndarray:
        """Zero-Forcing 검출"""
        W = np.linalg.pinv(H)
        x_hat = W @ y
        return x_hat

    @staticmethod
    def mmse_detection(y: np.ndarray, H: np.ndarray, noise_var: float) -> np.ndarray:
        """MMSE 검출"""
        n_tx = H.shape[1]
        W = H.conj().T @ np.linalg.inv(H @ H.conj().T + noise_var * np.eye(H.shape[0]))
        x_hat = W @ y
        return x_hat

    @staticmethod
    def ml_detection(y: np.ndarray, H: np.ndarray, constellation: np.ndarray) -> np.ndarray:
        """Maximum Likelihood 검출 (복잡하지만 최적)"""
        n_tx = H.shape[1]
        n_sym = len(constellation)

        # 모든 가능한 조합 검사 (지수적 복잡도)
        min_dist = float('inf')
        best_x = None

        # 간소화: 각 심볼을 독립적으로 검출
        x_hat = np.zeros(n_tx, dtype=complex)
        for i in range(n_tx):
            h_col = H[:, i]
            y_rem = y - H[:, :i] @ x_hat[:i] - H[:, i+1:] @ x_hat[i+1:] if i < n_tx - 1 else y - H[:, :i] @ x_hat[:i]

            min_d = float('inf')
            best_sym = constellation[0]
            for sym in constellation:
                d = np.linalg.norm(y_rem - h_col * sym)
                if d < min_d:
                    min_d = d
                    best_sym = sym
            x_hat[i] = best_sym

        return x_hat

class MIMOSimulator:
    """MIMO 시스템 시뮬레이터"""

    def __init__(self, config: MIMOConfig):
        self.config = config
        self.channel = MIMOChannel(config.n_tx, config.n_rx)
        self.precoder = MIMOPrecoder()
        self.detector = MIMODetector()

        # 성상도 생성
        if config.modulation == "BPSK":
            self.constellation = np.array([-1, 1])
        elif config.modulation == "QPSK":
            self.constellation = np.array([1+1j, -1+1j, -1-1j, 1-1j]) / np.sqrt(2)
        elif config.modulation == "16QAM":
            points = []
            for i in [-3, -1, 1, 3]:
                for q in [-3, -1, 1, 3]:
                    points.append(complex(i, q))
            self.constellation = np.array(points) / np.sqrt(10)

    def generate_bits(self, n_bits: int) -> np.ndarray:
        """랜덤 비트 생성"""
        return np.random.randint(0, 2, n_bits)

    def bits_to_symbols(self, bits: np.ndarray) -> np.ndarray:
        """비트를 심볼로 변환"""
        bits_per_sym = int(np.log2(len(self.constellation)))
        n_syms = len(bits) // bits_per_sym
        symbols = np.zeros(n_syms, dtype=complex)

        for i in range(n_syms):
            idx = 0
            for j in range(bits_per_sym):
                idx = (idx << 1) | bits[i * bits_per_sym + j]
            symbols[i] = self.constellation[idx]

        return symbols

    def symbols_to_bits(self, symbols: np.ndarray) -> np.ndarray:
        """심볼을 비트로 변환"""
        bits_per_sym = int(np.log2(len(self.constellation)))
        bits = []

        for sym in symbols:
            # 최근접 심볼 찾기
            distances = np.abs(self.constellation - sym)
            idx = np.argmin(distances)

            # 비트로 변환
            for j in range(bits_per_sym - 1, -1, -1):
                bits.append((idx >> j) & 1)

        return np.array(bits)

    def simulate_spatial_multiplexing(self, n_blocks: int = 1000) -> dict:
        """공간 다중화 시뮬레이션"""
        n_streams = self.config.n_streams
        bits_per_sym = int(np.log2(len(self.constellation)))

        total_bits = 0
        error_bits = 0

        for _ in range(n_blocks):
            # 비트 생성
            n_bits = n_streams * bits_per_sym
            bits = self.generate_bits(n_bits)

            # 심볼 매핑
            symbols = self.bits_to_symbols(bits)
            x = symbols.reshape(n_streams, 1)

            # 채널 생성
            H = self.channel.generate()

            # Precoding (SVD)
            V, U_rx, S = self.precoder.svd_precoding(H, n_streams)
            x_precoded = V @ x

            # 전송 (채널 통과)
            snr_linear = 10 ** (self.config.snr_db / 10)
            noise_var = 1 / snr_linear
            noise = np.sqrt(noise_var / 2) * (
                np.random.randn(self.config.n_rx, 1) +
                1j * np.random.randn(self.config.n_rx, 1)
            )

            y = H @ x_precoded + noise

            # 수신 처리 (SVD combiner)
            y_combined = U_rx.conj().T @ y

            # 검출
            noise_var_eff = noise_var  # 간소화
            x_hat = np.zeros(n_streams, dtype=complex)
            for i in range(n_streams):
                # 단순 threshold 검출
                y_i = y_combined[i, 0] / S[i] if S[i] > 0 else y_combined[i, 0]
                dist = np.abs(self.constellation - y_i)
                x_hat[i] = self.constellation[np.argmin(dist)]

            # 비트 복원
            bits_hat = self.symbols_to_bits(x_hat)

            # 에러 카운트
            total_bits += len(bits)
            error_bits += np.sum(bits != bits_hat)

        ber = error_bits / total_bits if total_bits > 0 else 0

        # 용량 계산
        H_avg = self.channel.generate()
        capacity = self.calculate_capacity(H_avg, snr_linear)

        return {
            'ber': ber,
            'total_bits': total_bits,
            'error_bits': error_bits,
            'capacity_bps_hz': capacity,
            'multiplexing_gain': np.sum(S > 0.1)  # 유효 모드 수
        }

    def calculate_capacity(self, H: np.ndarray, snr: float) -> float:
        """MIMO 채널 용량 계산"""
        n_tx = H.shape[1]
        I = np.eye(self.config.n_rx)
        capacity = np.log2(np.linalg.det(I + (snr / n_tx) * H @ H.conj().T))
        return np.real(capacity)

def run_mimo_simulation():
    """MIMO 시뮬레이션 실행"""
    print("=" * 70)
    print("MIMO 공간 분할 다중화 시뮬레이션")
    print("=" * 70)

    for n_ant in [2, 4, 8]:
        config = MIMOConfig(n_tx=n_ant, n_rx=n_ant, n_streams=n_ant)
        simulator = MIMOSimulator(config)

        print(f"\n--- {n_ant}×{n_ant} MIMO ---")

        for snr_db in [10, 15, 20, 25]:
            config.snr_db = snr_db
            simulator.config = config
            result = simulator.simulate_spatial_multiplexing(n_blocks=100)

            print(f"SNR={snr_db}dB: BER={result['ber']:.6f}, "
                  f"용량={result['capacity_bps_hz']:.2f} bps/Hz, "
                  f"다중화이득={result['multiplexing_gain']}")

if __name__ == "__main__":
    run_mimo_simulation()
