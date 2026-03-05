+++
title = "사가 패턴 (Saga Pattern)"
description = "마이크로서비스 아키텍처에서 분산 트랜잭션을 보상 트랜잭션을 통해 구현하는 패턴으로 2PC의 한계를 극복"
date = 2024-05-15
[taxonomies]
tags = ["Saga-Pattern", "MSA", "Distributed-Transaction", "Compensating-Transaction", "Eventual-Consistency"]
+++

# 사가 패턴 (Saga Pattern)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 마이크로서비스 아키텍처(MSA)에서 분산 트랜잭션을 **연속된 로컬 트랜잭션의 시퀀스**로 분해하고, 각 단계 실패 시 **보상 트랜잭션(Compensating Transaction)**을 역순으로 실행하여 결과적 일관성(Eventual Consistency)을 보장하는 디자인 패턴입니다.
> 2. **가치**: 2PC(Two-Phase Commit)의 글로벌 락(Lock)으로 인한 성능 병목과 가용성 저하를 해결하고, 각 서비스의 자율성을 유지하면서도 비즈니스 트랜잭션의 원자성(Atomicity)을 달성합니다.
> 3. **융합**: 이벤트 소싱(Event Sourcing), CQRS, 메시지 큐(Kafka/RabbitMQ), 오케스트레이션(Orchestration) vs 코레오그래피(Choreography) 방식과 결합하여 MSA 데이터 일관성 문제를 해결합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**사가 패턴(Saga Pattern)**은 1987년 Princeton 대학의 Hector Garcia-Molina와 Kenneth Salem이 제안한 분산 트랜잭션 패턴으로, **장기 실행되는 트랜잭션(Long-Running Transaction)을 여러 개의 로컬 트랜잭션으로 분해**하고, 각 로컬 트랜잭션은 자신의 DB에서만 실행됩니다. 핵심 개념:
- **순차적 로컬 트랜잭션**: T1 -> T2 -> T3 -> ... -> Tn
- **보상 트랜잭션(Compensating Transaction)**: T1 실패 시 C1(되돌리기) 실행
- **결과적 일관성(Eventual Consistency)**: 즉시 일관성이 아닌, 최종적으로 일관성 달성

### 2. 구체적인 일상생활 비유
여행 패키지 예약을 상상해 보세요. 항공권 -> 호텔 -> 렌터카 -> 투어를 순서대로 예약합니다. **2PC 방식**은 모든 예약이 동시에 가능한지 확인한 후 일괄 예약합니다. 하나라도 불가하면 전체 취소. 모두가 대기해야 합니다. **사가 패턴**은 순서대로 예약합니다. 항공권 OK -> 호텔 OK -> 렌터카 실패! 그러면 호텔 취소 -> 항공권 취소를 역순으로 실행합니다. 각 단계는 독립적이고, 실패 시 되돌리는 방법이 정의되어 있습니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (2PC의 글로벌 락 문제)**:
   모놀리식에서는 단일 DB 트랜잭션(ACID)으로 일관성을 보장했습니다. MSA에서는 각 서비스가 자체 DB를 가집니다. 분산 트랜잭션을 위해 2PC(Two-Phase Commit)를 사용하면: 1) 모든 참여자가 락을 잡고 대기 (성능 저하) 2) 코디네이터 장애 시 전체 차단 3) 네트워크 파티션 시 데드락. 이는 MSA의 핵심 가치인 가용성(Availability)과 상충합니다.

2. **혁신적 패러다임 변화의 시작**:
   2015년 Chris Richardson이 "Microservices Patterns"에서 사가 패턴을 MSA 트랜잭션 해법으로 재소개했습니다. 넷플릭스, Uber, 아마존 등이 대규모 분산 시스템에서 사가 패턴을 실제 구현하여 검증했습니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   이커머스 주문, 항공권 예약, 금융 결제 등 장기 실행 트랜잭션이 많은 도메인에서 MSA 도입과 함께 사가 패턴이 필수가 되었습니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Component) | 상세 역할 | 내부 동작 메커니즘 | 비고 |
