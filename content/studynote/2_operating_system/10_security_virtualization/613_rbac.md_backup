+++
title = "613. RBAC (Role-Based Access Control, 역할 기반 접근 제어)"
weight = 613
+++

# 613. RBAC (Role-Based Access Control, 역할 기반 접근 제어)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: RBAC는 사용자를 직접 권한에 매핑하는 대신, **역할(Role)**을 중개로 사용하여 역할에 권한을 부여하고 사용자에게 역할을 할당하는 3단계 접근 제어 모델이다.
> 2. **가치**: 사용자 수나 권한 수가 수백~수천 개로 늘어나도, 역할만 관리하면 되므로 관리 오버헤드가 O(n²)에서 O(n)로 줄어든다. 기업 환경, 클라우드 IAM(AWS/Azure/GCP)의 표준이다.
> 3. **융합**: Active Directory, LDAP, Kubernetes RBAC, AWS IAM 등 현대 시스템에서 널리 사용되며, SoD(Separation of Duties), 최소 권한 원칙, 권한 리뷰를 자동화할 수 있다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의

**RBAC(Role-Based Access Control)**는 **사용자(User)가 자신의 직무나 책임을 나타내는 역할(Role)**을 부여받고, 각 역할에 권한(Permission)이 연결되어, 사용자가 역할을 통해 간접적으로 권한을 획득하는 접근 제어 모델이다. 예를 들어, "개발자" 역할에는 "소스 코드 읽기/쓰기", "빌드 서버 접속" 권한이 연결되고, 사용자 "김철수"는 "개발자" 역할을 할당받아 이러한 권한을 갖는다. RBAC는 기업 환경에서 직무 분리(SoD: Separation of Duties)와 권한 관리의 효율성을 높인다.

### 💡 비유: 직함별 출입증

RBAC는 **회사의 직함별 출입증 시스템**과 같다. "사원", "대리", "과장", "부장" 직함마다 접근할 수 있는 방과 할 수 있는 일이 다르다. 예를 들어, "과장"은 "일반 사무실"과 "자신의 팀 회의실"에 들어갈 수 있고, "팀원의 연차 승인" 권한이 있다. 새로운 과장이 입사하면 "과장" 직함만 부여하면 모든 권한이 자동으로 부여된다. 반면 ACL 방식은 각 방마다 "누가 입장 가능한지" 개별적으로 등록해야 하므로 관리가 번거롭다. RBAC는 **직함(역할)**만 관리하면 되어, 사용자 수가 수천 명이 되어도 관리가 용이하다.

### 등장 배경

1. **1970s: 접근 제어 복잡도 문제**: DAC(Discretionary Access Control)는 사용자-권한 직접 매핑이므로, 사용자나 권한이 늘어나면 관리가 O(n²)으로 복잡해진다. 대규모 시스템에서는 관리가 불가능에 가까웠다.
2. **1992: Ferraiolo & Kuhn 표준 제안**: NIST의 David Ferraiolo와 Richard Kuhn이 RBAC 모델을 정형화하여, **ANSI INCITS 359-2004** 표준으로 제정되었다.
3. **1990s-2000s: 기업용 디렉터리 서비스**: Microsoft Active Directory(2000), Novell eDirectory, OpenLDAP 등이 RBAC를 구현하여, 기업의 사용자/그룹/권한 관리를 중앙화했다.
4. **2010s-현재: 클라우드 IAM**: AWS IAM, Azure RBAC, Google Cloud IAM이 RBAC를 클라우드 리소스 제어에 확장하였다. Kubernetes RBAC(2016)은 클러스터 리소스에 역할 기반 접근 제어를 제공한다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                  RBAC의 발전 역사                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  【1970s: 초기 접근 제어의 한계】                                           │
│  ──────────────────────────────                                         │
│  • DAC(Discretionary AC): 사용자-권한 직접 매핑                             │
│  • 사용자 n, 권한 m → 매핑 테이블 크기 O(n × m)                              │
│  • 대규모 시스템에서는 관리 불가능                                            │
│                                                                         │
│  【1992: Ferraiolo & Kuhn RBAC 모델】                                      │
│  ──────────────────────────────────                                      │
│  • User → Role → Permission 3단계 모델                                     │
│  • 역할을 중개로 사용자/권한 간 다대다(N:N) 관계 해결                             │
│  • SoD(Separation of Duties), 계층적 역할 지원                             │
│                                                                         │
│  【1996: RBAC 표준화】                                                    │
│  ────────────────────────                                               │
│  • ANSI/NCITS 359-1996, later INCITS 359-2004                            │
│  • NIST SP 800-162: RBAC 참조 모델                                         │
│  • Core RBAC, Hierarchical RBAC, Constrained RBAC 정의                      │
│                                                                         │
│  【1999: Windows 2000 Active Directory】                                   │
│  ────────────────────────────────────                                    │
│  • 그룹(Group)을 역할로 사용                                             │
│  • Organizational Unit(OU)로 계층적 구조                                  │
│  • Group Policy로 역할별 설정 배포                                         │
│                                                                         │
│  【2000s-현재: 클라우드 IAM과 컨테이너】                                     │
│  ──────────────────────────────────                                      │
│  • AWS IAM(2010): User/Group/Role/Policy                                 │
│  • Azure RBAC: Role Assignments, Scope(Subscription/Resource Group)         │
│  • GCP IAM: Primitive Roles, Custom Roles                                │
│  • Kubernetes RBAC: ServiceAccount, Role, RoleBinding                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소

