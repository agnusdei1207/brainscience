+++
weight = 313
title = "313. Known Hosts — SSH 서버 공개키 신뢰"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: `~/.ssh/known_hosts`는 한 번이라도 연결한 SSH 서버의 호스트 공개키를 저장하는 신뢰 데이터베이스로, 이후 접속 시 서버의 키가 바뀌면 MITM (Man-in-the-Middle) 공격 경고를 발생시켜 사용자를 보호한다.
> 2. **가치**: TOFU (Trust On First Use) 원칙을 구현해 별도의 PKI (Public Key Infrastructure) 없이도 서버 인증을 할 수 있으며, 대규모 환경에서는 SSHFP (SSH Fingerprint) DNS 레코드로 첫 접속 시점의 신뢰성을 강화할 수 있다.
> 3. **판단 포인트**: 자동화 환경(CI/CD, Ansible)에서 `StrictHostKeyChecking no`를 사용하면 MITM 방어가 완전히 무력화되므로, 대신 사전에 검증된 호스트 키를 `known_hosts`에 프로비저닝하거나 SSHFP DNS 레코드를 활용해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

SSH (Secure Shell)가 Telnet보다 우월한 핵심 이유 중 하나가 서버 인증이다. Telnet은 접속 대상이 진짜 서버인지 확인하지 않아 공격자가 중간에서 트래픽을 가로채는 MITM 공격에 무방비다. SSH는 서버가 고유한 호스트 키 쌍(Host Key Pair)을 보유하고, 클라이언트가 이를 `known_hosts` 파일로 관리해 서버의 신원을 지속적으로 검증한다.

`known_hosts`의 동작 원칙은 TOFU(Trust On First Use)다. 처음 접속 시 사용자에게 서버의 키 지문(fingerprint)을 보여주고 신뢰 여부를 묻는다. 수락하면 해당 서버의 공개키가 파일에 저장된다. 이후 접속 시마다 서버가 제시하는 공개키를 저장된 값과 비교해, 불일치하면 강력한 경고를 표시하고 접속을 중단한다.

그러나 TOFU에는 한계가 있다. 첫 번째 접속이 이미 MITM 상태라면 공격자의 키가 저장된다. 이 문제를 해결하는 방법이 대역 외(out-of-band) 키 검증이며, SSHFP DNS 레코드가 그 역할을 한다.

📢 **섹션 요약 비유**: known_hosts는 친구 얼굴 사진첩이다. 처음 만나면 얼굴을 찍어두고, 다음 만남에서 얼굴이 다르면 "이 사람 맞아?" 하고 경고한다.

---

## 2. 구성요소

### known_hosts 파일 구조

```
# ~/.ssh/known_hosts 파일 예시

# 형식: hostname [키_타입] [공개키_데이터]
github.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOMqqnkVzrm0SdG6UOoqKLsabgH5C9okWi0dh2l9GKJl
10.0.1.50  ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYA...
|1|hashed_hostname|base64_hash== ssh-ed25519 AAAA...  ← 해시된 hostname

# 와일드카드 항목 (권장하지 않음)
# *.internal.example.com ssh-rsa AAAA...
```

**호스트 키 저장 위치**:
- 사용자별: `~/.ssh/known_hosts`
- 시스템 전체: `/etc/ssh/ssh_known_hosts`

### SSH 서버 인증 흐름

```
최초 접속 시
Client                                       Server
  │                                            │
  │──── SSH 연결 요청 ──────────────────────►  │
  │◄─── Host Public Key (ed25519/ecdsa/rsa) ── │
  │                                            │
  │  known_hosts에서 hostname 검색             │
  │  ── 없음 ──►                               │
  │                                            │
  │  [경고 출력]                                │
  │  "The authenticity of host can't be        │
  │   established. ED25519 key fingerprint:    │
  │   SHA256:abc...xyz                         │
  │   Are you sure you want to continue? yes   │
  │                                            │
  │  known_hosts에 공개키 저장                  │
  │──── 인증 계속 ──────────────────────────►  │

이후 접속 시
  │◄─── Host Public Key ───────────────────── │
  │                                            │
  │  known_hosts에서 검색 ── 발견              │
  │  저장된 키와 비교                           │
  │  ┌─ 일치 → 인증 계속                       │
  │  └─ 불일치 → 강력 경고 + 접속 중단         │
  │                                            │
  │  [불일치 경고]                              │
  │  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      │
  │  @    WARNING: REMOTE HOST                 │
  │  @    IDENTIFICATION HAS CHANGED!          │
  │  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      │
```

