+++
weight = 419
title = "경로 순회 (Path Traversal / Directory Traversal) — 파일 시스템 비정상 접근"
date = "2026-03-28"
[extra]
categories = ["studynote-security"]
+++
## 0. 핵심 인사이트

> "/var/www/html/images/../../../../etc/passwd"

> 📝 모범 답안

- **부적절한 경로 조작 공격**: 웹 애플리케이션이 사용자 입력값을 파일 경로로 사용할 때, `../` (점-점-슬래시) 시퀀스를 삽입하여 웹 루트를 벗어나 시스템의 민감한 파일에 접근하는 기법임.
- **기밀 정보 유출의 통로**: `/etc/passwd`, 윈도우 설정 파일, 소스 코드 등 웹 서비스와 무관한 운영체제 핵심 정보를 탈취하여 추가 공격의 발판으로 활용됨.
- **방어의 핵심은 입력 정규화**: 사용자 입력을 화이트리스트 방식으로 제한하고, 파일 접근 전 경로를 정규화(Canonicalization)하여 상위 디렉터리 이동을 원천 차단해야 함.

### 1. 개요 및 필요성
- **배경:** 많은 웹 서비스가 이미지 로딩이나 파일 다운로드를 위해 파일명을 파라미터로 받음 (예: `view.php?file=logo.jpg`). 이때 입력값 검증이 미흡하면 해커의 놀이터가 됨.
- **정의:** 공격자가 입력값에 상위 디렉터리를 가리키는 특수 기호(`../`)를 반복적으로 사용하여, 서버의 임의 디렉터리에 있는 파일에 접근하거나 실행하는 취약점임.
- **위험성:** 시스템 설정 파일 유출뿐만 아니라, LFI(Local File Inclusion)와 결합하여 원격 코드 실행(RCE)으로 이어질 수 있음.

### 2. 구성요소
```text
[ Path Traversal Attack Flow ]

Attacker Request:
GET /view?file=../../../../etc/passwd

Vulnerable Server Logic:
1. $base_path = "/var/www/html/images/";
2. $user_input = "../../../../etc/passwd";
3. $target_file = $base_path . $user_input;
   =   => Normalized: "/etc/passwd"

Execution:
Kernel opens /etc/passwd and returns content to Attacker.

Defense (Safe Way):
1. Use Whitelist (e.g., only alphanumeric)
2. Use basename() to strip paths
3. Check if realpath() starts with $base_path
```
- **공격 원리:** 운영체제가 파일 경로를 해석할 때 `../`를 현재 위치의 상위 부모 디렉터리로 인식한다는 점을 악용함.
- **우회 기법:** 단순 필터링 시 `%2e%2e%2f` (URL 인코딩), `..%5c` (윈도우 역슬래시), `....//` (이중 필터링 우회) 등을 사용하여 탐지를 회피함.

### 3. 구조 및 동작 원리
| 비교 항목 | 경로 순회 (Path Traversal) | LFI (Local File Inclusion) | RFI (Remote File Inclusion) |
| :--- | :--- | :--- | :--- |
| **주요 목표** | 파일 '읽기' (내용 유출) | 파일 '실행/포함' (코드 실행) | 원격지 파일 '실행' (백도어) |
| **공격 수단** | `../` 를 통한 경로 이탈 | 로컬 스크립트 엔진 활용 | 외부 URL 주입 |
| **위험 수준** | 높음 (정보 유출) | 매우 높음 (RCE 가능) | 치명적 (완전 제어) |
| **방어 전략** | 경로 정규화, 권한 제한 | 입력 검증, 설정 제한 | allow_url_include=Off |

### 4. 비교 및 트레이드오프
- **적용 사례:** 이미지 업로드/다운로드 모듈, 문서 뷰어 서비스, 설정 파일 동적 로드 로직.
- **기술사적 판단:** 단순히 `../` 문자열을 치환하는 방식은 인코딩 우회에 취약함. 가장 견고한 설계는 DB의 정수형 ID(PK)를 인자로 받고 서버 내부 맵핑 테이블을 통해 실제 경로를 찾아가는 **'간접 참조(Indirect Object Reference)'** 패턴을 적용하는 것임. 또한, 웹 프로세스의 권한을 최소화(chroot jail 등)하여 탈취 범위를 격리해야 함.

### 5. 실무 적용 및 최적화 기법
- **기대효과:** 서버의 파일 시스템 구조 노출을 방지하고, 운영체제 수준의 보안 위협을 원천 차단하여 시스템의 전반적인 기밀성을 강화함.
- **결론:** 경로 순회는 고전적이지만 여전히 빈번한 취약점임. Secure SDLC 단계에서 파일 입출력 함수 사용 시 정규화와 권한 검증을 기본 가이드라인으로 설정하여 내재적 보안을 실현해야 함.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 입력 데이터 검증 미흡, IDOR (부적절한 객체 참조)
- **하위/파생 개념:** LFI, RFI, Directory Indexing, Zip Slip (압축 해제 취약점)

### 👶 어린이를 위한 3줄 비유 설명
- 도서관 사서에게 "어린이 코너의 3번 책 꺼내줘"라고 해야 하는데, "어린이 코너 밖으로 나가서 관리자 아저씨의 비밀 일기장 꺼내줘"라고 속이는 거예요.
- 사서 선생님이 무심코 밖으로 나가서 가져다주면 비밀이 다 탄로 나겠죠?
- 그래서 사서 선생님은 "어린이 코너 밖의 물건은 절대 안 가져올 거야!"라고 결심하고 경로를 꼭 확인해야 한답니다!
