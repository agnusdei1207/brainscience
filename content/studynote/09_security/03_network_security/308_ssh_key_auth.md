+++
weight = 308
title = "308. SSH 공개키 인증 (SSH Key-Based Authentication)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: SSH (Secure Shell) 공개키 인증은 사용자의 공개키를 서버 `authorized_keys`에 등록한 뒤, 개인키로 서버 챌린지에 서명해 신원을 증명하는 방식으로 비밀번호를 네트워크에 전혀 전송하지 않는다.
> 2. **가치**: 비밀번호 없이 강력한 인증이 가능하며, 자동화 스크립트·CI/CD 파이프라인에서 사람이 개입하지 않는 무인 접속을 안전하게 구현할 수 있다.
> 3. **판단 포인트**: RSA 4096bit는 범용 호환성, Ed25519는 성능·보안·코드 품질 모든 면에서 우월하므로 신규 키는 Ed25519를, 레거시 호환이 필요한 경우만 RSA 4096bit를 선택한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

SSH 비밀번호 인증은 서버마다 다른 비밀번호를 기억하기 어렵고, 무차별 대입(Brute Force) 공격의 표적이 된다. 공개키 인증은 이 두 문제를 동시에 해결한다. 수백 개의 서버에 동일한 공개키를 배포해두면, 개인키 파일 하나(또는 ssh-agent에 적재된 키)로 모든 서버에 비밀번호 없이 접속할 수 있다.

비대칭 암호화 기반이므로 네트워크를 통해 비밀 정보가 이동하지 않는다. 서버는 챌린지를 암호화해 클라이언트에 보내고, 클라이언트는 개인키로만 풀 수 있는 서명을 반환한다. 개인키 자체는 클라이언트 장치를 절대 벗어나지 않는다. 따라서 네트워크를 아무리 도청해도 개인키를 얻을 수 없다.

기업 환경에서 공개키 인증은 CIS (Center for Internet Security) Benchmarks의 필수 항목이며, SOC 2 (Service Organization Control 2) 감사에서도 "특권 접근 관리"의 요건으로 요구된다.

📢 **섹션 요약 비유**: 공개키 인증은 자물쇠를 서버에 걸어두고 열쇠는 본인이 보관하는 방식이다. 자물쇠(공개키)가 노출되어도 열쇠(개인키) 없이는 문이 열리지 않는다.

---

## 2. 구성요소

### 공개키 인증 흐름

```
클라이언트 준비 단계 (1회)
  ssh-keygen → 개인키(id_ed25519) + 공개키(id_ed25519.pub) 생성
  ssh-copy-id user@server → 공개키를 서버 authorized_keys에 등록

인증 흐름 (매 접속 시)
┌──────────────────────────────────────────────────────┐
│ Client                              Server           │
│   │                                   │             │
│   │── SSH_MSG_USERAUTH_REQUEST ───────►│             │
│   │   (username, "publickey",          │             │
│   │    key_algorithm, public_key)      │             │
│   │                                   │             │
│   │   ┌────────────────────────────┐  │             │
│   │   │서버: authorized_keys에서   │  │             │
│   │   │공개키 탐색 → 발견 시       │  │             │
│   │   │챌린지 데이터 생성          │  │             │
│   │   └────────────────────────────┘  │             │
│   │◄── SSH_MSG_USERAUTH_PK_OK ────── │             │
│   │    (challenge 포함)               │             │
│   │                                   │             │
│   │  signature = Sign(개인키, challenge)│             │
│   │── SSH_MSG_USERAUTH_REQUEST ───────►│             │
│   │   (signature 포함)                │             │
│   │                                   │             │
│   │   ┌────────────────────────────┐  │             │
│   │   │서버: Verify(공개키,        │  │             │
│   │   │  challenge, signature)    │  │             │
│   │   │→ 검증 성공 시 접속 허용    │  │             │
│   │   └────────────────────────────┘  │             │
│   │◄── SSH_MSG_USERAUTH_SUCCESS ──── │             │
└──────────────────────────────────────────────────────┘
```

### 키 알고리즘 비교

| 항목 | RSA 4096bit | Ed25519 | ECDSA P-256 |
|:---|:---|:---|:---|
| 기반 수학 | 인수분해 | 에드워즈 타원 곡선 | 바이어슈트라스 타원 곡선 |
| 키 크기 | 4096 bit | 256 bit | 256 bit |
| 서명 크기 | 512 byte | 64 byte | 72 byte |
| 서명 속도 | 느림 | 매우 빠름 | 빠름 |
| 타이밍 공격 저항 | 구현 의존 | 설계 내장 | 구현 의존 |
| 랜덤성 요구 | 낮음 | 결정론적 | 높음(취약 RNG 시 키 노출) |
| 지원 범위 | 광범위 | OpenSSH 6.5+ | OpenSSH 5.7+ |
| 신규 권장 | 레거시 호환 | ✅ 최우선 권장 | 차선 |

### 파일 구조

```
클라이언트 측 ~/.ssh/
├── id_ed25519          ← 개인키 (chmod 600 필수)
├── id_ed25519.pub      ← 공개키 (서버에 배포)
├── config              ← 호스트별 접속 설정
└── known_hosts         ← 신뢰한 서버 호스트 키

서버 측 ~/.ssh/
└── authorized_keys     ← 허용된 공개키 목록 (chmod 600)
```

