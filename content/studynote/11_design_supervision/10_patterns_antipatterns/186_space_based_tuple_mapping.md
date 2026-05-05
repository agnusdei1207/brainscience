+++
weight = 186
title = "186. 스페이스 기반 아키텍처 (Space-Based Architecture)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: 스페이스 기반 아키텍처 (Space-Based Architecture, SBA)는 인메모리 데이터 그리드(In-Memory Data Grid)를 공유 튜플 스페이스(Tuple Space)로 사용하여 데이터베이스를 요청 처리 경로에서 제거하는 초고성능 분산 아키텍처다.
> 2. **가치**: 전통 3계층 아키텍처의 DB 병목을 근본적으로 제거하여 수십만 TPS(Transactions Per Second)의 처리 성능을 달성할 수 있다.
> 3. **판단 포인트**: SBA는 처리 유닛(Processing Unit)이 공유 메모리에서 직접 데이터를 읽고 쓰므로 DB 없이 수평 확장이 가능하지만, 메모리 데이터의 영속성(Persistence) 보장이 핵심 과제다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 전통 3계층 아키텍처의 DB 병목

```
[전통 3계층 아키텍처의 한계]
     웹 레이어    ─── 수평 확장 가능 ───
     서비스 레이어 ─── 수평 확장 가능 ───
     데이터베이스  ─── 수평 확장 어려움!  ← 병목!

트래픽이 급증하면:
- 웹 서버: 로드 밸런서로 쉽게 확장
- 서비스 서버: 스케일 아웃 가능
- DB: 샤딩, 레플리케이션 필요 → 복잡하고 한계 존재
```

스케일러빌리티의 천장(Scalability Ceiling)은 항상 데이터베이스였다.

### 스페이스 기반 아키텍처의 해결책

```
[SBA 개념]
처리 요청
    │
    ▼
┌──────────────────────────────────────────────────────────┐
│           가상화 미들웨어 (Virtualized Middleware)          │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Processing   │  │ Processing   │  │ Processing   │   │
│  │ Unit 1       │  │ Unit 2       │  │ Unit 3       │   │
│  │ (웹+서비스+캐시│  │ (웹+서비스+캐시│  │ (웹+서비스+캐시│   │
│  │ 포함)        │  │ 포함)        │  │ 포함)        │   │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘   │
│         │                 │                 │           │
│         └─────────────────┴─────────────────┘           │
│                           │                             │
│          ┌────────────────▼────────────────┐            │
│          │    튜플 스페이스 (Tuple Space)    │            │
│          │  In-Memory Data Grid            │            │
│          │  (Hazelcast, GigaSpaces)        │            │
│          └────────────────────────────────┘            │
└──────────────────────────────────────────────────────────┘
                            │ 비동기 영속화
                            ▼
                       Database (영속 저장)
```

📢 **섹션 요약 비유**: 모든 계산원(Processing Unit)이 각자의 서랍(In-Memory)에서 재고(데이터)를 꺼내 처리한다. 창고(DB)에는 마감 시간(비동기)에만 최종 재고를 기록한다.

---

## 2. 구성요소

### SBA의 3대 핵심 컴포넌트

| 컴포넌트 | 역할 | 기술 예시 |
|:---|:---|:---|
| **처리 유닛 (Processing Unit)** | 웹, 서비스, 인메모리 캐시를 하나로 통합 | Spring Boot + Hazelcast |
| **가상화 미들웨어 (Virtualized Middleware)** | 요청 라우팅, 세션 관리, 데이터 복제 조율 | GigaSpaces XAP |
| **데이터 복제 엔진 (Data Replication Engine)** | 처리 유닛 간 인메모리 데이터 동기화 | Hazelcast IMap |

### 튜플 스페이스 (Tuple Space) 원리

린다(Linda) 병렬 컴퓨팅 모델에서 유래한 개념이다.

