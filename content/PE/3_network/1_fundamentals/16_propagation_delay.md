+++
title = "016. 전파 지연 (Propagation Delay) - 거리/속도"
description = "전파 지연의 물리적 원리, 계산 방법, 거리와 매체에 따른 차이, 실무적 영향 및 최적화 기법을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["PropagationDelay", "SpeedOfLight", "FiberOptic", "Satellite", "NetworkLatency", "Distance"]
categories = ["studynotes-3_network"]
+++

# 016. 전파 지연 (Propagation Delay) - 거리/속도

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 전파 지연은 신호가 물리적 매체를 통해 이동하는 데 걸리는 시간으로, 거리(d)를 전파 속도(v)로 나눈 값(d/v)이며, 광섬유에서는 약 200,000 km/s, 무선에서는 약 300,000 km/s의 속도로 전파됩니다.
> 2. **가치**: 전파 지연은 물리 법칙에 의해 결정되는 최소 지연으로, 지구 반대편 통신에서도 약 100ms의 왕복 지연이 불가피하며, 이는 CDN, 엣지 컴퓨팅, 위성 통신 설계의 핵심 제약 조건입니다.
> 3. **융합**: 저궤도 위성(LEO) 인터넷, 해저 광케이블 최단 경로 라우팅, 프리픽싱(Prefetching) 등이 전파 지연의 물리적 한계를 극복하기 위한 전략으로 활용됩니다.

---

## I. 개요 (Context & Background)

**전파 지연(Propagation Delay)**은 신호가 송신 지점에서 수신 지점까지 물리적 매체를 통해 이동하는 데 걸리는 시간입니다. 이는 **물리 법칙에 의해 결정되는 불가항적 지연**으로, 거리를 줄이거나 전파 속도를 높이는 방법 외에는 최소화할 수 없습니다.

### 전파 지연 공식

```
전파 지연 (d_prop) = 거리 (d) / 전파 속도 (v)
```

### 다양한 매체에서의 전파 속도

| 매체 | 전파 속도 | 상대 속도 | 굴절률 |
|------|----------|----------|--------|
| **진공** | 299,792 km/s (c) | 100% | 1.0 |
| **공기 (무선)** | ~299,700 km/s | ~99.97% | ~1.0003 |
| **광섬유** | ~200,000 km/s | ~67% | ~1.5 |
| **동축 케이블** | ~200,000 km/s | ~67% | ~1.5 |
| **UTP 케이블** | ~190,000 km/s | ~63% | ~1.6 |

### 광섬유에서 속도가 느린 이유

빛이 광섬유의 코어(Core)와 클래딩(Cladding) 경계에서 **전반사(Total Internal Reflection)**를 반복하며 지그재그 경로로 이동하기 때문입니다. 또한 **굴절률(Refractive Index)**이 진공보다 높아 빛의 속도가 감소합니다.

```
매체 내 빛의 속도 = c / n
여기서 n = 굴절률

광섬유 (n ≈ 1.5): 299,792 / 1.5 ≈ 200,000 km/s
```

**💡 비유**: 전파 지연을 **'비행기 여행 시간'**에 비유할 수 있습니다.

- **거리**: 서울에서 뉴욕까지 비행 거리는 약 11,000km입니다. 이는 비행기의 성능과 상관없이 정해진 거리입니다.
- **속도**: 여객기는 시속 약 900km로 비행합니다. 서울-뉴욕 비행 시간은 11,000 / 900 ≈ 12시간입니다.
- **전파 지연**: 광섬유에서 서울-뉴욕 신호 전파 시간은 11,000 / 200,000 = 0.055초 = 55ms입니다.

비행기가 아무리 좋아도 거리가 줄어들지 않는 것처럼, 네트워크 장비가 아무리 좋아도 전파 지연은 줄어들지 않습니다. **"물리학의 벽"**입니다.

**등장 배경 및 발전 과정**:

