+++
weight = 314
title = "314. 인터럽트 구동 I/O (Interrupt-driven I/O)"
date = "2026-03-26"
[extra]
categories = "studynote-computer-architecture"
+++
## 0. 핵심 인사이트

> **핵심**: 인터럽트 구동 I/O는 I/O 장치가 작업 완료를 CPU에 알리기 위해 Interrupt 신호를 보내 CPU가 다른 유용한 연산을 수행하다가 Interrupt 발생 시 즉시 대응하는 방식으로, 폴링 대비 CPU 이용률을 극대화한다.
> 2. **가치**: 고속 I/O 환경에서 폴링의 Busy-waiting으로 인한 CPU 낭비를 제거하여, 동일 시간에 더 많은 연산을 완료할 수 있게 하며, 시스템 전체 처리량(Throughput)을 획기적으로 향상시켰다.
> 3. **융합**: DMA, APIC, MSI(Message Signaled Interrupt) 등 다른 하드웨어 메커니즘과 결합되어 현대 컴퓨터의 I/O 처리 표준을 이루며, OS의 스케줄러와 긴밀하게 통합된다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 탄생 배경: 폴링의 한계

이전 세대의 컴퓨터에서는 CPU가 I/O 장치의 상태를 확인하기 위해 폴링(Polling) 방식을 사용했다. CPU가 "데이터 준비됐어?"라고 1초에 수백만 번씩 물어보는 방식인데, 이는 CPU 사이클의 극심한 낭비를 야기했다.

```
[폴링 방식의 문제: CPU 시간의 엄청난 낭비]

CPU 시간 = 1초 (1GHz 시스템)

polling 루프: ████████████████████████████████████████ 99.9% (바쁜 대기)
실제 연산:    █                                             0.1%

>>> CPU의 능력 99.9%가 아무 의미 없는 "준비됐어?" 질문에 소모되고 있다
```

**[다이어그램 해설]** 폴링 방식에서 CPU는 I/O 장치가 준비될 때까지 의미 없는 루프를 실행하며 대기한다. 1GHz CPU에서 10Gbps 네트워크 카드 하나의 데이터를 기다린다면, CPU는 매 사이클마다 버스에서 상태 레지스터를 읽어야 하므로 수백만 사이클이 낭비된다. 이 문제를 해결하기 위해 등장한 것이 Interrupt-driven I/O다.

### Interrupt-driven I/O의 혁신

Interrupt-driven I/O는 "CPU가 I/O를 폴링하는 것이 아니라, I/O가 필요할 때 CPU에게 Interrupt를 건다"는 발상의 전환이다. 사장(CPU)이 직원(I/O 장치)에게 자꾸 "다 했어?"라고 물어보는 것이 아니라, 직원이 일이 끝나면 사장에게 직접 보고하듯이 하는 것이다.

```
[폴링 vs Interrupt-driven: 근본적 차이]

[폴링] CPU가 능동적으로 확인
  CPU ──▶ "데이터 준비됐어?" ──▶ I/O 장치
       ◀── "아직..." ─────────
  CPU ──▶ "데이터 준비됐어?" ──▶ I/O 장치
       ◀── "아직..." ─────────
  ... (수백만 번 반복) ...

[Interrupt] I/O가 수동적으로 보고
  I/O 장치 ──[작업 완료!]──▶ CPU
  CPU: [다른 중요 작업 수행 중]
  CPU: [파일 압축 중]
  CPU: [네트워크 패킷 처리 중]
  ... (유용한 작업 수행) ...
  ── Interrupt 수신 ──
  CPU: [해당 I/O 작업 완료 처리]
```

📢 **섹션 요약 비유:** 타이머(Interrupt)에 맞추고 TV를 보다가 알람 소리가 울릴 때만 냉장고(해당 장치)로 뛰어가서 대처하는 효율적인 방식이다. 매번 냉장고 문을 열어서 확인하지 않아도 돼서 시간을 많이 절약한다.

---

## 2. 구성요소

### 인터럽트 구동 I/O의 5단계 처리 모델

