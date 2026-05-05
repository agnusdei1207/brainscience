+++
weight = 421
title = "로컬 파일 포함 (LFI, Local File Inclusion) — 원격 코드 실행의 발판"
date = "2026-03-28"
[extra]
categories = ["studynote-security"]
+++
## 0. 핵심 인사이트

>

> 📝 모범 답안

- **파일의 비정상적 포함(Inclusion)**: 웹 애플리케이션의 `include`, `require` 같은 함수가 사용자 입력을 검증 없이 받아들여 서버 내부의 임의 파일을 스크립트로 실행하게 만드는 취약점임.
- **경로 순회와의 결합**: `../` 시퀀스를 통해 웹 루트 밖의 파일을 불러오며, 특히 로그 파일이나 환경 변수 파일에 악성 코드를 심은 뒤 실행하는 로그 포이즈닝(Log Poisoning)으로 이어짐.
- **방어의 핵심은 신뢰할 수 없는 입력 차단**: 동적 파일 포함 로직을 지양하고, 고정된 목록(Whitelist)에서만 파일을 로드하거나 웹 서버 설정을 통해 외부 입력을 제한해야 함.

### 1. 개요 및 필요성
- **배경:** 초기 PHP나 JSP 기반 웹 앱에서 헤더나 푸터와 같이 공통된 레이아웃을 동적으로 로드하기 위해 파일 경로를 파라미터로 받는 기법(`?page=home.php`)이 유행하면서 탄생함.
- **정의:** 공격자가 서버 로컬에 존재하는 파일(운영체제 설정, 로그, 업로드된 파일 등)을 애플리케이션의 실행 흐름으로 끌어들여 코드가 실행되게 하거나 기밀을 유출하는 공격임.
- **위험성:** 단순한 정보 유출을 넘어, 서버를 완전히 장악하는 원격 코드 실행(RCE)으로 발전할 가능성이 매우 높음.

### 2. 구성요소
```text
[ LFI Attack to RCE (Log Poisoning) ]

Step 1: Code Injection
- Attacker sends HTTP request with PHP code in User-Agent or Referer header.
  User-Agent: <?php system($_GET['cmd']); ?- Server logs this request into /var/log/apache2/access.log

Step 2: File Inclusion (LFI)
- Attacker requests vulnerable page:
  GET /index?page=../../../../var/log/apache2/access.log&cmd=id

Vulnerable Logic:
1. $page = $_GET['page'];
2. include($page); // Executes content of access.log as PHP code!

Result:
Server executes 'id' command and returns system info.
```
- **공격 트리거:** PHP의 `include`, `require`, `fopen`이나 JSP의 `jsp:include` 등 파일 시스템에 접근하여 내용을 처리하는 함수들이 주요 타겟임.
- **공격 진화 (Wrapper 활용):** PHP의 경우 `php://filter` (인코딩된 소스 코드 유출), `data://` (평문 코드 실행) 등 다양한 프로토콜 래퍼를 사용하여 보안 장비를 우회함.

### 3. 구조 및 동작 원리
| 비교 항목 | 로컬 파일 포함 (LFI) | 원격 파일 포함 (RFI) | 경로 순회 (Path Traversal) |
| :--- | :--- | :--- | :--- |
| **파일 위치** | 서버 로컬 시스템 내부 | 외부 공격자 서버 (URL) | 서버 로컬 시스템 내부 |
| **주요 행위** | 파일 실행 (Inclusion) | 외부 코드 실행 | 파일 읽기 (Reading) |
| **취약 설정** | PHP wrapper 활용 등 | allow_url_include=On | 입력 검증 부재 |
| **결과 영향** | RCE, 정보 유출 | 치명적 RCE | 정보 유출 |

### 4. 비교 및 트레이드오프
- **적용 사례:** 다국어 지원 페이지(`?lang=ko`), 템플릿 엔진 로딩 로직, 파일 업로드 후 미리보기 기능.
- **기술사적 판단:** LFI는 경로 순회의 '확장판'이자 RCE의 '입구'임. 근본적 해결책은 사용자 입력을 파일명으로 직접 사용하지 않는 것이며, 부득이한 경우 `basename()`과 같은 경로 필터링 함수 사용 및 `open_basedir` 설정을 통해 프로세스가 접근할 수 있는 디렉터리 범위를 엄격히 한정해야 함.

### 5. 실무 적용 및 최적화 기법
- **기대효과:** 서버 내부 자원의 비정상적 노출을 막고, 악성 스크립트 실행 경로를 원천 차단하여 인프라의 전반적인 안전성을 확보함.
- **결론:** 클라우드 네이티브 환경으로 갈수록 컨테이너 내부 파일 시스템 보안이 중요해짐. LFI 방어는 단순 웹 취약점 대응을 넘어, 컨테이너 격리와 최소 권한 원칙(PoLP)을 실현하는 필수적인 보안 요구사항임.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 파일 시스템 접근 제어 취약점, RCE (Remote Code Execution)
- **하위/파생 개념:** Log Poisoning, PHP Wrappers (php://), RFI, Null Byte Injection

### 👶 어린이를 위한 3줄 비유 설명
- "영수증 보여줘"라고 해야 할 자리에 "도둑이 몰래 숨겨놓은 독이 든 사탕 상자를 열어줘"라고 속이는 것과 같아요.
- 사탕 상자를 여는 순간(파일 포함), 도둑이 계획한 나쁜 일(악성 코드)이 벌어지게 된답니다.
- 그래서 주인님은 "내가 미리 허락한 영수증만 보여줄 거야!"라고 약속을 지켜야 안전해요.