| 요소명 | 정의 | 예시 | 비유 |
|:---|:---|:---|:---|
| **User(사용자)** | 시스템에 접근하는 주체 | kim, lee, admin | 직원 |
| **Role(역할)** | 직무/책임을 나타내는 추상적 개념 | Developer, Manager, Auditor | 직함 |
| **Permission(권한)** | 리소스에 대해 수행 가능한 연산 | `file.read`, `vm.stop` | 할 수 있는 일 |
| **Session(세션)** | 사용자가 활성화한 역할 집합 | kim이 Developer+Auditor 역할 활성화 | 근무 중 직함 |
| **UA(User-Role) 할당** | 사용자에게 역할 부여 | `kim → Developer` | 직책 발령 |
| **PA(Role-Permission) 할당** | 역할에 권한 부여 | `Developer → {code.read, build.run}` | 직무 내용 |
| **RH(Role Hierarchy)** | 역할 간 상하 관계 | `Manager > Developer` | 직급 체계 |

### RBAC 구조

기본적인 RBAC의 구조와 ACL/DAC과의 대비를 보자.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│            RBAC vs DAC/ACL 구조 비교                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  【DAC(Discretionary Access Control): 사용자-권한 직접 매핑】                │
│  ────────────────────────────────────────────────────────                 │
│                                                                         │
│    User1 ─┐                                                             │
│    User2 ─┼──→ Permissions: {file1.read, file2.write, vm.stop}           │
│    User3 ─┘                                                             │
│                                                                         │
│  문제: User가 1000명, Permission이 1000개이면 매핑 테이블 크기 100만           │
│                                                                         │
│  【RBAC(Role-Based Access Control): 3단계 매핑】                        │
│  ────────────────────────────────────────────────────                     │
│                                                                         │
│    User1 ─┐                                                             │
│    User2 ─┼─→ Roles: {Developer, Tester}                                │
│    User3 ─┘                                                             │
│              │                                                          │
│              ▼                                                          │
│    Developer ─┐                                                         │
│    Tester ────┼──→ Permissions: {code.read, code.write, build.run}       │
│    Auditor ──┘                                                         │
│                                                                         │
│  장점: User가 1000명, Role이 10개, Permission이 1000개이어도                  │
│         매핑 테이블 크기 = (1000×10) + (10×1000) ≈ 11,000 (99% 감소)        │
│                                                                         │
│  【RBAC 구성 요소 관계】                                                  │
│  ──────────────────────────                                              │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  Users(U)          │  Roles(R)          │  Permissions(P)         │ │
│  │  ──────            │  ─────            │  ──────────            │ │
│  │  {kim, lee, park}  │  {Dev, Ops, Mgr}  │  {code.rw, vm.stop}    │ │
│  │       │            │       │           │                         │ │
│  │       └─────────────┴───────┘           │                         │ │
│  │                      │                        │                     │
│  │          UA(User Assignment)            PA(Permission Assignment)│ │
│  │              kim → {Dev, Ops}              Dev → {code.rw}        │ │
│  │              lee → {Ops}                   Ops → {vm.stop}        │ │
│  │                                               Mgr → {code.rw, vm.stop}│ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  【RBAC의 3단계 접근 제어 흐름】                                            │
│  ───────────────────────────────────                                     │
│                                                                         │
│  User kim → (1) UA 확인 → kim은 {Developer, Manager} 역할 보유             │
│           → (2) PA 확인 → Developer는 {code.read, build.run} 권한          │
│           → (3) Permission 확인 → code.read 요청 허용                      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** DAC는 사용자와 권한을 직접 연결하므로, 사용자 n명과 권한 m개에 대해 최대 n×m 개의 매핑을 관리해야 한다. RBAC는 역할(Role)을 중개하여, 사용자-역할(UA: User Assignment)과 역할-권한(PA: Permission Assignment)으로 분리한다. 역할 수는 사용자나 권한 수보다 훨씬 적게(보통 10~50개) 설계할 수 있으므로, 전체 관리 복잡도가 O(|U|×|R| + |R|×|P|)로 줄어든다. 예를 들어, 사용자 1000명, 권한 1000개, 역할 20개라면 DAC는 100만 개 매핑을, RBAC는 약 4만 개 매핑((1000×20) + (20×1000))만 관리하면 된다. 이는 **관리 오버헤드가 96% 감소**하는 효과가 있다.

