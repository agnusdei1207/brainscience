+++
weight = 25
title = "25. CFR (Change Failure Rate) — 변경 실패율"
date = "2026-04-29"
[extra]
categories = "studynote-devops-sre"
+++

## 0. 핵심 인사이트

> **핵심**: CFR (Change Failure Rate, 변경 실패율)은 DORA (DevOps Research and Assessment, 데브옵스 연구·평가) 4대 핵심 메트릭 중 하나로, "전체 배포 건수 대비 서비스 장애·롤백·핫픽스를 유발한 배포의 비율"을 측정하여 배포 프로세스의 안정성을 정량화한다.
> **비유**: CFR은 비행기 이착륙 성공률이다. 비행기가 얼마나 자주 뜨고 내리느냐(배포 빈도)보다, 사고 없이 안전하게 착륙하느냐(CFR)가 항공사(서비스)의 신뢰성을 결정한다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

```text
┌──────────────────────────────────────────────────────────┐
│        DORA 4대 메트릭                                     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  처리량(Throughput):                                      │
│  1. Deployment Frequency (배포 빈도) — 얼마나 자주?        │
│  2. Lead Time for Changes (변경 리드타임) — 얼마나 빨리?   │
│                                                          │
│  안정성(Stability):                                       │
│  3. CFR (Change Failure Rate) — 얼마나 안전하게?           │
│  4. MTTR (Mean Time to Recover) — 장애 시 얼마나 빨리?     │
│                                                          │
│  ★ CFR = 실패 배포 수 / 전체 배포 수 × 100%               │
└──────────────────────────────────────────────────────────┘
```

### DORA 성과 수준별 CFR 벤치마크

| 성과 수준 | CFR | 설명 |
|:---|:---|:---|
| **Elite** | 0~15% | 자동화 테스트, 점진적 배포 성숙 |
| **High** | 0~15% | Elite와 동일 범위 |
| **Medium** | 16~30% | 자동화 부분 도입 |
| **Low** | 46~60%+ | 수동 배포, 테스트 부족 |

---

## 2. 구성요소

### CFR 감소를 위한 배포 전략

```text
1. 자동화 테스트 피라미드
   E2E Tests (적음)
   Integration Tests
   Unit Tests (많음) → 빠른 피드백, CFR 감소

2. 점진적 배포 (Progressive Delivery)
   Blue-Green: 전체 트래픽을 신규 버전으로 한 번에 전환
                → 문제 시 즉시 롤백
   Canary:     5% → 25% → 100% 단계적 트래픽 전환
                → 소수 사용자에서 문제 조기 탐지

3. Feature Flag
   배포(Deploy) ≠ 릴리스(Release)
   코드는 배포하되 Feature Flag로 ON/OFF
   → 문제 시 코드 배포 없이 플래그만 OFF
```

---

## 3. 구조 및 원리

**핵심 조건**: 공유된 목표, 자동화된 피드백 루프, 측정 가능한 성과 지표가 동시에 작동해야 문화가 실행력으로 전환된다.

동작 순서:
1. 공동 목표를 정의해 개발·운영·보안의 KPI를 고객 가치 중심으로 정렬한다.
2. 작업 흐름을 시각화해 병목과 대기 시간을 식별하고 제거한다.
3. 자동화와 표준화를 도입해 사람 의존 절차를 축소한다.
4. 운영 데이터와 회고 결과를 다시 개발 계획에 반영해 학습 루프를 닫는다.

```text
[전체 트래픽 100%]
         │
  ┌──────┴──────┐
  │ Stable v1.0 │  → 95% 트래픽
  └─────────────┘

  ┌──────────────┐
  │ Canary v1.1  │  → 5% 트래픽 (모니터링 중)
  └──────────────┘
         │
   에러율 증가 감지
         │
  자동 롤백 또는 계속 진행
```

