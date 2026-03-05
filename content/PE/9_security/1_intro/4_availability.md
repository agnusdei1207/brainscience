+++
title = "가용성 (Availability)"
date = 2026-03-05
[extra]
categories = "studynotes-security"
+++

# 가용성 (Availability)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 인가된 사용자가 필요한 시점에 정보와 자원에 접근할 수 있는 능력으로, 고가용성(HA) 설계·DDoS 방어·백업/복원 체계가 핵심 구현 기술이다.
> 2. **가치**: 99.99% 가용성(연간 52.6분 중단)은 전자상거래에서 매출 손실을 90% 감소시키며, SLA 위반 페널티(최대 25%)를 예방한다.
> 3. **융합**: 클라우드 네이티브 환경에서는 오토스케일링·서비스 메시·멀티 리전 페일오버가 가용성을 99.999%까지 끌어올린다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

**가용성(Availability)**이란 인가된 사용자가 필요한 시점에 정보 시스템, 데이터, 서비스에 정상적으로 접근하고 사용할 수 있는 능력을 의미한다. 이는 단순히 "서버가 켜져 있는 상태"를 넘어, **서비스 수준 협약(SLA)에 정의된 성능 기준을 충족하며 사용자 요청에 응답할 수 있는 상태**를 보장하는 종합적인 개념이다.

가용성은 일반적으로 **가용성 비율(%)**로 측정되며, 이는 전체 시간 대비 정상 서비스 제공 시간의 비율이다. 업계에서는 이를 "Nines of Availability"로 표현한다.