### NIST RBAC 참조 모델

NIST SP 800-162은 RBAC를 **Core RBAC**, **Hierarchical RBAC**, **Constrained RBAC**의 3가지 수준으로 정의한다.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│            NIST RBAC 참조 모델 (4가지 구성 요소)                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  【구성 요소】                                                            │
│  ────────────                                                           │
│                                                                         │
│  1. USERS(U): 사용자 집합 {u₁, u₂, ...}                                    │
│  2. ROLES(R): 역할 집합 {r₁, r₂, ...}                                     │
│  3. PRMS(P): 권한 집합 {p₁, p₂, ...}                                      │
│  4. SESSIONS(S): 세션 집합 {s₁, s₂, ...}                                  │
│                                                                         │
│  【관계(Relations)】                                                      │
│  ────────────────                                                      │
│                                                                         │
│  UA ⊆ U × R : User-Role 할당 (사용자에게 역할 부여)                          │
│    예: {(kim, Dev), (kim, Ops), (lee, Ops)}                               │
│                                                                         │
│  PA ⊆ R × P : Role-Permission 할당 (역할에 권한 부여)                        │
│    예: {(Dev, code.read), (Dev, build.run), (Ops, vm.stop)}               │
│                                                                         │
│  user_sessions(s): S → U (세션의 소유자)                                  │
│  session_roles(s): S → 2^R (세션이 활성화한 역할 집합)                       │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  수준         │  추가 기능                              │  예시     │ │
│  │  ────         │  ───────────                              │  ────     │ │
│  │  Core RBAC   │  UA, PA, 세션 관리                     │  최소 RBAC│ │
│  │  Hier RBAC   │  Core + 역할 계층(RH)               │  Manager > Dev│ │
│  │  Conf RBAC   │  Core + SoD(직무 분리)               │  제안+승인 분리│ │
│  │  Full RBAC   │  Hier + Conf                         │  기업용 RBAC│ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  【역할 계층(Role Hierarchy: RH)】                                         │
│  ────────────────────────────────────                                     │
│                                                                         │
│  • r₁ ≥ r₂ : r₁은 r₂의 모든 권한을 상속                                      │
│  • 상위 역할: 하위 역할의 권한 + 자체 권한                                    │
│  • 예: Manager ≥ Developer ≥ Intern                                       │
│                                                                         │
│  【SoD(Separation of Duties) 제약조건】                                   │
│  ──────────────────────────────────────                                  │
│                                                                         │
│  • SSD(Static SoD): 사용자가 동시에 가질 수 없는 역할 집합                     │
│    예: {(Req, Appr)}는 상호 배제(한 사용자는 요청자/승인자 둘 다 불가)           │
│                                                                         │
│  • DSD(Dynamic SoD): 세션에서 동시에 활성화할 수 없는 역할 집합                   │
│    예: 한 세션에서 Developer와 QA 동시 활성화 금지                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Core RBAC는 UA, PA, 세션 관리의 기본 기능만 제공한다. Hierarchical RBAC은 역할 간 상속(RH)을 추가하여, 상위 역할(예: Manager)이 하위 역할(예: Developer)의 모든 권한을 자동으로 상속받는다. Constrained RBAC은 SoD(Separation of Duties)를 지원하여, **"요청자"와 "승인자" 역할은 한 사용자가 동시에 가질 수 없게** 강제한다. 이는 내자자 방지, 권한 분리를 위한 필수 기능이다. Full RBAC은 Hierarchical과 Constrained를 모두 포함한 완전한 모델로, 대규모 기업 환경에 적합하다.

