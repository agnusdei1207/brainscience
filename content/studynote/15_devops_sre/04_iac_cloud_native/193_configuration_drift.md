+++
weight = 193
title = "구성 편류 (Configuration Drift)"
date = "2024-03-24"
[extra]
categories = "studynote-devops-sre"
+++
## 0. 핵심 인사이트

> **핵심**: (개념 본질)
> **비유**: (개념 비유)

> 📝 모범 답안

- **상태의 불일치:** 시간이 흐름에 따라 실제 운영 환경의 인프라 설정이 최초 정의된 코드(IaC)나 문서와 달라지는 현상.
- **장애의 씨앗:** 수동 패치나 임시 조치가 누적되어 "어제는 됐는데 오늘은 안 되는" 비결정적 오류와 보안 취약점을 유발.
- **해결 전략:** 불변 인프라 도입, 주기적인 Drift Detection 자동화, 그리고 GitOps를 통한 강제 동기화(Reconciliation Loop)가 필수.

### 1. 개요 및 필요성
자동화된 인프라 관리 환경에서도 긴급 장애 대응을 위해 관리자가 콘솔에서 직접 설정을 변경(ClickOps)하거나, 특정 서버에만 보안 패치를 수동으로 적용하는 일이 발생하곤 합니다. 이러한 미세한 차이가 쌓여 개발-테스트-운영 환경이 서로 달라지는 것을 '구성 편류(Configuration Drift)'라고 합니다. 이는 배포 실패의 1순위 원인이자 사이버 공격자가 노리는 약점이 됩니다.

### 2. 구성요소
구성 편류는 관리자가 인지하지 못하는 사이에 인프라의 '엔트로피'가 증가하는 과정입니다.

```text
[ The Phenomenon of Configuration Drift ]

 (Day 1: Perfect Alignment)    (Day 30: Drift Occurs)     (Day 60: System Failure)
      IaC Code == Live              IaC Code != Live           IaC Code << Live
   +--------------------+        +--------------------+     +--------------------+
   |   [VPC Config]     |        |   [VPC Config]     |     |   [VPC Config]     |
   |   - Subnet A       |        |   - Subnet A       |     |   - Subnet A       |
   |   - Port 80 Open   |        |   - Port 80 Open   |     |   - Port 80 Open   |
   +--------------------+        +--------------------+     +--------------------+
             ||                            ||                         !!
   +--------------------+        +--------------------+     +--------------------+
   |   Actual Cloud     |        |   Actual Cloud     |     |   Actual Cloud     |
   |   - Subnet A       |        |   - Subnet A       |     |   - Subnet A       |
   |   - Port 80 Open   |        |   - Port 22 Open*  |     |   - Port 3306 Open*|
   +--------------------+        +--------------------+     +--------------------+
                                 (*Manual Change!)          (*Unauthorized Risk!)

[ Detection & Remediation Loop ]
1. Plan: IaC 코드 실행 계획 생성.
2. Compare: 실제 리소스 상태(State)와 코드 비교.
3. Detect: 불일치(Diff) 항목 식별 및 경고.
4. Sync: 코드를 기반으로 실제 인프라를 다시 덮어씀(Overwrite).
```

### 3. 구조 및 동작 원리

| 비교 항목 | 구성 편류 (Configuration Drift) | 눈송이 서버 (Snowflake Server) |
| :--- | :--- | :--- |
| **정의** | 코드와 실제 상태 간의 '차이' 자체 | 제각각 다른 설정을 가진 '서버 결과물' |
| **발생 원인** | 수동 변경, 자동 스케일링 설정 오류 | 수동 관리, 파편화된 스크립트 실행 |
| **주요 위험** | 배포 예측 불가, 보안 구멍(Hole) | 장애 복제 불가, 담당자 의존성 심화 |
| **방지 도구** | Terraform Drift Detection, ArgoCD | Docker, Ansible, Immutable Image |

### 4. 비교 및 트레이드오프
- **실무 적용:** 테라폼의 `terraform plan` 명령을 스케줄러(Cron)로 주기적으로 실행하여 'No changes'가 나오는지 감시하거나, AWS Config와 같은 서비스를 통해 리소스 변경 이벤트를 실시간 추적하여 Slack 알람을 보냅니다.
- **기술사적 판단:** 구성 편류를 막는 가장 궁극적인 방법은 '읽기 전용 인프라'를 지향하는 것입니다. 운영 환경에 대한 직접 쓰기 권한을 인간에게서 뺏고, 오직 파이프라인(GitOps)만이 변경을 수행할 수 있도록 거버넌스를 강화해야 합니다. 이는 단순히 기술적인 문제를 넘어 조직의 운영 성숙도를 의미합니다.

### 5. 실무 적용 및 최적화 기법
구성 편류를 효과적으로 관리하면 인프라의 '가시성'과 '재현성'이 확보됩니다. 이는 재해 복구(DR) 상황에서 코드를 실행하는 것만으로 운영 환경을 100% 똑같이 복구할 수 있음을 의미합니다. 앞으로는 AI가 Drift를 실시간으로 감지하고 IaC 코드를 역으로 업데이트하거나 자동 복구하는 'Self-healing IaC'가 표준이 될 전망입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** IaC Lifecycle, Infrastructure Governance
- **하위 개념:** Drift Detection, State File Management, ClickOps
- **연관 기술:** Terraform, ArgoCD, AWS Config, Azure Policy

### 👶 어린이를 위한 3줄 비유 설명
1. 엄마가 써준 '장보기 목록'이 IaC 코드라면, 실제로 바구니에 담긴 물건이 현재 인프라 상태예요.
2. 목록에 없는 과자를 몰래 담거나, 사야 할 우유를 안 샀다면 '편류(Drift)'가 생긴 거예요.
3. 나중에 계산대에서 돈이 모자라거나 요리를 못 하게 되는 사고를 막으려면, 항상 목록과 바구니를 똑같이 맞춰야 해요.
