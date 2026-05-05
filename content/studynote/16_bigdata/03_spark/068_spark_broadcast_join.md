+++
weight = 68
title = "Spark Broadcast Join"
date = "2026-03-04"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Spark Broadcast Join은(는) 인메모리 분산 실행과 쿼리 최적화를 통해 대화형 분석·배치·스트리밍을 빠르게 연결하는 스파크 핵심 개념이다.
> **비유**: 같은 재료를 다시 꺼내지 않도록 조리대 위에 올려 두고 빠르게 여러 요리를 완성하는 주방과 같다.

📝 모범 답안

## 1. 개요 및 필요성

분산 환경에서 두 테이블을 조인하려면 보통 동일한 키를 가진 데이터를 같은 노드로 모으는 '셔플 해시 조인(Shuffle Hash Join)'이 발생한다. 하지만 하나는 수십억 건이고 다른 하나는 수천 건 정도라면, 작은 쪽을 모든 노드에 뿌려버리는 것이 전체 데이터를 섞는 것보다 훨씬 효율적이다. 이것이 Broadcast Join의 핵심 아이디어다.

---

## 2. 구성요소

Broadcast Join은 **작은 테이블의 수집(Collect)**과 **전체 배포(Broadcast)** 과정을 거친다.

```text
[ Broadcast Join Architecture / 브로드캐스트 조인 아키텍처 ]

    [ Driver ] --(Collect 小 Table)--        |
        +----(Broadcast to all nodes)----> [ Executor 1 ] [ Executor 2 ] ...
                                                 |              |
                                           (Local Join)    (Local Join)
                                                 |              |
                                           [ Big Data A ]  [ Big Data B ]

1. Collect: Driver fetches the small table from executors.
2. Broadcast: Driver pushes the small table to every executor using BitTorrent-like protocol.
3. Execution: Each executor performs a hash join locally with its portion of big data.
4. Advantage: No Shuffle for the big table.
```

- **임계값 설정:** `spark.sql.autoBroadcastJoinThreshold` (기본값 10MB) 이하의 테이블은 자동으로 브로드캐스트 조인 대상이 된다.
- **작동 조건:** 한쪽 테이블이 드라이버와 각 익스큐터의 메모리에 충분히 들어갈 수 있을 만큼 작아야 한다. 너무 크면 `OutOfMemory(OOM)` 오류가 발생할 수 있다.

---

## 3. 구조 및 원리

**핵심 조건**: 지연 평가, 파티션, 메모리 활용, 실행 계획 최적화가 동시에 설계되어야 한다.

동작 순서:
| 비교 항목 | Shuffle Hash Join | Broadcast Join |
| :--- | :--- | :--- |
| **데이터 이동** | 두 테이블 모두 셔플 발생 | **작은 테이블만 복제, 큰 테이블 이동 없음** |
| **네트워크 부하** | 매우 높음 (N:N 이동) | 낮음 (1:N 복제) |
| **메모리 요구사항** | 중간 | 익스큐터마다 작은 테이블을 담을 메모리 필요 |
| **성능 (대:소 조인)** | 느림 | **매우 빠름** |
| **권장 상황** | 두 테이블 모두 대용량일 때 | 한쪽 테이블이 수십 MB 이내로 작을 때 |

---

## 4. 비교 및 연결

- **OOM 주의:** 브로드캐스트 조인은 드라이버 메모리를 거쳐 전송되므로 드라이버 메모리 설정(`spark.driver.memory`)이 충분해야 한다. 또한 익스큐터들이 동시에 복제본을 유지하므로 익스큐터 메모리 부하도 고려해야 한다.
- **기술사적 통찰:** AQE(Adaptive Query Execution)를 활성화하면, 스파크가 런타임에 통계를 확인하여 셔플 조인을 브로드캐스트 조인으로 자동 전환(Demote to Broadcast)해준다. 이는 데이터 통계가 부정확한 상황에서도 안정적인 성능을 보장하는 핵심 전략이다.

---

## 5. 실무 적용 및 판단

Broadcast Join은 '데이터는 연산보다 이동 비용이 비싸다'는 분산 컴퓨팅의 진리를 가장 잘 활용한 기술이다. 실무에서는 차원 테이블(Dimension Table)과 사실 테이블(Fact Table) 간의 조인에서 표준으로 사용된다. 향후에는 메모리 가격 하락과 네트워크 기술(RDMA 등)의 발전에 따라 더 큰 규모의 테이블도 브로드캐스트 방식으로 처리될 가능성이 높다.

---

## 6. 기대효과 및 결론

Spark Broadcast Join은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 스파크 계열 기술의 성능은 단순 API 선택보다 실행 계획과 메모리·셔플 제어를 얼마나 정교하게 하느냐에서 결정된다.

---

## 7. 발전 흐름도

```text
[셔플 해시 조인 (Shuffle Hash Join) — 양쪽 테이블 전체 셔플, 네트워크 비용 O(N+M)]
    │
    ▼
[소트 병합 조인 (Sort-Merge Join) — 정렬 후 병합, 대용량 대용량 조인 기본 전략]
    │
    ▼
[브로드캐스트 조인 (Broadcast Join) — 소규모 테이블 전 노드 복사, 셔플 제로]
    │
    ▼
[버킷 조인 (Bucket Join) — 사전 버킷팅으로 셔플 없이 로컬 조인, 반복 조인 최적화]
    │
    ▼
[AQE (Adaptive Query Execution) — 런타임 통계 기반 동적 조인 전략 전환]
    │
    ▼
[DPP (Dynamic Partition Pruning) — 브로드캐스트 필터로 대규모 테이블 파티션 제거]
```
이 흐름은 대용량 데이터 조인의 네트워크 셔플 비용을 줄이기 위해 브로드캐스트 조인이 도입되고, 런타임 적응형 실행과 동적 파티션 제거로 진화하는 Spark SQL 최적화 기법의 발전을 보여준다.

---

## 8. 관련 개념 맵

- **상위 개념:** 조인 전략 (Join Strategies), 분산 컴퓨팅 최적화
- **핵심 기술:** 브로드캐스트 변수 (Broadcast Variable), 해시 조인
- **연관 기술:** AQE, Shuffle Hash Join, Sort Merge Join
