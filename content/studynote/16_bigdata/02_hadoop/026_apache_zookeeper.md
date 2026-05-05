+++
weight = 26
title = "04. Apache ZooKeeper - 분산 코디네이션의 간호사"
date = "2026-04-05"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Apache ZooKeeper - 분산 코디네이션의 간호사은(는) 분산 저장, 병렬 처리, 자원 관리를 결합해 대규모 데이터를 저비용으로 처리하게 하는 하둡 계열 핵심 기술이다.
> **비유**: 대형 물류창고에 재고를 나눠 보관하고 작업 지시서를 현장 직원에게 보내는 체계와 같다.

📝 모범 답안

## 1. 개요 및 필요성

ZooKeeper는 Zab 프로토콜을 통해 분산 환경에서의 원자적 브로드캐스트를 달성합니다.
- **역할**: Zab은"모든 Follower이 동일한 순서로 동일한 메시지를受領"하도록保証하는原子적 브로드캐스트 프로토콜입니다. 이것이 보장되지 않으면, 일부 Follower만 업데이트되어 상태가 불일치하게 됩니다.
- **모드**: Zab은 두 가지 모드로 동작합니다. (1) **Recovery (리더 선출 후)**: 새 리더가 모든 Follower의 상태를 동기화하여 일관성을 확보합니다. (2) **Broadcast (정상 작동)**: 리더가 받은 쓰기 요청을 모든 Follower에 동시에 전파(Atomic Broadcast)합니다.

---

## 2. 구성요소

| Znode 유형 | 설명 | 활용 예 |
|:---|:---|:---|
| **영속 Regular (P)** | 명시적 삭제 전까지永久保存 | 설정 정보 (/config) |
| **임시 Ephemeral (E)** | 세션 종료 시 자동 삭제 |存活 확인 (-worker1 활성 표시) |
| **순차 Sequential** | 생성 시 자동으로 10자리 순번 증가 | 리더 선출, 분산 잠금 |

- **Sequential Ephemeral (SE)**: 가장 중요한 유형입니다. 임시(Ephemeral)이면서 순번이 자동 증가(SE)하는 노드로, 노드 작성 시`s "/leader/worker-0000000001"`과 같이 순번이 부여됩니다. ZooKeeper 세션이 종료되면(해당 노드 연결이 끊기면) 해당 Sequential Ephemeral 노드는 자동으로 삭제되어, 장애 노드의"리더 후보" 자격을自動的に剥奪합니다.

---

## 3. 구조 및 원리

**핵심 조건**: 데이터 배치 위치, 메타데이터 관리, 병렬 실행, 장애 복구가 함께 맞물려야 한다.

동작 순서:
| 비교 항목 | Apache ZooKeeper | etcd (CoreOS) | Consul (HashiCorp) |
|:---|:---|:---|:---|
| **일관성 모델** | 임계적 일관성 (Fencing Token) | Raft 기반 강한 일관성 | Gossip 기반 Eventually Consistent |
| **주요 용도** | 리더 선출, 분산 잠금 | 분산 키-값 스토어 | 서비스 메쉬, KV 스토어 |
| **CAP** | CP (일관성+파티션 허용) | CP | AP (가용성+파티션 허용) |
| ** bahasa pemrograman** | Java 중심 | Go | Go, Python, etc |
| **헬스체크** | 없음 (ephemeral 노드로 간접) | 자체 제공 | 에이전트 기반 |
| **주요 사용자** | Hadoop 생태계, Kafka | Kubernetes | 마이크로서비스 |

- **ZooKeeper의 가장 큰 강점**: Hadoop 생태계(HDFS NameNode HA, HBase Region Server 관리, Kafka 브로커 관리) 전반에 깊이 내장되어 있으며, 수십 년간의 프로덕션 검증과 안정성을 보유하고 있습니다. 다만"무거운部erapy"를 처리하는 것은 etcd나 Consul에 비해 복잡할 수 있어, 새로운 마이크로서비스 아키텍처에서는 etcd/Kubernetes etcd가 선호되는 경향이 있습니다.

---

## 4. 비교 및 연결

| 고려 사항 | 세부 내용 | 주요 의사결정 |
|:---|:---|:---|
| **필요 용도** | 리더 선출만 필요 → ZooKeeper/SimpleServiceRegistry | KV 스토어 + 리더 선출 → etcd |
| **일관성 요구** | 강한 일관성 필수 → etcd / ZooKeeper Quorum | Eventual 허용 → Consul |
| **규모** | 수십 개 수준 노드 → ZooKeeper 3~5대 | 수백~수천 노드 → Consul Gossip |
| **운영 난이도** | ZooKeeper 전담 관리 역량 필요 | etcd는 Kubernetes와 긴밀 | Consul은 간단한 KV |

