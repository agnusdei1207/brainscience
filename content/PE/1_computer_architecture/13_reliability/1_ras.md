+++
title = "449. RAS (Reliability, Availability, Serviceability)"
description = "고신뢰성 시스템의 핵심 지표인 RAS 특성 심층 분석"
date = "2026-03-05"
[taxonomies]
tags = ["RAS", "Reliability", "Availability", "Serviceability", "고신뢰성", "결함허용"]
categories = ["studynotes-1_computer_architecture"]
+++

# 449. RAS (Reliability, Availability, Serviceability)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: RAS는 시스템이 얼마나 오래 고장 없이 동작하는가(Reliability), 필요할 때 얼마나 사용 가능한가(Availability), 얼마나 빨리 복구 가능한가(Serviceability)를 종합적으로 평가하는 고신뢰성 시스템의 핵심 척도이다.
> 2. **가치**: 엔터프라이즈 서버에서 RAS 적용 시 MTBF 100,000시간 이상, 가용성 99.999%(연간 5분 이하 다운타임) 달성 가능하며, 비즈니스 연속성 보장으로 연간 수십억 원의 손실 방지 효과가 있다.
> 3. **융합**: RAS는 하드웨어 이중화, ECC 메모리, 핫스왑, 컨테이너 오케스트레이션(K8s), 클라우드 멀티AZ 배치 등 전 계층에서 구현되며, 특히 AI 인퍼런스 서버의 SLA 보장에 필수적이다.

---

### I. 개요 (Context & Background)

#### 개념 정의

**RAS(Reliability, Availability, Serviceability)**는 컴퓨터 시스템, 특히 엔터프라이즈급 서버, 스토리지, 네트워크 장비의 신뢰성을 종합적으로 평가하고 설계하는 프레임워크이다. IBM 메인프레임 시대부터 발전해 온 RAS 개념은 현대 클라우드 인프라, AI 가속기, 자율주행 시스템 등에서도 핵심 설계 철학으로 자리 잡았다.

- **Reliability (신뢰성)**: 시스템이 주어진 조건과 시간 동안 고장 없이 기능을 수행할 확률. MTBF(Mean Time Between Failures)로 정량화된다.
- **Availability (가용성)**: 시스템이 언제든지 사용 가능한 상태로 존재할 확률. MTBF와 MTTR(Mean Time To Repair)의 함수로 표현된다.
- **Serviceability (유지보수성/서비스 용이성)**: 고장 발생 시 얼마나 빠르고 효율적으로 진단, 수리, 업그레이드할 수 있는 능력. 예방 정비, 핫스왑, 원격 관리 등이 포함된다.

#### 비유

> **RAS는 "병원 응급실의 3가지 핵심 지표"와 같다.**
>
> - **Reliability** = 응급실 장비가 고장 없이 계속 작동할 신뢰도 (제세동기가 얼마나 자주 고장 나는가?)
> - **Availability** = 응급실이 24시간 365일 언제든 환자를 받을 준비가 되어 있는가 (문이 닫히는 시간이 연간 5분 이내인가?)
> - **Serviceability** = 장비가 고장 났을 때 얼마나 빨리 수리 기사가 와서 고칠 수 있는가 (예비 부품이 준비되어 있고, 수리 매뉴얼이 명확한가?)
>
> 이 세 가지가 모두 높아야 "최고의 응급실"로 인정받을 수 있다.

#### 등장 배경 및 발전 과정

1. **1960-70년대: 메인프레임 시대의 태동**
   - IBM System/360 및 이후 모델에서 비즈니스 크리티컬 시스템의 중단은 막대한 손실을 초래
   - 초기 RAS 개념: 이중화(Redundancy), ECC 메모리, 핫스왑 디스크

2. **1980-90년대: UNIX 서버와 RISC 아키텍처**
   - Sun SPARC, HP PA-RISC, IBM POWER 등 엔터프라이즈 UNIX 서버에서 RAS 고도화
   - CPU 다이내믹 재구성, 메모리 미러링, 서비스 프로세서 도입

3. **2000년대: x86 서버의 RAS 강화**
   - Intel Xeon, AMD Opteron에서 RAS 기능 대거 도입
   - MCA(Machine Check Architecture), 메모리 스페어링, PCIe AER

