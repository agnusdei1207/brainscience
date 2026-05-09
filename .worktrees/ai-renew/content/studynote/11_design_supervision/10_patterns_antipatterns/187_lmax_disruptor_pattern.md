+++
weight = 187
title = "187. LMAX 아키텍처 - 디스럽터 패턴 (LMAX Disruptor Pattern)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: LMAX 디스럽터 (Disruptor)는 링버퍼(Ring Buffer) 기반의 락프리(Lock-Free) 인메모리 큐로, CAS (Compare-And-Swap) 연산으로 동시성을 제어하여 초저지연(Ultra-Low Latency) 처리를 달성하는 아키텍처 패턴이다.
> 2. **가치**: 전통적 `BlockingQueue`(락 기반)보다 수십 배 빠른 처리량(수백만 TPS)을 달성하며, 금융 거래 시스템처럼 마이크로초 단위 응답이 필요한 시스템에 적용된다.
> 3. **판단 포인트**: 디스럽터의 성능 비결은 캐시 라인 패딩(Cache Line Padding)으로 폴스 셰어링(False Sharing)을 방지하고, 락 대신 CAS로 동시성을 제어하는 하드웨어 친화적 설계에 있다.

---

## Ⅰ. 개요 및 필요성

### 전통 메시지 큐의 한계

금융 거래 시스템(LMAX Exchange)은 초당 수백만 건의 주문을 처리해야 했다.

```
[전통 BlockingQueue의 성능 병목]
Producer ──► [  Lock  ] ──► BlockingQueue ──► [  Lock  ] ──► Consumer
                 │                                  │
                 │ 락 획득 대기                      │ 락 획득 대기
                 │ → 컨텍스트 스위칭                │ → 컨텍스트 스위칭
                 │ → CPU 캐시 미스                  │ → CPU 캐시 미스
                 ▼                                  ▼
              성능 저하!                          성능 저하!
```

- **락 경합 (Lock Contention)**: 여러 스레드가 동시에 큐에 접근 시 대기 발생
- **컨텍스트 스위칭 (Context Switching)**: 스레드 블로킹 시 CPU 전환 오버헤드
- **폴스 셰어링 (False Sharing)**: 다른 변수가 같은 CPU 캐시 라인을 공유하여 불필요한 캐시 무효화

LMAX Exchange는 이 문제를 링버퍼 + CAS로 해결했다.

📢 **섹션 요약 비유**: 카페 계산대(큐) 앞에 줄(락) 서서 차례 기다리는 대신, 번호표(CAS 시퀀스)를 뽑아 자리에서 기다리다 호출될 때만 나오는 방식이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 링버퍼 (Ring Buffer) 구조

```
링버퍼 (크기 = 2^N, 예: 크기 8):

        ┌──────────────────────────────────────┐
        │                                      │
     ┌──▼──┐    ┌─────┐    ┌─────┐    ┌─────┐ │
     │  0  │    │  1  │    │  2  │    │  3  │ │
     │[Evt]│    │[Evt]│    │[Evt]│    │[Evt]│ │
     └─────┘    └─────┘    └─────┘    └─────┘ │
     ┌─────┐    ┌─────┐    ┌─────┐    ┌──▲──┐ │
     │  7  │    │  6  │    │  5  │    │  4  │ │
     │[Evt]│    │[Evt]│    │[Evt]│    │[Evt]│ │
     └─────┘    └─────┘    └─────┘    └─────┘ │
        │                                      │
        └──────────────────────────────────────┘

Producer: Sequence 번호를 CAS로 예약 후 이벤트 작성
Consumer: 자신의 Sequence 위치의 이벤트 읽기 (블로킹 없음)

핵심: 인덱스 = sequence % ringBufferSize (비트 AND 연산)
```

### CAS (Compare-And-Swap) 기반 동시성 제어

```
CAS 동작 원리:
- 기대값(expected)과 메모리 현재값을 비교
- 일치하면 새값(newValue)으로 원자적 교체
- 불일치하면 재시도 (스핀)

// Producer 시퀀스 예약
long sequence = ringBuffer.next(); // CAS: 다음 쓰기 위치 원자적 획득
try {
    Event event = ringBuffer.get(sequence);
    event.setValue(data);
} finally {
    ringBuffer.publish(sequence); // Consumer에게 사용 가능 신호
}
```