| :--- | :--- | :--- | :--- |
| **Local Transaction** | 단일 서비스의 DB 트랜잭션 | ACID 보장, 자체 DB만 수정 | T1, T2, T3... |
| **Compensating Transaction** | 로컬 트랜잭션을 되돌리는 작업 | 비즈니스적 의미의 취소/환불 | C1, C2, C3... |
| **Saga Coordinator** | 사가 실행 순서 관리 (Orchestration) | 상태 머신, 이벤트 발행 | Order Service |
| **Event/Message** | 서비스 간 통신 매개체 | Kafka, RabbitMQ | 주문 생성됨 -> 재고 차감 요청 |
| **Saga Log** | 트랜잭션 상태 기록 | Outbox Pattern, Event Sourcing | 장애 복구용 |

### 2. 정교한 구조 다이어그램: 사가 패턴 실행 흐름

```text
=====================================================================================================
                      [ Saga Pattern - Order Processing Example ]
=====================================================================================================

  [ Happy Path: All Transactions Succeed ]
  ════════════════════════════════════════

  Order Service           Inventory Service        Payment Service          Shipping Service
       |                        |                        |                        |
       | 1. Create Order        |                        |                        |
       | (Local Tx: PENDING)    |                        |                        |
       v                        |                        |                        |
  +---------+                   |                        |                        |
  | Order   |                   |                        |                        |
  | Created |                   |                        |                        |
  +----+----+                   |                        |                        |
       |                        |                        |                        |
       | 2. ReserveInventory    |                        |                        |
       +----------------------->|                        |                        |
       |                        | (Local Tx: RESERVE)    |                        |
       |                        v                        |                        |
       |                   +---------+                   |                        |
       |                   | Stock   |                   |                        |
       |                   | Reserved|                   |                        |
       |                   +----+----+                   |                        |
       |                        |                        |                        |
       | 3. InventoryReserved   |                        |                        |
       |<-----------------------+                        |                        |
       |                        |                        |                        |
       | 4. ProcessPayment      |                        |                        |
       +----------------------------------------------->|                        |
       |                        |                        | (Local Tx: CHARGE)     |
       |                        |                        v                        |
       |                        |                   +---------+                   |
       |                        |                   | Payment |                   |
       |                        |                   | Success |                   |
       |                        |                   +----+----+                   |
       |                        |                        |                        |
       | 5. PaymentCompleted    |                        |                        |
       |<-----------------------------------------------+                        |
       |                        |                        |                        |
       | 6. ShipOrder           |                        |                        |
       +------------------------------------------------------+--------------->|
       |                        |                        |                        |
       |                        |                        | 7. StartShipping       |
       |                        |                        | (Local Tx: SHIP)       |
       |                        |                        v                        |
       |                        |                        |                   +---------+
       |                        |                        |                   | Shipped |
       |                        |                        |                   +----+----+
       |                        |                        |                        |
       | 8. ShippingCompleted   |                        |                        |
       |<--------------------------------------------------------------+--------+
       |                        |                        |                        |
       | 9. Complete Order      |                        |                        |
       | (Local Tx: COMPLETED)  |                        |                        |
       v                        |                        |                        |
  +---------+                   |                        |                        |
  | Order   |                   |                        |                        |
  | Complete|                   |                        |                        |
  +---------+                   |                        |                        |


  [ Failure Path: Payment Fails -> Compensating Transactions ]
  ══════════════════════════════════════════════════════════════

  Order Service           Inventory Service        Payment Service
       |                        |                        |
       | 1-4. Same as above...  |                        |
       |                        |                        |
       | 5. ProcessPayment      |                        |
       +----------------------------------------------->|
       |                        |                        | X Payment FAILED!
       |                        |                        v
       | 6. PaymentFailed       |                   +---------+
       |<-----------------------------------------------+ Payment |
       |                        |                        | Failed  |
       |                        |                        +---------+
       |                        |                        |
       | 7. COMPENSATE: ReleaseInventory (C2)
       +----------------------->|
       |                        | (Local Tx: RELEASE)
       |                        v
       |                   +---------+
       |                   | Stock   |
       |                   | Released|
       |                   +----+----+
       |                        |
       | 8. InventoryReleased   |
       |<-----------------------+
       |                        |
       | 9. COMPENSATE: CancelOrder (C1)
       | (Local Tx: CANCELLED)  |
       v                        |
  +---------+                   |
  | Order   |                   |
  | Cancelled                   |
  +---------+                   |

=====================================================================================================

                      [ Saga Coordination Patterns ]
=====================================================================================================

  ORCHESTRATION (중앙 제어):                    CHOREOGRAPHY (분산 제어):
  +------------------+                        +------------------+
  | Order Service    |                        | Order Service    |
  | (Orchestrator)   |                        | (Event Producer) |
  |                  |                        |                  |
  | 1. Start Saga    |                        | OrderCreated     |
  | 2. Call T1       |                        | Event Published  |
  | 3. Call T2       |                        +--------+---------+
  | 4. Call T3       |                                 |
  | 5. If fail, call|                          v      |      v
  |    C2, C1       |                 +-------+ +-----+ +------+
  +------------------+                 | Inv   | | Pay | | Ship |
                                       | Svc   | | Svc | | Svc  |
  Centralized logic                    |       | |     | |      |
  Easier to understand                 +-------+ +-----+ +------+
  Single point of failure              Each service reacts to events
                                       More resilient
                                       Harder to debug

=====================================================================================================
```