```
┌─────────────────────────────────────────────────────────────────┐
│                   가용성 등급 (Nines of Availability)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   가용성    연간 중단시간     월간 중단시간    일간 중단시간    │
│   ─────────────────────────────────────────────────────────────│
│   90%       36.5일           73시간          2.4시간          │
│   95%       18.3일           36.5시간        1.2시간          │
│   99%       3.65일           7.3시간         14.4분           │
│   99.9%     8.77시간         43.8분          1.44분           │
│   99.99%    52.6분           4.38분          8.64초           │
│   99.999%   5.26분           26.3초          0.864초          │
│   99.9999%  31.5초           2.63초          0.0864초         │
│                                                                 │
│   ▲─────────────────────────────────────────────────────▲       │
│   │                  비용 기하급수적 증가                  │       │
│   └─────────────────────────────────────────────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 💡 비유

가용성은 **"24시간 편의점"**과 같다.
- 언제 가도 문이 열려 있고 물건을 살 수 있다
- 가끔 정기 점검으로 잠깐 문을 닫을 수도 있다
- 하지만 너무 자주 문을 닫으면 손님들은 다른 가게로 간다

또 다른 비유로 **"비상 발전기"**가 있다.
- 정전이 나면 자동으로 발전기가 켜져서 전기를 공급한다
- 전기가 없으면 병원의 수술실, 은행의 서버는 멈춘다
- 비상 발전기는 평소엔 대기하다가 필요할 때 즉시 작동해야 한다

### 등장 배경 및 발전 과정

**1. 기존 기술의 치명적 한계점**
- **단일 장애점(SPOF)**: 서버 1대가 고장 나면 서비스 전체 중단
- **수동 복구**: 장애 발생 시 관리자가 수동으로 복구 (평균 4-8시간)
- **DDoS 공격**: 대규모 트래픽 공격으로 서비스 마비 (2016년 Dyn 공격)

**2. 혁신적 패러다임 변화**
- **1990년대 HA Clustering**: Active-Standby 이중화 (Veritas, Sun Cluster)
- **2000년대 L4 로드밸런싱**: 트래픽 분산 + 헬스체크 (F5, Cisco)
- **2010년대 클라우드**: 오토스케일링, 멀티 리전 (AWS, Azure)
- **2020년대 서비스 메시**: 인텔리전트 라우팅, 서킷 브레이커 (Istio, Linkerd)

**3. 비즈니스적 요구사항 강제**
- **전자상거래**: 1시간 중단 = 매출 손실 10만 달러+
- **금융 서비스**: SLA 99.99% 이상 의무 (규제)
- **헬스케어**: 생명 관련 서비스는 99.999% 요구

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|-----------|-----------|-------------------|-----------|------|
| **이중화 (Redundancy)** | 단일 장애점 제거 | Active-Active, Active-Standby | RAID, HA Cluster | 예비 타이어 |
| **로드밸런싱** | 트래픽 분산 및 헬스체크 | L4/L7 스위칭, 알고리즘 기반 분배 | F5, Nginx, HAProxy | 교통경찰 |
| **페일오버** | 장애 시 자동 전환 | Heartbeat, VIP 이동, DNS 페일오버 | VRRP, Pacemaker | 비상계단 |
| **백업/복원** | 데이터 보호 및 복구 | 전체/증분/차이 백업, RTO/RPO | Veeam, Commvault | 보험 |
| **DDoS 방어** | 대규모 공격 완화 | Scrubbing, Rate Limiting, Anycast | Cloudflare, Akamai | 경비원 |
| **오토스케일링** | 부하 대응 자동 확장 | 메트릭 기반 트리거, 인스턴스 증설 | AWS ASG, K8s HPA | 늘어나는 건물 |

### 고가용성 아키텍처 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    고가용성 (HA) 종합 아키텍처                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   [사용자 계층]                                                              │
│   ┌──────────────────────────────────────────────────────────────────┐     │
│   │   👤 사용자 (Internet) ──────→ CDN (Cloudflare)                  │     │
│   │                    │              ├── 캐싱                        │     │
│   │                    │              ├── DDoS 방어                   │     │
│   │                    │              └── Anycast                      │     │
│   └────────────────────┼──────────────────────────────────────────────┘     │
│                        │                                                    │
│   [DNS 계층]            ▼                                                    │
│   ┌──────────────────────────────────────────────────────────────────┐     │
│   │   Route 53 / Cloud DNS                                           │     │
│   │   ├── Health Check (30초 간격)                                   │     │
│   │   ├── Failover Routing (Active-Passive)                          │     │
│   │   └── Latency Routing (Multi-Region)                             │     │
│   └────────────────────────┬─────────────────────────────────────────┘     │
│                            │                                                │
│   [로드밸런서 계층]        ▼                                                │
│   ┌──────────────────────────────────────────────────────────────────┐     │
│   │   ALB / NLB (L7/L4 Load Balancer)                                │     │
│   │   ┌──────────────┐        ┌──────────────┐                       │     │
│   │   │  ALB-1 (AZ-A)│ ◄────► │  ALB-2 (AZ-B)│  (Cross-Zone LB)      │     │
│   │   │  Active      │        │  Active      │                       │     │
│   │   └──────┬───────┘        └──────┬───────┘                       │     │
│   │          │                       │                                │     │
│   │   Health Check: HTTP GET /health (5초 간격, 3회 실패 시 제거)    │     │
│   └──────────┼───────────────────────┼────────────────────────────────┘     │
│              │                       │                                      │
│   [애플리케이션 계층]                                                  │
│   ┌──────────┼───────────────────────┼────────────────────────────────┐     │
│   │          ▼                       ▼                                │     │
│   │   ┌────────────┐           ┌────────────┐                        │     │
│   │   │ EC2-1 (AZ-A)│           │ EC2-2 (AZ-B)│                       │     │
│   │   │ Web Server │           │ Web Server │                        │     │
│   │   └─────┬──────┘           └─────┬──────┘                        │     │
│   │         │                        │                                │     │
│   │   ┌────────────┐           ┌────────────┐                        │     │
│   │   │ EC2-3 (AZ-A)│           │ EC2-4 (AZ-B)│  (Auto Scaling Group) │     │
│   │   │ App Server │           │ App Server │                        │     │
│   │   └─────┬──────┘           └─────┬──────┘                        │     │
│   │         │                        │                                │     │
│   │   [오토스케일링 정책]                                             │     │
│   │   • CPU > 70% → 인스턴스 +1 (Scale Out)                          │     │
│   │   • CPU < 30% → 인스턴스 -1 (Scale In)                           │     │
│   │   • Min: 2, Max: 10, Desired: 4                                  │     │
│   └──────────┼───────────────────────┼────────────────────────────────┘     │
│              │                       │                                      │
│   [데이터베이스 계층]                                                  │
│   ┌──────────┼───────────────────────┼────────────────────────────────┐     │
│   │          ▼                       ▼                                │     │
│   │   ┌────────────────────────────────────────────┐                  │     │
│   │   │         RDS Multi-AZ (Primary-Standby)     │                  │     │
│   │   │   ┌───────────┐      ┌───────────┐        │                  │     │
│   │   │   │ Primary   │ ───→ │ Standby   │        │ (동기 복제)      │     │
│   │   │   │ (AZ-A)    │      │ (AZ-B)    │        │                  │     │
│   │   │   │ Read/Write│      │ Ready     │        │                  │     │
│   │   │   └───────────┘      └───────────┘        │                  │     │
│   │   │                                            │                  │     │
│   │   │   ┌────────────────────────────────────┐  │                  │     │
│   │   │   │   Read Replicas (읽기 전용)        │  │                  │     │
│   │   │   │   ┌─────┐ ┌─────┐ ┌─────┐         │  │                  │     │
│   │   │   │   │RR-1 │ │RR-2 │ │RR-3 │         │  │ (비동기 복제)    │     │
│   │   │   │   └─────┘ └─────┘ └─────┘         │  │                  │     │
│   │   │   └────────────────────────────────────┘  │                  │     │
│   │   └────────────────────────────────────────────┘                  │     │
│   │                                                                    │     │
│   │   [페일오버 시나리오]                                              │     │
│   │   Primary 장애 → Standby 승격 (60-120초 내 자동 전환)             │     │
│   └────────────────────────────────────────────────────────────────────┘     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 심층 동작 원리: HA 장애 감지 및 복구

**1단계: 모니터링 → 2단계: 장애 감지 → 3단계: 장애 격리 → 4단계: 페일오버 → 5단계: 복구**

```
[1단계: 모니터링]             [2단계: 장애 감지]
┌──────────────────┐         ┌──────────────────┐
│ Health Check     │         │ 연속 실패 횟수   │
│                  │   →     │ Threshold 도달   │
│ • HTTP GET       │         │ (3회 연속 실패)  │
│ • TCP Connect    │         │                  │
│ • ICMP Ping      │         │ 장애 판정        │
│ 간격: 5초        │         │                  │
└────────┬─────────┘         └────────┬─────────┘
         │                            │
         ▼                            ▼
