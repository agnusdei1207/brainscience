+++
title = "젠킨스 (Jenkins)"
description = "가장 널리 사용되는 오픈소스 CI/CD 자동화 서버로 1800개 이상의 플러그인 생태계를 가진 확장 가능한 빌드 파이프라인 플랫폼"
date = 2024-05-15
[taxonomies]
tags = ["Jenkins", "CI/CD", "Automation", "Pipeline", "DevOps", "OpenSource"]
+++

# 젠킨스 (Jenkins)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: Java로 작성된 오픈소스 **CI/CD 자동화 서버**로, 선언적(Declarative) 및 스크립트(Scripted) 파이프라인을 통해 빌드, 테스트, 배포를 자동화하고, 1800개 이상의 플러그인으로 거의 모든 도구와 통합 가능한 확장성을 제공합니다.
> 2. **가치**: 무료 오픈소스이면서도 엔터프라이즈급 기능(분산 빌드, 보안, RBAC)을 제공하여, 전 세계 수백만 조직이 표준 CI/CD 플랫폼으로 채택하고 있으며, "Pipeline as Code"로 Git과 완벽히 통합됩니다.
> 3. **융합**: Git, Docker, Kubernetes, AWS/Azure/GCP, SonarQube, Slack, Jira 등과 플러그인으로 연동되며, GitOps(ArgoCD) 및 최신 CI 도구(GitHub Actions)와 하이브리드 구성도 가능합니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**젠킨스(Jenkins)**는 지속적 통합(Continuous Integration, CI)과 지속적 배포(Continuous Deployment, CD)를 자동화하는 **오픈소스 자동화 서버**입니다. 2004년 Sun Microsystems의 Kohsuke Kawaguchi가 Hudson으로 개발을 시작했고, 2011년 Oracle과의 분쟁 이후 Jenkins로 이름이 변경되었습니다. 핵심 특징:
- **Pipeline as Code**: Jenkinsfile로 파이프라인을 코드로 정의
- **Plugin Ecosystem**: 1800+ 플러그인으로 확장
- **Distributed Builds**: Master-Agent 구조로 분산 빌드
- **Multi-platform**: Linux, Windows, macOS, Docker, Kubernetes 지원

### 2. 구체적인 일상생활 비유
공장의 **자동화 조립 라인**을 상상해 보세요. 부품이 들어오면 -> 조립 -> 검사 -> 포장 -> 출하까지 자동으로 진행됩니다. 젠킨스는 **소프트웨어 공장의 자동화 라인**입니다. 코드가 들어오면 -> 컴파일 -> 테스트 -> 보안 스캔 -> 패키징 -> 배포까지 자동으로 진행됩니다. 사람이 개입하지 않아도 24/7 돌아갑니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (수동 빌드의 지옥)**:
   개발자가 로컬에서 `mvn clean install`을 실행하고, 성공하면 운영팀에 war 파일을 전달했습니다. 다른 개발자의 환경에서는 실패하는 "내 컴퓨터에서는 되는데" 문제가 빈발했습니다.

2. **혁신적 패러다임 변화의 시작**:
   2004년 Hudson(Jenkins 전신)이 "지속적 통합" 개념을 도구화했습니다. 모든 커밋마다 중앙 서버에서 자동으로 빌드/테스트를 실행하여, 통합 문제를 조기 발견합니다. 2016년 Jenkins 2.0에서 Pipeline as Code가 도입되며 현대적 CI/CD 도구로 진화했습니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   비록 GitHub Actions, GitLab CI, CircleCI 등 클라우드 네이티브 도구가 등장했지만, 온프레미스, 커스터마이징, 레거시 시스템 연동이 필요한 기업에서는 여전히 Jenkins가 1순위입니다.

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Component) | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 |
| :--- | :--- | :--- | :--- |
| **Master (Controller)** | 스케줄링, 설정 관리, UI 제공 | Jetty 서블릿 컨테이너, 큐 관리 | Java, Servlet |
| **Agent (Node)** | 실제 빌드 실행 | SSH, JNLP로 Master와 연결 | Docker, K8s Pod |
| **Pipeline** | 빌드 단계 정의 | Groovy DSL, Declarative/Scripted | Jenkinsfile |
| **Plugin Manager** | 플러그인 설치/관리 | Update Center에서 다운로드 | HPI 형식 |
| **Build Queue** | 빌드 요청 대기열 | FIFO, 우선순위 지원 | 메모리 큐 |
| **SCM Polling/Webhook** | 코드 변경 감지 | Git hook,定时 polling | Git, GitHub |

### 2. 정교한 구조 다이어그램: Jenkins 분산 아키텍처

