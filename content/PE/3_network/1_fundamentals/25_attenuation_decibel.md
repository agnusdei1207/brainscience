+++
title = "025. 감쇠 (Attenuation) 및 데시벨(dB) 측정"
description = "신호 감쇠의 원리, 데시벨(dB) 스케일, 감쇠 계수, 주파수 의존성, 측정 방법을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["Attenuation", "Decibel", "dB", "PathLoss", "SignalLoss", "FiberOptic", "CoaxialCable"]
categories = ["studynotes-3_network"]
+++

# 025. 감쇠 (Attenuation) 및 데시벨(dB) 측정

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 감쇠(Attenuation)는 신호가 전송 매체를 통과하면서 에너지를 잃어 약해지는 현상으로, 거리, 주파수, 매체 특성에 따라 지수함수적으로 감소합니다.
> 2. **가치**: 데시벨(dB)은 매우 넓은 범위의 전력/전압 비를 관리 가능한 수치로 표현하며, 통신 시스템 설계에서 링크 예산 계산의 핵심 단위입니다.
> 3. **융합**: 광섬유(0.2 dB/km), 동축케이블(수 dB/100m), 무선(자유공간 20log₁₀d) 등 매체별 감쇠 특성을 이해해야 최적의 전송 설계가 가능합니다.

---

## I. 개요 (Context & Background)

감쇠(Attenuation)는 전자기파, 음파, 광 신호 등이 매체를 통과하면서 **에너지가 손실되어 진폭이 감소하는 현상**입니다. 통신 시스템에서 감쇠는 송신 전력과 수신 전력의 차이로 정의되며, 일반적으로 데시벨(dB) 단위로 측정됩니다.

**감쇠의 정의**:
```
감쇠 (dB) = 10 × log₁₀(P_입력 / P_출력)
         = P_입력_dBm - P_출력_dBm

감쇠 계수 (α): 단위 길이당 감쇠 (dB/km, dB/m, dB/100m)
```

**비유**: 감쇠는 **"수도관을 흐르는 물의 압력 감소"**와 같습니다.
- **긴 관**: 물이 멀리 갈수록 마찰로 인해 압력이 떨어집니다 (거리 감쇠).
- **좁은 관**: 관이 좁을수록 마찰이 커서 압력 손실이 큽니다 (주파수 의존성).
- **거친 내벽**: 관 내벽이 거칠수록 저항이 커집니다 (매체 품질).

**등장 배경 및 발전 과정**:
1. **전신 시대 (1840년대)**: 해저 케이블에서 신호가 약해지는 현상이 처음 체계적으로 관찰되었습니다.
2. **벨 연구소 (1920년대)**: 전화망 확장과 함께 감쇠 측정의 표준화가 필요해져 'bel'과 'decibel' 단위가 정립되었습니다.
3. **광통신 혁명 (1970년대~)**: 저손실 광섬유(0.2 dB/km) 개발로 장거리 대용량 전송이 가능해졌습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 데시벨(dB) 체계 상세 분석

| 개념 | 정의 | 공식 | 기준 |
|------|------|------|------|
| **Bel** | 전력비의 상용로그 | log₁₀(P₁/P₀) | Alexander Graham Bell |
| **Decibel (dB)** | Bel의 1/10 | 10×log₁₀(P₁/P₀) | 표준 로그 단위 |
| **dBm** | 1 mW 기준 전력 | 10×log₁₀(P/1mW) | 절대 전력 |
| **dBW** | 1 W 기준 전력 | 10×log₁₀(P/1W) | 고전력 |
| **dBμV** | 1 μV 기준 전압 | 20×log₁₀(V/1μV) | RF 측정 |

**전력 vs 전압 dB 변환**:
```
전력비 (dB) = 10 × log₁₀(P₁/P₀)

전압비 (dB) = 20 × log₁₀(V₁/V₀)
            = 20 × log₁₀(V₁/V₀)
            = 10 × log₁₀((V₁/V₀)²)
            = 10 × log₁₀(P₁/P₀)  [같은 임피던스에서]
```

