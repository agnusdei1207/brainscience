+++
weight = 2
title = "ABAC"
description = "속성 기반 접근 제어(ABAC)의 원리와 보안"
date = 2024-01-15
+++

# ABAC (Attribute-Based Access Control)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: ABAC(Attributed-Based Access Control)는 접근 제어 결정에 사용자(User) 속성, 자원(Resource) 속성, 행동(Action) 속성, 환경(Environment) 속성 등 다양한 속성을 기반으로 접근 허가를 판단하는 접근 제어 모델이다.
> 2. **가치**: 시간, 위치, 기기 유형, 보안 레벨 등 다양한 속성을 동적으로 평가하므로, 정적인 역할만으로는 표현하기 어려운 세밀한 접근 제어가 가능하다.
> 3. **융합**: ABAC은 XACML(XML 기반 ABAC 정책 언어), OAuth 2.0(Scope), Kubernetes(NetworkPolicy) 등과 결합하며,Zero Trust Architecture의 핵심 구현 메커니즘으로 활용된다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

### 개념 정의

ABAC(Attributed-Based Access Control)는 접근 제어 결정 시 Subject(사용자), Resource(자원), Action(행동), Environment(환경)의 네 가지 속성류를 평가하여 접근 허가를 판단하는 모델이다. 예를 들어 "월요일 9시-18시 사이에, 사내 네트워크에서 접속하는, 보안 레벨 '机密' 이상의 문서에 대해, '읽기' 권한이 있는 Analyst 역할의 사용자는 접근 허가"와 같은 세밀한 규칙을 만들 수 있다. RBAC이 역할을중심으로静态적인 권한을 부여한다면, ABAC은 속성을중심으로动态적인 접근 제어가 가능하다.

### 필요성

현대 시스템은 다양한 환경에서 접근되며, 단순한 역할만으로는 표현할 수 없는 복잡한 접근 정책이 필요하다. 예를 들어, 같은 "의사" 역할이라 하더라도 "응급실 당직 의사"와 "외래 담당 의사"는 접근해야 하는 환자 기록이 다르며, "야간 근무"와 "주간 근무"도 다른 접근 권한이 필요하다. ABAC은 이러한 시간, 위치, 기기, 상황 등 다양한 속성을 기반으로 세밀한 접근 제어를 가능하게 한다. 또한 규제 요건(GDPR, HIPAA 등)에서 요구하는 "필요한知道的 원칙(Need-to-Know)"을 충족하기 위해 ABAC의 동적 평가 능력이 필수적이다.

### 💡 비유

ABAC은 **호텔의스마트 카드 시스템**과 같다. 객실키는 단순히 "고객"이라는 역할만으로 작동하는 것이 아니라,チェックイン日時、チェックアウト日時、客室のfloor、客室のタイプ(일반/스위트)、付費サービス加入 여부, 現在の時刻(酒吧利用時間帯 등) 등 다양한 속성을 기반으로 객실 출입을 판단한다. 그래서 동일한 "고객" 역할이라도、付与された속성에 따라 접근 가능한区域과 시간이 달라진다.

### 등장 배경

ABAC은 NIST에서 1990년대 말~2000년대 初頭 연구가 시작되었으며, 2014년 NIST SP 800-162로 공식 가이드가发布되었다. 그 뒤로 ABAC는 기업 환경의세밀한 접근 제어, 규제 준수, 그리고Zero Trust Architecture의 구현 수단으로 널리 활용되고 있다. XACML(eXtensible Access Control Markup Language)이 ABAC 정책의표준 표현 언어로 널리 사용된다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### ABAC 속성 유형

ABAC는 네 가지 주요 속성류를 기반으로 접근을 판단한다.

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    ABAC 속성 유형                                           │
  ├─────────────────────────────────────────────────────────────────────┤
  │
  │  [1. Subject (주체) 속성]                                              │
  │  - 사용자 ID, 역할, 소속 부서, 보안 레벨, 보안 허가 등급              │
  │  예: user.role=engineer, user.department=IT, user.clearance=SECRET   │
  │
  │  [2. Resource (자원) 속성]                                           │
  │  - 자원 유형, 소유자, 생성일, 보안 레벨, 기밀 등급, 태그               │
  │  예: doc.classification=SECRET, doc.owner=HR, doc.type=report       │
  │
  │  [3. Action (행동) 속성]                                             │
  │  - 조작 유형 (읽기, 쓰기, 삭제, 실행, 관리)                            │
  │  예: action.type=READ, action.type=DELETE                            │
  │
  │  [4. Environment (환경) 속성]                                         │
  │  - 현재 시간, 날짜, 위치( IP), 기기 유형, 네트워크 유형                │
  │  예: env.time=OFF_HOURS, env.location=REMOTE, env.device=MOBILE    │
  │
  │  [ABAC 정책 예시]                                                    │
  │
  │  PERMIT user.role=PHYSICIAN                                         │
  │     AND user.department=EMERGENCY                                    │
  │     AND doc.patient.status=EMERGENCY                                │
  │     AND env.time>=0:00 AND env.time<=23:59                         │
  │     AND action.type=READ                                             │
  │  DENY OTHERWISE                                                     │
  │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** ABAC의 핵심은 다양한 속성을 Policy에 따라 조합하여 접근 판단하는 것이다. Policy는 PERMIT 또는 DENY를 반환하는 규칙의 집합이며, 각 규칙은 속성 값의 조합을 평가한다. 예를 들어, "응급실 당직 의사는 24시간 환자의 응급 기록에 대해 읽기 접근이 가능하다"는 Policy는 의사 역할, 응급실 부서, 응급 환자 상태, 시간 무관, 읽기 행동이라는 속성 조합으로 정의된다.