[3단계: 장애 격리]           [4단계: 페일오버]
┌──────────────────┐         ┌──────────────────┐
│ 트래픽 차단      │         │ Standby 승격     │
│ (LB에서 제거)    │   →     │ VIP 이동         │
│                  │         │ DNS 갱신         │
│ 알림 발송        │         │ 서비스 재개      │
│ (PagerDuty)      │         │                  │
└────────┬─────────┘         └────────┬─────────┘
         │                            │
         ▼                            ▼
[5단계: 복구]                 [정상화]
┌──────────────────┐         ┌──────────────────┐
│ 원인 분석        │         │ 서비스 정상      │
│ 장애 서버 수리   │   →     │ Active-Active    │
│ 동기화           │         │ 복구 완료        │
│ 재투입           │         │                  │
└──────────────────┘         └──────────────────┘
```

### 핵심 알고리즘: 가용성 계산 및 SLA 모니터링

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict
import statistics

@dataclass
class Incident:
    """장애 이력"""
    start_time: datetime
    end_time: datetime
    severity: str  # 'critical', 'major', 'minor'
    affected_service: str
    root_cause: str

class AvailabilityCalculator:
    """
    가용성 계산 및 SLA 모니터링

    가용성 = (총 시간 - 중단 시간) / 총 시간 × 100
    """

    def __init__(self, sla_target: float = 99.99):
        """
        Args:
            sla_target: 목표 가용성 (%)
        """
        self.sla_target = sla_target
        self.incidents: List[Incident] = []

    def calculate_availability(self, period_start: datetime,
                               period_end: datetime) -> Dict:
        """
        기간별 가용성 계산
        """
        total_seconds = (period_end - period_start).total_seconds()
        downtime_seconds = 0

        for incident in self.incidents:
            # 기간 내 장애 시간 계산
            incident_start = max(incident.start_time, period_start)
            incident_end = min(incident.end_time, period_end)

            if incident_start < incident_end:
                downtime_seconds += (incident_end - incident_start).total_seconds()

        uptime_seconds = total_seconds - downtime_seconds
        availability = (uptime_seconds / total_seconds) * 100

        # 허용 중단 시간 (SLA 기준)
        allowed_downtime = total_seconds * (1 - self.sla_target / 100)

        return {
            'period_start': period_start.isoformat(),
            'period_end': period_end.isoformat(),
            'total_time_hours': total_seconds / 3600,
            'uptime_hours': uptime_seconds / 3600,
            'downtime_hours': downtime_seconds / 3600,
            'availability_percent': round(availability, 4),
            'sla_target': self.sla_target,
            'sla_met': availability >= self.sla_target,
            'allowed_downtime_hours': allowed_downtime / 3600,
            'downtime_budget_used_percent': round((downtime_seconds / allowed_downtime) * 100, 2)
        }

    def calculate_mttr(self, period_start: datetime,
                       period_end: datetime) -> Dict:
        """
        MTTR (Mean Time To Recovery) 계산
        """
        recovery_times = []
        for incident in self.incidents:
            if period_start <= incident.start_time <= period_end:
                recovery_time = (incident.end_time - incident.start_time).total_seconds() / 60
                recovery_times.append(recovery_time)

        if not recovery_times:
            return {'mttr_minutes': 0, 'incidents': 0}

        return {
            'mttr_minutes': round(statistics.mean(recovery_times), 2),
            'mttr_median': round(statistics.median(recovery_times), 2),
            'incidents': len(recovery_times),
            'max_recovery_minutes': max(recovery_times),
            'min_recovery_minutes': min(recovery_times)
        }

    def calculate_mtbf(self, period_start: datetime,
                       period_end: datetime) -> Dict:
        """
        MTBF (Mean Time Between Failures) 계산
        """
        sorted_incidents = sorted(
            [i for i in self.incidents if period_start <= i.start_time <= period_end],
            key=lambda x: x.start_time
        )

        if len(sorted_incidents) < 2:
            return {'mtbf_hours': None, 'intervals': 0}

        intervals = []
        for i in range(1, len(sorted_incidents)):
            interval = (sorted_incidents[i].start_time - sorted_incidents[i-1].end_time).total_seconds() / 3600
            intervals.append(interval)

        return {
            'mtbf_hours': round(statistics.mean(intervals), 2),
            'intervals': len(intervals),
            'max_interval_hours': max(intervals),
            'min_interval_hours': min(intervals)
        }

# 실무 예시: 월간 가용성 보고서
calculator = AvailabilityCalculator(sla_target=99.99)

# 장애 이력 추가
calculator.incidents = [
    Incident(
        start_time=datetime(2026, 3, 1, 10, 0),
        end_time=datetime(2026, 3, 1, 10, 15),
        severity='major',
        affected_service='API Gateway',
        root_cause='Memory leak'
    ),
    Incident(
        start_time=datetime(2026, 3, 15, 14, 30),
        end_time=datetime(2026, 3, 15, 14, 35),
        severity='minor',
        affected_service='Database',
        root_cause='Connection pool exhaustion'
    ),
]

# 3월 가용성 계산
report = calculator.calculate_availability(
    period_start=datetime(2026, 3, 1),
    period_end=datetime(2026, 4, 1)
)
print(f"가용성: {report['availability_percent']}%")
print(f"SLA 충족: {'예' if report['sla_met'] else '아니오'}")
print(f"다운타임 예산 사용: {report['downtime_budget_used_percent']}%")

# MTTR/MTBF 계산
mttr = calculator.calculate_mttr(datetime(2026, 3, 1), datetime(2026, 4, 1))
mtbf = calculator.calculate_mtbf(datetime(2026, 3, 1), datetime(2026, 4, 1))
print(f"MTTR: {mttr['mttr_minutes']}분")
print(f"MTBF: {mtbf['mtbf_hours']}시간")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 비교표 1: HA 아키텍처 패턴 비교

| 구분 | Active-Standby | Active-Active | Multi-Site Active-Active |
|------|----------------|---------------|--------------------------|
| **구성** | 1대 운영, 1대 대기 | 2대 동시 운영 | 2개 데이터센터 동시 운영 |
| **자원 활용률** | 50% (낮음) | 100% | 100% |
| **페일오버 시간** | 60-300초 | 즉시 (0초) | 즉시 (0초) |
| **복잡도** | 낮음 | 중간 | 높음 |
| **비용** | 중간 | 중간 | 높음 |
| **RTO** | 1-5분 | 0초 | 0초 |
| **RPO** | 0 (동기복제) | 0 | 0-5분 (비동기) |
| **적용 사례** | DB, Legacy | 웹서버, API | 전자상거래, 금융 |

### 비교표 2: DDoS 방어 기술 비교

| 구분 | Rate Limiting | Scrubbing Center | Anycast | CDN |
|------|---------------|------------------|---------|-----|
| **방어 규모** | 소규모 | 대규모 (Tbps) | 대규모 | 대규모 |
| **지연 시간** | <1ms | 10-50ms | <10ms | <5ms |
| **비용** | 낮음 | 높음 | 중간 | 중간 |
| **L7 공격** | 부분 | 완벽 | 제한적 | 완벽 |
| **대표 서비스** | Nginx, iptables | Cloudflare, Akamai | Cloudflare | CloudFront |

### 과목 융합 관점 분석

**1. 운영체제(OS) × 가용성**
- **프로세스 관리**: systemd 자동 재시작, Watchdog
- **메모리**: OOM Killer, Swap
- **스토리지**: RAID, LVM, Journaling FS

**2. 네트워크 × 가용성**
- **L2**: STP, LACP (Link Aggregation)
- **L3**: VRRP/HSRP, ECMP, Anycast
- **L7**: L4/L7 로드밸런서, GSLB

**3. 데이터베이스 × 가용성**
- **복제**: Master-Slave, Multi-Master
- **페일오버**: Automatic Failover, Manual Failover
- **백업**: Hot Backup, Cold Backup, Point-in-Time Recovery

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단 시나리오

**시나리오 1: 99.99% 가용성 달성 설계**

```
상황: 핀테크 서비스, 연간 중단 52.6분 이내 목표

