+++
title = "15. DevOps / SRE / 플랫폼엔지니어링 키워드 목록"
date = 2026-03-03
[extra]
categories = "pe_exam-devops"
+++

# DevOps / SRE / 플랫폼 엔지니어링 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 DevOps·SRE·플랫폼공학 전 영역 기술사 수준 키워드
> ⚡ DevOps/SRE는 "소프트웨어를 얼마나 빠르고 안전하게 운영 환경에 전달하고 유지하는가"의 전체 철학·도구·조직

---

## 1. DevOps 문화 / 원칙 — 14개

1. DevOps 정의 — Dev+Ops 통합 문화, CALMS (Culture/Automation/Lean/Measurement/Sharing)
2. The Three Ways (Gene Kim) — 흐름/피드백/지속적 학습·실험
3. DevOps 메트릭 — DORA 4지표 (배포빈도/리드타임/MTTR/변경실패율)
4. DevOps 성숙도 — DORA Research, Elite/High/Medium/Low 분류
5. DevSecOps — 보안 Left-Shift, 파이프라인에 보안 내재화
6. 가치 스트림 맵핑 (Value Stream Mapping) — 낭비 식별, 흐름 최적화
7. 내부 개발자 플랫폼 (IDP, Internal Developer Platform) — 골든 패스 제공
8. 플랫폼 엔지니어링 (Platform Engineering) — 개발자 경험(DX) 향상
9. Shift Left — 테스트·보안·품질을 개발 초기 단계로 이동
10. 심리적 안전감 (Psychological Safety) — 실수를 학습으로, 비난 없는 사후분석
11. 카오스 엔지니어링 (Chaos Engineering) — Chaos Monkey, 의도적 장애 실험
12. 사이트 신뢰성 공학 (SRE) — Google, 소프트웨어 엔지니어링으로 운영 문제 해결
13. Toil (노동) — 수작업·반복·자동화 가능 운영 작업, SRE는 50% 이하 유지
14. DevOps 도구체인 — 계획(Jira)/소스(Git)/빌드(Maven)/CI(Jenkins)/CD(ArgoCD)/모니터링(Grafana)

---

## 2. 소스 관리 / 형상 관리 — 14개

1. Git — 분산 버전 관리,  커밋/브랜치/태그/스태시/리베이스
2. Git 브랜치 전략 — GitFlow / GitHub Flow / GitLab Flow / Trunk-Based Development
3. Trunk-Based Development (TBD) — 짧은 수명 브랜치, 빈번한 통합, DORA 권장
4. GitFlow — Feature/Develop/Release/Hotfix/Main 브랜치 모델
5. 모노레포 (Monorepo) — Nx / Turborepo / Bazel — 단일 저장소 다중 패키지
6. Pull Request / Code Review — LGTM, 최소 2인 승인 정책
7. 시맨틱 버전닝 (SemVer) — MAJOR.MINOR.PATCH, 하위 호환성
8. CHANGELOG / Release Notes 자동화 — Conventional Commits, semantic-release
9. Git Hooks — Pre-commit, Husky, lint-staged 자동화
10. 코드 서명 (Code Signing) — GPG, 커밋 서명 확인
11. 바이너리 관리 — Artifactory / Nexus — 패키지 저장소
12. Submodule / Subtree — 모노레포 대안, 외부 저장소 참조
13. 코드 소유권 (CODEOWNERS) — 자동 리뷰어 지정
14. 오픈소스 기여 모델 — Fork → PR → Merge, CLA (기여자 라이선스)

---

## 3. CI/CD 파이프라인 심화 — 20개

