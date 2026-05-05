+++
weight = 157
title = "157. OOM (Out Of Memory) Killer 프로세스 종료 정책"
date = "2026-03-22"
[extra]
categories = "studynote-operating-system"
+++

## 0. 핵심 인사이트

> **핵심**: OOM (Out Of Memory) Killer 프로세스 종료 정책은(는) 운영체제가 자원을 추상화하고 통제하는 과정에서 성능, 보호, 응답성을 동시에 조율하기 위해 필요한 핵심 개념이다.
> **비유**: OOM Killer는 "비상시 배를 가볍게 하기 위해 화물을 바다에 던지는 선장"이다. 배(시스템)가 침몰하는 것보다 일부 화물(프로세스)을 희생하는 것이 낫다.

---

📝 모범 답안

## 1. 개요 및 필요성

### 1. 정의

OOM Killer (Out-Of-Memory Killer)는 Linux 커널이 시스템의 물리 메모리 및 스왑 영역이 완전히 고갈되었을 때, 메모리를 확보하기 위해 특정 프로세스를 강제 종료(Kill)하는 커널 메커니즘이다. OOM 상태에서는 새로운 메모리 할당이 불가능하므로, 커널이 직접 개입하여 시스템 전체의 다운(Crash)을 방지한다.

### 2. OOM 발생 조건

```
OOM 발생 과정

[정상 상태]
  물리 메모리: 8GB / 16GB
  Swap: 0GB / 4GB
      |
      v  (메모리 사용 증가)
[메모리 압박 상태]
  물리 메모리: 15.5GB / 16GB
  Swap: 3.5GB / 4GB
  --> kswapd 활성, 페이지 회수 시작
      |
      v  (회수 불충분)
[OOM 경고 상태]
  물리 메모리: 16GB / 16GB (FULL)
  Swap: 4GB / 4GB (FULL)
  --> Direct Reclaim, Memory Compaction 시도
      |
      v  (모든 회수 실패)
[OOM 발생!]
  커널이 oom_badness()로 희생 프로세스 선정
  --> OOM Killer가 프로세스에 SIGKILL 전송
  --> 메모리 확보 후 시스템 계속 운영
```

### 3. OOM Killer의 목적

| 목적 | 설명 |
|------|------|
| 시스템 생존 보장 | 전체 시스템 패닉(Panic) 방지 |
| 서비스 연속성 | 필수 서비스 유지, 덜 중요한 프로세스 희생 |
| 메모리 확보 | 종료된 프로세스의 메모리를 즉시 회수 |
| 자동 복구 | 관리자 개입 없이 자동으로 메모리 복원 |

---

## 2. 구성요소

### 1. oom_badness() 알고리즘

커널은 `oom_badness()` 함수를 통해 각 프로세스의 OOM 점수(oom_score)를 계산한다. 점수가 높을수록 OOM Killer에 의해 먼저 종료될 확률이 높다.

```
oom_score 산정 모델

oom_score = 프로세스 메모리 사용량 + 가중치 보정

+-----------------------------------------------+
|  oom_score 구성 요소                           |
|                                               |
|  1. Resident Set Size (RSS)                   |
|     --> 물리 메모리 상주 크기                   |
|                                               |
|  2. 페이지 테이블 크기 (Page Table Size)        |
|     --> 페이지 테이블 엔트리 수                  |
|                                               |
|  3. Swap 사용량                                |
|     --> 스왑 영역 사용 크기                     |
|                                               |
|  4. oom_score_adj 보정값                       |
|     --> 관리자가 수동 조정 (-1000 ~ +1000)     |
|                                               |
|  최종 점수 = (RSS + Swap + PageTable) / 총메모리 |
|             + oom_score_adj 보정                |
+-----------------------------------------------+
```

### 2. oom_score 범위

| 점수 범위 | 의미 |
|-----------|------|
| **0** | 메모리를 거의 사용하지 않음 (거의 종료되지 않음) |
| **1~999** | 보통 수준의 메모리 사용 |
| **1000** | 매우 높은 점수 (OOM 발생 시 높은 우선순위로 종료) |

### 3. 점수 확인 방법

```bash
cat /proc/[pid]/oom_score

cat /proc/[pid]/oom_score_adj

ps -eo pid,comm,rss,oom_score | sort -k4 -rn | head -10
```

