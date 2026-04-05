+++
title = "Jenkins"
description = "Jenkins"
category = "4_software_engineering"
weight = 836
+++

# Jenkins

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Jenkins (이전 Hudson)는 Java 기반의 오픈소스 CI/CD 자동화 서버로, Pipeline (dsl) 코드를 통해 복잡한 빌드-테스트-배포 파이프라인을コード화하고 자동화하는 대표적인 CI/CD 도구다.
> 2. **가치**: Jenkins는 수천 개의 플러그인을 통해 다양한 도구와 통합되어, 조직의 특성에맞춤화된 CI/CD 파이프라인을 구축할 수 있으며, 대규모 엔터프라이즈 환경에서 가장 널리 사용되는 CI/CD 도구 중 하나다.
> 3. **융합**: Jenkins는 Git, Docker, Kubernetes, SonarQube, Artifactory 등 주요 DevOps 도구와 긴밀하게 통합되며, Jenkinsfile (Groovy DSL)을 통해 파이프라인을 코드로 관리하고, Jenkins X는 Kubernetes-native CI/CD로 확장되었다.

---

## Ⅰ. 개요 및 필요성 (Context & Necessity)

- **개념**: Jenkins는 2004년 Sun Microsystems의 Kohsuke Kawaguchi가 Hudsonとして開発を開始し、2011年にJenkinsとしてforkされたJava 기반 CI/CD 서버다. Jenkins의 핵심 기능은"Pipeline as Code"로, groovy 기반 DSL인 Jenkinsfile을 통해 빌드, 테스트, 배포 과정을 코드로 정의하고 자동화한다. 이를 통해 파이프라인의版本관리, 검토, 공유가 가능해졌다.

- **필요성**:手動ビルドとテストは、時間のかかり、人は介在的错误を犯しがちで、再現性がない。 Jenkinsは、これらの手動プロセスを自動化し、"信頼できる反復可能なプロセス"を実現する.

- **💡 비유**: Jenkins는"자동化工場の控制室"과 같다. 控制室에서 각 기계의 가동/정지,品質 검사, 제품 흐름을監視하고, 문제 발생 시即時 경고한다. Jenkins도 코드 변경Detectorから始まり、빌드/테스트/배포流程를自動化し, 문제 발견 시即時 알림한다.

- **등장 배경**: 2004년 Hudsonとして 시작, 2011年 분기업무之後 Jenkinsとして独立. 현재까지 가장 널리 사용되는 CI/CD 도구 중 하나.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### Jenkins 아키텍처

| 구성 요소 | 역할 |
|:---|:---|
| **Master** | Jenkins의 중추, 스케줄링, UI 제공, API 관리 |
| **Agent (Node)** | 실제 빌드/테스트를 실행하는 워커 |
| **Plugin** | 기능 확장 (Git, Docker, Kubernetes 등) |
| **Jenkinsfile** | Pipeline 정의를 담은 코드 파일 |

### Jenkins Pipeline 구조

```text
  ┌─────────────────────────────────────────────────────────────────┐
  │                    Jenkins Pipeline 구조                               │
  ├─────────────────────────────────────────────────────────────────┤
  │
  │  [ Declarative Pipeline 예시]
  │
  │  pipeline {
  │      agent any
  │      stages {
  │          stage('Build') {
  │              steps {
  │                  echo 'Building...'
  │                  sh 'mvn clean package'
  │              }
  │          }
  │          stage('Test') {
  │              steps {
  │                  echo 'Testing...'
  │                  sh 'mvn test'
  │              }
  │              post {
  │                  always {
  │                      junit 'target/surefire-reports/*.xml'
  │                  }
  │              }
  │          }
  │          stage('Deploy') {
  │              when {
  │                  branch 'main'
  │              }
  │              steps {
  │                  echo 'Deploying...'
  │                  sh 'kubectl apply -f k8s/'
  │              }
  │          }
  │      }
  │  }
  │
  │  ※ Jenkinsfile은 Git에 함께 저장되어 版本管理의 이점을 제공           │
  │
  └─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Jenkins의 Declarative Pipeline은"코드로서의 파이프라인"을実現한다. 위 예시에서 Build → Test → Deploy 단계로 구성되고, 각 단계에서実行되는 명령어 (sh)와 결과 보고 (junit)를 정의한다. Post 블록에서는测试 결과를 항상 수집하고, When 블록에서는 main 브랜치에서만 Deploy가実行される도록条件을 걸었다. Jenkinsfile은 Git에 함께 저장되므로, 파이프라인 변경도 코드 변경과 동일하게 검토하고롤백할 수 있다.

---

## Ⅲ. 주요 플러그인

| 플러그인 | 용도 |
|:---|:---|
| **Git Plugin** | Git 소스 코드 관리 |
| **Docker Plugin** | Docker 이미지 빌드/푸시 |
| **Kubernetes Plugin** | Jenkins Agent를 Kubernetes Pod로 실행 |
| **SonarQube Scanner** | 정적 분석 실행 |
| **JUnit Plugin** | 테스트 결과 보고서 |
| **Blue Ocean** | 파이프라인 시각화 UI |
| **Pipeline (plugin)** | Pipeline as Code 지원 |

### Master-Agent架构

```text  ┌─────────────────────────────────────────────────────────────────┐
  │                 Jenkins Master-Agent 아키텍처                          │
  ├─────────────────────────────────────────────────────────────────┤
  │
  │       [Jenkins Master]                                            │
  │       ┌───────────────────────┐                                 │
  │       │ • 스케줄링             │                                 │
  │       │ • 파이프라인 조정       │                                 │
  │       │ • UI / API 제공        │                                 │
  │       │ • Plugin 관리          │                                 │
  │       └───────────┬───────────┘                                 │
  │                   │                                              │
  │     ┌─────────────┼─────────────┐                                │
  │     │             │             │                                │
  │     ▼             ▼             ▼                                │
  │  [Agent 1]   [Agent 2]   [Agent 3]                              │
  │  (Linux)     (Windows)   (Kubernetes)                           │
  │  빌드 실행     빌드 실행     빌드 실행                          │
  │                                                              │
  └─────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** Jenkins Master는 파이프라인의"조정자" 역할만 하며, 실제 빌드와 테스트는 Agent (Node)에서実行된다. Agent는物理 서버, VM, 또는 Kubernetes Podとして配置でき、複数の 빌드를병렬로実行할 수 있다. 이를 통해 Master의 부하를分散하고, 다양한 환경 (Linux, Windows, Kubernetes)에서 빌드를실행할 수 있다.

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 권장 설정

