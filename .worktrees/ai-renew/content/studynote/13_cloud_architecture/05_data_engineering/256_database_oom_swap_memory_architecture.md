+++
weight = 256
title = "256. 데이터베이스 OOM 킬 대비 메모리 아키텍처"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Linux OOM Killer는 메모리 부족 시 oom_score가 높은 프로세스를 강제 종료하는데, DB 프로세스가 대상이 되면 서비스 장애로 직결된다 — Huge Pages, vm.swappiness=0, Cgroup 격리로 DB 메모리를 보호해야 한다.
> 2. **가치**: DB는 자체 메모리 풀(Buffer Pool)로 성능을 최적화하므로, 커널이 메모리를 스왑하거나 강제 종료하면 캐시 무효화 + 예기치 않은 재시작으로 치명적 데이터 일관성 문제가 발생한다.
> 3. **판단 포인트**: K8s 환경에서 DB 파드의 메모리 Request = Limit으로 설정(Guaranteed QoS)하여 OOM 우선순위를 낮추고, Huge Pages를 활용하여 TLB 미스 감소와 메모리 단편화를 동시에 해결한다.

---

## Ⅰ. 개요 및 필요성

DB 서버에서 새벽 4시에 갑자기 PostgreSQL이 종료되고, 에러 로그에 `Killed` 한 줄만 남아있는 상황. 이것이 **Linux OOM(Out of Memory) Killer**의 소행이다.

Linux 커널은 물리 메모리가 부족하면 OOM Killer를 발동하여 특정 프로세스를 강제 종료(SIGKILL)한다. 대상은 `oom_score`가 높은 프로세스로, 메모리를 많이 쓰고 실행 시간이 짧은 프로세스가 높은 점수를 받는다.

DB 프로세스는 의도적으로 메모리를 많이 사용(Buffer Pool)하므로 OOM Killer의 우선 타깃이 된다. 이를 방어하는 메모리 아키텍처 설계가 반드시 필요하다.

```
[OOM Killer 동작 원리]

물리 메모리 100% 소진
        │
        ▼
커널: OOM Killer 활성화
        │
        ▼
프로세스별 oom_score 계산
┌────────────────────────────────────┐
│ nginx:     oom_score = 50          │
│ app:       oom_score = 200         │
│ postgresql:oom_score = 800 ← 타깃! │
│ kernel:    oom_score = 0  (보호됨) │
└────────────────────────────────────┘
        │
        ▼
postgresql SIGKILL → 서비스 장애!
```

📢 **섹션 요약 비유**: OOM Killer는 배가 침몰할 때 가장 무거운 짐을 바다에 던지는 선장이다. DB(버퍼 풀)는 크고 무거운 짐이라 가장 먼저 버려진다. 이 짐이 사실은 가장 소중한 화물임에도 불구하고.

---

## Ⅱ. 아키텍처 및 핵심 원리

### OOM 방어 전략

| 전략 | 설정 | 효과 |
|:---|:---|:---|
| **oom_score_adj 조정** | `echo -1000 > /proc/[pid]/oom_score_adj` | -1000 시 OOM Killer 완전 제외 |
| **vm.swappiness 조정** | `sysctl -w vm.swappiness=0` | 스왑 사용 최소화 |
| **vm.overcommit_memory** | `sysctl -w vm.overcommit_memory=2` | 과다 메모리 할당 방지 |
| **Huge Pages** | `/sys/kernel/mm/hugepages/` 설정 | TLB 미스 감소, 단편화 방지 |
| **Cgroup Memory Limit** | systemd 또는 K8s 설정 | DB 메모리 상한 제어 |

### Huge Pages 아키텍처

```
일반 페이지 (4KB)                  Huge Pages (2MB)
┌─┬─┬─┬─┬─┬─┬─┬─┐               ┌──────────────────┐
│4│4│4│4│4│4│4│4│KB × 512개     │    2MB × 1개      │
└─┴─┴─┴─┴─┴─┴─┴─┘               └──────────────────┘

TLB 엔트리: 512개 필요             TLB 엔트리: 1개 필요
TLB 미스: 빈번                     TLB 미스: 거의 없음

Oracle/PostgreSQL/MySQL에서
1GB 이상 Buffer Pool 사용 시
Huge Pages 설정이 필수
```

