+++
weight = 261
title = "261. 카프카 로그 컴팩션 (Log Compaction)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 카프카 로그 컴팩션은 토픽에서 동일 키(Key)의 구버전 메시지를 제거하고 최신 값(Value)만 보존하는 압축 전략으로, 전체 이력이 아닌 "현재 상태(Current State)"만 필요한 CDC·시스템 상태 복구에 최적화된다.
> 2. **가치**: 일반 로그 보존(시간/용량 기반 삭제)과 달리 로그 컴팩션은 키당 마지막 값을 영구 보존하여, 새로운 컨슈머가 전체 토픽을 처음부터 읽어도 각 키의 현재 상태를 완전히 재구성할 수 있다.
> 3. **판단 포인트**: 이벤트 소싱(Event Sourcing)에서 전체 이력이 필요하면 컴팩션 사용 금지. CDC(Change Data Capture)처럼 현재 상태만 필요하면 컴팩션이 스토리지를 획기적으로 절감한다.

---

## Ⅰ. 개요 및 필요성

Kafka 토픽에 사용자 프로필 업데이트 이벤트가 계속 쌓인다고 하자.

```
시간 순서:
user_id=101, name="홍길동"          (초기 등록)
user_id=101, name="홍길동", phone="010-1234"  (전화번호 추가)
user_id=101, name="홍길동2"         (이름 변경)
user_id=102, name="김철수"          (신규 사용자)
user_id=101, name="홍길동2", email="hong@..." (이메일 추가)
```

새로운 소비자가 "현재 사용자 프로필 상태"를 복구하려면 user_id=101의 최신 메시지만 필요하다. 구버전 3개는 불필요한 스토리지 낭비다.

**로그 컴팩션(Log Compaction)**은 각 키의 최신 메시지만 보존하고 구버전을 제거한다.

📢 **섹션 요약 비유**: 로그 컴팩션은 가계부 정리다. 은행 잔액이 현재 100만 원이라면, 과거의 입금·출금 내역을 모두 보관하는 대신 최종 잔액(100만 원)만 기록해도 현재 상태를 알 수 있다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 로그 세그먼트 구조

```
[Kafka 파티션 로그 구조]

Clean 세그먼트           Dirty 세그먼트 (컴팩션 대상)
┌─────────────────┐    ┌─────────────────────────┐
│ Offset 0: K1=A  │    │ Offset 10: K1=B          │
│ Offset 1: K2=X  │    │ Offset 11: K2=Y          │
│ Offset 2: K3=P  │    │ Offset 12: K1=C ← K1 최신│
│ (이미 컴팩션됨)  │    │ Offset 13: K2=Z ← K2 최신│
└─────────────────┘    │ Offset 14: K3=Q ← K3 최신│
                       └─────────────────────────┘

컴팩션 후:
┌─────────────────────────────────────────────┐
│ Offset 0: K1=A (Clean 영역 K1 → 삭제됨)     │
│ ....                                        │
│ Offset 12: K1=C (최신값 유지)               │
│ Offset 13: K2=Z (최신값 유지)               │
│ Offset 14: K3=Q (최신값 유지)               │
└─────────────────────────────────────────────┘
※ Offset 10(K1=B), 11(K2=Y) 구버전 제거됨
```

### 컴팩션 동작 원리

```
컴팩션 프로세스 (백그라운드 스레드):

1. Dirty 로그 스캔: Offset 순으로 Key-Offset 쌍 수집
   {K1: 12, K2: 13, K3: 14}  (최신 Offset 기록)

2. Clean 로그 병합: 최신 Offset이 아닌 메시지 제거

3. 결과: 각 Key당 1개의 최신 메시지만 보존
```

### Null Value = Tombstone (삭제)

```
삭제 이벤트: user_id=101, value=null  (Tombstone)
         │
         ▼
컴팩션 과정에서 key=101의 모든 메시지 + Tombstone 제거
→ 결과: user_id=101 관련 메시지 완전 삭제

Tombstone 보존 기간 설정:
delete.retention.ms=86400000 (24시간 동안 Tombstone 유지)
→ 느린 컨슈머도 삭제 이벤트를 받을 수 있도록
```

### 컴팩션 관련 설정

| 설정 | 기본값 | 설명 |
|:---|:---|:---|
| `cleanup.policy=compact` | delete | 컴팩션 정책 활성화 |
| `cleanup.policy=compact,delete` | - | 컴팩션 + 시간 기반 삭제 혼합 |
| `min.cleanable.dirty.ratio` | 0.5 | Dirty/전체 비율 이상이면 컴팩션 시작 |
| `delete.retention.ms` | 86400000 | Tombstone 유지 기간 (ms) |
| `segment.ms` | 604800000 | 세그먼트 롤링 주기 |

📢 **섹션 요약 비유**: 컴팩션은 화이트보드 지우개다. 여러 번 수정된 내용에서 이전 내용을 지우고 최신 내용만 남긴다. 화이트보드 공간을 절약하면서도 현재 상태는 완벽하게 유지한다.

---

## Ⅲ. 비교 및 연결

### 삭제 정책 vs 컴팩션 정책

| 항목 | delete (기본) | compact |
|:---|:---|:---|
| **보존 기준** | 시간(ms) 또는 용량(bytes) | 키당 최신 값 |
| **소비자 복구** | 오래된 데이터 접근 불가 | 처음부터 읽어도 현재 상태 복구 가능 |
| **스토리지** | 오래되면 자동 삭제 | 키 수에 비례 (키가 적으면 매우 효율적) |
| **적합 사례** | 이벤트 로그, 감사 기록 | CDC, 시스템 상태, DB 변경 이력 |