1. **전신 시대의 인식**: 19세기 전신에서 송신과 수신 사이의 시간차가 인식되었습니다. 대륙 횡단 전신은 수 초의 지연이 있었습니다.

2. **광통신의 도래**: 1970년대 광섬유 통신이 상용화되면서 전파 지연이 크게 단축되었습니다. 동축 케이블이나 마이크로파 중계보다 직선 경로가 가능해졌습니다.

3. **위성 통신의 도전**: 정지 궤도 위성(GEO)은 35,786km 고도로 인해 왕복 240ms의 전파 지연이 발생합니다. 이는 실시간 통신에 큰 장애가 되었습니다.

4. **저궤도 위성(LEO)의 해결**: 스타링크, 원웹 등의 LEO 위성은 550~1,200km 고도에서 운영되어 왕복 지연을 20~40ms로 단축합니다.

5. **엣지 컴퓨팅의 부상**: 물리적 거리를 줄이기 위해 서버를 사용자 근처에 배치하는 전략이 보편화되었습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성요소 | 명칭 | 값 | 단위 | 설명 | 비고 |
|---------|------|-----|------|------|------|
| **c** | 빛의 속도 (진공) | 299,792,458 | m/s | 물리 상수 | 정확히 정의됨 |
| **v_fiber** | 광섬유 속도 | ~200,000 | km/s | c / 1.5 | 굴절률 고려 |
| **v_wireless** | 무선 속도 | ~300,000 | km/s | ≈ c | 공기 중 |
| **n** | 굴절률 | 1.0~1.6 | 무차원 | 매체별 상수 | v = c/n |
| **d** | 거리 | 가변 | km | 물리적 거리 | 경로 의존 |
| **d_prop** | 전파 지연 | d/v | ms | 계산 값 | 물리적 한계 |

### 정교한 구조 다이어그램: 전파 경로와 지연

