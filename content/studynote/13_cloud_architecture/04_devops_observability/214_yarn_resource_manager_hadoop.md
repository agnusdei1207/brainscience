+++
weight = 214
title = "214. YARN (Yet Another Resource Negotiator)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: YARN(Yet Another Resource Negotiator)은 하둡 클러스터의 CPU와 메모리를 중앙에서 조율하는 범용 리소스 관리자로, Hadoop 2.x에서 도입되어 MapReduce뿐 아니라 Spark·Flink·Tez 등 다양한 처리 엔진을 동일 클러스터에서 실행 가능하게 한다.
> **비유**: YARN은 다목적 스포츠 경기장과 같다. 야구 경기(MapReduce), 콘서트(Spark), 축구 경기(Flink)를 각각 별도 경기장에서 하는 대신, 하나의 경기장(YARN 클러스터)에서 스케줄을 조율하여 효율적으로 사용한다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

Hadoop 1.x의 JobTracker는 클러스터 전체의 리소스 관리와 모든 MapReduce 작업의 스케줄링을 혼자 담당했다. 이 단일 서버가 수만 개의 태스크를 추적하면서 두 가지 문제가 발생했다: **확장성 한계**(4,000 노드 이상에서 병목)와 **SPOF**(JobTracker 다운 = 전체 클러스터 정지).

더 큰 문제는 **플랫폼 고착화**였다. Hadoop 1.x에서는 MapReduce가 아닌 처리 엔진을 실행하려면 별도 클러스터를 만들어야 했다. Spark를 위한 별도 클러스터, MPI를 위한 별도 클러스터가 생기면서 자원 낭비와 관리 복잡성이 폭발했다.

YARN은 이 두 문제를 동시에 해결했다. 리소스 관리를 처리 엔진과 완전히 분리하여, 어떤 처리 엔진이든 YARN 위에서 실행될 수 있는 **범용 클러스터 운영 체제**가 됐다. 이 변화로 하나의 YARN 클러스터에서 MapReduce·Spark·Flink가 자원을 공유하며 실행될 수 있게 됐다.

---

## 2. 구성요소

### YARN 아키텍처

```
  ┌─────────────────────────────────────────────────────────────┐
  │                     YARN 아키텍처                             │
  ├─────────────────────────────────────────────────────────────┤
  │                                                              │
  │  클라이언트: spark-submit / hadoop jar                        │
  │       │ 애플리케이션 제출                                     │
  │       ▼                                                      │
  │  ┌───────────────────────────────────────────────────────┐  │
  │  │   ResourceManager (마스터, 전체 클러스터 관리)           │  │
  │  │                                                        │  │
  │  │   Scheduler ←─── 자원 할당 결정                        │  │
  │  │   ApplicationsManager ←─── AM 생명주기 관리            │  │
  │  └─────────────────────────┬─────────────────────────────┘  │
  │                             │ 자원 협상                      │
  │     ┌───────────────────────┼──────────────────────┐        │
  │     ▼                       ▼                      ▼        │
  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
  │  │  NodeManager │  │  NodeManager │  │  NodeManager │      │
  │  │  (노드1)     │  │  (노드2)     │  │  (노드3)     │      │
  │  │  Container:  │  │  Container:  │  │  Container:  │      │
  │  │  [AM]        │  │  [Task1]     │  │  [Task2]     │      │
  │  │  [Task3]     │  │  [Task4]     │  │  [Task5]     │      │
  │  └──────────────┘  └──────────────┘  └──────────────┘      │
  └─────────────────────────────────────────────────────────────┘
  
  ApplicationMaster (AM): 각 애플리케이션별로 생성
                          자신의 애플리케이션 태스크 스케줄링
```

### 핵심 컴포넌트 역할

| 컴포넌트 | 역할 |
|:---|:---|
| **ResourceManager** | 클러스터 전체 자원 관리, 애플리케이션 스케줄링 |
| **NodeManager** | 각 노드의 자원(CPU/메모리) 상태 보고, 컨테이너 실행 |
| **ApplicationMaster** | 애플리케이션별 생성, 해당 앱의 태스크 관리 |
| **Container** | YARN이 할당하는 자원 단위 (CPU 코어 + 메모리) |

### YARN 스케줄러 비교

| 스케줄러 | 방식 | 적합 상황 |
|:---|:---|:---|
| FIFO | 먼저 온 작업 우선 처리 | 단일 사용자, 단순 환경 |
| Capacity Scheduler | 팀별 자원 비율 보장 | 멀티 테넌트 기업 환경 (기본값) |
| Fair Scheduler | 모든 앱에 균등 자원 배분 | 다수의 소규모 작업 혼재 |

---

## 3. 구조 및 원리

**핵심 조건**: 변경 자동화와 운영 안정성은 별개가 아니라 하나의 루프이며, 빌드·검증·배포·관측·피드백이 끊기지 않아야 지속 개선이 가능하다.