### 호스트 키 타입별 특성

| 키 타입 | 알고리즘 | 키 길이 | 현재 권장 |
|:---|:---|:---|:---|
| ssh-rsa | RSA | 2048~4096 bit | ⚠️ OpenSSH 8.8부터 기본 비활성 |
| ecdsa-sha2-nistp256 | ECDSA P-256 | 256 bit | ✅ |
| ssh-ed25519 | Ed25519 | 256 bit | ✅✅ 최우선 권장 |
| sk-ssh-ed25519 | Ed25519 + FIDO2 | 256 bit | ✅✅ 하드웨어 키 |

📢 **섹션 요약 비유**: 호스트 키는 건물의 고유 DNA다. 매번 건물 입구에서 DNA를 스캔해, 이전에 방문한 건물 DNA와 다르면 "건물이 바뀐 것 아니냐"고 경고한다.

---

## 3. 구조 및 동작 원리

### SSHFP (SSH Fingerprint) DNS 레코드

SSHFP는 서버의 SSH 호스트 키 지문을 DNS에 등록해, 첫 접속 시 TOFU 대신 DNSSEC (DNS Security Extensions) 검증된 DNS 응답으로 호스트 키를 확인하는 방법이다.

```
# SSHFP 레코드 형식
; server.example.com 의 SSH 호스트 키 지문
server.example.com. IN SSHFP 4 2 9a52d5...  
; 형식: [키_타입] [해시_알고리즘] [지문_16진수]
; 키_타입: 1=RSA, 3=ECDSA, 4=Ed25519
; 해시_알고리즘: 1=SHA-1(폐기), 2=SHA-256

# 서버에서 SSHFP 레코드 생성
ssh-keygen -r server.example.com
```

```bash
# 클라이언트에서 SSHFP 검증 활성화
ssh -o "VerifyHostKeyDNS yes" user@server.example.com

# ~/.ssh/config에서 영구 설정
Host *.example.com
    VerifyHostKeyDNS yes
```

| 항목 | TOFU | SSHFP + DNSSEC |
|:---|:---|:---|
| 첫 접속 보호 | ❌ 취약 (이미 MITM이면 공격자 키 저장) | ✅ DNS로 사전 검증 |
| 설정 복잡도 | 매우 낮음 | 중간 (DNS 설정 필요) |
| DNSSEC 의존 | 불필요 | ✅ 필수 (없으면 의미 없음) |
| 기업 환경 적합 | 소규모 | 중대형 권장 |

📢 **섹션 요약 비유**: TOFU는 처음 만나는 사람 얼굴을 그냥 믿는 것, SSHFP+DNSSEC는 정부가 발급한 주민등록증으로 신원을 확인하는 것이다.

---

## 4. 비교 및 트레이드오프

**자동화 환경에서 안전한 known_hosts 관리**