| 설정 | 권장 |
|:---|:---|
| **파이프라인 문서화** | Jenkinsfile에 주석 필수 |
| **代理机构池** | 용도별 (빌드/테스트/배포) 분리 |
| **보안** | 권한 관리 (Matrix Authorization) |
| **백업** | JENKINS_HOME 정기 백업 |

### 안티패턴

- **Free-styleプロジェクトの過度**: Pipeline으로 전환하지 않고 많은 Free-style 프로젝트 운영
- **大型单打者**: 하나의巨大的 Pipeline이 여러 역할을 수행
- **Plugin過多**: 필요한 플러그인만 설치 (보안 ↑
- **설정分散**: Jenkins 설정이 코드화되지 않고 GUI에서 직접 관리

- **📢 섹션 요약 비유**: Jenkins는"공장 자동化控制系统"과 같다. Control Room (Master)에서 생산라인 (Agent)을 제어하고, 각 공정 (Stage)에서 품질 검사 (Test)를実施하며, 문제 발생 시即時 경고한다.

---

## Ⅴ. 기대효과 및 결론

### 미래 전망

- **Jenkins X / Tekton**: Kubernetes-native CI/CD로의 진화
- **Configuration as Code**: Jenkins 설정의全自动化

### 대안 도구

| 도구 | 특징 |
|:---|:---|
| **GitHub Actions** | GitHub에 통합, YAML 설정 |
| **GitLab CI** | GitLab에 통합, YAML 설정 |
| **CircleCI** | 관리형 CI/CD, 빠른 속도 |
| **Tekton** | Kubernetes-native CI/CD 프레임워크 |

- **📢 섹션 요약 비유**: Jenkins는"万能 리모컨"과 같다. 여러 기기 (도구)를 하나의 리모컨 (Jenkins)에서制御하고, 그 操作 방법 (Pipeline)을 코드 (Jenkinsfile)로保存할 수 있다.

---

## 📌 관련 개념 맵 (Knowledge Graph)

| 개념 명칭 | 관계 및 시너지 설명 |
|:---|:---|
| **CI/CD Pipeline** | Jenkins는 CI/CD 파이프라인을 구현하는 대표적인 도구이며, Jenkinsfile을 통해 파이프라인을 코드로 정의한다. |
| **Pipeline as Code** | 파이프라인 정의를 코드 (Jenkinsfile)로管理하여, 版本管理와 코드 검토의 이점을 취한다. |
| **Agent/Node** | Jenkins Master의 지시下で실제 빌드/테스트를実行하는 워커이다. |
| **Docker** | Jenkins에서 Docker 이미지를 빌드하고 실행하기 위한 통합이다. |
| **Kubernetes** | Kubernetes Plugin을 통해 Jenkins Agent를 Pod로 실행하여, 동적 스케일링을 지원한다. |
| **GitOps** | Jenkins와 GitOps를 결합하여, Git을 단일 진실 공급원으로活用한 배포 자동화가 가능하다. |
| **SonarQube** | Jenkins 파이프라인의 분석 단계에서 활용되는 정적 분석 도구로, 코드 품질 게이트를 설정한다. |

---

## 👶 어린이를 위한 3줄 비유 설명

1. Jenkins는"공장ラインの全てを取り持つ_manager"와 같다. 생산 라인에 문제가 생기면Manager가即時 파악하고, 생산을 다시 진행하거나 사람을 호출한다.
2. Jenkinsfile은"생산라인の操作手順書"와 같아. Manager가従って動く一指图であり、何か問題が生じたときに備えた指示書でもある.
3. Jenkins의 Agent는"생산라인의 일하는 사람들"과 같아. Manager(마스터)의 지시을 받아 각자 일(빌드/테스트)을 수행하고, 결과를 Manager에게報告한다.