### RBAC 구현 예시

Active Directory와 Kubernetes에서의 RBAC 구현을 보자.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│         RBAC 구현 예시: Active Directory vs Kubernetes                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  【Active Directory (Windows)】                                         │
│  ────────────────────────────────                                        │
│                                                                         │
│  1. 사용자(User) 생성                                                    │
│     $ New-ADUser -Name "kim" -SamAccountName "kim"                      │
│                                                                         │
│  2. 그룹(Group) = 역할(Role) 생성                                        │
│     $ New-ADGroup -Name "Developers" -GroupScope Global                   │
│     $ New-ADGroup -Name "Managers" -GroupScope Global                    │
│                                                                         │
│  3. 그룹에 사용자 추가 (UA: User Assignment)                                │
│     $ Add-ADGroupMember -Identity "Developers" -Members "kim"            │
│                                                                         │
│  4. ACL에 그룹에 권한 부여 (PA: Permission Assignment)                        │
│     $_acl = Get-Acl "C:\SourceCode"                                     │
│     $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule(│
│         "Developers", "ReadWrite", "Allow")                              │
│     Set-Acl "C:\SourceCode" $acl                                        │
│                                                                         │
│  5. 상속(Inheritance)으로 자식 폴더에 자동 적용                               │
│     # C:\SourceCode\* 폴더에 Developers 권한 자동 상속                       │
│                                                                         │
│  【Kubernetes RBAC】                                                      │
│  ──────────────────────────                                               │
│                                                                         │
│  1. ServiceAccount(사용자) 생성                                           │
│     $ kubectl create serviceaccount jenkins                             │
│                                                                         │
│  2. Role(역할) 생성 - ClusterRole(클러스 전체) 또는 Role(네임스페이스)          │
│     apiVersion: rbac.authorization.k8s.io/v1                             │
│     kind: Role                                                          │
│     metadata:                                                           │
│       name: pod-reader                                                  │
│     rules:                                                              │
│     - apiGroups: [""]                                                   │
│       resources: ["pods"]                                               │
│       verbs: ["get", "list", "watch"]                                   │
│     ---                                                                 │
│                                                                         │
│  3. RoleBinding(UA: User-Role 할당)                                      │
│     apiVersion: rbac.authorization.k8s.io/v1                             │
│     kind: RoleBinding                                                   │
│     metadata:                                                           │
│       name: jenkins-pod-reader                                          │
│     subjects:                                                           │
│     - kind: ServiceAccount                                              │
│       name: jenkins                                                     │
│     roleRef:                                                            │
│       kind: Role                                                        │
│       name: pod-reader                                                  │
│                                                                         │
│  4. 검증: jenkins ServiceAccount가 pods를 읽을 수 있는지                      │
│     $ kubectl auth can-i get pods --as=system:serviceaccount:default:jenkins│ │
│     yes                                                                  │
│                                                                         │
│  【AWS IAM RBAC】                                                        │
│  ────────────────────────                                                │
│                                                                         │
│  1. IAM User 생성                                                        │
│     $ aws iam create-user --user-name kim                               │
│                                                                         │
│  2. IAM Group(역할) 생성                                                  │
│     $ aws iam create-group --group-name Developers                       │
│                                                                         │
│  3. Group에 User 추가 (UA)                                                 │
│     $ aws iam add-user-to-group --user-name kim --group-name Developers │
│                                                                         │
│  4. Policy(권한) 생성 및 Group에 부여 (PA)                                    │
│     {                                                                   │
│       "Version": "2012-10-17",                                           │
│       "Statement": [{                                                    │
│         "Effect": "Allow",                                              │
│         "Action": ["s3:Get*", "s3:List*"],                              │
│         "Resource": "arn:aws:s3:::dev-bucket/*"                         │
│       }]                                                                │
│     }                                                                   │
│     $ aws iam attach-group-policy --group-name Developers --policy-arn ...│ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Active Directory는 그룹(Group)을 역할로 사용한다. `Developers` 그룹에 사용자를 추가하고, 폴더 ACL에 그룹 권한을 부여한다. Kubernetes는 ServiceAccount를 사용자, Role/ClusterRole을 역할, RoleBinding을 UA로 사용한다. AWS IAM은 Group을 역할, Policy(JSON 권한)을 Permission으로 사용한다. 모든 시스템이 **User → Role → Permission** 3단계 구조를 따르지만, 구체적인 용어와 API는 다르다.