### CDC (Change Data Capture)에서 로그 컴팩션 활용

```
[Debezium CDC + Kafka 컴팩션]

PostgreSQL DB ──▶ Debezium ──▶ Kafka 토픽 (compact)
                              ┌────────────────────┐
                              │ Key: table.primary_key│
                              │ Value: 최신 행 상태   │
                              └────────────────────┘
                                        │
                              ┌─────────▼──────────┐
                              │ 소비자: Elasticsearch│
                              │ 전체 토픽 읽기로     │
                              │ 현재 DB 상태 동기화 │
                              └────────────────────┘
```

📢 **섹션 요약 비유**: CDC + 컴팩션 조합은 "증분 백업의 최적화"다. 매번 전체 DB를 백업하지 않고, 변경된 행의 최신 상태만 Kafka에 쌓아두면 소비자가 언제든 전체 상태를 재구성할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 토픽 설정 예시

```bash
# 컴팩션 토픽 생성
kafka-topics.sh --create \
  --topic user-profiles \
  --partitions 12 \
  --replication-factor 3 \
  --config cleanup.policy=compact \
  --config min.cleanable.dirty.ratio=0.1 \
  --config delete.retention.ms=3600000

# 기존 토픽에 컴팩션 정책 추가
kafka-configs.sh --alter \
  --entity-type topics \
  --entity-name user-profiles \
  --add-config cleanup.policy=compact
```

### 컴팩션 모니터링

```bash
# 컴팩션 지연 모니터링
# kafka.log:type=LogFlushStats,name=LogFlushRateAndTimeMs
# kafka.log:type=Log,name=LogEndOffset,topic=...,partition=...

# Kafka Connect에서 컴팩션 토픽 활용 (오프셋 저장)
# connect-offsets, connect-configs, connect-status 토픽은
# 기본적으로 compact 정책 사용
```

### 기술사 시험 판단 포인트

- **컴팩션의 보장**: "키당 최신 값 영구 보존" — Retention 정책과 달리 오래된 메시지도 최신이면 삭제 안 됨
- **Tombstone 처리**: value=null은 삭제 시그널 — delete.retention.ms 이후 완전 제거
- **컴팩션 + 삭제 혼합**: `cleanup.policy=compact,delete`로 컴팩션 적용 후 일정 기간 지난 세그먼트 삭제

📢 **섹션 요약 비유**: 로그 컴팩션이 없는 Kafka는 모든 이사 내역을 보관하는 주민등록부다. 컴팩션이 있으면 "현재 거주지만" 기록하는 효율적 등본이 된다. 이사 이력이 아닌 현재 주소만 필요하다면 컴팩션이 훨씬 효율적이다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 영역 | 효과 |
|:---|:---|
| **스토리지 절감** | 키 수가 많지 않은 CDC 시나리오에서 대폭 절감 |
| **빠른 복구** | 소비자 재시작 시 전체 토픽 리플레이로 현재 상태 복구 |
| **무한 보존** | 최신값은 retention 기간 관계없이 영구 보존 |
| **데이터 삭제 준수** | Tombstone으로 GDPR 삭제 요청 이행 가능 |

### 한계 및 주의사항

- **컴팩션 비용**: 백그라운드 스레드가 CPU/I/O 자원 사용 — 피크 시간 컴팩션 부하 주의
- **순서 보장 제한**: 컴팩션 후 오프셋에 "구멍"(gap)이 생겨 순서 기반 처리 로직 재검토 필요
- **이벤트 소싱 부적합**: 전체 이력이 필요한 경우 컴팩션은 이력을 파괴
- **컴팩션 지연**: dirty.ratio 임계값에 도달하기 전까지 컴팩션 미실행 — 일시적으로 중복 키 존재

📢 **섹션 요약 비유**: 로그 컴팩션의 가장 큰 주의사항은 "되돌릴 수 없다"는 것이다. 구버전 메시지가 삭제되면 이벤트 재생(Event Replay)으로 과거 상태를 복원할 수 없다. 이벤트 이력이 비즈니스 자산이라면 컴팩션은 금물이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| CDC (Change Data Capture) | 컴팩션 토픽의 핵심 사용 사례 |
| Tombstone | null value로 키 삭제 시그널 |
| Log Segment | 컴팩션 처리 단위 |
| Debezium | CDC 도구, Kafka 컴팩션 토픽과 연동 |
| Event Sourcing | 전체 이벤트 이력 필요 → 컴팩션 부적합 |
| Kafka Streams | 컴팩션 토픽을 상태 저장소(changelog)로 활용 |

### 👶 어린이를 위한 3줄 비유 설명
1. 카프카 로그 컴팩션은 노트 정리야. 같은 내용을 여러 번 수정했으면, 중간 수정본은 지우고 최종본만 남기는 거야.
2. "사용자 101번 이름이 처음엔 홍길동, 그다음엔 홍길동2"였다면 컴팩션 후엔 최신 "홍길동2"만 남아.
3. 그래서 새로 들어온 친구(소비자)가 처음부터 읽어도 현재 상태를 정확히 알 수 있어 - 구버전을 다 읽을 필요 없이!
