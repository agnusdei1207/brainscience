+++
weight = 320
title = "320. BPDU — STP 제어 메시지 (Bridge Protocol Data Unit)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: BPDU (Bridge Protocol Data Unit)는 STP (Spanning Tree Protocol)가 네트워크 루프(Loop)를 방지하기 위해 스위치 간에 교환하는 제어 메시지로, 루트 브리지(Root Bridge) 선출과 포트 상태 결정에 사용된다.
> 2. **가치**: BPDU Guard는 엔드포인트 포트에서 BPDU가 수신되면 즉시 포트를 차단(err-disable)해 가짜 루트 브리지(Root Bridge) 주입과 STP 토폴로지 조작 공격을 원천 차단한다.
> 3. **판단 포인트**: PortFast와 BPDU Guard의 조합이 핵심이다. PortFast는 스위치 수렴 시간(Convergence Time)을 단축하지만, BPDU Guard 없이 단독으로 사용하면 STP 조작 공격에 취약해진다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

STP (Spanning Tree Protocol, IEEE 802.1D)는 이더넷 네트워크에서 스위치 간 경로 중복으로 발생하는 브로드캐스트 스톰(Broadcast Storm)과 MAC 테이블 불안정을 방지하는 프로토콜이다. STP는 네트워크 내 하나의 루트 브리지를 선출하고, 중복 경로를 차단 상태(Blocking)로 전환해 루프-프리(Loop-free) 토폴로지를 유지한다.

BPDU는 이 STP 프로세스의 핵심 메시지다. 스위치들은 주기적으로 BPDU를 교환하며 루트 브리지를 확인하고 토폴로지 변화를 전파한다. 일반 BPDU는 2초마다, TCN (Topology Change Notification) BPDU는 토폴로지 변경 시 전송된다.

보안 문제는 여기서 시작된다. 공격자가 자신의 PC나 스위치에서 낮은 Bridge ID 값을 가진 BPDU를 전송하면, 현재 루트 브리지보다 "더 좋은 후보"로 인식되어 네트워크 전체의 STP 루트 브리지가 교체된다. 이를 BPDU Spoofing 또는 루트 브리지 하이재킹(Root Bridge Hijacking)이라 한다. 공격자가 루트 브리지가 되면 네트워크 트래픽이 공격자를 경유하게 되어 MITM (Man-in-the-Middle) 공격이 가능해진다.

📢 **섹션 요약 비유**: STP는 교통 신호 시스템이고 BPDU는 신호 제어 메시지다. 공격자가 "내가 교통 본부야"라는 가짜 신호를 보내면 모든 신호가 혼란에 빠지고, 차량(트래픽)이 공격자 방향으로 유도된다.

---

## 2. 구성요소

### BPDU 구조 및 STP 루트 브리지 선출

```
BPDU 프레임 주요 필드:
┌────────────────────────────────────────────────┐
│  Protocol ID │ Version │ Message Type          │
│  Root ID (Bridge Priority + MAC)               │
│  Root Path Cost                                │
│  Bridge ID (송신 스위치)                        │
│  Port ID │ Message Age │ Max Age               │
│  Hello Time │ Forward Delay                    │
└────────────────────────────────────────────────┘

루트 브리지 선출 기준 (낮을수록 우선):
  1순위: Bridge Priority (기본 32768, 4096 단위 조정)
  2순위: MAC 주소 (낮은 값 우선)
```

### BPDU Spoofing 공격 흐름

```
정상 상태:
  루트 브리지 (우선순위 32768, MAC: 00:11:22:...)
    │
    ├── 스위치 A ── 스위치 B ── 스위치 C

공격 시작:
  공격자 PC → BPDU 전송 (우선순위 0 또는 4096)
    │
    ▼  스위치가 "더 좋은 루트 후보"로 인식
    │
  루트 브리지 교체 → 모든 트래픽이 공격자 경유
  → MITM 성립!
```

### BPDU Guard vs BPDU Filter 비교