**dB 계산 예시**:
```
전력 2배 증가    = +3.01 dB ≈ +3 dB
전력 10배 증가   = +10 dB
전력 100배 증가  = +20 dB
전력 1000배 증가 = +30 dB
전력 반감       = -3 dB
전력 1/10       = -10 dB

1 mW = 0 dBm
10 mW = +10 dBm
100 mW = +20 dBm
1 W = +30 dBm = 0 dBW
100 W = +50 dBm = +20 dBW
```

### 매체별 감쇠 특성

| 매체 | 감쇠 계수 | 주파수 의존성 | 특징 |
|------|----------|--------------|------|
| **광섬유 (SMF)** | 0.2~0.5 dB/km | 1310/1550nm 최적 | 초저손실, 장거리 |
| **광섬유 (MMF)** | 1~3 dB/km | 모드 분산 추가 | 단거리 LAN |
| **UTP Cat6** | ~20 dB/100m @ 250MHz | 주파수 증가시 급증 | 기가비트 이더넷 |
| **동축 RG-6** | ~6 dB/100m @ 100MHz | √f 비례 | 케이블 TV |
| **자유 공간** | FSPL = 20log₁₀d + 20log₁₀f + 32.44 | f², d² 비례 | 무선 전파 |
| **해수** | ~100 dB/m @ 2.4GHz | 매우 높음 | 수중 통신 불가 |

### 정교한 구조 다이어그램: 감쇠 메커니즘

```ascii
================================================================================
[ Signal Attenuation Mechanisms ]
================================================================================

입력 신호                          매체                           출력 신호
  ___                                                            ___
 |   |                                                          |   |
 | P | ==================>  ==============================>  | P |
 | in|                    |                               |   |out|
 |___|                    |      감쇠 요인들               |   |___|
                          |                               |
                          |  ┌─────────────────────────┐  |
                          |  │ 1. 도전 손실 (Conduction)│  |
                          |  │    - 저항에 의한 열 손실 │  |
                          |  │    - 표면 효과 (Skin)   │  |
                          |  └─────────────────────────┘  |
                          |                               |
                          |  ┌─────────────────────────┐  |
                          |  │ 2. 유전체 손실 (Dielectric)│ |
                          |  │    - 분자 마찰          │  |
                          |  │    - 주파수 비례 증가    │  |
                          |  └─────────────────────────┘  |
                          |                               |
                          |  ┌─────────────────────────┐  |
                          |  │ 3. 방사 손실 (Radiation) │  |
                          |  │    - 전자기파 누설       │  |
                          |  │    - 굽힘/불연속점      │  |
                          |  └─────────────────────────┘  |
                          |                               |
                          |  ┌─────────────────────────┐  |
                          |  │ 4. 산란 (Scattering)    │  |
                          |  │    - 불순물, 불균질     │  |
                          |  │    - 광섬유 레일리 산란 │  |
                          |  └─────────────────────────┘  |
                          |                               |
                          └───────────────────────────────┘

감쇠 (Attenuation) = P_in - P_out (dB)
                    = 10 × log₁₀(P_in / P_out)

================================================================================
[ Frequency-Dependent Attenuation ]
================================================================================

감쇠 (dB/km)
    ^
 40 |                                     *
    |                                   *
 30 |                                 *
    |                               *
 20 |                             *      <-- UTP Cat5e
    |                           *
 10 |                       *  *
    |                     *
  5 |           * * *                    <-- 광섬유 (1550nm)
    |         *
  0.2|_* * * *                          <-- 광섬유 최적점
    +----|----|----|----|----|----|----|----|--> 주파수
         1M  10M  100M 1G   10G  100G
              Hz   Hz   Hz   Hz   Hz

    광섬유: 1310nm, 1550nm에 저손실 윈도우
    UTP: 주파수 높을수록 감쇠 급증
    동축: √f에 비례하여 완만한 증가

================================================================================
[ Free Space Path Loss (FSPL) ]
================================================================================

    FSPL (dB) = 20×log₁₀(d) + 20×log₁₀(f) + 32.44
              = 20×log₁₀(d_km) + 20×log₁₀(f_MHz) + 32.44

    또는:

    FSPL (dB) = 20×log₁₀(d) + 20×log₁₀(f) + 92.45
              (d: km, f: GHz)

FSPL (dB)
    ^
 150|                                       *
    |                                    *
 140|                                 *
    |                              *
 130|                           *
    |                        *
 120|                     *
    |                  *
 110|               *                  2.4 GHz
    |            *        * * *
 100|         *      * *       *
    |       *    * *              *
  90|     *  * *                    *      900 MHz
    |   * *                            *
  80| *                                  *
    +----|----|----|----|----|----|----|----|--> 거리 (km)
         0.1  0.5  1    2    5   10   20   50

    주파수 2배 → FSPL 6 dB 증가
    거리 2배 → FSPL 6 dB 증가

================================================================================
```

