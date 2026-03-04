+++
title = "13. 클라우드 아키텍처 키워드 목록"
date = 2026-03-03
[extra]
categories = "pe_exam-cloud"
+++

# 클라우드 아키텍처 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 클라우드 전 영역 기술사 수준 키워드
> ⚡ 클라우드 아키텍처는 단순 서비스 나열이 아닌 **비용·성능·가용성·보안·운영성 5축의 트레이드오프 판단**이 핵심

---

## 1. 클라우드 기초 / 서비스 모델 — 22개

1. 클라우드 컴퓨팅 정의 — NIST SP 800-145 (5특성·3서비스·4배포 모델)
2. NIST 5특성 — 온디맨드 셀프서비스 / 광범위 접속 / 자원 풀링 / 신속 탄력성 / 측정 가능 서비스
3. IaaS — EC2, Azure VM, GCP Compute Engine, 가상 서버 제공
4. PaaS — Elastic Beanstalk, Heroku, Cloud Foundry, 플랫폼 제공
5. SaaS — Gmail, Salesforce, M365, 완성 소프트웨어
6. FaaS (Function as a Service) — AWS Lambda, Azure Functions, Cloud Run
7. CaaS (Container as a Service) — EKS, GKE, AKS
8. DBaaS (Database as a Service) — RDS, Aurora, Cloud SQL, Cosmos DB
9. STaaS (Storage as a Service) — S3, Azure Blob, GCS
10. AIaaS (AI as a Service) — OpenAI API, Vertex AI, Azure OpenAI
11. 퍼블릭 클라우드 — AWS / Azure / GCP / OCI / Alibaba Cloud
12. 프라이빗 클라우드 — 온프레미스, OpenStack, VMware vSAN
13. 하이브리드 클라우드 — AWS Outposts, Azure Arc, Anthos
14. 멀티 클라우드 — 복수 퍼블릭 활용, 벤더 종속 회피
15. 엣지 클라우드 — MEC, AWS Wavelength, Azure Edge Zones
16. 분산 클라우드 — GCP 분산 포드, 기술 주권 대응
17. 소버린 클라우드 (Sovereign Cloud) — 국가 규제 데이터 요건
18. 공동 책임 모델 (Shared Responsibility Model) — IaaS/PaaS/SaaS별 책임 분계
19. 클라우드 경제성 — OPEX 전환 / RI (예약) / Spot / Savings Plans
20. FinOps — 클라우드 비용 최적화, 엔지니어링+재무 협업
21. 클라우드 Well-Architected (AWS) — 6개 기둥 (운영우수/보안/신뢰성/성능효율/비용최적화/지속가능성)
22. Google Cloud Architecture Framework / Azure Well-Architected Framework

---

## 2. 가상화 / 컨테이너 / 오케스트레이션 — 28개

