+++
title = "327. OLTP (On-Line Transaction Processing) - 실시간 트랜잭션, 정규화된 RDB, 빠른 응답 속도"
weight = 327
+++
## 0. 핵심 인사이트

> **💡 핵심 인사이트**
> Hint Handoff와 Anti-entropy는 **"분산 데이터베이스에서 네트워크 분할(Partition)이나 노드 장애 시 데이터 불일치를 해결하기 위해使用되는 두 가지 상이한 복구 메커니즘"**입니다.
> Hint Handoff는 **"일시적 장애 시Hints(지시서)를 활용하여 데이터를 나중에 올바른 노드에 전달하는 즉각적 대응"**이고, Anti-entropy는 **"，定期적으로 전체 데이터의 Checksum이나 해시 트리(Merkle Tree)를 비교하여 불일치를 발견하고修正하는background 복구"**입니다. 이 두 기법은 CAP 정리에서 **"일시적 정합성(Causal Consistency)이 깨진 후 복구"**하는 핵심 수단입니다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

```
[분산 DB에서 발생할 수 있는 장애 유형]

  1. 일시적 장애 (Transient Failure)
     - 네트워크 혼잡으로 인한 지연/丢包
     - 노드 과부하로 인한 일시적 응답 불가
     - → 짧은 시간 후 자연 복구 가능

  2. 영구 장애 (Permanent Failure)
     - 디스크 손상,Hardware故障
     - → 복제본(Replica)からの 再構築 필요

  3. 네트워크 분할 (Network Partition)
     - 네트워크 장비故障로 일부 노드끼리만 통신 가능
     - → 서로 다른 파티션에서 동일 데이터에 대한書き込み 충돌 가능
```

**분할 상황에서의 데이터 불일치:**

```
[네트워크 분할로 인한 불일치]

  정상 상태:
  ┌─────────┐     ┌─────────┐     ┌─────────┐
  │ Node A  │ ◄──►│ Node B  │ ◄──►│ Node C  │
  │ X=100   │     │ X=100   │     │ X=100   │
  └─────────┘     └─────────┘     └─────────┘

  분할 발생 (A-B는 연결, C는 단절):
  ┌─────────┐     ┌─────────┐  X   ┌─────────┐
  │ Node A  │ ◄──►│ Node B  │  X   │ Node C  │
  │ X=100   │     │ X=100   │  X   │ X=100   │ ← 단절!
  └─────────┘     └─────────┘      └─────────┘

  분할 중写入 발생:
  ┌─────────┐     ┌─────────┐     ┌─────────┐
  │ Node A  │ ◄──►│ Node B  │     │ Node C  │
  │ X=200   │     │ X=200   │     │ X=100   │ ← 불일치!
  └─────────┘     └─────────┘     └─────────┘
      ↑
  A, B에서 X를 100→200으로 변경
  C는 그 사실을 모름
```

---

## II. Hint Handoff (힌트 핸드오프)

### 개념과 작동 원리

**핵심 아이디어**: "장애 노드에 보내야 할 데이터를 일시적으로 다른 노드에 '힌트'와 함께 저장했다가, 장애 노드가 복구되면 전달하자"

```
[Hint Handoff 작동 과정]

  상황: Node B (복제본)가 일시적 장애

  1. 원본 쓰기 요청:
     Client → Node A (프라이머리): X = 200 write
                    │
                    │ "Node B에도 복제해줘"
                    ▼
  2. Node B 접근 실패! (장애 중)
     Node A는 Node C에게:
     "이거 대신 저장해줘 (Hint)! 언젠가 Node B가
      복구되면 Node B에게 전달해줘"
                    │
                    ▼
  3. Hint 저장 (Node C):
     ┌─────────────────────────────────┐
     │ Hints Table:                     │
     │  - Target: Node B               │
     │  - Operation: X = 200           │
     │  - For: 'partition-1'           │
     │  - TTL: 24시간                   │
     └─────────────────────────────────┘

  4. Node B 복구:
     Node C가 pending 되었던 Hint들을 Node B에게 전달
     → X = 200이 Node B에 적용됨
     → 복제본 간 최종 일치
```

### Cassandra의 Hint Handoff 구현

```yaml
# Cassandra.yaml 설정
hinted_handoff_enabled: true
hinted_handoff_throttle_in_kb: 1024  # 쓰rottle
max_hints_delivery_threads: 4         # 병렬 delivery 스레드
hints_directory: /var/lib/cassandra/hints

# 특정 키сп레이에 대한 힌트 비활성화
hinted_handoff_disabled_by_topic:
  - keyspace1:table1  # 특정 테이블만 힌트 오프
```

**힌트 크기 제한:**
```yaml
# 힌트 최대 크기 (Cassandra 기본값: 128KB)
max_hint_window: 3h  # 장애 발생 후 3시간 이내만 힌트 저장
# (3시간 넘게 장애가 지속되면 힌트丢弃 → Anti-entropy로 복구)
```

---

## III. Anti-entropy (앤티 엔트로피)

### Merkle Tree (머클 트리)를 利用한 차분 检测

Anti-entropy의 핵심은 **"데이터 전체를 비교하지 않고, 해시 트리(Merkle Tree)를 利用하여快速に差分を発見"**하는 것입니다.

