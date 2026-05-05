+++
weight = 270
title = "쿠키 하이재킹 (Cookie Hijacking)"
date = "2024-03-24"
[extra]
categories = ["studynote-security", "web-security"]
+++
## 0. 핵심 인사이트

> |                         |

> 📝 모범 답안

1. 사용자의 유효한 세션 쿠키를 탈취하여 공격자가 해당 사용자로 가장하여 시스템에 접근하는 **세션 하이재킹** 기법이다.
2. XSS(Cross-Site Scripting), 스니핑, 물리적 접근 등 다양한 경로로 발생하며, 일단 성공하면 아이디/패스워드 없이도 권한을 획득할 수 있다.
3. 이를 방지하기 위해 쿠키의 `HttpOnly`, `Secure`, `SameSite` 속성 설정과 세션 타임아웃 관리가 필수적이다.

### 1. 개요 및 필요성
HTTP는 본래 상태가 없는(Stateless) 프로토콜이므로, 서버는 사용자를 식별하기 위해 쿠키(Cookie)를 활용한다. 쿠키에는 대개 로그인 성공 후 부여되는 고유한 '세션 ID'가 담겨 있으며, 이 쿠키가 유출되면 공격자는 피해자의 브라우저 세션을 그대로 복제할 수 있다. 아이디와 패스워드가 아무리 복잡하더라도 최종 결과물인 쿠키가 털리면 보안 체계가 무력화된다는 점에서 매우 치명적인 위협이다.

### 2. 구성요소
쿠키 하이재킹은 주로 클라이언트 측(XSS)과 네트워크 측(Sniffing)에서 발생한다.

```text
[ Cookie Hijacking Attack Scenario ]

 ( Victim: User )          ( Attacker: Hacker )          ( Server )
        |                         |                         |
        | --- 1. Login ---------        | <--- 2. Set-Cookie ---- |                         | (Set: session_id=XYZ)
        |                         |                         |
        | --- 3. Script Attack -> |                         | (via XSS)
        |    [ document.cookie ]  |                         |
        |                         |                         |
        |         4. Cookie Stolen: session_id=XYZ          |
        |                         |                         |
        |                         | --- 5. Request with --->|
        |                         |      session_id=XYZ     |
        |                         |                         |
        |                         | <--- 6. Access Granted -| (Server is fooled)

1. XSS 활용: 악성 스크립트를 통해 `document.cookie`를 외부 서버로 전송.
2. 패킷 스니핑: 암호화되지 않은 HTTP 통신에서 쿠키 헤더를 도청.
3. 세션 고정: 공격자가 미리 만든 세션 ID를 사용자에게 강제로 심어놓음.
```

### 3. 구조 및 동작 원리

| 쿠키 보안 속성 | 기능 및 방어 효과 | 상세 설명 |
| :--- | :--- | :--- |
| **HttpOnly** | XSS 방어 (핵심) | JavaScript가 쿠키에 접근하지 못하도록 차단. |
| **Secure** | 스니핑 방어 | 오직 HTTPS 프로토콜을 통해서만 쿠키를 전송하도록 제한. |
| **SameSite** | CSRF 방어 | 외부 사이트의 요청에 쿠키가 전송되지 않도록 차단 (Strict, Lax). |
| **Path/Domain** | 유출 범위 최소화 | 특정 경로와 도메인에서만 쿠키가 유효하도록 설정. |

### 4. 비교 및 트레이드오프
기술사적 관점에서 쿠키 보안은 **심층 방어(Defense in Depth)**의 핵심이다.
1.  **쿠키 속성 하드닝**: 모든 중요 세션 쿠키에 `HttpOnly; Secure; SameSite=Strict`를 기본값으로 적용해야 한다.
2.  **세션 바인딩(Session Binding)**: 세션 ID뿐만 아니라 클라이언트의 IP 주소, User-Agent 등의 정보를 조합하여 세션 유효성을 검증함으로써, 쿠키가 유출되더라도 다른 환경에서의 접근을 차단한다.
3.  **HSTS 도입**: `Secure` 속성이 있더라도 SSL 스트리핑 공격으로 HTTPS가 해제되면 쿠키가 노출될 수 있으므로 HSTS를 병행해야 한다.

### 5. 실무 적용 및 최적화 기법
클라우드 서비스와 SaaS 사용이 폭증함에 따라 세션 쿠키는 현대 보안의 '실질적 열쇠'가 되었다. 최근에는 쿠키 탈취를 통한 MFA(다중 인증) 우회 기법이 활발해짐에 따라, 일회성 쿠키나 기기 인증(Device Trust)을 결합한 제로 트러스트(Zero Trust) 모델로의 진화가 필수적이다. 쿠키 관리는 단순한 웹 프로그래밍의 영역을 넘어 기업 보안 거버넌스의 최우선 과제이다.

### 📌 관련 개념 맵 (Knowledge Graph)
*   **상위 개념**: 세션 하이재킹 (Session Hijacking), 중간자 공격
*   **하위/파생 개념**: HttpOnly, Secure Flag, XSS, CSRF, 세션 고정 (Session Fixation)
*   **대응 기술**: HSTS, Token-based Auth (JWT), FIDO2

### 👶 어린이를 위한 3줄 비유 설명
1. 쿠키는 놀이공원에서 한 번 검사하고 받은 '자유이용권 팔찌'와 같아요.
2. 나쁜 사람이 몰래 내 팔찌를 훔쳐서 자기 팔에 차면, 나인 척하고 놀이기구를 탈 수 있게 되죠.
3. 그래서 팔찌가 절대 빠지지 않게 딱딱한 잠금장치(HttpOnly)를 채워두는 것이 중요하답니다!
