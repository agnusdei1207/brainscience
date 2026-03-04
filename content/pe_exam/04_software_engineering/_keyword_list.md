+++
title = "04. 소프트웨어공학 키워드 목록"
date = 2026-03-03
[extra]
categories = "pe_exam-se"
+++

# 소프트웨어공학 (Software Engineering) 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 소프트웨어공학 전 영역 핵심 키워드

---

## 1. SW 공학 기초 / 프로세스 — 20개

1. 소프트웨어 공학 (Software Engineering) 정의 및 목표
2. 소프트웨어 위기 (Software Crisis)
3. SDLC (Software Development Life Cycle) — 요구→설계→구현→시험→유지보수
4. 폭포수 모델 (Waterfall Model) — 순차적, 단계별 산출물
5. V 모델 (V-Model) — 개발-검증 연계, 각 단계별 테스트
6. 프로토타입 모델 (Prototype Model) — 요구 명확화
7. 나선형 모델 (Spiral Model) — 위험 분석 기반, Boehm
8. 반복적 개발 (Iterative Development)
9. 점진적 개발 (Incremental Development)
10. RAD (Rapid Application Development)
11. 소프트웨어 프로세스 성숙도
12. CMMI (Capability Maturity Model Integration) — ML1~ML5
13. ISO/IEC 12207 — 소프트웨어 생명주기 프로세스
14. ISO/IEC 15504 (SPICE) — 프로세스 역량 평가
15. 소프트웨어 형상 관리 (SCM) — 버전 관리, 변경 통제
16. 형상 항목 (Configuration Item) — 기준선 (Baseline)
17. 변경 관리 (Change Management) — CCB (변경 통제 위원회)
18. CMMi 레벨 — 초기/관리됨/정의됨/정량 관리됨/최적화
19. PSP (Personal Software Process) — 개인 수준 프로세스
20. TSP (Team Software Process) — 팀 수준 프로세스

---

## 2. 애자일 (Agile) — 24개

1. 애자일 선언 (Agile Manifesto) — 4가지 가치, 12원칙
2. 스크럼 (Scrum) — 스프린트, 백로그, 데일리 스탠드업
3. 스프린트 (Sprint) — 2~4주 이터레이션
4. 제품 백로그 (Product Backlog) — 사용자 스토리 우선순위
5. 스프린트 백로그 (Sprint Backlog)
6. 번다운 차트 (Burndown Chart)
7. 스크럼 마스터 / 제품 오너 / 개발팀
8. 데일리 스크럼 (Daily Scrum) — 어제/오늘/장애요인
9. 스프린트 리뷰 (Sprint Review) — 데모
10. 스프린트 레트로스펙티브 (Sprint Retrospective) — 개선
11. XP (eXtreme Programming) — TDD, 페어 프로그래밍, 지속 통합
12. 테스트 주도 개발 (TDD, Test-Driven Development) — Red-Green-Refactor
13. 페어 프로그래밍 (Pair Programming)
14. 지속 통합 (CI, Continuous Integration)
15. 칸반 (Kanban) — 흐름 기반, WIP 제한
16. Lean Software Development — 7가지 원칙, 낭비 제거
17. SAFe (Scaled Agile Framework) — 대규모 애자일
18. LeSS (Large-Scale Scrum) — 다중 팀 스크럼
19. Nexus — 3~9팀 스크럼 확장
20. 속도 (Velocity) — 스프린트별 완료 스토리 포인트
21. 에픽 (Epic) / 사용자 스토리 (User Story) / 태스크 (Task)
22. 인수 기준 (Acceptance Criteria)
23. DoD (Definition of Done)
24. WIP (Work In Progress) 제한 — 칸반 핵심

---

## 3. 요구공학 (Requirements Engineering) — 18개