4. **2010년대~현재: 클라우드 및 AI 인프라**
   - AWS, Azure, GCP 등 클라우드 서비스에서 "99.99% 가용성 SLA" 보장
   - NVIDIA H100, TPU 등 AI 가속기에 RAS 기능 내장 (ECC, SRAM 스크러빙)
   - 컨테이너/Kubernetes의 Self-healing, Auto-scaling으로 소프트웨어 RAS 구현

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### RAS 구성 요소 상세 분석

| 구성 요소 | 정의 | 정량적 지표 | 구현 기술 | 비고 |
|-----------|------|-------------|-----------|------|
| **Reliability** | 고장 없이 동작할 확률 | MTBF (시간), 고장률 λ (1/MTBF) | 부품 품질 관리, 번인 테스트, 설계 여유 | R(t) = e^(-λt) |
| **Availability** | 필요 시 사용 가능 확률 | A = MTBF/(MTBF+MTTR), % | 이중화, 페일오버, 자동 복구 | 99.999% = "Five 9s" |
| **Serviceability** | 수리/유지보수 용이성 | MTTR (시간), 예방 정비 주기 | 핫스왑, BMC/IPMI, 진단 로그, 모듈화 | 설계 단계부터 고려 |

#### RAS 삼각형 다이어그램

```
                          ┌─────────────────────┐
                          │     RAS Triangle    │
                          │  (상호 보완 관계)    │
                          └─────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
          ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
          │ Reliability │  │ Availability│  │Serviceability│
          │  (신뢰성)   │  │  (가용성)   │  │ (유지보수성) │
          └─────────────┘  └─────────────┘  └─────────────┘
                │                │                │
                │   MTBF         │  MTBF/(MTBF   │    MTTR
                │   ↑↑↑         │   +MTTR)       │    ↓↓↓
                │                │                │
                ▼                ▼                ▼
          · 부품 품질      · 이중화/다중화   · 핫스왑
          · 설계 여유      · 페일오버       · 원격 관리(BMC)
          · 번인 테스트    · 자동 복구      · 진단 로그
          · ECC/패리티     · 로드밸런싱     · 모듈화 설계
          · 환경 제어      · 지리적 분산     · 예방 정비
```

#### 가용성 계산 및 등급 체계

```
┌─────────────────────────────────────────────────────────────────┐
│                    Availability Tiers                           │
├─────────────────┬────────────────┬─────────────────────────────┤
│   가용성 (%)    │   연간 다운타임  │         등급/용도           │
├─────────────────┼────────────────┼─────────────────────────────┤
│    99.0%        │   87.6 시간     │  일반 PC, 소규모 서버       │
│    99.9%        │    8.76 시간    │  중소기업 서버 (Three 9s)   │
│    99.99%       │   52.56 분      │  엔터프라이즈 (Four 9s)     │
│    99.999%      │    5.26 분      │  금융/통신 (Five 9s)        │
│    99.9999%     │   31.54 초      │  미션 크리티컬 (Six 9s)     │
└─────────────────┴────────────────┴─────────────────────────────┘

가용성 공식: A = MTBF / (MTBF + MTTR)

예시 계산:
· MTBF = 10,000시간, MTTR = 1시간
· A = 10,000 / (10,000 + 1) = 0.9999 = 99.99%
```

#### 심층 동작 원리: 5단계 RAS 구현 프로세스

