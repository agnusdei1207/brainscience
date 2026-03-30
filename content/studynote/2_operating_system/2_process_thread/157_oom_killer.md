+++
weight = 157
title = "OOM Killer 프로세스 종료 정책"
date = "2026-03-22"
[extra]
categories = "studynote-operating-system"
+++

# OOM Killer 프로세스 종료 정책 (OOM Killer Process Termination Policy)

## Ⅰ. OOM Killer의 개념

### 1. 정의

OOM Killer (Out-Of-Memory Killer)는 Linux 커널이 시스템의 물리 메모리 및 스왑 영역이 완전히 고갈되었을 때, 메모리를 확보하기 위해 특정 프로세스를 강제 종료(Kill)하는 커널 메커니즘이다. OOM 상태에서는 새로운 메모리 할당이 불가능하므로, 커널이 직접 개입하여 시스템 전체의 다운(Crash)을 방지한다.

> **비유**: OOM Killer는 "비상시 배를 가볍게 하기 위해 화물을 바다에 던지는 선장"이다. 배(시스템)가 침몰하는 것보다 일부 화물(프로세스)을 희생하는 것이 낫다.

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

## Ⅱ. OOM 점수 산정 (oom_score)

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
# 특정 프로세스의 OOM 점수 확인
cat /proc/[pid]/oom_score
# 예: 543

# OOM 점수 조정값 확인
cat /proc/[pid]/oom_score_adj
# 예: 0

# 전체 프로세스의 OOM 점수 확인 (높은 순서)
ps -eo pid,comm,rss,oom_score | sort -k4 -rn | head -10
```

> **비유**: oom_score는 "위험도 순위표"다. 선장(OOM Killer)은 가장 높은 점수를 받은 화물을 먼저 바다에 던진다. 점수를 낮추면 안전하다.

---

## Ⅲ. oom_score_adj를 통한 제어

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
# 프로세스를 OOM Killer로부터 보호
echo -1000 > /proc/1234/oom_score_adj

# 프로세스를 OOM 시 우선 종료 대상으로 지정
echo 500 > /proc/1234/oom_score_adj

# 기본값으로 복원
echo 0 > /proc/1234/oom_score_adj

# 설정 확인
cat /proc/1234/oom_score_adj
```

### 3. systemd에서의 OOMScoreAdjust

```ini
# /etc/systemd/system/myapp.service
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

## Ⅳ. cgroup 기반 OOM 제어

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
# cgroup v2에서 OOM 이벤트 확인
cat /sys/fs/cgroup/memory/mygroup/memory.events
# low 0
# high 0
# max 3
# oom 1
# oom_kill 1

# 메모리 한계 설정
echo "2G" > /sys/fs/cgroup/memory/mygroup/memory.max

# OOM Kill 비활성화 (v2에서는 memory.oom.group 등 활용)
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

## Ⅴ. OOM Killer 로그 분석 및 대응

### 1. OOM Killer 로그

```bash
# dmesg 또는 /var/log/syslog에서 OOM 이벤트 확인
dmesg | grep -i "oom\|out of memory\|killed process"

# 로그 예시:
# Out of memory: Killed process 12345 (java) total-vm:8G, anon-rss:6G
# oom-kill:constraint=CONSTRAINT_NONE,nodemask=(null),
#   cpuset=systemd,mems_allowed=0,oom_memcg=/database,
#   task=java,pid=12345,uid=1000,oom_score_adj=0
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

## 요약

### 지식 그래프

```
OOM Killer 프로세스 종료 정책
├── 개념
│   ├── Out-Of-Memory 상태
│   ├── 커널 개입으로 시스템 생존 보장
│   └── SIGKILL로 강제 프로세스 종료
├── 점수 산정
│   ├── oom_badness() 함수
│   ├── RSS (Resident Set Size)
│   ├── 페이지 테이블 크기
│   └── Swap 사용량
├── 점수 제어
│   ├── oom_score (0~1000, 읽기 전용 산정값)
│   ├── oom_score_adj (-1000~+1000, 수동 조정)
│   └── /proc/[pid]/oom_score_adj
├── cgroup 제어
│   ├── cgroup v1: memory.oom_control
│   ├── cgroup v2: memory.events
│   ├── memory.limit_in_bytes
│   └── oom_kill_disable
├── 관리자 도구
│   ├── dmesg (OOM 로그 확인)
│   ├── ps (프로세스 점수 확인)
│   └── systemd OOMScoreAdjust
└── 방지 전략
    ├── 모니터링
    ├── 메모리 제한 설정
    └── 자동 복구
```

### 세 줄 설명 (어린이용)

1. OOM Killer는 컴퓨터의 메모리가 꽉 찼을 때, 가장 덜 중요한 프로그램을 골라서 끄는 "긴급 구조대"예요.
2. 각 프로그램은 점수(oom_score)를 받는데, 점수가 높을수록 먼저 끌려가고, 점수를 낮추면 안전해져요.
3. 점수를 -1000으로 하면 "절대 끄지 마!"라고 표시할 수 있고, cgroup으로도 그룹 단위로 지킬 수 있어요.

### 약어 정리

| 약어 | Full Name |
|------|-----------|
| OOM | Out-Of-Memory |
| RSS | Resident Set Size |
| SIGKILL | Signal Kill (무조건 종료 시그널) |
| ENOMEM | Error No Memory |
| cgroup | Control Group |
