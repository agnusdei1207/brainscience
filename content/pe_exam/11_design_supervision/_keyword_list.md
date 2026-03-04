+++
title = "11. 정보통신 설계·감리 키워드 목록"
date = 2026-03-03
[extra]
categories = "pe_exam-design-supervision"
+++

# 정보통신 설계·감리 키워드 목록

정보통신기술사 시험 **출제 비중 30~40%** 차지 — 기술사 수준 통합 설계·감리 핵심 키워드
> ⚡ "1000만원으로 대학 네트워크 구축"처럼 **현장 설계 판단·법적 요건·아키텍처 결정·비용 분석**을 통합한 문제 유형이 핵심

---

## 1. 정보통신 설계 법규·제도 — 20개

1. 정보통신공사업법 — 공사업 등록, 시공, 도급 제한
2. 정보통신공사 설계·감리 제도 — 의무 대상, 공사 규모
3. 정보통신기술자 — 자격 등급 (기술사/기사/산업기사/기능사), 배치 기준
4. 정보통신감리원 자격 — 기술사 취득 후 감리원 등록
5. 감리 의무 대상 — 1억원 이상 공사
6. 정보통신공사 발주 — 설계도서, 입찰, 계약, 착공, 준공
7. 정보통신 설비 기준 — KCS (Korean Construction Specification), KDS
8. 건축물 정보통신설비 기술 기준
9. 방송통신설비의 기술기준에 관한 규정
10. 전파법 — 주파수 분배, 기기 인증, 적합성 평가
11. 전기통신사업법 — 역무 분류, 망 개방, 번호 관리
12. 정보통신망법 — 보안 의무, 개인정보 보호, 침해 신고
13. 전자정부법 — 공공 정보시스템, 표준, 상호운용성
14. 개인정보보호법 — 처리 원칙, DPO, 영향평가
15. 소방법·건축법 연계 — 케이블 내화, 방화 구획 관통
16. 건축전기설비 설계 기준 — 케이블 트레이, 덕트
17. 물가 변동 조항 (ES) — 물가 상승 시 계약 금액 조정
18. 하자 보수 보증 — 공사 종류별 하자 기간
19. 사업수행계획서 (PMP) — 사업 관리 계획
20. PMO (Project Management Office) — 대형 프로젝트 관리 기관

---

## 2. 구내 정보통신 설비 설계 — 24개

1. 구내 정보통신 설비 — 구내 교환, LAN, 구내선, 구조 배선
2. 건물 정보통신 배선 체계 — EF→BDF/IDF→수평배선→TO
3. TIA-942 데이터센터 표준 — Tier 1~4
4. ANSI/TIA-568 — 구조화 배선 표준 (Cat6A/Cat7/Cat8/광섬유)
5. 수평 배선 (Horizontal Cabling) — TO ↔ IDF, 90m 이내
6. 수직 배선 (Backbone Cabling) — 층간, IDF ↔ MDF
7. TO (Telecommunication Outlet) — 사용자 접점 잭
8. IDF (Intermediate Distribution Frame) — 층 배선반
9. MDF (Main Distribution Frame) — 건물 중앙 배선반
10. 구내 광섬유 — OM3/OM4/OM5 (다중모드), OS1/OS2 (단일모드)
11. Cat6 vs Cat6A vs Cat7 — 주파수/전송거리/노이즈 차이
12. PoE (Power over Ethernet) — IEEE 802.3af/at/bt, 최대 90W
13. 구내 무선 설계 — AP 배치 계획, 채널 계획, 커버리지 모델
14. 무선 사이트 서베이 — Ekahau, 전파 측정, 간섭 분석
15. 인터폰 / 원격화상 — 비디오 인터폰, IP 인터폰
16. CCTV 설계 — 해상도/화각/야간/저장 용량 계산
17. IP CCTV — NVR, H.265 압축, 비트레이트 설계
18. 출입통제 시스템 — 카드/생체 복합 인증
19. 방송 설비 — IP 방송, 스피커 배치 계획
20. 빌딩 자동화 (BAS/BMS) — 공조/조명/보안 통합
21. SMARTBldg / 제로에너지 건축물 — IBS (지능형 건축물)
22. 데이터센터 설계 — 전력/냉각/케이블 3요소 통합
23. UPS (무정전 전원 장치) — 용량 계산, 배터리 수명
24. 접지 (Grounding) 설계 — 기기 접지, TN-S 계통