| 기능 | BPDU Guard | BPDU Filter |
|:---|:---|:---|
| 동작 | BPDU 수신 시 포트 err-disable | BPDU 송수신 모두 차단 |
| 목적 | 보안 (공격 차단) | STP 토폴로지에서 포트 제외 |
| 경보 발생 | 있음 (로그 + SNMP) | 없음 |
| 포트 복구 | 수동 (`shutdown/no shutdown`) | 자동 (BPDU 수신 중단 시) |
| 권고 용도 | 엔드포인트 포트 (PortFast 포트) | 특수한 경우만 (주의 필요) |

### PortFast + BPDU Guard 조합 원리

```
PortFast 단독 사용:
  엔드포인트 포트 → STP 수렴 생략 → 즉시 Forwarding
  ⚠ 문제: 스위치/공격자 장비 연결 시 STP 조작 가능

PortFast + BPDU Guard 조합:
  엔드포인트 포트 → STP 수렴 생략 (빠른 연결)
  + BPDU 수신 감지 → 즉시 err-disable (차단)
  → 정상 PC는 빠르고, 악의적 스위치는 즉시 차단!
```

📢 **섹션 요약 비유**: PortFast는 VIP 전용 빠른 입장 통로다. 그런데 빠른 통로에는 경비가 없으면 위험하다. BPDU Guard는 그 빠른 통로에서 "스위치 흉내를 내는 침입자"를 즉시 차단하는 경비원이다.

---

## 3. 구조 및 동작 원리

### STP 보안 기능 전체 비교

| 기능 | 목적 | 방어 대상 |
|:---|:---|:---|
| BPDU Guard | 엔드포인트 포트 BPDU 차단 | Root Bridge Hijacking, STP 조작 |
| BPDU Filter | STP 토폴로지에서 포트 제외 | 특정 포트 STP 비참여 (남용 주의) |
| Root Guard | 특정 포트에서 더 우선 BPDU 수신 시 차단 | 현재 루트 브리지 보호 |
| Loop Guard | 단방향 링크 오류 시 루프 방지 | 단방향 링크 장애 |
| PortFast | 엔드포인트 빠른 연결 | STP 수렴 지연 제거 |

### BPDU Guard vs Root Guard 비교

```
BPDU Guard: 엔드포인트(PC, 서버) 포트에 적용
  → "이 포트에서 BPDU 오면 무조건 차단"
  → 즉시 err-disable, 관리자 확인 필요

Root Guard: 비루트 포트(스위치 간 연결)에 적용
  → "이 포트에서 현재 루트보다 좋은 BPDU 오면 차단"
  → Root-Inconsistent 상태, 자동 복구 가능
```

### 연관 STP 프로토콜 버전

| 프로토콜 | 표준 | 특징 |
|:---|:---:|:---|
| STP (Spanning Tree Protocol) | IEEE 802.1D | 원본, 수렴 속도 30~50초 |
| RSTP (Rapid STP) | IEEE 802.1w | 수렴 1~2초, 현재 표준 |
| MSTP (Multiple STP) | IEEE 802.1s | 여러 VLAN을 인스턴스로 묶음 |
| PVST+ (Per VLAN STP+) | Cisco 독점 | VLAN별 독립 STP 인스턴스 |

📢 **섹션 요약 비유**: BPDU Guard는 "이 문으로는 직원 카드만 가능"이고, Root Guard는 "이 문으로는 임원 출입 불가"다. 목적과 적용 포트가 다르지만 둘 다 STP 토폴로지 보호를 위한 것이다.

---

## 4. 비교 및 트레이드오프

### Cisco 스위치 BPDU Guard + PortFast 설정

```
! 방법 1: 전역(Global) 기본값 설정
spanning-tree portfast default       ! 모든 Access 포트에 PortFast
spanning-tree portfast bpduguard default  ! 모든 PortFast 포트에 BPDU Guard

! 방법 2: 개별 포트 설정 (권장)
interface range GigabitEthernet0/1-20
  switchport mode access
  spanning-tree portfast
  spanning-tree bpduguard enable

! err-disable 복구 확인
show interfaces GigabitEthernet0/5 status
! → err-disabled 상태 확인

! 포트 수동 복구
interface GigabitEthernet0/5
  shutdown
  no shutdown

! err-disable 자동 복구 설정 (선택)
errdisable recovery cause bpduguard
errdisable recovery interval 300     ! 5분 후 자동 복구
```