```
┌──────────────────────────────────────────────────────────────────┐
│         RAS Implementation Lifecycle (5-Step Process)           │
└──────────────────────────────────────────────────────────────────┘

Step 1: [고장 감지 (Fault Detection)]
        ┌────────────────────────────────────────────────────┐
        │ · 하드웨어: ECC, 패리티, CRC, heartbeat           │
        │ · 소프트웨어: Watchdog, health check, timeout     │
        │ · 센서: 온도, 전압, 팬 속도 임계값 초과            │
        │ · Intel MCA, PCIe AER, Memory Scrubbing           │
        └────────────────────────────────────────────────────┘
                                │
                                ▼
Step 2: [고장 격리 (Fault Isolation)]
        ┌────────────────────────────────────────────────────┐
        │ · 고장 난 컴포넌트 식별 (CPU, 메모리, 디스크 등)    │
        │ · 영향 범위 한정 (다른 컴포넌트로 전파 방지)        │
        │ · 로그 기록 (BMC SEL, OS 커널 로그)               │
        │ · 알림 발송 (SNMP trap, 이메일, SMS)              │
        └────────────────────────────────────────────────────┘
                                │
                                ▼
Step 3: [고장 대응 (Fault Containment/Recovery)]
        ┌────────────────────────────────────────────────────┐
        │ · 자동 페일오버 (Standby → Active)                │
        │ · 서비스 마이그레이션 (VM migration, pod reschedule)│
        │ · 트래픽 라우팅 변경 (Load balancer)              │
        │ · 저성능 모드로 안전 운전 (Degraded mode)         │
        └────────────────────────────────────────────────────┘
                                │
                                ▼
Step 4: [복구 및 수리 (Repair & Restoration)]
        ┌────────────────────────────────────────────────────┐
        │ · 핫스왑 부품 교체 (디스크, 팬, 전원)             │
        │ · 메모리 페이지 리타이어 (Bad page offline)       │
        │ · 마이크로코드/펌웨어 업데이트                    │
        │ · 예비 자원으로 재구성 (Spare core activation)   │
        └────────────────────────────────────────────────────┘
                                │
                                ▼
Step 5: [정상화 및 검증 (Normalization & Verification)]
        ┌────────────────────────────────────────────────────┐
        │ · 교체 부품 인식 및 구성                          │
        │ · 서비스 재시작 및 health check                   │
        │ · 트래픽 복원 (풀 캐패시티)                       │
        │ · RAS 지표 업데이트 (MTBF, MTTR 기록)            │
        └────────────────────────────────────────────────────┘
```

#### 핵심 알고리즘: 가용성 계산 및 예측 모델