Interrupt-driven I/O는 Interrupt 발생부터 처리 완료까지 일정한 단계를 따른다. 각 단계는 엄격한 순서로 실행되며, 이전 단계의 완료 이후에만 다음 단계가 시작된다.

```
[Interrupt-driven I/O 5단계 처리 모델]

┌─────────────────────────────────────────────────────┐
│  1단계: Interrupt 발생                              │
│  I/O 장치가 INTERRUPT 신호를 시스템 버스에 발행      │
│       │                                            │
│       ▼                                            │
│  2단계: 컨텍스트 저장 (Context Save)               │
│  CPU가 현재 레지스터/PC를 스택에 백업              │
│       │                                            │
│       ▼                                            │
│  3단계: 벡터 분기 (Interrupt Vector)                │
│  CPU가 IVT에서 ISR 주소를 참조하여 점프            │
│       │                                            │
│       ▼                                            │
│  4단계: ISR 실행 (Interrupt Service Routine)       │
│  커널 모드에서 장치의 데이터를 처리                │
│       │                                            │
│       ▼                                            │
│  5단계: 컨텍스트 복구 및 반환 (Context Restore)   │
│  IRET 명령어로 원래 작업으로 복귀                  │
└─────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** 5단계 모델의 핵심은 2단계와 5단계다. Interrupt가 발생하면 CPU는 하던 작업의 상태(레지스터 값, 프로그램 카운터)를 모두 메모리 스택에 저장한다. 이 과정이 없으면 ISR이 레지스터를 수정한 뒤 반환할 때 원래 프로그램의 상태가 깨져버린다. 이 "아무 일도 없었던 것처럼" 완벽한 복구를 보장하는 메커니즘이 현대 OS의 가장 근본적인 신뢰성 보장 장치다.

### Interrupt의 Hardware 계층 vs Software 계층

Interrupt 처리는 물리적 하드웨어 IRQ(Interrupt Request) 핀에서부터 OS 커널의 ISR 핸들러까지 다층적으로 구성된다.

```
[Interrupt 처리 전체 아키텍처]

I/O 장치 (키보드)
    │
    │ (전기 신호)
    ▼
PIC / APIC (Interrupt Controller) ◀─── 여러 장치의 IRQ를 수집/우선순위 판정
    │ (INT 신호)
    ▼
CPU ( Interrupt 핀) ◀─── 물리적 신호
    │
    ▼
IVT / IDT (벡터 테이블)
    │
    ▼
ISR (Interrupt Service Routine, 커널 메모리)
```

**[다이어그램 해설]** PIC(Programmable Interrupt Controller)는 8259A 같은 칩으로, 여러 I/O 장치의 Interrupt 요청을 수집하여 가장 우선순위가 높은 요청을 CPU에 전달하는 중간 제어자 역할을 한다. APIC(Advanced PIC)는 현대의 다중 코어 시스템에서 로컬 APIC와 I/O APIC로 나뉘어 확장성을 제공한다. MSI(Message Signaled Interrupt)는 이러한 물리적 IRQ 핀을 대신하여 PCIe 장치가 메모리 쓰기를 통해 Interrupt를 표현하는 소프트웨어 인터페이스 방식이다.

### Poll vs Interrupt-Driven vs DMA 비교

|I/O 방식|CPU 개입 수준|적합한 장면|CPU 비용|하드웨어 복잡도|
|:---|:---|:---|:---|:---|
|폴링 (Programmed I/O)|100% (계속 확인)|극히 저속 장치, 극단적 단순성 요구|매우 높음 (Busy-wait)|최저|
|Interrupt-Driven I/O|Interrupt 시에만|I/O 빈도가 중간, 다양한 장치|중간|중간|
|DMA|거의 없음 (초기 설정만)|대용량 데이터 전송|최저|가장 높음|

📢 **섹션 요약 비유:** Interrupt-driven I/O는 급식실(CPU)이 메뉴를 만들기 전까지 매번 확인하러 가는 대신, 조리사(I/O 장치)가 완료되면 호루라기(Interrupt)를 불어 알려주는 방식이다. 이를 통해 급식실은 다른 요리(연산)를 준비하는 데 모든 시간을 집중할 수 있다.

---

## 3. 구조 및 동작 원리

### Interrupt Storm 현상과 고속 I/O의 딜레마

Interrupt-driven I/O의 가장 큰 과제는 고속 장치에서의 Interrupt 폭발(Interrupt Storm)이다. 10Gbps 네트워크 카드와 같이 초고속으로 데이터가 도착하는 장치는 1초에 수십만 개의 Interrupt를 생성할 수 있다.

```
[Interrupt Storm 시나리오]

