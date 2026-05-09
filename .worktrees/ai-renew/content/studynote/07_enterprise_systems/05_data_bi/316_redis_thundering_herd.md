+++
weight = 316
title = "316. Redis 데이터 스탬피드 Thundering Herd 장애 회피 (Redis Thundering Herd)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Thundering Herd (캐시 스탬피드)는 캐시가 만료된 순간 수천 개의 요청이 동시에 DB를 공격하여 DB를 마비시키는 장애 패턴이다.
> 2. **가치**: Redis SETNX 기반 분산 락과 Probabilistic Early Expiration, TTL Jitter를 조합하면 초당 10,000 req/s 환경에서도 DB 쿼리를 1~5건으로 제한할 수 있다.
> 3. **판단 포인트**: 캐시 TTL이 짧고 동시 접속자가 많을수록 위험도가 높으며, 핫 키(Hot Key)에 대한 사전 예방 설계가 필수다.

## Ⅰ. 개요 및 필요성

캐시(Redis)는 DB 부하를 90% 이상 감소시키지만, 캐시 만료(TTL 0)와 대량 동시 요청이 겹치면 모든 요청이 동시에 DB를 호출하는 Cache Stampede (캐시 스탬피드, Thundering Herd)가 발생한다.

발생 메커니즘:
1. 캐시 TTL 만료
2. 동시 요청 10,000건이 캐시 미스 감지
3. 모두 DB에 동일 쿼리 전송
4. DB CPU 100%, 응답 시간 폭증, 서비스 마비

Dog-pile Effect라고도 불리며, 인기 있는 콘텐츠(핫 키)일수록 피해가 크다.

대표 시나리오:
- 뉴스 속보: 동시 접속자 100,000명 → 기사 캐시 만료 → DB 폭주
- 주요 상품 페이지: 세일 시작 동시 캐시 만료

📢 **섹션 요약 비유**: Thundering Herd는 건물 비상구가 갑자기 열리는 순간 모두가 동시에 달려가 문이 막히는 상황이다.

## Ⅱ. 아키텍처 및 핵심 원리

### 해결 전략 비교

| 전략 | 방법 | 장점 | 단점 |
|:---|:---|:---|:---|
| Mutex Lock | SETNX로 1개 요청만 DB 조회, 나머지 대기 | 정확한 제어 | 지연 발생 (Lock 대기) |
| Probabilistic Early Expiration | TTL 소진 전 일부 요청이 미리 갱신 | 지연 없음 | 구현 복잡 |
| TTL Jitter | 만료 시간에 랜덤값 추가 | 간단 | 완전한 예방은 아님 |
| Cache Warming | 배포 전 캐시 사전 로드 | 근본 해결 | 운영 부담 |
| Local Cache | L1 로컬 캐시 + L2 Redis | DB 쿼리 0건 가능 | 메모리 사용 증가 |

### Redis SETNX 기반 분산 락

```python
# 캐시 미스 시 분산 락으로 단일 재빌드
def get_with_lock(key, ttl=300):
    value = redis.get(key)
    if value:
        return value

    lock_key = f"lock:{key}"
    # SETNX: Set if Not eXists (원자적 연산)
    acquired = redis.set(lock_key, "1", nx=True, ex=5)  # 5초 락

    if acquired:
        # 락 획득: DB 조회 후 캐시 갱신
        value = db.query(key)
        redis.setex(key, ttl, value)
        redis.delete(lock_key)
        return value
    else:
        # 락 미획득: 짧은 대기 후 재시도 (or stale cache 반환)
        time.sleep(0.05)
        return redis.get(key)  # 락 해제 후 캐시 재조회
```

### Probabilistic Early Expiration

```python
import math, random

def get_with_early_expiration(key, beta=1.0):
    value, delta, expiry = redis.get_with_meta(key)
    ttl_remaining = expiry - time.time()

    # 만료 임박 시 확률적으로 미리 갱신
    if -beta * delta * math.log(random.random()) >= ttl_remaining:
        value = db.query(key)
        redis.setex(key, TTL, value)

    return value
```

### ASCII 다이어그램: Thundering Herd vs 보호 패턴

```
  [Thundering Herd 발생]
  ┌───────────────────────────────────────────────────┐
  │  캐시 만료                                         │
  │  요청 10,000건 ──────────────────▶ DB (폭주!)      │
  │  (모두 동시에)                    CPU 100%         │
  └───────────────────────────────────────────────────┘

  [분산 락 보호 패턴]
  ┌───────────────────────────────────────────────────┐
  │  캐시 만료                                         │
  │  요청 1번 ──── SETNX 락 획득 ──▶ DB 쿼리 (1건)    │
  │  요청 2~10,000번                                   │
  │  ├── 락 대기 ──── 락 해제 후 캐시 히트 ──▶ 응답   │
  │  └── Stale Cache ──▶ 이전 캐시값 반환 ──▶ 응답     │
  │  결과: DB 쿼리 1건만 발생                          │
  └───────────────────────────────────────────────────┘
```

