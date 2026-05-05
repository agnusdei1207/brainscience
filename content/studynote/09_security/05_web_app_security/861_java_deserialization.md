+++
weight = 861
title = "861. Java Deserialization 취약점"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: Java Deserialization 취약점은 `ObjectInputStream.readObject()`가 사용자 제어 데이터를 처리할 때, 클래스패스에 존재하는 가젯 체인을 통해 원격 코드 실행(RCE)이 가능한 취약점이다.
> 2. **가치**: Apache Commons Collections, Spring Framework, Groovy 같은 광범위하게 사용되는 라이브러리들이 가젯 체인을 포함하여, 대부분의 Java EE 서버가 잠재적으로 취약하다.
> 3. **판단 포인트**: Java 9+의 ObjectInputFilter로 역직렬화 허용 클래스를 화이트리스트로 제한하는 것이 가장 효과적인 방어이며, 레거시 시스템은 SerialKiller 라이브러리로 임시 방어 가능하다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

Java 역직렬화 취약점은 2015년 FoxGlove Security의 보고서 "What Do WebLogic, WebSphere, JBoss, Jenkins, OpenNMS, and Your Application Have in Common?"으로 대중에 알려졌다. 당시 Apache Commons Collections 라이브러리의 가젯 체인을 이용한 RCE가 Java EE 서버 전반에 영향을 미쳤다.

Java의 직렬화 형식은 매직 바이트 `0xACED 0x0005`로 시작한다. 이 바이트 시퀀스는 쿠키, POST 바디, HTTP 헤더 등 어디서든 나타날 수 있으며, Base64로 인코딩된 경우 `rO0AB`로 시작하는 패턴이 역직렬화 엔드포인트의 특징이다.

```text
┌──────────────────────────────────────────────────────────────┐
│             Java 직렬화 데이터 식별                           │
├──────────────────────────────────────────────────────────────┤
│  Raw 바이트:  AC ED 00 05  (매직 바이트)                      │
│  Base64:      rO0AB...     (쿠키·파라미터에서 자주 발견)       │
│                                                              │
│  취약한 엔드포인트 예:                                        │
│  - Java RMI (Remote Method Invocation) 포트 1099             │
│  - JMX (Java Management Extensions) 포트 1099, 9999          │
│  - WebLogic T3 프로토콜 포트 7001                             │
│  - Apache JServ Protocol (AJP) 포트 8009                     │
│  - AMF (Action Message Format) for Flash                     │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: Java 직렬화 매직 바이트는 "이 소포 안에 폭발물이 있을 수 있다"는 경고 스티커다. 이 스티커가 붙은 소포는 특별 처리가 필요하다.

---

## 2. 구성요소

### 주요 가젯 체인 라이브러리

| 라이브러리 | CVE 예시 | 영향 범위 |
|:---|:---|:---|
| Apache Commons Collections | CVE-2015-4852 | 광범위 (대부분 Java EE) |
| Spring Framework | CVE-2011-2894 | Spring 애플리케이션 |
| Apache Groovy | CVE-2015-3253 | Groovy 사용 앱 |
| JBoss/EAP | CVE-2015-7501 | JBoss 서버 |
| Oracle WebLogic | CVE-2019-2725 | WebLogic 서버 |

```text
┌──────────────────────────────────────────────────────────────┐
│          Apache Commons Collections 가젯 체인 흐름           │
├──────────────────────────────────────────────────────────────┤
│  readObject()                                                │
│      │                                                       │
│      ▼ HashSet.readObject()                                  │
│      │                                                       │
│      ▼ TiedMapEntry.hashCode()                               │
│      │                                                       │
│      ▼ LazyMap.get(key)                                      │
│      │                                                       │
│      ▼ ChainedTransformer.transform()                        │
│      │                                                       │
│      ▼ InvokerTransformer("exec", ...)                       │
│      │                                                       │
│      ▼ Runtime.getRuntime().exec("whoami")   ← RCE!          │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 가젯 체인은 마치 자동 도미노처럼, 첫 번째 가젯이 쓰러지면 연쇄적으로 마지막 '폭발'(RCE)까지 자동 진행된다.