10Gbps NIC: 1초에 1,000,000 패킷 도착
  → Interrupt 빈도 = 1,000,000 interrupts/sec
  → CPU가 각 Interrupt 처리 = 5μs 소요
  → CPU 활용률 = 5,000,000μs / 1,000,000μs = 500% (CPU 포화!)

>>> CPU가 Interrupt 처리만으로도 이미 과부하
```

이 딜레마를 해결하기 위해 고속 장치에서는 폴링과 Interrupt를 하이브리드로 결합한 NAPI(New API)나 DPDK(Data Plane Development Kit)를 사용한다. 평소에는 Interrupt를 사용하다가 Interrupt 빈도가 임계치를 넘으면 폴링 모드로 전환한다.

| 해결방식|핵심 아이디어|CPU 부담|처리 레이턴시|적용|
|:---|:---|:---|:---|:---|
|Traditional Interrupt| Interrupt마다 즉시 처리|높음|최저|저속 장치|
|NAPI (Linux)|Interrupt → 폴링 모드 전환|중간|중간|1~10Gbps NIC|
|DPDK|Interrupt 완전 비활성화|최저|최저|10Gbps+ NIC|
|Hybrid (설정상 기본)| Interrupt coalescing|중간|중간|대부분의 고속 장치|

### OS 커널 설계와의 융합

Interrupt는 OS 커널의 스케줄러(Scheduler)와 긴밀하게 통합된다. Interrupt 발생 시 현재 프로세스의 상태가 스택에 저장되고, ISR 실행 후에는 인터럽트로부터 복귀될 때 스케줄링(Scheduling) 결정이 발생하여 더 높은 우선순위의 프로세스가 실행될 수 있다.

```
[Interrupt와 OS 스케줄링의 통합]

[프로세스 A 실행 중]
    │
    │ Timer Interrupt 발생
    ▼
[컨텍스트 저장: 프로세스 A 상태 → 스택]
    │
    ▼
[ISR 실행: 타이머.tick()] ◀── 커널 모드
    │
    ▼
[ISR 완료 + scheduler_wakeup() 실행]
    │
    ▼