```python
#!/usr/bin/env python3
"""
RAS Metrics Calculator & Predictor
- MTBF, MTTR, Availability 계산
- 고장률 예측 (배스터브 곡선)
- SLA 달성 가능성 분석
"""

import math
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum

class FailurePhase(Enum):
    INFANT_MORTALITY = "early"      # 초기 고장기
    RANDOM_FAILURES = "useful"       # 우발 고장기
    WEAR_OUT = "wearout"             # 마모 고장기

@dataclass
class RASMetrics:
    mtbf: float      # Mean Time Between Failures (hours)
    mttr: float      # Mean Time To Repair (hours)

    @property
    def availability(self) -> float:
        """가용성 계산: A = MTBF / (MTBF + MTTR)"""
        return self.mtbf / (self.mtbf + self.mttr)

    @property
    def availability_percent(self) -> str:
        """가용성을 퍼센트와 9의 개수로 표시"""
        pct = self.availability * 100
        nines = min(int(-math.log10(1 - self.availability)), 6)
        return f"{pct:.6f}% ({nines} 9s)"

    @property
    def annual_downtime(self) -> Tuple[float, str]:
        """연간 다운타임 계산"""
        hours_per_year = 365.25 * 24
        downtime_hours = hours_per_year * (1 - self.availability)

        if downtime_hours >= 1:
            return downtime_hours, f"{downtime_hours:.2f} 시간"
        elif downtime_hours >= 1/60:
            return downtime_hours, f"{downtime_hours * 60:.2f} 분"
        else:
            return downtime_hours, f"{downtime_hours * 3600:.2f} 초"

    @property
    def failure_rate(self) -> float:
        """고장률 λ = 1/MTBF (failures per hour)"""
        return 1 / self.mtbf if self.mtbf > 0 else float('inf')

    def reliability_at_time(self, t_hours: float) -> float:
        """
        시간 t 후 신뢰도 계산 (지수 분포 가정)
        R(t) = e^(-λt) = e^(-t/MTBF)
        """
        return math.exp(-t_hours / self.mtbf)

def calculate_system_availability(
    component_metrics: List[RASMetrics],
    redundancy_config: str = "series"
) -> RASMetrics:
    """
    시스템 전체 가용성 계산

    Args:
        component_metrics: 각 컴포넌트의 RAS 메트릭
        redundancy_config: "series"(직렬), "parallel"(병렬/이중화)

    Returns:
        시스템 전체의 RAS 메트릭
    """
    if redundancy_config == "series":
        # 직렬: 모든 컴포넌트가 작동해야 함
        # A_system = A1 * A2 * ... * An
        system_availability = 1.0
        total_failure_rate = 0.0

        for comp in component_metrics:
            system_availability *= comp.availability
            total_failure_rate += comp.failure_rate

        system_mtbf = 1 / total_failure_rate if total_failure_rate > 0 else float('inf')
        # 근사: MTTR은 가장 긴 것으로
        system_mttr = max(c.mttr for c in component_metrics)

    elif redundancy_config == "parallel":
        # 병렬(Active-Active): 하나라도 작동하면 됨
        # A_system = 1 - (1-A1) * (1-A2) * ... * (1-An)
        system_unavailability = 1.0
        for comp in component_metrics:
            system_unavailability *= (1 - comp.availability)

        system_availability = 1 - system_unavailability
        # N+1 중복 시스템의 근사 MTBF
        n = len(component_metrics)
        avg_mtbf = sum(c.mtbf for c in component_metrics) / n
        system_mtbf = avg_mtbf * (n / (n - 1)) if n > 1 else avg_mtbf
        system_mttr = min(c.mttr for c in component_metrics)

    else:
        raise ValueError(f"Unknown redundancy config: {redundancy_config}")

    return RASMetrics(mtbf=system_mtbf, mttr=system_mttr)

def predict_failure_rate(
    base_failure_rate: float,
    phase: FailurePhase,
    hours_in_service: float,
    wearout_threshold: float = 50000  # 마모 고장기 시작 시점
) -> float:
    """
    배스터브 곡선 기반 고장률 예측

    λ(t) = λ_early(t) + λ_random + λ_wearout(t)
    """
    if phase == FailurePhase.INFANT_MORTALITY:
        # 초기 고장기: 웨이블 분포 (감소하는 고장률)
        return base_failure_rate * (1 + math.exp(-hours_in_service / 100))

    elif phase == FailurePhase.RANDOM_FAILURES:
        # 우발 고장기: 일정한 고장률
        return base_failure_rate

    elif phase == FailurePhase.WEAR_OUT:
        # 마모 고장기: 증가하는 고장률
        wear_factor = 1 + ((hours_in_service - wearout_threshold) / 10000) ** 2
        return base_failure_rate * wear_factor

    return base_failure_rate

# 예시 사용
if __name__ == "__main__":
    # 단일 서버 RAS 메트릭
    server = RASMetrics(mtbf=50000, mttr=4)  # MTBF: 50,000시간, MTTR: 4시간
    print(f"단일 서버 가용성: {server.availability_percent}")
    print(f"연간 다운타임: {server.annual_downtime[1]}")
    print(f"1년 후 신뢰도: {server.reliability_at_time(8760):.4f}")

    # 이중화 서버 (Active-Standby)
    primary = RASMetrics(mtbf=50000, mttr=4)
    standby = RASMetrics(mtbf=100000, mttr=1)  # Standby는 고장률 낮음

    ha_system = calculate_system_availability(
        [primary, standby],
        redundancy_config="parallel"
    )
    print(f"\nHA 시스템 가용성: {ha_system.availability_percent}")
    print(f"HA 시스템 연간 다운타임: {ha_system.annual_downtime[1]}")
```

---

### III. 융합 비교 및 다각도 분석

#### RAS 등급별 시스템 비교

| 등급 | 가용성 | 연간 다운타임 | 전형적 시스템 | 구현 비용 | 주요 기술 |
|------|--------|---------------|---------------|-----------|-----------|
| **Tier 1** | 99% | 87.6시간 | 소규무 서버, 데스크톱 | 기본 | RAID 1, UPS |
| **Tier 2** | 99.9% | 8.76시간 | 중소기업 서버 | 중간 | RAID 5/6, 이중 전원 |
| **Tier 3** | 99.99% | 52.6분 | 엔터프라이즈 서버 | 높음 | 이중화, 핫스왑, BMC |
| **Tier 4** | 99.999% | 5.26분 | 금융/통신 인프라 | 매우 높음 | 다중 경로, 지리적 이중화 |
| **Tier 5** | 99.9999% | 31.5초 | 미션 크리티컬 | 극도로 높음 | TMR, 무정전 설계 |

#### RAS vs. 비용 트레이드오프

```
        비용 (Cost)
            ▲
            │                                    ● Tier 5
            │                              ● Tier 4
            │                        ● Tier 3
            │                  ● Tier 2
            │            ● Tier 1
            │      ● 기본
            └──────────────────────────────────────▶ 가용성
                  99%  99.9%  99.99%  99.999%  99.9999%

    ※ "9 하나 추가에 비용 2~3배 증가" (수확 체감 법칙)
```

