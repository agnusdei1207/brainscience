+++
weight = 314
title = "314. SSH 서버 강화 설정 (SSH Server Hardening)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: SSH (Secure Shell)는 암호화된 원격 접속을 제공하지만, 기본 설정 그대로 운영하면 무차별 대입 공격(Brute Force)·루트 탈취·포트 스캔에 무방비 상태가 된다.
> 2. **가치**: `/etc/ssh/sshd_config` 설정 몇 줄만 바꿔도 공격 표면(Attack Surface)을 90% 이상 줄일 수 있어, 비용 대비 보안 효과가 가장 높은 강화 작업 중 하나다.
> 3. **판단 포인트**: 기술사 시험에서 "운영 서버 침입 사고 원인 분석"이나 "최소 권한 원칙" 문제에서 SSH 설정 항목을 직접 열거하고 그 이유를 논리적으로 서술해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

SSH (Secure Shell)는 Telnet을 대체하기 위해 1995년 등장한 암호화 기반 원격 관리 프로토콜로, 현재 RFC 4251~4254로 표준화되어 있다. 기본 포트 22번은 인터넷에 노출된 서버라면 하루에도 수천 번씩 스캔 대상이 되며, 봇넷(Botnet)이 자동으로 패스워드를 시도하는 무차별 대입 공격이 24시간 진행된다.

문제는 SSH 데몬(SSHd, SSH Daemon)의 설치 기본값이 "편의성 우선"으로 설계되어 있다는 점이다. `PasswordAuthentication yes`, `PermitRootLogin yes`, `Port 22` 등 기본 설정을 그대로 두면 누구나 루트 계정으로 패스워드만 알면 접속할 수 있다. 이를 방치한 채 방화벽만 믿는 것은 현관문은 잠갔는데 창문을 열어 둔 것과 같다.

SSH 강화 설정은 별도 소프트웨어 구매 없이 설정 파일 편집만으로 구현되므로, 보안 예산이 제한된 환경에서도 즉시 적용 가능하다. 관리자가 반드시 이해하고 적용해야 할 "제로 코스트(Zero Cost) 보안 활동"이다.

📢 **섹션 요약 비유**: 기본 SSH 설정은 잠금장치 없이 열쇠 구멍이 표준 규격인 자물쇠다. 강화 설정은 구멍 위치를 바꾸고, 지문 인식기를 달고, 관리자만 들어올 수 있게 이름표를 붙이는 작업이다.

---

## 2. 구성요소

### 핵심 설정 항목 요약

| 설정 지시자 | 기본값 | 권장값 | 보안 효과 |
|:---|:---:|:---:|:---|
| `Port` | 22 | 비표준 포트(예: 2222) | 자동화 스캐너 80% 이상 차단 |
| `PermitRootLogin` | yes | no | 루트 직접 탈취 경로 제거 |
| `PasswordAuthentication` | yes | no | 패스워드 기반 무차별 대입 원천 차단 |
| `MaxAuthTries` | 6 | 3 | 패스워드 추측 기회 최소화 |
| `AllowUsers` / `AllowGroups` | (없음) | 명시 설정 | 화이트리스트(Whitelist) 기반 접속 |
| `X11Forwarding` | yes | no | X11 프로토콜 터널링 악용 방지 |
| `LoginGraceTime` | 120s | 30s | 미인증 세션 점유 시간 축소 |
| `ClientAliveInterval` | 0 | 300 | 유휴 세션(Idle Session) 자동 종료 |
| `PubkeyAuthentication` | yes | yes | 공개키 인증 유지 |
| `Protocol` | 2,1 (구버전) | 2 | SSHv1 취약점(SSHv1 Vulnerability) 완전 차단 |

### 설정 파일 흐름 다이어그램

```
클라이언트                            SSH 데몬(SSHd)
    │                                     │
    │──── TCP SYN → Port 22(기본) ────────►│
    │                                     │
    │  [1] PermitRootLogin no             │
    │  [2] AllowUsers deploy              │  ← 화이트리스트 검사
    │  [3] MaxAuthTries 3                 │  ← 시도 횟수 제한
    │  [4] PasswordAuthentication no      │  ← 패스워드 거부
    │  [5] PubkeyAuthentication yes       │  ← 공개키만 허용
    │                                     │
    │◄──── 인증 성공 또는 연결 차단 ──────│
    │                                     │
    │  세션 성립 후:                       │
    │  [6] X11Forwarding no               │  ← 그래픽 터널 차단
    │  [7] ClientAliveInterval 300        │  ← 유휴 세션 정리
    └─────────────────────────────────────┘
```

### 공개키 인증(Public Key Authentication) 원리

