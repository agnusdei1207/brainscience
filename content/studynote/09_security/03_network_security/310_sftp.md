+++
weight = 310
title = "310. SFTP — SSH 기반 파일 전송 (SSH File Transfer Protocol)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: SFTP (SSH File Transfer Protocol)는 FTP (File Transfer Protocol)와 이름이 비슷하지만 완전히 다른 독립적 프로토콜로, SSH (Secure Shell) 세션 안에서 실행되는 서브시스템으로 모든 파일 작업이 암호화 채널을 통해 이루어진다.
> 2. **가치**: 파일 전송에 별도 포트나 복잡한 방화벽 설정 없이 SSH 포트(22)만으로 모든 파일 작업(업로드·다운로드·디렉터리 생성·삭제)을 처리할 수 있으며, chroot jail로 접근 범위를 엄격히 제한할 수 있다.
> 3. **판단 포인트**: FTP·FTPS·SFTP 중 신규 시스템에서는 반드시 SFTP를 선택하며, FTPS (FTP over TLS)는 레거시 호환이 필요한 경우에만 고려한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

고전적인 FTP는 제어 채널(포트 21)과 데이터 채널(포트 20 또는 임의 포트)을 분리해 사용하며, 모든 데이터를 평문으로 전송한다. 이는 세 가지 문제를 낳는다. 첫째, 자격 증명(아이디·비밀번호)이 네트워크에 평문 노출된다. 둘째, 수동 모드(PASV)에서 임의 포트를 열어야 해 방화벽 설정이 복잡하다. 셋째, NAT (Network Address Translation) 환경에서 데이터 채널 포트 협상이 자주 실패한다.

SFTP는 이 문제들을 모두 해결한다. SSH 세션 위에서 동작하므로 단일 TCP 포트 22만 사용하고, 모든 트래픽이 AES-256-GCM으로 암호화된다. 별도의 데이터 채널이 없으므로 방화벽 설정도 단순하다.

기업 환경에서 SFTP는 파트너사와의 파일 교환, 배치 ETL (Extract, Transform, Load) 데이터 수집, 고객 데이터 수신 등에 광범위하게 사용된다. PCI-DSS (Payment Card Industry Data Security Standard)는 카드 데이터 전송에 암호화 채널 사용을 의무화하므로 FTP는 명백한 위반이다.

📢 **섹션 요약 비유**: SFTP와 FTP는 이름만 비슷한 전혀 다른 배달 서비스다. FTP는 내용물을 투명 봉투에 담아 배달, SFTP는 금속 잠금 케이스에 넣어 배달한다.

---

## 2. 구성요소

### SFTP 동작 구조

```
클라이언트                      서버 (OpenSSH)
┌──────────────┐               ┌──────────────────────────────┐
│ SFTP 클라이언트│               │ sshd (포트 22)               │
│ (sftp, WinSCP│               │                              │
│  Cyberduck)  │               │ ┌──────────────────────────┐ │
│              │               │ │ SSH Transport Layer       │ │
│  SFTP 요청   │               │ │ (암호화 채널)             │ │
│  (open file  │◄──────────────►│ ├──────────────────────────┤ │
│   read/write │  SSH 세션     │ │ SSH Connection Protocol  │ │
│   mkdir, ls  │  (포트 22)    │ │                          │ │
│   rename,rm) │               │ │ subsystem sftp           │ │
│              │               │ │ → sftp-server 프로세스   │ │
└──────────────┘               │ └──────────────────────────┘ │
                               └──────────────────────────────┘
        단일 포트(22)만 사용, 모든 명령·데이터 암호화
```

### SFTP 주요 명령어

```bash
# SFTP 접속
sftp user@server

# 접속 후 명령어
sftp> ls              # 원격 디렉터리 목록
sftp> lls             # 로컬 디렉터리 목록
sftp> put localfile   # 업로드
sftp> get remotefile  # 다운로드
sftp> mput *.csv      # 다중 업로드
sftp> mkdir backups   # 원격 디렉터리 생성
sftp> rm old.csv      # 원격 파일 삭제
sftp> rename old new  # 이름 변경
sftp> chmod 644 file  # 권한 변경
sftp> exit
```

### FTP / FTPS / SFTP 삼각 비교

| 항목 | FTP | FTPS (FTP over TLS) | SFTP |
|:---|:---|:---|:---|
| 프로토콜 계층 | 독립 | FTP + TLS 래핑 | SSH 서브시스템 |
| 암호화 | ❌ 없음 | ✅ TLS | ✅ SSH |
| 포트 수 | 2개(21+데이터) | 2개(21/990+데이터) | 1개(22) |
| 방화벽 친화성 | ❌ 낮음 | ❌ 낮음 | ✅ 높음 |
| 자격증명 보호 | ❌ 평문 | ✅ | ✅ |
| 공개키 인증 | ❌ | ❌ | ✅ |
| chroot jail | 구현 복잡 | 구현 복잡 | ✅ 간단 |
| 현재 권장 | ❌ 폐기 | 레거시 호환만 | ✅ 신규 표준 |

