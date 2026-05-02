+++
title = "114. 아고 CD (ArgoCD)"
weight = 114
date = "2026-03-04"
[extra]
categories = ["studynote-cloud"]
+++

## 핵심 인사이트 (3줄 요약)
- **GitOps의 사실상 표준:** 쿠버네티스 클러스터의 '원하는 상태(Desired State)'를 Git 저장소에 선언형으로 정의하고, 이를 실제 상태와 자동 동기화(Sync)하는 CD 도구입니다.
- **풀(Pull) 방식 배포:** 외부의 CI 서버가 클러스터에 접속해 명령을 내리는 Push 방식 대신, 클러스터 내부의 ArgoCD가 Git을 감시하다가 끌어오는 Pull 방식을 사용하여 보안을 극대화합니다.
- **단일 진실 공급원 (SSOT):** Git이 곧 인프라의 최종 상태가 되므로, 장애 시 Git 내역만 롤백(Revert)하면 인프라 전체가 1초 만에 복구됩니다.

### Ⅰ. 개요 (Context & Background)
전통적인 CI/CD 파이프라인(Jenkins 등)은 CI(빌드)와 CD(배포)가 강결합되어, 배포 스크립트(kubectl apply)가 클러스터의 권한을 통째로 쥐고 외부에서 명령을 내리는 형태였습니다. 
**ArgoCD**는 **GitOps** 사상을 쿠버네티스 환경에 완벽히 구현한 오픈소스 컨트롤러로, 클러스터 내부에서 동작하며 선언적 매니페스트(YAML, Helm Chart, Kustomize)의 변경 사항을 감지해 자동으로 인프라를 일치시킵니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
ArgoCD는 쿠버네티스의 네이티브 컨트롤러 패턴을 활용하여 지속적인 조정(Reconciliation) 루프를 실행합니다.

```text
+-------------------+           +-------------------------------------+
|  Git Repository   |           |         Kubernetes Cluster          |
| (Source of Truth) |           |                                     |
|                   |  [ Pull ] |   +-----------+       +-----------+ |
| - deployment.yaml | <-------- |   |  ArgoCD   | ----> |   Pods    | |
| - service.yaml    |   (Sync)  |   |Controller |       |  (Actual) | |
| - configmap.yaml  |           |   +-----------+       +-----------+ |
+---------^---------+           |         ^                   |       |
          |                     |         | (Compare & Apply) |       |
          | (Commit/Push)       +---------|-------------------|-------+
          |                               |                   |
+---------+---------+                     |   (Status Check)  |
|  Developer / CI   |                     +-------------------+
+-------------------+
```

1. **상태 비교 (Diff & Drift Detection):** 지정된 Git 저장소의 매니페스트 상태(Desired)와 K8s 클러스터의 실제 상태(Live)를 지속적으로 비교하여 구성 편류(Configuration Drift)를 탐지합니다.
2. **동기화 (Sync):** 차이가 발생하면 ArgoCD가 자동으로(혹은 수동 승인 후) Git의 상태를 클러스터에 반영(`kubectl apply`)합니다.
3. **가시성 제공:** 직관적인 웹 UI를 통해 애플리케이션의 토폴로지, 파드의 헬스 상태, 동기화 여부를 실시간 시각화합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | 전통적 Push 기반 CD (Jenkins) | GitOps Pull 기반 CD (ArgoCD) |
| :--- | :--- | :--- |
| **방향성** | CI 서버가 클러스터로 Push 배포 | 클러스터 내부의 에이전트가 Git을 Pull |
| **보안 (자격증명)** | CI 서버가 K8s 접속 인증서(Kubeconfig)를 보관해야 함 (보안 리스크 높음) | 외부로 K8s 인증서 유출 필요 없음. (보안성 최고) |
| **상태 관리** | 스크립트 실행 후의 상태를 보장하기 어려움 | K8s 컨트롤러 루프를 통해 항구적 상태(Sync) 보장 |
| **장애 복구** | 배포 파이프라인 역순 재실행 복잡함 | Git 커밋 Revert 만으로 즉시 롤백 (Self-healing) |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
1. **SSOT (Single Source of Truth) 확립:** 모든 인프라 변경 작업은 반드시 Git 커밋과 PR(Pull Request) 리뷰를 거치게 하여, 휴먼 에러를 방지하고 감사(Audit) 로그를 100% 확보할 수 있습니다.
2. **운영 핫픽스 통제:** 관리자가 `kubectl` 커맨드로 임의 변경한 설정(Drift)도 ArgoCD가 감지하여 즉시 Git 원본 상태로 강제 덮어쓰기(Auto-healing)하여 불변 인프라(Immutable Infrastructure) 원칙을 지켜냅니다.
3. **멀티 클러스터 관리:** 하나의 ArgoCD 인스턴스에서 수십 개의 타겟 K8s 클러스터(Dev, Stg, Prod)에 동시 배포 및 중앙 관리가 가능합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
ArgoCD는 쿠버네티스의 생태계에서 CD의 패러다임을 Push에서 Pull로 완전히 전환시켰습니다. Git이라는 친숙하고 검증된 도구를 인프라 제어판으로 사용함으로써, 개발자와 운영자가 동일한 언어(YAML)와 도구(Git)로 협업하는 진정한 데브옵스/GitOps 문화를 완성하는 필수 플랫폼입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념:** 데브옵스 (DevOps), 지속적 배포 (CD), 쿠버네티스 (Kubernetes)
- **하위/연관 개념:** GitOps, 상태 동기화 (Reconciliation), 헬름 (Helm), 플럭스 (Flux CD)

### 👶 어린이를 위한 3줄 비유 설명
1. 집을 지을 때 '설계도(Git)'를 고치면, 마법의 목수(ArgoCD)가 그걸 보고 똑같이 집(클러스터)을 자동으로 고쳐줘요.
2. 누군가 몰래 벽에 낙서를 해도 목수가 설계도와 다르다는 걸 알고 금방 원래대로 싹 지워버리죠.
3. 그래서 우리는 집을 직접 고칠 필요 없이, 설계도만 예쁘게 잘 그리면 된답니다!