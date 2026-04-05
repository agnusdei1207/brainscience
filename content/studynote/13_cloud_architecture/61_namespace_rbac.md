+++
weight = 61
title = "61. 네임스페이스/RBAC"
date = "2026-04-05"
[taxonomies]
tags = ["Cloud", "Kubernetes", "K8s", "Namespace", "RBAC", "Security"]
categories = ["13_cloud_architecture"]
+++

# 네임스페이스/RBAC

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 네임스페이스는 하나의 물리적 쿠버네티스 클러스터를 여러 논리적 클러스터로분할하는 가상 격리 단위이며, RBAC(역할 기반 접근 제어)은 사용자와 서비스 어카운트에 대한 리소스 操作権限を定義(리소스 操作 권한을 정의)하는 보안 메커니즘이다.
> 2. **가치**: 이 두 가지 메커니즘의 조합은 멀티 테넌시 환경에서 팀별/환경별 자원 격리와 최소 권한 원칙에 따른 보안 접근 제어를 동시에実現한다.
> 3. **융합**: 네임스페이스, RBAC, ResourceQuota, NetworkPolicy 등이 결합하여 단일 클러스터 내에서완전한 멀티 테넌시 격리를実現하는 클라우드 네이티브 보안 아키텍처를構築한다.

---

### Ⅰ. 개요 및 필요성 (Context & Necessity)

쿠버네티스 클러스터는 대규모 컨테이너 워크로드를 Hosting하는 통합 플랫폼이다. 그러나 하나의 거대한 클러스터에서 수십 개의 팀, 수백 개의 서비스,数千 개의 파드가混在하면(혼재하면)管理`和安全` 측면에서 심각한 문제가 발생한다. 팀 A의 실수가 팀 B의 서비스에 영향을 미치고, 한 개발자의 과실로 전체 클러스터가 마비될 수 있으며, 보안 침해 시犯人の特定(범죄자 특정)이 어렵다. 전통적으로는 팀마다 개별 클러스터를 운영했으나, 이는 비용 비효율과 운영 복잡도를招来(야기)했다.

쿠버네티스는 이 문제를 **네임스페이스(Namespace)**와 **RBAC(역할 기반 접근 제어)**라는 두 가지 메커니즘으로解決한다. 네임스페이스는 클러스터를 논리적으로 분할하여各팀/각환경/각서비스が独立的(독립적으로) 리소스를 사용할 수 있게 한다. 네임스페이스 안에서만 이름이 고유하면 되므로 리소스命名衝突(충돌)을 걱정할 필요가 없다. RBAC는 누가 어떤 리소스에 대해 어떤 操作을 할 수 있는지를 역할(Role/ClusterRole)과 역할 바인딩(RoleBinding/ClusterRoleBinding)을 통해定義한다. 이로써 개발자는 자신의 네임스페이스에서만 작업할 수 있고, 클러스터 전체 리소스에 대한 관리자 권한은 필요한 사람에게만 부여된다.