📢 **섹션 요약 비유**: FTP는 엽서(내용 공개), FTPS는 봉투에 넣은 편지(내용 암호화, 봉투 구조는 FTP 유지), SFTP는 처음부터 다르게 설계된 암호 금낭(완전히 새로운 구조)이다.

---

## 3. 구조 및 동작 원리

### chroot jail로 SFTP 접근 제한

```bash
# /etc/ssh/sshd_config — SFTP 전용 사용자 그룹 설정
Match Group sftpusers
    ChrootDirectory /data/sftp/%u    # 사용자별 격리 디렉터리
    ForceCommand internal-sftp       # 셸 접근 차단, SFTP만 허용
    AllowTcpForwarding no
    X11Forwarding no

# 디렉터리 구조
# /data/sftp/alice/          ← ChrootDirectory (root 소유, 755)
# /data/sftp/alice/uploads/  ← 실제 쓰기 가능 디렉터리 (alice 소유)
```

**chroot 설정 시 필수 권한 규칙**:
- `ChrootDirectory` 자체는 반드시 `root` 소유 + `755` 권한
- 그 하위에 사용자 소유 디렉터리를 만들어야 쓰기 가능
- 이 규칙 위반 시 `"bad ownership or modes for chroot directory"` 오류 발생

📢 **섹션 요약 비유**: chroot jail은 특정 고객을 맞춤형 탈출 불가 개인 창고에 넣는 것이다. 창고 안에서만 물건을 넣고 뺄 수 있고 다른 공간은 볼 수 없다.

---

## 4. 비교 및 트레이드오프

**자동화 스크립트로 SFTP 사용**

```bash
# 비대화형 SFTP 배치 전송 (배치 파일 사용)
sftp -b batch_commands.txt user@server

# batch_commands.txt 내용
put /local/data/*.csv /remote/uploads/
bye

# Python paramiko 라이브러리 활용
python3 -c "
import paramiko
transport = paramiko.Transport(('server', 22))
transport.connect(username='user', pkey=paramiko.Ed25519Key.from_private_key_file('/home/user/.ssh/id_ed25519'))
sftp = paramiko.SFTPClient.from_transport(transport)
sftp.put('local.csv', '/remote/uploads/local.csv')
sftp.close()
transport.close()
"
```

**기술사 판단 포인트**:
- SFTP vs SCP (Secure Copy Protocol): SFTP는 상태 저장 세션(디렉터리 탐색, 재개)을 지원하나 SCP는 단순 복사만 가능. 대규모 디렉터리 동기화는 `rsync over SSH`가 더 효율적
- 금융권 B2B 파일 교환: SFTP + 공개키 인증 + chroot jail 조합이 사실상 표준
- 감사 로깅: `internal-sftp` 서브시스템은 `LogLevel VERBOSE`로 모든 파일 접근 로그 기록 가능

📢 **섹션 요약 비유**: SFTP는 기업 전용 암호화 택배 시스템이다. 어떤 물건이 오가는지 로그가 남고(감사 로그), 지정된 창고에만 배달된다(chroot jail).

---

## 5. 실무 적용 및 최적화 기법

SFTP 도입으로 파일 전송 보안이 세 가지 차원에서 강화된다. 기밀성(AES-256-GCM 암호화), 무결성(HMAC-SHA2 검증), 인증(공개키 또는 비밀번호)이 모두 SSH 채널이 제공하는 보안 속성으로 자동 보장된다.

기술사 시험 관점에서 SFTP의 핵심 논점은 세 가지다. 첫째, FTP·FTPS·SFTP의 아키텍처 차이와 각 프로토콜의 보안 특성. 둘째, chroot jail을 이용한 최소 권한 원칙 구현. 셋째, 대규모 파일 동기화에서 SFTP 대신 rsync over SSH를 선택하는 설계 판단.

📢 **섹션 요약 비유**: SFTP를 쓰는 것은 보안 금고 배달 서비스로 업그레이드하는 것이다. 외부에서 오는 모든 배달물이 검사되고, 허가된 창고에만 들어갈 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SSH Connection Protocol | 상위 | SFTP가 동작하는 서브시스템 계층 |
| chroot jail | 보안 강화 | 사용자 파일시스템 접근 범위 제한 |
| SCP | 비교 대상 | 단순 파일 복사 (SFTP보다 기능 적음) |
| rsync over SSH | 대안 | 대용량 디렉터리 동기화에 효율적 |
| FTP | 대체 대상 | 보안 미비로 폐기 권장 |
| PCI-DSS | 규정 | 카드 데이터 전송 암호화 요구 |

### 👶 어린이를 위한 3줄 비유 설명
1. SFTP는 인터넷을 통해 파일을 주고받을 때 쓰는 특수 잠금 택배 서비스예요.
2. 일반 FTP가 투명 봉투라면, SFTP는 열쇠 없이 못 여는 금속 상자예요.
3. 특별히 정해진 사람만 정해진 창고에 물건을 넣고 뺄 수 있어서, 실수로 다른 창고를 건드릴 수 없어요.