### 3. 싵층 동작 원리 (사가 패턴 핵심 메커니즘)

**1. 보상 트랜잭션 (Compensating Transaction)**
보상 트랜잭션은 기존 트랜잭션을 되돌리는 비즈니스적 작업입니다. 기술적 롤백(Rollback)이 아닙니다:
- **항공권 예약 취소**: 예약 레코드 삭제가 아니라 "취소됨" 상태로 변경
- **결제 환불**: 결제 내역 삭제가 아니라 "환불" 내역 생성
- **재고 복원**: 예약된 재고를 다시 가용 재고로 변경

**2. 코레오그래피 vs 오케스트레이션**
- **코레오그래피(Choreography)**: 각 서비스가 이벤트를 발행/구독하여 자율적으로 다음 단계 실행. 느슨한 결합, 디버깅 어려움.
- **오케스트레이션(Orchestration)**: 중앙 코디네이터(오케스트레이터)가 전체 흐름 제어. 명확한 제어, 단일 실패점.

**3. 아이솔레이션 문제 (Isolation Issues)**
사가는 ACID의 I(Isolation)를 보장하지 않습니다. 중간 상태가 다른 트랜잭션에 노출될 수 있습니다:
- **Lost Update**: 동시에 두 사가가 같은 데이터 수정
- **Dirty Read**: 커밋되지 않은 중간 상태 읽기
- **Fuzzy Read**: 같은 데이터를 두 번 읽었는데 값이 다름

해결책: **Semantic Lock(의미적 잠금)** - "예약 중" 상태로 표시하여 다른 트랜잭션이 접근하지 않도록 함.

### 4. 핵심 알고리즘 및 실무 코드 예시

**오케스트레이션 방식 사가 (Python 예시)**

```python
# order/saga_orchestrator.py
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Callable, Dict, List
import logging

logger = logging.getLogger(__name__)

class SagaStatus(Enum):
    STARTED = "started"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    COMPENSATED = "compensated"
    FAILED = "failed"

@dataclass
class SagaStep:
    name: str
    action: Callable  # Forward transaction
    compensate: Callable  # Compensating transaction
    status: str = "pending"

class OrderSagaOrchestrator:
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.status = SagaStatus.STARTED
        self.completed_steps: List[str] = []
        self.steps: List[SagaStep] = [
            SagaStep(
                name="reserve_inventory",
                action=self._reserve_inventory,
                compensate=self._release_inventory
            ),
            SagaStep(
                name="process_payment",
                action=self._process_payment,
                compensate=self._refund_payment
            ),
            SagaStep(
                name="create_shipment",
                action=self._create_shipment,
                compensate=self._cancel_shipment
            ),
        ]

    async def execute(self):
        """Execute saga steps sequentially."""
        for step in self.steps:
            try:
                logger.info(f"Executing step: {step.name}")
                await step.action(self.order_id)
                self.completed_steps.append(step.name)
                step.status = "completed"

            except Exception as e:
                logger.error(f"Step {step.name} failed: {e}")
                step.status = "failed"
                self.status = SagaStatus.COMPENSATING

                # Execute compensating transactions in reverse order
                await self._compensate()
                self.status = SagaStatus.COMPENSATED
                return

        self.status = SagaStatus.COMPLETED
        logger.info(f"Saga completed successfully: {self.order_id}")

    async def _compensate(self):
        """Execute compensating transactions in reverse order."""
        logger.info(f"Starting compensation for order: {self.order_id}")

        # Reverse the completed steps
        for step_name in reversed(self.completed_steps):
            step = next(s for s in self.steps if s.name == step_name)
            try:
                logger.info(f"Compensating step: {step.name}")
                await step.compensate(self.order_id)
                step.status = "compensated"
            except Exception as e:
                logger.error(f"Compensation failed for {step.name}: {e}")
                # Log for manual intervention
                self._log_compensation_failure(step.name, e)

    # Step implementations
    async def _reserve_inventory(self, order_id: str):
        """Call inventory service to reserve stock."""
        # HTTP call to inventory service
        response = await http_post(
            "http://inventory-service/reserve",
            {"order_id": order_id, "items": [...]}
        )
        if not response.success:
            raise Exception("Inventory reservation failed")

    async def _release_inventory(self, order_id: str):
        """Compensating: release reserved stock."""
        await http_post(
            "http://inventory-service/release",
            {"order_id": order_id}
        )

    async def _process_payment(self, order_id: str):
        """Call payment service to charge."""
        response = await http_post(
            "http://payment-service/charge",
            {"order_id": order_id, "amount": 100.00}
        )
        if not response.success:
            raise Exception("Payment processing failed")

    async def _refund_payment(self, order_id: str):
        """Compensating: refund payment."""
        await http_post(
            "http://payment-service/refund",
            {"order_id": order_id}
        )

    async def _create_shipment(self, order_id: str):
        """Call shipping service to create shipment."""
        response = await http_post(
            "http://shipping-service/create",
            {"order_id": order_id}
        )
        if not response.success:
            raise Exception("Shipment creation failed")

    async def _cancel_shipment(self, order_id: str):
        """Compensating: cancel shipment."""
        await http_post(
            "http://shipping-service/cancel",
            {"order_id": order_id}
        )

    def _log_compensation_failure(self, step_name: str, error: Exception):
        """Log compensation failure for manual intervention."""
        # Store in database for manual review
        # Send alert to operations team
        pass
```