```text
[네임스페이스 기반 멀티 테넌시 아키텍처]
┌─────────────────────────────────────────────────────────────────────────────┐
│                        물리적 쿠버네티스 클러스터                              │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐              │
│  │   dev 네임스페이스  │ │  stg 네임스페이스 │ │  prod 네임스페이스│              │
│  │  ┌───────────┐  │ │  ┌───────────┐  │ │  ┌───────────┐  │              │
│  │  │ Service A │  │ │  │ Service A │  │ │  │ Service A │  │              │
│  │  │ Service B │  │ │  │ Service B │  │ │  │ Service B │  │              │
│  │  └───────────┘  │ │  └───────────┘  │ │  └───────────┘  │              │
│  │   RBAC:dev-role │ │   RBAC:stg-role │ │  RBAC:prod-role │              │
│  │  ResourceQuota:  │ │  ResourceQuota:  │ │  ResourceQuota:  │              │
│  │   dev-limit      │ │   stg-limit      │ │   prod-limit     │              │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │               kube-system 네임스페이스 (클러스터 시스템용)                  │  │
│  │              CoreDNS, Metrics Server, Ingress Controller                │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

이 구조의 핵심은 **논리적 격리**이다. 물리적으로는同一(동일) 클러스터이지만, 논리적으로는 네임스페이스에 의해 분리되어 있어 팀 A의 문제가 팀 B에 영향을 주지 않는다. 그러나 네트워크 정책(NetworkPolicy)을 별도로 설정하지 않으면同一(동일) 클러스터 내의 네임스페이스 간 통신은デフォルト(기본)으로 가능하므로, 네트워크 격리가 필요한 경우 반드시 NetworkPolicy를 설정해야 한다.

📢 **섹션 요약 비유**: 쿠버네티스 네임스페이스는 대규모 종합병원(클러스터)의 진료科(과) 체계와 같습니다. 소화기과(DEV 네임스페이스), 심장내과(STG 네임스페이스), 뇌신경과(PROD 네임스페이스)가同一个(동일) 병원 건물 안에 있으나, 각 과의 환자名簿(명부)와 자원(의료기기, 약품)은 서로 격리되어 있습니다. 뇌신경과 의사의 실수가 소화기과에.incident(사건)를引起的(일으키지 않는) 것과 같습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**네임스페이스**는 쿠버네티스 리소스를 논리적으로 分離(분리)하는 단위이다. 네임스페이스는 IP, 포트, 파드 이름 등 논리적 리소스를 구분하지만, 스토리지(PV)와 같은 물리적 리소스는 공유한다. 시스템 네임스페이스인 `kube-system`은 쿠버네티스 시스템コンポーネント(컴포넌트)가使用하며, 일반 사용자는ここに(여기에) 리소스를作成하지 않는 것이 권장된다. `default` 네임스페이스는 사용자가 리소스를 생성할 때自動的に使用される(자동으로 사용된다).

네임스페이스의 주요 리소스 격리 기능은以下(이하)와 같다. **이름 충돌 방지와**、同一(동일) 클러스터에서 여러 팀/환경이各自(각자) 자신의 네임스페이스에서 중복되지 않는 이름을 사용할 수 있다. **RBAC 격리**: Role/RoleBinding은 특정 네임스페이스 내의 권한만管理하며, ClusterRole/ClusterRoleBinding은 클러스터 전체 리소스에 대한 권한을管理한다. **ResourceQuota**: 네임스페이스별로 CPU, 메모리, 파드 수等的(등의) 자원 사용량을 제한한다. **LimitRange**: 네임스페이스 내에서 생성되는 개별 리소스의 기본 request/limit 값을 설정한다. **네임스페이스 삭제**: 네임스페이스를 삭제하면 其内(그 안)의 모든 리소스도 함께 삭제(Cascading Delete)된다.

**RBAC(역할 기반 접근 제어)**는 쿠버네티스의 주요 권한 관리 메커니즘이다. RBAC는 네 가지 주요 오브젝트로 구성된다. **Role**은 특정 네임스페이스 내의 리소스에 대한 권한을定義하고, **RoleBinding**은 해당 Role을 사용자나 그룹에 할당한다. **ClusterRole**은 클러스터 전체의 리소스에 대한 권한을定義하고, **ClusterRoleBinding**은 해당 ClusterRole을 클러스터 전체에 할당한다. 권한은 HTTP 동사(verbs: get, list, create, update, patch, delete, deletecollection)로 표현된다.

```yaml
# Role 예시: 파드 읽기 권한
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
```

```yaml
# RoleBinding 예시: 사용자 alice에게 pod-reader 역할 부여
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader-binding
  namespace: default
subjects:           # 권한을 부여받는 대상
- kind: User
  name: alice
  apiGroup: rbac.authorization.k8s.io
roleRef:            # 할당될 역할
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

RBAC의 핵심 원칙은 **最小権限(최소 권한) 원칙**이다. 사용자에게는 업무 수행에 필요한最小限(최소한)의 권한만 부여해야 한다. 예를 들어, 개발자에게는 `kubectl get`과 `kubectl logs` 권한만 부여하고, 파드를削除하거나 Deployment를 수정할 수 있는 권한은 부여하지 않는 것이 권장된다. ClusterRoleBinding을 통해 한 번에 여러 사용자에게 클러스터 전체 권한을 부여하는 것은危険(위험)하며, 반드시 필요한 경우가 아니면 사용하지 않는 것이 좋다.

