+++
weight = 347
title = "347. CMMI 성숙도 5단계 SPICE 비교 (CMMI Maturity Model SPICE)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: CMMI(Capability Maturity Model Integration)는 소프트웨어 개발 조직의 프로세스 성숙도를 5단계로 측정하며, SPICE(Software Process Improvement and Capability dEtermination, ISO/IEC 15504)는 개별 프로세스 역량을 0~5단계로 측정하는 국제 표준이다.
> 2. **가치**: 두 모델 모두 조직의 프로세스 약점을 진단하고 단계적 개선 로드맵을 제공하며, 공공·국방 프로젝트 수주 요건이나 글로벌 소프트웨어 조달 기준으로 활용된다.
> 3. **판단 포인트**: CMMI는 조직 수준 평가(1~5), SPICE(VDA Automotive SPICE 포함)는 프로세스 수준 평가(0~5)로 적용 목적이 다르며, 자동차·금융 산업은 Automotive SPICE가 사실상 표준이다.

## Ⅰ. 개요 및 필요성

1980년대 미국 국방부(DoD)는 소프트웨어 프로젝트 실패율이 높아 카네기멜론 대학교(CMU) SEI(Software Engineering Institute)에 소프트웨어 품질 평가 모델 개발을 의뢰했다. 이를 통해 CMM(1991) → CMMI(2002, SEI) → CMMI v2.0(2018, ISACA)으로 진화했다.

SPICE(ISO/IEC 15504)는 1990년대 국제 표준화기구(ISO)가 각국 CMM 변형 모델을 통합하기 위해 개발한 프로세스 역량 프레임워크로, ISO/IEC 33000 시리즈로 업그레이드되었다. 특히 자동차 산업에서는 VDA(독일 자동차산업협회)가 개발한 Automotive SPICE(ASPICE)가 Tier-1 공급업체 평가 표준으로 자리잡았다.

📢 **섹션 요약 비유**: CMMI와 SPICE는 학교 성적표처럼, 조직/프로세스가 얼마나 성숙하게 소프트웨어를 개발하는지 객관적으로 등급을 매기는 도구다.

## Ⅱ. 아키텍처 및 핵심 원리

### CMMI 5단계 성숙도 모델

```
레벨 5 최적화 (Optimizing)
 │  정량적 데이터 기반 지속적 프로세스 혁신
 │  혁신 관리, 결함 원인 분석·해결
 │
레벨 4 정량적 관리 (Quantitatively Managed)
 │  프로세스 성과를 통계적으로 측정·통제
 │  정량적 PM, 조직 프로세스 성과 관리
 │
레벨 3 정의됨 (Defined)
 │  조직 표준 프로세스 정의, 전사 표준화
 │  요구사항 개발, 기술 솔루션, 검증, 확인
 │
레벨 2 관리됨 (Managed)
 │  프로젝트별 프로세스 계획·추적
 │  요구사항 관리, 프로젝트 모니터링
 │
레벨 1 초기 (Initial)
   임시 방편, 혼돈, 영웅적 노력에 의존
   성공이 개인 역량에 좌우
```

### SPICE (ISO/IEC 15504) 프로세스 역량 레벨

| 레벨 | 명칭 | 설명 |
|:---|:---|:---|
| 0 | Incomplete | 프로세스 미구현 또는 목적 미달성 |
| 1 | Performed | 프로세스 수행, 산출물 존재 |
| 2 | Managed | 계획·모니터링, 산출물 관리 |
| 3 | Established | 표준 프로세스 정의·배포 |
| 4 | Predictable | 정량적 측정 및 통제 |
| 5 | Innovating | 지속적 혁신으로 비즈니스 목표 초과 달성 |

### CMMI vs SPICE 비교

| 구분 | CMMI v2.0 | SPICE (ISO/IEC 15504) |
|:---|:---|:---|
| 평가 단위 | 조직(Organization) | 프로세스(Process) |
| 등급 | 1~5단계 (Maturity Level) | 0~5단계 (Capability Level) |
| 관리 기관 | ISACA | ISO |
| 인증 방식 | Appraisal (SCAMPI) | Assessment |
| 주요 적용 분야 | 공공/국방/일반 SI | 자동차(ASPICE), 금융, 통신 |
| 특이사항 | Dev/Svc/PPL 세부 모델 존재 | 자동차: ASPICE PAM 2.5/3.1 |

📢 **섹션 요약 비유**: CMMI는 학교 전체의 교육 수준(조직 평가)이고, SPICE는 과목별 수업 품질(프로세스 평가)을 따로 측정하는 것이다.