1. 서버 가상화 — Hypervisor Type1(ESXi/Hyper-V/Xen) / Type2(VMware)
2. KVM (Kernel-based VM) — 리눅스 모듈, QEMU, 클라우드 기반
3. vSphere (VMware ESXi) — vCenter, DRS, vMotion, HA
4. 마이크로VM — Firecracker (AWS Lambda), gVisor (Google) — 보안 + 경량
5. 컨테이너 (Docker) — 이미지/컨테이너/레이어/네임스페이스/cgroup
6. OCI (Open Container Initiative) — 이미지/런타임 표준
7. 컨테이너 런타임 — containerd / cri-o / runc / Podman
8. Kubernetes (k8s) 아키텍처 — Control Plane (API Server/etcd/Scheduler/Controller-Manager)
9. k8s 워커 노드 — kubelet / kube-proxy / Container Runtime
10. Pod / Deployment / ReplicaSet / StatefulSet / DaemonSet / Job / CronJob
11. Service (ClusterIP/NodePort/LoadBalancer/ExternalName) — 서비스 디스커버리
12. Ingress Controller — NGINX / Traefik / Envoy — L7 라우팅
13. Persistent Volume (PV) / PVC / StorageClass — 스테이트풀 스토리지
14. ConfigMap / Secret — 환경 설정 분리
15. HPA (Horizontal Pod Autoscaler) / VPA / KEDA — 자동 스케일링
16. Kubernetes Operator — CRD 기반 커스텀 컨트롤러
17. Helm Chart — 패키지 관리, 값 파일, 템플릿
18. GitOps — Argo CD / Flux — Git 상태 → 클러스터 동기화
19. Service Mesh — Istio / Linkerd / Consul Connect — sidecar Envoy, mTLS
20. eBPF 기반 네트워킹 — Cilium — Kubernetes 네트워크 고성능
21. CNI (Container Network Interface) — Flannel / Calico / Cilium / Weave
22. CSI (Container Storage Interface) — 스토리지 플러그인 표준
23. 멀티 클러스터 관리 — Rancher / ArgoCD ApplicationSet / KubeEdge
24. Kubernetes 보안 — RBAC / PodSecurityContext / NetworkPolicy / OPA Gatekeeper
25. Knative — 서버리스 워크로드 on Kubernetes
26. WASM / WASI on k8s — WebAssembly 런타임 컨테이너 대안
27. OpenShift (Red Hat) — 엔터프라이즈 Kubernetes 플랫폼
28. Tanzu (VMware) — VMware 기반 Kubernetes 관리

---

## 3. 서버리스 아키텍처 — 14개

1. 서버리스 (Serverless) 개념 — 서버 관리 추상화, 이벤트 기반 실행
2. FaaS 실행 모델 — Cold Start / Warm Start / Provisioned Concurrency
3. AWS Lambda — 15분 제한, 동시성, 계층(Layer)
4. Azure Functions — 소비 / 프리미엄 / 전용 플랜
5. Cloud Run (Google) — 컨테이너 기반 서버리스
6. Cloudflare Workers — 엣지 서버리스, V8 격리
7. 서버리스 프레임워크 — Serverless Framework / AWS SAM / CDK
8. 이벤트 소스 — S3 이벤트 / API GW / SQS / EventBridge / Kafka
9. Step Functions (AWS) — 서버리스 워크플로우 오케스트레이션
10. Cold Start 최적화 — 경량 런타임 / Provisioned / SnapStart (Lambda)
11. 서버리스 데이터베이스 — Aurora Serverless v2 / DynamoDB / Neon / PlanetScale
12. 서버리스 비용 모델 — 요청 수 × 실행 시간 × 메모리
13. 서버리스 보안 — 함수별 최소 IAM 권한, 환경 변수 암호화
14. 서버리스 모니터링 — AWS X-Ray / Lambda Power Tuning / Lumigo

---

## 4. 클라우드 네트워킹 — 20개

1. VPC (Virtual Private Cloud) — 논리 격리 네트워크, CIDR 블록 설계
2. 서브넷 설계 — 퍼블릭 / 프라이빗 / 격리 (DB) 계층
3. 인터넷 게이트웨이 / NAT 게이트웨이
4. VPC Peering / Transit Gateway — VPC 간 연결
5. AWS Direct Connect / Azure ExpressRoute / Cloud Interconnect — 전용선
6. CDN (Content Delivery Network) — CloudFront / Akamai / Fastly / Cloudflare
7. 글로벌 로드 밸런서 — AWS GLB / Azure Traffic Manager / GCP GCLB
8. Private Link / Private Endpoint — VPC 내 서비스 접근
9. 보안 그룹 (Security Group) / NACL — 인스턴스/서브넷 레벨 방화벽
10. AWS WAF / Azure Web Application Firewall — 애플리케이션 계층 보호
11. Shield (DDoS) — AWS Shield Standard/Advanced
12. Route 53 / Azure DNS — DNS 관리, 라우팅 정책
13. 서비스 디스커버리 — AWS Cloud Map / Consul / Eureka
14. API Gateway — AWS API GW / Azure API Management / Kong / Apigee
15. Service Mesh on Cloud — App Mesh (AWS) / Traffic Director (GCP)
16. 네트워크 ACL / 플로우 로그 — 감사, 트러블슈팅
17. SD-WAN + Cloud 통합 — SASE 아키텍처
18. IPv6 on Cloud — 이중 스택 지원, 주소 고갈 대응
19. 클라우드 네트워크 자동화 — Terraform / CDK / CloudFormation
20. PrivateLink Endpoint 비용 분석 — 데이터 전송 비용 최적화

