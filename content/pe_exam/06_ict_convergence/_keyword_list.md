+++
title = "06. ICT 융합기술 키워드 목록"
date = 2026-03-03
[extra]
categories = "pe_exam-ict"
+++

# ICT 융합기술 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 ICT 융합기술 전 영역 핵심 키워드

---

## 1. 클라우드 컴퓨팅 — 28개

1. 클라우드 컴퓨팅 (Cloud Computing) 정의 — NIST 5특성
2. NIST 5특성 — 온디맨드 셀프서비스/광범위 접속/자원 풀링/신속 탄력성/측정 가능 서비스
3. IaaS (Infrastructure as a Service) — EC2, Azure VM
4. PaaS (Platform as a Service) — AWS Elastic Beanstalk, Heroku
5. SaaS (Software as a Service) — Gmail, Salesforce, M365
6. FaaS (Function as a Service) — AWS Lambda, Azure Functions
7. CaaS (Container as a Service) — EKS, GKE, AKS
8. 퍼블릭 클라우드 — AWS / Azure / GCP / OCI
9. 프라이빗 클라우드 — 온프레미스, OpenStack
10. 하이브리드 클라우드 — 퍼블릭+프라이빗 통합
11. 멀티 클라우드 — 복수 퍼블릭 클라우드 사용
12. 클라우드 네이티브 — 마이크로서비스, 컨테이너, DevOps, CI/CD
13. 컨테이너화 — Docker, OCI 이미지
14. Kubernetes (k8s) — Pod/Service/Deployment/HPA, 오케스트레이션
15. 서비스 메시 (Service Mesh) — Istio, Linkerd, Envoy
16. API 게이트웨이 — Kong, AWS API GW, Apigee
17. 클라우드 스토리지 — 객체(S3)/블록(EBS)/파일(EFS)
18. CDN (Content Delivery Network) — CloudFront, Akamai, Fastly
19. 클라우드 데이터베이스 — RDS, Aurora, DynamoDB, Cosmos DB
20. 클라우드 보안 — IAM, 공동 책임 모델
21. 공동 책임 모델 (Shared Responsibility Model)
22. CSPM (Cloud Security Posture Management)
23. CASB (Cloud Access Security Broker)
24. FinOps — 클라우드 비용 최적화
25. 클라우드 RI/Spot — Reserved Instance, Spot Instance
26. 멀티 테넌시 (Multi-Tenancy) — 자원 공유, 격리
27. 클라우드 마이그레이션 전략 — 6R (Rehost/Replatform/Repurchase/Refactor/Retire/Retain)
28. 엣지 클라우드 (Edge Cloud) — MEC, AWS Outposts

---

## 2. 빅데이터 — 24개

1. 빅데이터 정의 — 3V (Volume/Velocity/Variety) → 5V (+Veracity/Value)
2. 빅데이터 수집 — 웹 크롤링, Kafka, Fluentd, Logstash
3. 빅데이터 저장 — HDFS (Hadoop Distributed File System)
4. Hadoop 생태계 — HDFS / MapReduce / YARN / Hive / Pig / HBase
5. MapReduce — Map(분산)/Reduce(집계), 분산 처리
6. Apache Spark — 인메모리 처리, RDD/DataFrame/Dataset, SparkML
7. Apache Kafka — 분산 메시지 큐, 스트리밍, 토픽/파티션/오프셋
8. Apache Flink — 이벤트 기반 스트리밍, 정확히 한 번(Exactly-once)
9. 람다 아키텍처 (Lambda Architecture) — 배치+스피드+서빙 레이어
10. 카파 아키텍처 (Kappa Architecture) — 스트리밍만으로 단순화
11. 데이터 레이크 (Data Lake) — S3, Azure Data Lake, ADLS
12. 레이크하우스 (Lakehouse) — Delta Lake, Apache Iceberg, Hudi
13. 데이터 파이프라인 — Apache Airflow, Prefect, dbt
14. 실시간 스트리밍 처리 — Kafka Streams, Samza, Storm
15. 데이터 시각화 — Tableau, Power BI, Grafana, Kibana
16. 데이터 마이닝 — 연관 규칙 (Apriori), 군집화, 분류
17. 연관 규칙 — 지지도(Support)/신뢰도(Confidence)/향상도(Lift)
18. 이상 탐지 (Anomaly Detection) — 통계/ML 기반
19. ETL vs ELT — Transform 위치 차이
20. Apache Iceberg / Delta Lake / Hudi — 오픈 테이블 포맷
21. 데이터 메시 (Data Mesh) — 도메인 소유권 분산
22. 빅데이터 보안 — 암호화, 마스킹, 접근 제어 (Ranger, Atlas)
23. 실시간 분석 DB — ClickHouse, Druid, Pinot
24. 데이터 거버넌스 도구 — Apache Atlas, Collibra, Alation

