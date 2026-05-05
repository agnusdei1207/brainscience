+++
weight = 860
title = "860. Deserialization 취약점 (Insecure Deserialization)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: 안전하지 않은 역직렬화 (Insecure Deserialization)는 신뢰할 수 없는 소스에서 직렬화된 데이터를 검증 없이 역직렬화할 때, 공격자가 객체 그래프를 조작해 임의 코드 실행(RCE)까지 가능한 심각한 취약점이다.
> 2. **가치**: 역직렬화 취약점은 인증 우회, 권한 상승, 원격 코드 실행, 서비스 거부까지 광범위한 공격이 가능하며, OWASP Top 10 2017 A08에서 독립 항목으로 다뤄질 만큼 중요하다.
> 3. **판단 포인트**: 사용자 입력을 역직렬화하는 것 자체를 피하는 것이 근본 해결책이며, 불가피한 경우 서명(HMAC) 검증과 역직렬화 필터(화이트리스트)가 필수다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

직렬화 (Serialization)는 객체를 바이트 스트림이나 텍스트(JSON, XML, 이진 포맷)로 변환해 저장·전송하는 과정이다. 역직렬화 (Deserialization)는 그 반대 과정으로 바이트 스트림을 다시 객체로 복원한다.

문제는 역직렬화 과정이 단순한 데이터 복원이 아니라, 객체의 생성자·매직 메서드·리플렉션 등을 실행할 수 있다는 점이다. 공격자가 역직렬화 과정에서 실행될 가젯 체인 (Gadget Chain)을 조작하면, 파일 삭제·네트워크 접속·명령 실행 등 임의 코드가 실행된다.

```text
┌──────────────────────────────────────────────────────────────┐
│          안전하지 않은 역직렬화 개념도                        │
├──────────────────────────────────────────────────────────────┤
│  직렬화 (정상 흐름):                                          │
│  [객체] ─직렬화─▶ [바이트 스트림] ─저장/전송─▶ [역직렬화]    │
│                                                              │
│  공격 흐름:                                                   │
│  [악성 객체 그래프] ─직렬화─▶ [조작된 바이트 스트림]          │
│                                ─쿠키/파라미터로 전송─▶        │
│                                     [역직렬화 시 RCE 실행]    │
│                                                              │
│  Java 예: readObject() 실행 중 Runtime.exec() 호출           │
│  Python 예: pickle.loads() 실행 중 os.system() 호출          │
└──────────────────────────────────────────────────────────────┘
```

역직렬화 취약점이 특히 위험한 이유는 공격 코드가 데이터처럼 보이기 때문이다. 방화벽이나 WAF (Web Application Firewall)가 "데이터"를 차단하기 어렵고, 서버 내부에서 실행되므로 탐지도 쉽지 않다.

📢 **섹션 요약 비유**: 역직렬화 취약점은 수상한 소포(직렬화된 데이터)를 개봉할 때(역직렬화) 안에 숨어있던 폭탄(악성 코드)이 터지는 것이다.

---

## 2. 구성요소

### 가젯 체인 (Gadget Chain) 동작 원리

| 단계 | 설명 | Java 예시 |
|:---|:---|:---|
| 1. 진입점 | 역직렬화 진입 클래스 | ObjectInputStream.readObject() |
| 2. 가젯 체인 시작 | 첫 번째 가젯 클래스 메서드 호출 | readObject() 오버라이드 |
| 3. 연쇄 호출 | 가젯들이 서로 메서드 호출 | InvokerTransformer |
| 4. 최종 실행 | 임의 명령 실행 | Runtime.exec("cmd") |

