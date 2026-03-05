+++
title = "451. MTTR (Mean Time To Repair)"
description = "평균 수리 시간 - 시스템 복구 능력의 핵심 지표"
date = "2026-03-05"
[taxonomies]
tags = ["MTTR", "Mean Time To Repair", "복구시간", "Serviceability", "RTO"]
categories = ["studynotes-1_computer_architecture"]
+++

# 451. MTTR (Mean Time To Repair, 평균 수리 시간)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MTTR은 시스템 고장 발생 후 정상 상태로 복구될 때까지의 평균 소요 시간으로, 고장 감지·진단·수리·검증 단계를 포함하며 Serviceability(유지보수성)의 핵심 정량 지표이다.
> 2. **가치**: MTTR 단축은 가용성 향상에 직접 기여하는데, MTBF가 같을 때 MTTR 1시간→30분 감소 시 가용성이 99.99%→99.995%로 향상되어 연간 다운타임이 52분→26분으로 절반 감소한다.
> 3. **융합**: MTTR은 RTO(Recovery Time Objective)와 밀접히 연관되며, 자동화된 페일오버, 컨테이너 오케스트레이션, IaC(Infrastructure as Code) 등의 DevOps 실천을 통해 획기적 단축 가능하다.

---

### I. 개요 (Context & Background)

#### 개념 정의

**MTTR(Mean Time To Repair, 평균 수리 시간)**는 시스템 고장이 발생한 시점부터 수리가 완료되어 정상 서비스가 재개될 때까지의 평균 시간을 의미한다. MTTR은 단순히 물리적 수리 시간뿐만 아니라 고장 감지, 진단, 부품 조달, 수리, 테스트, 서비스 재개까지의 전체 시간을 포함한다.

```
┌─────────────────────────────────────────────────────────────────┐
│                     MTTR 구성 요소                              │
└─────────────────────────────────────────────────────────────────┘

  고장 발생                                                 정상 복구
     │                                                        │
     ▼                                                        ▼
  ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐
  │감지  │──▶│진단  │──▶│조달  │──▶│수리  │──▶│테스트│──▶│재개  │
  │Detect│   │Diag  │   │Logis-│   │Repair│   │Test  │   │Resume│
  │      │   │      │   │tics  │   │      │   │      │   │      │
  └──────┘   └──────┘   └──────┘   └──────┘   └──────┘   └──────┘
     │           │          │          │          │          │
     ▼           ▼          ▼          ▼          ▼          ▼
  · 알림      · 로그     · 부품     · 교체     · 기능     · 서비스
    수신        분석       주문       작업        검증       재시작
  · 장애      · 원인     · 배송     · 설정     · 성능     · 트래픽
    확인        파악       대기       변경        테스트     복원

  ─────────────────────────────────────────────────────────────
                       전체가 MTTR에 포함
  ─────────────────────────────────────────────────────────────
```

**MTTR 세분화:**

| 구성 요소 | 영문 | 설명 | 일반적 소요시간 |
|-----------|------|------|-----------------|
| **MTTD** | Mean Time To Detect | 고장 감지 시간 | 5분~1시간 |
| **MTTA** | Mean Time To Acknowledge | 장애 인지 및 대응 시작 | 5~30분 |
| **MTTDi** | Mean Time To Diagnose | 원인 진단 시간 | 15분~4시간 |
| **MTTR** | Mean Time To Repair | 물리적 수리/복구 시간 | 30분~8시간 |
| **MTTV** | Mean Time To Verify | 복구 검증 시간 | 15분~1시간 |

#### 비유

> **MTTR은 "병원 응급실에서 환자가 도착해서 퇴원할 때까지의 시간"과 같다.**
>
> 1. **감지**: 환자가 응급실에 도착 (환자가 스스로 오거나 구급차가 데려옴)
> 2. **진단**: 의사가 검진하고 무슨 병인지 파악 (혈액검사, X-ray 등)
> 3. **조달**: 필요한 약이나 수술 도구 준비 (약국에서 약 가져오기)
> 4. **수리**: 실제 치료/수술 진행
> 5. **검증**: 회복 상태 확인 (증상 사라졌는지 검사)
> 6. **재개**: 퇴원해서 일상생활 복귀
>
> MTTR이 짧을수록 좋은 병원이듯, IT 시스템에서도 MTTR이 짧을수록 서비스 중단 시간이 줄어든다.