### K8s 환경의 DB 메모리 보호

```yaml
# PostgreSQL StatefulSet 메모리 설정
apiVersion: apps/v1
kind: StatefulSet
spec:
  template:
    spec:
      containers:
      - name: postgres
        resources:
          requests:
            memory: "8Gi"   # Guaranteed QoS: request = limit
            hugepages-2Mi: "4Gi"
          limits:
            memory: "8Gi"   # request = limit → Guaranteed QoS
            hugepages-2Mi: "4Gi"
        env:
        - name: POSTGRES_SHARED_BUFFERS
          value: "2GB"       # 물리 메모리의 25% 권장
```

### K8s QoS 클래스와 OOM 우선순위

```
QoS 클래스           조건                    OOM 우선순위
──────────────────────────────────────────────────────
Guaranteed   request == limit (CPU+메모리)  가장 마지막에 종료
Burstable    request < limit 또는 일부만    중간 우선순위
BestEffort   request, limit 없음            가장 먼저 종료

→ DB 파드는 반드시 Guaranteed QoS 클래스!
```

📢 **섹션 요약 비유**: K8s QoS는 비행기 좌석 등급이다. 이코노미(BestEffort)는 초과 예약 시 가장 먼저 내려야 한다. 비즈니스(Guaranteed)는 보장된 좌석이라 절대 내리지 않아도 된다. DB는 무조건 비즈니스석이어야 한다.

---

## Ⅲ. 비교 및 연결

### vm.swappiness 설정 값별 동작

| 값 | 동작 | 적합 환경 |
|:---|:---|:---|
| 0 | 스왑 최대 회피 (물리 메모리 고갈 시에만 스왑) | DB 서버 권장 |
| 1 | 실질적으로 스왑 없음 (RHEL 7 권장) | DB 서버 대안 |
| 10 | 물리 메모리 90% 사용 후 스왑 | 일반 서버 |
| 60 | 기본값, 균형적 스왑 | 일반 데스크톱 |
| 100 | 스왑 최대 활용 | 메모리 제한 환경 |

### DB별 메모리 관련 핵심 파라미터

| DB | 핵심 파라미터 | 권장값 |
|:---|:---|:---|
| **PostgreSQL** | shared_buffers | 물리 메모리의 25% |
| **MySQL InnoDB** | innodb_buffer_pool_size | 물리 메모리의 70~80% |
| **Oracle** | SGA_TARGET | 물리 메모리의 40~60% |
| **Redis** | maxmemory | 전체 물리 메모리의 80% 이하 |
| **MongoDB** | wiredTigerCacheSizeGB | (물리 메모리 - 1GB) × 50% |

📢 **섹션 요약 비유**: DB 메모리 설정은 냉장고 공간 배분이다. 전체 냉장고(물리 메모리)에서 DB 식재료(Buffer Pool)에 얼마를 할당할지 정하는데, 너무 많으면 OS가 쓸 공간이 없고 너무 적으면 DB가 자꾸 디스크(스왑)를 뒤진다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### Linux DB 서버 메모리 최적화 체크리스트

```bash
# 1. Huge Pages 설정 확인
grep HugePages /proc/meminfo

# 2. vm.swappiness 설정 (영구 적용)
echo "vm.swappiness=0" >> /etc/sysctl.conf
sysctl -p

# 3. DB 프로세스 OOM 보호 (PostgreSQL 예시)
PID=$(pgrep postgres | head -1)
echo -1000 > /proc/$PID/oom_score_adj

# 4. 투명 Huge Pages 비활성화 (DB에서 권장)
echo never > /sys/kernel/mm/transparent_hugepage/enabled

# 5. Numa 설정 확인 (NUMA 아키텍처 서버)
numactl --hardware
```