📢 **섹션 요약 비유**: RBAC는 은행의 역할별 금고 접근 권한과 같습니다. 은행원A(역할: 창구 담당)는 고객 접견(읽기)과 예금 취급(쓰기)만 가능하고, 금고 내부(클러스터 전체 중요 리소스)에는 접근할 수 없습니다. 은행장B(역할: 관리자)는 모든 금고에 접근할 수 있지만, 모든 직원에게その権限(그 권한)을委譲하면(위임하면) 보안 사고가 발생할 수 있습니다. 그래서 역할(Role/ClusterRole)은 업무 범위에 맞춰厳格히(엄격히) 정의되어야 합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

네임스페이스, RBAC, ResourceQuota, LimitRange, NetworkPolicy 등은 서로 다르지만 상호 보완적인 격리 메커니즘이다. **네임스페이스**는論理的な(논리적) 리소스 격리를 제공하고, **RBAC**는操作権限(操作 권한)을控制하며, **ResourceQuota**는 자원 사용량을 제한하고, **LimitRange**는 개별 리소스의 요청값/상한을 설정하며, **NetworkPolicy**는 네트워크 트래픽을制御한다. 이 다섯 가지가 함께 적용될 때初めて(비로소) 완전한 멀티 테넌시 격리가 실현된다.

| 격리 메커니즘 | 대상 | 기능 | 적용 레벨 |
|:---|:---|:---|:---|
| **네임스페이스** | 리소스 이름 | 이름 충돌 방지, 논리적 분리 | 네임스페이스 |
| **RBAC** | API 操作権限 | 사용자/서비스 계정 권한 제어 | NS / 클러스터 |
| **ResourceQuota** | CPU, Memory, 파드 수 | 네임스페이스 전체 자원 상한 | 네임스페이스 |
| **LimitRange** | Request/Limit | 개별 파드/컨테이너 기본값 | 네임스페이스 |
| **NetworkPolicy** | Ingress/Egress 트래픽 | 파드/네임스페이스 간 통신 제어 | 파드 |

**ServiceAccount와 RBAC의 조합**은 기계間(기계 간) 통신의 권한 관리에 중요하다. 파드内的(내部的)에 실행되는 애플리케이션이 쿠버네티스 API를 호출해야 할 때, 해당 애플리케이션은 Human User가 아닌 **ServiceAccount**를 사용하여 인증한다. ServiceAccount에도 RBAC Role을 바인딩할 수 있어, 각 애플리케이션이 자신의 네임스페이스의 리소스만 읽도록限制할 수 있다. 이를 통해 만약 한 파드가 침해되었더라도其の(그) 파드가 클러스터 전체를 컨트롤하는 것은 불가능해진다.

```yaml
# ServiceAccount 예시
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app-sa
  namespace: production
---
# 해당 ServiceAccount에 대한 RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: my-app-sa-binding
  namespace: production
subjects:
- kind: ServiceAccount
  name: my-app-sa
  namespace: production
roleRef:
  kind: Role
  name: my-app-read-only
  apiGroup: rbac.authorization.k8s.io
```

RBAC과 **Pod Security Policy(PSP)** 또는 **Pod Security Standard(PSS)**의 조합도 중요하다. RBAC이 "누가 어떤 리소스를 操作できる(操作할 수 있는)지"를 제어한다면, PSP/PSS는 "파드가 어떤 보안 제약 조건을遵守해야 하는지"를控制한다. 예컨대 RBAC으로 사용자가 파드를作成할 수 있는 권한이 있더라도, PSP에서Privileged(특권) 컨테이너 생성 거부되면Privileged 파드는 생성되지 않는다. 두 메커니즘을 함께 사용하여Defense in Depth(방어의 심층화)를 실현한다.