**코레오그래피 방식 사가 (Kafka 이벤트)**

```python
# inventory_service.py (Choreography)
from kafka import KafkaConsumer, KafkaProducer
import json

class InventoryService:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'order-events',
            bootstrap_servers=['kafka:9092'],
            group_id='inventory-service'
        )
        self.producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'],
            value_serializer=lambda v: json.dumps(v).encode()
        )

    def start(self):
        for message in self.consumer:
            event = json.loads(message.value)

            if event['type'] == 'OrderCreated':
                self._handle_order_created(event)

            elif event['type'] == 'PaymentFailed':
                self._handle_payment_failed(event)

    def _handle_order_created(self, event):
        """React to OrderCreated event - reserve inventory."""
        try:
            # Reserve inventory
            self._reserve_stock(event['order_id'], event['items'])

            # Publish success event
            self.producer.send('inventory-events', {
                'type': 'InventoryReserved',
                'order_id': event['order_id'],
                'timestamp': datetime.now().isoformat()
            })

        except InsufficientStockError:
            # Publish failure event (triggers compensation)
            self.producer.send('inventory-events', {
                'type': 'InventoryReservationFailed',
                'order_id': event['order_id'],
                'reason': 'insufficient_stock',
                'timestamp': datetime.now().isoformat()
            })

    def _handle_payment_failed(self, event):
        """React to PaymentFailed event - release inventory (compensate)."""
        self._release_stock(event['order_id'])

        self.producer.send('inventory-events', {
            'type': 'InventoryReleased',
            'order_id': event['order_id'],
            'timestamp': datetime.now().isoformat()
        })
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 분산 트랜잭션 패턴 비교

| 평가 지표 | 2PC (Two-Phase Commit) | 사가 패턴 | TCC (Try-Confirm-Cancel) |
| :--- | :--- | :--- | :--- |
| **락 방식** | 글로벌 락 | 로컬 락만 | 예약 락 |
| **일관성** | Strong | Eventual | Eventual |
| **가용성** | 낮음 (코디네이터 의존) | 높음 | 높음 |
| **복잡도** | 낮음 (DB 제공) | 높음 (직접 구현) | 높음 |
| **롤백** | 자동 | 보상 트랜잭션 | Cancel 단계 |
| **적용 시나리오** | 소규모, 동기 | MSA, 장기 실행 | 재고, 좌석 예약 |

### 2. 과목 융합 관점 분석

**사가 패턴 + 이벤트 소싱**
- 이벤트 소싱으로 모든 상태 변경을 이벤트로 저장하면, 사가 실행 이력과 보상 이력이 자연스럽게 기록됩니다. 장애 시 이벤트 리플레이로 복구 가능.

**사가 패턴 + CQRS**
- 사가는 쓰기 모델(Command)의 일관성을 보장하고, CQRS로 읽기 모델(Query)을 분리하여 성능 최적화.

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 이커머스 주문 시스템**
- **문제점**: 주문 -> 재고 차감 -> 결제 -> 배송이 4개 서비스로 분리되어 있습니다. 결제 실패 시 이전 단계를 되돌려야 합니다.
- **기술사 판단 (전략)**: 오케스트레이션 방식 사가 도입. Order Service가 오케스트레이터 역할. 각 단계 실패 시 보상 트랜잭션 실행.

**[상황 B] 항공권 예약 시스템 (High Concurrency)**
- **문제점**: 수만 명이 동시에 같은 좌석을 예약하려 합니다. 2PC는 락으로 인해 성능 저하.
- **기술사 판단 (전략)**: 코레오그래피 방식 + Semantic Lock. 좌석 상태를 "예약 중"으로 표시하고, 결제 완료 시 "확정"으로 변경. 타임아웃 시 자동 해제.

### 2. 도입 시 고려사항 (체크리스트)

**기술적 고려사항**
- [ ] 코레오그래피 vs 오케스트레이션 선택
- [ ] 보상 트랜잭션 멱등성 보장 (중복 실행 방지)
- [ ] 사가 로그 저장 (장애 복구용)

**운영적 고려사항**
- [ ] 모니터링: 진행 중인 사가 상태 추적
- [ ] 수동 개입: 보상 실패 시 수동 처리 프로세스
- [ ] 타임아웃: 장기 실행 사가의 타임아웃 정책

### 3. 주의사항 및 안티패턴 (Anti-patterns)

**안티패턴 1: 보상 트랜잭션 없이 사가 구현**
- 로컬 트랜잭션만 연결하고, 실패 시 되돌리는 방법이 없으면 데이터 불일치가 발생합니다. 모든 단계에 보상 트랜잭션이 정의되어야 합니다.

**안티패턴 2: 동기식 HTTP로 사가 구현**
- 서비스 간 동기 호출은 하나의 서비스 장애가 전체 사가를 차단합니다. 비동기 메시징(Kafka) 사용 권장.

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 2PC (AS-IS) | 사가 패턴 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **락 대기 시간** | 초~분 단위 | 없음 (로컬 락만) | **지연 99% 감소** |
| **가용성** | 낮음 (코디네이터 의존) | 높음 | **가용성 향상** |
| **확장성** | 제한적 | 용이 | **수평 확장 가능** |
| **MSA 적합성** | 낮음 | 높음 | **MSA 최적화** |

### 2. 미래 전망 및 진화 방향
- **Temporal/Cadence**: 워크플로우 엔진으로 사가 패턴을 더 쉽게 구현하는 프레임워크가 대중화됩니다.
- **AI 기반 자동 보상**: 머신러닝이 실패 패턴을 학습하여 최적의 보상 전략을 자동 생성.

### 3. 참고 표준/가이드
- **Microservices Patterns (Chris Richardson)**: 사가 패턴 정의 및 구현 가이드
- **Enterprise Integration Patterns**: 메시징 기반 통합 패턴

---

## 관련 개념 맵 (Knowledge Graph)
- **[MSA](@/studynotes/4_software_engineering/1_sdlc/msa.md)**: 사가 패턴이 적용되는 아키텍처
- **[이벤트 소싱](@/studynotes/15_devops_sre/4_iac/209_event_sourcing.md)**: 사가 상태 추적 방식
- **[CQRS](@/studynotes/15_devops_sre/4_iac/208_cqrs.md)**: 명령/조회 분리
- **[Kafka](@/studynotes/15_devops_sre/1_sre/340_kafka.md)**: 사가 이벤트 전달 메시지 큐
- **[결과적 일관성](@/studynotes/8_database/2_nosql/eventual_consistency.md)**: 사가의 일관성 모델

---

## 어린이를 위한 3줄 비유 설명
1. 피자와 콜라와 감자튀김을 주문했어요. **한 번에 모두 주문하려면** 모든 가게가 준비될 때까지 기다려야 해요.
2. 사가 패턴은 **순서대로 주문**하는 거예요. 피자 OK -> 콜라 OK -> 감자튀김 sold out! 그러면 콜라 취소, 피자 취소를 순서대로 해요.
3. 덕분에 한 가게가 준비 안 되어도 다른 가게는 계속 일할 수 있어요. 전체가 멈추지 않죠!