---

## 5. 클라우드 스토리지 / 데이터베이스 — 22개

1. 객체 스토리지 (Object Storage) — S3 / Azure Blob / GCS, 무한 확장
2. S3 스토리지 클래스 — Standard / IA / Glacier / Intelligent Tiering
3. 블록 스토리지 — EBS (gp3/io2) / Azure Premium SSD / Persistent Disk
4. 파일 스토리지 — EFS / FSx (Windows/Lustre) / Azure Files / Filestore
5. 스토리지 티어링 — 핫/웜/콜드, ILM (Information Lifecycle Management)
6. RDS (Relational DB Service) — MySQL/PostgreSQL/MariaDB/Oracle/SQL Server
7. Aurora — 스토리지 자동 확장, 6-way 복제, Aurora Serverless v2
8. DynamoDB — NoSQL, 서버리스, 적응형 용량, 글로벌 테이블
9. Cosmos DB — 멀티모델, 99.999% SLA, 5가지 일관성 수준
10. Cloud Spanner — 글로벌 ACID + 수평 확장 (TRUE TIME)
11. Bigtable — HBase 호환, 대규모 시계열/IoT
12. Redis on Cloud — ElastiCache / Azure Cache / Memorystore
13. 데이터 마이그레이션 — DMS (AWS) / Database Migration Service (GCP)
14. Cross-Region Replication — 지역 간 복제, DR 전략
15. 스냅샷 / 백업 정책 — 자동화, PITR (Point-In-Time Recovery)
16. 데이터 레이크 on Cloud — S3 + Glue / ADLS Gen2 + Synapse / GCS + BigQuery
17. 데이터 웨어하우스 on Cloud — Redshift / Synapse Analytics / BigQuery / Snowflake
18. Snowflake 아키텍처 — 스토리지/컴퓨팅 분리, VPS, Time Travel
19. BigQuery — 서버리스 DW, 열 지향, 공개 데이터셋
20. 데이터 메시 on Cloud — Dataplex (GCP) / AWS Data Zones / Fabric (MS)
21. CloudFormation / Terraform / CDK — IaC 비교
22. 스토리지 비용 최적화 — S3 Intelligent Tiering, EBS 볼륨 타입 선택

---

## 6. 클라우드 보안 / IAM — 18개

1. IAM (Identity and Access Management) — 사용자/역할/정책/그룹
2. RBAC on Cloud — AWS IAM Policy / Azure RBAC / GCP IAM
3. 최소 권한 원칙 — IAM 정책 분석, AWS IAM Access Analyzer
4. 서비스 계정 (Service Account) — Pod Identity / Workload Identity
5. Multi-Account / 랜딩 존 (Landing Zone) — AWS Control Tower / Azure Landing Zone
6. SCP (Service Control Policy) — AWS Organizations 조직 수준 통제
7. KMS (Key Management Service) — CMK, 자동 로테이션, Envelope Encryption
8. CloudHSM — 전용 하드웨어 HSM
9. 시크릿 관리 — AWS Secrets Manager / Azure Key Vault / HashiCorp Vault
10. CSPM (Cloud Security Posture Management) — Prisma Cloud / Wiz / Orca
11. CWPP (Cloud Workload Protection Platform) — 컨테이너/VM 보호
12. CNAPP — CSPM + CWPP + CIEM 통합 (Wiz, Prisma)
13. CIEM (Cloud Infrastructure Entitlement Management) — 과도 권한 감지
14. 클라우드 감사 로그 — CloudTrail / Azure Monitor / Cloud Audit Logs
15. Security Hub / Defender for Cloud / Security Command Center — 통합 보안 대시보드
16. GuardDuty / Defender / SCC — 위협 탐지 서비스
17. IAM Assume Role / Cross-Account Access — 교차 계정 보안 접근
18. 제로 트러스트 on Cloud — BeyondCorp / AWS Verified Access