[요구사항 분석]
- 연간 허용 중단: 52.6분
- 계획된 중단: 0분 (무중단 배포)
- 장애 중단: 52.6분 이내

[기술사적 의사결정]
┌─────────────────────────────────────────────────────────────────┐
│ [계층별 HA 설계]                                                 │
│                                                                 │
│ 1. DNS 계층:                                                     │
│    • Route53 Health Check + Failover                            │
│    • Multi-Region Active-Active                                 │
│                                                                 │
│ 2. 로드밸런서 계층:                                              │
│    • ALB Cross-Zone Load Balancing                              │
│    • Minimum 2 AZ, 2 ALB per AZ                                │
│                                                                 │
│ 3. 애플리케이션 계층:                                            │
│    • Auto Scaling: Min 4, Max 20                                │
│    • Blue-Green Deployment (무중단 배포)                        │
│    • Circuit Breaker (서킷 브레이커)                            │
│                                                                 │
│ 4. 데이터베이스 계층:                                            │
│    • RDS Multi-AZ (동기 복제)                                   │
│    • RPO: 0, RTO: 60초                                          │
│                                                                 │
│ 5. 캐시 계층:                                                    │
│    • ElastiCache Cluster Mode                                   │
│    • Automatic Failover 활성화                                  │
│                                                                 │
│ [장애 시나리오별 RTO]                                            │
│ • AZ 장애: 0초 (다른 AZ가 서비스)                                │
│ • 리전 장애: 60초 (DNS 페일오버)                                 │
│ • DB 장애: 60초 (Multi-AZ 페일오버)                              │
│ • 앱 장애: 30초 (오토스케일링 교체)                              │
└─────────────────────────────────────────────────────────────────┘
```

**시나리오 2: 재해 복구 (DR) 전략 수립**

```
상황: 서울 리전 전체 장애 대응