[컨텍스트 복구: 프로세스 A 또는 더 높은 우선순위 프로세스 B로 전환]
```

**[다이어그램 해설]** Interrupt는 OS의 선점형 멀티태스킹(Preemptive Multitasking)을 구현하는 가장 근본적인 장치이다. 타이머 Interrupt는 OS가 프로세스 실행 시간을 엄격하게 관리하고, 우선순위에 따라 프로세스를 선점(Preempt)하는 핵심 매커니즘이다. Interrupt가 없다면 OS는 프로세스가 자발적으로 CPU를 놓기를 기다려야 하므로, 한 프로세스가 무한 루프에 빠지면 전체 시스템이 멈추게 된다.

📢 **섹션 요약 비유:** Interrupt-driven I/O는 식당 관리 시스템에서 셰프(I/O 장치)가 요리를 끝낼 때마다 종을 쳐서(Interrupt) 서빙 담당자(CPU)에게 알려주는 것과 같다. 이를 통해 셰프가 아무 일도 하지 않는 동안 서빙 담당자가 홀에서 다른 업무(Task)를 수행할 수 있어 식당 운영 효율이 극대화된다.

---

## 4. 비교 및 트레이드오프

### 시나리오 1: 고속 네트워크 카드를 사용한 서버 설계

**상황**: 100Gbps 네트워크를 통한 대규모 패킷 처리 서버를 설계해야 한다.

**분석**: 전통적인 Interrupt-driven I/O는 패킷마다 Interrupt를 생성하므로 100Gbps 환경에서는 Interrupt storm이 발생한다. 이를 해결하기 위해 interrupt coalescing(Interrupt 묶음 처리)을 설정하여 수백 개의 패킷이 도착한 후 한 번에 Interrupt를 발생시키는 방식을 사용한다.

**설계 의사결정**: interrupt moderation granularity 설정 시, 너무 크게 설정하면 레이턴시가 높아지고 너무 작게 설정하면 Interrupt storm이 다시 나타난다. 따라서 균형점을 실험적으로 찾아야 한다.

### 시나리오 2: 임베디드 시스템의 실시간 Interrupt 응답성 보장

**상황**: 자동차 ABS(Anti-lock Braking System)에서 휠 속도 센서 Interrupt의 응답 시간이 1ms 이내여야 한다.

**분석**: Interrupt 응답 시간(Latency)은 하드웨어 Interrupt 핀에서 ISR 첫 명령어 실행까지의 시간이다. 이를 위해서는 선점형 커널(Preemptive Kernel) 설정이 필요하며, 높은 Interrupt 우선순위와 짧은 ISR 작성이 필수적이다.

```
[Interrupt 지연 시간 분석]

 Interrupt 발생 ──▶ CPU 인지 ──▶ IVT 참조 ──▶ ISR 시작
   0.1μs         0.2μs        0.1μs        0.5μs
   │              │            │            │
   └──────────────┴────────────┴────────────┘
                 총 지연 시간: ~1μs (최적 조건)

대부분의 지연은 IVT/IDT 참조(메모리 접근)와 ISR 시작 결정에서 발생
>>> 이를 줄이려면 L1 캐시에 ISR 코드가 위치해야 함
```

### 시나리오 3: 가상머신 환경에서의 Interrupt 전달

**상황**: VMware ESXi에서 실행되는 VM이 USB 장치를 사용해야 한다.

**분석**: VM에서 발생하는 Interrupt는 먼저 하이퍼바이저에게 전달되고, 하이퍼바이저가 이를 VM에 재삽입해야 한다. 이 과정은 물리적 Interrupt보다 수 배 더 긴 레이턴시를 유발하며, 실시간성이 중요한 VM에서는 문제가 될 수 있다. SR-IOV를 사용하면 VM이 직접 장치에 접근하여 Interrupt를 수신할 수 있다.

**운영 체크리스트**:
- [ ] Interrupt storm이 발생하지 않는지 /proc/interrupts를 통해 모니터링했는가?
- [ ] 높은 Interrupt 빈도를 보이는 장치는 interrupt coalescing 설정을 적용했는가?
- [ ] 실시간성이 중요한 응용 프로그램은 전용 CPU 코어(Dedicated Core)에서 Interrupt 처리를 수행하게 설정했는가?
- [ ] MSI 방식 Interrupt를 지원하는 장치는 가능한 MSI를 사용하도록 설정했는가?

**안티패턴**: NVMe SSD 환경에서 Interrupt mode를 레거시(Legacy) INTx로 설정하여 MSI-X 모드로 설정하지 않는 것. INTx는 Interrupt 공유로 인해 동시에 여러 Interrupt가 발생하면 처리가 지연되지만, MSI-X는 각 큐에 대해 독립적인 Interrupt를 생성하여 처리 병목을 제거한다.

📢 **섹션 요약 비유:** Interrupt storm은 식당에서 모든 셰프가 동시에 종을 쳐서(Interrupt) 서빙 담당자(CPU)가 어느 것부터 처리해야 할지 몰라 아무것도 하지 못하는 마비 상태다. 이를 방지하려면 셰프들이 약속(Interrupt moderation)을 정해 한꺼번에 종을 치되, 자주 치지 않도록 해야 한다.

---

## 5. 실무 적용 및 최적화 기법

### Interrupt 기술의 정량적 발전

|마일스톤|기술|Interrupt 수|지연 시간(Latency)|비고|
|:---|:---|:---|:---|:---|
|1980년대|8259A PIC|8개|15μs|IBM PC/AT|
|1990년대|APIC (82093AA)|24개|5μs|멀티프로세서 지원|
|2000년대|IOAPIC + MSI|224개|2μs|PCIe 통합|
|2010년대|ARM GICv2|480개|0.5μs|Mobile SoC|
|2026년|GICv5 / RISC-V PLIC|1024개|0.1μs|실시간 지원|

### 미래 전망: APIC에서 Message Unit으로

현대 시스템에서는 물리적 IRQ 핀을 사용하는 전통적 APIC 방식이 점진적으로 도태되고 있다. MSI(Message Signaled Interrupt)는 PCIe 장치가 메모리 쓰기 트랜잭션을 통해 Interrupt를 표현하는 방식이다.

```
[Interrupt 전달 방식의 진화]

