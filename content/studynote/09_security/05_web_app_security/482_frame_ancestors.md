+++
weight = 482
title = "482. frame-ancestors (CSP frame-ancestors 지시어)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: CSP (Content Security Policy) `frame-ancestors` 지시어는 X-Frame-Options의 현대적 대체제로, 페이지를 frame·iframe·object 안에 삽입할 수 있는 허용 출처를 정밀하게 제어한다.
> 2. **가치**: 다수의 신뢰 도메인(다른 서비스, 파트너사)을 화이트리스트로 설정할 수 있어 X-Frame-Options의 단일 ALLOW-FROM 한계를 극복한다.
> 3. **판단 포인트**: `frame-ancestors 'none'`은 DENY와 동일하며, CSP와 X-Frame-Options가 충돌 시 현대 브라우저는 CSP를 우선 적용한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

CSP Level 2에서 도입된 `frame-ancestors` 지시어는 브라우저가 해당 응답을 frame 안에 로드하기 전에 부모 frame의 출처를 검증하도록 강제한다. X-Frame-Options와 달리 다수의 출처를 공백으로 구분해 나열할 수 있다.

`frame-ancestors`는 Clickjacking 방어에 특화된 지시어로, `default-src`의 fallback이 적용되지 않아 명시적으로 선언해야 한다.

📢 **섹션 요약 비유**: 특정 건물(허용 도메인)에서 온 사람만 내 전시관(페이지)에 frame 형태로 전시할 수 있게 허용 목록을 만드는 것이다.

---

## 2. 구성요소

| 설정값 | 의미 | X-Frame-Options 대응 |
|:---|:---|:---|
| `'none'` | 모든 frame 차단 | DENY |
| `'self'` | 동일 출처만 허용 | SAMEORIGIN |
| `https://trusted.com` | 특정 도메인 허용 | ALLOW-FROM (deprecated) |
| `https://a.com https://b.com` | 다중 도메인 허용 | 불가능 |

```
[frame-ancestors 설정 예시]

Content-Security-Policy: frame-ancestors 'self' https://dashboard.corp.com

          브라우저 체크
               │
    ┌──────────┴──────────┐
    │ 부모 frame 출처?     │
    └──────────┬──────────┘
        ┌──────┴───────────┐
        ▼                   ▼
  self / corp.com          기타 출처
      → 허용                → 차단
```

📢 **섹션 요약 비유**: 전시관 입구에 "우리 건물(self)과 파트너 건물(trusted.com)에만 출품 허용" 안내문을 붙이는 것이다.

---

## 3. 구조 및 동작 원리

| 항목 | X-Frame-Options | CSP frame-ancestors |
|:---|:---|:---|
| 다중 출처 허용 | 불가 | 가능 |
| 브라우저 우선순위 | 낮음 | 높음 |
| 구형 브라우저 | 지원 | 미지원 |
| 메타 태그 사용 | 불가 | 불가(헤더만) |

두 헤더를 모두 설정하는 것이 최선이며, `frame-ancestors`가 없는 경우 X-Frame-Options로 폴백(fallback)된다.

📢 **섹션 요약 비유**: CSP는 최신 스마트 도어락, X-Frame-Options는 구형 열쇠—둘 다 달아야 모든 문이 안전하다.

---

## 4. 비교 및 트레이드오프

**설정 예시**:
```
# 완전 차단
Content-Security-Policy: frame-ancestors 'none';

# 동일 출처 + 파트너 허용
Content-Security-Policy: frame-ancestors 'self' https://partner.example.com;
```

임베디드 위젯(분석 대시보드, 지도 등)이 필요한 서비스는 `frame-ancestors 'self' https://app.corp.com`으로 파트너 도메인만 허용하고 나머지는 차단한다.

📢 **섹션 요약 비유**: 허가증(화이트리스트)을 가진 파트너만 전시관 액자(iframe)에 넣을 수 있게 한다.

---

## 5. 실무 적용 및 최적화 기법

`frame-ancestors`를 통해 Clickjacking 방어와 정상 임베딩 허용을 동시에 달성할 수 있다. X-Frame-Options와 병행 설정 시 모든 브라우저 환경에서 완전한 Clickjacking 방어가 가능하다.

📢 **섹션 요약 비유**: 최신 스마트 도어락과 구형 자물쇠를 모두 달면 어떤 침입자도 막을 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| X-Frame-Options | 레거시 대응 | 구형 브라우저 Clickjacking 방어 |
| CSP Level 2 | 표준 | frame-ancestors 도입 버전 |
| Clickjacking | 방어 대상 | iframe 기반 UI 기만 |
| DENY | 설정값 | none과 동일 효과 |

### 👶 어린이를 위한 3줄 비유 설명
frame-ancestors는 내 전시물(페이지)을 어떤 건물(도메인)의 액자(iframe)에 걸 수 있는지 목록을 만드는 규칙이에요.
목록에 없는 건물에서 전시하려 하면 경보(차단)가 울려요.
옛날 자물쇠(X-Frame-Options)도 함께 달면 구식 건물에서도 안전해요.
