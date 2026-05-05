+++
weight = 194
title = "멱등성 (Idempotency)"
date = "2024-03-24"
[extra]
categories = "studynote-devops-sre"
+++
## 0. 핵심 인사이트

>   | [Processing...] -> OK, A created.

> 📝 모범 답안

- **동일 결과 보장:** 연산을 여러 번 수행하더라도 시스템의 상태가 한 번 수행했을 때와 동일하게 유지되는 성질.
- **자동화의 안전장치:** 네트워크 오류나 타임아웃으로 인한 재시도(Retry) 상황에서 데이터 중복 생성이나 중복 결제 같은 부작용을 방지.
- **IaC/API 설계 원칙:** 테라폼, 앤서블 등 현대적 도구들이 인프라를 "추가"하는 것이 아니라 "목표 상태로 선언"하여 중복 실행에도 안전하게 설계된 핵심 이유.

### 1. 개요 및 필요성
수학에서 $f(f(x)) = f(x)$로 정의되는 멱등성은 컴퓨터 과학, 특히 분산 시스템과 DevOps에서 가장 중요한 설계 원칙 중 하나입니다. 불안정한 네트워크 환경에서는 요청이 성공했는지 알 수 없어 다시 보내는 경우가 빈번한데, 이때 시스템이 멱등적이지 않으면 치명적인 데이터 부패가 발생합니다. 인프라를 코드로 관리할 때도 "서버 1대를 추가해라"가 아닌 "서버는 1대여야 한다"는 선언적 방식이 멱등성을 보장합니다.

### 2. 구성요소
멱등성은 요청의 중복 처리를 내부적으로 필터링하거나 상태를 체크하여 구현됩니다.

```text
[ Idempotent API Workflow ]

   Client                Server (Target State: Storage A created)
     |                      |
     | --(1) Create A --     |  (Timeout! No Ack)   |
     |                      |
     | --(2) Create A -->   | [Check State] -> "A already exists."
     | <--- (3) OK (A) ---  | (No action, just returns success)
     |                      |

[ Idempotency in IaC (e.g. Terraform) ]
- Non-idempotent script: `aws ec2 run-instances` (Run 3 times = 3 instances)
- Idempotent declaration: `resource "aws_instance" "web" { count = 1 }`
  (Run 100 times = Always 1 instance)
```

**구현 기법:**
1. **멱등키 (Idempotency Key):** 요청 헤더에 고유한 UUID를 포함시켜, 서버가 일정 시간 동안 동일한 키의 요청을 기억하고 무시하거나 캐시된 결과를 반환.
2. **상태 기반 선언 (State-based):** 현재 상태를 먼저 조회(Read)하고 목표 상태와 다를 경우에만 변경(Write) 수행.
3. **데이터베이스 제약 조건:** Unique Key나 `INSERT ... ON DUPLICATE KEY UPDATE` 구문을 활용하여 물리적인 중복 차단.

### 3. 구조 및 동작 원리

| 비교 항목 | 멱등적 연산 (Idempotent) | 비멱등적 연산 (Non-idempotent) |
| :--- | :--- | :--- |
| **HTTP Method** | GET, PUT, DELETE, HEAD | POST, PATCH (일반적으로) |
| **실행 결과** | 여러 번 실행해도 상태 변화 없음 | 실행할 때마다 상태가 계속 변함 |
| **대표 예시** | "전등 스위치를 켜짐 상태로 둬라" | "전등 스위치를 눌러라 (Toggle)" |
| **장애 복구** | 단순 재시도(Retry) 가능 | 복잡한 보상 트랜잭션 필요 |

### 4. 비교 및 트레이드오프
- **실무 적용:** 결제 시스템 아키텍처에서 주문 번호를 멱등키로 사용하여, 사용자가 결제 버튼을 실수로 두 번 클릭하거나 통신 장애로 재시도가 일어나도 실제 출금은 한 번만 이루어지도록 보장합니다.
- **기술사적 판단:** 멱등성은 시스템의 '회복 탄력성(Resiliency)'을 결정짓는 척도입니다. 기술사는 모든 API와 인프라 스크립트 설계 시 "이 작업을 두 번 실행하면 어떻게 되는가?"를 스스로 질문해야 합니다. 특히 분산 트랜잭션이나 메시지 큐(Kafka)의 'At-least-once' 전달 환경에서는 컨슈머 측의 멱등적 처리가 시스템 전체의 데이터 무결성을 유지하는 유일한 방어선입니다.

### 5. 실무 적용 및 최적화 기법
멱등성은 복잡한 에러 처리 로직을 단순화시켜 시스템의 유지보수 비용을 획기적으로 낮춥니다. 최근의 'Self-healing' 인프라나 'Autonomous Computing' 역시 멱등성을 전제로 한 끝없는 상태 동기화 루프(Reconciliation Loop)를 통해 구현됩니다. 따라서 멱등적 설계는 현대 소프트웨어 엔지니어가 갖춰야 할 가장 기본적인 품질 표준입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** Distributed Systems, API Design, Fault Tolerance
- **하위 개념:** Idempotency Key, Side Effect, State Machine
- **연관 기술:** RESTful API, Terraform, Ansible, Kafka (Exactly-once), Stripe API

### 👶 어린이를 위한 3줄 비유 설명
1. 엘리베이터 버튼을 한 번 누르나 열 번 누르나, 엘리베이터가 우리 층으로 오는 결과는 똑같죠? 이게 '멱등성'이에요.
2. 하지만 TV 채널을 바꾸는 버튼은 한 번 누를 때마다 채널이 계속 바뀌니까 멱등성이 없는 거예요.
3. 컴퓨터 세상에서는 복잡한 일을 할 때 엘리베이터 버튼처럼 '항상 똑같은 결과'가 나오게 만드는 게 아주 중요하답니다.