---

## 3. 네트워크 인프라 설계 — 28개

1. 네트워크 설계 방법론 — 요구분석 → 논리 설계 → 물리 설계 → 구현 → 검증
2. PPDIOO (Prepare/Plan/Design/Implement/Operate/Optimize) — Cisco 방법론
3. 3계층 설계 (3-Tier) — 코어 / 분배 / 액세스 계층 (전통적)
4. 2계층 리프-스파인 (Leaf-Spine) — 데이터센터, 등지연 경로
5. 코어 스위치 (Core Switch) — 고속 라우팅, 이중화 필수
6. 분배 스위치 (Distribution Switch) — 정책 적용, 집선
7. 액세스 스위치 (Access Switch) — 단말 연결, PoE
8. 스위치 이중화 — VSS / vPC / MC-LAG / PVST+ / MSTP
9. 라우터 이중화 — HSRP / VRRP / GLBP (Gateway redundancy)
10. 링크 이중화 — LACP / 802.3ad (LACP 포트 채널)
11. 서버 이중화 — NIC Teaming, Bonding (Active/Active, Active/Standby)
12. STP (Spanning Tree Protocol) — 루프 방지, RSTP/MSTP로 대체
13. VLAN 설계 — 업무별 분리, 라우팅 간 격리
14. 라우팅 프로토콜 선택 — OSPF (내부) vs BGP (외부 연동)
15. SD-WAN 설계 — 다중 회선, QoS 정책, 중앙 관리
16. 네트워크 주소 계획 — IP 블록 할당, VLSM, IPv6 전환
17. DNS 설계 — 내부/외부 스플릿, 재귀/권한 서버 분리
18. DHCP 설계 — 범위, 임대 시간, 이중화 (DHCP Failover)
19. NTP 계층 — Stratum 0/1/2, 시간 동기화 정책
20. 대역폭 계획 (Bandwidth Planning) — 사용자 수 × 최대 사용량 × 부하율
21. QoS 설계 — DSCP 마킹, 대역폭 보장, 우선순위 큐
22. 보안 아키텍처 통합 — 방화벽 존 설계, DMZ, ACL
23. NAT 설계 — PAT, 1:1 NAT, 설계 고려사항
24. VPN 설계 — Site-to-Site (IPsec) / Remote Access (SSL/WireGuard)
25. 무선 컨트롤러 (WLC) 아키텍처 — 중앙집중형 vs 분산형
26. 802.1X 네트워크 인증 — RADIUS, EAP, 포스처 검사
27. 네트워크 관리 시스템 (NMS) — SNMP v3, NETCONF/YANG
28. 네트워크 자동화 — Ansible / Terraform / Python + NAPALM

---

## 4. 서버·스토리지 인프라 설계 — 22개

