+++
weight = 115
title = "테라폼 (Terraform) 인프라 프로비저닝"
date = "2026-03-04"
[extra]
categories = ["studynote-cloud"]
+++

## 핵심 인사이트 (3줄 요약)
1. **테라폼(Terraform)**은 하시코프(HashiCorp)가 개발한 대표적인 인프라스트럭처 애즈 코드(IaC) 도구로, HCL(선언적 언어)을 사용해 인프라를 코드로 관리합니다.
2. AWS, Azure, GCP 등 수백 개의 이기종 멀티 클라우드 프로바이더(Provider) 자원을 단일 템플릿 언어로 통합 제어할 수 있는 압도적 장점이 있습니다.
3. 인프라의 현재 상태를 저장하는 **상태 파일(tfstate)**을 기반으로 멱등성(Idempotency)을 보장하며, 변경 전 실행 계획(Plan)을 미리 보여주어 안전한 배포가 가능합니다.

### Ⅰ. 개요 (Context & Background)
과거 클라우드 엔지니어들은 웹 브라우저 UI(콘솔) 마우스 클릭이나 절차적 쉘 스크립트로 인프라를 구축했습니다. 이는 휴먼 에러를 유발하고 인프라 버전을 추적할 수 없는 한계가 있었습니다. 테라폼은 클라우드 아키텍처를 소스 코드로 형상 관리(Git 연동)하고, 코드 리뷰를 통해 배포하는 GitOps 패러다임을 열어준 핵심 기술입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)
테라폼은 선언형(Declarative) 방식을 사용하여 최종 목표 상태만 지정하면 내부 엔진이 알아서 생성/수정/삭제 순서를 최적화하여 실행합니다.

```text
+-------------------------------------------------------------+
|                Terraform Workflow Architecture              |
|                                                             |
|  [HCL Code (.tf)] ---> `terraform init` (Downloads Provider)|
|         |                                                   |
|         v                                                   |
|  `terraform plan` ---> Compares HCL with [.tfstate] & Cloud |
|         |              (Shows + Create, - Destroy, ~ Update)|
|         v                                                   |
|  `terraform apply` --> Calls Cloud API (AWS/GCP) to match   |
|                        Desired State and Updates [.tfstate] |
+-------------------------------------------------------------+
```

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

| 비교 항목 | Terraform (HashiCorp) | AWS CloudFormation | Ansible |
|---|---|---|---|
| **지원 환경** | 멀티/하이브리드 클라우드 | AWS 전용 종속(Lock-in) | 멀티 서버(OS 레벨) |
| **목적** | **인프라 프로비저닝** (VPC, VM 생성) | 인프라 프로비저닝 | **구성 관리** (OS 세팅, 패키지 설치) |
| **관리 방식** | 상태 파일(State) 기반 선언형 | Stack 단위 선언형 | 절차형 + 멱등성 지향 |
| **언어** | HCL (HashiCorp Configuration) | JSON / YAML | YAML |

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)
* **상태 파일(tfstate) 관리 보안**: `.tfstate` 파일에는 DB 패스워드 등 민감한 클라우드 메타데이터가 평문으로 저장됩니다. 따라서 절대 로컬 Git에 커밋하면 안 되며, AWS S3나 Terraform Cloud와 같은 원격 백엔드에 저장하고 락(DynamoDB State Lock)을 걸어 동시성 충돌을 막아야 합니다.
* **모듈화(Module)**: 반복되는 인프라 아키텍처(예: EKS 클러스터 구축 템플릿)를 모듈로 추상화하여 사내 개발팀에 벤딩 머신처럼 제공하는 플랫폼 엔지니어링 전략이 요구됩니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)
테라폼 도입은 클라우드 재해 복구(DR) 시 몇 분 만에 완벽히 동일한 인프라를 타 리전에 재생성하는 엄청난 복원력을 제공합니다. 최근 클라우드 네이티브 생태계에서는 쿠버네티스의 크로스플레인(Crossplane) 등과 융합되어 더욱 고도화된 IaC 표준으로 진화하고 있습니다.

### 📌 관련 개념 맵 (Knowledge Graph)
* **상위 개념**: 인프라 애즈 코드(IaC), 데브옵스(DevOps)
* **하위 개념**: HCL, tfstate, Provider, Module
* **연관 개념**: GitOps, Ansible, AWS CloudFormation, 멀티 클라우드

### 👶 어린이를 위한 3줄 비유 설명
1. 마인크래프트에서 집을 지을 때 블록을 하나씩 손으로 직접 쌓는 건 너무 귀찮고 힘들죠.
2. 테라폼은 "방 3개짜리 멋진 성을 지어줘"라고 설계도(코드)를 써서 주면, 마법 지팡이가 1초 만에 성을 뚝딱 만들어주는 도구예요.
3. 설계도만 잘 보관해두면 언제 어디서든 똑같은 성을 백 번이고 다시 만들 수 있답니다!