```
┌─────────────────────────────────────────────┐
│  클라이언트: ~/.ssh/id_rsa (개인키, Private) │
│  서버:       ~/.ssh/authorized_keys (공개키) │
│                                             │
│  1. 클라이언트 → 서버: 공개키 제시          │
│  2. 서버: authorized_keys에서 대조          │
│  3. 서버 → 클라이언트: 랜덤 챌린지(Challenge)│
│  4. 클라이언트: 개인키로 서명(Sign)          │
│  5. 서버: 공개키로 서명 검증 → 인증 성공    │
└─────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 공개키 인증은 자물쇠(공개키)를 서버에 미리 설치하고, 열쇠(개인키)는 본인만 갖는 방식이다. 패스워드는 "비밀번호를 외우는" 방식이지만, 공개키는 "열쇠 없이는 절대 못 여는" 방식이다.

---

## 3. 구조 및 동작 원리

### 인증 방식 비교

| 구분 | 패스워드 인증 | 공개키 인증 | OTP (One-Time Password) 기반 |
|:---|:---|:---|:---|
| 보안 강도 | 낮음 | 높음 | 높음 |
| 무차별 대입 취약 | 예 | 아니오 | 아니오 |
| 관리 복잡도 | 낮음 | 중간 | 높음 |
| 서버 탈취 시 피해 | 패스워드 노출 | 개인키 미유출 | 서버 단독 피해 |
| 권고 사용 환경 | 개발/테스트 한정 | 운영 서버 기본 | 고보안 환경 |

### 연관 방어 도구

| 도구 | 역할 | SSH와 연계 방법 |
|:---|:---|:---|
| `fail2ban` | 로그인 실패 IP 자동 차단 | MaxAuthTries와 연동하여 임계치 초과 시 iptables 차단 |
| `AllowUsers` | 허용 계정 화이트리스트 | 서비스 계정만 명시, 일반 계정 차단 |
| 방화벽(Firewall) | 포트 수준 접근 제어 | 특정 관리 IP 대역만 Port 허용 |
| SELinux / AppArmor | MAC(Mandatory Access Control) | SSHd 프로세스 권한 최소화 |

📢 **섹션 요약 비유**: SSH 강화는 여러 겹의 자물쇠 시스템이다. 포트 변경은 문 위치를 바꾸고, AllowUsers는 초대장 목록 확인이며, fail2ban은 문 앞에서 수상한 사람을 내쫓는 경비원이다.

---

## 4. 비교 및 트레이드오프

### 단계별 강화 절차

**Step 1. 백업 및 현재 설정 확인**
```bash
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
sshd -T | grep -E "port|root|password|maxauth"
```

**Step 2. 핵심 설정 적용**
```
Port 2222
PermitRootLogin no
PasswordAuthentication no
MaxAuthTries 3
AllowUsers deploy admin
X11Forwarding no
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
```

**Step 3. 검증 및 재시작**
```bash
sshd -t          # 문법 오류 확인
systemctl reload sshd   # 기존 세션 유지하며 재로드
```

### 기술사 시험 판단 포인트

기술사 시험에서 SSH 강화 설정 문제가 나올 때 핵심은 **"왜 이 설정이 필요한가"를 공격 시나리오와 연결**해 서술하는 것이다. 예를 들어 `PermitRootLogin no`는 "루트 계정은 패스워드를 알면 즉시 전체 시스템 제어권을 획득할 수 있으므로, sudo를 통한 권한 상승 단계를 강제해 감사 로그(Audit Log)를 남기기 위함"이라고 설명해야 한다.

`MaxAuthTries 3`은 단독으로는 불완전하다. 공격자는 연결을 끊고 재시도하므로 `fail2ban`과 함께 사용해야 의미 있는 방어가 된다는 점도 언급해야 한다.

📢 **섹션 요약 비유**: 의사가 처방전 없이 약을 줄 수 없듯, SSH 강화 설정도 "이 설정이 어떤 공격을 막는지"를 정확히 설명할 수 있어야 올바른 처방이다.

---

## 5. 실무 적용 및 최적화 기법

SSH 서버 강화 설정을 통해 조직은 다음 효과를 기대할 수 있다. 첫째, 자동화된 봇(Bot) 기반 무차별 대입 공격을 포트 변경과 공개키 전환만으로 거의 완전히 차단한다. 둘째, 내부자 위협(Insider Threat)에 대해서도 AllowUsers 화이트리스트와 감사 로그를 통해 접근 추적이 가능해진다. 셋째, 유휴 세션 제한으로 세션 하이재킹(Session Hijacking) 위험이 감소한다.

ISMS-P (Information Security Management System - Personal information)와 같은 인증 체계에서도 원격 접근 통제는 필수 점검 항목이며, 설정 파일 스냅샷이 증거 자료로 활용된다. 단기적으로는 설정 변경에 따른 기존 접속 방식 변경으로 사용자 불편이 생기지만, 장기적으로는 사고 대응 비용 절감 효과가 압도적으로 크다.

SSH 강화 설정은 한 번 적용으로 끝나지 않는다. 정기적인 `sshd_config` 점검, 공개키 로테이션(Rotation), 미사용 계정 정리가 병행되어야 지속적인 보안 수준을 유지할 수 있다.

📢 **섹션 요약 비유**: SSH 강화 설정은 집 보안 점검이다. 처음 한 번 자물쇠를 교체하고, 주기적으로 창문 잠금을 확인하고, 이사 간 사람의 열쇠는 반납받아야 안전이 유지된다.

---

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SSH (Secure Shell) | 기반 프로토콜 | 암호화 원격 접속 표준 (RFC 4251~4254) |
| SSHv1 | 취약 버전 | CRC32 취약점 존재, Protocol 2 전용으로 차단 필요 |
| 공개키 인증 | 핵심 방어 메커니즘 | 패스워드 무차별 대입 원천 차단 |
| `fail2ban` | 보완 도구 | MaxAuthTries와 연동, 임계치 초과 IP 자동 차단 |
| 최소 권한 원칙 (PoLP) | 보안 원칙 | AllowUsers/PermitRootLogin no 적용 근거 |
| 감사 로그 (Audit Log) | 사후 추적 | sudo 경유 강제로 접근 기록 확보 |
| ISMS-P | 인증 체계 | 원격 접근 통제 요구사항 포함 |

### 👶 어린이를 위한 3줄 비유 설명

- 기본 SSH 설정은 "누구나 열 수 있는 마스터키"가 존재하는 집이야.
- 강화 설정은 마스터키를 없애고, 내 열쇠로만 열리는 특수 자물쇠로 바꾸는 거야.
- 거기에 이름 목록(AllowUsers)까지 달아서, 허락된 사람만 문 앞에 올 수 있게 해두는 거지.