📢 **섹션 요약 비유**: RBAC과 PSP의 조합은 공항의보안檢索(검색) 체계와 같습니다. boarding ticket(RBAC)은「어떤 분실물 수하물」(어떤 네임스페이스/리소스)에 입장할 수 있는지를 보여주며, 보안 검색대(PSP/PSS)는 수하물 안에 어떤 물건(컨테이너 보안)이 들어있는지를 검사합니다. boarding ticket이 있어도 폭발물(特権 컨테이너)이 발견되면탑승이 거부됩니다.

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무에서 네임스페이스를設計할 때는 팀/환경/서비스 조합으로 струк화하는 것이 권장된다. 基本(기본) 구조는 `teamname-dev`, `teamname-stg`, `teamname-prod`처럼 팀명과 환경을 조합하거나, `frontend-dev`, `backend-dev`, `data-proc-dev`처럼 서비스 도메인과 환경을 조합하는 방법이 있다. 시스템 네임스페이스인 `kube-system`에는 시스템组件(컴포넌트)만 배치하고 일반 애플리케이션은ここに(여기에) 배치하지 않아야 한다.

RBAC을实务에 적용할 때는 다음要点을 따라야 한다. First, Human User와 ServiceAccount를명확히 구분하여管理해야 한다. Second, 권한은 업무 수행에 필요한最小限(최소한)의 권한만 부여하는 최소 권한 원칙을 준수해야 한다. Third, ClusterRoleBinding은 클러스터 전체에 영향을 미치므로 사용할 때 각별히 주의해야 하며, 일상적인操作에는 Namespace-scoped Role/RoleBinding을사용하는 것이 권장된다. Fourth, 정기적으로 사용되지 않는 계정과的角色을审核(감사)하여 정리해야 한다.

```text
[Production RBAC 安全运营 체크리스트]
1. 계정 관리
   ├─ Human User: SSO(Active Directory, Google 등) 연동
   ├─ ServiceAccount: 애플리케이션별 개별 SA 생성
   ├─ 영구 계정密钥(키) 정리: 사용하지 않는 계정 비활성화
   └─Periodic 감사: 역할 할당 내역 확인

2. 역할設計
   ├─ Namespace-scoped Role:日常操作用(일상적 조작용)
   ├─ ClusterRole: 클러스터 전체 권한이 필요한 경우만
   ├─ aggregation: ClusterRole에 여러 Role 조합 (재사용)
   └─ 권한 세분화: 너무 큰 권한은複数の(여러) 역할로 분할

3. 네임스페이스設計
   ├─ 팀/환경별 분리: team-prod, team-dev 등
   ├─ 시스템 네임스페이스 격리: kube-system에 일반 파드 배치禁止
   ├─ NetworkPolicy: 네임스페이스 간 통신이 필요한 경우만 허용
   └─ ResourceQuota: 네임스페이스별 자원 한계 설정

4. 모니터링 및审计
   ├─ Audit Logging: 모든 API 操作 기록 (cloud logging 연동)
   ├─ RBAC 변경 알람: 역할/바인딩 변경 시 Alert
   ├─ 시크릿 접근 로깅: 민감 리소스 접근 감사
   └─ Periodic Penetration Test: 침투 테스트로 권한 확인
```

또한 ResourceQuota와 LimitRange를 통해 네임스페이스 전체의 자원 사용량을control하고, 개별 파드의 자원 요청/상한을 설정하는 것이 권장된다. ResourceQuota를 설정하지 않으면 한 네임스페이스의 파드가 클러스터 전체 자원을 consume하여 다른 네임스페이스에 영향을 줄 수 있다. `LimitRange`를 설정하면 파드 생성 시 반드시 resource request/limit을 지정해야 하므로, 자원使用量(사용량)을 예측하기 쉬워진다.

📢 **섹션 요약 비유**: Production RBAC 실무는 고급 호텔의 카드키 체계와 같습니다. 각 직원(사용자)에게는 업무에 필요한 층(네임스페이스)만 입장할 수 있는 카드가 부여됩니다.客室清掃担当(객실 청소 담당)는客室(파드)이 있는 층만 갈 수 있고,フロント(프론트) 담당은全층(모든 네임스페이스)都可以하지만、金庫室(金고실)에는 누구도 개인 카드로 갈 수 없습니다(최소 권한).カードキー履歴(카드키 이력)는常に記録(항상 기록)되어 의심스러운 접근이 있으면即座に(즉시) 보안팀이 확인합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)

