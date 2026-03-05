+++
title = "453. 고장 허용 시스템 (Fault Tolerant System)"
description = "고장이 발생해도 서비스를 지속하는 시스템 아키텍처"
date = "2026-03-05"
[taxonomies]
tags = ["Fault Tolerance", "고장허용", "결함허용", "Redundancy", "HA"]
categories = ["studynotes-1_computer_architecture"]
+++

# 453. 고장 허용 시스템 (Fault Tolerant System)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 고장 허용(Fault Tolerance)은 하드웨어나 소프트웨어 구성 요소의 고장이 발생해도 시스템이 정상 동작을 지속하거나, 정의된 안전 상태로 전이하여 서비스 중단을 방지하는 시스템 설계 철학이다.
> 2. **가치**: TMR(삼중 모듈 중단), 이중화, 클러스터링 등의 기법을 적용하면 단일 고장 지점(SPOF)을 제거하여 가용성 99%→99.999% 향상이 가능하며, 항공/원자력/금융 등 미션 크리티컬 분야에서 필수적이다.
> 3. **융합**: FT는 하드웨어 이중화(CPU, 메모리, 네트워크), 소프트웨어 복제(Replication), 상태 머신 복제, 합의 알고리즘(Raft/Paxos) 등 다층적으로 구현되며, 특히 분산 시스템에서 핵심 개념이다.

---

### I. 개요 (Context & Background)

#### 개념 정의

**고장 허용 시스템(Fault Tolerant System, FT)**은 시스템 내의 하나 이상의 구성 요소에 고장(Fault)이 발생하더라도, 시스템 전체가 지정된 기능을 계속 수행할 수 있는 능력을 갖춘 시스템이다. 고장 허용은 단순한 신뢰성(Reliability)과 달리, 고장 자체를 허용하면서도 서비스 중단을 막는 것이 핵심이다.

```
┌─────────────────────────────────────────────────────────────────┐
│                고장 허용 vs. 고장 방지 vs. 고장 회피            │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┬──────────────────────────────────────────────────┐
│    유형      │                    설명                          │
├──────────────┼──────────────────────────────────────────────────┤
│ Fault        │ 고장이 발생해도 시스템이 계속 동작               │
│ Tolerance    │ 예: 이중화, TMR, 체크포인트                      │
│ (고장 허용)  │ "고장 나도 괜찮다"                               │
├──────────────┼──────────────────────────────────────────────────┤
│ Fault        │ 고장이 발생하면 안전하게 종료                    │
│ Secure       │ 예: 페일 세이프, 워치독                          │
│ (고장 보안)  │ "고장 나면 멈춘다"                               │
├──────────────┼──────────────────────────────────────────────────┤
│ Fault        │ 고장을 미리 감지하여 예방                        │
│ Prevention   │ 예: 품질 관리, 번인 테스트                        │
│ (고장 방지)  │ "고장 나지 않게 한다"                            │
├──────────────┼──────────────────────────────────────────────────┤
│ Fault        │ 고장 발생 시 정상 상태로 복구                    │
│ Recovery     │ 예: 재부팅, 롤백, 재시작                          │
│ (고장 복구)  │ "고장 나면 고친다"                               │
└──────────────┴──────────────────────────────────────────────────┘
```

#### 고장(Fault), 오류(Error), 실패(Failure)의 구분

```
┌─────────────────────────────────────────────────────────────────┐
│           Fault → Error → Failure 체인                          │
└─────────────────────────────────────────────────────────────────┘

    Fault (결함)        Error (오류)        Failure (실패)
    하드웨어/소프트웨어  내부 상태 오류      서비스 중단
    결함

    ┌─────────┐        ┌─────────┐        ┌─────────┐
    │  Fault  │ ───▶   │  Error  │ ───▶   │ Failure │
    │ (잠재적) │  활성화 │ (내부)  │  전파   │ (외부)  │
    └─────────┘        └─────────┘        └─────────┘

    예시:
    Fault:  메모리 셀의 물리적 손상
    Error:  해당 메모리 위치의 데이터 값이 틀림
    Failure: 잘못된 계산 결과로 서비스 오작동

    고장 허용의 목표:
    Fault → Error → Failure 체인을 차단!
    · Fault → Error: 예방 (Prevention)
    · Error → Failure: 허용 (Tolerance) 또는 복구 (Recovery)
```

#### 비유