```ascii
================================================================================
[ 지구 규모 전파 지연 시나리오 ]
================================================================================

                         북극
                           |
                 ┌─────────┴─────────┐
                 │                   │
                 │    대서양         │
           뉴욕 ─┤                   ├─ 런던
           (NY)  │   ~5,500km        │   (LDN)
                 │                   │
                 │                   │
                 │                   │
                 │    태평양         │
                 │                   │
           서울 ─┤                   ├─ LA
           (SEL) │  ~11,000km        │ (LAX)
                 │                   │
                 └─────────┬─────────┘
                           |
                         남극


================================================================================
[ 주요 도시 간 전파 지연 (광섬유, 단방향) ]
================================================================================

구간                거리(km)    광섬유 지연(ms)    RTT(ms)
─────────────────────────────────────────────────────────
서울-도쿄             1,200         6.0            12
서울-베이징           1,000         5.0            10
서울-상하이           1,400         7.0            14
서울-싱가포르         4,700        23.5            47
서울-런던             8,900        44.5            89
서울-뉴욕            11,000        55.0           110
서울-샌프란시스코      9,100        45.5            91
서울-시드니           8,300        41.5            83

참고: 실제 해저 케이블 경로는 육상 경로보다 길어질 수 있음
      실제 RTT는 처리 지연, 큐잉 지연 추가로 더 김


================================================================================
[ 위성 통신 전파 지연 비교 ]
================================================================================

┌──────────────────────────────────────────────────────────────────────────┐
│                          정지 궤도 위성 (GEO)                             │
│                                                                          │
│   지구국 A ───────────────────────────────────────────────> 지구국 B     │
│            \                                              /              │
│             \          ┌─────────────┐                  /               │
│              \         │   GEO 위성   │                /                │
│               \        │  고도 35,786km│              /                 │
│                \──────>└─────────────┘<─────────────/                   │
│                        │                   │                             │
│                        │   왕복 거리: 2 × 35,786 × 2 = 143,144 km       │
│                        │   왕복 지연: 143,144 / 300,000 ≈ 477 ms        │
│                        │   (처리 지연 추가 시 ~500-600 ms)               │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                          저궤도 위성 (LEO)                                │
│                                                                          │
│   지구국 A ───────────────────────────────────────────────> 지구국 B     │
│            \                                              /              │
│             \      ┌─────────────┐  ┌─────────────┐     /               │
│              \     │ LEO 위성 1   │->│ LEO 위성 2   │   /                │
│               \    │ 고도 ~550km  │  │ 고도 ~550km  │  /                 │
│                \──>└─────────────┘  └─────────────┘</                   │
│                                                                          │
│    왕복 거리 (사용자-위성-지구국-위성-사용자): 약 3,000 km              │
│    왕복 지연: 3,000 / 300,000 ≈ 10 ms                                   │
│    (ISL 위성간 링크 및 처리 지연 포함 시 ~20-40 ms)                      │
└──────────────────────────────────────────────────────────────────────────┘


================================================================================
[ 광섬유 신호 전파 원리 ]
================================================================================

광섬유 단면도:

     cladding (클래딩)
    ┌─────────────────────┐
    │   n₂ = 1.46         │
    │  ┌───────────────┐  │
    │  │  core (코어)   │  │
    │  │   n₁ = 1.48   │  │
    │  │               │  │
    │  │    ───────>   │  │  빛의 진행 방향
    │  │   전반사 반복  │  │
    │  │   /\/\/\/\/\  │  │
    │  │               │  │
    │  └───────────────┘  │
    └─────────────────────┘

전반사 조건: n₁ > n₂ (코어 굴절률 > 클래딩 굴절률)
임계각: θc = arcsin(n₂/n₁)

실제 광 경로 길이 > 물리적 거리 (지그재그로 인해)
유효 속도 = c / n₁ × cos(θ)  (θ: 입사각)


================================================================================
[ 전파 지연의 물리적 한계 ]
================================================================================

시나리오: 지구 반대편 통신 (지름 = 20,000 km)

이론적 최소 전파 지연 (단방향):
- 광섬유 직선: 20,000 / 200,000 = 100 ms
- 무선 직선: 20,000 / 300,000 = 67 ms

실제 해저 케이블 경로 (곡선):
- 광섬유 실제: ~120 ms (경로 굽이로 인해)

RTT (왕복):
- 광섬유 최소: 200 ms
- 실제 (처리/큐잉 추가): 220-300 ms

물리적 한계 돌파 방법:
1. 거리 단축 (CDN, 엣지 컴퓨팅)
2. 위성 직선 경로 (LEO)
3. 프리페칭 (예측적 캐싱)
```

### 심층 동작 원리: 전파 지연 영향 분석

1. **해저 케이블 경로**:
   - 실제 케이블은 해저 지형, 배타적경제구역(EEZ) 회피로 인해 직선보다 10~30% 길어집니다.
   - 중계기(Repeater)는 광신호를 증폭만 하고 지연은 무시할 수준입니다.

2. **지상 망 경로**:
   - 라우팅 경로가 물리적 최단 경로와 다를 수 있습니다.
   - 정책 라우팅, 비용 최적화로 인해 우회 경로가 발생합니다.

3. **위성 경로**:
   - GEO: 35,786km 고도로 인한 긴 지연
   - MEO: 5,000~20,000km (GPS 등)
   - LEO: 500~2,000km (스타링크, 원웹)

### 핵심 수식: 전파 지연 계산

```
기본 공식:
d_prop = d / v

광섬유에서:
d_prop = d × n / c
- d: 거리 (m)
- n: 굴절률 (~1.5)
- c: 빛의 속도 (299,792,458 m/s)

RTT 근사:
RTT ≈ 2 × d_prop × (1 + 경로_오버헤드_비율)

예시:
서울-뉴욕 11,000 km, 광섬유
d_prop = 11,000 × 1.5 / 299,792 = 55 ms
RTT ≈ 110 ms (이론적 최소)
```

### 핵심 코드: 전파 지연 계산기