네임스페이스와 RBAC의 조합은 대규모 조직에서 쿠버네티스 클러스터를安全하고 효율적으로管理하는 필수 요소이다. 단일 클러스터에서 팀별/환경별 논리적 격리를 실현하면, 클러스터 구축 및 운영 비용을 크게 절감하면서도보안성을維持할 수 있다. RBAC을 통해最小権限原則을 적용하면,万一(만약) 침해가 발생해도 그被害範囲(피해 범위)를 제한할 수 있어 Zero Trust Security的实现에 기여한다.

| 기대 효과 | 도입 전 | 도입後 | 효과 |
|:---|:---|:---|:---|
| 클러스터 관리 비용 | 팀당 개별 클러스터 (수십 개) | 단일/소수 클러스터 | 70% 비용 절감 |
| 보안 수준 | 수동 권한 관리, 과도한 권한 | RBAC 기반 최소 권한 | 90% 향상 |
| 운영 효율성 | 별도 클러스터별 관리 부담 | 통합 클러스터 관리 | 60% 향상 |
| 인시던트 대응 | 전체 클러스터 영향 | 네임스페이스 단위 격리 | 80% 향상 |

미래에는 RBAC이 더욱細分化되어(세분화되어), 애드혹(Ad-hoc) 작업 그룹을 위한 временные(임시) 권한 부여나, 외부 IDP(Identity Provider)와의 SAML/OIDC 연동을 통한 자동화된 Lifecycle 관리가 표준화될 것이다. 또한 Policy-as-Code(OPA, Kyverno) 도구와 결합하여, RBAC 정책의 자동 검증과 클러스터 내 모든 리소스에 대한Continuous Compliance Monitoring이 실현될 것이다. 결론적으로, 네임스페이스와 RBAC는 쿠버네티스 멀티 테넌시의 양대 축이며, 둘을 잘 조합하여 사용하면 비용 효율적이고安全な(보안성 높은) 클라우드 네이티브 환경을構築할 수 있다.

📢 **섹션 요약 비유**: 네임스페이스와 RBAC의 조합은 도시의区域(구역) 분리 및 출입 관리 시스템과 같습니다. 도시(클러스터)는住宅地区(거주 지역),商業地区(상업 지역),工業地区(산업 지역)로分区(분구)되어 있고, 주민(사용자)에게는 자신의住宅地区(해당 네임스페이스)의 시설만 사용할 수 있는 출입카드(역할)가 부여됩니다.郡守(관리자)만이 도시 전체 시설에 접근할 수 있어,万一火災(화재)가住宅地区에서 발생해도 그것が商业地区에 확대되지 않도록街区(구역) 격리가 됩니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- Namespace | 클러스터를 논리적으로 분할하는 가상 격리 단위
- RBAC (Role-Based Access Control) | 역할 기반으로 리소스 操作権限を定義(리소스 操作 권한을 정의)하는 메커니즘
- Role/RoleBinding | 네임스페이스 레벨의 권한 정의 및 할당
- ClusterRole/ClusterRoleBinding | 클러스터 레벨의 권한 정의 및 할당
- ServiceAccount | 파드나 다른 리소스가 쿠버네티스 API를 호출할 때 사용하는 계정

### 👶 어린이를 위한 3줄 비유 설명
1. 네임스페이스는 놀이공원 안에 있는 각각의 놀이기구 구역과 같아요. 회전목마는 회전목마 구역에만 있고, 밋밋이는 물건区域에만 있어요.
2. RBAC은 놀이공원의 입장과 같아요. 일반 손님(일반 개발자)은 놀이기구만 타지만, 관리자(운영자)는 모든 구역에 입장할 수 있어요.
3. 이렇게 하면 어떤 손님이 문제를 일으켜도 그 구역 안에서만 영향이 있고, 다른 놀이기구에는 영향이 없어요!