*(추가 실무 적용 가이드 - ZooKeeper 클러스터 구축)*
- **서버 수 결정**: 3대 (개발/테스트), 5대 (중규모 프로덕션), 7대 (대규모/심각하게 가용성 중요한 경우). 偶수台는 권장되지 않으며, 항상 奇数台를 선택합니다.
- **리더/팔로워 구분**: 리더 선출은 Zab 프로토콜이 자동 처리하므로,运维은"3대 중 어느 서버가 리더인지"만 Watch하면 됩니다.
- **Ephemeral 노드를活用한存活检测**: 각 Worker가"/workers/{worker-id}" ephemeral 노드를 생성하면, 해당 Worker가死ぬ/연결이 끊기면 노드가 자동으로 삭제되어"이 Worker는 이제 활성 상태가 아니다"라는 것을全システム에通知됩니다.

---

## 5. 실무 적용 및 판단

1. **ZooKeeper의 ZooKeeper 대체재 등장: KRaft와 etcd의 확산**
   Kafka 3.3+에서 도입된 KRaft 모드는 ZooKeeper를 대체하여 Kafka 자체의 Raft 프로토콜로 메타데이터를管理합니다. 이는 ZooKeeper에 대한 의존성을 제거하고"운영 단순화"와"단일 장애점 제거"를 동시에 달성합니다. 또한 Kubernetes의 etcd가 마이크로서비스 세계의"분산 코디네이션 표준"으로 자리잡음에 따라, ZooKeeper의 사용 범위가 줄어드는 추세가 가속화되고 있습니다.

2. **서비스 메시와 Service Mesh의 코디네이션 통합**
   HashiCorp Consul, Istio, Linkerd 등의 서비스 메시(Service Mesh) 기술이"서비스 디스커버리 + 분산 추적 + mTLS 암호화 + 코디네이션"을統合하여 제공함에 따라, ZooKeeper가 제공하던"서비스 등록/탐색" 기능이 서비스 메시 레벨로吸收되고 있습니다. 이러한 추세는"별도의 ZooKeeper 클러스터 운영"의 부담을 줄이면서"더 풍부한 서비스 관찰 가능성"을 제공하는 이점을 가집니다.

3. **ZooKeeper의 역할 재정의: 대규모 상태 저장이 아닌"이벤트 기반 코디네이션"으로**
   ZooKeeper의 설계 철학은"작고 빠른 코디네이션"에 집중하는 것입니다. 그러나 수십 만 개의 키를 저장해야 하는 경우, ZooKeeper의 성능은etcD나 Consul에 비해劣ります. 향후 ZooKeeper는"대규모 상태 저장이 아닌"高性能이 필요한"리더 선출 + 분산 잠금 + WATCH" 전용으로 그 역할이 재정의될 것으로 전망됩니다.

## 🧠 지식 맵 (Knowledge Graph)

*   **Apache ZooKeeper 핵심 개념**
    *   **Znode**: ZooKeeper의 기본 데이터 단위 (파일+디렉토리 hybrid)
    *   **Watcher**: 노드 변경 시 자동 알림
    *   **Zab Protocol**: Atomic Broadcast + Leader Election
    *   **Quorum**: 과반수 서버 consensus
*   **Znode 유형 조합**
    *   **Regular Persistent (P)**: 영속 비순차 - 설정 정보 저장
    *   **Ephemeral (E)**: 임시 비순차 -存活 확인
    *   **Persistent Sequential (PS)**: 영속 순차 - 일관된 이름 필요
    *   **Ephemeral Sequential (ES)**: 임시 순차 - 리더 선출, 분산 잠금
*   **주요 활용 패턴**
    *   **리더 선출**: 가장 낮은 sequence number의 ES 노드
    *   **분산 잠금**: Zookeeper의 `getChildren()` + `watch` 조합
    *   **서비스 디스커버리**: ephemeral 노드 등록 + watch

---

## 6. 기대효과 및 결론

Apache ZooKeeper - 분산 코디네이션의 간호사은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 하둡 계열 기술의 가치는 개별 컴포넌트보다 저장·자원·처리 계층이 얼마나 안정적으로 결합되는가에 달려 있다.

---

## 7. 발전 흐름도

```text
[Apache ZooKeeper 핵심 개념]
    │
    ▼
[Znode: ZooKeeper의 기본 데이터 단위 (파일+디렉토리 hybrid)]
    │
    ▼
[Watcher: 노드 변경 시 자동 알림]
    │
    ▼
[Zab Protocol: Atomic Broadcast + Leader Election]
    │
    ▼
[Quorum: 과반수 서버 consensus]
    │
    ▼
[Znode 유형 조합]
    │
    ▼
[Regular Persistent (P): 영속 비순차 - 설정 정보 저장]
```

이 흐름도는 Apache ZooKeeper 핵심 개념에서 출발해 Znode 유형 조합까지 이어지며, 중간 단계가 기초 개념을 실무 구조로 발전시키는 과정을 보여준다.

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| HDFS | 분산 저장 계층 |
| MapReduce·Spark | 분산 처리 엔진 연결점 |
| YARN | 클러스터 자원 관리 축 |
| Hive·HBase·Kafka | 하둡 생태계 확장 요소 |
