+++
title = "데드락 (Deadlock)"
date = "2026-03-04"
[extra]
categories = "studynotes-os"
+++

# 데드락 (Deadlock: 교착 상태)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 두 개 이상의 프로세스나 스레드가 서로가 점유하고 있는 자원을 무한정 대기하며 시스템의 흐름이 완전히 멈춰버리는 교착 상태를 의미합니다.
> 2. **가치**: 상호 배제(Mutual Exclusion), 점유 및 대기(Hold and Wait), 비선점(No Preemption), 환형 대기(Circular Wait)라는 4대 발생 조건을 이해하고 이를 관리함으로써 시스템의 신뢰성과 가용성을 보장합니다.
> 3. **융합**: 운영체제의 자원 관리를 넘어, 데이터베이스의 트랜잭션 처리, 분산 시스템의 합의 알고리즘, 그리고 병렬 프로그래밍의 동기화 메커니즘 전반에 걸쳐 해결해야 할 고질적인 아키텍처적 과제입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**데드락(Deadlock, 교착 상태)**이란 멀티프로그래밍 환경에서 한정된 시스템 자원을 사용하기 위해 경쟁하는 프로세스들이 서로 상대방이 가진 자원을 요구하며 무한정 대기 상태에 빠지는 현상을 말합니다. 어떤 프로세스도 실행을 계속할 수 없고, 외부의 개입(프로세스 강제 종료 등) 없이는 이 상태를 벗어날 수 없는 자원 할당의 논리적 모순 상태입니다.

#### 2. 💡 비유를 통한 이해
데드락은 **'외나무다리 위에서 마주친 두 염소'**에 비유할 수 있습니다.
- **상황**: 좁은 외나무다리 양 끝에서 두 염소가 걸어와 중간에서 마주쳤습니다.
- **교착**: 왼쪽 염소는 오른쪽 염소가 비켜주기를 기다리고(Hold and Wait), 오른쪽 염소는 왼쪽 염소가 물러나기를 기다립니다(Circular Wait). 서로 양보할 마음이 없고(No Preemption), 다리는 한 번에 한 마리만 지날 수 있습니다(Mutual Exclusion). 결국 두 염소는 그 자리에서 꼼짝달싹 못 하고 굶어 죽을 때까지 대기하게 됩니다. 이것이 전형적인 데드락의 모습입니다.