1. 서버 유형 — 타워 / 랙 / 블레이드 / 모듈러 / 슈퍼서버
2. 서버 사양 계획 — CPU (소켓·코어·클럭) / 메모리 / 스토리지 / NIC
3. x86 서버 — Intel Xeon Scalable / AMD EPYC
4. ARM 서버 — AWS Graviton / Ampere Altra — 에너지 효율
5. 용량 계획 (Capacity Planning) — CPU/메모리/스토리지/네트워크 예측
6. 서버 클러스터링 — HA 클러스터, 페일오버 클러스터링
7. 로드 밸런싱 — L4 (IP/포트) / L7 (URL/쿠키), HAProxy, NGINX, F5
8. 스토리지 유형 — DAS / NAS / SAN / 오브젝트 스토리지
9. SAN (Storage Area Network) — FC SAN / iSCSI / FCoE
10. NAS (Network Attached Storage) — SMB / NFS / AFP
11. 오브젝트 스토리지 — S3 호환, 비정형 데이터, 무한 확장
12. RAID 구성 설계 — 성능 vs 신뢰성 요구별 RAID 0/1/5/6/10 선택
13. SSD vs HDD — Tiering 전략, 핫/웜/콜드 데이터
14. NVMe-oF (NVMe over Fabrics) — 초저지연 스토리지 패브릭
15. 스토리지 이중화 — DRBD, SnapMirror, Active-Active
16. 백업 설계 — 3-2-1 규칙, RTO/RPO 계산, 백업 윈도우
17. 스냅샷 (Snapshot) vs 복제 (Replication) 차이
18. 재해복구 (DR) 사이트 — Hot/Warm/Cold, RTO/RPO 기반 선택
19. 가상화 인프라 — VMware vSphere / Hyper-V / KVM + oVirt
20. HCI (Hyper-Converged Infrastructure) — Nutanix, vSAN
21. 서버실 환경 — 온도 (18~27℃), 습도 (40~60%), 소화, 접지
22. PUE (Power Usage Effectiveness) — 에너지 효율 지표, 최적: 1.0

---

## 5. 데이터센터 설계 — 18개

1. 데이터센터 티어 (Tier) 분류 — Tier 1(99.67%) ~ Tier 4(99.9999%)
2. TIA-942 — 사이트 인프라 표준, 설비 요건
3. Uptime Institute 인증 — Tier 1~4 독립 인증
4. 전력 설계 — UPS / PDU / 이중화 (2N/N+1), kW 밀도
5. 전력공급 이중화 — 2N 배전, ATS (Auto Transfer Switch)
6. 발전기 (Generator) — 연료 공급, 자동 기동, 전환 시간
7. 냉각 시스템 — CRAC / CRAH / 공냉 / 액냉 / 침수냉각
8. 액침 냉각 (Immersion Cooling) — 전도성 액체, PUE 1.03
9. 직접 액체 냉각 (DLC) — 서버 내 액냉 코일
10. 핫 아일/콜드 아일 분리 — Hot Aisle Containment (HAC)
11. 데이터센터 네트워크 — 코어-TOR 구조, BGP ECMP
12. 데이터센터 상호 연결 (DCI) — DWDM, 다크 파이버, SD-DCI
13. 케이블 관리 — 케이블 트레이, 표지, 색별 구분
14. 화재 감지/진압 — VESDA, 하론 대체 (FM-200, NOVEC 1230)
15. 물리 보안 — 맨트랩, 생체 인식, CCTV, 카드키
16. DCIM (Data Center Infrastructure Management) — 실시간 자원 가시성
17. 지속 가능한 데이터센터 — RE100, 탄소 중립, 폐열 재활용
18. 모듈형 데이터센터 — 컨테이너 DC, 신속 구축

---

## 6. 용량·성능 계획 (Capacity/Performance Planning) — 16개

1. 용량 계획 방법론 — 현황 분석 → 수요 예측 → 갭 분석 → 도입 계획
2. 트래픽 모델링 — Erlang B/C (전화), Poisson (데이터), 피크 시간 측정
3. 얼랑 B (Erlang B) — 차단 확률, 회선 수 계산 (트래픽 설계 필수)
4. 얼랑 C (Erlang C) — 대기 큐 포함, 호출 센터 설계
5. 서버 CPU 용량 — 동시 사용자 × OPS × 트랜잭션 시간
6. 메모리 용량 계획 — RSS + Cache + OS 오버헤드
7. 스토리지 용량 계획 — 원본 × 증가율 × 복제 × 백업 비율
8. 네트워크 대역폭 계획 — 최대 동시 사용자 × 1인당 대역폭 × 부하율 (0.7~0.8)
9. QoS 기반 대역폭 배분 — 보장 (GBR) vs 비보장 (NGBR)
10. 성능 지표 — TPS / QPS / IOPS / Latency / Throughput
11. 성능 테스트 — 부하/스트레스/내구성/스파이크 (JMeter, k6, Locust)
12. 병목 분석 (Bottleneck Analysis) — CPU/메모리/Disk I/O/네트워크
13. Amdahl's Law — 병렬화 스피드업 한계
14. Little's Law — L = λ × W (큐잉 이론)
15. SLA 정의 — 가용성/응답시간/처리량 목표 수치화
16. 베이스라인 측정 — 정상 상태 기준 지표 수집

