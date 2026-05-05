+++
weight = 863
title = "863. PHP Object Injection"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: PHP Object Injection은 `unserialize()` 함수가 사용자 제어 문자열을 처리할 때 PHP 매직 메서드(`__wakeup`, `__destruct`, `__toString`)가 자동으로 실행되어 임의 코드 실행·파일 조작·SQL 인젝션 등이 가능한 취약점이다.
> 2. **가치**: WordPress, Laravel, Joomla 등 인기 PHP 프레임워크와 플러그인에서 반복적으로 발견되며, 가젯 클래스(POP Chain)를 결합하면 웹셸 업로드나 관리자 권한 탈취까지 가능하다.
> 3. **판단 포인트**: 사용자 입력에 `unserialize()`를 절대 적용하지 않는 것이 근본 해결책이며, PHP 7+의 `allowed_classes` 옵션으로 역직렬화 허용 클래스를 제한해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

PHP의 `unserialize()` 함수는 `serialize()`로 생성된 문자열을 다시 PHP 객체로 복원한다. 이 과정에서 PHP는 특정 매직 메서드를 자동으로 호출한다. `__wakeup()`은 역직렬화 직후, `__destruct()`는 객체가 소멸될 때, `__toString()`은 객체가 문자열로 변환될 때 자동 실행된다.

공격자는 이 매직 메서드들을 트리거하는 직렬화 문자열을 조작해, 코드 실행·파일 삭제·DNS 조회·SQL 쿼리 실행 등을 유발하는 POP (Property-Oriented Programming) 체인을 구성한다.

```text
┌──────────────────────────────────────────────────────────────┐
│           PHP Object Injection 기본 흐름                      │
├──────────────────────────────────────────────────────────────┤
│  PHP 직렬화 형식:                                             │
│  O:4:"User":2:{s:4:"name";s:5:"admin";s:4:"role";s:4:"user";}│
│  └── O: 객체, 4: 클래스명 길이, User: 클래스명              │
│                                                              │
│  공격자가 조작한 페이로드:                                    │
│  O:4:"Evil":1:{s:4:"file";s:15:"/etc/passwd";}               │
│                                                              │
│  서버: $obj = unserialize($_COOKIE['data']);                  │
│  → Evil 객체 생성 → __destruct() 자동 호출                   │
│  → $this->file 경로 삭제 또는 읽기 실행                       │
└──────────────────────────────────────────────────────────────┘
```

WordPress 플러그인에서 자주 발견되는 이유는 쿠키나 POST 파라미터에 직렬화 데이터를 저장하고 `unserialize()`로 처리하는 패턴이 관행적으로 사용됐기 때문이다.

📢 **섹션 요약 비유**: PHP Object Injection은 마법 인형(직렬화 객체)을 조작해서, 인형이 깨어날 때(역직렬화) 조작된 행동을 하도록 만드는 공격이다.

---

## 2. 구성요소

### PHP 매직 메서드와 악용 시나리오

| 매직 메서드 | 트리거 시점 | 악용 시나리오 |
|:---|:---|:---|
| __wakeup() | 역직렬화 직후 | 데이터베이스 연결, 파일 열기 |
| __destruct() | 객체 소멸 시 | 파일 삭제, 명령 실행 |
| __toString() | 문자열 변환 시 | SQL 인젝션, 파일 읽기 |
| __call() | 미정의 메서드 호출 | 임의 메서드 디스패치 |
| __get() | 미정의 속성 접근 | 파일 시스템 접근 |