#### 과목 융합 분석

| 융합 과목 | RAS 연계 내용 | 시너지 효과 |
|-----------|---------------|-------------|
| **OS** | 커널 Panic 복구, OOM Killer, Cgroups 자원 격리 | 소프트웨어 계층 RAS 구현 |
| **네트워크** | 다중 경로 라우팅, BGP 페일오버, Anycast | 네트워크 계층 가용성 보장 |
| **DB** | 복제(Replication), 페일오버 클러스터, 백업/복구 | 데이터 무결성 + 가용성 동시 확보 |
| **보안** | 보안 장비 이중화, DDoS 방어, 백업 암호화 | 보안 사고 시에도 서비스 연속성 |
| **클라우드** | Multi-AZ 배치, Auto Scaling, Blue-Green 배포 | 인프라 계층 자동 복구 |
| **AI/ML** | 모델 서빙 A/B 테스트, Canary 배포, 모델 버전관리 | AI 서비스 무중단 배포 |

---

### IV. 실무 적용 및 기술사적 판단

#### 실무 시나리오

**시나리오 1: 금융사 코어뱅킹 시스템 RAS 설계**
```
요구사항: 99.999% 가용성, 연간 다운타임 5분 이하

해결 방안:
1. 이중화 구조
   - Active-Active 데이터베이스 클러스터 (Oracle RAC)
   - 애플리케이션 서버 4중화 (Load Balancer)
   - 네트워크 2중화 (이중 ISP, 이중 스위치)

2. 지리적 분산
   - 서울-부산 DR 센터 구축
   - 동기 복제 (RPO=0) + 비동기 복제 (RPO<5분)

3. 자동 복구
   - Heartbeat 기반 페일오버 (30초 이내)
   - Kubernetes Self-healing

4. 모니터링
   - 실시간 RAS 대시보드
   - 자동 알림 (PagerDuty 연동)

예상 효과:
· 연간 다운타임: 3분 이내
· MTBF: 200,000시간 이상
· SLA 위반 페널티 방지: 연간 10억 원 이상
```

**시나리오 2: AI 인퍼런스 서버 RAS 설계**
```
요구사항: H100 GPU 8장 클러스터, 99.99% 가용성

해결 방안:
1. GPU RAS 기능 활용
   - NVLink 이중화
   - GPU 메모리 ECC 활성화
   - SRAM Scrubbing

2. 서비스 레벨 이중화
   - 2대의 서버에 모델 분산 배치
   - Triton Inference Server 클러스터

3. 자동 복구
   - GPU 고장 시 자동으로 다른 GPU로 워크로드 이관
   - degraded mode (성능 저하 허용, 서비스 중단 방지)

비용 분석:
· 이중화 비용: 서버 2대 × 5억 원 = 10억 원
· SLA 위반 방지 효과: 연간 5억 원
· ROI: 약 2년
```

**시나리오 3: 스타트업 SaaS 서비스 RAS 진화 과정**
```
Phase 1 (MVP): 가용성 99% 목표
· 단일 서버 + Managed DB (AWS RDS)
· 일일 백업, 수동 복구
· 비용: 월 100만 원

Phase 2 (성장기): 가용성 99.9% 목표
· Multi-AZ RDS, Auto Scaling Group
· CloudWatch 알림, Chef/Puppet 자동화
· 비용: 월 500만 원

Phase 3 (성숙기): 가용성 99.99% 목표
· Multi-Region Active-Active
· Kubernetes 기반 마이크로서비스
· Chaos Engineering (Gremlin)
· 비용: 월 3,000만 원

※ 단계적 투자로 비즈니스 성장과 RAS 투자 정렬
```

#### 도입 시 고려사항 체크리스트

```
□ 기술적 고려사항
  □ MTBF/MTTR 요구사항 정의
  □ 이중화 레벨 결정 (N+1, 2N, Active-Active)
  □ 페일오버 시간 목표 (RTO)
  □ 데이터 손실 허용 범위 (RPO)
  □ 핫스왑 가능 컴포넌트 식별
  □ BMC/IPMI 관리 네트워크 분리

□ 운영적 고려사항
  □ 24/7 모니터링 체계
  □ On-call 로테이션 및 에스컬레이션
  □ 정기적인 DR 훈련 (분기 1회 이상)
  □ 예비 부품 확보 (SPK, Spare Parts Kit)
  □ 유지보수 계약 (SLA) 체결

□ 비용적 고려사항
  □ 이중화 비용 vs 다운타임 비용 분석
  □ TCO (Total Cost of Ownership) 계산
  □ 클라우드 vs 온프레미스 비교

□ 보안적 고려사항
  □ 관리 인터페이스 (BMC) 접근 통제
  □ 페일오버 경로 보안
  □ 백업 데이터 암호화
```

