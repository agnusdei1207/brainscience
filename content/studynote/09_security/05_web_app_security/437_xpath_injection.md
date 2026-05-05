+++
weight = 437
title = "437. XPath Injection"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: XPath Injection (XPath 인젝션)은 XML (eXtensible Markup Language) 데이터를 쿼리하는 XPath 표현식에 사용자 입력이 직접 포함될 때, 공격자가 쿼리 논리를 변경해 인증을 우회하거나 XML 문서의 전체 내용을 추출하는 취약점이다.
> 2. **가치**: XPath 인젝션은 SQL 인젝션과 유사하지만 XML 데이터를 대상으로 하며, 권한 분리나 데이터 필터링 없이 전체 XML 트리에 접근할 수 있다는 특성이 있다.
> 3. **판단 포인트**: 파라미터화된 XPath (XPath Variables/Parameterized XPath)를 지원하는 언어에서는 반드시 사용하고, 그렇지 않으면 입력 이스케이프와 화이트리스트 검증을 적용해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

XML 데이터 저장소와 XSLT (eXtensible Stylesheet Language Transformations) 처리, SOA (Service-Oriented Architecture) 환경에서 XPath를 사용한 데이터 검색이 광범위하게 이루어진다. 이때 XPath 쿼리에 사용자 입력을 직접 포함하면 인젝션 취약점이 생긴다.

**취약 코드 예시 (Java)**:
```java
String xpath = "//users/user[name/text()='" + username + "' AND "
             + "password/text()='" + password + "']";
// 공격 입력: username = admin' or '1'='1
// 결과 XPath: //users/user[name/text()='admin' or '1'='1' AND ...]
// → password 조건 무시, admin 계정 인증 우회
```

XPath에는 SQL의 `--` 같은 주석이 없지만, `or '1'='1'`로 조건을 무력화할 수 있다.

📢 **섹션 요약 비유**: XPath 인젝션은 XML 파일로 만든 전화번호부에서 특정 사람을 찾을 때, 검색 조건에 "아니면 모든 사람"을 덧붙여 전체 목록을 가져오는 것이다.

---

## 2. 구성요소

XPath 인젝션 공격 패턴과 효과:

| 공격 유형 | 입력 예시 | 효과 |
|:---|:---|:---|
| 인증 우회 | `admin' or '1'='1` | 비밀번호 조건 무력화 |
| Blind 탐색 | `'] and count(/) > 0 and ('a'='a` | XML 구조 탐색 |
| 데이터 추출 | `admin' or name()='root` | 루트 요소 접근 |

```
┌──────────────────────────────────────────────────────────┐
│           XPath 인젝션 공격 흐름                         │
├──────────────────────────────────────────────────────────┤
│  정상 XPath: //user[name='admin' and pw='secret']        │
│                                                          │
│  공격 입력 (name): admin' or '1'='1                      │
│  변조 XPath: //user[name='admin' or '1'='1' and pw='x'] │
│                                                          │
│  결과: name='admin' 조건 OR '1'='1'(항상 참) → 인증 우회 │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: XPath 인젝션도 SQL 인젝션과 동일하게 조건에 "또는 항상 참인 조건"을 덧붙여 필터를 무력화한다.

---

## 3. 구조 및 동작 원리

| 구분 | SQL 인젝션 | XPath 인젝션 |
|:---|:---|:---|
| 대상 | 관계형 DB | XML 데이터 |
| 주석 | `--`, `#` | 없음 (다른 우회 기법 사용) |
| 전체 데이터 접근 | information_schema 활용 | 루트(`/`) 노드에서 전체 접근 |
| 권한 구분 | DB 권한 체계 | XPath는 권한 분리 없음 |

📢 **섹션 요약 비유**: XPath는 SQL처럼 권한 테이블이 없다. 한 번 접근하면 XML 문서 전체를 볼 수 있는 마스터키가 된다.

---

## 4. 비교 및 트레이드오프

**대응 전략**:
1. **파라미터화 XPath**: Java Saxon 라이브러리의 XPathVariable, .NET의 XPathExpression 파라미터 사용
2. **입력 이스케이프**: 아포스트로피(`'`), 따옴표(`"`), `<`, `>`, `&` 이스케이프
3. **화이트리스트 검증**: 사용자 입력은 영숫자만 허용 (`[a-zA-Z0-9]+`)
4. **XML 스키마 검증**: XSD (XML Schema Definition)로 입력 XML 구조 검증
5. **최소 노출**: XML 파일에 민감 데이터(비밀번호 해시) 저장 자체를 최소화

📢 **섹션 요약 비유**: 파라미터화 XPath는 SQL의 Prepared Statement와 같다. 데이터와 쿼리 구조를 분리해 구조 변경을 원천 차단한다.

---

## 5. 실무 적용 및 최적화 기법

파라미터화 XPath와 입력 화이트리스트를 적용하면 XPath 인젝션을 방어할 수 있다. XML 기반 설정 파일이나 데이터 저장소를 사용하는 레거시 시스템에서 특히 주의가 필요하며, 현대 시스템에서는 JSON 기반 REST API와 적절한 DB 사용으로 XPath 노출 자체를 줄이는 것이 최선이다.

📢 **섹션 요약 비유**: XPath 인젝션을 막는 것은 SQL 인젝션과 같은 원리다. 사용자가 제공한 문자열이 쿼리 구조의 일부가 되지 않도록 해야 한다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| XPath | 쿼리 언어 | XML 데이터 탐색 언어 |
| XML | 데이터 형식 | XPath의 대상 |
| SQL Injection | 유사 공격 | 동일 원리, 다른 인터프리터 |
| XPathVariable | 방어 방법 | 파라미터화 XPath |
| XSD | 검증 도구 | XML 스키마 검증 |

### 👶 어린이를 위한 3줄 비유 설명
- XPath 인젝션은 XML이라는 파일에서 정보를 찾을 때, "이 사람 찾아줘"라는 요청에 "아니면 모든 사람 보여줘"를 몰래 추가하는 방법이야.
- SQL 인젝션이랑 원리가 똑같아. 검색 조건을 속이는 거야.
- 그래서 검색어를 코드와 분리하는 파라미터화 방법을 항상 써야 해!