```
튜플 스페이스 = 공유 메모리 공간

작업자 A: write(("사용자", 1001, "홍길동", "active"))
작업자 B: take(("사용자", 1001, ?, ?))  ← 조건 매칭
→ 작업자 B가 해당 튜플 획득 및 처리

특징:
- 연관(Associative) 검색: 키가 아닌 패턴으로 조회
- 비동기 통신: 생산자와 소비자가 동시에 실행 불필요
- 공간적 분리(Space Decoupling): 위치 독립적 통신
```

### 데이터 복제 전략

```
처리 유닛 1          처리 유닛 2          처리 유닛 3
  [캐시 A]  ◄────────►  [캐시 B]  ◄────────►  [캐시 C]
  (복제본)              (복제본)              (복제본)

처리 유닛 1에서 데이터 변경 시:
1. 자신의 캐시 즉시 업데이트
2. 복제 이벤트 발행
3. 다른 처리 유닛 캐시 비동기 동기화
4. 데이터베이스 비동기 영속화 (Write-Behind)
```

📢 **섹션 요약 비유**: 각 편의점(Processing Unit)이 자체 재고(In-Memory)를 갖고 독립 운영된다. 중앙 물류창고(DB)에는 하루 마감 시 한 번만 재고 현황을 보고한다.

---

## 3. 구조 및 동작 원리

### SBA vs 전통 3계층 아키텍처 비교

| 비교 항목 | 전통 3계층 | 스페이스 기반 (SBA) |
|:---|:---|:---|
| **처리 병목** | DB 레이어 | 없음 (인메모리) |
| **확장 단위** | 레이어별 독립 확장 | 처리 유닛 전체 확장 |
| **지연시간** | ms~수십ms (DB I/O) | μs~1ms (메모리) |
| **데이터 일관성** | 강한 일관성 (ACID) | 최종 일관성 (Eventual Consistency) |
| **구현 복잡도** | 낮음 | 높음 (데이터 복제, 영속화 전략) |
| **적합 워크로드** | 일반 CRUD | 초고 동시성, 실시간 처리 |
| **대표 사례** | 일반 웹 서비스 | 금융 거래, 게임 서버, 실시간 경매 |

### In-Memory Data Grid (IMDG) 비교

| 제품 | 특징 | 주요 사용처 |
|:---|:---|:---|
| **Hazelcast** | 오픈소스, Spring 통합 우수 | 분산 캐시, 세션 클러스터링 |
| **GigaSpaces XAP** | 상용 SBA 플랫폼, 완전한 SBA 구현 | 금융, 통신 |
| **Apache Ignite** | 인메모리 DB + 분산 처리 통합 | 실시간 분석 |
| **Redis Cluster** | 고성능 키-값 저장소 | 캐싱, 세션, Pub/Sub |

📢 **섹션 요약 비유**: 3계층 아키텍처는 모든 메모에 창고(DB)까지 다녀와야 하지만, SBA는 각 직원(Processing Unit)이 메모장(인메모리)에 적어두고 퇴근 전에 창고에 최종 보고한다.

---

## 4. 비교 및 트레이드오프

### Hazelcast 기반 분산 캐시 예시

```java
// Spring Boot + Hazelcast 처리 유닛 구성
@Configuration
public class HazelcastConfig {
    @Bean
    public HazelcastInstance hazelcastInstance() {
        Config config = new Config();
        config.setClusterName("sba-cluster");

        // 분산 맵 설정: Near Cache + 복제
        MapConfig userMapConfig = new MapConfig("users")
            .setBackupCount(1)              // 복제본 1개
            .setTimeToLiveSeconds(300)      // 5분 TTL
            .setEvictionConfig(
                new EvictionConfig()
                    .setEvictionPolicy(EvictionPolicy.LRU)
            );
        config.addMapConfig(userMapConfig);
        return Hazelcast.newHazelcastInstance(config);
    }
}

// Processing Unit에서 In-Memory 데이터 접근
@Service
public class UserProcessingUnit {
    @Autowired
    private HazelcastInstance hz;

    public User getUser(Long id) {
        IMap<Long, User> users = hz.getMap("users");
        User user = users.get(id); // 인메모리에서 즉시 반환

        if (user == null) {
            user = userRepository.findById(id).orElseThrow();
            users.put(id, user); // 인메모리 캐싱
        }
        return user;
    }

    public void updateUser(User user) {
        hz.getMap("users").set(user.getId(), user); // 인메모리 즉시 업데이트
        // DB는 비동기 Write-Behind로 일괄 저장
    }
}
```