1. CI (Continuous Integration) — 자동 빌드/테스트, 빠른 피드백 루프
2. CD (Continuous Delivery) — 자동 배포 준비, 인간 승인 후 배포
3. CD (Continuous Deployment) — 완전 자동 프로덕션 배포
4. Jenkins — 가장 성숙한 CI 서버, Declarative Pipeline, Groovy DSL
5. GitHub Actions — YAML 기반, 마켓플레이스 액션, Self-hosted Runner
6. GitLab CI/CD — `.gitlab-ci.yml`, Runner, Auto DevOps
7. CircleCI — 오비트 기반, 빠른 캐싱, 병렬 실행
8. ArgoCD — GitOps 기반 CD, Kubernetes 클러스터 동기화
9. Flux CD — GitOps 오퍼레이터, Source Controller
10. Tekton — Kubernetes 네이티브 CI/CD, CRD 기반
11. Spinnaker — 멀티클라우드 CD, Netflix 개발
12. 파이프라인 as Code — Jenkinsfile / .github/workflows / .gitlab-ci.yml
13. 빌드 도구 — Maven / Gradle / Bazel / Buck / Make
14. 컨테이너 빌드 — Docker Buildx / Buildah / Kaniko / ko (Go)
15. 이미지 스캐닝 — Trivy / Snyk / Grype / Clair — CVE 탐지
16. SAST — SonarQube / Checkmarx / Semgrep — 정적 코드 분석
17. DAST — OWASP ZAP / Burp Suite — 동적 취약점 스캔
18. SCA (Software Composition Analysis) — 오픈소스 취약점, FOSSA / Snyk
19. SBOM (Software Bill of Materials) — 의존성 목록, CycloneDX / SPDX
20. Supply Chain Security — SLSA 레벨 1~4, Sigstore / cosign / rekor

---

## 4. 배포 전략 심화 — 14개

1. 블루/그린 배포 (Blue/Green) — 즉각 전환, 빠른 롤백, 2배 인프라
2. 카나리 배포 (Canary) — 점진적 트래픽 이동, 위험 최소화
3. 롤링 업데이트 (Rolling Update) — 순차 교체, 무중단
4. 피처 플래그 (Feature Flag / Toggle) — LaunchDarkly / Unleash — 코드 배포와 기능 출시 분리
5. 다크 론칭 (Dark Launch) — 프로덕션 트래픽 미러링, 숨겨진 기능 테스트
6. 섀도우 배포 (Shadow Deployment) — 실 트래픽 복제, 부담 없는 검증
7. A/B 테스트 배포 — 실험적, 통계적 유의성 검증
8. Immutable Infrastructure — 업데이트 대신 교체, 드리프트 없음
9. GitOps 배포 — Git 상태 = 클러스터 상태, ArgoCD/Flux
10. Progressive Delivery — 점진 출시 제어, Argo Rollouts / Flagger
11. Argo Rollouts — CanaryStep / BlueGreen Analysis / 자동 롤백
12. Feature Experimentation Platform — Split.io / Optimizely
13. 롤백 전략 — 즉각 롤백 / 재배포 시간 목표 < 5분
14. 배포 승인 게이트 (Approval Gate) — 수동 / 자동화 품질 게이트

---

## 5. 인프라 자동화 (IaC) — 14개

