+++
weight = 533
title = "533. SAML Assertion (SAML 어서션)"
date = "2026-04-22"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: SAML Assertion은 IdP가 발행하여 SP에게 전달하는 사용자의 인증(누구인가), 속성(어떤 특징인가), 인가(무엇을 할 수 있는가) 정보를 담은 **전자서명된 XML 문서**다.
> 2. **가치**: 신뢰할 수 있는 기관이 서명한 '디지털 증명서' 역할을 수행하여, 비밀번호 전달 없이도 도메인 간 신원 보증을 가능하게 한다.
> 3. **판단 포인트**: Assertion 내의 `Subject`, `Conditions`, `AuthnStatement` 등의 구문을 통해 토큰의 유효 기간과 사용 범위를 엄격히 제안하여 보안성을 확보한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

SAML Assertion은 SAML 프로토콜의 '핵심 화물 (Payload)'이다. 인증 서버(IdP)가 사용자의 신원을 확인한 후, 그 결과 보고서를 XML 형식으로 작성하여 서비스 제공자(SP)에게 전달하는 실체다.

이 문서가 중요한 이유는 "누가, 언제, 어디서, 어떻게 인증되었는가"에 대한 모든 정보가 여기에 들어있기 때문이다. 만약 Assertion이 없다면 SAML은 그저 빈 껍데기 프로토콜에 불과하며, 이 문서에 전자서명이 빠진다면 누구나 위조할 수 있는 가짜 신분증이 된다. 따라서 Assertion은 연합 인증 시스템에서 '신뢰의 증거' 그 자체다.

- **📢 섹션 요약 비유**: SAML Assertion은 시험 감독관이 확인하고 도장을 찍어준 '응시표'와 같다. 이 종이 한 장에 학생의 사진(식별자), 수험 번호(속성), 시험장 입장 가능 여부(인가)가 다 들어있다.

---

## 2. 구성요소

SAML Assertion은 크게 세 가지 유형의 문장(Statement)으로 구성된다.

| 문장 유형 | 설명 | 예시 데이터 |
|:---|:---|:---|
| **Authentication** | 사용자가 인증된 시간과 수단 증명 | 2026-04-22 10:00, Password 인증 |
| **Attribute** | 사용자에 대한 부가 정보 전달 | 이메일, 부서, 직급, 사번 |
| **Authorization** | 특정 자원에 대한 접근 허용 여부 | 리소스 A에 대한 'Read' 권한 허용 |

### SAML Assertion XML 메시지 구조 (추상화)

```xml
<saml:Assertion ID="..." IssueInstant="..." Version="2.0">
  <!-- 1. Issuer: 누가 발행했는가 -->
  <saml:Issuer>https://idp.example.com</saml:Issuer>
  
  <!-- 2. Signature: 위조 방지를 위한 전자서명 -->
  <ds:Signature> ... [Digital Signature Data] ... </ds:Signature>
  
  <!-- 3. Subject: 누구에 대한 증명인가 -->
  <saml:Subject>
    <saml:NameID Format="...:emailAddress">user@example.com</saml:NameID>
  </saml:Subject>
  
  <!-- 4. Conditions: 언제, 어디서만 유효한가 (재사용 방지) -->
  <saml:Conditions NotBefore="..." NotOnOrAfter="...">
    <saml:AudienceRestriction>
      <saml:Audience>https://sp.example.com</saml:Audience>
    </saml:AudienceRestriction>
  </saml:Conditions>
  
  <!-- 5. AuthnStatement: 인증 사실 기록 -->
  <saml:AuthnStatement AuthnInstant="...">
    <saml:AuthnContext> ... [Password/MFA] ... </saml:AuthnContext>
  </saml:AuthnStatement>
</saml:Assertion>
```

핵심 원리는 **'비대칭키 기반의 무결성 보장'**이다. IdP는 자신의 개인키로 Assertion을 서명하고, SP는 IdP의 공개키로 서명을 검증한다. 이를 통해 SP는 전달받은 데이터가 중간에 변조되지 않았음을 확신할 수 있다.

- **📢 섹션 요약 비유**: Assertion은 위조 방지 홀로그램이 박힌 고급 백화점 상품권과 같다. 발행처(Issuer)가 확실하고 금액(속성)이 적혀 있으며, 유효기간(Conditions)이 지나면 쓸 수 없다.

---

## 3. 구조 및 동작 원리