#### 등장 배경 및 발전 과정

1. **1960-70년대: 메인프레임 시대**
   - 수리 시간 = 엔지니어 현장 도착 + 진단 + 부품 교체
   - MTTR 수시간~수일 소요

2. **1980-90년대: 클라이언트-서버 시대**
   - 원격 진단 도구, 예비 부품 비축
   - MTTR 수시간 수준으로 개선

3. **2000년대: 인터넷 데이터센터**
   - 핫스왑, 모듈화, 자동화된 모니터링
   - MTTR 1~4시간 수준

4. **2010년대~현재: 클라우드 및 DevOps**
   - 자동 페일오버, Blue-Green 배포, Infrastructure as Code
   - MTTR 분 단위 (심지어 초 단위) 달성

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### MTTR 계산 공식

```
┌─────────────────────────────────────────────────────────────────┐
│                     MTTR 핵심 공식                              │
└─────────────────────────────────────────────────────────────────┘

기본 공식:
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│         Σ(모든 수리 시간)                                      │
│  MTTR = ─────────────────                                      │
│           고장 횟수                                            │
│                                                                │
└────────────────────────────────────────────────────────────────┘

가용성과의 관계:
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│                    MTBF                                        │
│  Availability = ───────────────                                │
│                  MTBF + MTTR                                   │
│                                                                │
│  ∴ MTTR 감소 → Availability 증가                               │
│                                                                │
└────────────────────────────────────────────────────────────────┘

예시 계산:
┌────────────────────────────────────────────────────────────────┐
│ 고장 #1: 수리시간 2시간                                        │
│ 고장 #2: 수리시간 4시간                                        │
│ 고장 #3: 수리시간 1시간                                        │
│ 고장 #4: 수리시간 3시간                                        │
│                                                                │
│ MTTR = (2+4+1+3) / 4 = 2.5시간                                 │
└────────────────────────────────────────────────────────────────┘
```

#### MTTR 단계별 상세 분석

```
┌─────────────────────────────────────────────────────────────────┐
│               MTTR 단계별 상세 분석                             │
└─────────────────────────────────────────────────────────────────┘

Stage 1: 고장 감지 (Failure Detection)
┌────────────────────────────────────────────────────────────────┐
│ 목표: 고장 발생 후 최대한 빨리 인지                             │
│                                                                │
│ 기술:                                                          │
│ · Health Check (HTTP GET /health every 10s)                   │
│ · Heartbeat (TCP keepalive, application ping)                 │
│ · SNMP Trap / Syslog                                          │
│ · APM (Application Performance Monitoring)                    │
│ · Synthetic Monitoring (외부에서 주기적 호출)                  │
│                                                                │
│ 소요시간: 1~5분 (자동화된 경우)                                │
│          30분~수시간 (수동인 경우)                             │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
Stage 2: 장애 인지 및 에스컬레이션 (Acknowledgment & Escalation)
┌────────────────────────────────────────────────────────────────┐
│ 목표: 담당자에게 장애 알림 및 대응 체계 가동                    │
│                                                                │
│ 기술:                                                          │
│ · PagerDuty, Opsgenie 등 On-call 시스템                       │
│ · 자동 에스컬레이션 (15분 내 응답 없으면 상급자 호출)           │
│ · War Room 구성 (Slack/Teams 채널 자동 생성)                  │
│                                                                │
│ 소요시간: 5~15분                                               │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
Stage 3: 원인 진단 (Root Cause Diagnosis)
┌────────────────────────────────────────────────────────────────┐
│ 목표: 무엇이 고장 났는지, 왜 고장 났는지 파악                   │
│                                                                │
│ 기술:                                                          │
│ · 로그 분석 (ELK Stack, Splunk)                               │
│ · 메트릭 분석 (Prometheus, Grafana)                           │
│ · 트레이싱 (Jaeger, Zipkin)                                   │
│ · 디버깅 도구 (gdb, pprof, jstack)                            │
│ · Runbook 참조                                                │
│                                                                │
│ 소요시간: 15분~4시간                                           │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
Stage 4: 수리/복구 (Repair/Recovery)
┌────────────────────────────────────────────────────────────────┐
│ 목표: 실제 문제 해결                                            │
│                                                                │
│ 유형별 수리 방법:                                               │
│ ┌────────────────┬───────────────────────────────────────────┐ │
│ │ 장애 유형       │ 수리 방법                                 │ │
│ ├────────────────┼───────────────────────────────────────────┤ │
│ │ HW 고장        │ 핫스왑, 부품 교체, 서버 교체              │ │
│ │ SW 버그        │ 롤백, 핫픽스 배포                         │ │
│ │ 설정 오류      │ 설정 변경, IaC 재적용                     │ │
│ │ 용량 부족      │ 스케일 아웃, 리소스 추가                  │ │
│ │ 보안 공격      │ 격리, 패치, 방화벽 규칙 변경              │ │
│ └────────────────┴───────────────────────────────────────────┘ │
│                                                                │
│ 소요시간: 30분~8시간                                           │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
Stage 5: 검증 (Verification)
┌────────────────────────────────────────────────────────────────┐
│ 목표: 수리가 제대로 되었는지 확인                               │
│                                                                │
│ 기술:                                                          │
│ · Smoke Test (기본 기능 테스트)                               │
│ · Integration Test                                            │
│ · Load Test (소규모)                                          │
│ · Canary Deployment (일부 트래픽만)                           │
│                                                                │
│ 소요시간: 15분~1시간                                           │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
Stage 6: 서비스 재개 (Service Resumption)
┌────────────────────────────────────────────────────────────────┐
│ 목표: 정상 서비스로 복귀                                        │
│                                                                │
│ 기술:                                                          │
│ · DNS 페일오버 복구                                            │
│ · 로드밸런서 트래픽 복원                                       │
│ · Auto Scaling 그룹 복구                                       │
│ · 모니터링 강화 (Post-incident)                               │
│                                                                │
│ 소요시간: 5~30분                                               │
└────────────────────────────────────────────────────────────────┘
```