## Ⅲ. 비교 및 연결

### Automotive SPICE (ASPICE) 특징

자동차 소프트웨어는 기능 안전(ISO 26262) 요건과 결합되어 ASPICE Level 2~3이 양산 계약의 전제 조건이 된다. 주요 평가 프로세스 그룹:

```
System Engineering Processes
  ├── SYS.1 Requirements Elicitation
  ├── SYS.2 System Requirements Analysis
  └── SYS.5 System Integration Test

Software Engineering Processes
  ├── SWE.1 Software Requirements Analysis
  ├── SWE.2 Software Architectural Design
  ├── SWE.3 Software Detailed Design
  ├── SWE.4 Software Unit Construction
  └── SWE.6 Software Qualification Test
```

### CMMI와 애자일(Agile) 병행

CMMI v2.0은 애자일·스크럼과의 통합을 공식 지원한다. 스프린트 계획·리뷰·회고가 CMMI Level 2의 프로젝트 모니터링·추적 프랙티스와 매핑 가능하다.

📢 **섹션 요약 비유**: CMMI 레벨 향상은 팀이 수작업(레벨1) → 메모장(레벨2) → 매뉴얼(레벨3) → 데이터 대시보드(레벨4) → AI 예측(레벨5)으로 업그레이드되는 것이다.

## Ⅳ. 실무 적용 및 기술사 판단

### CMMI 인증 획득 로드맵 (레벨2 → 레벨3)

```
현황 진단 (Gap Analysis)
    │
    ▼
프로세스 정의 작업 (PA별 프랙티스 이행)
    │
    ▼
파일럿 프로젝트 적용 (1~2개 프로젝트)
    │
    ▼
전사 확산 (표준 프로세스 배포)
    │
    ▼
SCAMPI A 심사 (공인 평가)
    │
    ▼
인증서 발급 (유효기간 3년)
```

### 의사결정 포인트

1. **수주 목적 vs 내재화 목적**: 인증 취득만을 목적으로 할 경우 실질적 조직 역량 향상이 어려움
2. **Automotive SPICE 적용 여부**: 자동차 Tier-1 납품 기업은 ASPICE Level 2 이상 필수
3. **CMMI vs ISO 9001 선택**: IT 특화 역량 평가는 CMMI, 일반 품질경영은 ISO 9001

📢 **섹션 요약 비유**: CMMI 레벨은 자동차 면허처럼, 1종 면허(레벨3)를 따야 대형 프로젝트(공공 조달)에 입찰할 수 있는 공식 자격이 된다.

## Ⅴ. 기대효과 및 결론

CMMI Level 3 이상 조직은 그렇지 않은 조직 대비 프로젝트 일정 준수율 30~50% 향상, 결함률 50~70% 감소가 보고된다. 공공기관 소프트웨어 용역 사업에서 CMMI Level 2~3은 기술평가 가점 요건이며, 대기업 SI의 경우 Level 3~4가 일반적이다.

**한계**: CMMI 인증은 심사 시점의 스냅샷으로, 인증 후 프로세스가 퇴행하는 경우가 많다. 지속적 내재화를 위해 PO(Process Owner) 제도와 정기 내부 심사가 필요하다.

📢 **섹션 요약 비유**: CMMI 인증은 운전면허처럼 따는 것이 목표가 아니라, 실제로 안전하게 운전(프로세스 실행)하는 능력을 갖추는 것이 진짜 목표다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| ISO 9001 | 병행 | 일반 품질경영 표준, CMMI와 중복 영역 多 |
| PMO | 연계 | 표준 프로세스 수립·배포의 주체 |
| Agile/Scrum | 통합 | CMMI v2.0과 공식 통합 지원 |
| ISO 26262 | 연계 | 기능안전 + ASPICE 병행 요건(자동차 분야) |
| SCAMPI | 방법 | CMMI 공식 인증 심사 방법론 |

### 👶 어린이를 위한 3줄 비유 설명

1. CMMI는 학교 성적처럼, "우리 팀이 소프트웨어를 얼마나 체계적으로 만드는지"를 1~5점으로 매기는 성적표예요.
2. 1점(레벨1)은 매번 즉흥으로 하고, 5점(레벨5)은 데이터로 예측하고 스스로 개선하는 최고 수준이에요.
3. 좋은 성적(레벨3 이상)이 있어야 정부 프로젝트나 큰 회사에서 "믿고 맡길 수 있는 팀"으로 선택받을 수 있어요.