> **고장 허용 시스템은 "비행기의 다중 엔진"과 같다.**
>
> - 일반적인 자동차는 엔진이 고장 나면 멈춘다 (Fault Secure)
> - 비행기는 4개의 엔진 중 1~2개가 고장 나도 날 수 있다 (Fault Tolerant)
> - 4발 비행기에서 1개 엔진 고장 → 3개로 계속 비행
> - 2개 엔진 고장 → 비상 착륙 가능
> - 3개 엔진 고장 → 치명적 (하지만 여전히 착륙 시도)
>
> 항공 우주, 원자력 발전소, 심장 박동기 등에서는 고장 허용이 필수이다.

#### 등장 배경 및 발전 과정

1. **1960-70년대: 항공우주 및 방산**
   - Apollo 우주선: 3중화 컴퓨터 (TMR)
   - 미군 전투기: Fly-by-wire 시스템

2. **1980년대: 메인프레임**
   - IBM, Tandem(NonStop) 등 고장 허용 서버
   - 전체 시스템 이중화

3. **1990-2000년대: 클러스터링**
   - Sun Cluster, Microsoft Cluster Server
   - Active-Passive 페일오버

4. **2010년대~현재: 분산 시스템/클라우드**
   - Google Spanner, etcd (Raft 합의)
   - Kubernetes Self-healing
   - Multi-Region Active-Active

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 고장 허용 기법 분류

```
┌─────────────────────────────────────────────────────────────────┐
│                 고장 허용 기법 분류                              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     Hardware Redundancy                         │
│                     (하드웨어 이중화)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Space Redundancy (공간 이중화)                              │
│     ┌──────┐ ┌──────┐ ┌──────┐                                 │
│     │ M1   │ │ M2   │ │ M3   │  ◀── 동일 모듈 3개 병렬         │
│     └──────┘ └──────┘ └──────┘                                 │
│         │       │       │                                       │
│         └───────┴───────┘                                       │
│                 │                                               │
│                 ▼                                               │
│         [Voter / Majority]                                      │
│                 │                                               │
│                 ▼                                               │
│            [결과]                                               │
│                                                                 │
│  · TMR (Triple Modular Redundancy)                              │
│  · N-Modular Redundancy (NMR)                                   │
│  · Hot Standby, Cold Standby                                    │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  2. Time Redundancy (시간 이중화)                               │
│                                                                 │
│     ┌──────┐     ┌──────┐     ┌──────┐                         │
│     │ 실행 │ ──▶ │ 재실행│ ──▶ │ 비교 │                        │
│     │ 1회  │     │ 2회  │     │      │                         │
│     └──────┘     └──────┘     └──────┘                         │
│                                                                 │
│  · 같은 연산을 여러 번 수행하여 비교                            │
│  · 일시적 고장(Transient Fault) 감지                            │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  3. Information Redundancy (정보 이중화)                        │
│                                                                 │
│     Data ──▶ [Encoder] ──▶ Encoded Data ──▶ [Decoder] ──▶ Data │
│                                                                 │
│  · ECC (Error Correcting Code)                                  │
│  · Parity, Checksum, CRC                                        │
│  · Hamming Code, Reed-Solomon                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     Software Redundancy                         │
│                     (소프트웨어 이중화)                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. N-Version Programming                                       │
│     · 독립적인 팀이 같은 스펙으로 N개 버전 개발                 │
│     · 결과를 비교하여 다수결로 결정                             │
│                                                                 │
│  2. Recovery Blocks                                             │
│     · Primary 모듈 실행 → 결과 검증                             │
│     · 실패 시 Alternate 모듈 실행                               │
│                                                                 │
│  3. Checkpoint & Restart                                        │
│     · 주기적 상태 저장 (Checkpoint)                              │
│     · 장애 시 마지막 체크포인트로 복구                          │
│                                                                 │
│  4. State Machine Replication                                   │
│     · 여러 노드에서 같은 상태 머신 실행                         │
│     · 합의 알고리즘(Paxos, Raft)으로 일관성 유지                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### TMR (Triple Modular Redundancy) 심층 분석

```
┌─────────────────────────────────────────────────────────────────┐
│           TMR (Triple Modular Redundancy) 구조                  │
└─────────────────────────────────────────────────────────────────┘

                    입력 (Input)
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
     ┌─────────┐  ┌─────────┐  ┌─────────┐
     │ Module1 │  │ Module2 │  │ Module3 │
     │  (M1)   │  │  (M2)   │  │  (M3)   │
     └────┬────┘  └────┬────┘  └────┬────┘
          │            │            │
          │    ┌───────┴───────┐    │
          │    │               │    │
          ▼    ▼               ▼    ▼
     ┌──────────────────────────────────┐
     │          Voter (투표기)          │
     │                                  │
     │   if M1 == M2: return M1        │
     │   elif M1 == M3: return M1      │
     │   elif M2 == M3: return M2      │
     │   else: Error (모두 다름)       │
     │                                  │
     └──────────────┬───────────────────┘
                    │
                    ▼
                출력 (Output)

