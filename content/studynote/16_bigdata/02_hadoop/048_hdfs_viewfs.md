+++
weight = 48
title = "26. HDFS ViewFS — Hadoop 연합 네임스페이스 통합 뷰"
date = "2026-04-29"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: HDFS ViewFS (View File System)는 HDFS 연합(Federation) 환경에서 여러 독립 NameNode 클러스터를 단일 논리 네임스페이스 `/user`, `/data`, `/tmp` 등으로 마운트하여 통합 파일 시스템 뷰를 제공하는 클라이언트 측 가상 마운트 레이어다.
> **비유**: 대형 물류창고에 재고를 나눠 보관하고 작업 지시서를 현장 직원에게 보내는 체계와 같다.

📝 모범 답안

## 1. 개요 및 필요성

```text
┌───────────────────────────────────────────────────────┐
│           HDFS Federation + ViewFS 구조                │
├───────────────────────────────────────────────────────┤
│ 클라이언트 (ViewFS 설정 적용)                           │
│   /user  → viewfs://cluster1/user                      │
│   /data  → viewfs://cluster2/data                      │
│   /tmp   → viewfs://cluster1/tmp                       │
│                ↓                                       │
│  NameNode-1 (cluster1): /user, /tmp 담당               │
│  NameNode-2 (cluster2): /data 담당                     │
│                ↓                                       │
│  DataNode 풀 (공유) — 실제 블록 저장                    │
└───────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

### ViewFS 설정 (core-site.xml)

```xml
<property>
  <name>fs.viewfs.mounttable.default.link./user</name>
  <value>hdfs://nn1/user</value>
</property>
<property>
  <name>fs.viewfs.mounttable.default.link./data</name>
  <value>hdfs://nn2/data</value>
</property>
<property>
  <name>fs.defaultFS</name>
  <value>viewfs://default</value>
</property>
```

### ViewFS vs. RBF (Router-Based Federation)

| 비교 | ViewFS | RBF |
|:---|:---|:---|
| 추상화 위치 | 클라이언트 측 | 서버 측 (Router) |
| 설정 위치 | 각 클라이언트 | 중앙 Router 서버 |
| 크로스 경계 rename | 불가 | Router 지원 |
| 투명성 | 클라이언트 인식 필요 | 완전 투명 |

---

## 3. 구조 및 원리

**핵심 조건**: 데이터 배치 위치, 메타데이터 관리, 병렬 실행, 장애 복구가 함께 맞물려야 한다.

동작 순서:
| 비교 | 단일 NameNode | HDFS Federation | ViewFS |
|:---|:---|:---|:---|
| 확장성 | NameNode 메모리 한계 | 네임스페이스 수평 분할 | 통합 뷰 제공 |
| 단일 장애점 | NameNode HA 필요 | 독립 NN per 풀 | 클라이언트 추상화 |
| 관리 복잡도 | 낮음 | 높음 | 설정 파일 관리 |

---

## 4. 비교 및 연결

### 대규모 Hadoop 클러스터 설계
- 파일 수 > 1억 개: 단일 NameNode JVM 힙 ~60GB 초과 → Federation 분리 시점.
- 분리 기준: 팀별, 부서별, 데이터 특성별(배치/실시간/아카이브) 논리 분리.
- ViewFS로 기존 MapReduce/Spark 잡 경로 변경 없이 전환.

### Ozone (차세대 Hadoop 스토리지)
- Hadoop 3.x: HDFS ViewFS → Apache Ozone으로 진화. Ozone은 객체 스토리지 기반으로 수십 억 개 파일을 NameNode 메모리 없이 처리한다.

---

## 5. 실무 적용 및 판단

| 기대효과 | 내용 |
|:---|:---|
| **확장성** | 수십 억 파일 수용을 위한 네임스페이스 분산 |
| **투명성** | 기존 Hadoop 잡 코드 변경 없이 Federation 적용 |
| **가용성** | NameNode 독립 운영으로 단일 장애점 제거 |

HDFS ViewFS는 RBF로 진화하고, 궁극적으로 Ozone의 클라우드 네이티브 객체 스토리지로 대체되는 방향으로 발전 중이다.

---

## 6. 기대효과 및 결론

HDFS ViewFS — Hadoop 연합 네임스페이스 통합 뷰은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 하둡 계열 기술의 가치는 개별 컴포넌트보다 저장·자원·처리 계층이 얼마나 안정적으로 결합되는가에 달려 있다.

---

## 7. 발전 흐름도

```text
[단일 NameNode HDFS — 수억 파일 한계]
    │
    ▼
[HDFS Federation — 네임스페이스 수평 분할]
    │
    ▼
[ViewFS — 클라이언트 측 통합 마운트 뷰]
    │
    ▼
[RBF (Router-Based Federation) — 서버 측 통합 라우팅]
    │
    ▼
[Apache Ozone — 객체 스토리지 기반 무제한 확장]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **HDFS Federation** | ViewFS가 추상화하는 분산 네임스페이스 구조 |
| **NameNode** | 네임스페이스 메타데이터 관리 서버 |
| **RBF** | ViewFS의 서버 측 진화 버전 |
| **Apache Ozone** | HDFS 한계 극복을 위한 차세대 스토리지 |
| **DataNode** | 실제 블록을 저장하는 공유 스토리지 노드 |