---

## 7. 클라우드 마이그레이션 / 운영 — 16개

1. 마이그레이션 전략 6R — Rehost / Replatform / Repurchase / Refactor / Retire / Retain
2. 리프트 앤 시프트 (Rehost) — 빠른 이전, 최적화 미흡
3. 리플랫폼 — RDS 전환, 일부 최적화
4. 리팩터 — 마이크로서비스, 컨테이너, 서버리스로 재설계
5. 마이그레이션 도구 — AWS MGN / DMS / Snowball / Azure Migrate
6. 클라우드 운영 체계 — CCoE (Cloud Center of Excellence)
7. 태그 전략 (Tagging) — 비용 배분, 자원 식별, 정책 적용
8. 클라우드 비용 관리 — Cost Explorer / Budgets / Cost Anomaly Detection
9. 예약 인스턴스 (RI) / Savings Plans / Spot Instance 비교
10. 자동 스케일링 — Auto Scaling Group / KEDA / HPA + Cluster Autoscaler
11. 멀티 AZ (Availability Zone) 설계 — 가용성 향상
12. 멀티 리전 설계 — DR, 데이터 주권, 글로벌 사용자 기반
13. CloudWatch / Azure Monitor / Cloud Monitoring — 메트릭/로그/알람
14. 비용 최적화 도구 — Compute Optimizer / Azure Advisor / GCP Recommender
15. 클라우드 거버넌스 — Policy as Code, OPA, Sentinel
16. 클라우드 폐기 (Cloud Exit Strategy) — 이식성 확보, 데이터 반환

---

## 8. 클라우드 네이티브 / 현대 아키텍처 — 16개

1. 클라우드 네이티브 (Cloud Native) — CNCF 정의, 컨테이너+마이크로서비스+DevOps
2. 마이크로서비스 아키텍처 (MSA) — 독립 배포, 서비스 경계, DB per service
3. API-First 설계 — OpenAPI 3.0, Design-First 개발
4. 이벤트 드리븐 아키텍처 (EDA) — 느슨한 결합, 비동기, Kafka/SNS/EventBridge
5. CQRS + Event Sourcing — 읽기/쓰기 분리, 이벤트 히스토리
6. Saga 패턴 — 분산 트랜잭션 조율 (Choreography / Orchestration)
7. 아웃박스 패턴 (Outbox Pattern) — 이중 쓰기 문제 해결
8. 서킷 브레이커 (Circuit Breaker) — Resilience4j / Hystrix, 장애 전파 차단
9. Bulkhead 패턴 — 실패 격리, 스레드 풀 분리
10. Retry / Timeout / Fallback — 복원력 패턴
11. BFF (Backend for Frontend) — 클라이언트별 최적 API
12. Strangler Fig 패턴 — 레거시 점진적 교체
13. 플랫폼 엔지니어링 (Platform Engineering) — IDP (Internal Developer Platform)
14. Backstage (Spotify) — 개발자 포털, 서비스 카탈로그
15. 골든 패스 (Golden Path) — 표준화된 개발·배포 경로
16. Software Supply Chain Security — SLSA 프레임워크, 서명된 빌드

---

**총 키워드 수: 156개**
