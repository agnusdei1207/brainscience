+++
weight = 259
title = "259. 카산드라 안티 엔트로피 - 머클 트리 복구"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Cassandra는 노드 간 데이터 불일치를 머클 트리(Merkle Tree) 비교로 효율적으로 탐지하고, Read Repair·Hinted Handoff·Anti-Entropy Repair로 일관성을 복구하는 3단계 자가 치유 메커니즘을 갖춘다.
> 2. **가치**: 네트워크 장애, 노드 다운 등으로 발생한 데이터 불일치를 전체 데이터를 전송하지 않고 머클 트리 루트 해시 비교만으로 불일치 범위를 O(log N)에 특정하여 최소한의 데이터만 동기화한다.
> 3. **판단 포인트**: `nodetool repair`는 정기적으로 실행해야 하며, gc_grace_seconds(기본 10일) 안에 실행하지 않으면 삭제된 데이터(Tombstone)가 복구되는 "좀비 데이터" 문제가 발생한다.

---

## Ⅰ. 개요 및 필요성

Cassandra는 마스터 없는 P2P 분산 아키텍처로, 쓰기 작업이 ConsistencyLevel에 따라 일부 노드에만 즉시 반영될 수 있다. 네트워크 파티션이나 노드 장애 후 복구 시 노드 간 데이터가 불일치할 수 있다.

**안티 엔트로피(Anti-Entropy)**는 이 불일치를 감지하고 복구하는 메커니즘이다. 엔트로피(무질서도)가 증가하는 것(데이터 불일치)에 반(Anti)하는 자동 복구 체계를 의미한다.

```
[Cassandra 노드 간 불일치 시나리오]

쓰기 요청: INSERT key=A, value=100 (ConsistencyLevel=ONE)
        │
        ▼
Node-1 [A=100] ✓ (즉시 반영)
Node-2 [A=100] ✓ (즉시 반영)
Node-3 [A=???] ✗ (네트워크 장애로 미반영)

→ Node-3 복구 후, A의 값이 없거나 구버전일 수 있음
→ Anti-Entropy 메커니즘이 불일치 탐지 및 복구
```

📢 **섹션 요약 비유**: 세 사람이 같은 문서를 편집하는데 한 사람이 잠깐 인터넷이 끊겼다. 다시 연결됐을 때 누가 뒤처진 부분을 찾아서 동기화해줄지를 자동으로 해결하는 게 안티 엔트로피다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 머클 트리(Merkle Tree) 구조

```
[머클 트리 구조]

파티션 범위를 재귀적으로 해싱하여 계층 트리 구성

Root Hash: H(H12, H34)
     │
     ├── H12: H(H1, H2)
     │    ├── H1: hash(데이터 범위 0~25%)
     │    └── H2: hash(데이터 범위 25%~50%)
     └── H34: H(H3, H4)
          ├── H3: hash(데이터 범위 50%~75%)
          └── H4: hash(데이터 범위 75%~100%)

두 노드의 Root Hash가 같으면 → 데이터 완전 동일 (비교 종료)
Root Hash 다르면 → 하위 노드 비교로 불일치 범위 특정
→ O(log N) 탐색으로 불일치 파티션 찾기
```

### 안티 엔트로피 복구 3가지 메커니즘

| 메커니즘 | 동작 시점 | 방식 | 특징 |
|:---|:---|:---|:---|
| **Read Repair** | 읽기 요청 시 | ConsistencyLevel에 따라 여러 노드 읽기 → 최신 버전으로 낡은 노드 업데이트 | 읽기 경로에서 자동 복구 |
| **Hinted Handoff** | 쓰기 시 일부 노드 다운 | 힌트(메시지)를 다른 노드에 저장, 복구된 노드에 나중에 전달 | 일시적 노드 다운 대응 |
| **Anti-Entropy Repair** | `nodetool repair` 명령 | 머클 트리 비교로 불일치 탐지 → 전체 동기화 | 장기 불일치 해소 |

### Hinted Handoff 흐름

```
쓰기 요청 (W=2, 3개 노드 대상)
        │
        ├── Node-1: 쓰기 성공 ✓
        ├── Node-2: 쓰기 성공 ✓
        └── Node-3: 다운 ✗
                │
                ▼
        Coordinator가 힌트 저장
        (Node-3에 전달할 데이터를 힌트 형태로 보관)
                │
                ▼ Node-3 복구 후
        힌트 데이터 Node-3으로 전달
                │
                ▼
        Node-3 데이터 동기화 완료
```

### Tombstone과 gc_grace_seconds

```
삭제 요청 처리:
DELETE key=A (즉시 삭제하지 않음)
        │
        ▼
모든 노드에 Tombstone(삭제 마커) 기록

gc_grace_seconds (기본 10일) 동안 Tombstone 유지
        │
        ▼ 10일 후
Compaction 과정에서 Tombstone과 원본 데이터 영구 삭제

! 10일 내에 nodetool repair를 실행하지 않으면:
  오프라인이었던 노드가 복구될 때 Tombstone 없이
  원본 데이터만 보유 → "좀비 데이터" 부활!
```

📢 **섹션 요약 비유**: 머클 트리는 회사 문서 목록을 체계화하는 체크섬과 같다. 전체 폴더의 체크섬이 같으면 동일한 문서, 다르면 어떤 하위 폴더가 다른지 절반씩 나눠 확인하여 빠르게 찾는다.

---

## Ⅲ. 비교 및 연결