신뢰도 분석:
· 단일 모듈 신뢰도: R
· TMR 시스템 신뢰도: R_TMR = 3R² - 2R³

예시:
· R = 0.9 (단일 모듈 90% 신뢰도)
· R_TMR = 3×0.81 - 2×0.729 = 2.43 - 1.458 = 0.972 (97.2%)
· 신뢰도 7.2% 향상

※ 단, 모듈 신뢰도가 높을수록 효과 증대
   R = 0.99 → R_TMR = 0.999702 (99.97%)
```

#### 분산 시스템에서의 고장 허용

```
┌─────────────────────────────────────────────────────────────────┐
│           분산 시스템 고장 허용 아키텍처                         │
└─────────────────────────────────────────────────────────────────┘

Replication + Consensus = Fault Tolerance

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│           ┌──────────────────────────────────────┐              │
│           │           Client                     │              │
│           └──────────────┬───────────────────────┘              │
│                          │                                      │
│                          ▼                                      │
│           ┌──────────────────────────────────────┐              │
│           │        Load Balancer                 │              │
│           └──────────────┬───────────────────────┘              │
│                          │                                      │
│       ┌──────────────────┼──────────────────┐                   │
│       ▼                  ▼                  ▼                   │
│ ┌─────────────┐   ┌─────────────┐   ┌─────────────┐            │
│ │  Node 1     │   │  Node 2     │   │  Node 3     │            │
│ │  (Leader)   │◀─▶│ (Follower)  │◀─▶│ (Follower)  │            │
│ │             │   │             │   │             │            │
│ │  ┌───────┐  │   │  ┌───────┐  │   │  ┌───────┐  │            │
│ │  │ State │  │   │  │ State │  │   │  │ State │  │            │
│ │  │Machine│  │   │  │Machine│  │   │  │Machine│  │            │
│ │  └───────┘  │   │  └───────┘  │   │  └───────┘  │            │
│ │             │   │             │   │             │            │
│ │  ┌───────┐  │   │  ┌───────┐  │   │  ┌───────┐  │            │
│ │  │ Log   │  │   │  │ Log   │  │   │  │ Log   │  │            │
│ │  │(Raft) │  │   │  │(Raft) │  │   │  │(Raft) │  │            │
│ │  └───────┘  │   │  └───────┘  │   │  └───────┘  │            │
│ └─────────────┘   └─────────────┘   └─────────────┘            │
│       │                  │                  │                   │
│       └──────────────────┴──────────────────┘                   │
│                    Raft Consensus                               │
│                    (과반수 합의)                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Raft/Paxos 기반 고장 허용:
· 노드 1개 고장 → 나머지 2개로 계속 동작 (과반수 유지)
· 노드 2개 고장 → 서비스 중단 (과반수 상실)
· N개 노드 → 최대 (N-1)/2개 노드 고장까지 허용

┌─────────────────────────────────────────────────────────────────┐
│ 노드 수 │  과반수  │  허용 고장 수 │  가용성 등급               │
├─────────────────────────────────────────────────────────────────┤
│   3     │    2     │       1       │  1개 노드 고장까지 OK      │
│   5     │    3     │       2       │  2개 노드 고장까지 OK      │
│   7     │    4     │       3       │  3개 노드 고장까지 OK      │
│   9     │    5     │       4       │  4개 노드 고장까지 OK      │
└─────────────────────────────────────────────────────────────────┘
```

#### 핵심 코드: TMR 구현 예시

```c
/*
 * TMR (Triple Modular Redundancy) Implementation
 * 하드웨어/소프트웨어 고장 허용을 위한 3중 모듈 중단
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef enum {
    VOTE_SUCCESS,
    VOTE_DISAGREE,
    VOTE_ALL_DIFFERENT
} VoteResult;

typedef struct {
    int value;
    int module_id;
} ModuleOutput;

typedef struct {
    int final_value;
    VoteResult result;
    int agreeing_modules;  // 동의한 모듈 수
} VoterOutput;

/*
 * Module 함수 타입 정의
 * 각 모듈은 동일한 입력에 대해 연산을 수행
 */