1. Infrastructure as Code (IaC) — 역할 드리프트 방지, 버전 관리, 재현 가능 인프라
2. Terraform — HCL, 선언적, 멀티클라우드, State 파일, Plan/Apply/Destroy
3. Terraform 모듈 — 재사용 가능 인프라 컴포넌트, Registry
4. Terraform State — Remote Backend (S3+DynamoDB), 잠금, 민감 데이터
5. OpenTofu — Terraform 오픈소스 포크, BSL 라이선스 대응
6. Pulumi — 범용 언어 (Python/Go/TS/C#), Crossplatform SDK
7. AWS CDK (Cloud Development Kit) — L1/L2/L3 컨스트럭트, TypeScript/Python
8. CloudFormation — AWS 네이티브, 스택/변경셋, StackSets
9. ARM Template / Bicep (Azure) — Azure 네이티브 IaC
10. Ansible — 에이전트리스, YAML Playbook, 구성 관리
11. Packer — VM/컨테이너 이미지 빌드 자동화
12. Vagrant — 개발 환경 가상화, Vagrantfile
13. 구성 드리프트 감지 — Terraform Plan / InSpec / AWS Config
14. Policy as Code — OPA (Open Policy Agent) / Sentinel / Checkov — 인프라 정책 검사

---

## 6. 가관측성 (Observability) 심화 — 20개

1. 가관측성 3 기둥 — 로그(Logs) / 메트릭(Metrics) / 추적(Traces)
2. OpenTelemetry — 계측 표준화, OTLP 프로토콜, SDK/API/Collector
3. 분산 추적 (Distributed Tracing) — TraceID/SpanID, Jaeger / Zipkin / Tempo
4. 메트릭 (Metrics) — 카운터/게이지/히스토그램/서머리
5. Prometheus — Pull 기반 수집, PromQL, Alertmanager
6. PromQL — 메트릭 쿼리 언어, rate()/increase()/histogram_quantile()
7. Grafana — 대시보드, 다중 데이터소스, 알람
8. Grafana LGTM Stack — Loki(로그)/Grafana(시각화)/Tempo(추적)/Mimir(메트릭)
9. ELK Stack — Elasticsearch / Logstash / Kibana, 로그 분석
10. Loki — Prometheus 방식 로그 집계, Label 기반, 저비용
11. Datadog — SaaS APM, 트레이스/메트릭/로그 통합, AI 이상 탐지
12. New Relic / Dynatrace / AppDynamics — 엔터프라이즈 APM
13. APM (Application Performance Monitoring) — 응답시간/에러율/처리량
14. RUM (Real User Monitoring) — 실제 사용자 경험, Core Web Vitals
15. 에러 추적 — Sentry / Rollbar / Bugsnag
16. SLI (Service Level Indicator) — 측정 가능 지표 (예: 99퍼센타일 응답시간)
17. SLO (Service Level Objective) — SLI의 목표값 (예: 99.9%)
18. 에러 예산 (Error Budget) — 1 - SLO, 허용 가능한 다운타임
19. SLA (Service Level Agreement) — 외부 계약, 위반 시 페널티
20. 알람 피로 (Alert Fatigue) — 노이즈 감소, 심각도 분류, Page/Ticket 구분

---

## 7. SRE (Site Reliability Engineering) 심화 — 16개

1. SRE 개념 — Google, 소프트웨어 엔지니어링 방식으로 운영 문제 해결
2. SRE vs DevOps — SRE는 DevOps 구현 방법론, 실천적 역할
3. 에러 예산 정책 — SLO 위반 시 기능 출시 제한
4. 포스트모템 (Post-Mortem) — 비비난 원칙, 5-Why, 액션 아이템
5. Runbook / Playbook — 운영 절차서, 자동화 연동
6. Incident Management — 인시던트 등급 / 지휘 체계 / 역할 (IC, Comms, SCribe)
7. On-Call 운영 — PagerDuty / OpsGenie / VictorOps, 순환 당직
8. 용량 계획 (Capacity Planning) — 수요 예측, 적정 자원
9. 성능 테스트 — 부하/스트레스/내구성/스파이크, JMeter/k6/Locust/Gatling
10. 카오스 엔지니어링 도구 — Chaos Monkey / LitmusChaos / Gremlin / Steadybit
11. 게임 데이 (Game Day) — 의도적 장애 시나리오 훈련
12. 자동화 기준 — 반복 50%+ → 자동화 필수
13. SRE 조직 모델 — 임베디드 / 중앙화 / 위성 모델
14. 가용성 목표 — 99.9% = 8.7h/y / 99.99% = 52min/y / 99.999% = 5min/y
15. RTO / RPO / MTD — 복구 시간/데이터 손실/최대 허용 다운타임
16. BCP (Business Continuity Plan) + DR (Disaster Recovery) 연계

---

## 8. 현대 소프트웨어 개발 도구 — 10개

1. 코드 리뷰 도구 — Gerrit / GitHub PR / GitLab MR / Phabricator
2. 이슈 추적 — Jira / Linear / GitHub Issues / YouTrack
3. 지식 관리 — Confluence / Notion / Obsidian / GitBook
4. 의사소통 — Slack / Teams / Discord — ChatOps 통합 (GitOps 알림 채널)
5. 설계 협업 — Figma / Miro / Lucidchart — 아키텍처/UX 시각화
6. API 개발 — Postman / Insomnia / Bruno — API 테스트, 문서화
7. 데이터베이스 관리 — DBeaver / TablePlus / DataGrip
8. 시크릿 관리 (로컬) — direnv / dotenv 보안 처리
9. DevContainer — VS Code 원격 개발, Docker 기반 일관 환경
10. GitHub Codespaces / Gitpod — 클라우드 IDE, 즉시 개발 환경

---

**총 키워드 수: 122개**
