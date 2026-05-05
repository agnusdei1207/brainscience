+++
weight = 176
title = "RTO (Recovery Time Objective)"
date = "2024-03-20"
[extra]
categories = ["it-management", "bcp-drs"]
+++
## 0. 핵심 인사이트

> |

> 📝 모범 답안

1. 재난 발생 시 서비스 중단(Downtime)을 감내할 수 있는 최대 허용 시간으로, 서비스의 가용성 복구 목표를 의미합니다.
2. 비즈니스 영향 분석(BIA)을 통해 결정되며, RTO가 짧을수록 복구 비용(CAPEX/OPEX)은 기하급수적으로 증가합니다.
3. DRS(재해복구시스템) 구축 시 복구 체계(Mirror, Hot, Warm, Cold)를 결정하는 가장 핵심적인 지표입니다.

### 1. 개요 및 필요성
현대 IT 환경에서 시스템 장애는 단순한 기술적 문제가 아닌 비즈니스의 생존 문제입니다. RTO(Recovery Time Objective, 복구 목표 시간)는 사고 발생 시점부터 서비스가 다시 정상적으로 가동될 때까지 걸리는 목표 시간을 정의합니다. 이는 업무 연속성 계획(BCP)의 핵심 정량 지표로서, 기업이 재난 상황에서도 고객 신뢰와 법적 준거성을 유지할 수 있도록 하는 기준점이 됩니다.

### 2. 구성요소

```text
[ Timeline of Disaster Recovery ]
Disaster Occurs             RTO (Target)             Service Resumed
      | <----------------------------------------------      v                                                  v
------+--------------------------------------------------+-------------> (Time)
      |          DR Execution (Recover Activities)        |
      | - Disaster Declaration                           |
      | - Infrastructure Provisioning                    |
      | - Data Restoration & Service Start              |
```

**Bilingual Key Components:**
- **가용성 목표 (Availability Goal):** 서비스가 다시 '살아나는(Up and Running)' 속도를 의미합니다.
- **재해 복구 선언 (DR Declaration):** 사고 인지 후 실제 DR 복구를 시작하기로 결정하는 소요 시간도 RTO에 포함될 수 있습니다.
- **복구 자동화 (Recovery Automation):** RTO 단축을 위해 클라우드 기반 인프라 배포(IaC) 기술이 활용됩니다.

### 3. 구조 및 동작 원리

| 비교 항목 | RTO (Recovery Time Objective) | RPO (Recovery Point Objective) |
| :--- | :--- | :--- |
| **핵심 질문** | "얼마나 빨리 서비스를 복구할 것인가?" | "얼마나 많은 데이터를 잃어도 되는가?" |
| **측정 기준** | 시간 (Time) - 분, 시간, 일 단위 | 시점 (Point) - 최종 백업 시점 |
| **관심 영역** | 서비스 중단 (Downtime) 관리 | 데이터 유실 (Data Loss) 관리 |
| **주요 기술** | High Availability, Clustering, IaC | Backup, Data Replication (Sync/Async) |

### 4. 비교 및 트레이드오프
기술사로서 RTO는 '최소 비용으로 최대 효과'를 내는 균형점(Balance Point)을 찾는 것이 핵심입니다.
- **전략적 의사결정:** 모든 시스템의 RTO를 0으로 설정하면 비용 감당이 불가능합니다. 시스템의 중요도(Class)에 따라 핵심 업무는 미러 사이트(RTO=0~수분), 주변 업무는 콜드 사이트(RTO=수일)로 차등화해야 합니다.
- **감리 주안점:** RTO 수치 설정이 실제 비즈니스 가용성 요구사항을 반영하고 있는지(BIA 적정성), 그리고 실제 모의 훈련을 통해 선언된 RTO 내에 복구가 가능한지 실효성을 검증해야 합니다.

### 5. 실무 적용 및 최적화 기법
RTO는 기업의 위기 관리 역량을 나타내는 지표입니다. 최근에는 클라우드 네이티브 기술과 멀티 리전 아키텍처를 통해 과거 수억 원이 들던 실시간 복구(RTO=0)를 보다 경제적으로 달성하고 있습니다. 향후 AI 기반 자동 장애 탐지 및 복구 시스템이 고도화됨에 따라 RTO는 점차 '즉각적 가용성(Instant Availability)'으로 진화할 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** BCP (Business Continuity Planning), DRS (Disaster Recovery System)
- **하위 개념:** Mirror/Hot/Warm/Cold Site, Recovery Time
- **연관 개념:** RPO, BIA (Business Impact Analysis), SLA, High Availability

### 👶 어린이를 위한 3줄 비유 설명
1. **RTO**는 자전거를 타다가 넘어졌을 때, "얼마나 빨리 다시 일어나서 탈 수 있느냐"를 정하는 시간이에요.
2. 무릎 치료(복구)를 5분 안에 끝내고 다시 달릴지, 아니면 1시간 동안 쉴지 미리 약속하는 거예요.
3. 빨리 일어나고 싶을수록 비싼 약과 반창고를 미리 준비해 두어야 한답니다!