---

## Ⅲ. 융합 비교 및 다각도 분석

### 비교 1: RBAC vs ACL vs ABAC

| 비교 항목 | ACL | RBAC | ABAC(Attribute-Based) |
|:---|:---|:---|:---|
| **관리 단위** | 사용자-권한 직접 매핑 | 역할 중개 | 속성 기반 동적 결정 |
| **확장성** | O(n×m) | O(n×r + r×m) | 속성 조합에 따라 다름 |
| **유연성** | 낮음(정적) | 중간(역할 재정의 필요) | 높음(속성 기반 동적) |
| **SoD 지원** | 복잡(수동 검증) | 쉬움(역할 상호 배제) | 쉬움(속성 제약) |
| **복잡도** | 단순 | 중간 | 복잡(정책 엔진 필요) |
| **대표적 구현** | Unix, Windows | AD, Kubernetes | XACML, AWS ABAC |

### 비교 2: Flat RBAC vs Hierarchical RBAC

```text
┌─────────────────────────────────────────────────────────────────────────┐
│            Flat RBAC vs Hierarchical RBAC                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  【Flat RBAC】                                                          │
│  ────────────                                                           │
│  • 역할 간 상속 없음                                                       │
│  • 각 역할에 독립적으로 권한 부여                                             │
│  • 장점: 단순, 명확                                                       │
│  • 단점: 권한 중복, 역할 수 폭발                                              │
│                                                                         │
│  예:                                                                    │
│  Intern: {code.read}                                                     │
│  Developer: {code.read, code.write, build.run}                          │
│  Senior Developer: {code.read, code.write, code.review, build.run}     │
│  Manager: {code.read, code.review, approve}                              │
│  # code.read가 4개 역할에 중복                                             │
│                                                                         │
│  【Hierarchical RBAC】                                                   │
│  ────────────────────────                                               │
│  • 역할 간 상속(RH: Role Hierarchy) 지원                                   │
│  • 상위 역할은 하위 역할의 모든 권한 상속                                    │
│  • 장점: 권한 중복 감소, 관리 효율                                           │
│  • 단점: 순환 참조 위험, 상속 이해 필요                                       │
│                                                                         │
│  예:                                                                    │
│  Manager ≥ Senior Developer ≥ Developer ≥ Intern                         │
│  Manager는 {code.read, code.write, code.review, build.run, approve}    │
│  # code.read는 Manager만 정의, 상위 역할로 자동 상속                           │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  계층 구조 시각화                                                      │ │
│  │                                                                       │ │
│  │        Admin                                                          │ │
│  │          │                                                            │ │
│  │      ┌───┴───┐                                                         │ │
│  │      │       │                                                         │ │
│  │   Manager   TechLead                                                 │ │
│  │      │       │                                                         │ │
│  │   ┌───┴───┐   │                                                      │ │
│  │   │       │   │                                                      │ │
│  │ Senior Dev QA Lead                                                  │ │
│  │   │       │   │                                                      │ │
│  │   └───┬───┘   │                                                      │ │
│  │       │       │                                                       │ │
│  │    Developer  Tester                                                  │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Flat RBAC는 각 역할이 독립적이므로, `code.read` 권한이 여러 역할에 중복된다. 역할이 추가될 때마다 권한을 재정의해야 한다. Hierarchical RBAC은 상위 역할이 하위 역할의 권한을 상속받으므로, `code.read`는 최하위 역할(예: Intern)에만 정의하면 된다. 단, 순환 참조(A ≥ B ≥ A)를 방지하는 검증이 필요하고, 상속 관계가 복잡해지면 이해하기 어려워진다.

### 과목 융합 관점

- **데이터베이스**: Oracle, PostgreSQL의 ROLE 기능은 RBAC를 구현한다. `CREATE ROLE developer; GRANT SELECT ON schema.table TO developer;`로 역할에 권한 부여하고, `GRANT developer TO kim;`으로 사용자에게 역할 할당한다.
- **네트워크**: RADIUS, TACACS+는 네트워크 장치 접근 제어에 RBAC를 사용한다. "network-admin" 역할은 모든 장치 설정 변경 가능, "helpdesk" 역할은 사용자 포트만 설정 가능하다.
- **클라우드**: AWS IAM, Azure RBAC, GCP IAM은 모두 RBAC를 기반으로 한다. AWS는 User/Group/Role/Policy 4가지 개념을, Azure는 Role Assignment/Definition으로 RBAC을 구현한다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 실무 시나리오

1. **시나리오 — 기업 내부 시스템 RBAC 설계**: 직원 500명, 시스템 30개의 기업에서 SoD(직무 분리)와 최소 권한 원칙을 준수하는 RBAC 설계. 아키텍트는 (1) 직무 분석: {Req, Appr, Exec, Audit} 역할 정의, (2) SoD 정책: Req와 Appr는 상호 배제, (3) 역할 계층: Executive > Manager > Staff, (4) 권한 할당: 각 역할에 필요한 최소 권한만 부여, (5) 정기적 리뷰(quarterly)로 부적절한 권한 회수, (6) 감사 로그로 모든 역할 변경/활성화 기록을 남긴다.

2. **시나리오 — Kubernetes 클러스터 RBAC 구성**: 개발팀에 네임스페이스 `dev`에서만 파드 생성/조회 권한 부여. 아키텍트는 (1) ServiceAccount `jenkins` 생성, (2) Role `dev-pod-manager`: verbs=["create", "get", "list"] resources=["pods"] 생성, (3) RoleBinding으로 `jenkins`와 `dev-pod-manager` 연결, (4) ClusterRole을 사용하지 않아 클러스터 전체 권한 노출 방지, (5) `kubectl auth can-i`로 권한 검증, (6) 정기적 `kubectl get rolebindings` audit로 불필요한 권한 제거.

3. **시나리오 — AWS IAM 거버넌스 구축**: 다중 계정(AWS Organizations)에서 각 부서별 계정과 역할 분리. 아키텍트는 (1) Organizations로 부서별 OU(Units) 생성, (2) 각 OU에 역할(Admin, Developer, Viewer) 정의, (3) SSO(Single Sign-On)로 IdP(Azure AD)와 연동, (4) MFA(Multi-Factor Authentication) 강제, (5) IAM Access Analyzer로 과도한 권한 탐지, (6) SCP(Service Control Policy)로 OU 간 권한 격리, (7) CloudTrail로 모든 IAM 호출 로그를 SIEM에 전송.

### 도입 체크리스트

- **기술적**: 모든 사용자가 개별 권한을 갖지 않고 역할을 통해 접근하는가? 역할 수가 최소화되어 있는가(10~50개 권장)? SoD 정책이 강제되는가?
- **운영·보안적**: 정기적(분기/반기) 권한 리뷰(Re-certification)가 수행되는가? 역할 생성/변경/삭제 시 승인 워크플로우가 있는가? 감사 로그에 모든 RBAC 변경이 기록되는가?

### 안티패턴

- **역할 폭발(Role Explosion)**: 너무 많은 역할(100개 이상)을 생성하면 관리가 복잡해진다. 역할을 직무 기반으로 재설계해야 한다.
- **"super-admin" 역할 남용**: 모든 권한을 갖는 역할은 보안 위험입니다. 최대한 분리하고, 임시 자격 증명(STS AssumeRole)을 권장한다.
- **정적 역할만 사용**: 속성 기반(ABAC) 동적 역할(예: "영업 직군 + 영업 시간대 + 사무실 내")을 활용하면 더 세분화된 제어가 가능하다.
- **감사 로그 미기록**: 역할 할당/변경을 로그에 남기지 않으면, 침해 시 원인 파악이 불가능하다.

---

## Ⅴ. 기대효과 및 결론

### 정량/정성 기대효과

| 구분 | 최적화 전 | 최적화 후 | 개선 효과 |
|:---|:---|:---|:---|
| **정량** | 사용자-권한 직접 매핑, O(100만) | RBAC 도입, O(4만) | **관리 오버헤드 96% 감소** |
| **정량** | 권한 리뷰 불가, 불필요 권한 방치 | 정기적 리뷰, 자동 회수 | **과도한 권한 80% 감소** |
| **정성** | 직무 분리 미준수, 내부자 위험 | SoD 강제, 거버넌스 강화 | **규정 준수**, 거버넌스 확립 |

### 미래 전망

- **ABAC(Attribute-Based Access Control)**: 사용자, 환경(시간, 위치), 리소스 속성을 기반으로 동적 접근 제어. XACML로 정의하며, "9시-18시 사이에 사무실 IP에서만 접속" 같은 복잡한 정책 가능.
- **Zero Trust RBAC**: "신뢰할 사용자는 없다"는 원칙하에, 모든 접근을 실시간 검증. BeyondProd, Google BeyondCorp가 이를 구현한다.
- **ML-based RBAC Optimization**: 기계 학습으로 사용자 행동 패턴을 분석하여, 이상적 역할 추천 및 비정상적 접근 탐지.

### 참고 표준

- **ANSI INCITS 359-2004**: RBAC 표준
- **NIST SP 800-162**: RBAC 참조 모델
- **ISO/IEC 24760**: 스마트 카드 기반 RBAC
- **RFC 2903**: Authorization for Access Control in the Internet

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [접근 제어 행렬](./610_access_matrix.md) → RBAC의 수학적 기반
- [ACL](./611_acl.md) → 사용자-권한 직접 매핑 대안
- [Capability](./612_capability.md) → 주체 중심 접근 제어
- [SoD](./630_separation_of_duties.md) → 직무 분리
- [Active Directory](./631_ad.md) → 구현 예시
- [Kubernetes RBAC](./632_k8s_rbac.md) → 쿠버네티스 RBAC
- [AWS IAM](./633_aws_iam.md) → 클라우드 RBAC

### 👶 어린이를 위한 3줄 비유 설명

**개념**: RBAC는 **회사의 직함별 출입증 제도** 같아요! "사원", "대리", "과장" 직함마다 들어갈 수 있는 방이 다르고, 할 수 있는 일도 다른 것처럼요.

**원리**: 내가 "개발자"라는 직함(역할)을 받으면, 개발자가 할 수 있는 모든 것(코드 읽기, 서버 접속 등)을 할 수 있어요. 새로운 개발자가 입사하면 "개발자" 직함만 주면 돼서 관리가 쉬워요.

**효과**: 사람이 100명이어도 직함(역할)은 10개면 돼서요! 각 사람마다 일일이 "무엇을 할 수 있나?" 적어 주는 것보다, 직함만 부여하면 모든 권한이 자동으로 따라와서 편리해요.
