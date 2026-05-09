+++
weight = 122
title = "이벤트 소싱 (Event Sourcing)"
date = "2026-03-04"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)
- **상태 보존 방식의 혁신**: 데이터를 현재의 최종 상태(Current State)가 아닌, 모든 상태 변경 이력(Event Log)의 시퀀스로 저장하는 기법이다.
- **완벽한 감사(Audit)**: 시스템의 모든 행위를 재생(Replay)할 수 있어, 장애 복구 및 비즈니스 분석(Time Travel)에 절대적인 장점을 가진다.
- **CQRS와의 필수 결합**: 이벤트 스트림에서 현재 상태를 계산하는 비용을 줄이기 위해 조회를 전담하는 CQRS 패턴과 함께 사용된다.

### Ⅰ. 개요 (Context & Background)
일반적인 관계형 데이터베이스(RDBMS) 방식은 데이터가 변경될 때마다 기존 레코드를 덮어쓰기(Update)하여 최종 결과만 남긴다. 이로 인해 '누가, 언제, 왜' 이 데이터를 변경했는지에 대한 맥락(Context)이 유실된다. 이벤트 소싱은 이러한 데이터 유실 문제를 해결하고, 분산 시스템에서 데이터의 무결성과 확장성을 보장하기 위해 도입되었다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
이벤트 소싱 시스템은 모든 상태 변화를 **불변(Immutable) 이벤트**로 기록하며, 이를 **Append-Only** 방식으로 저장한다.

```text
[ Command ] --(Execute)--> [ Domain Engine ] --(Create Event)--> [ Event Store ]
                                                                      |
[ Snapshot ] <--(Restore)-- [ Aggregate Root ] <--(Replay)------------+
                                     |
                                     +---(Publish)---> [ External System ]

<Bilingual ASCII Diagram: Event Sourcing Workflow>
- Event Store: 모든 이벤트(OrderCreated, OrderPaid 등)를 순차적으로 영구 저장
- Replay: 저장된 이벤트를 순서대로 재생하여 객체의 최종 상태 복원 (Snapshot 활용)
- Snapshot: 이벤트가 너무 많아질 때 일정 시점의 상태를 캐싱하여 복원 속도 향상
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)
| 비교 항목 | 전통적 상태 저장 (State-based) | 이벤트 소싱 (Event-based) |
| :--- | :--- | :--- |
| **저장 방식** | CRUD (덮어쓰기/삭제) | Append-Only (이벤트 추가) |
| **정보의 질** | 최종 상태만 존재 (맥락 유실) | 모든 이력 존재 (맥락 보존) |
| **성능 (쓰기)** | 락(Lock)에 의한 병목 가능성 | 락 없는 순차 쓰기로 매우 빠름 |
| **성능 (읽기)** | 매우 빠름 (즉시 조회) | 느림 (Replay 연산 필요 -> CQRS 필요) |
| **장애 복구** | 백업 시점으로만 복원 가능 | 특정 시점으로 완벽 복구 가능 |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
- **감리 포인트**: 이벤트 스토어의 데이터가 위변조되지 않도록 **WORM(Write Once Read Many)** 속성을 보장하는지 점검해야 한다. 또한 이벤트 버전 관리(Upcasting) 전략이 수립되었는지 확인이 필요하다.
- **전략적 판단**: 금융, 결제, 물류 추적과 같이 데이터의 신뢰성과 감사 추적이 비즈니스의 핵심인 도메인에 강력 추천한다. 단순한 정보 게시판 등에는 오버헤드가 크므로 지양한다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
이벤트 소싱은 단순히 기술적인 저장 방식을 넘어, 비즈니스의 흐름을 데이터로 포착하는 강력한 수단이다. 향후 인공지능(AI) 기반의 행위 분석이나 데이터 분석을 위한 고품질 로우 데이터(Raw Data) 공급원으로서 그 가치가 더욱 높아질 것이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 데이터 영속성(Persistence), 아키텍처 스타일
- **하위 개념**: Event Store, Replay, Snapshot, Upcasting
- **연관 개념**: CQRS, DDD, EDA, 결과적 일관성

### 👶 어린이를 위한 3줄 비유 설명
- **보통 일기**: 오늘 기분을 "행복함"이라고 쓰고, 내일 기분이 나빠지면 그걸 지우고 "슬픔"으로 고쳐 쓰는 거예요.
- **이벤트 소싱**: 일기장에 "오늘은 떡볶이를 먹어서 기뻤다", "동생이랑 싸워서 슬펐다"라고 모든 일을 순서대로 다 써두는 거예요.
- **장점**: 나중에 다시 읽어보면 내가 왜 기쁘고 슬펐는지 언제든지 다 알 수 있어요!