#### MTTR 단축 기술 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│               MTTR 단축을 위한 아키텍처 패턴                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │  모니터링   │────▶│  자동화     │────▶│  오케스트   │       │
│  │ Monitoring  │     │ Automation  │     │ Orchestration│       │
│  └─────────────┘     └─────────────┘     └─────────────┘       │
│        │                   │                   │                │
│        ▼                   ▼                   ▼                │
│  · Prometheus         · Ansible           · Kubernetes        │
│  · Grafana            · Terraform         · Docker Swarm      │
│  · Datadog            · Chef/Puppet       · Nomad             │
│  · New Relic          · SaltStack                             │
│                                                                 │
│  ═══════════════════════════════════════════════════════════   │
│                                                                 │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │  이중화     │     │  롤백       │     │  Runbook    │       │
│  │ Redundancy  │     │ Rollback    │     │ Runbooks    │       │
│  └─────────────┘     └─────────────┘     └─────────────┘       │
│        │                   │                   │                │
│        ▼                   ▼                   ▼                │
│  · Active-Passive     · Blue-Green        · 표준 절차서       │
│  · Active-Active      · Canary            · 의사결정 트리     │
│  · Multi-AZ           · GitOps            · 자동 실행 스크립트 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

                     MTTR 단축 효과
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  수동 복구               반자동 복구             완전 자동화    │
│  (Manual)                (Semi-auto)            (Full-auto)     │
│                                                                 │
│  MTTR: 4~8시간           MTTR: 30분~2시간        MTTR: 1~5분    │
│    │                        │                       │           │
│    └────────────────────────┴───────────────────────┘           │
│              ▼                    ▼                ▼            │
│         가용성 99.9%         가용성 99.99%      가용성 99.999%  │
│         (8.76시간/년)       (52분/년)         (5분/년)         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 핵심 코드: 자동 복구 시스템 예시

