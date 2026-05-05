+++
weight = 438
title = "438. Expression Language Injection"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: EL (Expression Language) Injection (표현식 언어 인젝션)은 Java EE (Enterprise Edition) 의 JSP (JavaServer Pages) EL, Spring SpEL (Spring Expression Language), JSF (JavaServer Faces) EL 등 표현식 언어 엔진에 사용자 입력이 직접 평가될 때 임의 코드를 실행하는 취약점이다.
> 2. **가치**: EL 인젝션은 단순 데이터 조작을 넘어 서버 측 Java 코드를 직접 실행할 수 있어 원격 코드 실행(RCE, Remote Code Execution)으로 이어질 수 있다.
> 3. **판단 포인트**: 사용자 입력을 EL 표현식 컨텍스트에 직접 포함하지 않고, 입력값을 EL 처리 전에 이스케이프하거나, SpEL의 경우 SimpleEvaluationContext를 사용해 평가 컨텍스트를 제한해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

Java 웹 프레임워크(Spring, JSF, Thymeleaf 등)는 표현식 언어를 통해 서버 사이드 데이터를 HTML 템플릿에 동적으로 바인딩한다. 그러나 사용자 입력이 표현식으로 평가되는 맥락에 포함되면, 공격자가 임의 Java 코드를 서버에서 실행할 수 있다.

**Spring SpEL 인젝션 예시**:
```java
// 취약한 코드: 사용자 입력을 SpEL 표현식으로 평가
ExpressionParser parser = new SpelExpressionParser();
Expression expr = parser.parseExpression(userInput);
Object result = expr.getValue();

// 공격 입력: T(java.lang.Runtime).getRuntime().exec("id")
// → 서버에서 OS 명령 실행!
```

JSP EL의 경우 `${userInput}` 형태로 출력할 때, 입력이 다시 EL로 평가되는 이중 평가(Double Evaluation) 취약점이 대표적이다.

📢 **섹션 요약 비유**: EL 인젝션은 "계산기에 '2+3'을 입력하면 5가 나오듯, 공격자가 '서버에서 이 명령을 실행해'라는 표현식을 입력하면 그대로 실행되는 것이다.

---

## 2. 구성요소

EL 인젝션 공격 경로:

| 프레임워크 | 취약 패턴 | 공격 예시 |
|:---|:---|:---|
| Spring SpEL | `parser.parseExpression(input)` | `T(java.lang.Runtime).getRuntime().exec("id")` |
| JSP EL | `${param.input}` 이중 평가 | `${applicationScope}` (설정 탈취) |
| Spring Boot | `@Value("${input}")` (동적) | `#{T(java.lang.System).exit(0)}` |

```
┌──────────────────────────────────────────────────────────┐
│           SpEL 인젝션 → RCE 공격 흐름                    │
├──────────────────────────────────────────────────────────┤
│  공격자 입력: T(java.lang.Runtime).getRuntime()           │
│                .exec(new String[]{"sh","-c","id"})        │
│       │                                                   │
│       ▼                                                   │
│  SpEL 파서가 Java 코드로 평가                             │
│       │                                                   │
│       ▼                                                   │
│  서버에서 "id" 명령 실행 → uid=www-data 등 반환          │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: SpEL 인젝션은 수식 계산기에 `execute(os_command)`라는 함수를 입력해 서버 명령을 실행하는 것이다.

---

## 3. 구조 및 동작 원리

| 구분 | EL Injection | SSTI (Server-Side Template Injection) |
|:---|:---|:---|
| 대상 | Java EL 엔진 | Jinja2, Freemarker, Thymeleaf 등 |
| 위험도 | RCE 가능 | RCE 가능 |
| 발생 환경 | Java 웹 프레임워크 | Python/Java/Ruby 템플릿 |
| 방어 | SimpleEvaluationContext | 템플릿 샌드박스, 이스케이프 |

📢 **섹션 요약 비유**: EL Injection과 SSTI는 같은 공격의 다른 방언이다. 둘 다 "표현식 엔진이 사용자 입력을 코드로 실행한다"는 공통점이 있다.

---

## 4. 비교 및 트레이드오프

**Spring SpEL 안전 사용**:
1. **SimpleEvaluationContext 사용**: `StandardEvaluationContext` 대신 제한된 컨텍스트 사용
2. **사용자 입력을 SpEL 표현식으로 사용 금지**: 고정 표현식 + 파라미터 바인딩으로 대체
3. **JSP EL 이중 평가 방지**: `JSTL c:out`으로 출력, `isELIgnored` 설정 검토
4. **Spring MVC 설정**: 사용자 입력이 뷰 이름으로 사용되지 않도록 엄격한 뷰 이름 검증

📢 **섹션 요약 비유**: SimpleEvaluationContext는 계산기에서 수학 연산만 허용하고, OS 명령 실행 함수는 아예 없애버리는 것이다.

---

## 5. 실무 적용 및 최적화 기법

EL 인젝션은 적절한 컨텍스트 제한과 사용자 입력을 표현식으로 처리하지 않는 아키텍처 원칙으로 방어할 수 있다. 특히 Spring 기반 애플리케이션에서 SpEL이 필요한 경우 SimpleEvaluationContext를 기본값으로 사용하는 팀 코딩 표준이 중요하다.

기술사 관점에서 EL 인젝션은 "표현식 언어 엔진의 강력함이 취약점이 된다"는 교훈을 담고 있다. 강력한 기능일수록 입력 처리에 더욱 엄격한 원칙이 필요하다.

📢 **섹션 요약 비유**: 강력한 계산기를 사용자에게 직접 쥐어주는 것은 위험하다. 버튼을 제한해 수식만 입력할 수 있게 하는 것이 안전한 설계다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| SpEL | 공격 대상 | Spring 표현식 언어 |
| SimpleEvaluationContext | 방어 방법 | 제한된 SpEL 평가 컨텍스트 |
| SSTI | 유사 공격 | 서버 측 템플릿 인젝션 |
| RCE | 최종 피해 | 원격 코드 실행 |
| Double Evaluation | 취약 패턴 | 이중 EL 평가 |

### 👶 어린이를 위한 3줄 비유 설명
- EL 인젝션은 수식 계산기에 "2+3" 대신 "이 명령어를 실행해"라고 입력해 컴퓨터가 그대로 따르는 공격이야.
- Java 웹 프로그램에서 특히 많이 쓰이는 표현식 언어(SpEL)가 공격 대상이 돼.
- 그래서 사용자가 넣은 값은 절대 표현식으로 평가하면 안 되고, 제한된 기능만 쓸 수 있게 해야 해!