> **비유**: oom_score는 "위험도 순위표"다. 선장(OOM Killer)은 가장 높은 점수를 받은 화물을 먼저 바다에 던진다. 점수를 낮추면 안전하다.

---

## 3. 구조 및 원리

**핵심 조건**: 운영체제의 해당 메커니즘은 현재 상태 정보, 자원 제약, 정책 기준이 함께 정합성을 가질 때 안정적으로 동작한다.

동작 순서:
1. **요청 또는 이벤트 발생**: 사용자 요청, 인터럽트, 시스템 호출 등으로 커널이 해당 기능을 처리할 필요가 생긴다.
2. **현재 상태 확인**: 커널은 큐, 제어 블록, 메타데이터, 자원 가용량을 확인해 실행 가능 여부와 우선순위를 판단한다.
3. **정책 적용 및 자원 배정**: 해당 주제의 핵심 정책에 따라 상태 전이, 자원 할당, 보호 검사를 수행한다.
4. **결과 반영 및 후속 처리**: 처리 결과를 시스템 상태에 기록하고 다음 인터럽트·스케줄링·복구 단계로 연결한다.

### 1. oom_score_adj

`oom_score_adj`는 관리자가 프로세스의 OOM 우선순위를 수동으로 조정할 수 있는 인터페이스이다. `/proc/[pid]/oom_score_adj` 파일에 값을 기록하여 변경한다.

```
oom_score_adj 설정에 따른 동작

[-1000]  ================================================
         OOM 면제: 이 프로세스는 OOM Killer 대상에서 제외
         단, 시스템 자체가 불가피한 상황이면 예외 존재

[-999 ~ -1]  ==========================================
              oom_score에서 해당 값만큼 차감
              종료 확률 낮아짐

[0]  ====================================================
     기본값: oom_badness()로 계산된 점수 그대로 사용

[+1 ~ +999]  ==========================================
              oom_score에서 해당 값만큼 가산
              종료 확률 높아짐

[+1000]  ================================================
          무조건 최우선 종료 대상
          OOM 발생 시 가장 먼저 SIGKILL
```

### 2. 설정 예시

```bash
echo -1000 > /proc/1234/oom_score_adj

echo 500 > /proc/1234/oom_score_adj

echo 0 > /proc/1234/oom_score_adj

cat /proc/1234/oom_score_adj
```

### 3. systemd에서의 OOMScoreAdjust

```ini
[Service]
OOMScoreAdjust=-500    # OOM 종료 우선순위 낮춤 (보호)
ExecStart=/usr/bin/myapp
```

| OOMScoreAdjust | systemd 기본값 |
|----------------|---------------|
| systemd 자체 | -1000 (항상 보호) |
| 사용자 서비스 | 0 |
| 커스텀 설정 | -1000 ~ 1000 |

---

## 4. 비교 및 연결

### 1. oom_score_adj

`oom_score_adj`는 관리자가 프로세스의 OOM 우선순위를 수동으로 조정할 수 있는 인터페이스이다. `/proc/[pid]/oom_score_adj` 파일에 값을 기록하여 변경한다.

```
oom_score_adj 설정에 따른 동작

[-1000]  ================================================
         OOM 면제: 이 프로세스는 OOM Killer 대상에서 제외
         단, 시스템 자체가 불가피한 상황이면 예외 존재

[-999 ~ -1]  ==========================================
              oom_score에서 해당 값만큼 차감
              종료 확률 낮아짐

[0]  ====================================================
     기본값: oom_badness()로 계산된 점수 그대로 사용

[+1 ~ +999]  ==========================================
              oom_score에서 해당 값만큼 가산
              종료 확률 높아짐

[+1000]  ================================================
          무조건 최우선 종료 대상
          OOM 발생 시 가장 먼저 SIGKILL
```

### 2. 설정 예시

```bash
echo -1000 > /proc/1234/oom_score_adj

echo 500 > /proc/1234/oom_score_adj

echo 0 > /proc/1234/oom_score_adj

cat /proc/1234/oom_score_adj
```

### 3. systemd에서의 OOMScoreAdjust

```ini
[Service]
OOMScoreAdjust=-500    # OOM 종료 우선순위 낮춤 (보호)
ExecStart=/usr/bin/myapp
```

| OOMScoreAdjust | systemd 기본값 |
|----------------|---------------|
| systemd 자체 | -1000 (항상 보호) |
| 사용자 서비스 | 0 |
| 커스텀 설정 | -1000 ~ 1000 |