```python
#!/usr/bin/env python3
"""
Auto-Recovery System for MTTR Minimization
- Kubernetes-style self-healing pattern
- Health check + automatic failover
"""

import time
import logging
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Callable
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

@dataclass
class ServiceInstance:
    id: str
    host: str
    port: int
    status: HealthStatus = HealthStatus.UNKNOWN
    last_check: Optional[datetime] = None
    consecutive_failures: int = 0

class AutoRecoveryManager:
    """
    자동 복구 관리자
    - Health check 수행
    - 장애 감지 시 자동 조치
    - MTTR 최소화
    """

    def __init__(
        self,
        instances: List[ServiceInstance],
        health_check_fn: Callable[[ServiceInstance], bool],
        recovery_fn: Callable[[ServiceInstance], bool],
        max_failures: int = 3,
        check_interval: int = 10,
    ):
        self.instances = instances
        self.health_check_fn = health_check_fn
        self.recovery_fn = recovery_fn
        self.max_failures = max_failures
        self.check_interval = check_interval

        # MTTR 측정용
        self.repair_times: List[float] = []
        self.failure_detected_at: Optional[datetime] = None

    def health_check(self, instance: ServiceInstance) -> bool:
        """개별 인스턴스 헬스 체크"""
        try:
            is_healthy = self.health_check_fn(instance)
            instance.status = HealthStatus.HEALTHY if is_healthy else HealthStatus.UNHEALTHY
            instance.last_check = datetime.now()

            if is_healthy:
                instance.consecutive_failures = 0
            else:
                instance.consecutive_failures += 1
                logger.warning(
                    f"Instance {instance.id} unhealthy "
                    f"(failures: {instance.consecutive_failures})"
                )

            return is_healthy

        except Exception as e:
            logger.error(f"Health check failed for {instance.id}: {e}")
            instance.status = HealthStatus.UNKNOWN
            instance.consecutive_failures += 1
            return False

    def is_instance_failed(self, instance: ServiceInstance) -> bool:
        """인스턴스 장애 판정"""
        return instance.consecutive_failures >= self.max_failures

    def recover_instance(self, instance: ServiceInstance) -> bool:
        """
        인스턴스 복구 시도
        MTTR 측정 포함
        """
        # MTTR 측정 시작
        if self.failure_detected_at is None:
            self.failure_detected_at = datetime.now()

        logger.info(f"Starting recovery for instance {instance.id}")

        try:
            recovery_success = self.recovery_fn(instance)

            if recovery_success:
                # 복구 성공 - MTTR 기록
                repair_time = (datetime.now() - self.failure_detected_at).total_seconds()
                self.repair_times.append(repair_time)
                self.failure_detected_at = None

                instance.status = HealthStatus.HEALTHY
                instance.consecutive_failures = 0

                logger.info(
                    f"Instance {instance.id} recovered successfully "
                    f"(repair time: {repair_time:.1f}s)"
                )
                return True
            else:
                logger.error(f"Recovery failed for instance {instance.id}")
                return False

        except Exception as e:
            logger.error(f"Recovery exception for {instance.id}: {e}")
            return False

    def get_mttr(self) -> Optional[float]:
        """평균 MTTR 계산"""
        if not self.repair_times:
            return None
        return sum(self.repair_times) / len(self.repair_times)

    def run_health_checks(self) -> dict:
        """모든 인스턴스 헬스 체크"""
        results = {
            "healthy": 0,
            "unhealthy": 0,
            "unknown": 0,
            "recovering": 0,
        }

        for instance in self.instances:
            if instance.status == HealthStatus.HEALTHY:
                # 정상 인스턴스도 주기적 체크
                self.health_check(instance)

            if self.is_instance_failed(instance):
                # 장애 판정 → 복구 시도
                results["recovering"] += 1
                self.recover_instance(instance)
            else:
                results[instance.status.value] += 1

        return results

    def run_forever(self):
        """무한 루프로 헬스 체크 수행"""
        logger.info("Starting Auto-Recovery Manager")

        while True:
            try:
                results = self.run_health_checks()
                mttr = self.get_mttr()

                logger.info(
                    f"Health check complete - "
                    f"Healthy: {results['healthy']}, "
                    f"Unhealthy: {results['unhealthy']}, "
                    f"Recovering: {results['recovering']}, "
                    f"MTTR: {mttr:.1f}s" if mttr else "MTTR: N/A"
                )

                time.sleep(self.check_interval)

            except KeyboardInterrupt:
                logger.info("Shutting down...")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                time.sleep(self.check_interval)

# 사용 예시
if __name__ == "__main__":
    # 샘플 인스턴스
    instances = [
        ServiceInstance(id="app-1", host="10.0.1.1", port=8080),
        ServiceInstance(id="app-2", host="10.0.1.2", port=8080),
        ServiceInstance(id="app-3", host="10.0.1.3", port=8080),
    ]

    # 샘플 헬스 체크 함수 (실제로는 HTTP 요청 등)
    def health_check(instance: ServiceInstance) -> bool:
        import random
        # 90% 확률로 정상
        return random.random() < 0.9

    # 샘플 복구 함수 (실제로는 재시작, 재배포 등)
    def recover(instance: ServiceInstance) -> bool:
        logger.info(f"Restarting service on {instance.host}...")
        time.sleep(5)  # 재시작 시뮬레이션
        return True

    # 자동 복구 매니저 실행
    manager = AutoRecoveryManager(
        instances=instances,
        health_check_fn=health_check,
        recovery_fn=recover,
        max_failures=3,
        check_interval=5,
    )

    manager.run_forever()
```