동작 순서:
1. 변경 사항을 버전 관리 시스템에서 감지한다.
2. 빌드·테스트·보안 검증으로 변경의 품질을 빠르게 확인한다.
3. 승인된 산출물을 선언형 배포나 자동화 파이프라인으로 운영 환경에 반영한다.
4. 메트릭·로그·트레이스를 통해 실제 동작 결과를 관측한다.
5. 피드백을 다음 개선 주기에 연결해 반복적으로 신뢰성을 높인다.

### Hadoop 1.x vs 2.x YARN

| 항목 | Hadoop 1.x | Hadoop 2.x (YARN) |
|:---|:---|:---|
| 리소스 관리 | JobTracker (단일 서버) | ResourceManager (분리) |
| 작업 관리 | JobTracker (단일 서버) | ApplicationMaster (앱별 분리) |
| 지원 엔진 | MapReduce 전용 | MapReduce + Spark + Flink + 기타 |
| 확장성 | ~4,000 노드 | 수만 노드 |
| SPOF | ✅ JobTracker | ❌ RM HA 구성 가능 |

### YARN vs K8s 리소스 관리

| 항목 | YARN | Kubernetes |
|:---|:---|:---|
| 주 용도 | 빅데이터 처리 워크로드 | 컨테이너 기반 마이크로서비스 |
| 리소스 단위 | Container (CPU+메모리) | Pod |
| 생태계 | Hadoop 에코시스템 | 클라우드 네이티브 |
| 트렌드 | Spark on K8s로 이동 중 | 빅데이터 통합 가속 |

---

## 4. 비교 및 연결

**Capacity Scheduler 설정 예시**:
```xml
<!-- capacity-scheduler.xml -->
<property>
  <name>yarn.scheduler.capacity.root.queues</name>
  <value>analytics,engineering,default</value>
</property>
<property>
  <name>yarn.scheduler.capacity.root.analytics.capacity</name>
  <value>40</value>  <!-- 전체 클러스터의 40% 보장 -->
</property>
<property>
  <name>yarn.scheduler.capacity.root.engineering.capacity</name>
  <value>40</value>
</property>
<property>
  <name>yarn.scheduler.capacity.root.default.capacity</name>
  <value>20</value>
</property>
```

**Spark on YARN 실행**:
```bash
spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --num-executors 10 \
  --executor-cores 4 \
  --executor-memory 8g \
  --driver-memory 4g \
  my_spark_app.py
```

**기술사 판단 포인트**:
- YARN의 리소스 단위는 vCore(가상 CPU 코어)와 메모리 MB다. Container = X vCore + Y MB 메모리.
- ApplicationMaster가 실패하면 YARN이 자동으로 재시작(최대 `yarn.resourcemanager.am.max-attempts` 횟수)한다.
- 최신 트렌드: Spark on Kubernetes(K8s)가 YARN 대체 움직임. 클라우드 환경에서는 EMR on EKS처럼 K8s 위에 Spark를 올리는 방식이 증가하고 있다.

---

## 5. 실무 적용 및 판단

| 기대효과 | 설명 |
|:---|:---|
| 클러스터 활용률 향상 | 다양한 엔진 혼재로 유휴 자원 최소화 |
| 확장성 향상 | JobTracker 한계 극복, 수만 노드 지원 |
| 멀티 테넌트 지원 | 팀별 자원 보장 및 격리 |
| 범용 플랫폼 | MapReduce + Spark + Flink 단일 클러스터 운영 |

YARN은 하둡을 "MapReduce 전용 시스템"에서 "빅데이터 범용 운영 플랫폼"으로 탈바꿈시킨 핵심 혁신이다. 현재 Spark on K8s 등으로 점차 대체되고 있지만, 수천 노드 하둡 클러스터를 운영하는 환경에서는 여전히 핵심 인프라다.

---

## 6. 기대효과 및 결론

YARN (Yet Another Resource Negotiator)를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 YARN (Yet Another Resource Negotiator)의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
Hadoop 1.0: JobTracker (MapReduce 전용)
    │
    ▼
YARN: ResourceManager + NodeManager (범용 리소스 관리)
    ├─► ApplicationMaster: 앱별 독립 관리
    └─► Capacity/Fair Scheduler: 멀티테넌트 리소스 배분
    │
    ▼
K8s on Hadoop · Spark on K8s → 클라우드 통합 관리
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| ResourceManager | YARN의 마스터 노드, 전체 자원 할당 결정 |
| ApplicationMaster | 애플리케이션별 독립 스케줄러, SPOF 제거 핵심 |
| NodeManager | 각 노드 자원 상태 보고 및 컨테이너 실행 |
| Capacity Scheduler | 멀티 테넌트 환경의 팀별 자원 보장 |
| Spark on YARN | Spark가 YARN을 통해 하둡 클러스터 자원 활용 |
| Spark on K8s | YARN 대체 트렌드, 클라우드 네이티브 빅데이터 |

---
