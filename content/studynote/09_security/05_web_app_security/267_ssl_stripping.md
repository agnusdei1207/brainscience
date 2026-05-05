+++
weight = 267
title = "SSL 스트리핑 (SSL Stripping)"
date = "2024-03-24"
[extra]
categories = ["studynote-security", "network-security"]
+++
## 0. 핵심 인사이트

> |                         |

> 📝 모범 답안

1. 사용자의 HTTPS 요청을 강제로 **HTTP로 다운그레이드**하여 중간에서 데이터를 평문으로 탈취하는 중간자 공격(MitM) 기법이다.
2. 2009년 Moxie Marlinspike에 의해 제안되었으며, 서버의 리다이렉션(`301/302`) 과정을 가로채어 브라우저와 공격자 사이를 비암호화 구간으로 만든다.
3. 근본적인 방어를 위해 브라우저에 HTTPS 접속을 강제하는 **HSTS(HTTP Strict Transport Security)** 도입이 필수적이다.

### 1. 개요 및 필요성
SSL 스트리핑은 암호화된 통신(HTTPS)의 초기 접속 단계가 대개 비암호화된 HTTP 요청으로 시작된다는 점을 악용한다. 대부분의 사용자는 주소창에 `https://`를 직접 입력하지 않고 `naver.com`처럼 입력하며, 서버는 이를 `302 Found` 등의 응답을 통해 HTTPS로 리다이렉트한다. 공격자는 이 리다이렉트 응답을 가로채어 사용자에게는 일반 HTTP 페이지를 제공함으로써 보안 연결 수립을 차단한다.

### 2. 구성요소
공격자는 피해자와 게이트웨이 사이에서 **ARP 스푸핑** 등을 통해 통신 경로를 장악한 후 동작한다.

```text
[ SSL Stripping Attack Flow: Downgrade Attack ]

   ( User )           ( Attacker/MitM )           ( Server )
      |                   |                         |
      | --- HTTP Req ---      |   (bank.com)      | --- HTTP Req (Proxy) -> |
      |                   |                         |
      |                   | <--- HTTPS Resp (302) - |
      |                   |    (Location: https://) |
      | <--- HTTP Resp ---|                         |
      |   (Modified)      |                         |
      |                   |                         |
      | --- HTTP Data --> | --- HTTPS Data -------> |
      |   (ID/PW 평문)    |    (Encrypted)          |

1. Intercept: 서버가 보내는 HTTPS 리다이렉트 응답을 가로챔.
2. Strip: HTTPS 링크를 모두 HTTP로 변조하여 사용자에게 전달.
3. Proxy: 사용자와는 HTTP로, 서버와는 HTTPS로 통신하며 중간에서 데이터 탈취.
```

### 3. 구조 및 동작 원리

| 구분 | SSL 스트리핑 (SSL Stripping) | SSL 스니핑 (SSL Sniffing) |
| :--- | :--- | :--- |
| **핵심 기법** | HTTPS → HTTP 다운그레이드 | 가짜 인증서를 통한 암호화 해제 |
| **브라우저 경고** | 없음 (주소창이 http://로 보임) | 있음 (신뢰할 수 없는 인증서 경고) |
| **난이도** | 상대적으로 쉬움 (Moxie 도구 활용) | 높음 (인증서 경증 우회 필요) |
| **주요 방어** | HSTS (Strict Transport Security) | 인증서 핀닝 (Pinning), 올바른 CA 검증 |

### 4. 비교 및 트레이드오프
기술사적 관점에서 SSL 스트리핑은 **세션 보안의 취약성**을 극명하게 보여준다.
1.  **HSTS의 필수성**: 서버가 `Strict-Transport-Security` 헤더를 전송하면, 브라우저는 일정 기간 동안 해당 도메인에 대해 HTTP 요청 자체를 생성하지 않고 내부적으로 HTTPS로 전환(Internal Redirect)하여 공격을 원천 차단한다.
2.  **HSTS Preload List**: 첫 접속 시(Trust on First Use)의 취약점을 보완하기 위해 브라우저 엔진에 미리 HTTPS 접속 강제 도메인 리스트를 내장하는 전략이 필요하다.
3.  **사용자 교육**: 주소창의 자물쇠 아이콘 부재나 `http://` 시작 여부를 확인하는 보안 인식이 병행되어야 한다.

### 5. 실무 적용 및 최적화 기법
SSL 스트리핑은 고전적인 공격이지만, 설정이 미흡한 레거시 시스템에서는 여전히 유효한 위협이다. 현대의 보안 표준은 'Default HTTPS'를 넘어 'Enforced HTTPS'로 진화하고 있다. 서비스 설계 시 단순히 SSL/TLS를 적용하는 것에 그치지 않고, HSTS와 보안 쿠키(`Secure`, `HttpOnly`) 설정을 통해 전체 라이프사이클에 걸친 **End-to-End 암호화 강제**가 이루어져야 한다.

### 📌 관련 개념 맵 (Knowledge Graph)
*   **상위 개념**: 중간자 공격 (MitM), 세션 하이재킹
*   **하위/파생 개념**: HSTS, ARP Spoofing, 리다이렉션 취약점
*   **연관 도구**: sslstrip (Moxie), Bettercap, Ettercap

### 👶 어린이를 위한 3줄 비유 설명
1. 금고(HTTPS)를 쓰려고 했는데, 나쁜 사람이 중간에서 열쇠를 뺏고 "그냥 비밀번호 없는 상자(HTTP)에 넣어!"라고 속이는 거예요.
2. 우리는 상자에 소중한 물건을 넣었지만, 나쁜 사람이 몰래 열어볼 수 있게 된 상황이죠.
3. 이럴 땐 "나는 무조건 금고만 쓸 거야!"라고 미리 약속(HSTS)해두면 속지 않을 수 있답니다.