---

### III. 융합 비교 및 다각도 분석

#### MTTR vs. RTO

```
┌─────────────────────────────────────────────────────────────────┐
│              MTTR vs. RTO 비교                                   │
└─────────────────────────────────────────────────────────────────┘

┌────────────┬────────────────────────────────────────────────────┐
│   용어     │                    설명                            │
├────────────┼────────────────────────────────────────────────────┤
│   MTTR     │ 실제 측정된 평균 수리 시간 (과거 데이터 기반)      │
│            │ Mean Time To Repair                                │
│            │ · 운영 메트릭 (Operational Metric)                 │
│            │ · 실제 복구 이력의 평균                            │
├────────────┼────────────────────────────────────────────────────┤
│   RTO      │ 목표 복구 시간 (비즈니스 요구사항 기반)            │
│            │ Recovery Time Objective                            │
│            │ · SLA 요구사항 (Requirement)                       │
│            │ · "이 시간 내에 복구해야 한다"                     │
└────────────┴────────────────────────────────────────────────────┘

관계:
· RTO ≥ MTTR 이어야 함 (RTO < MTTR 이면 SLA 위험)
· RTO - MTTR = 안전 여유 (Safety Margin)
· 실무: RTO를 MTTR의 1.5~2배로 설정 권장
```

#### 복구 유형별 MTTR 비교

| 복구 유형 | 설명 | MTTR | 복잡도 | 비용 |
|-----------|------|------|--------|------|
| **수동 복구** | 엔지니어가 직접 진단·수리 | 4~8시간 | 낮음 | 낮음 |
| **Runbook 기반** | 표준 절차서 따라 수행 | 1~2시간 | 중간 | 낮음 |
| **반자동화** | 스크립트로 일부 자동화 | 15~30분 | 중간 | 중간 |
| **완전 자동화** | Kubernetes Self-healing | 1~5분 | 높음 | 중간 |
| **Active-Active** | 트래픽 자동 분산 | < 1초 | 높음 | 높음 |

#### 과목 융합 분석

| 융합 과목 | MTTR 관점 | 적용 기술 |
|-----------|-----------|-----------|
| **OS** | 커널 패닉 복구, 프로세스 재시작 | systemd, supervisor |
| **네트워크** | 링크 장애 복구, 라우팅 수렴 | BFD, Fast Reroute |
| **DB** | 장애 조치, 복구 | replication failover, PITR |
| **클라우드** | Auto Healing, Auto Scaling | ELB health check, ASG |
| **보안** | 침해 사고 대응 | incident response playbook |

---

### IV. 실무 적용 및 기술사적 판단

#### 실무 시나리오

**시나리오 1: E-커머스 서비스 MTTR 개선 프로젝트**
```
Before:
· 장애 감지: 모니터링 툴 알림 → 평균 10분
· 담당자 도착: On-call 엔지니어 → 평균 15분
· 원인 파악: 로그 분석 → 평균 30분
· 수리: 코드 롤백 → 평균 20분
· 검증: Smoke test → 평균 10분
· ─────────────────────────────────────
· 총 MTTR: 약 85분

After (자동화 도입):
· 장애 감지: 자동 (Prometheus Alert) → 1분
· 담당자 도착: PagerDuty 자동 호출 → 5분
· 원인 파악: 자동 진단 (Runbook) → 5분
· 수리: 자동 롤백 (ArgoCD) → 3분
· 검증: 자동 Smoke test → 2분
· ─────────────────────────────────────
· 총 MTTR: 약 16분 (80% 단축)

비용 대비 효과:
· 자동화 도구 도입 비용: 5,000만 원
· 연간 다운타임 감소: 85분 × 12회 - 16분 × 12회 = 828분
· 매출 손실 방지 (분당 100만 원): 8억 2,800만 원
· ROI: 16.5배
```