### 폴스 셰어링 방지 (Cache Line Padding)

```
CPU L1 캐시 라인 = 64 bytes

[문제: False Sharing]
캐시 라인 1 (64 bytes):
┌─────────────────────────────────────────────────────────────┐
│  producerSeq (8B) │ consumerSeq (8B) │ padding (48B 낭비) │
└─────────────────────────────────────────────────────────────┘
→ Producer가 producerSeq 수정 → 캐시 라인 무효화
→ Consumer가 consumerSeq 읽기 → 캐시 미스 발생!
→ 서로 다른 변수인데 같은 캐시 라인 때문에 간섭!

[해결: 패딩으로 캐시 라인 분리]
캐시 라인 1 (64 bytes):
┌─────────────────────────────────────────────────────────────┐
│  producerSeq (8B) │          패딩 56B                       │
└─────────────────────────────────────────────────────────────┘
캐시 라인 2 (64 bytes):
┌─────────────────────────────────────────────────────────────┐
│  consumerSeq (8B) │          패딩 56B                       │
└─────────────────────────────────────────────────────────────┘
→ 서로 다른 캐시 라인 → 간섭 없음!
```

| 성능 기법 | 전통 방식 | Disruptor |
|:---|:---|:---|
| **동시성 제어** | `synchronized`, `Lock` | CAS (Compare-And-Swap) |
| **캐시 최적화** | 없음 | Cache Line Padding |
| **메모리 구조** | 연결 리스트 큐 | Ring Buffer (배열, 연속 메모리) |
| **가비지 수집** | 객체 생성/소멸 | 사전 할당 이벤트 재사용 |
| **처리 패턴** | 스레드 블로킹 | 바쁜 대기(Busy-Spin) 또는 Park |

📢 **섹션 요약 비유**: 수동 카메라 필름(링버퍼)은 미리 채워져 있고 번호(Sequence)가 적혀 있다. 사진사(Producer)는 번호를 예약하고, 인화 담당(Consumer)은 번호 순서대로 처리한다. 중간에 필름을 버리지 않고 재사용한다.

---

## Ⅲ. 비교 및 연결

### Disruptor vs 전통 큐 성능 비교

| 비교 항목 | Java BlockingQueue | Disruptor Ring Buffer |
|:---|:---|:---|
| **동시성 제어** | Mutex Lock | CAS (락프리) |
| **메모리 할당** | 이벤트마다 신규 객체 | 사전 할당, 재사용 |
| **캐시 효율** | 낮음 (힙 메모리 분산) | 높음 (연속 배열) |
| **GC 압력** | 높음 | 낮음 (객체 재사용) |
| **처리량 (ops/sec)** | ~100만 | ~수천만 |
| **지연시간** | 수십 μs ~ ms | 수 ns ~ μs |
| **복잡성** | 낮음 | 높음 |

### Disruptor 이벤트 처리 토폴로지

```
[단순 파이프라인]
Producer ──► [RB] ──► Consumer1 ──► Consumer2 ──► Consumer3

[다이아몬드 토폴로지]
                    ──► Consumer1 ──►
Producer ──► [RB] ──►               ──► Consumer3
                    ──► Consumer2 ──►

[브로드캐스트]
                    ──► Consumer1
Producer ──► [RB] ──► Consumer2
                    ──► Consumer3
(모든 Consumer가 모든 이벤트 처리)
```

📢 **섹션 요약 비유**: 공장 컨베이어 벨트(Ring Buffer)가 멈추지 않고 돌아가며, 각 작업대(Consumer)는 자기 앞을 지나가는 제품을 처리한다. 벨트는 항상 돌고, 자리를 뺏으러 싸울 필요가 없다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Java Disruptor 사용 예시