```text
┌──────────────────────────────────────────────────────────────┐
│          Java 가젯 체인 구조 (Apache Commons Collections)     │
├──────────────────────────────────────────────────────────────┤
│  ObjectInputStream.readObject()                              │
│         │                                                    │
│         ▼                                                    │
│  HashSet.readObject() ─▶ HashMap.put()                       │
│         │                                                    │
│         ▼                                                    │
│  TiedMapEntry.hashCode() ─▶ LazyMap.get()                    │
│         │                                                    │
│         ▼                                                    │
│  ChainedTransformer.transform()                              │
│         │                                                    │
│         ▼                                                    │
│  InvokerTransformer.transform() ─▶ Runtime.exec("calc.exe") │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 가젯 체인은 도미노처럼 하나가 쓰러지면 연쇄 반응으로 마지막 폭발물(RCE)이 터지도록 설계된 트랩이다.

---

## 3. 구조 및 동작 원리

| 언어/플랫폼 | 취약 함수 | 위험 수준 | 주요 도구 |
|:---|:---|:---|:---|
| Java | ObjectInputStream.readObject() | 매우 높음 | ysoserial |
| Python | pickle.loads() | 매우 높음 | - |
| PHP | unserialize() | 높음 | phpggc |
| Ruby | Marshal.load() | 높음 | - |
| .NET | BinaryFormatter | 높음 | ysoserial.net |

ysoserial은 Java 역직렬화 가젯 체인을 자동으로 생성하는 도구로, 보안 연구자와 공격자 모두 사용한다. 알려진 가젯 체인 라이브러리(Apache Commons Collections, Spring Framework 등)가 클래스패스에 있으면 취약하다.

📢 **섹션 요약 비유**: 언어마다 다른 역직렬화 취약점은 같은 설계 결함이 각기 다른 재질(언어)로 만들어진 것이다. 금속이든 나무든 같은 설계 오류가 있으면 똑같이 위험하다.

---

## 4. 비교 및 트레이드오프

**방어 전략**:
1. **근본 해결**: 사용자 입력을 역직렬화하지 않음. JSON/XML 등 단순 포맷 사용
2. **무결성 검증**: HMAC (Hash-based Message Authentication Code) 서명으로 데이터 변조 탐지
3. **역직렬화 필터**: Java 9+ ObjectInputFilter로 허용 클래스 화이트리스트 적용
4. **격리 실행**: 역직렬화를 별도 프로세스에서 샌드박스로 실행
5. **모니터링**: 역직렬화 호출 로깅 + 이상 클래스 로딩 탐지 (Java 에이전트)

Java ObjectInputFilter 예:
```java
ObjectInputFilter filter = info -> {
    if (info.serialClass() != null &&
        !ALLOWED_CLASSES.contains(info.serialClass().getName()))
        return ObjectInputFilter.Status.REJECTED;
    return ObjectInputFilter.Status.ALLOWED;
};
ObjectInputStream ois = new ObjectInputStream(inputStream);
ois.setObjectInputFilter(filter);
```

📢 **섹션 요약 비유**: 역직렬화 방어는 소포를 받기 전에 발신인 목록(화이트리스트)을 확인하고, 목록에 없는 발신인의 소포는 개봉 전에 파기하는 것이다.

---

## 5. 실무 적용 및 최적화 기법

안전하지 않은 역직렬화를 방어하면 RCE를 포함한 심각한 취약점 계층 전체를 제거할 수 있다. 특히 자바 기반 엔터프라이즈 시스템에서 레거시 직렬화 사용은 정기적으로 점검해야 하며, 가능하면 현대적 직렬화 포맷(JSON with schema validation, Protocol Buffers)으로 전환하는 것이 장기적 해결책이다.

📢 **섹션 요약 비유**: 역직렬화 완전 방어는 소포 수령 방식 자체를 바꾸는 것이다 — 박스째 받는 것이 아니라, 내용물만 확인된 것으로만 받는 안전 배송 시스템으로 전환하는 것.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| 가젯 체인 (Gadget Chain) | 공격 구조 | 역직렬화 중 연쇄 실행 |
| ysoserial | 공격 도구 | Java 가젯 체인 생성기 |
| ObjectInputFilter | 방어 도구 | Java 역직렬화 화이트리스트 |
| HMAC | 무결성 보장 | 데이터 변조 탐지 |
| RCE (Remote Code Execution) | 최악의 결과 | 임의 코드 실행 |

### 👶 어린이를 위한 3줄 비유 설명
- 역직렬화 취약점은 마법 상자(직렬화 데이터)를 열면(역직렬화) 안에서 몬스터(악성 코드)가 튀어나오는 거예요.
- 상자를 열 때 "안에 뭐가 있는지" 확인 안 하면 아무 것도 모르고 당해요.
- 허락된 물건만 들어있는 상자만 열기로 하면(화이트리스트) 몬스터가 못 나와요!
