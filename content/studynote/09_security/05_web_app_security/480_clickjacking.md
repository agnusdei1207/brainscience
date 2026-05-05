+++
weight = 480
title = "480. Clickjacking (클릭재킹)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: Clickjacking(UI Redressing)은 공격자가 투명한 iframe으로 합법적 페이지를 덮어 피해자가 보이지 않는 버튼을 클릭하게 만드는 시각적 기만 공격이다.
> 2. **가치**: JavaScript 취약점 없이도 피해자의 클릭 행위를 가로채 의도치 않은 작업(계좌 이체, 권한 부여 등)을 실행시킬 수 있다.
> 3. **판단 포인트**: X-Frame-Options 또는 CSP frame-ancestors 헤더로 해당 사이트가 iframe 안에 삽입될 수 없도록 차단하는 것이 핵심 방어이다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

Clickjacking은 UI Redressing 또는 Iframe Overlay Attack으로도 불린다. 공격자는 `opacity:0`으로 투명하게 처리한 대상 사이트의 iframe을 자신의 페이지 위에 올려놓는다. 피해자는 매력적인 버튼을 클릭한다고 생각하지만 실제로는 투명 iframe의 버튼(예: 구매, 이체, 친구 추가)을 클릭하게 된다.

2008년 Adobe Flash 권한 허용 버튼을 가로채는 공격이 최초 발견 사례이며, Facebook 좋아요 버튼 클릭재킹(Likejacking)이 대규모 피해를 일으키기도 했다.

📢 **섹션 요약 비유**: 투명 유리판 위에 예쁜 그림을 그려서 유리판 아래 버튼을 누르게 유도하는 마술 트릭이다.

---

## 2. 구성요소

| 구성 요소 | 역할 | 공격자 코드 예시 |
|:---|:---|:---|
| 외부 페이지 | 클릭 유도 UI | `<div>클릭하면 경품!` |
| 투명 iframe | 실제 피해 대상 | `opacity:0; position:absolute` |
| 위치 조정 | 버튼 정렬 | `top:100px; left:200px` |

```
공격자 페이지 (피해자 화면)
┌──────────────────────────────┐
│  "여기 클릭하면 경품!"        │  ← 보이는 레이어
│                              │
│     [클릭하세요!]             │  ← 버튼처럼 보임
└──────────────────────────────┘
          │ 실제로는 위에
┌──────────────────────────────┐
│  bank.com (투명 iframe)      │  ← 안 보이는 레이어
│                              │
│     [이체 확인]               │  ← 실제 클릭 대상
└──────────────────────────────┘
```

�� **섹션 요약 비유**: 유리판(투명 iframe) 위에 달콤한 사탕 그림을 그려서 유리 아래의 버튼을 누르게 하는 것이다.

---

## 3. 구조 및 동작 원리

| 방어 헤더 | 효과 | 지원 브라우저 |
|:---|:---|:---|
| X-Frame-Options: DENY | 모든 iframe 차단 | 구형 포함 전체 |
| X-Frame-Options: SAMEORIGIN | 동일 출처만 허용 | 구형 포함 전체 |
| CSP frame-ancestors 'none' | 모든 iframe 차단 | 현대 브라우저 |
| CSP frame-ancestors 'self' | 동일 출처만 허용 | 현대 브라우저 |

CSP `frame-ancestors`가 X-Frame-Options보다 더 세밀한 제어(특정 도메인 허용)가 가능해 현대 권장 방법이다.

📢 **섹션 요약 비유**: X-Frame-Options는 구형 자물쇠, CSP frame-ancestors는 스마트 잠금 장치다.

---

## 4. 비교 및 트레이드오프

**서버 설정 예시 (Nginx)**:
```
add_header X-Frame-Options "DENY";
add_header Content-Security-Policy "frame-ancestors 'none'";
```

**Frame Busting JavaScript** (레거시 방어, CSP에 의해 우회 가능):
```js
if (top !== self) { top.location = self.location; }
```

Frame Busting은 `sandbox` 속성 iframe으로 우회 가능하므로 헤더 기반 방어가 필수이다.

📢 **섹션 요약 비유**: 유리판을 애초에 못 쓰게 하는 법(헤더)이 유리판 위 그림을 지우는 것(JS)보다 확실하다.

---

## 5. 실무 적용 및 최적화 기법

X-Frame-Options와 CSP frame-ancestors를 함께 적용하면 모든 브라우저에서 클릭재킹 공격이 차단된다. 중요한 결제·권한 페이지에는 반드시 이 헤더를 설정해야 한다.

📢 **섹션 요약 비유**: 투명 유리판 자체를 만들지 못하게 하면 클릭재킹 마술 트릭이 애초에 불가능해진다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| X-Frame-Options | 방어 | iframe 삽입 차단 헤더 |
| CSP frame-ancestors | 방어 | 세밀한 frame 삽입 제어 |
| Likejacking | 사례 | Facebook 좋아요 클릭재킹 |
| Frame Busting | 레거시 방어 | JS 기반 iframe 탈출 |

### 👶 어린이를 위한 3줄 비유 설명
클릭재킹은 유리판 위에 그림을 그려서 유리 아래 버튼을 누르게 하는 속임수예요.
피해자는 예쁜 그림을 클릭했지만 사실은 송금 버튼을 누른 거예요.
서버가 "내 페이지는 유리판 안에 넣지 마세요"(X-Frame-Options)라고 규칙을 세우면 막을 수 있어요.
