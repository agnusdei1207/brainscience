+++
weight = 170
title = "170. 모듈 패턴 (Module Pattern)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++
## 0. 핵심 인사이트

> **핵심**: 모듈(Module) 패턴은 클로저(Closure)를 이용해 private 스코프를 만들고, 공개 API만 외부에 노출하는 정보 은닉(Information Hiding) 구조다.
> 2. **가치**: 클래스 키워드가 없는 언어(초기 JavaScript 등)에서 캡슐화(Encapsulation)를 달성하고 전역 네임스페이스(Global Namespace) 오염을 방지한다.
> 3. **판단 포인트**: ES6 이상에서는 네이티브 모듈(`import`/`export`)을 우선 사용하되, 클로저 기반 상태 캡슐화가 명시적으로 필요한 경우 모듈 패턴의 원리를 이해하고 적용한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

### 클래스 없이 캡슐화하기

Java나 C++와 달리 초기 JavaScript는 클래스(Class) 키워드가 없었고, `var`로 선언한 변수는 함수 스코프를 가졌다. 모든 변수가 전역 객체(`window`)에 노출되는 구조에서는 라이브러리 간 변수명 충돌, 내부 구현 노출 등 심각한 문제가 발생했다.

이를 해결하기 위해 등장한 패턴이 **IIFE (Immediately Invoked Function Expression, 즉시 실행 함수 표현식)**를 활용한 모듈 패턴이다.

### IIFE와 클로저의 역할

```javascript
const counter = (function () {
    let _count = 0;  // private: 외부 접근 불가

    function _validate(n) {  // private 함수
        return n >= 0;
    }

    return {
        increment() { _count++; },
        decrement() { if (_validate(_count - 1)) _count--; },
        getCount()  { return _count; }
    };
})();

counter.increment();
counter.getCount(); // 1
// counter._count   → undefined (접근 불가)
```

IIFE가 실행되며 함수 스코프가 형성되고, 반환된 객체(public API)의 메서드들은 해당 스코프를 **클로저(Closure)**로 참조한다. 스코프 자체는 외부에서 접근할 수 없으므로 `_count`는 완전히 은닉된다.

📢 **섹션 요약 비유**: 금고(함수 스코프) 안에 돈(private 변수)을 넣고, 금고 문을 잠근 뒤 입금 슬롯과 잔액 조회 창(public API)만 밖으로 내놓는 구조다.

---

## 2. 구성요소

### 모듈 패턴 구조도

```
┌──────────────────────────────────────────────────────────────┐
│                      IIFE 실행 (모듈 경계)                    │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Private Scope (외부 접근 차단)                       │   │
│  │                                                      │   │
│  │  let _state = { ... }      ← private 상태            │   │
│  │  function _helper() { }    ← private 함수            │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                   │
│            클로저로 참조 (Closure Reference)                  │
│                          ▼                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Public API Object (반환 객체)                        │   │
│  │                                                      │   │
│  │  publicMethodA() { ... _state ... _helper() ... }    │   │
│  │  publicMethodB() { ... }                             │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                   │
└──────────────────────────┼───────────────────────────────────┘
                           │ return
                    ┌──────▼──────┐
                    │   Client    │
                    │ module.A()  │
                    └─────────────┘
```

### 모듈 패턴 확장: 공개/비공개 멤버 명확화

```javascript
const UserModule = (function () {
    // Private
    const _users = [];
    function _validate(user) {
        return user && user.name && user.email;
    }

    // Public
    return {
        add(user) {
            if (_validate(user)) _users.push(user);
        },
        count() { return _users.length; },
        getAll() { return [..._users]; }  // 방어적 복사(Defensive Copy)
    };
})();
```

📢 **섹션 요약 비유**: 식당 주방(private 공간)은 손님이 들어갈 수 없지만, 주문 창구(public API)를 통해 음식을 주문하고 받을 수 있다.

---

## 3. 구조 및 동작 원리

### 캡슐화 방식 비교

| 비교 항목 | 클래스 기반 캡슐화 | 모듈 패턴 | ES6 Module |
|:---|:---|:---|:---|
| **private 구현** | `private` 키워드 | 클로저(Closure) 스코프 | 파일 스코프 (외부 export 안 하면 비공개) |
| **인스턴스 생성** | `new` 키워드 | IIFE 결과 객체 | 싱글턴 (모듈 캐싱) |
| **다중 인스턴스** | `new`로 여러 개 가능 | IIFE 여러 번 호출 | 기본적으로 싱글턴 |
| **상속** | `extends` | 객체 합성(Composition) | 재수출(re-export) |
| **트리 쉐이킹(Tree-shaking)** | 불가 | 불가 | 가능 (번들러 지원) |
| **지원 환경** | ES5+ | ES3+ | ES6+, Node.js |
| **사용 권장** | 현대 JS/TS | 레거시 코드 유지보수 | 현대 프로젝트 기본 |

### 모듈 시스템 역사 흐름

