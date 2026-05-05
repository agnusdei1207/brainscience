+++
weight = 867
title = "867. Host Header Injection (호스트 헤더 인젝션)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: Host Header Injection은 HTTP 요청의 `Host` 헤더를 조작해 웹 서버가 잘못된 호스트 정보를 신뢰하게 만들어 패스워드 재설정 링크 탈취, 캐시 포이즈닝, SSRF 등을 유발하는 취약점이다.
> 2. **가치**: 서버가 `Host` 헤더를 신뢰해 동적으로 URL을 생성하는 패턴(패스워드 재설정 이메일, 절대 URL 생성 등)에서 직접적인 피해로 이어진다.
> 3. **판단 포인트**: 서버에서 절대 URL을 생성할 때 `Host` 헤더 대신 설정 파일에서 도메인을 읽거나, 허용된 호스트 목록과 일치 여부를 검증해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

HTTP/1.1에서 `Host` 헤더는 가상 호스팅을 지원하기 위해 필수 헤더로 도입됐다. 서버가 여러 도메인을 호스팅할 때 `Host` 헤더로 어떤 사이트에 대한 요청인지 구분한다.

문제는 서버 애플리케이션이 `Host` 헤더 값을 신뢰하고 이메일의 링크, 절대 URL, 리다이렉트 목적지 등에 그대로 사용할 때 발생한다. 공격자가 `Host: attacker.com`으로 요청을 보내면, 서버가 패스워드 재설정 링크를 `attacker.com` 도메인으로 생성해 피해자에게 이메일로 보내는 상황이 만들어진다.

```text
┌──────────────────────────────────────────────────────────────┐
│           패스워드 재설정 링크 탈취 공격                      │
├──────────────────────────────────────────────────────────────┤
│  공격자 요청:                                                 │
│  POST /reset-password                                        │
│  Host: attacker.com                                          │
│  email: victim@example.com                                   │
│                                                              │
│  서버 동작 (취약):                                            │
│  reset_url = "http://" + request.host + "/reset?token=" + t  │
│  → "http://attacker.com/reset?token=ABCD1234"                │
│                                                              │
│  피해자에게 이메일 발송:                                      │
│  "패스워드 재설정: http://attacker.com/reset?token=ABCD1234" │
│                                                              │
│  피해자 클릭 → attacker.com에서 토큰 탈취 → 계정 탈취        │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: Host Header Injection은 편지를 받는 주소(Host 헤더)를 조작해서, 회신 편지(패스워드 재설정 이메일)가 내 집이 아닌 공격자 집으로 가게 만드는 것이다.

---

## 2. 구성요소

### Host Header Injection 공격 유형

| 공격 유형 | 조작 방법 | 영향 |
|:---|:---|:---|
| 패스워드 재설정 탈취 | Host: attacker.com | 리셋 토큰 탈취 |
| 웹 캐시 포이즈닝 | Host: evil.com | 캐시에 악성 응답 저장 |
| SSRF 우회 | Host: internal.server | 내부 서비스 접근 |
| 가상 호스트 우회 | Host: admin.internal | 관리 인터페이스 접근 |
| X-Forwarded-Host 인젝션 | X-Forwarded-Host: attacker.com | 프록시 경유 시 우회 |

```text
┌──────────────────────────────────────────────────────────────┐
│               방어 아키텍처                                   │
├──────────────────────────────────────────────────────────────┤
│  방어 1: 설정 파일에서 도메인 읽기                           │
│  BASE_URL = config.get('BASE_URL')  # "https://mysite.com"   │
│  reset_url = BASE_URL + "/reset?token=" + token              │
│  (Host 헤더 사용하지 않음)                                    │
│                                                              │
│  방어 2: Host 헤더 검증                                      │
│  ALLOWED_HOSTS = ['mysite.com', 'www.mysite.com']            │
│  if request.host not in ALLOWED_HOSTS:                       │
│      return 400 Bad Request                                  │
│                                                              │
│  방어 3: 웹 서버 레벨 차단 (Nginx)                           │
│  server {                                                    │
│    if ($host !~* ^(mysite\.com|www\.mysite\.com)$) {         │
│      return 400;                                             │
│    }                                                         │
│  }                                                           │
└──────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 방어는 회사에서 "회신 주소는 항상 우리 회사 주소를 사용하고, 고객이 알려준 주소를 사용하지 않는다"는 규정을 두는 것이다.

---

## 3. 구조 및 동작 원리

| 항목 | Host Header Injection | Open Redirect | SSRF |
|:---|:---|:---|:---|
| 조작 대상 | Host 헤더 | URL 파라미터 | URL 파라미터 |
| 주요 피해 | 패스워드 탈취, 캐시 포이즈닝 | 피싱 | 내부 서비스 접근 |
| 방어 핵심 | 허용 호스트 목록 | 허용 URL 목록 | 허용 URL 목록 |

Django 프레임워크는 `ALLOWED_HOSTS` 설정으로 Host 헤더 검증을 내장 지원한다. Rails, Spring, Laravel도 유사한 호스트 검증 메커니즘을 제공한다.

📢 **섹션 요약 비유**: Host Header Injection은 열쇠를 복사하는 것과 달리, 열쇠 공장(서버)에 "이 주소로 열쇠를 보내줘"라고 거짓 주소를 알려주는 것이다.

---

## 4. 비교 및 트레이드오프

**Django 설정 예**:
```python
# settings.py
ALLOWED_HOSTS = ['mysite.com', 'www.mysite.com']
# Host 헤더가 목록에 없으면 400 에러
```

**Spring Boot 설정**:
```yaml
server:
  forward-headers-strategy: framework  # 프록시 헤더 검증
```

**테스트 방법**:
- Burp Suite에서 Host 헤더 변경 후 응답의 URL에 조작된 호스트 포함 여부 확인
- 패스워드 재설정 요청에 `Host: burpcollaborator.net` 삽입 후 이메일 수신 확인

📢 **섹션 요약 비유**: Host Header Injection 테스트는 "이 편지를 공격자 주소로 보내줘"라고 서버에 요청해보고, 서버가 정말 그 주소로 보내는지 확인하는 것이다.

---

## 5. 실무 적용 및 최적화 기법

Host Header Injection 방어를 통해 패스워드 재설정 토큰 탈취, 웹 캐시 포이즈닝, 가상 호스트 우회 등 다양한 공격을 차단할 수 있다. 방어 구현이 단순(허용 호스트 목록)한 것에 비해 방치 시 피해가 크므로, 기본 보안 설정으로 항상 포함해야 한다.

📢 **섹션 요약 비유**: Host Header Injection 방어는 우체국에 "이 회사에서 보내는 편지는 항상 이 주소로만 보낼 수 있다"는 규정을 등록해두는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| 패스워드 재설정 | 주요 공격 대상 | 리셋 토큰 탈취 |
| 웹 캐시 포이즈닝 | 결합 공격 | 오염된 응답 캐시 저장 |
| X-Forwarded-Host | 우회 수단 | 프록시 경유 시 악용 |
| ALLOWED_HOSTS | 핵심 방어 | 허용 호스트 목록 |
| Django ALLOWED_HOSTS | 구현 예시 | 프레임워크 내장 방어 |

### 👶 어린이를 위한 3줄 비유 설명
- Host Header Injection은 편지에 "답장은 이 주소로 보내줘"라고 가짜 주소를 적는 거예요.
- 우체부(서버)가 그 주소를 믿으면 비밀 편지(패스워드 재설정 링크)가 나쁜 사람에게 가요.
- "답장 주소는 항상 회사 주소(설정 파일)"를 쓰도록 규정하면 막을 수 있어요!
