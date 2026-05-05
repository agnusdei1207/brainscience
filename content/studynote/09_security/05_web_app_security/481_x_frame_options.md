+++
weight = 481
title = "481. X-Frame-Options 헤더"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: X-Frame-Options는 브라우저에게 해당 페이지를 `<frame>`, `<iframe>`, `<object>` 태그 안에 삽입하는 것을 허용할지 제어하는 HTTP (Hypertext Transfer Protocol) 응답 헤더이다.
> 2. **가치**: Clickjacking 공격을 서버 설정만으로 간단하게 방어할 수 있는 가장 직관적인 수단이며, 구형 브라우저(IE 8+)도 지원한다.
> 3. **판단 포인트**: ALLOW-FROM 지시어는 현대 브라우저에서 지원이 중단되었으므로, 특정 도메인 허용이 필요하면 CSP frame-ancestors를 사용해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

X-Frame-Options는 2009년 Microsoft와 Mozilla가 공동으로 제안한 비표준 헤더로, RFC 7034로 표준화되었다. 세 가지 값을 지원한다.
- `DENY`: 어떠한 frame 안에도 삽입 불가
- `SAMEORIGIN`: 동일 출처(same origin) frame 안에만 허용
- `ALLOW-FROM uri`: 특정 URI만 허용(현대 브라우저 미지원)

📢 **섹션 요약 비유**: "내 초상화를 다른 집 액자(iframe)에 걸지 마세요"라고 알리는 저작권 표시이다.

---

## 2. 구성요소

| 값 | 동작 | 현대 브라우저 지원 |
|:---|:---|:---|
| DENY | 모든 frame 차단 | 전체 |
| SAMEORIGIN | 동일 오리진만 허용 | 전체 |
| ALLOW-FROM | 특정 URL만 허용 | 미지원(deprecated) |

```
[X-Frame-Options 동작]

서버 응답
  HTTP/1.1 200 OK
  X-Frame-Options: DENY
        │
        ▼
  브라우저 판단
        │
  ┌─────┴───────┐
  │ iframe 시도? │
  └─────┬───────┘
        │ YES
        ▼
  로드 차단 + 콘솔 오류
  "Refused to display ... in a frame
   because it set 'X-Frame-Options' to 'deny'"
```

📢 **섹션 요약 비유**: 집 문에 "손님은 현관으로만, 창문으로는 출입 불가"라고 붙여두는 것이다.

---

## 3. 구조 및 동작 원리

| 비교 항목 | X-Frame-Options | CSP frame-ancestors |
|:---|:---|:---|
| 표준 여부 | RFC 7034(비공식) | W3C CSP Level 2 |
| 세밀한 제어 | 제한적 | 다중 출처 허용 가능 |
| 구형 브라우저 | 지원(IE 8+) | 미지원 |
| 권장 | 호환성용 | 현대 기본 권장 |

두 헤더를 모두 설정하면 구형·현대 브라우저 모두 커버된다.

📢 **섹션 요약 비유**: 구형 자물쇠(X-Frame-Options)와 스마트 잠금(CSP)을 함께 쓰면 모든 문이 잠긴다.

---

## 4. 비교 및 트레이드오프

**설정 예시**:
```
# Nginx
add_header X-Frame-Options "SAMEORIGIN" always;

# Apache
Header always append X-Frame-Options SAMEORIGIN

# Spring Security
http.headers().frameOptions().sameOrigin();
```

어드민·결제·인증 페이지는 `DENY`, 대시보드 위젯처럼 자체 iframe 허용이 필요한 경우 `SAMEORIGIN`을 사용한다.

📢 **섹션 요약 비유**: 중요 방(결제 페이지)은 완전히 잠그고, 내부 공유 방(대시보드)은 가족(동일 오리진)만 열수 있게 하는 것이다.

---

## 5. 실무 적용 및 최적화 기법

X-Frame-Options를 적용하면 Clickjacking 공격의 가장 기본적인 기법이 차단된다. CSP frame-ancestors와 함께 설정하면 모든 브라우저 환경에서 완전한 Clickjacking 방어가 구현된다.

📢 **섹션 요약 비유**: 오래된 자물쇠(X-Frame-Options)와 최신 잠금 장치(CSP)를 함께 달면 어떤 도둑도 못 들어온다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Clickjacking | 방어 대상 | iframe 기반 UI 기만 공격 |
| CSP frame-ancestors | 대체·보완 | 현대 브라우저 권장 |
| RFC 7034 | 표준 | X-Frame-Options 명세 |
| SAMEORIGIN | 설정값 | 동일 출처 frame 허용 |

### 👶 어린이를 위한 3줄 비유 설명
X-Frame-Options는 내 사진을 다른 집 액자에 걸지 못하게 하는 저작권 딱지예요.
"DENY"는 아무도 못 쓰게, "SAMEORIGIN"은 우리 집(동일 사이트)만 쓸 수 있게 해요.
이 딱지가 없으면 나쁜 사람이 내 사진 위에 유리판을 덮어 사기를 칠 수 있어요.