```text
=====================================================================================================
                      [ Jenkins Master-Agent Distributed Architecture ]
=====================================================================================================

  [ Developers ]               [ Jenkins Master ]                [ Build Agents ]
       |                            |                                   |
       | git push                   |                                   |
       v                            v                                   v

+----------------+          +----------------------+          +----------------------+
| Git Repository |  webhook | Jenkins Controller   |          | Build Agents         |
| (GitHub/       | -------> | +------------------+ |          | +------------------+ |
|  GitLab)       |          | | Web UI (Jetty)   | |          | | Agent-1 (Docker) | |
+-------+--------+          | | - Job Config      | |  SSH/   | | - Maven          | |
        |                   | | - Build Queue     | |  JNLP   | | - Node.js        | |
        |                   | | - Plugin Manager  | | ------->| +------------------+ |
        |                   | +------------------+ |          |                      |
        |                   | | SCM Polling/      | |          | +------------------+ |
        |                   | | Webhook Listener  | |          | | Agent-2 (K8s)    | |
        |                   | +------------------+ | -------->| | - Helm           | |
        |                   | | Scheduler         | |          | | - kubectl       | |
        |                   | +---------+--------+ |          | +------------------+ |
        |                   |           |          |          |                      |
        |                   |           v          |          | +------------------+ |
        |                   | +-----------------+  |          | | Agent-3 (Windows)| |
        |                   | | Build Executor  |  | -------->| | - MSBuild       | |
        |                   | | (Distributed)   |  |          | | - .NET          | |
        |                   | +-----------------+  |          | +------------------+ |
        |                   +----------------------+          +----------------------+
        |                                                             |
        |                    +---------------------------------------+
        |                    |
        v                    v
+----------------+          +----------------------+
| Artifacts      |<---------| Deploy Targets       |
| Repository     |          | - Kubernetes Cluster |
| (Nexus/        |          | - AWS EC2            |
|  Artifactory)  |          | - Docker Registry    |
+----------------+          +----------------------+

=====================================================================================================

                      [ Jenkins Pipeline Stages ]
=====================================================================================================

  Jenkinsfile (Pipeline as Code)
  +------------------------------------------+
  | pipeline {                               |
  |   agent any                              |
  |   stages {                               |
  |     stage('Checkout') { -------------> [1] git checkout
  |       steps { checkout scm }             |
  |     }                                    |
  |     stage('Build') { ---------------> [2] mvn clean package
  |       steps { sh 'mvn package' }         |
  |     }                                    |
  |     stage('Test') { ----------------> [3] junit, jacoco
  |       steps { sh 'mvn test' }            |
  |     }                                    |
  |     stage('SonarQube') { ------------> [4] code quality scan
  |       steps { ... }                      |
  |     }                                    |
  |     stage('Docker Build') { ---------> [5] docker build
  |       steps { ... }                      |
  |     }                                    |
  |     stage('Deploy to Staging') { ----> [6] kubectl apply
  |       steps { ... }                      |
  |     }                                    |
  |     stage('Integration Test') { -----> [7] e2e tests
  |       steps { ... }                      |
  |     }                                    |
  |     stage('Deploy to Prod') { -------> [8] kubectl apply
  |       when { branch 'main' }             |
  |       steps { ... }                      |
  |     }                                    |
  |   }                                      |
  | }                                        |
  +------------------------------------------+

=====================================================================================================
```

### 3. 핵심 알고리즘 및 실무 코드 예시

**선언적 파이프라인 (Jenkinsfile)**