#### 안티패턴 및 주의사항

```
❌ Anti-pattern 1: "이중화만 하면 된다"
   → 이중화 없이 단일 장애점(SPOF) 해결이 우선

❌ Anti-pattern 2: "무조건 99.999% 목표"
   → 비즈니스 요구사항에 맞는 적정 수준 설정

❌ Anti-pattern 3: "HA 소프트웨어가 알아서 한다"
   → 정기적인 페일오버 테스트 필수

❌ Anti-pattern 4: "하드웨어만 RAS 적용"
   → 소프트웨어 계층(SW RAS)도 함께 고려

❌ Anti-pattern 5: "복구 계획만 있으면 된다"
   → 실제 복구 절차 검증(Dry run) 필수
```

---

### V. 기대효과 및 결론

#### 정량적/정성적 기대효과

| 구분 | 도입 전 | 도입 후 | 개선 효과 |
|------|---------|---------|-----------|
| 가용성 | 99.5% | 99.99% | 99.5% → 52분 다운타임 |
| MTBF | 5,000시간 | 50,000시간 | 10배 향상 |
| MTTR | 8시간 | 30분 | 16배 단축 |
| 연간 다운타임 비용 | 1억 원 | 500만 원 | 95% 절감 |
| SLA 달성률 | 90% | 99.9% | 10% 향상 |

#### 미래 전망

1. **AI 기반 예지 보전 (Predictive Maintenance)**
   - 머신러닝으로 고장 시점 예측
   - 사전 예방 정비로 MTBF 획기적 향상

2. **자율 복구 시스템 (Self-Healing Infrastructure)**
   - Kubernetes, Service Mesh 등 소프트웨어 RAS 고도화
   - 인간 개입 없는 완전 자동 복구

3. **Quantum-Resistant RAS**
   - 양자 컴퓨팅 환경에서의 새로운 고장 모드 대응
   - 양자 오류 정정 (Quantum Error Correction)

#### 참고 표준/가이드

- **IEEE 1413**: Reliability Prediction Standard
- **ISO/IEC 25010**: Systems and software Quality Requirements
- **ITIL v4**: Service Availability Management
- **Uptime Institute Tier Standards**: Data Center Classification
- **NIST SP 800-34**: Contingency Planning Guide

---

### 관련 개념 맵 (Knowledge Graph)

- [450. MTBF](./2_mtbf.md) - 평균 무고장 시간, Reliability의 핵심 지표
- [451. MTTR](./3_mttr.md) - 평균 수리 시간, Serviceability의 핵심 지표
- [452. 가용성](./4_availability.md) - Availability, RAS의 종합 결과
- [453. 고장 허용 시스템](./5_fault_tolerance.md) - Fault Tolerance, RAS를 구현하는 아키텍처
- [454. SPOF](./6_spof.md) - 단일 장애점, RAS 설계에서 반드시 제거해야 할 위험 요소
- [463. ECC 메모리](./15_ecc_memory.md) - Error Correcting Code, Reliability 핵심 기술

---

### 어린이를 위한 3줄 비유 설명

**RAS는 "절대 멈추지 않는 놀이공원"과 같아요!**

1. **Reliability (신뢰성)**는 놀이기구가 고장 없이 계속 안전하게 작동하는 거예요. 롤러코스터가 1년 내내 고장 한 번 나지 않고 달리는 것처럼요!

2. **Availability (가용성)**는 놀이공원이 365일 24시간 언제나 문을 열어서 친구들이 언제 가도 놀 수 있는 거예요. 문이 닫히는 시간이 1년에 5분뿐이라면 정말 대단하겠죠?

3. **Serviceability (유지보수성)**는 놀이기구가 고장 나더라도 직원 아저씨가 5분 만에 쌩쌩 고쳐서 다시 탈 수 있게 하는 거예요. 예비 부품도 많이 갖고 있고, 고치는 방법도 완벽하게 알고 있어서요!
