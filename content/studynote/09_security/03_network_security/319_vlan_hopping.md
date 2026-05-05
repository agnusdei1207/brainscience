+++
weight = 319
title = "319. VLAN 호핑 (VLAN Hopping)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: VLAN 호핑(VLAN Hopping)은 스위치의 VLAN (Virtual Local Area Network) 격리를 우회해 공격자가 속하지 않은 VLAN의 트래픽에 접근하는 L2 계층 공격으로, Switch Spoofing과 Double Tagging 두 가지 방식이 있다.
> 2. **가치**: VLAN은 논리적 네트워크 분리로 보안 경계를 제공하지만, 스위치 설정 실수(DTP 활성화, Native VLAN 미변경)가 있으면 이 경계가 무너져 물리적 분리 없이 접근 통제가 불가능해진다.
> 3. **판단 포인트**: 방어의 핵심은 DTP (Dynamic Trunking Protocol) 비활성화, Native VLAN 1 변경(또는 사용 금지), 사용하지 않는 포트의 명시적 접근 포트(Access Port) 설정이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

VLAN은 동일 물리 스위치에 연결된 장비들을 논리적으로 분리해 브로드캐스트 도메인을 나누고 보안 경계를 형성하는 핵심 네트워크 보안 기술이다. VLAN 10(일반 직원), VLAN 20(서버팀), VLAN 30(재무팀)으로 분리하면 서로의 트래픽이 라우터나 방화벽을 거치지 않고는 교환되지 않는다.

그러나 스위치의 트렁크(Trunk) 포트 자동 협상 기능과 IEEE 802.1Q 태그 처리 로직에 취약점이 존재한다. 공격자가 이를 악용하면 다른 VLAN의 트래픽에 접근할 수 있다. VLAN 호핑은 인증을 우회하거나 패스워드를 탈취하는 방식이 아니라, "네트워크 격리 자체를 무효화"한다는 점에서 더 근본적인 위협이다.

기업 환경에서 VLAN 호핑이 성공하면 재무 데이터, 서버 관리 트래픽, 내부 통신이 모두 노출될 수 있다. 스위치 설정 기본값에 의존하는 환경에서는 별도의 공격 도구 없이도 가능한 경우가 있어 특히 위험하다.

📢 **섹션 요약 비유**: VLAN 호핑은 아파트 단지에서 "1동 주민 전용" 엘리베이터를 몰래 타는 것이다. 엘리베이터 열쇠 없이 버튼 조작만으로 다른 동에 들어갈 수 있다면, 동별 분리가 의미 없어진다.

---

## 2. 구성요소

### 공격 방식 1: Switch Spoofing (스위치 사칭)

DTP (Dynamic Trunking Protocol)는 Cisco 스위치가 이웃 장비와 트렁크 포트를 자동으로 협상하는 프로토콜이다. 공격자 PC가 DTP 협상 프레임을 보내면, 스위치가 이를 이웃 스위치로 인식하고 트렁크 모드로 전환한다. 이후 공격자는 모든 VLAN의 태그된 트래픽을 수신·전송할 수 있다.

```
정상:
  스위치 포트 ← DTP 비활성화 → 단일 VLAN(Access 포트)

Switch Spoofing 공격:
  공격자 PC → DTP Negotiate 프레임 전송
  스위치 포트 → Trunk 모드로 전환
  공격자 ↔ 스위치: 모든 VLAN 트래픽 교환 가능
```

### 공격 방식 2: Double Tagging (이중 태깅)

802.1Q 태그는 VLAN ID를 패킷에 삽입한다. 스위치는 패킷 수신 시 외부 태그를 제거하고 내부 태그 기반으로 전달한다. 공격자가 Native VLAN(VLAN 1) 포트에서 이중 태그를 붙인 패킷을 보내면, 첫 번째 스위치는 외부 Native VLAN 태그를 제거하고 전달하고, 두 번째 스위치는 남은 내부 태그를 읽어 다른 VLAN으로 패킷을 전달한다.