typedef int (*ModuleFunc)(int input);

/*
 * Module 1: 정상 동작 (의도적 오류 없음)
 */
int module1_compute(int input) {
    return input * 2 + 1;
}

/*
 * Module 2: 정상 동작
 */
int module2_compute(int input) {
    return input * 2 + 1;
}

/*
 * Module 3: 가끔 오류 발생 (시뮬레이션)
 */
int module3_compute(int input) {
    // 20% 확률로 오류 발생
    if (rand() % 100 < 20) {
        return input * 2 + 2;  // 잘못된 결과
    }
    return input * 2 + 1;
}

/*
 * Voter: 다수결 투표
 * 3개의 모듈 출력을 비교하여 최종 결과 결정
 */
VoterOutput tmr_vote(ModuleOutput m1, ModuleOutput m2, ModuleOutput m3) {
    VoterOutput output;

    // Case 1: 모두 동의
    if (m1.value == m2.value && m2.value == m3.value) {
        output.final_value = m1.value;
        output.result = VOTE_SUCCESS;
        output.agreeing_modules = 3;
        return output;
    }

    // Case 2: M1 == M2 (M3가 틀림)
    if (m1.value == m2.value) {
        output.final_value = m1.value;
        output.result = VOTE_SUCCESS;
        output.agreeing_modules = 2;
        printf("[TMR] Module 3 disagrees (M1=M2=%d, M3=%d)\n",
               m1.value, m3.value);
        return output;
    }

    // Case 3: M1 == M3 (M2가 틀림)
    if (m1.value == m3.value) {
        output.final_value = m1.value;
        output.result = VOTE_SUCCESS;
        output.agreeing_modules = 2;
        printf("[TMR] Module 2 disagrees (M1=M3=%d, M2=%d)\n",
               m1.value, m2.value);
        return output;
    }

    // Case 4: M2 == M3 (M1가 틀림)
    if (m2.value == m3.value) {
        output.final_value = m2.value;
        output.result = VOTE_SUCCESS;
        output.agreeing_modules = 2;
        printf("[TMR] Module 1 disagrees (M2=M3=%d, M1=%d)\n",
               m2.value, m1.value);
        return output;
    }

    // Case 5: 모두 다름 - 치명적 오류
    output.final_value = -1;  // 에러 값
    output.result = VOTE_ALL_DIFFERENT;
    output.agreeing_modules = 0;
    printf("[TMR] CRITICAL: All modules disagree!\n");
    return output;
}

/*
 * TMR 시스템 실행
 */
int tmr_execute(int input, ModuleFunc m1, ModuleFunc m2, ModuleFunc m3) {
    // 각 모듈 실행
    ModuleOutput out1 = {m1(input), 1};
    ModuleOutput out2 = {m2(input), 2};
    ModuleOutput out3 = {m3(input), 3};

    printf("[TMR] Input: %d\n", input);
    printf("[TMR] Module outputs: M1=%d, M2=%d, M3=%d\n",
           out1.value, out2.value, out3.value);

    // Voter로 투표
    VoterOutput vote = tmr_vote(out1, out2, out3);

    if (vote.result == VOTE_SUCCESS) {
        printf("[TMR] Final output: %d (agreed by %d modules)\n\n",
               vote.final_value, vote.agreeing_modules);
        return vote.final_value;
    } else {
        printf("[TMR] SYSTEM FAILURE - cannot determine correct value\n\n");
        return -1;
    }
}

/*
 * TMR 신뢰도 분석
 * R_TMR = 3R² - 2R³ (단일 모듈 신뢰도 R)
 */
double tmr_reliability(double single_reliability) {
    double R = single_reliability;
    return 3 * R * R - 2 * R * R * R;
}

