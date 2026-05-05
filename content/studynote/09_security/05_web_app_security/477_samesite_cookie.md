+++
weight = 477
title = "SameSite 쿠키 (SameSite Cookie)"
date = "2025-05-14"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> |      Site B       |

> 📝 모범 답안

1. SameSite 쿠키는 브라우저가 교차 사이트 요청(Cross-Site Request) 시 쿠키를 전송할지 여부를 결정하는 보안 속성이다.
2. CSRF(Cross-Site Request Forgery) 공격을 방어하는 가장 현대적이고 강력한 브라우저 레벨의 방어 수단이다.
3. Chrome 80 버전부터 'Lax'가 기본값이 되어, 명시적으로 설정하지 않아도 기본적인 보안이 강화되었다.

---

### 1. 개요 및 필요성
- **정의**: HTTP 응답 헤더 `Set-Cookie`에 추가되는 속성으로, 제3자 사이트에서 발생한 요청 시 쿠키 전송 범위를 제한한다.
- **등장 배경**: 전통적인 쿠키 메커니즘은 사이트의 출처(Origin)와 관계없이 무조건 쿠키를 함께 전송하는 특성 때문에 CSRF 공격에 취약했다. 이를 해결하기 위해 브라우저가 스스로 쿠키를 필터링하도록 설계되었다.

---

### 2. 구성요소
- **전송 메커니즘**: 사용자가 Site A에서 Site B로 요청을 보낼 때, 브라우저는 Site B의 쿠키가 SameSite 속성을 가지고 있는지 확인한다.

```text
[ Browser SameSite Cookie Decision ]
+-------------------+       (1) Cross-Site Request      +-------------------+
|      Site A       | --------------------------------| (Attacker's Site) |                                   |  (Target Server)  |
+-------------------+                                   +-------------------+
          |                                                       ^
          | [ Browser Policy Engine ]                             |
          v                                                       |
+-------------------------------------------------------+         |
| SameSite Attribute Check:                             |         |
| 1. Strict: No cookie sent.                            |         |
| 2. Lax   : Only sent for Top-level Navigation (GET).  | --------+
| 3. None  : Sent always (Requires Secure attribute).   |
+-------------------------------------------------------+
```

- **핵심 속성 값**:
    - **Strict**: 동일한 사이트(First-party) 요청에서만 쿠키를 전송한다. 가장 안전하지만 사용자 편의성(로그인 유지 상태로 링크 클릭 등)이 저하된다.
    - **Lax**: 안전한 HTTP 메소드(GET)를 사용한 최상위 탐색(Top-level Navigation) 시에만 제3자 사이트 요청에 쿠키를 포함한다. 보안과 편의성의 균형점이다.
    - **None**: 모든 요청에 쿠키를 포함한다. 반드시 `Secure` 속성(HTTPS)이 동반되어야 한다.

---

### 3. 구조 및 동작 원리

| 구분 | Strict | Lax (Default) | None |
| :--- | :--- | :--- | :--- |
| **쿠키 전송 시점** | 동일 사이트 내부만 | 동일 사이트 + 외부 링크(GET) | 모든 요청 (제3자 포함) |
| **CSRF 방어 효과** | 강력함 | 매우 높음 (POST 차단) | 없음 |
| **사용자 경험** | 외부 링크 클릭 시 재로그인 필요 | 로그인 유지 상태로 외부 유입 가능 | 광고/트래킹 등에 사용 |
| **보안 요구사항** | - | - | Secure 속성 필수 |
| **주요 용도** | 금융, 결제 세션 | 대부분의 일반 웹 서비스 | 타 사이트 임베딩 (iframe) |

---

### 4. 비교 및 트레이드오프
- **기술사적 판단**: SameSite 속성은 'Defense in Depth' 관점에서 1차 방어선이다. 브라우저 파편화(구형 브라우저 미지원)를 고려하여 CSRF Token과 병행하여 사용하는 것이 표준이다.
- **실무 적용 전략**:
    - **Chrome 정책 대응**: `SameSite=None` 설정 시 반드시 `Secure` 속성을 추가하지 않으면 쿠키가 거부되므로 HTTPS 환경 구축이 필수적이다.
    - **서드파티 쿠키 차단 대응**: 광고 및 분석 도구는 `None; Secure`를 사용하되, 사용자 개인정보 보호 강화 추세(Privacy Sandbox 등)에 따라 대체 기술을 고려해야 한다.

---

### 5. 실무 적용 및 최적화 기법
- **기대효과**: 서버 측의 복잡한 로직 없이 브라우저 단에서 CSRF 및 정보 유출(XS-Leaks) 위험을 획기적으로 낮춘다.
- **결론**: SameSite는 현대 웹 보안의 'Default Secure' 철학을 반영하는 핵심 기술이며, 웹 개발 시 필수적으로 고려해야 할 표준 명세이다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: 웹 보안 아키텍처, 쿠키 관리 (Cookie Management)
- **직접 위협**: CSRF (Cross-Site Request Forgery), XS-Leaks
- **동위 기술**: CSRF Token, Double Submit Cookie, HSTS

---

### 👶 어린이를 위한 3줄 비유 설명
1. "우리 집 초대를 받은 사람만 우리 집 간식을 먹을 수 있게 하는 규칙"이에요.
2. 밖에서 모르는 사람이 "이 집 간식 좀 갖다줘!"라고 시켜도 브라우저가 거절하는 거예요.
3. 모르는 사람의 심부름은 안 들어주고, 믿을 수 있는 사람만 도와주는 착한 경비원 아저씨와 같답니다!