SAML Assertion은 현대적인 토큰인 **JWT (JSON Web Token)**와 기능적으로 유사하지만 구조와 처리 방식에서 차이가 있다.

| 항목 | SAML Assertion | JWT (JSON Web Token) |
|:---|:---|:---|
| 포맷 | XML (Extensible Markup Language) | JSON (JavaScript Object Notation) |
| 서명 방식 | XMLDSig (강력하지만 복잡함) | JWS (간결하고 가벼움) |
| 크기 | 큼 (Verbose한 XML 특성) | 작음 (네트워크 효율적) |
| 표준 기구 | OASIS | IETF |
| 주요 연결 | 기업용 AD 연동, 보안 감사 | 모바일 API, 마이크로서비스 (MSA) |

이 Assertion은 사용자가 로그인한 상태를 유지하는 **세션(Session)** 정보로 변환되어 서비스에 활용된다.

- **📢 섹션 요약 비유**: SAML Assertion이 두꺼운 종이로 된 권위 있는 임명장이라면, JWT는 지갑에 쏙 들어가는 얇은 모바일 사원증이다.

---

## 4. 비교 및 트레이드오프

기술사적 관점에서 Assertion의 보안 핵심은 **'보안 속성(Security Attributes)'**의 엄격한 관리다. 특히 `AudienceRestriction`이 없으면 한 서비스용 Assertion으로 다른 서비스에 로그인하는 '토큰 재사용 공격'이 가능해진다.

### 체크리스트
1. **NameID 정책**: 사용자를 특정할 수 있는 고유하고 변경되지 않는 값(Persistent ID)을 사용하고 있는가?
2. **Audience 검증**: Assertion이 해당 SP만을 위해 발행된 것인지 확인하는 로직이 있는가?
3. **유효 기간 (Skew Time)**: 서버 간 시차를 고려하되 유효 기간을 5분 이내로 짧게 설정했는가?
4. **암호화 필요성**: Assertion이 브라우저를 거쳐 전달될 때 민감한 속성값(급여, 주민번호 등)이 노출되지 않도록 암호화했는가?

### 안티패턴
- `Conditions` 항목을 생략하여 한 번 발행된 토큰이 영원히 유효하게 만드는 경우
- 전자서명을 Assertion 전체가 아닌 일부에만 적용하여 'Signature Wrapping' 공격을 허용하는 경우

- **📢 섹션 요약 비유**: Assertion 실무는 수표 발행과 같다. 금액(속성)만 적는 게 아니라, 누구에게 주는 것인지(Audience)와 유효 일자(Conditions)를 꼼꼼히 적어야 사고가 안 난다.

---

## 5. 실무 적용 및 최적화 기법

SAML Assertion은 '정보의 파편화'를 해결한다. 각 서비스마다 사용자 정보를 따로 저장할 필요 없이, 인증 시점에 IdP로부터 최신 정보를 받아오기 때문에 데이터 동기화 문제를 해결하고 보안 일관성을 유지할 수 있다.

결론적으로 Assertion은 연합 신원의 '메신저'다. 복잡한 XML 구조 때문에 무겁다는 비판도 있지만, 엔터프라이즈 환경이 요구하는 엄격한 무결성과 상세한 인증 증적 정보를 담기에는 여전히 가장 신뢰할 수 있는 수단이다.

- **📢 섹션 요약 비유**: Assertion은 전문 감정사가 써준 '진품 증명서'와 같다. 이 종이가 있는 한, 물건(사용자)의 가치는 어디서든 인정받는다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| XMLDSig | Assertion의 무결성을 보장하는 XML 전자서명 표준 |
| NameID | Assertion 내부에서 사용자를 식별하는 핵심 필드 |
| AudienceRestriction | Assertion이 사용될 수 있는 대상 앱을 제한하는 보안 필터 |
| EncryptedAssertion | Assertion 내용을 암호화하여 기밀성을 확보하는 기술 |

### 👶 어린이를 위한 3줄 비유 설명

1. SAML Assertion은 산타 할아버지가 써주신 "이 어린이는 착한 어린이가 맞아요"라는 편지에요.
2. 편지에는 어린이 이름과 선물을 받아도 된다는 내용이 적혀 있고, 할아버지 도장이 쾅 찍혀 있어요.
3. 이 편지만 있으면 장난감 나라(서비스) 문지기 아저씨가 기쁘게 문을 열어준답니다.
