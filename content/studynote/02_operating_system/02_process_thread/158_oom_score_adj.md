+++
weight = 158
title = "158. oom_score_adj - OOM 킬러 우선순위 조정"
date = "2026-03-22"
[extra]
categories = "studynote-operating-system"
+++

## 0. 핵심 인사이트

> **핵심**: oom_score_adj은(는) 운영체제가 자원을 추상화하고 통제하는 과정에서 성능, 보호, 응답성을 동시에 조율하기 위해 필요한 핵심 개념이다.
> **비유**: oom_score_adj는 "위험도 점수에 더하거나 빼는 보너스/패널티 점수"다. -1000점을 받으면 "무적 쉴드"가 씌워지고, +1000점을 받으면 "가장 먼저 퇴장" 대상이 된다.

---

📝 모범 답안

## 1. 개요 및 필요성

### 1. 정의

**oom_score_adj**는 Linux 커널이 OOM (Out-Of-Memory) 상태에서 프로세스를 강제 종료할 때의 우선순위를 관리자가 수동으로 조정할 수 있는 파라미터이다. `/proc/[pid]/oom_score_adj` 파일을 통해 -1000부터 +1000 사이의 정수값을 설정할 수 있으며, 이 값은 커널이 계산한 `oom_score`에 더해져 최종 OOM 점수를 결정한다.

### 2. oom_score와 oom_score_adj의 관계

```
최종 OOM 점수 계산 구조

+------------------------------------------------------+
|  oom_score (커널이 자동 계산, 읽기 전용)               |
|  = (RSS + Swap + PageTable) / 총 메모리 * 1000       |
|                                                      |
|  oom_score_adj (관리자 수동 설정, -1000 ~ +1000)      |
|  = 수동 보정값                                        |
|                                                      |
|  최종 점수 = oom_score + oom_score_adj                |
|                                                      |
|  주의: 최종 점수가 음수라도 0 이하로 내려가지 않음      |
|        (단, oom_score_adj = -1000은 특별 예외)         |
+------------------------------------------------------+

예시:
  프로세스 A: oom_score=500, oom_score_adj=0   --> 최종: 500
  프로세스 B: oml_score=500, oom_score_adj=-500 --> 최종: 0 (보호됨)
  프로세스 C: oom_score=300, oom_score_adj=+500 --> 최종: 800 (위험)
```

---

## 2. 구성요소

### 1. 상세 범위별 동작

| oom_score_adj | 의미 | OOM Killer 동작 |
|---------------|------|-----------------|
| **-1000** | OOM 면제 (Immune) | OOM 발생 시 절대 종료되지 않음 |
| **-999 ~ -1** | 낮은 우선순위 | oom_score에서 해당 값 차감, 종료 확률 감소 |
| **0** | 기본값 (Default) | 커널 계산 점수 그대로 사용 |
| **+1 ~ +999** | 높은 우선순위 | oom_score에 해당 값 가산, 종료 확률 증가 |
| **+1000** | 최우선 종료 (Always Kill First) | OOM 발생 시 가장 먼저 종료됨 |

### 2. -1000 (OOM 면제)의 특수 동작

```
oom_score_adj = -1000 설정 시

[일반 프로세스]
  oom_score_adj = -1000
  oom_score = 0으로 고정 (실제 메모리 사용량 무관)
  --> OOM Killer 대상에서 완전 제외

[예외 상황: cpuset 또는 mempolicy 제한]
  cgroup/mempolicy로 메모리가 제한된 노드에서
  해당 노드 내에서만 OOM 발생 시
  --> -1000 프로세스도 종료 가능 (Linux 2.6.36 이후)
  --> 단, 전역 OOM에서는 여전히 보호됨

[커널 스레드]
  커널 스레드는 기본적으로 oom_score_adj = -1000
  --> 커널 스레드는 항상 OOM으로부터 보호됨
```

### 3. 설정 방법

```bash
echo -1000 > /proc/$(pidof mysqld)/oom_score_adj

echo 1000 > /proc/$(pidof stress_worker)/oom_score_adj

echo -500 > /proc/1234/oom_score_adj

cat /proc/1234/oom_score_adj

for pid in /proc/[0-9]*/oom_score_adj; do
  echo "$pid: $(cat $pid)"
done
```

> **비유**: -1000은 "관람석 VIP 패스"로 경기장이 폭주해도 VIP는 안전하다. +1000은 "가장 앞줄 석"으로 불이 나면 제일 먼저 대피(퇴장)해야 한다.

---

## 3. 구조 및 원리

**핵심 조건**: 운영체제의 해당 메커니즘은 현재 상태 정보, 자원 제약, 정책 기준이 함께 정합성을 가질 때 안정적으로 동작한다.