### ABAC 정책 엔진 동작 원리

ABAC 시스템은 Policy Administration Point(PAP), Policy Decision Point(PDP), Policy Enforcement Point(PEP), Policy Information Point(PIP)로 구성된다.

```text
  ┌─────────────────────────────────────────────────────────────────────┐
  │                    ABAC 아키텍처 구성 요소                                  │
  ├─────────────────────────────────────────────────────────────────────┤
  │
  │  [PAP - Policy Administration Point]                                │
  │  - 정책 작성 및 관리 인터페이스                                        │
  │  - 관리자가 정책 정의, 수정, 삭제                                       │
  │
  │  [PDP - Policy Decision Point]                                       │
  │  - 접근 결정 엔진                                                     │
  │  - 요청된 속성들을 평가하여 PERMIT/DENY 결정                         │
  │
  │  [PEP - Policy Enforcement Point]                                     │
  │  - 접근 Enforcement (차단/허용)                                       │
  │  - PDP의 결정을實際 자원 접근에 적용                                   │
  │
  │  [PIP - Policy Information Point]                                    │
  │  - 속성 정보 조회 인터페이스                                           │
  │  - 사용자 속성, 자원 속성, 환경 속성을 조회하여 PDP에 제공              │
  │
  │  [동작 흐름]                                                        │
  │
  │  User ──▶ PEP: "문서 읽기 요청"                                     │
  │             │                                                        │
  │             ▼                                                        │
  │          PIP: 속성 수집                                               │
  │          - user.role, user.department, user.clearance               │
  │          - doc.classification, doc.owner                              │
  │          - env.time, env.location                                    │
  │             │                                                        │
  │             ▼                                                        │
  │          PDP: 정책 평가 ──▶ "PERMIT" 또는 "DENY"                   │
  │             │                                                        │
  │             ▼                                                        │
  │          PEP: 결과 적용 (접근 허용 또는 차단)                         │
  │
  └─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** ABAC 시스템에서 PAP는 정책 관리자가 정책을 정의하고 관리하는 인터페이스이다. PDP는 접근 요청이 들어올 때마다 속성을 평가하여 PERMIT 또는 DENY를 반환하는 정책 결정 엔진이다. PEP는 자원 접근 시점에 PDP의 결정을 enforce하는 역할을 하며, DENY 결정을 내리면 접근을 차단한다. PIP는 각 속성을 조회하는 인터페이스로, LDAP, Active Directory, DBMS, 타임 서버 등 다양한 소스로부터 속성 정보를 수집하여 PDP에 제공한다.

### ABAC vs RBAC

| 비교 항목 | RBAC | ABAC |
|:---|:---|:---|
| **제어粒度** | 역할 단위 (粗糙) | 속성 단위 (세밀) |
| **정책 정의** | 역할-권한 매핑 중심 | 속성-규칙 기반 |
| **동적 평가** | 제한적 (역할 할당 시) | 매우 동적 (요청 시 마다) |
| **관리 편의성** | 높음 (역할 단위) | 낮음 (복잡한 규칙) |
| **적합 상황** | 역할 기반 권한이 명확한 경우 | 시간, 위치, 상황 기반 접근 제어 필요 시 |
| **표준** | NIST RBAC | XACML |

- **📢 섹션 요약 비유**: ABAC은 **호텔의스마트 카드 시스템**과 같다. 객실키는 단순히 "고객" 역할만으로 작동하는 것이 아니라,チェックイン日時、チェックアウト日時、客室のfloor、客室のタイプ 등 다양한 속성을 기반으로 객실 출입을 판단한다. 그래서 동일한 "고객" 역할이라도、付与された속성에 따라 접근 가능한区域과 시간이 달라진다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### ABAC와Zero Trust

Zero Trust Architecture에서 ABAC는 핵심 구현 메커니즘으로 활용된다.

| Zero Trust 원칙 | ABAC 구현 |
|:---|:---|
| **Never Trust, Always Verify** | 매 요청 시 속성 기반 동적 검증 |
| **Least Privilege Access** | 속성 기반 최소 권한 부여 |
| **Assume Breach** | 지속적인 속성 모니터링 |
| **Verify Explicitly** | 다중 속성(역할+시간+위치+기기) 동시 검증 |

### 과목 융합 관점

- **네트워크**: Kubernetes NetworkPolicy, AWS Security Group이 네트워크 레벨 ABAC를 구현한다.
- **클라우드**: AWS IAM Policy(ABAC 기반), Azure Conditional Access가 ABAC를 활용한다.
- **규제 준수**: GDPR의 "处理的最小화", HIPAA의 "need-to-know" 원칙 충족에 ABAC가 필수적이다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 —의료 records ABAC**: HIPAA 준수를 위해, "의사는 본인의 환자 기록만, 응급 상황에서는 모든 기록에 접근 가능, 단 야간에는 부서장 승인 필요"와 같은 세밀한 접근 정책을 ABAC로 구현.

2. **시나리오 — AWS IAM ABAC**: SAML federation으로 SSO 접속 시, 사용자의 attribute(department, team)를 기반으로 S3 버킷에 대한 접근을 동적으로 제어.

### 도입 체크리스트

- **기술적**: 속성 정보가 정확하고最新の 상태인가? 정책이 복잡하여 의사결정이 느려지지 않는가?
- **운영·보안적**: 정책 변경이 감사 추적 가능한가?

### 안티패턴

- **과도하게 복잡한 정책**: 속성 조합이爆発적으로 증가하여 정책 관리와 감사 가시성이 떨어진다.
- **순환 속성 의존**: 속성끼리 서로를 참조하는 순환 구조가 발생하지 않도록 설계해야 한다.
- **PEP 누락**: PDP만 있고 PEP이 없으면 접근 제어가 실제로 enforce되지 않는다.

- **📢 섹션 요약 비유**: ABAC은 **호텔의스마트 카드 시스템**과 같다. 객실키는 역할(고객)뿐 아니라,チェックイン/out日時、客室のタイプ、付費サービスなどの속성을 기반으로 작동한다. 그래서 동일한 고객이라도부여된속성에 따라 접근区域과 유효 기간이动态적으로달라진다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | RBAC만 사용 | ABAC 추가 적용 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 역할당 평균 10개 권한 | 세밀한 속성 기반 권한 | 규제 준수 향상 |
| **정성** | 시간/위치 기반 제어 불가 | 동적 세밀한 제어 | 위험 감소 |

### 미래 전망

ABAC은Zero Trust Architecture와 밀접하게 결합하여, 지속적으로 발전하고 있다. 또한 Policy as Code(예: Open Policy Agent)와의 통합으로 정책 관리의 자동화, GitOps적용이 진행되고 있다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **XACML** | ABAC 정책을XML로표현하는 표준 언어이다. |
| **Zero Trust** | 매 요청을 매번 검증하는 보안 모델로, ABAC가 구현 메커니즘으로 활용된다. |
| **RBAC** | 역할 기반 접근 제어이며, ABAC와 함께 사용하여粒度를补完한다. |
| **OAuth 2.0 Scope** | OAuth에서 ABAC를模仿하여 권한 범위를 정의한다. |
| **Kubernetes RBAC** | Kubernetes의 역할 기반 접근 제어로, ABAC와 결합된다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. ABAC은 **호텔에서 고객 등급에 따라 방을 쓰는 것이 아니라, 고객의 다양한 속성(몇월에 숙박, 몇 박, 어떤 방 타입, 부대 시설 사용 여부)을 실시간으로 확인해서 문을 여는 것**과 같아요.

2. 예를 들어, 체크인 날짜가 되었고(속성:時間), 객실 타입이 스위트이고(속성:방타입), 추가로付費服务를 이용하고 있으면(속성:서비스), 비로소 스위트 lounge(특정区域)에 출입이 허용돼요.

3. computer 세상에서도 마찬가지예요. "의사"라는 역할(기분)뿐만 아니라, 지금 응급실에值班 중이고(속성:시간), 환자가 응급 환자이고(속성:환자状態), 접근하려는 기록이 그 환자의 것(속성:소유)이면 접근이 허용되는 식으로 다양한 속성을 동시에 확인해서保安을管理하는 거예요.