| DORA 메트릭 | 측정 대상 | CFR과의 관계 |
|:---|:---|:---|
| **배포 빈도** | 단위 시간당 배포 횟수 | 높은 빈도 + 낮은 CFR = Elite 팀 |
| **리드 타임** | 커밋→배포 소요 시간 | 짧은 리드타임 → 빠른 피드백 → CFR↓ |
| **CFR** | 실패 배포 비율 | 안정성의 핵심 지표 |
| **MTTR** | 장애 복구 평균 시간 | CFR 높아도 MTTR 낮으면 영향 최소화 |

---

## 4. 비교 및 연결

### CFR 측정 및 개선 사이클

```python
def calculate_cfr(deployments, incidents):
    """
    deployments: 전체 배포 목록 (타임스탬프, 버전)
    incidents: 배포 관련 장애 목록 (타임스탬프, 관련 배포)
    """
    failed_deployments = set()
    for incident in incidents:
        related = [d for d in deployments
                   if abs(d.timestamp - incident.timestamp) < 3600]
        failed_deployments.update(related)

    cfr = len(failed_deployments) / len(deployments) * 100
    return cfr  # Elite 목표: 15% 이하
```

### 안티패턴
- CFR을 낮추기 위해 배포 빈도를 줄이는 안티패턴. 배포 빈도 감소 → 배포 당 변경 크기 증가 → 오히려 CFR 상승(큰 변경 = 높은 위험). 빈번하고 작은 변경(Small Batches)이 CFR을 낮추는 올바른 접근이다.

---

## 5. 실무 적용 및 판단

| 기대효과 | 내용 |
|:---|:---|
| **배포 안정성** | 서비스 장애 유발 배포 감소 |
| **팀 신뢰도** | 낮은 CFR = 배포에 대한 공포 감소 |
| **비즈니스 가치** | 빠르고 안전한 기능 출시 |

DORA 메트릭은 SPACE (Satisfaction, Performance, Activity, Communication, Efficiency) 프레임워크와 결합하여 개발자 경험(Developer Experience, DevEx)을 종합적으로 측정하는 방향으로 발전하고 있다. CFR은 단순 KPI가 아닌 팀 심리적 안전감과 기술적 역량의 복합 지표다.

---

## 6. 기대효과 및 결론

CFR (Change Failure Rate) — 변경 실패율을(를) 도입하면 자동화와 표준화를 통해 속도·안정성·가시성의 균형을 높일 수 있다. 다만 효과를 얻으려면 공유된 목표, 자동화된 피드백 루프, 측정 가능한 성과 지표가 동시에 작동해야 문화가 실행력으로 전환된다는 전제가 충족되어야 하며, 도구만 도입하고 운영 원칙을 바꾸지 않으면 기대 효과가 빠르게 한계에 부딪힌다.

결론적으로 CFR (Change Failure Rate) — 변경 실패율은(는) 개별 기능이 아니라 운영 체계 전체의 품질을 재정렬하는 방식이며, 향후에는 플랫폼화·정책화·AI 기반 최적화와 결합해 더 높은 수준의 자동 운영으로 확장된다.

---

## 7. 발전 흐름도

```text
[수동 배포 — 높은 CFR, 낮은 배포 빈도]
    │
    ▼
[CI/CD 자동화 — 테스트 자동화로 CFR 감소]
    │
    ▼
[점진적 배포 (Canary/Blue-Green) — 리스크 최소화]
    │
    ▼
[Feature Flag — 배포와 릴리스 완전 분리]
    │
    ▼
[DORA 메트릭 기반 Elite DevOps — CFR 0~15%]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **DORA 4 메트릭** | CFR은 안정성 지표 중 하나 |
| **Canary/Blue-Green 배포** | CFR 감소를 위한 점진적 배포 전략 |
| **Feature Flag** | 배포와 릴리스 분리로 CFR 영향 최소화 |
| **MTTR** | CFR과 쌍으로 분석하는 복구 시간 지표 |
| **자동화 테스트** | CFR 감소의 근본적 해결책 |