```
Double Tagging 패킷 구조:
┌──────────────────────────────────────────────┐
│  Dst MAC │ Src MAC │ 802.1Q VLAN 1 │ 802.1Q VLAN 20 │ Payload │
└──────────────────────────────────────────────┘
         외부 태그(Native VLAN=1)  내부 태그(목표 VLAN=20)

처리 흐름:
  1단계 스위치: VLAN 1 포트에서 수신 → 외부 VLAN 1 태그 제거 → 트렁크로 전달
  2단계 스위치: VLAN 20 태그 읽음 → VLAN 20으로 패킷 전달
  → 공격자가 VLAN 20에 직접 패킷 전송 성공!
```

### 방어 기법 요약

| 방어 기법 | 대상 공격 | 설정 방법 |
|:---|:---|:---|
| DTP 비활성화 (`switchport nonegotiate`) | Switch Spoofing | 모든 엔드포인트 포트에 적용 |
| 명시적 Access 포트 설정 | Switch Spoofing | `switchport mode access` 강제 |
| Native VLAN 1 변경 | Double Tagging | 사용하지 않는 VLAN 번호로 변경 |
| Native VLAN 태깅 강제 | Double Tagging | `vlan dot1q tag native` 활성화 |
| 미사용 포트 비활성화 | 모든 공격 | `shutdown` + 별도 VLAN 할당 |
| VLAN 1 사용 금지 | Double Tagging | 관리용 VLAN 별도 지정 |

📢 **섹션 요약 비유**: Switch Spoofing은 "나도 스위치야"라고 속여 모든 통로를 열게 하는 것이고, Double Tagging은 봉투 안에 봉투를 넣어서 최종 목적지가 다른 곳에 도달하게 하는 것이다.

---

## 3. 구조 및 동작 원리

### Switch Spoofing vs Double Tagging 비교

| 비교 항목 | Switch Spoofing | Double Tagging |
|:---|:---|:---|
| 전제 조건 | DTP 활성화 상태 | Native VLAN = 공격자 포트 VLAN (기본 VLAN 1) |
| 방향성 | 양방향 통신 가능 | 단방향 (피해 VLAN → 공격자 불가) |
| 특수 장비 필요 | DTP 지원 NIC/도구 | 이중 태깅 가능 도구 |
| 탐지 난이도 | 중간 (DTP 프레임 이상) | 높음 (패킷 분석 필요) |
| 방어 방법 | DTP 비활성화 | Native VLAN 변경 + 태깅 강제 |

### VLAN 보안 전체 방어 레이어

```
┌──────────────────────────────────────────────┐
│         VLAN 보안 계층 구조                  │
│                                              │
│  L3: 방화벽 / ACL (VLAN 간 통신 제어)        │
│     │                                        │
│  L2: DAI + DHCP Snooping (ARP 오염 방어)     │
│     │                                        │
│  L2: VLAN 호핑 방어                          │
│     ├── DTP 비활성화                         │
│     ├── Native VLAN 변경                     │
│     └── 포트 보안 (Port Security)            │
│     │                                        │
│  L1: 물리적 포트 비활성화 (미사용)            │
└──────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: VLAN 보안은 아파트 보안 시스템이다. 현관 비밀번호(L3 방화벽), 동 입구 카드키(L2 VLAN 격리), 비어있는 동 출입 차단(미사용 포트 셧다운)이 모두 있어야 진짜 안전하다.

---

## 4. 비교 및 트레이드오프

### Cisco 스위치 VLAN 호핑 방어 설정

```
! 엔드포인트 포트 명시적 Access 설정
interface range GigabitEthernet0/1-24
  switchport mode access
  switchport access vlan 10
  switchport nonegotiate        ! DTP 완전 비활성화
  spanning-tree portfast        ! STP 수렴 가속
  spanning-tree bpduguard enable

! Native VLAN 변경 (VLAN 1 사용 금지)
interface GigabitEthernet0/25    ! 트렁크 포트
  switchport mode trunk
  switchport trunk native vlan 999  ! 비사용 VLAN으로 변경
  switchport trunk allowed vlan 10,20,30
  switchport nonegotiate