동작 순서:
1. **요청 또는 이벤트 발생**: 사용자 요청, 인터럽트, 시스템 호출 등으로 커널이 해당 기능을 처리할 필요가 생긴다.
2. **현재 상태 확인**: 커널은 큐, 제어 블록, 메타데이터, 자원 가용량을 확인해 실행 가능 여부와 우선순위를 판단한다.
3. **정책 적용 및 자원 배정**: 해당 주제의 핵심 정책에 따라 상태 전이, 자원 할당, 보호 검사를 수행한다.
4. **결과 반영 및 후속 처리**: 처리 결과를 시스템 상태에 기록하고 다음 인터럽트·스케줄링·복구 단계로 연결한다.

### 1. systemd의 OOMScoreAdjust 지시자

systemd 서비스 유닛 파일에서 `OOMScoreAdjust`를 설정하면 서비스 시작 시 자동으로 `/proc/[pid]/oom_score_adj`가 설정된다.

```ini
[Unit]
Description=Production Database
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/postgres -D /var/lib/pgsql/data
Restart=always
OOMScoreAdjust=-500       # 데이터베이스 보호
MemoryHigh=6G             # cgroup 메모리 soft limit
MemoryMax=8G              # cgroup 메모리 hard limit

[Install]
WantedBy=multi-user.target
```

```
systemd 서비스별 OOMScoreAssign 기본값

+-------------------------------------------+
|  systemd 프로세스 자체:      -1000 (보호)   |
|  시스템 서비스 (default):         0        |
|  사용자 서비스 (default):         0        |
|  커스텀 설정:             -1000 ~ +1000   |
+-------------------------------------------+

주의: systemd는 --user 인스턴스에서도 OOMScoreAdjust를 적용함
```

### 2. systemd 설정 확인

```bash
systemctl show production-db.service | grep OOM

systemctl status --no-pager | awk '{print $1}' | while read svc; do
  score=$(systemctl show "$svc" 2>/dev/null | grep OOMScoreAdjust | cut -d= -f2)
  echo "$svc: $score"
done
```

---

## 4. 비교 및 연결

### 1. systemd의 OOMScoreAdjust 지시자

systemd 서비스 유닛 파일에서 `OOMScoreAdjust`를 설정하면 서비스 시작 시 자동으로 `/proc/[pid]/oom_score_adj`가 설정된다.

```ini
[Unit]
Description=Production Database
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/postgres -D /var/lib/pgsql/data
Restart=always
OOMScoreAdjust=-500       # 데이터베이스 보호
MemoryHigh=6G             # cgroup 메모리 soft limit
MemoryMax=8G              # cgroup 메모리 hard limit

[Install]
WantedBy=multi-user.target
```

```
systemd 서비스별 OOMScoreAssign 기본값

+-------------------------------------------+
|  systemd 프로세스 자체:      -1000 (보호)   |
|  시스템 서비스 (default):         0        |
|  사용자 서비스 (default):         0        |
|  커스텀 설정:             -1000 ~ +1000   |
+-------------------------------------------+

주의: systemd는 --user 인스턴스에서도 OOMScoreAdjust를 적용함
```

### 2. systemd 설정 확인

```bash
systemctl show production-db.service | grep OOM

systemctl status --no-pager | awk '{print $1}' | while read svc; do
  score=$(systemctl show "$svc" 2>/dev/null | grep OOMScoreAdjust | cut -d= -f2)
  echo "$svc: $score"
done
```

---

## 5. 실무 적용 및 판단

### 1. Pod QoS (Quality of Service)와 oom_score_adj 매핑

Kubernetes는 Pod의 리소스 설정(Request/Limit)에 따라 QoS 클래스를 부여하고, 이에 따라 컨테이너 프로세스의 `oom_score_adj`를 자동 설정한다.

```
Kubernetes Pod QoS 매핑 구조

+--------------------------------------------------------------+
|  Guaranteed (보장됨)                                          |
|    Request = Limit (동일)                                     |
|    예: requests.memory=1Gi, limits.memory=1Gi                |
|    oom_score_adj = -998                                      |
|    --> OOM 발생 시 가장 마지막에 종료                          |
+--------------------------------------------------------------+
|  Burstable (가변)                                             |
|    Request < Limit (Request만 설정 또는 둘 다 설정)             |
|    예: requests.memory=256Mi, limits.memory=1Gi              |
|    oom_score_adj = min(0, 999 - (1000 * request / node_total))|
|    --> 중간 우선순위                                          |
+--------------------------------------------------------------+
|  BestEffort (최선 노력)                                        |
|    Request 미설정, Limit 미설정                                |
|    oom_score_adj = 1000                                      |
|    --> OOM 발생 시 가장 먼저 종료                              |
+--------------------------------------------------------------+
```