**시나리오 2: DB 장애 자동 페일오버**
```
구성: MySQL Primary-Replica (2노드)

Before (수동 페일오버):
· 장애 감지: 5분
· 엔지니어 확인: 15분
· 수동 페일오버 실행: 10분
· 애플리케이션 재시작: 5분
· MTTR: 35분

After (자동 페일오버 - Orchestrator):
· 장애 감지: 10초
· 자동 페일오버: 30초
· DNS/서비스 디스커버리 업데이트: 20초
· MTTR: 1분

개선 효과: MTTR 35분 → 1분 (97% 단축)
```

#### 도입 시 고려사항

```
□ 자동화 준비도 평가
  □ 모니터링 시스템 구축 상태
  □ 장애 패턴 분석 완료
  □ Runbook 작성 여부

□ 자동화 범위 결정
  □ 감지 → 자동
  □ 진단 → 반자동 (사람 확인)
  □ 복구 → 자동 (안전한 경우만)
  □ 검증 → 반자동

□ 안전장치 마련
  □ 자동 복구 실패 시 대응 절차
  □ 오작동 방지 (잘못된 자동 복구)
  □ Rate limiting (너무 잦은 복구 방지)

□ 측정 및 개선
  □ MTTR 대시보드 구축
  □ Post-mortem 프로세스
  □ 지속적 Runbook 개선
```

#### 안티패턴

```
❌ "무조건 자동화가 좋다"
   → 잘못된 자동화는 더 큰 장애 유발 가능

❌ "MTTR만 줄이면 된다"
   → MTBF도 함께 고려해야 (근본 원인 해결)

❌ "Runbook 없이 자동화"
   → 자동화 로직은 Runbook 기반으로 작성

❌ "모든 장애를 동일하게 처리"
   → 장애 유형별로 다른 복구 전략 필요
```

---

### V. 기대효과 및 결론

#### 정량적 기대효과

| 지표 | 개선 전 | 개선 후 | 향상률 |
|------|---------|---------|--------|
| MTTR | 85분 | 16분 | 81% 단축 |
| 연간 다운타임 | 17시간 | 3.2시간 | 81% 감소 |
| 가용성 | 99.8% | 99.96% | 0.16%p 향상 |
| SLA 달성률 | 92% | 99% | 7%p 향상 |

#### 미래 전망

1. **AI 기반 자동 진단**
   - LLM을 활용한 로그 분석 및 원인 추론
   - MTTR 50% 이상 추가 단축 기대

2. **Chaos Engineering 통합**
   - 사전에 장애 주입으로 복구 능력 검증
   - MTTR 예측 정확도 향상

#### 참고 표준

- **ITIL v4**: Incident Management
- **NIST SP 800-34**: Contingency Planning
- **ISO/IEC 27001**: A.17 Business Continuity

---

### 관련 개념 맵 (Knowledge Graph)

- [449. RAS](./1_ras.md) - 신뢰성, 가용성, 유지보수성 종합
- [450. MTBF](./2_mtbf.md) - 평균 무고장 시간
- [452. 가용성](./4_availability.md) - MTBF와 MTTR의 함수
- [457. 핫 스탠바이](./9_hot_standby.md) - MTTR 단축 핵심 기술
- [461. 워치독 타이머](./13_watchdog_timer.md) - 고장 자동 감지

---

### 어린이를 위한 3줄 비유 설명

**MTTR은 "장난감이 고장 났을 때 다시 가지고 놀 수 있을 때까지 걸리는 시간"이에요!**

1. 장난감 자동차가 고장 났어요! 아빠한테 말하고, 아빠가 어떤 부품이 고장 났는지 확인하고, 예비 부품을 찾아서 고치고, 다시 잘 되는지 확인하는 데 걸리는 시간이 바로 MTTR이에요.

2. MTTR이 짧으면 좋은 거예요! 1시간 만에 고치면 금방 다시 가지고 놀 수 있지만, 1주일이 걸리면 그동안 슬프게 장난감 없이 지내야 하니까요. 그래서 회사들은 MTTR을 줄이려고 노력해요.

3. MTTR을 줄이려면 미리 예비 부품을 준비해두고, 고치는 방법을 책에 적어두고, 고장 나면 바로 알 수 있게 해두면 돼요. 그러면 1시간 걸리던 게 10분으로 줄어들 수 있어요!
