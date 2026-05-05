+++
weight = 439
title = "439. Template Injection (SSTI)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: SSTI (Server-Side Template Injection)는 사용자 입력이 서버 측 템플릿 엔진(Jinja2, Freemarker, Twig, Pebble 등)에 의해 직접 평가될 때, 템플릿 구문을 이용해 임의 코드를 실행하는 취약점이다.
> 2. **가치**: `{{7*7}}`이 출력에서 `49`로 나타나면 SSTI가 존재한다는 신호이며, 이는 SSRF (Server-Side Request Forgery), RCE (Remote Code Execution), 파일 시스템 접근으로 확장될 수 있다.
> 3. **판단 포인트**: 사용자 입력을 템플릿 문자열로 렌더링하지 않고 데이터로만 전달하는 것이 근본 해결책이며, 템플릿 엔진의 샌드박스 모드 활성화가 보조 방어다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

웹 프레임워크는 HTML 템플릿에 서버 사이드 데이터를 바인딩하기 위해 템플릿 엔진을 사용한다. 그런데 사용자 입력 자체가 템플릿으로 렌더링되면, 공격자가 템플릿 구문(`{{...}}`, `${...}`, `#{}` 등)을 삽입해 서버에서 코드를 실행할 수 있다.

**Python Jinja2 SSTI 예시**:
```python
# 취약한 코드: 사용자 입력을 직접 렌더링
from flask import Flask, render_template_string, request
app = Flask(__name__)

@app.route("/")
def index():
    name = request.args.get("name", "")
    return render_template_string(f"<h1>Hello {name}</h1>")

# 공격 입력: {{7*7}} → Hello 49 (SSTI 확인)
# 고급 공격: {{config.items()}} → 설정 정보 유출
# RCE: {{''.__class__.mro()[1].__subclasses__()[...].popen("id").read()}}
```

SSTI 탐지 페이로드(엔진 식별용):
- `{{7*7}}` → 49 : Jinja2, Twig
- `${7*7}` → 49 : Freemarker, Thymeleaf
- `#{7*7}` → 49 : Ruby ERB
- `<%= 7*7 %>` → 49 : Ruby ERB

📢 **섹션 요약 비유**: SSTI는 마치 Word에서 {사용자이름}을 치환하는 기능을 악용해, "{사용자이름}이 아닌 {os.execute('명령')}"을 삽입하는 것이다.

---

## 2. 구성요소

SSTI 공격 단계와 페이로드:

| 단계 | 목표 | Jinja2 페이로드 예시 |
|:---|:---|:---|
| 1. 탐지 | SSTI 존재 여부 확인 | `{{7*7}}` → 49 |
| 2. 엔진 식별 | 템플릿 엔진 파악 | `{{7*'7'}}` → 7777777 (Jinja2 특성) |
| 3. 정보 수집 | 객체·설정 탐색 | `{{config.items()}}` |
| 4. RCE | 코드 실행 | `{{''.__class__...popen("id")}}` |

```
┌──────────────────────────────────────────────────────────┐
│           SSTI 탐지에서 RCE까지                          │
├──────────────────────────────────────────────────────────┤
│  입력: {{7*7}}                                           │
│  출력: 49 → SSTI 확인!                                  │
│                                                          │
│  입력: {{config.SECRET_KEY}}                             │
│  출력: 'my-secret-key' → 설정 정보 유출                 │
│                                                          │
│  입력: {{....__subclasses__()...popen("id")}}            │
│  출력: uid=1000 → RCE 성공!                             │
└──────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: SSTI 탐지는 "계산기에 2+2를 넣어서 4가 나오면 작동한다"고 확인하는 것이다. 그 다음 훨씬 위험한 계산(명령 실행)을 넣는다.

---

## 3. 구조 및 동작 원리

| 구분 | SSTI | EL Injection |
|:---|:---|:---|
| 대상 | 템플릿 엔진 (Jinja2, Freemarker) | Java EL (SpEL, JSP EL) |
| 언어 | Python, Java, Ruby, PHP | Java |
| 구문 | `{{...}}`, `${...}` | `${...}`, `#{...}` |
| 최종 피해 | RCE, 정보 유출 | RCE |

📢 **섹션 요약 비유**: SSTI와 EL Injection은 같은 원리의 공격이다. "엔진이 입력을 코드로 실행한다"는 점이 공통점이다.

---

## 4. 비교 및 트레이드오프

**핵심 방어 전략**:
1. **사용자 입력을 템플릿 문자열로 사용 금지**: `render_template_string(input)` 패턴 완전 제거
2. **데이터 바인딩만 허용**: `render_template("template.html", name=user_input)` 방식
3. **Jinja2 샌드박스**: `SandboxedEnvironment` 사용 — 위험한 객체 접근 차단
4. **SAST 탐지**: `render_template_string`, `Template(input)` 패턴 탐지 룰 설정
5. **최소 권한**: 웹 서버 프로세스 권한 최소화

```python
# 취약한 패턴
return render_template_string(f"Hello {name}")  # 금지

# 안전한 패턴
return render_template("hello.html", name=name)  # 권장
```

📢 **섹션 요약 비유**: 안전한 템플릿 사용은 사용자에게 빈칸을 채우는 권한만 주고, 편집 권한은 주지 않는 것이다.

---

## 5. 실무 적용 및 최적화 기법

사용자 입력을 데이터 컨텍스트에서만 처리하고 절대 템플릿 문자열로 사용하지 않는 원칙을 팀 전체가 준수하면 SSTI를 완전히 방어할 수 있다. SAST 도구로 위험 패턴을 빌드 시점에 탐지하면 실수를 사전에 차단할 수 있다.

기술사 관점에서 SSTI는 오픈소스 웹 프레임워크를 사용하는 현대 웹 개발에서 가장 과소평가된 고위험 취약점 중 하나다. 특히 Flask, Django, Spring Boot 개발자가 반드시 숙지해야 할 취약점이다.

📢 **섹션 요약 비유**: SSTI 방어는 요리사에게 레시피(템플릿)를 주되, 손님이 재료(입력)를 직접 레시피에 써넣지 못하게 하는 것이다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Jinja2 | 공격 대상 | Python 템플릿 엔진 |
| SandboxedEnvironment | 방어 도구 | Jinja2 안전 실행 환경 |
| render_template_string | 취약 패턴 | 입력을 직접 템플릿으로 렌더링 |
| EL Injection | 유사 공격 | Java 표현식 언어 인젝션 |
| RCE | 최종 피해 | 원격 코드 실행 |

### 👶 어린이를 위한 3줄 비유 설명
- SSTI는 "안녕, {이름}!"이라는 편지 양식에, 이름 자리에 "명령어"를 넣어 서버가 그 명령어를 실행하게 만드는 방법이야.
- {{7*7}}을 입력해서 "49"가 보이면 그 서버는 SSTI에 취약한 거야.
- 그래서 사용자 입력은 무조건 "채울 내용"으로만 쓰고, 절대 양식 자체를 수정하게 두면 안 돼!