#### 3. 등장 배경 및 발전 과정
1.  **기존 기술의 치명적 한계점**: 초기의 일괄 처리 시스템(Batch System)에서는 자원을 미리 선점하고 실행했기에 데드락 문제가 크지 않았습니다. 하지만 시분할 시스템(Time-sharing)과 멀티코어 컴퓨팅이 도입되면서 여러 프로세스가 동시에 자원을 동적으로 요청하게 되었고, 이 과정에서 예측 불가능한 교착 상태가 빈번히 발생하여 시스템 전체가 멈추는(Hang) 현상이 나타났습니다.
2.  **혁신적 패러다임의 변화**: Edsger Dijkstra는 데드락의 개념을 명확히 정의하고, 이를 방지하기 위한 **은행가 알고리즘(Banker's Algorithm)**을 제안했습니다. 이후 운영체제 설계자들은 자원 할당 그래프(Resource Allocation Graph)를 통해 데드락을 시각화하고 수학적으로 분석하는 기법을 발전시켰습니다.
3.  **비즈니스적 요구사항**: 클라우드 서비스나 금융 트랜잭션 시스템에서 데드락은 곧 서비스 중단과 경제적 손실을 의미합니다. 따라서 현대 아키텍처에서는 데드락을 '발생 후 해결'하기보다 '설계 단계에서 예방'하거나 '효율적으로 탐지 및 복구'하는 전략이 강제됩니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 데드락 발생의 4대 필수 조건 (Coffman Conditions) (표)

| 조건명 | 상세 역할 및 의미 | 제거 시 발생하는 현상 | 비유 |
| :--- | :--- | :--- | :--- |
| **상호 배제 (Mutual Exclusion)** | 한 번에 한 프로세스만 자원 사용 가능 | 공유 자원화 (읽기 전용 등) | 화장실은 한 명만 입장 가능 |
| **점유 및 대기 (Hold and Wait)** | 자원을 가진 채로 다른 자원을 기다림 | 필요 자원을 한꺼번에 모두 요청 | 포크를 들고 칼을 기다림 |
| **비선점 (No Preemption)** | 다른 프로세스의 자원을 뺏을 수 없음 | 자원 요청 실패 시 점유 자원 반납 | 남이 쓰는 물건 뺏기 금지 |
| **환형 대기 (Circular Wait)** | 대기 고리가 원형을 이룸 | 자원에 번호를 매겨 순서대로 요청 | 꼬리에 꼬리를 무는 대기 줄 |

#### 2. 자원 할당 그래프 (Resource Allocation Graph) 및 상태 다이어그램

```text
<<< Resource Allocation Graph (Deadlock Detected) >>>

       [ Process 1 ] <------- (Has) ------- [ Resource A (Instance 1) ]
            |                                      ^
            |                                      |
         (Requests)                             (Allocated to)
            |                                      |
            v                                      |
 [ Resource B (Instance 1) ] ------- (Has) ------> [ Process 2 ]

[ 그래프 해석 ]
- 원(Process)에서 사각형(Resource)으로 가는 화살표: Request Edge (대기)
- 사각형(Resource)에서 원(Process)으로 가는 화살표: Assignment Edge (점유)
- 위 그래프처럼 Cycle(순환)이 형성되면 데드락이 발생한 것으로 판단함 (단일 인스턴스 기준).

<<< Safe State vs Unsafe State >>>

       +---------------------------------------------+
       |             Total Resource Space            |
       |                                             |
       |    +-----------------------------------+    |
       |    |          Safe State (안전)         |    |
       |    |  (Deadlock avoidance possible)    |    |
       |    +-----------------------------------+    |
       |                                             |
       |    +-----------------------------------+    |
       |    |        Unsafe State (불안전)       |    |
       |    |    (Potential for Deadlock)       |    |
       |    |        +---------------------+    |    |
       |    |        |  DEADLOCK (교착)    |    |    |
       |    |        +---------------------+    |    |
       |    +-----------------------------------+    |
       +---------------------------------------------+
```

#### 3. 심층 동작 원리: 데드락 해결 전략 4단계
1.  **예방 (Prevention)**: 4대 조건 중 하나를 원천적으로 제거합니다. (가장 엄격하지만 자원 낭비 심함)
2.  **회피 (Avoidance)**: 자원 요청 시 시스템의 상태를 검사하여 안전한 경우에만 할당합니다. (**은행가 알고리즘**)
3.  **탐지 및 복구 (Detection & Recovery)**: 시스템이 데드락에 빠지는 것을 허용하되, 주기적으로 체크하여 발견 시 복구합니다. (프로세스 종료 혹은 자원 선점)
4.  **무시 (Ignorance)**: 데드락이 매우 드물게 발생한다고 가정하고 아무 조치도 취하지 않습니다. (**타조 알고리즘**, Unix/Windows 등 대부분의 범용 OS 채택)

#### 4. 실무 수준의 데드락 방지 코드 (Java/C++ ReentrantLock 관점)

동기화 객체를 사용할 때 정해진 순서대로 락을 획득하게 하여 **환형 대기**를 방지하는 프로덕션 레벨의 패턴입니다.

```java
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

/**
 * 자원 순서 지정(Resource Ordering)을 통한 데드락 방지 예제
 */
public class DeadlockAvoidance {
    private final Lock lockA = new ReentrantLock();
    private final Lock lockB = new ReentrantLock();

    // 안티패턴: 서로 다른 순서로 락을 획득하면 데드락 위험
    public void dangerousMethod() {
        lockA.lock();
        try {
            // ... 작업 중 ...
            lockB.lock(); // 이 시점에 다른 스레드가 lockB를 쥐고 lockA를 기다리면 데드락!
            try {
                System.out.println("Executing task...");
            } finally {
                lockB.unlock();
            }
        } finally {
            lockA.unlock();
        }
    }

    // 모범 사례: 항상 정해진 순서(Global Order)로 락을 획득
    public void safeMethod() {
        // 객체의 해시코드나 고유 ID를 기준으로 순서 결정
        Lock firstLock = lockA.hashCode() < lockB.hashCode() ? lockA : lockB;
        Lock secondLock = firstLock == lockA ? lockB : lockA;

        if (firstLock.tryLock()) { // Hold and Wait 방지를 위한 tryLock 활용
            try {
                if (secondLock.tryLock()) {
                    try {
                        System.out.println("Safely executing task...");
                    } finally {
                        secondLock.unlock();
                    }
                }
            } finally {
                firstLock.unlock();
            }
        }
    }
}
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 데드락 vs 라이브락 vs 기아 상태 비교

| 비교 항목 | 데드락 (Deadlock) | 라이브락 (Livelock) | 기아 상태 (Starvation) |
| :--- | :--- | :--- | :--- |
| **정의** | 프로세스들이 멈춘 상태로 대기 | 상태가 계속 변하지만 진행은 안 됨 | 특정 프로세스가 자원을 영구히 못 받음 |
| **CPU 점유** | 0% (Waiting) | 100% (Busy Waiting) | 0% ~ 100% (다른 놈들이 다 씀) |
| **상태 변화** | 정지 (Static) | 동적 (Dynamic) | 무한 대기 |
| **해결책** | 자원 회수, 프로세스 종료 | 임의의 지연 시간 도입 (Backoff) | 우선순위 에이징 (Aging) |
| **비유** | 염소가 다리 중간에 멈춤 | 서로 비키려다 계속 부딪힘 | 나만 빼고 새치기당함 |

#### 2. 과목 융합 관점 분석: 데이터베이스 및 분산 시스템
- **데이터베이스 (Transaction Control)**: DBMS는 트랜잭션 간의 데드락을 방지하기 위해 **Wait-Die** 또는 **Wound-Wait** 타임스탬프 기반 기법을 사용합니다. 이는 선점(Preemption) 조건을 조절하여 데드락을 회피하는 전략입니다.
- **네트워크 (L2/L3 Loop)**: 네트워크 스위치 간의 환형 경로로 인한 브로드캐스트 스톰은 일종의 네트워크 데드락입니다. 이를 해결하기 위한 **STP(Spanning Tree Protocol)**는 논리적으로 링크 하나를 끊어 '환형 대기' 조건을 제거하는 예방 전략의 일환입니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)
- **시나리오 1: 대규모 이커머스 결제 처리 마이크로서비스**
  - 상황: 재고 DB와 포인트 DB를 동시에 업데이트해야 하는 트랜잭션 폭주 시 데드락 발생.
  - 판단: 2단계 커밋(2PC)은 데드락 위험과 성능 저하가 큽니다. 기술사는 **SAGA 패턴**을 도입하여 트랜잭션을 분리하고, 실패 시 보상 트랜잭션을 실행하는 낙관적 접근 방식을 선택해야 합니다.
- **시나리오 2: 임베디드 실시간 제어 시스템 (RTOS)**
  - 상황: 센서 데이터를 읽는 태스크와 제어 신호를 보내는 태스크 간의 자원 경합.
  - 판단: RTOS에서는 데드락 탐지 오버헤드를 감당할 수 없습니다. 따라서 **우선순위 상속(Priority Inheritance)** 또는 **우선순위 천장(Priority Ceiling)** 프로토콜을 사용하여 자원 점유 시간을 엄격히 제한하고 순환 대기를 원천 봉쇄해야 합니다.

#### 2. 도입 시 고려사항 (체크리스트)
- [ ] **락 획득 순서 강제화**: 코드 리뷰 시 모든 모듈이 동일한 순서로 자원을 요청하는지 검증했는가?
- [ ] **타임아웃 설정**: 모든 `lock()` 요청에 타임아웃을 적용하여 무한 대기를 방지했는가?
- [ ] **가시성 확보**: APM이나 DB 모니터링 도구를 통해 락 점유 시간과 대기 큐의 길이를 실시간 추적하고 있는가?

#### 3. 안티패턴 (Anti-patterns)
- **Nested Locks**: 여러 락을 중첩해서 쥐는 행위는 데드락의 지름길입니다. 가급적 하나의 락으로 보호하거나, 락의 범위를 최소화해야 합니다.
- **God Lock**: 시스템 전체를 하나의 락으로 묶어버리면 데드락은 없겠지만 성능(Concurrency)이 재앙 수준으로 떨어집니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과
- **정량적**: 시스템 평균 무고장 시간(MTBF) 30% 향상, 데드락으로 인한 서비스 장애 시간 80% 감소.
- **정성적**: 고가용성 아키텍처 구현을 통한 고객 신뢰도 확보, 유지보수 비용 절감.

#### 2. 미래 전망
최근 하드웨어 레벨에서 지원하는 **HTM(Hardware Transactional Memory)**은 소프트웨어적인 복잡한 락 관리 없이도 하드웨어가 직접 데드락을 방지하고 트랜잭션을 처리하게 해줍니다. 또한, Rust 언어처럼 컴파일 타임에 데이터 레이스와 락 순서를 검증하는 **Memory Safety** 언어의 확산은 데드락 문제를 런타임이 아닌 빌드 단계에서 해결하는 방향으로 나아가게 할 것입니다.

#### 3. 참고 표준/가이드
- **POSIX Threads (Pthread)**: 뮤텍스 및 조건 변수의 데드락 방지 가이드라인.
- **MISRA C/C++**: 안전 필수 시스템에서의 락 사용 표준 규격.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **[세마포어 & 뮤텍스](@/studynotes/02_operating_system/01_process_management/process_vs_thread.md)**: 데드락이 발생하는 근본 원인인 상호 배제 구현 도구.
- **[은행가 알고리즘](@/studynotes/02_operating_system/01_process_management/deadlock.md)**: 자원 할당 전 안전 상태를 시뮬레이션하는 대표적인 회피 알고리즘.
- **[식사하는 철학자 문제](@/studynotes/02_operating_system/01_process_management/deadlock.md)**: 데드락과 기아 상태를 설명하는 가장 유명한 고전 문제.
- **[우선순위 역전](@/studynotes/02_operating_system/01_process_management/deadlock.md)**: 낮은 우선순위가 락을 쥐어 높은 우선순위가 멈추는 현상.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **장난감 싸움**: 친구 A는 로봇 몸통을 가지고 다리를 기다리고, 친구 B는 다리를 가지고 몸통을 기다리면서 서로 절대 양보하지 않는 상황이에요.
2. **멈춰버린 놀이**: 둘 다 장난감을 완성할 수 없어서 신나는 놀이가 완전히 멈춰버리고, 둘 다 울상인 채로 가만히 있는 거예요.
3. **해결 방법**: 선생님이 와서 장난감을 하나 뺏어서 친구에게 주거나, 애초에 "몸통을 먼저 집은 사람만 다리를 가질 수 있어"라고 규칙을 정해야 해요.