```groovy
// Jenkinsfile (Declarative Pipeline)
pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: maven
    image: maven:3.8-openjdk-17
    command: ['sleep', '99d']
  - name: docker
    image: docker:20.10
    command: ['sleep', '99d']
    volumeMounts:
    - name: docker-sock
      mountPath: /var/run/docker.sock
  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
'''
        }
    }

    environment {
        DOCKER_REGISTRY = 'registry.example.com'
        IMAGE_NAME = 'myapp'
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git rev-parse HEAD > .git/commit-id'
                script {
                    env.GIT_COMMIT = readFile('.git/commit-id').trim()
                }
            }
        }

        stage('Build') {
            steps {
                container('maven') {
                    sh 'mvn clean package -DskipTests'
                }
            }
        }

        stage('Unit Test') {
            steps {
                container('maven') {
                    sh 'mvn test'
                }
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                    jacoco execPattern: '**/target/jacoco.exec'
                }
            }
        }

        stage('Code Quality') {
            steps {
                container('maven') {
                    withSonarQubeEnv('SonarQube') {
                        sh 'mvn sonar:sonar'
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                container('docker') {
                    sh """
                        docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} .
                        docker tag ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Push to Registry') {
            steps {
                container('docker') {
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-registry-creds',
                        usernameVariable: 'REGISTRY_USER',
                        passwordVariable: 'REGISTRY_PASS'
                    )]) {
                        sh """
                            echo ${REGISTRY_PASS} | docker login ${DOCKER_REGISTRY} -u ${REGISTRY_USER} --password-stdin
                            docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                            docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:latest
                        """
                    }
                }
            }
        }

        stage('Deploy to Staging') {
            environment {
                KUBECONFIG = credentials('staging-kubeconfig')
            }
            steps {
                sh """
                    kubectl set image deployment/${IMAGE_NAME} ${IMAGE_NAME}=${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} -n staging
                    kubectl rollout status deployment/${IMAGE_NAME} -n staging --timeout=300s
                """
            }
        }

        stage('Integration Test') {
            steps {
                sh './run-integration-tests.sh staging'
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            input {
                message "Deploy to production?"
                ok "Deploy"
                submitter "release-team"
            }
            environment {
                KUBECONFIG = credentials('prod-kubeconfig')
            }
            steps {
                sh """
                    kubectl set image deployment/${IMAGE_NAME} ${IMAGE_NAME}=${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} -n production
                    kubectl rollout status deployment/${IMAGE_NAME} -n production --timeout=300s
                """
            }
        }
    }

    post {
        success {
            slackSend(
                color: 'good',
                message: "Build Successful: ${env.JOB_NAME} #${env.BUILD_NUMBER}\nURL: ${env.BUILD_URL}"
            )
        }
        failure {
            slackSend(
                color: 'danger',
                message: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}\nURL: ${env.BUILD_URL}"
            )
        }
    }
}
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: CI/CD 도구 비교

| 평가 지표 | Jenkins | GitHub Actions | GitLab CI | CircleCI |
| :--- | :--- | :--- | :--- | :--- |
| **설치 방식** | Self-hosted | SaaS (+ Self-hosted) | SaaS + Self-hosted | SaaS |
| **비용** | 무료 | 무료(공개) / 유료(비공개) | 무료 / 유료 | 유료 |
| **플러그인** | 1800+ | Marketplace | Built-in | Orb |
| **학습 곡선** | 높음 (Groovy) | 낮음 (YAML) | 낮음 (YAML) | 낮음 (YAML) |
| **UI** | 구형 | 현대적 | 현대적 | 현대적 |
| **확장성** | 매우 높음 | 중간 | 높음 | 중간 |
| **레거시 연동** | 매우 강함 | 약함 | 중간 | 약함 |

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 레거시 시스템과의 연동 필요**
- **문제점**: 온프레미스 SVN, 사내 Nexus, 레거시 배포 스크립트를 사용해야 합니다.
- **기술사 판단 (전략)**: Jenkins가 최적. SVN, SSH, 커스텀 스크립트 플러그인이 풍부. Self-hosted로 내부망에서 운영 가능.

**[상황 B] 스타트업의 신규 프로젝트**
- **문제점**: 인프라 운영 인력이 없고, 빠르게 CI/CD를 구축해야 합니다.
- **기술사 판단 (전략)**: GitHub Actions 또는 GitLab CI가 더 적합. Jenkins는 설치/운영 오버헤드가 큼.

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 수동 빌드 (AS-IS) | Jenkins 자동화 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **빌드 빈도** | 주 1회 | 커밋마다 | **빌드 100배 증가** |
| **통합 문제 발견** | 배포 직전 | 커밋 즉시 | **조기 발견 90%** |
| **인건비** | 높음 | 낮음 | **운영 비용 70% 절감** |

### 2. 참고 표준/가이드
- **Jenkins User Documentation**: 공식 사용자 가이드
- **Jenkins Pipeline Syntax Reference**: 파이프라인 문법 참조

---

## 관련 개념 맵 (Knowledge Graph)
- **[CI/CD 파이프라인](@/studynotes/15_devops_sre/3_automation/continuous_integration.md)**: Jenkins가 구현하는 자동화 흐름
- **[GitOps](@/studynotes/15_devops_sre/3_automation/86_gitops.md)**: Jenkins + ArgoCD 하이브리드 구성
- **[SonarQube](@/studynotes/15_devops_sre/3_automation/79_sonarqube.md)**: 정적 분석 통합
- **[Docker](@/studynotes/13_cloud_architecture/1_native/docker.md)**: 컨테이너 빌드 자동화
- **[ArgoCD](@/studynotes/15_devops_sre/3_automation/89_argocd.md)**: Jenkins CI -> ArgoCD CD

---

## 어린이를 위한 3줄 비유 설명
1. 공장에는 **로봇 팔**이 있어서 부품을 조립하고 검사해요. 젠킨스는 **소프트웨어 공장의 로봇**이에요!
2. 개발자가 코드를 올리면, 젠킨스가 알아서 "컴파일하고, 테스트하고, 배포까지" 다 해줘요.
3. 덕분에 개발자는 코드만 잘 쓰면 돼요. 로봇이 24시간 돌아가니까 밤에도 일해줘요!