! VLAN 1 완전 비사용화
no vlan 1                         ! 일부 스위치는 삭제 불가
vlan 999
  name UNUSED_NATIVE

! 미사용 포트 비활성화 + 격리 VLAN 할당
interface range GigabitEthernet0/20-24
  switchport mode access
  switchport access vlan 888      ! 격리 VLAN
  shutdown
```

### 기술사 시험 판단 포인트

VLAN 호핑 문제에서 핵심은 두 공격 방식의 차이를 명확히 구분하고 각각의 방어 설정을 대응시켜 서술하는 것이다. Switch Spoofing → `switchport nonegotiate` + `switchport mode access`, Double Tagging → `switchport trunk native vlan 999` + `vlan dot1q tag native`를 정확히 짝지어야 한다.

또한 "VLAN만으로 충분한가?"라는 질문에 "VLAN은 논리적 분리일 뿐, 완전한 격리를 위해서는 L3 방화벽이 필요하다"는 관점을 추가하면 높은 수준의 답안이 된다.

📢 **섹션 요약 비유**: VLAN 호핑 방어 답안은 "문을 잠그고(DTP 비활성화), 비상구 번호를 바꾸고(Native VLAN 변경), 빈 방은 봉쇄하는(미사용 포트 차단)" 세 줄로 요약된다.

---

## 5. 실무 적용 및 최적화 기법

VLAN 호핑 방어 설정을 통해 조직은 내부 네트워크 분리의 신뢰성을 확보한다. DTP 비활성화와 Native VLAN 변경만으로 두 가지 주요 VLAN 호핑 공격이 모두 차단된다. 이는 스위치 CLI 설정만으로 구현되어 추가 비용이 없다.

그러나 VLAN 격리는 논리적 분리이며, 라우터나 방화벽 없이는 VLAN 간 완전한 격리가 보장되지 않는다. 특히 L3 스위치에서 VLAN 간 라우팅이 활성화된 경우, ACL (Access Control List)로 VLAN 간 불필요한 통신을 제한해야 완전한 보안이 달성된다.

VLAN 보안은 정기적인 포트 감사(Port Audit), VLAN 할당 검토, 트렁크 포트 허용 VLAN 목록 최소화를 통해 지속적으로 유지·관리되어야 한다.

📢 **섹션 요약 비유**: VLAN 방어 완료는 각 층(VLAN)별 전용 엘리베이터가 생기고, 엘리베이터 열쇠는 해당 층 주민만 갖고, 비어있는 층 엘리베이터는 아예 잠가두는 상태다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| VLAN (Virtual Local Area Network) | 공격 대상 격리 구조 | 논리적 네트워크 분리, IEEE 802.1Q 표준 |
| DTP (Dynamic Trunking Protocol) | Switch Spoofing 취약점 | Cisco 독점 트렁크 자동 협상 프로토콜 |
| 802.1Q 태그 | Double Tagging 취약점 | VLAN ID를 패킷에 삽입하는 표준 |
| Native VLAN | Double Tagging 악용 포인트 | 태그 없는 트래픽이 속하는 기본 VLAN |
| Trunk 포트 | 공격/방어 핵심 포인트 | 여러 VLAN 트래픽 동시 전송 |
| Access 포트 | 방어 설정 | 단일 VLAN만 허용, DTP 비활성화 |
| ACL (Access Control List) | 보완 방어 | L3 레벨에서 VLAN 간 통신 제어 |

### 👶 어린이를 위한 3줄 비유 설명

- VLAN 호핑은 "나는 다른 스위치야"라고 속이거나, 이중 봉투로 택배를 다른 층에 보내는 거야.
- 방어는 스위치에게 "절대 자동으로 통로를 열어주지 마"(DTP 비활성화)라고 설정하는 거야.
- 그리고 비상통로 번호(Native VLAN)를 바꿔서 이중 봉투 속임수도 막아버리는 거지.