```python
from dataclasses import dataclass
from typing import List, Tuple
import math

@dataclass
class CableRoute:
    """케이블 경로 정의"""
    name: str
    endpoints: Tuple[str, str]
    distance_km: float
    hop_count: int = 1

# 주요 해저 케이블 라우트
SUBMARINE_CABLES = [
    CableRoute("TPC-5", ("Japan", "USA"), 9,500, 1),
    CableRoute("SEA-ME-WE 3", ("Germany", "Japan"), 39,000, 3),
    CableRoute("AC-1", ("USA", "UK"), 6,400, 1),
    CableRoute("FLAG Europe-Asia", ("UK", "Japan"), 28,000, 2),
]

class PropagationDelayCalculator:
    """
    전파 지연 계산기
    """
    # 물리 상수
    SPEED_OF_LIGHT_VACUUM = 299_792.458  # km/s
    SPEED_OF_LIGHT_FIBER = 200_000       # km/s (굴절률 1.5 가정)
    SPEED_OF_LIGHT_WIRELESS = 299_700    # km/s (공기 중)

    def __init__(self, medium: str = 'fiber'):
        """
        Args:
            medium: 'fiber', 'wireless', 'vacuum'
        """
        self.medium = medium
        self.speed = {
            'fiber': self.SPEED_OF_LIGHT_FIBER,
            'wireless': self.SPEED_OF_LIGHT_WIRELESS,
            'vacuum': self.SPEED_OF_LIGHT_VACUUM
        }.get(medium, self.SPEED_OF_LIGHT_FIBER)

    def calculate_delay(self, distance_km: float) -> float:
        """
        전파 지연 계산

        Args:
            distance_km: 거리 (km)

        Returns:
            전파 지연 (ms)
        """
        delay_seconds = distance_km / self.speed
        return delay_seconds * 1000  # ms 변환

    def calculate_rtt(self, distance_km: float,
                     processing_overhead_ms: float = 0) -> float:
        """
        RTT 계산

        Args:
            distance_km: 단방향 거리 (km)
            processing_overhead_ms: 처리 지연 오버헤드 (ms)

        Returns:
            RTT (ms)
        """
        one_way = self.calculate_delay(distance_km)
        return 2 * one_way + processing_overhead_ms

    def calculate_satellite_delay(self, altitude_km: float,
                                  elevation_angle_deg: float = 90) -> dict:
        """
        위성 통신 지연 계산

        Args:
            altitude_km: 위성 고도 (km)
            elevation_angle_deg: 고각 (도)

        Returns:
            지연 정보 딕셔너리
        """
        earth_radius = 6_371  # km

        # 고각에 따른 실제 거리 계산
        if elevation_angle_deg >= 90:
            slant_range = altitude_km
        else:
            # 간소화된 계산
            angle_rad = math.radians(elevation_angle_deg)
            slant_range = altitude_km / math.sin(angle_rad)

        # 왕복 거리
        round_trip_distance = 2 * slant_range

        # 무선 전파 지연
        one_way_delay = self.calculate_delay(slant_range)
        rtt_delay = 2 * one_way_delay

        return {
            'altitude_km': altitude_km,
            'slant_range_km': slant_range,
            'round_trip_distance_km': round_trip_distance,
            'one_way_delay_ms': one_way_delay,
            'rtt_delay_ms': rtt_delay
        }

    def analyze_cable_route(self, cable: CableRoute) -> dict:
        """
        케이블 라우트 분석
        """
        one_way = self.calculate_delay(cable.distance_km)
        rtt = 2 * one_way

        return {
            'cable_name': cable.name,
            'endpoints': cable.endpoints,
            'distance_km': cable.distance_km,
            'one_way_delay_ms': one_way,
            'rtt_delay_ms': rtt,
            'medium': self.medium
        }

class GreatCircleDistance:
    """
    대권 거리(Great Circle Distance) 계산
    지구상 두 지점 간 최단 거리
    """
    EARTH_RADIUS_KM = 6_371

    @staticmethod
    def haversine(lat1: float, lon1: float,
                  lat2: float, lon2: float) -> float:
        """
        Haversine 공식으로 대권 거리 계산

        Args:
            lat1, lon1: 지점 1의 위도, 경도 (도)
            lat2, lon2: 지점 2의 위도, 경도 (도)

        Returns:
            거리 (km)
        """
        # 라디안 변환
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        lon1_rad = math.radians(lon1)
        lon2_rad = math.radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Haversine 공식
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(dlon / 2) ** 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return GreatCircleDistance.EARTH_RADIUS_KM * c

# 주요 도시 좌표
CITIES = {
    'Seoul': (37.5665, 126.9780),
    'Tokyo': (35.6762, 139.6503),
    'NewYork': (40.7128, -74.0060),
    'London': (51.5074, -0.1278),
    'Sydney': (-33.8688, 151.2093),
    'Singapore': (1.3521, 103.8198),
    'SanFrancisco': (37.7749, -122.4194),
}

class NetworkPathAnalyzer:
    """
    네트워크 경로 분석기
    """
    def __init__(self):
        self.prop_calc = PropagationDelayCalculator(medium='fiber')

    def analyze_city_pair(self, city1: str, city2: str) -> dict:
        """두 도시 간 지연 분석"""
        if city1 not in CITIES or city2 not in CITIES:
            return {'error': '알 수 없는 도시'}

        lat1, lon1 = CITIES[city1]
        lat2, lon2 = CITIES[city2]

        # 대권 거리 (이론적 최소)
        great_circle = GreatCircleDistance.haversine(lat1, lon1, lat2, lon2)

        # 실제 케이블은 15~30% 더 김
        actual_distance = great_circle * 1.2

        one_way = self.prop_calc.calculate_delay(actual_distance)
        rtt = 2 * one_way

        return {
            'from': city1,
            'to': city2,
            'great_circle_km': round(great_circle, 1),
            'estimated_actual_km': round(actual_distance, 1),
            'one_way_delay_ms': round(one_way, 2),
            'rtt_delay_ms': round(rtt, 2)
        }

# 실무 사용 예시
if __name__ == "__main__":
    # 1. 기본 전파 지연 계산
    calc = PropagationDelayCalculator(medium='fiber')

    print("=" * 60)
    print("전파 지연 계산 (광섬유)")
    print("=" * 60)

    for distance in [100, 1000, 5000, 10000, 20000]:
        delay = calc.calculate_delay(distance)
        rtt = calc.calculate_rtt(distance)
        print(f"{distance:6d} km: 단방향 {delay:6.2f} ms, RTT {rtt:6.2f} ms")

    # 2. 위성 통신 지연
    print("\n" + "=" * 60)
    print("위성 통신 지연")
    print("=" * 60)

    for altitude in [550, 2000, 10000, 35786]:  # LEO, MEO, GEO
        result = calc.calculate_satellite_delay(altitude)
        satellite_type = {
            550: 'LEO (Starlink)',
            2000: 'LEO (OneWeb)',
            10000: 'MEO (GPS)',
            35786: 'GEO'
        }.get(altitude, '')
        print(f"{satellite_type:15s}: 고도 {altitude:6d}km, "
              f"RTT {result['rtt_delay_ms']:6.1f}ms")

    # 3. 도시 간 지연 분석
    analyzer = NetworkPathAnalyzer()

    print("\n" + "=" * 60)
    print("서울에서 주요 도시까지 지연")
    print("=" * 60)

    for city in ['Tokyo', 'Singapore', 'London', 'NewYork', 'SanFrancisco', 'Sydney']:
        result = analyzer.analyze_city_pair('Seoul', city)
        print(f"Seoul -> {result['to']:15s}: "
              f"{result['estimated_actual_km']:7.0f}km, "
              f"RTT {result['rtt_delay_ms']:6.1f}ms")
