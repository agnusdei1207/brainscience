+++
weight = 268
title = "HSTS (HTTP Strict Transport Security)"
date = "2024-03-24"
[extra]
categories = ["studynote-security", "web-security"]
+++
## 0. 핵심 인사이트

>| (SSL/TLS Handshake)

> 📝 모범 답안

1. 브라우저에게 해당 웹사이트는 **반드시 HTTPS로만** 접속해야 함을 강제하는 보안 메커니즘이다.
2. `301/302` 리다이렉트 과정을 거치지 않고 브라우저가 직접 HTTPS 요청을 생성하도록 하여, **SSL 스트리핑**과 같은 다운그레이드 공격을 원천 차단한다.
3. RFC 6797 표준이며, 브라우저가 첫 접속 시에 받는 `Strict-Transport-Security` 헤더를 통해 동작한다.

### 1. 개요 및 필요성
일반적인 보안 설정(HTTPS 전환 리다이렉션)은 사용자가 처음 HTTP로 접속할 때 공격자가 중간에서 가로챌 수 있는 '찰나의 취약점'을 가지고 있다. HSTS(HTTP Strict Transport Security)는 이러한 초기 접속 시의 위험(MitM)을 제거하기 위해 고안되었다. 서버가 응답 헤더를 통해 HTTPS 강제 규약을 선언하면, 브라우저는 그 이후 설정된 유효 기간 동안 HTTP 통신을 스스로 거부한다.

### 2. 구성요소
HSTS는 브라우저 내부의 'HSTS 데이터베이스'와 HTTP 응답 헤더 간의 상호작용으로 구현된다.

```text
[ HSTS Protocol Mechanism ]

( Client/Browser )             ( Server )
       |                          |
       | --- 1. Initial HTTPS ---       | <--- 2. HSTS Header ---- | (Strict-Transport-Security: max-age=31536000)
       |                          |
       | (Cache Site in HSTS List)|
       |                          |
       | --- 3. Try http:// ----->| (User types 'http://site.com')
       |    [ Internal Redirect ] |
       | --- 4. Auto HTTPS ------>| (Browser sends HTTPS directly)

* max-age: 규약 유지 시간 (초)
* includeSubDomains: 모든 서브도메인에 적용
* preload: 브라우저 사전 등록 리스트 포함 요청
```

**[HSTS Preload]**: 첫 접속 시(Trust on First Use)의 취약점(최초 1회 헤더 받기 전까지 무방비)을 막기 위해 브라우저 엔진에 강제 도메인 리스트를 하드코딩하는 방식이다.

### 3. 구조 및 동작 원리

| 구분 | 일반 리다이렉트 (301/302) | HSTS (Strict Transport Security) |
| :--- | :--- | :--- |
| **제어 주체** | 서버 (Server-side) | 클라이언트/브라우저 (Client-side) |
| **공격 방어** | SSL 스트리핑에 취약 | SSL 스트리핑 원천 방어 |
| **성능 효율** | RTT 발생 (HTTP -> 리다이렉트 -> HTTPS) | RTT 감소 (즉시 HTTPS 요청) |
| **유연성** | 높음 (조건부 전환 가능) | 낮음 (잘못 설정 시 사이트 접속 불가) |

### 4. 비교 및 트레이드오프
기술사적 관점에서 HSTS는 **강제 보안(Enforced Security)**의 전형이다.
1.  **점진적 적용**: `max-age`를 처음에는 짧게(예: 300초) 설정하여 호환성 문제가 없는지 확인한 후, 점차 늘려가는 전략이 권장된다.
2.  **보안 인증서 검증 강화**: HSTS가 적용된 도메인은 인증서 오류가 발생할 경우 사용자에게 '위험을 무시하고 계속하기' 옵션을 제공하지 않아 보안 신뢰성을 극대화한다.
3.  **컴플라이언스**: 금융권 및 공공기관의 웹 서비스 보안 가이드라인에서 HSTS 설정은 필수 항목으로 자리 잡고 있다.

### 5. 실무 적용 및 최적화 기법
HSTS는 보안뿐만 아니라 비암호화 통신 시도 자체를 없애 성능 최적화에도 기여한다. 향후 6G 및 초연결 사회에서 모든 웹 트래픽의 암호화가 기본값(HTTPS Only)이 됨에 따라, HSTS는 개별 설정의 영역을 넘어 인터넷 통신의 **기본 인프라스트럭처**로 완전히 내재화될 것이다.

### 📌 관련 개념 맵 (Knowledge Graph)
*   **상위 개념**: HTTPS, 암호화 통신 강제
*   **하위/파생 개념**: HSTS Preload, HPKP (Deprecated), CSP
*   **방어 대상**: SSL Stripping, Downgrade Attack, Cookie Hijacking

### 👶 어린이를 위한 3줄 비유 설명
1. "엄마, 저 나갈 때 꼭 마스크(HTTPS) 쓰고 나갈게요!"라고 약속하는 거예요.
2. 현관문 앞에서 마스크를 안 쓰면 아예 문이 안 열리게 브라우저가 막아주는 거죠.
3. 나쁜 사람이 밖에서 "마스크 안 써도 돼~"라고 꼬셔도, 이미 약속했기 때문에 안전하게 나갈 수 있답니다!