[DR 전략 옵션]
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ 전략 1: Backup & Restore                                        │
│ • 비용: 낮음 ($1,000/월)                                        │
│ • RTO: 24시간                                                   │
│ • RPO: 1시간                                                    │
│ • 적용: 개발/테스트 환경                                        │
│                                                                 │
│ 전략 2: Pilot Light                                             │
│ • 비용: 중간 ($5,000/월)                                        │
│ • RTO: 4시간                                                    │
│ • RPO: 15분                                                     │
│ • 적용: 비핵심 서비스                                           │
│                                                                 │
│ 전략 3: Warm Standby                                            │
│ • 비용: 높음 ($15,000/월)                                       │
│ • RTO: 1시간                                                    │
│ • RPO: 5분                                                      │
│ • 적용: 핵심 서비스                                             │
│                                                                 │
│ 전략 4: Multi-Site Active-Active                                │
│ • 비용: 매우 높음 ($50,000/월)                                  │
│ • RTO: 0분 (즉시)                                               │
│ • RPO: 0분 (실시간)                                             │
│ • 적용: 미션 크리티컬 (결제, 인증)                              │
│                                                                 │
│ [최종 의사결정]                                                  │
│ • 핵심 서비스 (결제): Multi-Site Active-Active                  │
│ • 일반 서비스: Warm Standby                                     │
│ • 개발/테스트: Backup & Restore                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 도입 시 고려사항 체크리스트