---

## 7. 정보통신 설계·제안서 작성 — 14개

1. 제안요청서 (RFP, Request for Proposal) 분석
2. 제안서 구성 — 이해도 / 방법론 / 기술력 / 일정 / 비용
3. 개념 설계 (Conceptual Design) — 큰 그림, 기술 방향 결정
4. 기본 설계 (Basic Design) — 시스템 구성도, 주요 사양
5. 상세 설계 (Detailed Design) — 도면, 시방서, 수량 산출
6. WBS (Work Breakdown Structure) — 업무 분해 구조
7. 네트워크 구성도 (NW Diagram) — 논리 구성도 / 물리 구성도
8. 시스템 구성도 — 서버/스토리지/SW 배치
9. 수량 산출서 — 물량 내역, 단가 산출
10. 공사 시방서 (Specification) — 자재/공법/품질 기준
11. 인터페이스 정의서 (ICD) — 시스템 간 연동 명세
12. 시험 및 검증 계획 (Test Plan) — FAT / SAT / UAT
13. 준공도서 — As-Built 도면, 시험 성적서, 운영 매뉴얼
14. PM (Project Management) 도구 — MS Project / JIRA / Smartsheet

---

## 8. 감리 업무 — 16개

1. 정보통신 감리 목적 — 공사 품질 확보, 발주자 보호
2. 감리 단계 — 설계감리 / 공사감리 (착공전/시공중/준공)
3. 감리원 역할 — 기술 검토, 품질 검사, 공정 관리
4. 착공 전 검토 — 설계 도서 검토, 사전 협의
5. 시공 중 감리 — 자재 검수, 시공 확인, 품질 시험
6. 준공 감리 — 시운전, 성능 시험, 준공 도서 확인
7. 공정 관리 — S-Curve, CPM, 공정률 확인
8. 품질 관리 (QC) — ITP (Inspection & Test Plan), 체크리스트
9. 안전 관리 — 산업안전보건법, 안전 점검
10. 지적 사항 처리 — 시정 요구, 재시공 지시, 이행 확인
11. 감리 보고서 — 주간/월간/준공 감리 보고서
12. 기술 검토 의견서 (RFI) — 설계 불명확 시 발주자 질의
13. 성능 검사 — 네트워크 측정 (iPerf3), 광손실 측정 (OTDR)
14. OTDR (Optical Time Domain Reflectometer) — 광섬유 장애점 탐지
15. 네트워크 검수 — RFC 2544 (기가비트 성능 시험)
16. 하자 검사 — 하자 기간 내 이행 확인

---

## 9. 비용 분석 / 경제성 평가 — 12개

1. 비용 편익 분석 (CBA, Cost-Benefit Analysis)
2. TCO (Total Cost of Ownership) — 초기 비용 + 운영 비용 + 폐기 비용
3. ROI (Return on Investment) = (편익 - 비용) / 비용 × 100%
4. NPV (Net Present Value) — 현재 가치 기준 편익-비용
5. IRR (Internal Rate of Return) — NPV=0 이 되는 할인율
6. 경제적 내용연수 — 기술 교체 주기 고려
7. 공사비 산정 — 직접비 + 간접비 (일반관리비 + 이윤)
8. 제경비 산출 — 기술료, 안전관리비, 산재보험료
9. 가성비 분석 — 기가비트 당 비용, 사용자당 비용
10. 시나리오 분석 — 낙관/기준/비관 시나리오
11. 민감도 분석 — 핵심 변수 변화 시 결과 영향
12. 조달 방식 — 직접 구매 / 렌탈 / 운용 리스 / 클라우드 전환

---

**총 키워드 수: 170개**