### 2. 실제 oom_score_adj 계산 예시

```
노드 메모리: 8GB (8192 MiB)

[Guaranteed Pod]
  Container A: request=memory:4Gi, limit=memory:4Gi
  oom_score_adj = -998

[Burstable Pod]
  Container B: request=memory:2Gi, limit=memory:4Gi
  oom_score_adj = 999 - (1000 * 2048 / 8192)
               = 999 - 250
               = 749

  Container C: request=memory:512Mi, limit=memory:2Gi
  oom_score_adj = 999 - (1000 * 512 / 8192)
               = 999 - 62
               = 937

[BestEffort Pod]
  Container D: (request/limit 미설정)
  oom_score_adj = 1000

OOM 발생 시 종료 순서: D --> C --> B --> A
```

### 3. 노드 OOM 시 Pod 종료 프로세스

```
Kubernetes 노드 OOM 발생 시 처리 흐름

[OOM 발생]
    |
    v
[Kubelet이 노드 상태 조건(NodeCondition) 업데이트]
    Status: MemoryPressure=True
    |
    v
[OOM Killer가 oom_score_adj 기준으로 프로세스 종료]
    BestEffort Pod 먼저 종료 (oom_score_adj=1000)
    |
    v
[Pod 내 컨테이너 종료 감지]
    kubelet이 ContainerStatus Changed 이벤트 수신
    |
    v
[Pod 재시작 정책 적용]
    RestartPolicy=Always --> 컨테이너 재시작
    RestartPolicy=Never --> Pod 상태를 Completed/Failed로 변경
    |
    v
[이벤트 기록]
    kubectl describe node | grep OOM
    kubectl describe pod | grep OOMKilled
```

> **비유**: Kubernetes의 QoS 매핑은 "비상 상황 시 대피 우선순위표"다. Guaranteed는 "소방관(필수 인원)", Burstable은 "일반 직원", BestEffort는 "방문객"이다. 방문객이 먼저 대피하고, 소방관은 마지막까지 남는다.

---

## 6. 기대효과 및 결론

### 1. 모니터링 설정

```bash
#!/bin/bash
echo "=== Top 10 OOM Risk Processes ==="
ps -eo pid,comm,rss,oom_score,oom_score_adj --sort=-oom_score | head -11

echo ""
echo "=== Protected Processes (oom_score_adj < 0) ==="
for pid in /proc/[0-9]*; do
  adj=$(cat "$pid/oom_score_adj" 2>/dev/null)
  if [ "$adj" -lt 0 ] 2>/dev/null; then
    comm=$(cat "$pid/comm" 2>/dev/null)
    echo "PID=$(basename $pid) COMM=$comm OOM_ADJ=$adj"
  fi
done
```

### 2. 주의사항

```
oom_score_adj 설정 시 주의사항

+--------------------------------------------------+
| 1. 권한 필요                                      |
|    root 또는 CAP_SYS_RESOURCE capability 필요       |
|    일반 사용자는 자신의 프로세스만 수정 가능          |
+--------------------------------------------------+
| 2. -1000 남용 금지                                 |
|    너무 많은 프로세스를 -1000으로 설정하면           |
|    OOM Killer가 선택할 프로세스가 없어짐             |
|    --> 시스템 전체 정지 가능                         |
+--------------------------------------------------+
| 3. 프로세스 재시작 시 초기화                         |
|    oom_score_adj는 /proc를 통한 런타임 설정          |
|    프로세스 재시작 시 기본값(0)으로 리셋              |
|    --> 영구 설정은 systemd/k8s에서 관리              |
+--------------------------------------------------+
| 4. cgroup과의 상호작용                              |
|    cgroup 메모리 제한과 oom_score_adj은 독립적       |
|    cgroup 제한 위반 시 cgroup 내에서만 OOM 발생      |
+--------------------------------------------------+
```

---

## 7. 발전 흐름도

```text
기초 자원 관리 문제
    ↓
oom_score_adj
    ↓
성능·격리·공정성 최적화
    ↓
가상화·관측·자동화 통합
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| oom_score_adj | 운영체제 자원 관리와 보호 정책이 실제로 적용되는 핵심 주제 |
| 커널 (Kernel) | 정책 집행, 상태 전이, 시스템 호출 처리의 중심 |
| 프로세스/스레드 | CPU, 메모리, 동기화 자원과 직접 연결되는 실행 단위 |
| 메모리/I/O | 성능 병목과 보호 요구사항이 함께 드러나는 연계 영역 |
| 가상화/보안 | 격리, 제어, 관측 확장 관점에서 해당 주제가 연결되는 상위 개념 |