**기술적 고려사항**
- [ ] RTO/RPO 목표 설정 (서비스별)
- [ ] HA 아키텍처 패턴 선정
- [ ] 로드밸런서 알고리즘 선택 (Round Robin, Least Connection, IP Hash)
- [ ] 백업 주기 및 보관 기간
- [ ] 페일오버 테스트 계획

**운영/보안적 고려사항**
- [ ] Chaos Engineering (장애 주입 테스트)
- [ ] Runbook 작성 (장애 대응 매뉴얼)
- [ ] 모니터링 대시보드 구축
- [ ] 정기적 DR 훈련 (분기 1회)

**주의사항 및 안티패턴**

| 안티패턴 | 문제점 | 올바른 접근 |
|----------|--------|-------------|
| **단일 AZ** | AZ 장애 시 서비스 중단 | Multi-AZ 구성 |
| **수동 페일오버** | RTO 증가, 인적 오류 | 자동 페일오버 |
| **백업 미검증** | 복구 실패 가능성 | 정기적 복구 테스트 |
| **과도한 이중화** | 비용 증가, 복잡도 상승 | 비즈니스 영향도 기반 설계 |

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 구분 | 도입 전 | 도입 후 | 개선 효과 |
|------|---------|---------|-----------|
| **서비스 중단 시간** | 연 8.76시간 (99.9%) | 연 52.6분 (99.99%) | **10배 개선** |
| **장애 복구 시간 (MTTR)** | 4시간 | 15분 | **16배 단축** |
| **SLA 위반 페널티** | 연 5,000만 원 | 0원 | **100% 절감** |
| **고객 이탈률** | 3.2% | 0.8% | **75% 감소** |

### 미래 전망 및 진화 방향

**1. 사이버 레질리언스 (Cyber Resilience)**
- 공격을 받아도 서비스 지속 능력
- 저항성 + 흡수력 + 복구력 + 적응력
- NIST Cybersecurity Framework 2.0

**2. AI 기반 예측적 HA**
- ML로 장애 예측 및 선제 대응
- AIOps (Artificial Intelligence for IT Operations)
- 이상 징후 자동 감지

**3. 엣지 컴퓨팅 가용성**
- 지연 민감 서비스의 엣지 분산
- 5G MEC (Multi-access Edge Computing)
- 로컬 페일오버

### ※ 참고 표준/가이드

| 표준 | 내용 | 적용 범위 |
|------|------|-----------|
| **ISO/IEC 27031** | ICT 비즈니스 연속성 | 글로벌 |
| **ISO/IEC 22301** | 비즈니스 연속성 관리 | 글로벌 |
| **NIST SP 800-34** | IT 시스템 비상계획 | 미국 정부 |
| **PCI DSS Req.12** | 비즈니스 연속성 계획 | 금융 |
| **SOC 2** | 가용성 신뢰 서비스 기준 | 클라우드 |

---

## 📌 관련 개념 맵 (Knowledge Graph)

- [정보보안 3요소 (CIA Triad)](./1_cia_triad.md): 가용성을 포함한 보안 3대 속성
- [DDoS 공격 및 방어](../3_network/ddos.md): 가용성 위협 대응
- [TLS 1.3](../3_network/tls13.md): 전송 계층 가용성
- [재해 복구 (DR)](./dr_bcp.md): 재해 상황 가용성
- [로드밸런싱](../3_network/load_balancing.md): 트래픽 분산
- [오토스케일링](../6_cloud/auto_scaling.md): 자동 확장

---

## 👶 어린이를 위한 3줄 비유 설명

**🏪 24시간 편의점**
편의점은 밤낮없이 항상 열려 있어요. 언제 가도 과자를 살 수 있어서 참 좋아요.

**💡 비상등과 발전기**
병원에는 정전되면 켜지는 비상등이 있어요. 수술 중에 불이 꺼지면 큰일이니까요.

**🚗 예비 타이어**
자동차 트렁크에는 예비 타이어가 있어요. 타이어가 터져도 예비로 갈아 끼우면 계속 갈 수 있어요.

---

*최종 수정일: 2026-03-05*
*작성 기준: 정보통신기술사·컴퓨터응용시스템기술사 대비 심화 학습 자료*