---

## 3. IoT (사물인터넷) — 20개

1. IoT (Internet of Things) 정의 및 아키텍처
2. IoT 계층 구조 — 인식/전송/서비스/응용 계층
3. 엣지 컴퓨팅 (Edge Computing) — 장치 단 데이터 처리
4. 포그 컴퓨팅 (Fog Computing) — 엣지와 클라우드 중간
5. IoT 플랫폼 — AWS IoT Core, Azure IoT Hub, Google Cloud IoT
6. 통신 프로토콜 — MQTT / CoAP / AMQP / HTTP / WebSocket
7. MQTT (Message Queuing Telemetry Transport) — Pub/Sub, 경량, QoS 0/1/2
8. CoAP (Constrained Application Protocol) — REST over UDP, IoT
9. 단거리 IoT 통신 — Bluetooth BLE / ZigBee / Z-Wave / RFID / NFC / UWB
10. 장거리 IoT 통신 (LPWAN) — LoRa, NB-IoT, LTE-M, Sigfox
11. 스마트홈 — Matter (구 Connected Home over IP), Thread
12. 산업용 IoT (IIoT) — OPC-UA, Modbus, PROFINET, EtherNet/IP
13. Industrial 4.0 — 스마트 팩토리, CPS, M2M
14. 디지털 트윈 (Digital Twin) — 물리 시스템의 가상 복제
15. 스마트 시티 (Smart City) — 교통/에너지/안전
16. 자율주행 V2X (Vehicle-to-Everything) — C-V2X, DSRC
17. 웨어러블 (Wearable) — 스마트워치, 헬스케어 IoT
18. IoT 보안 — 기기 인증, 펌웨어 업데이트, DTLS, PKI
19. OWASP IoT Top 10 취약점
20. 엣지 AI — TFLite, ONNX Runtime, CoreML, NPU

---

## 4. 보안 / 사이버보안 — 30개

1. 정보보안 3요소 — CIA (기밀성/무결성/가용성)
2. 보안 위협 — 악성코드/피싱/랜섬웨어/APT/내부자 위협
3. 악성코드 유형 — 바이러스/웜/트로이목마/랜섬웨어/스파이웨어/루트킷
4. APT (Advanced Persistent Threat) — 지속적 표적 공격
5. 랜섬웨어 (Ransomware) 공격 사례 및 대응
6. 피싱 / 스피어 피싱 / 웨일링 / 스미싱 / 비싱
7. 사회공학 공격 (Social Engineering)
8. 영지식 증명 (Zero-Knowledge Proof)
9. 대칭키 암호화 — AES-256 / DES / 3DES / ChaCha20
10. 비대칭키 암호화 — RSA / ECC (타원 곡선) / ElGamal
11. 해시 함수 — SHA-256 / SHA-3 / BLAKE2/3
12. 디지털 서명 — RSA-PSS, ECDSA, EdDSA
13. PKI (Public Key Infrastructure) — CA / RA / CRL / OCSP
14. 인증서 — X.509 v3, SAN, CT (Certificate Transparency)
15. 제로 트러스트 아키텍처 (Zero Trust Architecture, ZTA) — NIST SP 800-207
16. SASE (Secure Access Service Edge) — Gartner, 클라우드 기반 보안
17. ZTNA (Zero Trust Network Access) — SDP 기반 접근 제어
18. WAF (Web Application Firewall) — OWASP 룰셋
19. SIEM (Security Information Event Management) — Splunk, IBM QRadar
20. SOAR (Security Orchestration, Automation and Response)
21. EDR (Endpoint Detection and Response) — 단말 위협 탐지
22. XDR (Extended Detection and Response) — 통합 위협 대응
23. 취약점 관리 — CVE / CVSS / NVD / VPT
24. 침투 테스트 (Penetration Testing) — 방법론, 킬체인
25. MITRE ATT&CK 프레임워크 — 전술/기법/절차
26. OWASP Top 10 (2021) — Broken Access Control, Cryptographic Failures 등
27. DDoS 공격 / 방어 — SYN Flood, Amplification, Anycast, Scrubbing
28. 내부자 위협 (Insider Threat) — UBA/UEBA
29. 공급망 보안 (Supply Chain Security) — SolarWinds, Log4Shell
30. 컨피덴셜 컴퓨팅 (Confidential Computing) — Intel SGX, AMD SEV, TDX