```
전역 변수 오염 문제
        │
        ▼
   모듈 패턴 (IIFE + Closure)  ← 2000년대 초
        │
        ▼
   CommonJS (require/module.exports)  ← Node.js 2009
        │
        ▼
   AMD (Asynchronous Module Definition, 비동기 모듈 정의)  ← RequireJS 2010
        │
        ▼
   UMD (Universal Module Definition, 범용 모듈 정의)  ← AMD + CommonJS 통합
        │
        ▼
   ES6 Module (import/export)  ← 2015, 표준화
```

📢 **섹션 요약 비유**: 마을 사람들이 처음엔 길에 짐을 널어놓다가(전역 변수), 창고(모듈 패턴)를 만들고, 이후 표준 우체국(ES6 Module)이 생겨 체계적으로 관리하게 됐다.

---

## 4. 비교 및 트레이드오프

### jQuery 플러그인 구조: 모듈 패턴 활용

```javascript
// jQuery 플러그인 - 모듈 패턴으로 전역 오염 방지
(function ($) {
    const _defaults = { speed: 300, easing: 'linear' };

    $.fn.myPlugin = function (options) {
        const settings = Object.assign({}, _defaults, options);
        return this.each(function () {
            // 플러그인 로직
        });
    };
})(jQuery);
```

### Node.js CommonJS와의 관계

CommonJS의 `module.exports`는 모듈 패턴과 동일한 철학을 파일 단위로 구현한다.

```javascript
// userService.js (CommonJS)
const _db = require('./db');  // 모듈 내부에서만 참조

function _findInDb(id) { return _db.query(id); }

module.exports = {
    getUser(id) { return _findInDb(id); }
};
```

### 레거시 코드 분석 시 모듈 패턴 식별 기준

| 신호 | 의미 |
|:---|:---|
| `(function () { ... })()` 구조 | IIFE 기반 모듈 패턴 |
| `return { }` 으로 끝나는 IIFE | Revealing Module Pattern |
| `var Module = {}` 네임스페이스 객체 | 네임스페이스 패턴 (단순 버전) |
| 파일 최상단 `'use strict';` + IIFE | 엄격 모드 모듈 패턴 |

### Revealing Module Pattern (공개 모듈 패턴)

```javascript
const Calculator = (function () {
    function add(a, b) { return a + b; }
    function sub(a, b) { return a - b; }

    // 명시적으로 공개할 것만 선택
    return { add, sub };
})();
```

private 함수를 모두 일반 함수로 작성하고, 마지막에 공개할 것만 선택적으로 반환하는 방식이다. 가독성이 높아 실무에서 선호된다.

📢 **섹션 요약 비유**: 레거시 자동차(구형 JS) 엔진룸은 복잡하게 엉켜있지만, 모듈 패턴으로 만들어진 차는 "가속", "제동" 버튼만 외부에 노출된 전기차처럼 깔끔하다.

---

## 5. 실무 적용 및 최적화 기법

모듈 패턴의 기대효과:

- **전역 네임스페이스 보호**: 라이브러리 충돌 방지.
- **정보 은닉**: 내부 구현 변경이 외부 API에 영향 없음.
- **코드 구조화**: 관련 기능을 단일 단위로 묶어 응집도(Cohesion) 향상.
- **테스트 경계 명확화**: public API만 테스트 대상이 됨.

현대 프로젝트에서는 ES6 Module이 모듈 패턴을 대체하지만, **클로저 기반 상태 캡슐화**의 원리는 React의 `useState` 훅(Hook), 커스텀 훅, Redux 미들웨어(Middleware) 등에서 여전히 살아 있다. 원리를 이해하면 현대 프레임워크의 동작 방식도 더 깊이 파악할 수 있다.

📢 **섹션 요약 비유**: 모듈 패턴은 벽돌집 시대의 건축 기법이다. 현대엔 조립식 건물(ES6 Module)이 기본이지만, 벽돌 쌓는 원리(클로저, 스코프)를 이해해야 건축 전문가가 될 수 있다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | Information Hiding (정보 은닉) | 내부 구현을 외부로부터 숨기는 설계 원칙 |
| 하위 개념 | IIFE (즉시 실행 함수 표현식) | 모듈 패턴의 핵심 구현 수단 |
| 하위 개념 | Closure (클로저) | private 스코프 유지 메커니즘 |
| 연관 개념 | ES6 Module (import/export) | 언어 수준 모듈 시스템, 현대 표준 |
| 연관 개념 | CommonJS (require/module.exports) | Node.js 모듈 시스템 |
| 연관 개념 | AMD (비동기 모듈 정의) | 브라우저 비동기 모듈 로딩 |
| 연관 개념 | Encapsulation (캡슐화) | OOP 4대 특성 중 하나, 모듈 패턴 목표 |
| 연관 개념 | Revealing Module Pattern | 공개 멤버를 명시적으로 선택하는 변형 |

---

### 👶 어린이를 위한 3줄 비유 설명

- 일기장(private 변수)은 자물쇠로 잠가두고, 엄마한테는 "오늘 학교에서 있었던 일 중 말해도 되는 것"(public API)만 이야기해요.
- 일기장 안에 뭐가 있는지 직접 꺼내볼 수 없고, 내가 허락한 창구로만 물어볼 수 있어요.
- 그래서 친구가 내 일기를 몰래 볼 수도 없고, 내가 마음대로 바꿔도 친구는 아무것도 몰라도 돼요.