📢 **섹션 요약 비유**: Ed25519는 최신 고성능 자동차다. RSA 4096이 대형 화물차라면 Ed25519는 같은 짐을 훨씬 빠르고 효율적으로 나르는 소형 전기차다.

---

## 3. 구조 및 동작 원리

| 인증 방식 | 보안 | 편의성 | 자동화 | 비고 |
|:---|:---|:---|:---|:---|
| 비밀번호 | ⚠️ 브루트포스 위험 | 쉬움 | 어려움(평문 노출) | 비권장 |
| 공개키 | ✅ 강력 | 설정 후 편리 | ✅ 완전 자동화 | 권장 |
| TOTP (Time-based OTP) | ✅ 2FA | 불편 | ❌ 불가 | 추가 인증 수단 |
| 공개키 + Passphrase | ✅✅ 최강 | 불편(ssh-agent 활용) | ✅ agent 사용 시 | 프로덕션 권장 |

### `~/.ssh/config` 활용

```
# 기본 설정
Host *
    ServerAliveInterval 60
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519

# 프로젝트별 서버
Host prod-web
    HostName 10.0.1.100
    User deploy
    IdentityFile ~/.ssh/id_ed25519_prod
    Port 2222

Host dev-*
    HostName %h.example.internal
    User developer
    IdentityFile ~/.ssh/id_ed25519_dev
```

📢 **섹션 요약 비유**: `~/.ssh/config`는 전화번호부다. "엄마" 누르면 자동으로 번호 입력하듯, `ssh prod-web`이라고만 치면 IP·포트·사용자·키를 자동 적용한다.

---

## 4. 비교 및 트레이드오프

**키 생성 및 배포 절차**

```bash
# Ed25519 키 생성 (passphrase 반드시 설정)
ssh-keygen -t ed25519 -C "alice@company.com" -f ~/.ssh/id_ed25519

# 공개키를 서버에 배포
ssh-copy-id -i ~/.ssh/id_ed25519.pub alice@prod-server

# 수동 배포 방법 (ssh-copy-id 없는 경우)
cat ~/.ssh/id_ed25519.pub | ssh alice@prod-server \
  "mkdir -p ~/.ssh && chmod 700 ~/.ssh && \
   cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# 서버에서 비밀번호 인증 비활성화
# /etc/ssh/sshd_config
PasswordAuthentication no
PubkeyAuthentication yes
```

**Passphrase + ssh-agent 운영**

```bash
# 에이전트 시작 및 키 적재
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_ed25519
# → passphrase 1회 입력 후 세션 동안 재입력 불필요

# 키 목록 확인
ssh-add -l
```

**기술사 판단 포인트**:
- `authorized_keys` 파일 권한이 `644`이면 다른 사용자가 키를 추가 가능 → 반드시 `600` 유지
- 퇴직 직원의 공개키를 즉시 `authorized_keys`에서 삭제하는 절차 필수 (중앙화된 키 관리 도구: Vault, Teleport 권장)
- AWS EC2 키페어, GitHub Deploy Key 모두 이 메커니즘 기반

📢 **섹션 요약 비유**: Passphrase는 자물쇠(개인키 파일)에 또 다른 잠금장치를 추가한 것이다. 파일을 훔쳐도 passphrase를 몰라 쓸 수 없다.

---

## 5. 실무 적용 및 최적화 기법

SSH 공개키 인증은 현대 인프라 보안의 기초다. 무차별 대입 공격을 원천 차단하고, 자동화 파이프라인을 안전하게 운영하며, 유출된 비밀번호로 인한 침해 사고를 예방한다.

기술사 논술에서는 "공개키 인증의 수학적 원리(비대칭 암호화 기반 챌린지-응답) → 키 알고리즘 선택 기준(Ed25519 vs RSA) → 엔터프라이즈 환경에서의 키 생명주기 관리 방안"을 순서대로 전개하면 완성도 높은 답안이 된다.

📢 **섹션 요약 비유**: SSH 공개키 인증 도입은 은행 금고의 비밀번호를 지문 인식으로 교체하는 것이다. 비밀번호를 알아내려는 시도 자체가 무의미해진다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SSH User Auth Protocol | 상위 | 공개키 인증이 구현되는 계층 |
| Ed25519 | 권장 알고리즘 | Edwards 타원 곡선 서명 |
| ssh-agent | 연동 | 개인키를 메모리에 보관해 passphrase 반복 입력 방지 |
| authorized_keys | 저장소 | 서버 측 허용 공개키 목록 |
| SSH Agent Forwarding | 확장 | 에이전트를 원격 서버에서도 사용 |
| Vault / Teleport | 보완 도구 | 엔터프라이즈 중앙 키 관리 |

### 👶 어린이를 위한 3줄 비유 설명
1. 공개키 인증은 서버에 자물쇠를 달고 나만 가진 열쇠로 여는 것이에요.
2. 자물쇠(공개키)는 세상에 공개해도 되지만, 열쇠(개인키)는 내 컴퓨터 밖으로 절대 나가지 않아요.
3. Ed25519 열쇠는 매우 작지만 매우 단단해서, 큰 자물쇠(RSA 4096)보다 오히려 더 안전해요.