int main() {
    srand(time(NULL));

    printf("=============================================\n");
    printf("  TMR (Triple Modular Redundancy) Demo\n");
    printf("=============================================\n\n");

    // 여러 입력에 대해 TMR 테스트
    int test_inputs[] = {5, 10, 15, 20, 25};
    int num_tests = sizeof(test_inputs) / sizeof(test_inputs[0]);

    int success = 0, failure = 0;

    for (int i = 0; i < num_tests; i++) {
        int result = tmr_execute(test_inputs[i],
                                 module1_compute,
                                 module2_compute,
                                 module3_compute);

        if (result != -1) {
            success++;
        } else {
            failure++;
        }
    }

    printf("=============================================\n");
    printf("  Results: %d successes, %d failures\n", success, failure);
    printf("=============================================\n\n");

    // 신뢰도 분석
    printf("Reliability Analysis:\n");
    printf("----------------------------------------\n");
    printf("Single Module R | TMR System R | Improvement\n");
    printf("----------------------------------------\n");

    double R_values[] = {0.8, 0.9, 0.95, 0.99, 0.999};
    for (int i = 0; i < 5; i++) {
        double R = R_values[i];
        double R_tmr = tmr_reliability(R);
        double improvement = (R_tmr - R) * 100;
        printf("    %.3f       |    %.5f   |   +%.2f%%\n",
               R, R_tmr, improvement);
    }

    return 0;
}
```

---

### III. 융합 비교 및 다각도 분석

#### 고장 허용 기법 비교

| 기법 | 설명 | 장점 | 단점 | 적용 분야 |
|------|------|------|------|-----------|
| **TMR** | 3중 모듈 + 투표 | 1개 고장 허용 | 3배 비용 | 항공, 우주 |
| **NMR** | N개 모듈 + 투표 | (N-1)/2개 고장 허용 | N배 비용 | 원자력, 국방 |
| **Hot Standby** | 활성-대기 | 즉시 페일오버 | 자원 낭비 | DB, 서버 |
| **Cold Standby** | 수동 대기 | 저렴 | 복구 느림 | 백업 시스템 |
| **Checkpoint** | 상태 저장 | 복구 가능 | 오버헤드 | HPC, 배치 |
| **Replication** | 데이터 복제 | 고가용성 | 일관성 문제 | DB, 스토리지 |

#### 고장 모델별 대응 전략

```
┌─────────────────────────────────────────────────────────────────┐
│              고장 유형별 고장 허용 전략                          │
└─────────────────────────────────────────────────────────────────┘

┌────────────────┬────────────────────────────────────────────────┐
│    고장 유형   │              대응 전략                         │
├────────────────┼────────────────────────────────────────────────┤
│ Transient      │ · 재시도 (Retry)                              │
│ (일시적 고장)  │ · Time Redundancy                            │
│                │ · ECC (메모리)                                │
├────────────────┼────────────────────────────────────────────────┤
│ Intermittent   │ · 로깅 및 패턴 분석                           │
│ (간헐적 고장)  │ · Threshold 기반 격리                        │
│                │ · Predictive Maintenance                      │
├────────────────┼────────────────────────────────────────────────┤
│ Permanent      │ · 모듈 교체                                   │
│ (영구 고장)    │ · Hot Standby 전환                           │
│                │ · TMR/NMR 투표                                │
├────────────────┼────────────────────────────────────────────────┤
│ Byzantine      │ · Byzantine Fault Tolerance (BFT)            │
│ (악의적 고장)  │ · 3f+1개 노드 필요 (f개 고장 허용)           │
│                │ · Practical BFT, HoneyBadgerBFT               │
└────────────────┴────────────────────────────────────────────────┘
```

#### 과목 융합 분석

| 융합 과목 | FT 적용 | 기술 예시 |
|-----------|---------|-----------|
| **OS** | 프로세스 격리, 재시작 | systemd restart policy |
| **네트워크** | 다중 경로, 페일오버 | ECMP, VRRP |
| **DB** | 복제, 자동 페일오버 | MySQL InnoDB Cluster, PostgreSQL Patroni |
| **보안** | Byzantine Fault Tolerance | 블록체인 컨센서스 |
| **클라우드** | Auto Scaling, Multi-AZ | AWS ASG, Azure Availability Set |

---

### IV. 실무 적용 및 기술사적 판단

#### 실무 시나리오

**시나리오 1: 금융 결제 시스템 FT 설계**
```
요구사항: 99.999% 가용성, 어떤 단일 고장에도 서비스 지속

설계:
1. 애플리케이션 계층
   - 3개 AZ에 각 2개 인스턴스 (총 6개)
   - Kubernetes Deployment (replicas: 6)
   - Health check + 자동 재시작

2. 데이터베이스 계층
   - MySQL InnoDB Cluster (3노드, Group Replication)
   - Raft 기반 합의
   - 자동 페일오버