---

## 3. 구조 및 동작 원리

| 방어 방법 | 적용 범위 | 효과 | 비고 |
|:---|:---|:---|:---|
| ObjectInputFilter (Java 9+) | JVM 수준 | 매우 높음 | 화이트리스트 적용 |
| SerialKiller 라이브러리 | 애플리케이션 | 높음 | 레거시 Java 8 지원 |
| NotSoSerial Java 에이전트 | JVM 에이전트 | 높음 | 런타임 패치 |
| 취약 라이브러리 업그레이드 | 클래스패스 | 중간 | 새 가젯 발견 가능 |
| 네트워크 분리 | 네트워크 | 중간 | 노출 범위 축소 |

JNDI (Java Naming and Directory Interface) 인젝션 (Log4Shell, CVE-2021-44228)도 역직렬화와 유사하게 JNDI 조회를 통해 원격 코드를 실행한다. 이는 Java 역직렬화 취약점의 변형이자 관련된 공격 패턴이다.

📢 **섹션 요약 비유**: 방어 방법들은 폭탄 처리 방식의 차이다. 폭탄 자체를 제거(취약 라이브러리 제거)가 최고지만, 폭발해도 피해를 막는 방어벽(필터)도 중요하다.

---

## 4. 비교 및 트레이드오프

**취약 여부 진단 체크리스트**:
1. `ObjectInputStream`을 직접 사용하는 코드 위치 목록 작성
2. 클래스패스에 취약한 가젯 라이브러리 버전 확인 (`mvn dependency:tree`)
3. Java RMI, JMX, AJP 포트 외부 노출 여부 점검
4. 애플리케이션 쿠키에서 `rO0AB` 패턴 확인
5. ysoserial 도구로 모의 공격 페이로드 테스트 (승인된 범위에서)

**마이그레이션 전략**:
- Java 직렬화 → Jackson JSON + 스키마 검증
- 분산 캐시: Java 직렬화 → Kryo + 화이트리스트, 또는 JSON
- Java RMI → gRPC (Protocol Buffers)

📢 **섹션 요약 비유**: Java 역직렬화 마이그레이션은 노후화된 위험한 배관(Java 직렬화)을 현대적인 안전 배관(JSON/Protocol Buffers)으로 교체하는 리모델링이다.

---

## 5. 실무 적용 및 최적화 기법

Java 역직렬화 취약점을 제거하면 RCE, 권한 상승, 서비스 거부 등 심각한 공격 벡터를 원천 차단할 수 있다. 특히 엔터프라이즈 Java 환경(WebLogic, JBoss, WebSphere)에서는 정기적인 패치와 ObjectInputFilter 적용이 필수적이다.

새로운 가젯 체인은 지속적으로 발견되므로, 단순한 취약 라이브러리 업그레이드만으로는 충분하지 않다. 근본적으로 사용자 입력 역직렬화 자체를 제거하는 아키텍처 전환이 장기 해결책이다.

📢 **섹션 요약 비유**: Java 역직렬화 방어의 완성은 택배 수령 방식을 "박스째 받아 개봉"에서 "내용물만 목록 확인 후 수령"으로 바꾸는 물류 시스템 혁신이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| ysoserial | 공격/테스트 도구 | Java 가젯 체인 생성 |
| ObjectInputFilter | 핵심 방어 | Java 9+ 역직렬화 필터 |
| Log4Shell | 연관 취약점 | JNDI 인젝션 RCE |
| SerialKiller | 방어 라이브러리 | 역직렬화 블랙리스트 |
| Apache Commons Collections | 취약 라이브러리 | 가젯 체인 포함 |

### 👶 어린이를 위한 3줄 비유 설명
- Java 역직렬화 취약점은 마법 상자의 잠금이 풀릴 때 안에 숨어있던 마법이 자동으로 실행되는 거예요.
- 나쁜 마법사가 상자 안에 "열리면 문을 열어라"는 마법을 심어뒀거든요.
- 상자를 열기 전에 "이 상자에서 어떤 마법이 나올지" 확인하면(ObjectInputFilter) 막을 수 있어요!