```java
// 이벤트 클래스 (사전 할당)
public class TradeEvent {
    private long tradeId;
    private double price;
    private long quantity;
    // 재사용을 위해 setter로 값 변경
}

// Disruptor 설정
int BUFFER_SIZE = 1024; // 반드시 2^N
Disruptor<TradeEvent> disruptor = new Disruptor<>(
    TradeEvent::new,           // 이벤트 팩토리 (사전 할당)
    BUFFER_SIZE,
    DaemonThreadFactory.INSTANCE,
    ProducerType.SINGLE,       // 단일 생산자: 추가 최적화
    new BusySpinWaitStrategy() // 최저 지연: CPU를 양보하지 않고 스핀
);

// Consumer 등록
disruptor.handleEventsWith(
    (event, sequence, endOfBatch) -> {
        riskEngine.process(event);    // 위험 관리
    }
).then(
    (event, sequence, endOfBatch) -> {
        orderBook.update(event);      // 오더북 업데이트
    }
);

RingBuffer<TradeEvent> ringBuffer = disruptor.start();

// Producer: 이벤트 발행
long sequence = ringBuffer.next();
try {
    TradeEvent event = ringBuffer.get(sequence);
    event.setTradeId(tradeId);
    event.setPrice(price);
} finally {
    ringBuffer.publish(sequence);
}
```

### 기술사 판단 포인트

| 상황 | Disruptor 적합 여부 | 이유 |
|:---|:---|:---|
| 금융 거래 매칭 엔진 | 적합 | 마이크로초 단위 응답, 고처리량 |
| 실시간 게임 이벤트 처리 | 적합 | 낮은 지연, 높은 동시성 |
| 일반 웹 애플리케이션 | 과도한 복잡성 | Kafka, RabbitMQ로 충분 |
| 마이크로서비스 간 통신 | 부적합 | 프로세스 내 큐이므로 서비스 간 불가 |

📢 **섹션 요약 비유**: 디스럽터는 F1 레이싱 엔진이다. 일반 출퇴근용(일반 애플리케이션)으로는 과도하지만, 레이싱(초저지연 금융 시스템)에선 유일한 선택이다.

---

## Ⅴ. 기대효과 및 결론

### Disruptor 도입 기대효과

| 기대효과 | 구체적 내용 |
|:---|:---|
| **초저지연** | 단일 자리수 마이크로초(μs) 이벤트 처리 |
| **고처리량** | 초당 수천만 이벤트 처리 가능 |
| **GC 최소화** | 이벤트 객체 재사용으로 GC 중지(Stop-the-World) 최소화 |
| **CPU 캐시 최적화** | 연속 메모리 배열과 Cache Line Padding |
| **락프리 동시성** | 락 경합 없는 CAS 기반 스레드 안전성 |

LMAX Disruptor는 "소프트웨어 성능의 한계를 하드웨어 수준으로 끌어올린" 혁신적 패턴이다. CPU 캐시 동작 방식을 이해하고 하드웨어 친화적 알고리즘을 설계하는 것이 진정한 고성능 시스템 설계다. Martin Fowler도 LMAX의 아키텍처 문서에서 이 패턴을 극찬했다.

📢 **섹션 요약 비유**: 디스럽터는 도로 교통 체증(락 경합)을 없애기 위해 번호표(Sequence) 시스템과 논스톱 순환 도로(Ring Buffer)를 설계한 것이다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | 동시성 패턴 (Concurrency Pattern) | 락프리 동시성의 고급 구현 |
| 상위 개념 | 고성능 아키텍처 | 하드웨어 친화적 소프트웨어 설계 |
| 하위 개념 | 링버퍼 (Ring Buffer) | Disruptor의 핵심 자료구조 |
| 하위 개념 | CAS (Compare-And-Swap) | 락프리 원자적 연산 |
| 연관 개념 | 캐시 라인 패딩 | False Sharing 방지 기법 |
| 연관 개념 | 스페이스 기반 아키텍처 | 인메모리 고성능 아키텍처 |
| 연관 개념 | 이벤트 버스 패턴 | 이벤트 처리 파이프라인 구성 |

### 👶 어린이를 위한 3줄 비유 설명

- 놀이공원 매표소(전통 큐)에서 차례 기다리면 줄(락)이 길어지지만, 번호표(CAS Sequence) 뽑고 자리에서 기다리면 더 빠르다.
- 링버퍼는 회전목마(8칸 순환)처럼 타는 사람(Producer)과 내리는 사람(Consumer)이 서로 방해 없이 동시에 움직인다.
- 금융 거래소는 1초에 백만 건의 거래를 처리해야 해서, 이 회전목마처럼 멈추지 않는 설계가 꼭 필요하다.