3. 네트워크 계층
   - 이중 ISP
   - 이중 로드밸런서
   - DNS 페일오버

4. 스토리지 계층
   - RAID 10 (미러링 + 스트라이핑)
   - 다중 경로 I/O

비용: 일반 시스템의 3~4배
효과: 연간 다운타임 < 5분
```

**시나리오 2: Kubernetes 고장 허용**
```
기본 FT 기능:
· Pod 장애 → 자동 재스케줄링
· Node 장애 → 다른 노드로 Pod 이동
· 컨테이너 장애 → 재시작

고급 FT 설정:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: critical-app
spec:
  replicas: 3                    # 3개 복제본
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1         # 동시에 1개만 불가용
      maxSurge: 1
  template:
    spec:
      containers:
      - name: app
        image: myapp:latest
        livenessProbe:          # 생존 프로브
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:         # 준비 프로브
          httpGet:
            path: /ready
            port: 8080
          periodSeconds: 5
      affinity:
        podAntiAffinity:        # 다른 노드에 분산
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: critical-app
            topologyKey: kubernetes.io/hostname
```

#### 도입 시 고려사항

```
□ 고장 모드 분석 (FMEA)
  □ 가능한 모든 고장 시나리오 식별
  □ 각 고장의 영향도 평가
  □ 우선순위 결정

□ 이중화 수준 결정
  □ N+1 vs 2N vs Active-Active
  □ 비용 vs 가용성 트레이드오프

□ 페일오버 테스트
  □ 정기적 Chaos Engineering
  □ GameDay 수행

□ 모니터링 및 알림
  □ 고장 감지 시스템
  □ 자동 복구 검증
```

#### 안티패턴

```
❌ "이중화만 하면 FT다"
   → 페일오버가 제대로 동작하는지 검증 필수

❌ "하드웨어만 FT 적용"
   → 소프트웨어 버그, 설정 오류도 고장의 원인

❌ "공통 모드 고장 무시"
   → 전원, 네트워크, 설정 등 동시에 영향받는 요인 분석

❌ "테스트 없이 운영"
   → 정기적 페일오버 테스트 필수
```

---

### V. 기대효과 및 결론

#### 정량적 기대효과

| 지표 | FT 미적용 | FT 적용 | 개선 |
|------|-----------|---------|------|
| 가용성 | 99% | 99.999% | +0.999% |
| 연간 다운타임 | 87.6시간 | 5.26분 | 99.9% 감소 |
| SPOF | 다수 존재 | 제거 | 리스크 제거 |
| 복구 시간 | 수동 (시간) | 자동 (분) | 95% 단축 |

#### 미래 전망

1. **AI 기반 고장 예측**
   - 머신러닝으로 고장 시점 예측
   - 선제적 조치

2. **Self-Healing Infrastructure**
   - 완전 자동화된 복구
   - 인간 개입 최소화

#### 참고 표준

- **IEC 61508**: Functional Safety
- **ISO 26262**: Automotive Safety
- **DO-178C**: Software Considerations in Airborne Systems

---

### 관련 개념 맵 (Knowledge Graph)

- [449. RAS](./1_ras.md) - 신뢰성, 가용성, 유지보수성
- [452. 가용성](./4_availability.md) - FT의 목표 지표
- [454. SPOF](./6_spof.md) - FT로 제거해야 할 대상
- [455. TMR](./7_tmr.md) - 대표적 FT 기법
- [456. 이중화](./8_redundancy.md) - FT의 핵심 수단

---

### 어린이를 위한 3줄 비유 설명

**고장 허용 시스템은 "다리가 3개인 의자"와 같아요!**

1. 보통 의자는 다리가 4개인데, 하나가 부러지면 의자가 흔들리거나 넘어져요. 하지만 6개 다리 의자는 1~2개가 부러져도 여전히 안전하게 앉을 수 있어요. 이게 바로 고장 허용이에요!

2. 비행기도 4개의 엔진 중 1~2개가 고장 나도 날 수 있어요. 그래서 비행기는 안전하죠. 모든 엔진이 동시에 고장 나지 않는 한, 승객들은 모르고 여행을 계속할 수 있어요.

3. 컴퓨터도 마찬찬가지예요. 중요한 컴퓨터는 2~3대가 같은 일을 하고, 하나가 고장 나면 다른 컴퓨터가 바로 대신해요. 그래서 은행 앱이나 게임 서버가 멈추지 않고 계속 작동하는 거예요!