### Root Guard 설정 (업스트림 포트 보호)

```
! 현재 루트 브리지와 연결된 포트 외에 적용
interface GigabitEthernet0/25
  spanning-tree guard root
! → 이 포트에서 더 좋은 BPDU 수신 시 Root-Inconsistent 상태
```

### 기술사 시험 판단 포인트

BPDU/STP 보안 문제에서 핵심은 세 가지다. 첫째, BPDU Spoofing이 "왜 위험한가"를 루트 브리지 교체 → 트래픽 경로 변경 → MITM 순서로 설명. 둘째, PortFast + BPDU Guard 조합의 필요성을 "빠른 연결"과 "보안"이라는 두 목적의 조화로 서술. 셋째, BPDU Guard와 Root Guard의 적용 대상(엔드포인트 포트 vs 스위치 간 포트)을 명확히 구분해야 한다.

"BPDU Guard만으로 충분한가?"라는 심화 질문에는 Root Guard, Loop Guard를 계층적 방어로 추가 언급해 종합적 STP 보안 설계 능력을 보여줘야 한다.

📢 **섹션 요약 비유**: BPDU Guard 설정은 "직원 출입구에서 스위치 장비 반입 즉시 차단" 정책이다. 직원(PC)은 빠르게 입장하지만, 스위치 장비(BPDU 발신)는 문에서 바로 막힌다.

---

## 5. 실무 적용 및 최적화 기법

PortFast + BPDU Guard 조합은 스위치 보안 설정 중 가장 효과 대비 구현 비용이 낮은 기법이다. 엔드포인트 포트에 두 줄의 CLI 설정만으로 STP 기반 루트 브리지 하이재킹을 원천 차단하고, 동시에 PC나 서버의 네트워크 연결 속도도 향상시킨다.

Root Guard를 스위치 간 포트에 추가 적용하면 공격자가 트렁크 포트를 통해 더 좋은 BPDU를 주입하는 시도도 차단할 수 있다. 이 두 설정의 조합은 STP 보안의 기본 베이스라인(Baseline)으로, 모든 기업 스위치 환경에 의무적으로 적용되어야 한다.

RSTP (Rapid STP, IEEE 802.1w) 환경에서도 BPDU Guard와 Root Guard는 동일하게 동작하므로, STP 버전 마이그레이션 시에도 설정 변경 없이 유효하다. 장기적으로는 SDN (Software-Defined Networking) 환경에서의 STP 대체 기술(SPB, TRILL 등)과의 병행 고려도 필요하다.

📢 **섹션 요약 비유**: BPDU Guard + Root Guard 적용 완료는 교통 신호 시스템에 "가짜 교통 본부 신호 자동 차단" 기능을 달고, 본부 전용 회선에 "직원 외 접근 금지" 잠금을 건 상태다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| STP (Spanning Tree Protocol) | BPDU의 기반 프로토콜 | 루프 방지, IEEE 802.1D |
| RSTP (Rapid STP) | STP 개선 버전 | 수렴 속도 향상, IEEE 802.1w |
| Root Bridge | BPDU 공격 목표 | 네트워크 토폴로지 중심 스위치 |
| BPDU Guard | 핵심 방어 기능 | 엔드포인트 포트 BPDU 수신 시 err-disable |
| Root Guard | 보완 방어 기능 | 현재 루트보다 좋은 BPDU 차단 |
| PortFast | BPDU Guard 전제 | STP 수렴 생략, 엔드포인트 빠른 연결 |
| err-disable | BPDU Guard 동작 결과 | 포트 강제 비활성화, 관리자 확인 필요 |
| MITM (Man-in-the-Middle) | BPDU 공격 목표 | 루트 브리지 탈취 후 트래픽 도청 |

### 👶 어린이를 위한 3줄 비유 설명

- STP는 학교 복도에서 아이들이 부딪히지 않도록 일방통행 규칙을 정하는 것과 같아.
- BPDU Spoofing은 "내가 선생님이야"라고 거짓말해서 일방통행 방향을 마음대로 바꾸는 거야.
- BPDU Guard는 학생 출입문에서 "선생님 복장을 한 낯선 사람"을 즉시 차단하는 경비원이야.