---

## 5. 블록체인 — 16개

1. 블록체인 (Blockchain) 원리 — 분산 원장, 불변성, 합의
2. 합의 알고리즘 — PoW / PoS / DPoS / PBFT / Raft
3. PoW (Proof of Work) — 비트코인, 채굴, 에너지 소비
4. PoS (Proof of Stake) — 이더리움 Merge, 검증자
5. 스마트 컨트랙트 (Smart Contract) — 이더리움, Solidity
6. 이더리움 (Ethereum) — EVM, ERC-20/ERC-721, DeFi
7. 퍼블릭 블록체인 — 비트코인, 이더리움 — 완전 탈중앙
8. 프라이빗/컨소시엄 블록체인 — Hyperledger Fabric, Quorum
9. Hyperledger Fabric — 채널, 체인코드, MSP, CA
10. NFT (Non-Fungible Token) — ERC-721, 디지털 소유권
11. DeFi (Decentralized Finance) — DEX, Lending, Yield Farming
12. 탈중앙화 ID (DID, Decentralized Identity) — W3C 표준
13. 크로스체인 (Cross-Chain) — 브리지, IBC 프로토콜
14. 레이어 2 솔루션 — Lightning Network, Rollup (Optimistic/ZK)
15. Web3 — 탈중앙화 웹, DAO (Decentralized Autonomous Org)
16. CBDC (Central Bank Digital Currency) — 한국은행 디지털 원화

---

## 6. AI/ML 융합 — 20개

1. AI 융합 서비스 — AI 헬스케어, AI 제조, AI 금융
2. 디지털 트윈 + AI — 예측 유지보수, 시뮬레이션
3. 생성 AI (Generative AI) 산업 적용 — 콘텐츠/코드/설계
4. AI 반도체 — GPU/NPU/TPU/FPGA/ASIC
5. 온디바이스 AI (On-Device AI) — 스마트폰 NPU, 엣지
6. 추천 시스템 (Recommender System) — CF/CB/하이브리드
7. AI 기반 이상 탐지 — 금융사기, 네트워크 침입, 품질 불량
8. AIOps — AI 기반 IT 운영 자동화
9. MLOps — ML 파이프라인 자동화, 모델 모니터링
10. Explainable AI (XAI) — LIME, SHAP, 신뢰 가능 AI
11. AI 윤리 — 편향성, 공정성, 투명성, EU AI Act
12. LLM 기업 적용 — RAG, 챗봇, 코드 생성, 문서 요약
13. 컴퓨터 비전 산업 응용 — 품질 검사, 안면 인식, 의료 영상
14. NLP 산업 응용 — 감성 분석, 기계 번역, 계약서 분석
15. 자율주행 AI — L1~L5, CARLA, ADAS
16. 로봇 AI (Robotics AI) — 강화학습, 모션 플래닝
17. 의료 AI (Medical AI) — FDA 승인 AI, 영상 진단, DrugDiscovery
18. 금융 AI (FinAI) — 로보어드바이저, 알고트레이딩, AML
19. 스마트 제조 AI — 예지 정비, MES+AI, 품질4.0
20. AI 거버넌스 — NIST AI RMF, EU AI Act, OECD AI 원칙

---

## 7. XR / 메타버스 — 14개

1. AR (Augmented Reality) — 증강현실, ARKit, ARCore
2. VR (Virtual Reality) — 가상현실, Meta Quest, PCVR
3. MR (Mixed Reality) — 혼합현실, HoloLens, Magic Leap
4. XR (Extended Reality) — AR+VR+MR 총칭
5. 메타버스 (Metaverse) — 정의, 4요소 (경험/발견/창작자/공간컴퓨팅)
6. 공간 컴퓨팅 (Spatial Computing) — Apple Vision Pro
7. 디지털 트윈 메타버스 — NVIDIA Omniverse
8. Open XR 표준 — Khronos Group
9. WebXR — 브라우저 기반 XR
10. 햅틱 (Haptic Feedback) — 촉각 인터페이스
11. 아바타 (Avatar) — 정체성, 상호작용
12. NFT + 메타버스 — 디지털 자산, 소유권
13. 클라우드 렌더링 — 스트리밍 XR, NVIDIA CloudXR
14. 6DoF (Six Degrees of Freedom) — 위치/자세 추적