### Cassandra 일관성 레벨(Consistency Level)과 안티 엔트로피

| 일관성 레벨 | Read Repair 빈도 | 설명 |
|:---|:---|:---|
| **ONE** | 낮음 | 1개 노드에서만 읽기, Read Repair 드묾 |
| **QUORUM** | 중간 | 과반수 노드 읽기, 불일치 탐지 확률 높음 |
| **ALL** | 높음 | 모든 노드 읽기, 즉시 불일치 탐지 및 복구 |

### Cassandra vs HBase 수리 메커니즘

| 항목 | Cassandra | HBase |
|:---|:---|:---|
| **토폴로지** | 마스터리스 P2P | Master-RegionServer |
| **수리 방식** | Anti-Entropy + Hinted Handoff | WAL 기반 복구 |
| **머클 트리** | ✅ 사용 | 사용 안 함 |
| **일관성 보장** | 튜닝 가능 (Eventually → Strong) | 강한 일관성 |

📢 **섹션 요약 비유**: Cassandra의 일관성 레벨은 회의 참석 기준이다. ONE은 1명만 동의해도 결정, QUORUM은 과반수 동의, ALL은 전원 동의. 참석자가 많을수록 모두가 같은 정보를 가지고 있는지 확인하기 쉽다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### nodetool repair 운영 전략

```bash
# 전체 클러스터 수리 (무거운 작업)
nodetool repair -full

# 특정 키스페이스 수리
nodetool repair keyspace_name

# 증분 수리 (변경된 부분만) - Cassandra 3.0+
nodetool repair --inc

# 병렬 수리 (각 노드가 동시에 수리)
nodetool repair -par

# 수리 진행 모니터링
nodetool compactionstats
```

### 운영 권장 사항

| 설정/실천 | 권장값/방법 | 이유 |
|:---|:---|:---|
| `nodetool repair` 주기 | gc_grace_seconds 이내 (기본 7~10일) | Tombstone 복구 방지 |
| `gc_grace_seconds` | 10일 (864000초) | 모든 노드에 삭제 전파 보장 시간 |
| Read Repair 비율 | `read_repair_chance=0.1` | 10% 읽기 시 자동 복구 실행 |
| Repair 도구 | Cassandra Reaper | 분산 환경에서 안전한 Repair 스케줄링 |

### 기술사 시험 판단 포인트

- **머클 트리 효율성**: 전체 데이터 전송 없이 해시 비교만으로 불일치 범위 O(log N) 특정
- **gc_grace_seconds와 좀비 데이터**: 삭제 후 10일 내 repair를 실행하지 않으면 삭제된 데이터 부활
- **BASE vs ACID**: Cassandra는 BASE(Basically Available, Soft state, Eventually consistent) 모델

📢 **섹션 요약 비유**: Hinted Handoff는 택배 대리 수령이다. 집에 없을 때(노드 다운) 경비실(다른 노드)이 택배를 보관했다가, 귀가하면(노드 복구) 택배를 전달한다. 택배를 놓치지 않는 것이 목표다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 영역 | 효과 |
|:---|:---|
| **데이터 일관성** | 정기 repair로 최종적 일관성 보장 |
| **자가 치유** | 운영자 개입 없이 일시적 장애 후 자동 복구 |
| **수리 효율성** | 머클 트리로 불일치 데이터만 선택적 전송 |
| **고가용성** | 노드 다운 중 Hinted Handoff로 쓰기 가용성 유지 |

### 한계 및 주의사항

- **repair 부하**: 전체 repair는 I/O와 CPU를 많이 소비 → 운영 시간 외 실행 권장
- **Tombstone 누적**: 삭제 많은 테이블에서 Tombstone 과다 누적 시 읽기 성능 저하
- **hinted_handoff_enabled=true**: 힌트 크기 무제한이면 디스크 고갈 → `max_hints_delivery_threads` 제한
- **repair 빠뜨리면**: gc_grace_seconds 초과 시 일부 노드에서 삭제된 데이터가 복구 불가능하게 부활

📢 **섹션 요약 비유**: 안티 엔트로피는 아파트 관리비 자동 정산이다. 월마다 각 세대 사용량을 비교(머클 트리)해서 차이가 있는 세대만 찾아내고(불일치 탐지) 정산해준다(repair). 정산을 너무 오래 미루면(gc_grace_seconds 초과) 이미 정리된 내역이 다시 청구될 수 있다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 머클 트리 | 불일치 범위를 O(log N)에 탐지하는 해시 트리 |
| Read Repair | 읽기 경로에서 자동 일관성 복구 |
| Hinted Handoff | 일시 다운 노드 대신 힌트 저장 후 복구 시 전달 |
| Tombstone | Cassandra의 논리적 삭제 마커 |
| gc_grace_seconds | Tombstone 유지 기간 (이 안에 repair 필수) |
| nodetool repair | 수동 anti-entropy repair 실행 명령 |

### 👶 어린이를 위한 3줄 비유 설명
1. 세 명이 같은 공책을 쓰는데, 한 명이 잠깐 자리를 비웠다가 돌아오면 빠진 내용을 채워줘야 해 - 그게 안티 엔트로피야.
2. 머클 트리는 공책 목차 비교야. 목차(해시)가 같으면 내용이 같은 거, 다르면 어떤 챕터가 다른지 찾아가는 거야.
3. Hinted Handoff는 부재중 메모야. "너 없을 때 이 내용 추가됐어" 메모를 붙여뒀다가 돌아왔을 때 알려주는 거야!