### 심층 동작 원리: 광섬유 감쇠

**광섬유 감쇠의 주요 요인**:

1. **레일리 산란 (Rayleigh Scattering)**:
   ```
   α_rayleigh ∝ 1/λ⁴
   단파장에서 지배적
   1550nm에서 약 0.15 dB/km
   ```

2. **적외선 흡수 (Infrared Absorption)**:
   ```
   SiO₂ 분자 진동에 의한 흡수
   장파장에서 지배적
   1600nm 이상에서 급격히 증가
   ```

3. **OH⁻ 이온 흡수 (Water Peak)**:
   ```
   1383nm 부근에서 피크
   저가 광섬유에서 두드러짐
   고급 광섬유는 OH⁻ 제거로 평탄화
   ```

**광섬유 저손실 윈도우**:
```
       감쇠
        ^
  2.0   |                    OH⁻ Peak
        |                      /\
  1.5   |                     /  \
        |        1310nm      /    \    1550nm
  1.0   |         |    _____/      \___/____
        |         |   /                  \
  0.5   |    _____|__/                    \
        |   /     |                        \
  0.2   |--|------|------------------------|--> 파장 (nm)
            850   1310      1383          1550
            1번   2번       3번            4번
            윈도우 윈도우    윈도우         윈도우

    2번 윈도우 (1310nm): 분산 0, 감쇠 ~0.35 dB/km
    4번 윈도우 (1550nm): 감쇠 최저 ~0.2 dB/km, EDFA 증폭 가능
```

### 핵심 코드: 감쇠 계산 및 링크 분석 (Python)