```text
┌──────────────────────────────────────────────────────────────┐
│              POP Chain (Property-Oriented Programming)       │
├──────────────────────────────────────────────────────────────┤
│  Entry: ClassA::__destruct()                                 │
│      │ $this->obj->method()                                  │
│      ▼                                                       │
│  ClassB::__call('method', args)                              │
│      │ $this->callback($args)                                │
│      ▼                                                       │
│  ClassC::__invoke()                                          │
│      │ eval($this->code)  ← 코드 실행!                        │
│      ▼                                                       │
│  또는 ClassD::__toString()                                   │
│      │ $this->db->query($this->sql)  ← SQL 인젝션!           │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: POP 체인은 인형이 깨어나면 친구 인형을 건드리고, 그 인형이 다른 인형을 건드려 마지막 인형이 창문을 깨는(코드 실행) 도미노다.

---

## 3. 구조 및 동작 원리

| 항목 | PHP Object Injection | Java Deserialization | Python pickle |
|:---|:---|:---|:---|
| 역직렬화 함수 | unserialize() | readObject() | loads() |
| 매직 메서드 | __wakeup, __destruct | readObject | __reduce__ |
| 공격 복잡도 | 중간 (POP Chain) | 높음 (가젯 체인) | 낮음 (직접 실행) |
| 방어 난이도 | 중간 | 높음 | 낮음 (사용 금지) |

PHP 7.0+에서 `unserialize($data, ['allowed_classes' => false])` 옵션으로 모든 클래스 역직렬화를 차단하거나, 특정 클래스만 허용하는 화이트리스트를 적용할 수 있다.

📢 **섹션 요약 비유**: PHP, Java, Python 역직렬화 취약점은 같은 건물의 다른 입구를 통한 침입과 같다. 입구마다 경비원(방어)이 필요하다.

---

## 4. 비교 및 트레이드오프

**취약 코드 탐지 및 방어**:

취약한 코드:
```php
$data = unserialize($_COOKIE['user_data']);
```

안전한 코드:
```php
// 옵션 1: JSON으로 대체
$data = json_decode($_COOKIE['user_data'], true);

// 옵션 2: 클래스 화이트리스트 (PHP 7+)
$data = unserialize($input, ['allowed_classes' => ['SafeClass']]);

// 옵션 3: HMAC 서명 검증 후 역직렬화
$expected_hmac = hash_hmac('sha256', $serialized, SECRET_KEY);
if (!hash_equals($expected_hmac, $_COOKIE['hmac'])) {
    die('Invalid signature');
}
$data = unserialize($serialized);
```

**자동화 탐지**: phpggc 도구로 PHP 가젯 체인 페이로드 생성 및 테스트 (승인된 범위에서)

📢 **섹션 요약 비유**: PHP 방어 코드는 마법 인형을 받을 때 "우리 공장(화이트리스트)에서 만든 인형만 받고, 서명(HMAC)이 있는 인형만 개봉"하는 규칙을 만드는 것이다.

---

## 5. 실무 적용 및 최적화 기법

PHP Object Injection 방어를 통해 RCE, 파일 시스템 접근, SQL 인젝션 체인 등 연쇄적 공격을 차단할 수 있다. 특히 WordPress·Drupal·Joomla 기반 사이트에서 플러그인의 unserialize 사용을 정기적으로 감사하는 것이 중요하다.

📢 **섹션 요약 비유**: PHP Object Injection 완전 방어는 마법 인형 제도를 완전 폐지하고, 인형 대신 그냥 메모지(JSON)를 쓰는 것이다 — 메모지는 읽기만 하고 저절로 움직이지 않는다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| POP Chain | 공격 구조 | PHP 가젯 체인 |
| phpggc | 공격/테스트 도구 | PHP 가젯 생성기 |
| allowed_classes | 방어 옵션 | unserialize 화이트리스트 |
| __destruct | 공격 진입점 | 가장 많이 악용되는 매직 메서드 |
| HMAC | 무결성 보장 | 직렬화 데이터 서명 |

### 👶 어린이를 위한 3줄 비유 설명
- PHP Object Injection은 마법 인형(직렬화 객체)에 나쁜 주문을 심어서, 인형이 깨어날 때(역직렬화) 집에 불을 지르게 하는 공격이에요.
- 인형이 깨어나면 자동으로 주문이 실행되니까 나쁜 주문이 있으면 위험해요.
- 직접 만든 인형(JSON)만 쓰거나, 허락된 인형만 받으면(화이트리스트) 안전해요!