[물리적 IRQ 핀 시대]
  장치 ──(전선)──▶ APIC ──(INT 신호)──▶ CPU
  문제: 핀 수 제한, 공유 필수, 라우팅 복잡

[MSI 시대]
  장치 ──(PCIe 트랜잭션)──▶ 루트 포트 ──▶ CPU
  장점: 핀이 무한(이론상), 공유 없음, SW 라우팅 가능
```

**[다이어그램 해설]** MSI의 가장 큰 혁명은 Interrupt의 물리적 전선이라는 개념을 추상화했다는 점이다. 모든 Interrupt가 PCIe의 메모리 쓰기 트랜잭션으로 표현되므로, Interrupt의 라우팅이 소프트웨어(OS의 ACPI 테이블)로 완전히 제어될 수 있다. 이로 인해 핀 부족 문제도 해결되고, Interrupt 전달 경로도 동적으로 변경 가능해진다.

📢 **섹션 요약 비유:** Interrupt 전달 방식의 진화는 수동 전화 교환반에서 자동화된 전화 교환 시스템으로 이동한 것과 같다. 종업원이 각 테이블에 직접 찾아가서 알려드리던(물리적 IRQ) 방식에서, 중앙 교환대가 모든 통화를 자동으로 연결하는(MSI) 방식으로 전환된 것이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| 인터럽트 벡터 (Interrupt Vector) | Interrupt 번호로부터 ISR 주소를 참조하는 IVT/IDT 테이블 항목 |
| ISR (Interrupt Service Routine) | Interrupt 발생 시 커널 모드에서 실행되는 실제 처리 핸들러 |
| PIC/APIC | I/O 장치들의 Interrupt를 수집, 우선순위 판정, CPU에 전달하는 전용 제어기 |
| DMA (Direct Memory Access) | Interrupt-driven I/O와 함께 사용되어 대용량 데이터 전송에서 CPU 부담을 제거 |
| MSI (Message Signaled Interrupt) | PCIe 기반 시스템의 Interrupt를 메모리 쓰기 트랜잭션으로 표현하는 최신 방식 |

---

### 👶 어린이를 위한 3줄 비유 설명
1. Interrupt-driven I/O는 조리사가 음식을 다 끝내면 손을 들고 "다 됐습니다!(Interrupt)"라고 종을 쳐서(신호) 매니저(CPU)에게 바로 알려주는 방식이다. 매니저가 그때마다 조리사에게 가서 확인하고 오는 수고를 줄였다.
2. 그런데 셰프가 너무 빨리 음식을 만들어서(고속 하드디스크) 1초에 1만 번이나 종을 치면, 매니저가 어느 종부터 맞춰야 할지 몰라 정상적으로 일할 수 없게 된다. 이것이 인터럽트 폭풍(Interrupt storm)이다.
3. 그래서 요즘 식당(컴퓨터)에서는 "종을 너무 자꾸 치지 말고, 100개쯤 되면 한 번에 쳐!"라고 조절(Moderation) 설정을 해두는데, NVMe SSD나 고속 랜카드에서는 이런 튜닝(Tuning)이 성능을 결정한다.