### 메모리 아키텍처 설계 원칙

```
물리 메모리 32GB 서버 예시:

┌──────────────────────────────────────────┐
│ 물리 메모리 32GB                          │
│                                          │
│  OS 커널/시스템 예비    ▒▒▒▒▒▒   4GB     │
│  DB Buffer Pool (PG)  ▓▓▓▓▓▓▓▓   8GB    │
│  DB Work Memory       ████████   8GB     │
│  App/JVM Heap         ░░░░░░░░   8GB     │
│  스왑 사용             (0에 가깝게)         │
└──────────────────────────────────────────┘
```

### 기술사 시험 판단 포인트

- **OOM Killer 발동 원인**: 메모리 오버커밋(Overcommit) + 실제 물리 메모리 부족
- **Huge Pages vs THP(Transparent Huge Pages)**: DB에서는 THP 비활성화 권장 (성능 불안정)
- **K8s 환경**: DB를 K8s에 올릴 때 Guaranteed QoS + Stateful + PVC 조합 필수

📢 **섹션 요약 비유**: 메모리 아키텍처 설계는 사무실 자리 배치다. DB팀(버퍼 풀)은 이사와 계약한 자리(Guaranteed)라 아무도 뺏을 수 없고, 인턴(BestEffort 프로세스)은 빈자리 앉다가 자리가 부족하면 가장 먼저 쫓겨난다.

---

## Ⅴ. 기대효과 및 결론

### 기대효과

| 영역 | 효과 |
|:---|:---|
| **안정성** | OOM Killer로 인한 DB 프로세스 강제 종료 방지 |
| **성능** | Huge Pages로 TLB 미스 감소 → 쿼리 속도 향상 |
| **예측성** | vm.swappiness=0으로 메모리 성능 일관성 유지 |
| **K8s 운영** | Guaranteed QoS로 DB 파드 우선 보호 |

### 한계 및 주의사항

- **Huge Pages 유연성 부족**: 정적 Huge Pages는 한번 할당하면 반환이 어려움 (메모리 과소 할당 문제)
- **oom_score_adj -1000**: DB가 보호되는 대신 다른 프로세스가 종료될 수 있음 — 전체 메모리 계획 필요
- **K8s DB의 한계**: K8s는 원래 무상태(Stateless) 서비스를 위해 설계 — DB는 VM 또는 Bare Metal이 더 적합한 경우도 있음
- **스왑 완전 비활성화 위험**: 특수한 메모리 스파이크 상황에서 최악의 경우 시스템 전체 패닉 가능

📢 **섹션 요약 비유**: DB 메모리 보호는 중요 정부 시설 경호와 같다. VIP(DB)를 보호하면 할수록 다른 곳의 경비가 약해진다. 전체 메모리 예산을 계획하고 균형을 맞추는 것이 진짜 해법이다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Linux OOM Killer | 메모리 부족 시 프로세스 강제 종료 커널 메커니즘 |
| Huge Pages | 메모리 페이지 크기를 4KB→2MB로 확대하여 TLB 효율화 |
| K8s QoS | Guaranteed/Burstable/BestEffort 클래스별 OOM 우선순위 |
| Buffer Pool | DB가 디스크 데이터를 캐시하는 메모리 영역 |
| Cgroup | 프로세스 그룹별 리소스 제한 (K8s 기반 기술) |
| NUMA | 멀티소켓 서버에서 메모리 접근 비대칭 아키텍처 |

### 👶 어린이를 위한 3줄 비유 설명
1. 컴퓨터 메모리가 꽉 차면 리눅스가 몰래 프로그램을 강제로 끄는데, 이걸 OOM Killer라고 해.
2. DB는 메모리를 많이 쓰니까 항상 1순위 대상이 돼 - 근데 DB가 꺼지면 데이터가 날아가서 큰일 나!
3. 그래서 미리 DB에 "이건 절대 끄지 마!"라는 보호 표시(oom_score_adj=-1000)를 붙여두는 거야.
