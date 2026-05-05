+++
weight = 864
title = "864. Prototype Pollution (JavaScript Prototype Pollution)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: Prototype Pollution은 JavaScript의 프로토타입 체인 메커니즘을 악용해 `Object.prototype`을 오염시킴으로써, 애플리케이션 전체 객체에 악성 속성을 주입하는 취약점이다.
> 2. **가치**: 서버 측(Node.js)에서는 Prototype Pollution이 RCE로 이어질 수 있고, 클라이언트 측에서는 XSS (Cross-Site Scripting) 방어 우회로 활용된다.
> 3. **판단 포인트**: `__proto__`, `constructor`, `prototype` 키를 사용자 입력에서 필터링하거나, `Object.create(null)`로 프로토타입 없는 객체를 생성하는 것이 핵심 방어다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

JavaScript에서 모든 객체는 `prototype`을 통해 상위 객체의 속성을 상속받는다. 이 메커니즘 덕분에 `{}.toString()`처럼 모든 객체에서 공통 메서드를 사용할 수 있다.

Prototype Pollution은 이 메커니즘을 역이용한다. 공격자가 `obj.__proto__.adminRole = true`처럼 `__proto__`를 통해 `Object.prototype`에 속성을 추가하면, 이후 생성된 모든 객체가 `adminRole = true`를 가지게 된다. 이는 인증 우회, 권한 상승, 더 나아가 템플릿 엔진이나 eval을 사용하는 코드에서 RCE로 이어진다.

```text
┌──────────────────────────────────────────────────────────────┐
│           Prototype Pollution 개념도                          │
├──────────────────────────────────────────────────────────────┤
│  정상:                                                        │
│  user = {}                                                   │
│  user.__proto__ === Object.prototype  (공통 조상)             │
│                                                              │
│  오염 공격:                                                   │
│  payload = {"__proto__": {"isAdmin": true}}                  │
│  merge(target, payload)  ← 재귀 병합 함수가 취약한 경우      │
│                                                              │
│  결과:                                                        │
│  Object.prototype.isAdmin === true                           │
│  let victim = {}                                             │
│  victim.isAdmin === true  ← 새로 만든 모든 객체가 오염됨     │
└──────────────────────────────────────────────────────────────┘
```

2019년 lodash의 `_.merge()`, `_.set()` 함수에서 Prototype Pollution이 발견됐고(CVE-2019-10744), 이는 수백만 개의 Node.js 프로젝트에 영향을 미쳤다.

📢 **섹션 요약 비유**: Prototype Pollution은 마을 공용 우물(Object.prototype)에 독을 타는 것이다. 이후 우물을 쓰는 모든 사람(객체)이 오염된 물을 마신다.

---

## 2. 구성요소

### 취약한 코드 패턴

| 취약 패턴 | 코드 예시 | 위험 |
|:---|:---|:---|
| 재귀 merge | lodash _.merge() | Object.prototype 오염 |
| 경로 설정 | lodash _.set(obj, "a.__proto__.x", v) | 오염 가능 |
| JSON 파싱 후 병합 | Object.assign()으로 사용자 JSON 병합 | 제한적 위험 |
| 깊은 클론 | deepClone(userInput) | 재귀 처리 시 위험 |

```text
┌──────────────────────────────────────────────────────────────┐
│              Node.js RCE 경로 (템플릿 엔진)                   │
├──────────────────────────────────────────────────────────────┤
│  1. Object.prototype.outputFunctionName = "x;process.mainModule│
│     .require('child_process').execSync('id')//";             │
│                                                              │
│  2. EJS (Embedded JavaScript) 템플릿 렌더링 시:              │
│     template options에서 outputFunctionName 참조             │
│     → eval(오염된 속성 값) 실행 → RCE!                       │
│                                                              │
│  영향받는 템플릿 엔진: EJS, Handlebars, Pug (구버전)         │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: Node.js RCE는 우물에 탄 독이 요리사의 냄비(템플릿 엔진)를 통해 모든 음식(코드 실행)에 스며드는 것이다.

---

## 3. 구조 및 동작 원리

| 공격 컨텍스트 | 영향 | 방어 |
|:---|:---|:---|
| 클라이언트 측 | XSS 방어 우회, UI 조작 | 입력 필터링 |
| 서버 측 (Node.js) | 인증 우회, RCE | Object.create(null) |
| 패키지 의존성 | 광범위한 영향 | 라이브러리 업데이트 |

Python의 경우에도 `__class__`, `__base__`, `__subclasses__` 를 통한 유사한 공격(Python SSTI에서 MRO 탐색)이 존재한다.

📢 **섹션 요약 비유**: 클라이언트와 서버 측 Prototype Pollution은 같은 독이 집 안 수돗물(클라이언트)과 마을 공용 식당(서버) 모두에 퍼지는 것이다.

---

## 4. 비교 및 트레이드오프

**방어 코드 패턴**:
```javascript
// 방어 1: 위험한 키 필터링
function safeMerge(target, source) {
    const dangerous = ['__proto__', 'constructor', 'prototype'];
    for (const key of Object.keys(source)) {
        if (dangerous.includes(key)) continue;  // 필터링
        if (typeof source[key] === 'object') {
            safeMerge(target[key] ??= {}, source[key]);
        } else {
            target[key] = source[key];
        }
    }
}

// 방어 2: 프로토타입 없는 객체 생성
const safe = Object.create(null);  // __proto__ 없음

// 방어 3: Object.freeze()로 Object.prototype 고정
Object.freeze(Object.prototype);  // 오염 시도 시 에러 또는 무시
```

📢 **섹션 요약 비유**: Object.freeze()는 공용 우물 위에 투명한 덮개를 씌우는 것이다. 누가 독을 넣으려 해도 덮개 때문에 들어가지 않는다.

---

## 5. 실무 적용 및 최적화 기법

Prototype Pollution 방어를 통해 인증 우회, 권한 상승, Node.js RCE, XSS 방어 우회 등 광범위한 공격 체인을 차단할 수 있다. lodash 4.17.21+, jQuery 3.4+, 최신 Node.js 라이브러리들은 이미 패치됐으므로, 의존성 최신화가 가장 빠른 완화 방법이다.

📢 **섹션 요약 비유**: Prototype Pollution 방어 완성은 공용 우물(Object.prototype)을 잠그고, 각 집마다 개별 정수기(Object.create(null))를 설치하는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| __proto__ | 공격 진입점 | 프로토타입 체인 접근 |
| lodash _.merge() | 취약 함수 | CVE-2019-10744 |
| Object.freeze() | 방어 기술 | 프로토타입 동결 |
| EJS (Embedded JavaScript) | RCE 경로 | 오염된 속성 eval 실행 |
| Object.create(null) | 방어 기술 | 프로토타입 없는 객체 |

### 👶 어린이를 위한 3줄 비유 설명
- Prototype Pollution은 마을 공용 식수대(Object.prototype)에 색소를 타는 것이에요.
- 이 식수대에서 물을 받는 모든 집(객체)의 물이 오염돼요.
- 식수대에 자물쇠(Object.freeze)를 달거나, 집마다 개별 정수기(Object.create(null))를 쓰면 안전해요!