---

## 5. 실무 적용 및 판단

### 1. cgroup v1: memory.oom_control

cgroup (Control Group)을 사용하면 프로세스 그룹 단위로 메모리 사용량을 제한하고 OOM 동작을 제어할 수 있다.

```
cgroup 메모리 제어 구조

[System Level]
  oom_kill_disable=0 (default)
  -->
  [cgroup: /sys/fs/cgroup/memory/database]
    memory.limit_in_bytes = 4G
    memory.oom_control:
      oom_kill_disable = 0  --> OOM Killer 활성
      under_oom = 0         --> 현재 OOM 아님
    |
    +-- [PostgreSQL] (PID 1001)
    +-- [Redis]      (PID 1002)

  [cgroup: /sys/fs/cgroup/memory/app]
    memory.limit_in_bytes = 2G
    memory.oom_control:
      oom_kill_disable = 1  --> OOM Killer 비활성
    --> 메모리 초과 시 해당 cgroup 내 프로세스 멈춤 (Sleep)
    --> 관리자가 수동 해제해야 함
```

### 2. cgroup v2: memory.events

```bash
cat /sys/fs/cgroup/memory/mygroup/memory.events

echo "2G" > /sys/fs/cgroup/memory/mygroup/memory.max

echo 1 > /sys/fs/cgroup/memory/mygroup/memory.swap.max
```

### 3. OOM Kill Disable의 주의사항

```
oom_kill_disable=1 설정 시 동작

+--------------------------------------------------+
| memory.limit_in_bytes = 2G                       |
| oom_kill_disable = 1                             |
|                                                  |
| [메모리 초과 시]                                  |
|   --> OOM Killer가 프로세스를 죽이지 않음          |
|   --> 해당 cgroup 내 프로세스이 Sleep 상태로 대기   |
|   --> 새 메모리 할당은 즉시 실패 (ENOMEM)          |
|   --> 시스템 전체 OOM으로 확산 가능               |
|                                                  |
| [주의!]                                          |
|   부적절한 사용은 시스템 전체 불안정 유발          |
|   반드시 모니터링과 알림 필요                     |
+--------------------------------------------------+
```

> **비유**: cgroup은 "건물별 전기 사용량 제한기"다. 한 건물이 한계를 넘으면 그 건물만 차단(OOM Kill)하는데, oom_kill_disable=1은 "한계를 넘어도 차단하지 않겠다"는 의미로, 결국 전체 건물(시스템)이 정전될 수 있다.

---

## 6. 기대효과 및 결론

### 1. OOM Killer 로그

```bash
dmesg | grep -i "oom\|out of memory\|killed process"

```

### 2. OOM 방지 전략

```
OOM 방지 다중 방어 레이어

[Layer 1: 예방]
  ├── 메모리 사용량 모니터링 (Prometheus, Grafana)
  ├── Swap 영역 적절한 크기 설정
  └── 과도한 메모리 할당 제한 (ulimit -v)

[Layer 2: 제어]
  ├── cgroup 메모리 제한 설정
  ├── oom_score_adj로 중요 프로세스 보호
  └── 메모리 과다 할당 해제 (vm.overcommit_memory)

[Layer 3: 대응]
  ├── OOM 이벤트 알림 설정
  ├── 자동 재시작 메커니즘 (systemd restart)
  └── 장애 후 포스트모템 분석
```

---

## 7. 발전 흐름도

```text
기초 자원 관리 문제
    ↓
OOM (Out Of Memory) Killer 프로세스 종료 정책
    ↓
성능·격리·공정성 최적화
    ↓
가상화·관측·자동화 통합
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| OOM (Out Of Memory) Killer 프로세스 종료 정책 | 운영체제 자원 관리와 보호 정책이 실제로 적용되는 핵심 주제 |
| 커널 (Kernel) | 정책 집행, 상태 전이, 시스템 호출 처리의 중심 |
| 프로세스/스레드 | CPU, 메모리, 동기화 자원과 직접 연결되는 실행 단위 |
| 메모리/I/O | 성능 병목과 보호 요구사항이 함께 드러나는 연계 영역 |
| 가상화/보안 | 격리, 제어, 관측 확장 관점에서 해당 주제가 연결되는 상위 개념 |