```
[Merkle Tree 구조]

  모든 데이터의 해시를 계산:
  Hash(A) = hash("A")      Hash(B) = hash("B")
  Hash(C) = hash("C")      Hash(D) = hash("D")
  Hash(E) = hash("E")      Hash(F) = hash("F")

                Root Hash
              (전체 데이터 해시)
                    │
        ┌───────────┴───────────┐
        │                       │
   Hash(AB)                 Hash(CD)              ← 2개 자식의 해시
   hash(AB) =               hash(CD) =
   hash(hash(A)+            hash(hash(C)+
        hash(B))                 hash(D))
        │                       │
    ┌───┴───┐               ┌───┴───┐
    │       │               │       │
 Hash(A) Hash(B)        Hash(C) Hash(D)
    A       B               C       D
```

**Anti-entropy 복구 과정:**

```
[Anti-entropy 차분 检测]

  Node A와 Node B의 Merkle Tree 비교:

  1. Root Hash만 먼저 비교:
     Node A: 0x7F3A...
     Node B: 0x7F3A...
     → 동일! → 더 이상 비교 불필요 (빠른 완료)

  2. Root Hash가 다를 경우:
     → 자식 Hash 비교로 불일치 부분 찾기
     → Root(0x7F3A) ≠ Root(0x92BC)
     → Hash(AB)와 Hash(CD) 비교
     → Hash(AB) 같음 → Hash(CD) 다름
     → C와 D 중 불일치 노드 파악
     → 불일치한 리프만 실제 데이터 비교 → 차분 데이터만 복제
```

### Cassandra의 Anti-entropy

```python
# Cassandra의 Anti-entropy는 Read Repair로実装

def read_repair(key, column_family):
    """
    읽기 시 복제본들 간 불일치를檢出して修復
    """
    # 1. 모든 복제본에서 데이터 읽기
    responses = [replica.read(key) for replica in replicas]

    # 2. 가장 최근 버전 선택 (LWW 또는 Timestamp 기준)
    latest = max(responses, key=lambda r: r.timestamp)

    # 3. 오래된 복제본에게 최신 데이터 제공
    for replica in replicas:
        if replica.data != latest:
            replica.write(latest)  # 차분만 복제
```

---

## IV. Hint Handoff vs Anti-entropy 비교

```
[두 기법 비교]

  ┌────────────────┬─────────────────────┬─────────────────────┐
  │                │   Hint Handoff      │    Anti-entropy     │
  ├────────────────┼─────────────────────┼─────────────────────┤
  │ 트리거 조건    │ 장애 노드 복구 시     │ 정기적 (Background)  │
  │                │ (즉각적 복구)        │ (상시 모니터링)      │
  ├────────────────┼─────────────────────┼─────────────────────┤
  │ 대상          │ 장애 시 accumulated   │ 전체 데이터         │
  │                │ Hints (부분)         │ (머클 트리 비교)     │
  ├────────────────┼─────────────────────┼─────────────────────┤
  │ 복구 범위     │ 힌트가 있는           │ 차분만 검출/복구     │
  │                │ 변경 사항만           │                     │
  ├────────────────┼─────────────────────┼─────────────────────┤
  │ 오버헤드      │ 低 (힌트 저장소 크기) │ 中 (주기적 트리 구축)│
  ├────────────────┼─────────────────────┼─────────────────────┤
  │ 영구 장애     │ 힌트 TTL 이후는       │ 영구 장애 복구       │
  │ 복구          │ 복구 불가             │ (리플리카에서 재구성) │
  ├────────────────┼─────────────────────┼─────────────────────┤
  │ 네트워크       │ 분할 중 변경 사항      │ 분할 전후 상태       │
  │ 분할          │ 핸들링               │ 비교를 통한 복구     │
  └────────────────┴─────────────────────┴─────────────────────┘
```

---

## 5. 실무 적용 및 최적화 기법

**Cassandra에서 두 기법의 역할:**

```
[분산 복구 파이프라인]

  네트워크 단절 (Partition)
         │
         ▼
  분할 중写入 발생 (Hint Handoff 대기)
         │
         ▼
  분할 복구 ─────────────────────────────────────┐
         │                                        │
         ▼                                        │
  Hint Handoff 실행 ──────────────────────► 실패 시 │
         │                                        │ (Hint TTL 초과)
         ▼                                        ▼
  Anti-entropy (Read Repair)              Anti-entropy (Background)
  (읽기 시점 복구)                          (정기적 전체 검산)
         │                                        │
         └──────────────────┬───────────────────┘
                            ▼
                    모든 복제본 일치 (Eventual Consistency)
```

> 📢 **섹션 요약 비유:** Hint Handoff와 Anti-entropy는 **"우체국 시스템"**과 같습니다. Hint Handoff는 **"배달원이不在時に、近所に預けておく仕組み"**에 비유됩니다. 받을 사람(장애 노드)이不在시, 대신 받은 이웃집(다른 노드)이 **"부적당한 게 있으면 이걸 네 곳에 전달해줘 (Hint)"**라고メモ를 붙여두었다가, 받을 사람이 돌아오면 전달하는 것입니다. 반면 Anti-entropy는 **"두 우체국 지국이 서로등기 우표를 비교해서 다르면 확인하고修正하는 것"**입니다. 전체 우편물을 전부 비교하는 것이 아니라 **"먼저 전체 목록의 요약(머클 트리)을 비교하고, 다르다면 해당 우편물만 추려서 비교하는"** 효율적인 방법입니다. 이 두 시스템이 함께 작동해서 **"부패한 近所にあった置き配が 결국 원래 수령인에게 도착하고, 우체국 지국 간 우편물 목록이 일치하게 되는"** 것입니다.