---

## 8. 핀테크 / 디지털 금융 — 16개

1. 핀테크 (FinTech) — 금융 + 기술 융합
2. 오픈뱅킹 (Open Banking) — API 개방, PSD2
3. 오픈 API — 계좌 조회/이체 API, 공동 결제 API
4. 간편 결제/간편 송금 — 카카오페이, 네이버페이, 토스
5. CBDC (Central Bank Digital Currency) — 한국, 중국, 바하마
6. 디지털 지갑 (Digital Wallet) — Apple Pay, Google Wallet
7. 로보어드바이저 (Robo-Advisor) — 알고리즘 자산 운용
8. 리걸테크 (LegalTech) — AI 계약서 분석
9. 레그테크 (RegTech) — 규제 자동화, KYC/AML
10. 보험테크 (InsurTech) — 디지털 보험, 텔레매틱스
11. 블록체인 금융 — DeFi, 스마트 컨트랙트, 토큰증권
12. Buy Now Pay Later (BNPL) — 후불 결제 서비스
13. 마이데이터 (MyData) — 개인신용정보 이동권
14. PCI DSS — 카드 결제 보안 표준
15. 금융 보안 — 이상거래탐지 (FDS), 생체 인증, 비밀번호리스
16. 오픈파이낸스 (Open Finance) — 마이데이터 확장, 종합 금융

---

## 9. 차세대 통신 / 5G 융합 — 14개

1. 5G 융합 서비스 — eMBB / URLLC / mMTC
2. eMBB (Enhanced Mobile Broadband) — 초고속, 대용량
3. URLLC (Ultra-Reliable Low Latency Communication) — 초저지연, 고신뢰
4. mMTC (Massive Machine-Type Communications) — 대규모 기기
5. 네트워크 슬라이싱 (Network Slicing) — 가상 전용망
6. MEC (Multi-access Edge Computing) — 5G 엣지 서버
7. C-RAN / O-RAN — 클라우드 기지국, 개방형
8. 5G 특화망 (Private 5G) — 스마트팩토리, 스마트항만
9. 위성 인터넷 — Starlink (LEO), OneWeb, 아리랑위성
10. 6G 연구 동향 — 테라헤르츠, AI 네이티브, 지능형 반사면 (RIS)
11. 양자 통신 (Quantum Communication) — QKD, 양자 암호
12. ISAC (Integrated Sensing and Communication) — 센싱+통신
13. V2X (Vehicle-to-Everything) — C-V2X, 자율주행 통신
14. 위성-5G 통합 (NTN, Non-Terrestrial Network)

---

## 10. 디지털 전환 (DX) / 최신 트렌드 — 18개

1. 디지털 전환 (Digital Transformation, DX) — 비즈니스 모델 혁신
2. 디지털 트윈 (Digital Twin) — 실시간 동기화, 예측
3. 스마트 팩토리 (Smart Factory) — AI+IoT+로봇+5G
4. 산업 인터넷 (Industrial Internet) — GE Predix
5. 사이버물리시스템 (CPS) — 물리세계+사이버세계 통합
6. 초연결사회 (Hyper-Connected Society) — IoT, 5G, AI 융합
7. 양자컴퓨팅 (Quantum Computing) — Qbit, 중첩·얽힘
8. 양자 우위 (Quantum Supremacy) — Google Sycamore
9. 양자 내성 암호 (PQC, Post-Quantum Cryptography) — NIST 표준화
10. 뉴로모픽 컴퓨팅 (Neuromorphic Computing) — Intel Loihi, IBM NS3e
11. 차세대 반도체 — 3D 낸드, GAA-FET, GAAFET, 2nm
12. 지속 가능한 ICT (Green ICT) — 탄소 중립, 에너지 효율
13. AI 탄소 발자국 — GPT-4 학습 CO₂, Green AI
14. 스마트 그리드 (Smart Grid) — AMI, ESS, 에너지 관리
15. 클라우드 지속 가능성 — RE100, PPA, 탄소 제로 데이터센터
16. GovTech — 정부 디지털 서비스, 전자정부
17. DataOps — 데이터 파이프라인 자동화, 품질
18. 생체 인증 (Biometric Authentication) — 지문/얼굴/홍채/정맥/행동

---

**총 키워드 수: 200개**