```python
import numpy as np
from dataclasses import dataclass
from typing import Tuple, List
from enum import Enum

class MediaType(Enum):
    """전송 매체 타입"""
    FIBER_SMF = "Single Mode Fiber"
    FIBER_MMF = "Multi Mode Fiber"
    UTP_CAT5E = "UTP Cat5e"
    UTP_CAT6 = "UTP Cat6"
    COAX_RG6 = "Coaxial RG-6"
    FREE_SPACE = "Free Space"

@dataclass
class AttenuationParams:
    """감쇠 계산 파라미터"""
    frequency_hz: float = 2.4e9       # 주파수 (Hz)
    distance_m: float = 1000.0        # 거리 (m)
    tx_power_dbm: float = 20.0        # 송신 전력 (dBm)


class AttenuationCalculator:
    """
    다양한 매체에서의 감쇠 계산 클래스
    """

    # 매체별 감쇠 계수 (기본값, 실제는 주파수 의존)
    ATTENUATION_COEFFICIENTS = {
        MediaType.FIBER_SMF: 0.20,     # dB/km @ 1550nm
        MediaType.FIBER_MMF: 1.0,      # dB/km @ 850nm
        MediaType.UTP_CAT5E: 0.22,     # dB/m @ 100MHz (근사)
        MediaType.UTP_CAT6: 0.18,      # dB/m @ 250MHz (근사)
        MediaType.COAX_RG6: 0.06,      # dB/m @ 100MHz
    }

    @staticmethod
    def power_ratio_to_db(ratio: float) -> float:
        """전력비를 dB로 변환"""
        if ratio <= 0:
            raise ValueError("비율은 양수여야 함")
        return 10 * np.log10(ratio)

    @staticmethod
    def db_to_power_ratio(db: float) -> float:
        """dB를 전력비로 변환"""
        return 10 ** (db / 10)

    @staticmethod
    def voltage_ratio_to_db(ratio: float) -> float:
        """전압비를 dB로 변환"""
        if ratio <= 0:
            raise ValueError("비율은 양수여야 함")
        return 20 * np.log10(ratio)

    @staticmethod
    def dbm_to_watt(dbm: float) -> float:
        """dBm을 Watt로 변환"""
        return 10 ** ((dbm - 30) / 10)

    @staticmethod
    def watt_to_dbm(watt: float) -> float:
        """Watt를 dBm으로 변환"""
        if watt <= 0:
            raise ValueError("전력은 양수여야 함")
        return 10 * np.log10(watt * 1000)

    def calculate_fiber_attenuation(
        self,
        distance_km: float,
        wavelength_nm: float = 1550,
        fiber_type: MediaType = MediaType.FIBER_SMF
    ) -> float:
        """
        광섬유 감쇠 계산

        Args:
            distance_km: 거리 (km)
            wavelength_nm: 파장 (nm)
            fiber_type: 광섬유 타입

        Returns:
            감쇠 (dB)
        """
        # ITU-T G.652 광섬유 모델 (근사)
        if fiber_type == MediaType.FIBER_SMF:
            # 레일리 산란 + UV 흡수 + IR 흡수 + OH 흡수
            lambda_um = wavelength_nm / 1000

            # 레일리 산란 항
            alpha_rayleigh = 0.8 * (1.0 / lambda_um) ** 4

            # 적외선 흡수 항
            alpha_ir = 0.1 * np.exp(4.5 / lambda_um)

            # OH 흡수 항 (1383nm 피크)
            oh_peak = 1383
            alpha_oh = 0.5 * np.exp(-((wavelength_nm - oh_peak) ** 2) / (2 * 20 ** 2))

            total_attenuation_db_km = alpha_rayleigh + alpha_ir + alpha_oh

        else:  # MMF
            total_attenuation_db_km = self.ATTENUATION_COEFFICIENTS[fiber_type]

        return total_attenuation_db_km * distance_km

    def calculate_utp_attenuation(
        self,
        distance_m: float,
        frequency_hz: float,
        category: int = 6
    ) -> float:
        """
        UTP 케이블 감쇠 계산

        Args:
            distance_m: 거리 (m)
            frequency_hz: 주파수 (Hz)
            category: 카테고리 (5, 5e, 6, 6a, 7)

        Returns:
            감쇠 (dB)
        """
        # 주파수 의존 감쇠 모델 (IEEE 802.3 기반 근사)
        # IL = k1 * sqrt(f) + k2 * f + k3 / sqrt(f)

        f_mhz = frequency_hz / 1e6

        if category == 5:
            # Cat 5: 100MHz까지
            k1, k2, k3 = 1.967, 0.023, 0.05
        elif category == 6:
            # Cat 6: 250MHz까지
            k1, k2, k3 = 1.808, 0.017, 0.02
        elif category >= 7:
            # Cat 6a/7: 600MHz까지
            k1, k2, k3 = 1.5, 0.01, 0.01
        else:  # 5e
            k1, k2, k3 = 1.92, 0.022, 0.04

        # 100m당 삽입 손실
        il_100m = k1 * np.sqrt(f_mhz) + k2 * f_mhz + k3 / np.sqrt(f_mhz)

        # 거리 비례
        attenuation_db = il_100m * (distance_m / 100)

        return attenuation_db

    def calculate_coax_attenuation(
        self,
        distance_m: float,
        frequency_hz: float,
        cable_type: str = "RG6"
    ) -> float:
        """
        동축 케이블 감쇠 계산

        Args:
            distance_m: 거리 (m)
            frequency_hz: 주파수 (Hz)
            cable_type: 케이블 타입 (RG6, RG11, RG59)

        Returns:
            감쇠 (dB)
        """
        f_mhz = frequency_hz / 1e6

        # 케이블별 감쇠 계수 (100m당 @ 100MHz 기준)
        # 실제는 sqrt(f)에 비례
        coax_params = {
            "RG6": (0.6, 5.65),    # (α_100MHz, k_sqrt_f)
            "RG11": (0.4, 4.0),
            "RG59": (1.2, 9.0),
        }

        if cable_type not in coax_params:
            cable_type = "RG6"

        _, k = coax_params[cable_type]

        # 감쇠 = k * sqrt(f_MHz) dB/100m
        attenuation_100m = k * np.sqrt(f_mhz)

        return attenuation_100m * (distance_m / 100)

    def calculate_free_space_path_loss(
        self,
        distance_m: float,
        frequency_hz: float
    ) -> float:
        """
        자유 공간 경로 손실 (FSPL)

        Args:
            distance_m: 거리 (m)
            frequency_hz: 주파수 (Hz)

        Returns:
            FSPL (dB)
        """
        c = 3e8  # 빛의 속도 (m/s)
        wavelength = c / frequency_hz

        # FSPL = (4πd/λ)²
        fspl_linear = (4 * np.pi * distance_m / wavelength) ** 2
        fspl_db = 10 * np.log10(fspl_linear)

        return fspl_db

    def calculate_total_link_loss(
        self,
        params: AttenuationParams,
        media_type: MediaType,
        connector_loss_db: float = 0.5,
        num_connectors: int = 4
    ) -> Tuple[float, float]:
        """
        전체 링크 손실 계산

        Args:
            params: 링크 파라미터
            media_type: 매체 타입
            connector_loss_db: 커넥터 1개당 손실
            num_connectors: 커넥터 수

        Returns:
            (매체 감쇠, 총 손실)
        """
        distance_km = params.distance_m / 1000

        if media_type in [MediaType.FIBER_SMF, MediaType.FIBER_MMF]:
            media_loss = self.calculate_fiber_attenuation(
                distance_km, 1550, media_type
            )
        elif media_type in [MediaType.UTP_CAT5E, MediaType.UTP_CAT6]:
            cat = 6 if media_type == MediaType.UTP_CAT6 else 5
            media_loss = self.calculate_utp_attenuation(
                params.distance_m, params.frequency_hz, cat
            )
        elif media_type == MediaType.COAX_RG6:
            media_loss = self.calculate_coax_attenuation(
                params.distance_m, params.frequency_hz, "RG6"
            )
        else:  # Free Space
            media_loss = self.calculate_free_space_path_loss(
                params.distance_m, params.frequency_hz
            )

        # 커넥터 손실 추가
        connector_loss = connector_loss_db * num_connectors
        total_loss = media_loss + connector_loss

        return media_loss, total_loss

    def calculate_rx_power(
        self,
        tx_power_dbm: float,
        total_loss_db: float
    ) -> float:
        """
        수신 전력 계산

        Args:
            tx_power_dbm: 송신 전력 (dBm)
            total_loss_db: 총 손실 (dB)

        Returns:
            수신 전력 (dBm)
        """
        return tx_power_dbm - total_loss_db

    def calculate_max_distance(
        self,
        tx_power_dbm: float,
        rx_sensitivity_dbm: float,
        attenuation_coeff_db_km: float,
        margin_db: float = 6.0
    ) -> float:
        """
        최대 통신 거리 계산

        Args:
            tx_power_dbm: 송신 전력 (dBm)
            rx_sensitivity_dbm: 수신 감도 (dBm)
            attenuation_coeff_db_km: 감쇠 계수 (dB/km)
            margin_db: 링크 마진 (dB)

        Returns:
            최대 거리 (km)
        """
        available_budget = tx_power_dbm - rx_sensitivity_dbm - margin_db
        max_distance = available_budget / attenuation_coeff_db_km
        return max_distance


class DecibelConverter:
    """
    다양한 dB 변환 유틸리티
    """

    @staticmethod
    def add_db(*args: float) -> float:
        """
        dB 값들의 합 (전력 덧셈)
        dB + dB = 10×log₁₀(10^(dB₁/10) + 10^(dB₂/10) + ...)
        """
        linear_sum = sum(10 ** (db / 10) for db in args)
        return 10 * np.log10(linear_sum)

    @staticmethod
    def subtract_db(db1: float, db2: float) -> float:
        """
        dB 값들의 차 (전력 뺄셈)
        """
        linear_diff = 10 ** (db1 / 10) - 10 ** (db2 / 10)
        if linear_diff <= 0:
            return float('-inf')
        return 10 * np.log10(linear_diff)

    @staticmethod
    def cascade_system(*gains_db: float) -> float:
        """
        직렬 연결 시스템의 총 이득/손실
        단순히 dB 값을 더함
        """
        return sum(gains_db)

    @staticmethod
    def power_to_voltage_db(dbm: float, impedance: float = 50.0) -> Tuple[float, float]:
        """
        dBm을 dBμV로 변환

        Returns:
            (dBμV, 전압 V)
        """
        power_w = 10 ** ((dbm - 30) / 10)
        voltage_v = np.sqrt(power_w * impedance)
        dbuv = 20 * np.log10(voltage_v * 1e6)
        return dbuv, voltage_v


# 사용 예시
if __name__ == "__main__":
    calc = AttenuationCalculator()
    converter = DecibelConverter()

    print("=" * 60)
    print("감쇠 및 dB 계산 예시")
    print("=" * 60)

    # 1. 광섬유 감쇠
    fiber_loss = calc.calculate_fiber_attenuation(80, 1550, MediaType.FIBER_SMF)
    print(f"\n광섬유 80km @ 1550nm 감쇠: {fiber_loss:.2f} dB")

    # 2. UTP 감쇠
    utp_loss = calc.calculate_utp_attenuation(100, 100e6, 6)
    print(f"UTP Cat6 100m @ 100MHz 감쇠: {utp_loss:.2f} dB")

    # 3. FSPL
    fspl = calc.calculate_free_space_path_loss(1000, 2.4e9)
    print(f"자유공간 1km @ 2.4GHz FSPL: {fspl:.2f} dB")

    # 4. dB 변환
    print(f"\n전력 100mW = {converter.watt_to_dbm(0.1):.1f} dBm")
    print(f"20 dBm = {calc.dbm_to_watt(20):.3f} W")

    # 5. 전압 변환
    dbuv, voltage = converter.power_to_voltage_db(0, 50)
    print(f"\n0 dBm @ 50Ω = {dbuv:.1f} dBμV = {voltage*1000:.3f} mV")

    # 6. 직렬 시스템
    total = converter.cascade_system(20, -3, -50, 30)  # Tx + cable + path + Rx gain
    print(f"\n직렬 시스템 (20-3-50+30) dB: {total:.1f} dB")

    # 7. 최대 거리
    max_dist = calc.calculate_max_distance(
        tx_power_dbm=0,      # 1 mW
        rx_sensitivity_dbm=-25,
        attenuation_coeff_db_km=0.2,  # SMF
        margin_db=3
    )
    print(f"\n광섬유 최대 거리 (0 dBm Tx, -25 dBm Rx): {max_dist:.1f} km")

    print("\n=== 감쇠 계산 완료 ===")
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 매체별 감쇠 비교 (100m 기준)

| 매체 | 1 MHz | 10 MHz | 100 MHz | 1 GHz | 특징 |
|------|-------|--------|---------|-------|------|
| **UTP Cat6** | 1.8 dB | 5.7 dB | 18 dB | 57 dB | 주파수 √비례 |
| **동축 RG-6** | 0.6 dB | 1.9 dB | 6 dB | 19 dB | √f 완만 |
| **광섬유 SMF** | 0.02 dB | 0.02 dB | 0.02 dB | 0.02 dB | 주파수 무관 |

### dB 단위 체계 비교

| 단위 | 기준 | 양/음 | 용도 |
|------|------|-------|------|
| **dB** | 상대값 | 양=이득, 음=손실 | 시스템 이득/손실 |
| **dBm** | 1 mW | 주로 양 | RF 전력 |
| **dBW** | 1 W | 음~양 | 고전력 |
| **dBi** | 등방성 | 양 | 안테나 이득 |
| **dBd** | 반파장 다이폴 | 양 | 안테나 이득 |
| **dBc** | 반송파 | 음 | 스퓨리어스 |

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: FTTH 광 접속망 설계

**문제 상황**: OLT(광라인터미널)에서 가입자 ONT까지 20km PON 망을 설계합니다. 1490nm 하향 신호로 1 Gbps 전송이 필요합니다.

**기술사의 전략적 의사결정**:

1. **광섬유 감쇠 계산**:
   ```
   1490nm 감쇠: ~0.25 dB/km
   20km 감쇠: 0.25 × 20 = 5 dB
   ```

2. **기타 손실**:
   ```
   커넥터 (SC/APC): 0.3 dB × 4 = 1.2 dB
   스플라이스: 0.1 dB × 6 = 0.6 dB
   분배기 (1:32): 17 dB
   총 손실: 5 + 1.2 + 0.6 + 17 = 23.8 dB
   ```

3. **전력 예산 확인**:
   ```
   OLT 출력: +3 dBm
   ONT 감도: -28 dBm
   가용 예산: 31 dB
   여유: 31 - 23.8 = 7.2 dB > 3 dB (만족)
   ```

---

## V. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 매체 | 100m당 감쇠 | 1km 전력 전달률 | 적용 |
|------|------------|----------------|------|
| **광섬유** | 0.02 dB | 95.5% | 장거리 백본 |
| **동축** | 6 dB | 25% | 케이블 TV |
| **UTP** | 18 dB | 1.6% | LAN (100m 제한) |

### 참고 표준/가이드

| 표준 | 기관 | 내용 |
|------|------|------|
| **ITU-T G.652** | ITU-T | SMF 광섬유 규격 |
| **TIA-568** | TIA | UTP 케이블 규격 |
| **IEEE 802.3** | IEEE | 이더넷 물리 계층 |
| **IEC 61753** | IEC | 광부품 성능 표준 |

---

## 관련 개념 맵 (Knowledge Graph)
- [SNR 신호 대 잡음비](./24_snr_signal_to_noise_ratio.md) - 감쇠의 영향
- [전파 지연](./16_propagation_delay.md) - 거리와 전파 속도
- [광섬유 케이블](../3_network/osi_7_layer.md) - 물리 계층 매체
- [자유 공간 경로 손실](./15_latency_delay.md) - 무선 감쇠
- [이더넷 물리 계층](./multiplexing_techniques.md) - 케이블 표준

---

## 어린이를 위한 3줄 비유 설명
1. **감쇠**는 **멀리 떨어진 친구에게 말할 때 목소리가 작아지는 것**과 같아요. 멀수록 더 작게 들려요.
2. **dB**는 **목소리 크기를 점수로 매기는 것**이에요. 10점 더 크면 10배 더 큰 소리예요!
3. **광섬유**는 **초특급 울타리 터널**이라서 아주 멀리까지 빛이 거의 안 줄어요!