### 기술사 판단 포인트

| 상황 | SBA 적합 여부 | 이유 |
|:---|:---|:---|
| 1초 내 수십만 TPS | 적합 | DB 병목 없는 인메모리 처리 |
| 금융 실시간 거래 | 적합 (+ 강한 일관성 보장 추가) | 초저지연 필수 |
| 일반 전자상거래 | 과도한 복잡성 | 3계층 + Redis 캐시로 충분 |
| 데이터 정합성이 최우선 | 부적합 | 최종 일관성으로 데이터 손실 위험 |

📢 **섹션 요약 비유**: 증권 거래소(금융 SBA)는 1초에 수십만 건의 거래를 처리해야 한다. 매 거래마다 창고(DB)에 다녀오는 것은 불가능하다. 모든 것을 RAM에서 처리하고 나중에 정리한다.

---

## 5. 실무 적용 및 최적화 기법

### SBA 도입 기대효과

| 기대효과 | 구체적 내용 |
|:---|:---|
| **초고성능** | 인메모리 처리로 DB I/O 지연 제거 |
| **수평 확장** | 처리 유닛 추가만으로 선형 성능 확장 |
| **높은 가용성** | 처리 유닛 간 데이터 복제로 장애 내성 |
| **DB 부하 감소** | 비동기 Write-Behind로 DB 부하 최소화 |
| **실시간 처리** | 마이크로초 단위 응답 시간 |

SBA는 "데이터베이스가 없다면 얼마나 빠를까?"라는 질문에서 출발한 극단적 성능 최적화 아키텍처다. 금융 거래 시스템, 실시간 경매, 온라인 게임 서버처럼 **순간 최대 부하가 극도로 높은 시스템**에서 진가를 발휘한다. 그러나 데이터 영속성과 일관성 보장의 복잡성 때문에 일반 시스템에는 Redis 캐시가 더 현실적인 선택이다.

📢 **섹션 요약 비유**: F1 레이싱카(SBA)는 극한의 속도를 위해 에어컨, 네비게이션, 에어백을 제거했다. 일반 도로에는 SUV(3계층 + Redis)가 더 실용적이다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 분산 컴퓨팅 아키텍처 | SBA는 분산 컴퓨팅의 특수 형태 |
| 상위 개념 | 확장성 패턴 (Scalability Pattern) | DB 병목 제거를 통한 극단적 확장 |
| 하위 개념 | 처리 유닛 (Processing Unit) | SBA의 핵심 실행 단위 |
| 하위 개념 | In-Memory Data Grid (IMDG) | 분산 인메모리 데이터 저장소 |
| 연관 개념 | 마스터-워커 패턴 | 분산 작업 처리의 유사 패턴 |
| 연관 개념 | LMAX Disruptor | 인메모리 기반 초고성능 패턴 |
| 연관 개념 | 최종 일관성 (Eventual Consistency) | SBA의 데이터 일관성 모델 |

### 👶 어린이를 위한 3줄 비유 설명

- 학교 도서관(DB)이 너무 멀어서 매번 책을 빌리러 가기 힘들다. 각 교실(Processing Unit)에 미니 서재(In-Memory)를 두면 훨씬 빠르다.
- 각 교실 미니 서재의 책은 서로 자동으로 복사되어(데이터 복제) 어느 교실에서나 찾을 수 있다.
- 하루가 끝나면 모든 변경 사항을 도서관(DB)에 최종 보고한다(비동기 영속화).