```bash
# 잘못된 방법 — MITM 방어 무력화 (절대 프로덕션 사용 금지)
ssh -o "StrictHostKeyChecking no" user@server  # ❌

# 올바른 방법 1: 사전에 호스트 키를 known_hosts에 프로비저닝
# 서버 호스트 키 수집
ssh-keyscan -t ed25519 server.example.com >> ~/.ssh/known_hosts
# 단, 이 과정 자체도 MITM 위험이 있으므로 첫 실행은 신뢰 환경에서만

# 올바른 방법 2: HashKnownHosts로 호스트 이름 난독화
# /etc/ssh/ssh_config 또는 ~/.ssh/config
HashKnownHosts yes
# → 저장된 hostname이 해시됨, 파일 탈취 시 대상 서버 목록 노출 방지

# 특정 호스트 키 삭제 (서버 키 교체 후)
ssh-keygen -R server.example.com

# 저장된 지문 확인
ssh-keygen -l -f ~/.ssh/known_hosts

# 특정 호스트 키 지문 확인
ssh-keygen -l -E sha256 -f /etc/ssh/ssh_host_ed25519_key.pub
```

**CI/CD 파이프라인 권장 설정**

```yaml
# GitHub Actions 예시 — 사전 프로비저닝된 known_hosts 사용
- name: Setup SSH known_hosts
  run: |
    mkdir -p ~/.ssh
    echo "${{ secrets.KNOWN_HOSTS }}" >> ~/.ssh/known_hosts
    chmod 600 ~/.ssh/known_hosts
```

**기술사 판단 포인트**:
- 클라우드 환경에서 VM을 재생성하면 호스트 키가 바뀜 → `ssh-keygen -R ip` 후 재등록 필요
- IaC (Infrastructure as Code) 도구(Terraform, Ansible)에서 `host_key_checking = False` 설정은 보안 감사 지적 사항 → SSHFP 또는 Vault SSH CA로 대체
- SSH CA (Certificate Authority): 호스트 키를 CA가 서명하는 방식으로 known_hosts 없이도 신뢰 검증 가능한 엔터프라이즈 대안

📢 **섹션 요약 비유**: `StrictHostKeyChecking no`는 방문자 ID 확인을 아예 생략하는 것이다. 편하지만 가짜 방문자도 무조건 입장된다.

---

## 5. 실무 적용 및 최적화 기법

`known_hosts` 기반의 서버 인증은 별도의 PKI 인프라 없이도 MITM 공격을 방어하는 현실적인 메커니즘이다. TOFU의 한계는 SSHFP+DNSSEC 또는 SSH CA를 통해 보완할 수 있으며, 자동화 환경에서는 `StrictHostKeyChecking no` 대신 사전 프로비저닝된 `known_hosts`를 사용하는 것이 모범 사례다.

기술사 논술에서는 "TOFU 원칙의 동작과 한계 → SSHFP DNS 레코드로 첫 접속 보호 강화 → 엔터프라이즈 SSH CA로 중앙화된 신뢰 관리"의 흐름으로 기술 진화 로드맵을 제시하면 완성도 높은 답안이 된다.

📢 **섹션 요약 비유**: known_hosts는 내가 만든 신뢰하는 사람들의 사진첩이다. 처음 만나면 사진을 찍고, 다음 만남에서 얼굴이 달라지면 "이 사람이 아닐 수 있다"고 경고해준다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SSH Transport Layer | 상위 | 호스트 키 인증이 수행되는 계층 |
| TOFU | 원칙 | 최초 접속 시 키를 신뢰하고 이후 변경 감지 |
| SSHFP | 강화 수단 | DNS에 호스트 키 지문을 등록해 첫 접속 보호 |
| DNSSEC | 의존 | SSHFP 신뢰를 위한 DNS 서명 검증 |
| SSH CA | 엔터프라이즈 대안 | CA 서명 기반으로 known_hosts 불필요 |
| HashKnownHosts | 보안 강화 | hostname을 해시로 저장해 파일 탈취 피해 최소화 |

### 👶 어린이를 위한 3줄 비유 설명
1. known_hosts는 내가 방문한 집들의 초인종 소리를 기억하는 수첩이에요.
2. 다음 방문 시 초인종 소리가 다르면 "집을 바꿨거나 이상한 집이야!" 하고 경고해줘요.
3. SSHFP는 마을 게시판(DNS)에 각 집의 초인종 소리를 공식 등록해두어 처음 방문해도 진짜 집인지 확인하는 방법이에요.