1. 요구공학 개요 — 도출/분석/명세/검증/관리
2. 기능 요구사항 (Functional Requirements)
3. 비기능 요구사항 (Non-Functional Requirements) — 성능/보안/가용성
4. 요구사항 도출 — 인터뷰, 관찰, 프로토타입, 브레인스토밍, JAD
5. 유스케이스 (Use Case) — 액터, 기본/대안/예외 흐름
6. 사용자 스토리 (User Story) — As a / I want / So that
7. SRS (Software Requirements Specification) — IEEE 830
8. 요구사항 추적 행렬 (RTM, Requirements Traceability Matrix)
9. 요구사항 검증 — 리뷰, 프로토타이핑, 모델 검증
10. 기능점수 (Function Point, FP) — IFPUG, NESMA
11. Use-Case Point (UCP) — 유스케이스 기반 규모 산정
12. 스토리 포인트 (Story Point) — 상대적 규모 추정
13. 와이드밴드 델파이 (Wideband Delphi) — 그룹 추정
14. COCOMO (Constructive Cost Model) — 기본/중간/고급
15. 프로젝트 규모 측정 — LOC, FP, UCP
16. 이해관계자 분석 (Stakeholder Analysis)
17. 요구사항 우선순위 — MoSCoW (Must/Should/Could/Won't)
18. 요구사항 변경 영향 분석

---

## 4. 소프트웨어 설계 — 26개

1. 설계 원칙 — SOLID (SRP/OCP/LSP/ISP/DIP)
2. 단일 책임 원칙 (SRP)
3. 개방-폐쇄 원칙 (OCP)
4. 리스코프 치환 원칙 (LSP)
5. 인터페이스 분리 원칙 (ISP)
6. 의존성 역전 원칙 (DIP)
7. DRY (Don't Repeat Yourself) / YAGNI / KISS
8. 모듈화 (Modularity) — 결합도/응집도
9. 응집도 (Cohesion) 유형 — 기능/순차/절차/교환/시간/논리/우연
10. 결합도 (Coupling) 유형 — 내용/공통/제어/스탬프/자료
11. 추상화 (Abstraction) / 캡슐화 / 상속 / 다형성
12. 계층형 아키텍처 (Layered Architecture)
13. MVC (Model-View-Controller) 패턴
14. MVP / MVVM — 프론트엔드 아키텍처 패턴
15. 마이크로서비스 아키텍처 (MSA)
16. 이벤트 드리븐 아키텍처 (EDA)
17. CQRS (Command Query Responsibility Segregation)
18. 헥사고날 아키텍처 (Hexagonal / Ports and Adapters)
19. 클린 아키텍처 (Clean Architecture) — Robert C. Martin
20. 도메인 주도 설계 (DDD, Domain-Driven Design) — 바운디드 컨텍스트, 애그리게이트
21. UML (Unified Modeling Language) — 구조/행위 다이어그램
22. 클래스 다이어그램 — 연관/집합/합성/의존성/상속
23. 시퀀스 다이어그램 — 객체 간 메시지 순서
24. 상태 다이어그램 — 상태 전이
25. 액티비티 다이어그램 — 흐름 제어
26. 컴포넌트/배포 다이어그램 — 물리적 구조

---

## 5. 디자인 패턴 (Design Patterns) — 24개

1. GoF 디자인 패턴 23가지 — 생성/구조/행위
2. 생성 패턴 (Creational) — 객체 생성 메커니즘
3. 싱글톤 (Singleton) — 단일 인스턴스
4. 팩토리 메서드 (Factory Method)
5. 추상 팩토리 (Abstract Factory)
6. 빌더 (Builder)
7. 프로토타입 (Prototype)
8. 구조 패턴 (Structural) — 클래스/객체 구성
9. 어댑터 (Adapter) — 호환 인터페이스
10. 브리지 (Bridge) — 추상/구현 분리
11. 컴포지트 (Composite) — 트리 구조
12. 데코레이터 (Decorator) — 동적 기능 추가
13. 퍼사드 (Facade) — 복잡 시스템 단순 인터페이스
14. 플라이웨이트 (Flyweight) — 공유를 통한 메모리 효율
15. 프록시 (Proxy) — 대리 객체
16. 행위 패턴 (Behavioral)
17. 옵서버 (Observer) — 이벤트 알림
18. 전략 (Strategy) — 알고리즘 교체 가능
19. 커맨드 (Command) — 요청 캡슐화
20. 템플릿 메서드 (Template Method) — 골격 알고리즘
21. 이터레이터 (Iterator) — 순차 접근
22. 스테이트 (State) — 상태별 행위
23. 책임 연쇄 (Chain of Responsibility)
24. 미디에이터 (Mediator) — 객체 간 통신 중재

---

## 6. 소프트웨어 테스팅 — 22개

1. 소프트웨어 테스트 목표 — 결함 발견, 신뢰성 확인
2. 테스트 레벨 — 단위(Unit) / 통합(Integration) / 시스템(System) / 인수(Acceptance)
3. 단위 테스트 (Unit Test) — 모듈별, Mock 객체
4. 통합 테스트 — 빅뱅 / 하향식 / 상향식 / 샌드위치
5. 시스템 테스트 — 기능/성능/보안/호환성
6. UAT (User Acceptance Testing) — 사용자 인수
7. 회귀 테스트 (Regression Test) — 수정 후 재검증
8. 블랙박스 테스트 — 동등 분할, 경계값 분석, 원인-결과
9. 동등 분할 (Equivalence Partitioning)
10. 경계값 분석 (Boundary Value Analysis)
11. 화이트박스 테스트 — 문장/분기/조건/경로 커버리지
12. 구문 커버리지 (Statement Coverage)
13. 분기 커버리지 (Branch Coverage)
14. 조건 커버리지 (Condition Coverage)
15. MC/DC (Modified Condition/Decision Coverage) — 항공/안전 결정적
16. 경로 커버리지 (Path Coverage)
17. 퍼즈 테스팅 (Fuzz Testing / Fuzzing)
18. 돌연변이 테스팅 (Mutation Testing)
19. TDD (Test-Driven Development) — Red-Green-Refactor
20. BDD (Behavior-Driven Development) — Given-When-Then
21. 성능 테스트 — 부하(Load)/스트레스(Stress)/내구성(Soak)/스파이크(Spike)
22. 정적 분석 (Static Analysis) — SAST, 코드 리뷰, SonarQube

---

## 7. 소프트웨어 유지보수 / 품질 — 16개

1. 소프트웨어 유지보수 유형 — 수정/개선/적응/예방
2. 소프트웨어 품질 모델 — ISO/IEC 25010 (SQuaRE)
3. ISO/IEC 25010 특성 — 기능성/성능효율성/호환성/사용성/신뢰성/보안성/유지보수성/이식성
4. 맥콜 품질 모델 (McCall Model)
5. 기술 부채 (Technical Debt) — 단기 편의 vs 장기 비용
6. 리팩토링 (Refactoring) — 외부 동작 유지, 내부 구조 개선
7. 코드 냄새 (Code Smell) — 중복/긴 메서드/신의 클래스
8. 소프트웨어 재공학 (Software Re-engineering)
9. 역공학 (Reverse Engineering)
10. 정방향 공학 (Forward Engineering)
11. 소프트웨어 마이그레이션 — 레거시 현대화
12. 결함 밀도 (Defect Density) — 결함 수 / LOC
13. SLA (Service Level Agreement) — 가용성, MTTR, MTBF
14. MTBF (Mean Time Between Failures) — 신뢰성 지표
15. MTTR (Mean Time to Repair) — 회복성 지표
16. RTO / RPO — 재해 복구 목표

---

## 8. DevOps / CI/CD — 20개

1. DevOps 개념 — 개발+운영 통합, 문화/자동화/측정
2. CI (Continuous Integration) — 자동 빌드/테스트
3. CD (Continuous Delivery) — 자동 배포 준비
4. CD (Continuous Deployment) — 자동 프로덕션 배포
5. Pipeline as Code — Jenkinsfile, GitHub Actions, GitLab CI
6. 컨테이너 기반 배포 — Docker, Kubernetes
7. 블루/그린 배포 (Blue/Green Deployment)
8. 카나리 배포 (Canary Deployment)
9. 롤링 업데이트 (Rolling Update)
10. 피처 플래그 (Feature Flag / Feature Toggle)
11. GitOps — Git 기반 인프라 선언, Argo CD, Flux
12. Infrastructure as Code (IaC) — Terraform, Ansible, Pulumi
13. 불변 인프라 (Immutable Infrastructure)
14. 관찰가능성 (Observability) — 로그/메트릭/추적 (Logs/Metrics/Traces)
15. 분산 추적 (Distributed Tracing) — Jaeger, Zipkin, OpenTelemetry
16. 알람 및 모니터링 — Prometheus, Grafana, ELK Stack
17. SRE (Site Reliability Engineering) — 에러 예산, SLI/SLO/SLA
18. 카오스 엔지니어링 (Chaos Engineering) — Chaos Monkey
19. 보안 DevOps (DevSecOps) — SAST/DAST/SCA 통합
20. Value Stream Mapping — 낭비 식별, 흐름 최적화

---

## 9. SW 보안 / 안전 — 14개

1. 시큐어 코딩 (Secure Coding) — OWASP Top 10, CWE
2. OWASP Top 10 — Injection, XSS, CSRF, SSRF, 취약한 인증 등
3. SQL 인젝션 (SQL Injection) — 파라미터화 쿼리, ORM
4. XSS (Cross-Site Scripting) — 입력 검증, CSP
5. CSRF (Cross-Site Request Forgery) — CSRF 토큰
6. 인증 (Authentication) — MFA, OAuth 2.0, JWT
7. 인가 (Authorization) — RBAC, ABAC, 최소 권한
8. 취약점 관리 — CVE, CVSS 점수
9. 정적 분석 (SAST) — Checkmarx, SonarQube
10. 동적 분석 (DAST) — OWASP ZAP, Burp Suite
11. SCA (Software Composition Analysis) — 오픈소스 취약점
12. SBOM (Software Bill of Materials) — 공급망 보안
13. 암호화 — TLS, AES, RSA, 키 관리
14. 소프트웨어 공급망 보안 — SolarWinds 교훈, 서명 검증

---

## 10. 프로젝트 관리 — 18개

1. 프로젝트 관리 (PM) — PMBOK 10대 지식 영역
2. WBS (Work Breakdown Structure)
3. CPM (Critical Path Method) — 주경로, 최장 경로
4. PERT (Program Evaluation and Review Technique) — 확률적 일정
5. 간트 차트 (Gantt Chart) — 일정 시각화
6. EVM (Earned Value Management) — PV/EV/AC, CPI/SPI
7. CPI (Cost Performance Index) / SPI (Schedule Performance Index)
8. 위험 관리 (Risk Management) — 식별/분석/대응/모니터링
9. 위험 대응 전략 — 회피/전가/완화/수용
10. 품질 관리 (Quality Management) — QA vs QC
11. 조달 관리 (Procurement Management)
12. 이해관계자 관리 (Stakeholder Management)
13. 의사소통 관리 — 의사소통 계획
14. SW 비용 추정 — COCOMO / FP / Delphi
15. 프로젝트 포트폴리오 관리 (PPM)
16. OKR (Objectives and Key Results) — 목표 관리
17. KPI (Key Performance Indicator)
18. 세 가지 제약 (Triple Constraint) — 범위/시간/비용

---

**총 키워드 수: 202개**