### TTL Jitter 적용

```python
# 동일 TTL 대신 랜덤 범위를 추가해 만료 시간 분산
base_ttl = 3600  # 1시간
jitter = random.randint(0, 600)  # ±10분 랜덤 추가
redis.setex(key, base_ttl + jitter, value)
# 결과: 동시에 여러 핫 키가 만료되는 상황 방지
```

📢 **섹션 요약 비유**: TTL Jitter는 시험 종료 시간을 학생마다 살짝 다르게 해서 모두가 동시에 문을 향해 달리는 혼잡을 방지하는 것이다.

## Ⅲ. 비교 및 연결

### 핫 키 (Hot Key) 문제

단일 캐시 키가 초당 수만 건 조회되는 경우:
- Redis 단일 노드 CPU 병목
- 해결책: Read Replica, Key Sharding (hot-key:shard:0~9), Local L1 Cache

| 방법 | 효과 | 복잡도 |
|:---|:---|:---|
| Read Replica | 읽기 부하 분산 | 낮음 |
| Key Sharding | 여러 키로 분산 | 중간 |
| Local L1 Cache | Redis 쿼리 자체 제거 | 높음 (일관성 주의) |

📢 **섹션 요약 비유**: 핫 키는 한 창구에 모든 손님이 몰리는 것이다. 창구를 늘리거나(Read Replica) 번호표로 분산하거나(Key Sharding), 손님이 직접 정보를 갖고 오게 해야 한다(L1 Cache).

## Ⅳ. 실무 적용 및 기술사 판단

### Thundering Herd 방지 체크리스트

- [ ] TTL Jitter 적용: base_ttl + random(0~10%) 적용
- [ ] 핫 키 식별: Redis `--hotkeys` 옵션으로 상위 100개 키 모니터링
- [ ] 분산 락 타임아웃: Lock TTL은 DB 쿼리 예상 시간 × 3배 설정
- [ ] Stale Cache 정책: 락 대기 중 이전 캐시값 반환 (약간의 오래된 데이터 허용)
- [ ] Cache Warming 자동화: 배포 파이프라인에 캐시 사전 로드 포함

### 안티패턴

| 안티패턴 | 문제 | 해결 방법 |
|:---|:---|:---|
| 모든 캐시 동일 TTL | 일시에 만료 → 스탬피드 | TTL Jitter 필수 |
| Lock TTL 너무 짧음 | DB 쿼리 중 락 만료 → 다중 DB 쿼리 | TTL = 쿼리 시간 × 3배 |
| Stale Cache 미사용 | 락 대기 중 에러 응답 | 이전 캐시값 임시 반환 설계 |

📢 **섹션 요약 비유**: Lock TTL이 너무 짧은 건 화장실 잠금장치 비밀번호가 문 열리기 전에 초기화되는 것이다. 다음 사람이 들어와 혼잡해진다.

## Ⅴ. 기대효과 및 결론

| 항목 | Thundering Herd 미방지 | 방지 후 |
|:---|:---|:---|
| DB 쿼리 수 (캐시 만료 시) | 10,000건/초 | 1~5건/초 |
| DB 응답 시간 | 수초~타임아웃 | 정상 범위 유지 |
| 서비스 가용성 | 장애 (DB 폭주) | 정상 |
| 사용자 경험 | 서비스 중단 | 캐시 히트율 99%+ 유지 |

📢 **섹션 요약 비유**: Thundering Herd 방지는 쇼핑몰 입장 관리다. 동시에 모두 문을 열지 않고, 줄을 세워 순서대로 입장시킨다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Thundering Herd | 장애 패턴 | 캐시 만료 동시 DB 공격 |
| SETNX | 해결 기법 | Redis 원자적 분산 락 |
| TTL Jitter | 예방 기법 | 만료 시간 랜덤 분산 |
| Cache Warming | 예방 전략 | 배포 전 캐시 사전 로드 |
| Hot Key | 연관 문제 | 단일 키 과다 조회 |
| Stale Cache | 대응 전략 | 이전 캐시값 임시 반환 |

### 👶 어린이를 위한 3줄 비유 설명

1. Thundering Herd는 학교 벨이 울리자마자 모든 학생이 교문으로 달려가 문이 막히는 것이에요.
2. 분산 락은 "한 명씩 나가세요" 선생님처럼, 한 요청만 DB에 접근하게 하는 규칙이에요.
3. TTL Jitter는 학생마다 다른 시간에 내보내서 문이 막히지 않게 하는 거예요.
