+++
weight = 199
title = "199. 사이버 킬체인 및 MITRE ATT&CK (Cyber Kill Chain & MITRE ATT&CK)"
date = "2026-04-21"
[extra]
categories = "studynote-it-management"
+++
## 0. 핵심 인사이트

> **핵심**: 사이버 킬체인(Cyber Kill Chain)은 공격자의 침투 과정을 7단계로 모델링하여, 방어자가 각 단계에서 공격을 차단할 수 있는 구조적 프레임워크다. 단계가 앞을수록 차단 비용이 낮다.
> 2. **가치**: MITRE ATT&CK (Adversarial Tactics, Techniques, and Common Knowledge)는 실제 공격 캠페인에서 관찰된 TTP (Tactics, Techniques, and Procedures, 전술·기법·절차)를 행렬 형태로 정리한 글로벌 표준 지식 베이스로, SOC (Security Operations Center, 보안 운영 센터) 탐지 룰셋 작성의 사실상 표준이다.
> 3. **판단 포인트**: 두 프레임워크는 상호 보완적이다. 킬체인은 공격의 '흐름'을, ATT&CK는 각 단계의 '방법'을 설명한다. 기술사 답안에서는 이 구분을 명확히 하고, TIP (Threat Intelligence Platform, 위협 인텔리전스 플랫폼)·SIEM (Security Information and Event Management, 보안 정보 및 이벤트 관리) 연동 방안까지 서술해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

현대의 사이버 공격, 특히 APT (Advanced Persistent Threat, 지능형 지속 위협) 공격은 단순한 단발성 침입이 아니라 정찰·무기화·전달·익스플로잇·설치·C2 확립·목표 달성까지 체계적인 단계를 거친다. 방어자가 이 과정을 이해하지 못하면, 공격이 이미 깊숙이 침투한 뒤에야 발견하게 되어 막대한 피해를 초래한다.

Lockheed Martin이 2011년 발표한 **사이버 킬체인(Cyber Kill Chain)**은 이 공격 과정을 7단계로 정의하여, 방어자가 각 단계에서 어떤 통제 수단을 적용해야 하는지 명확한 기준을 제공한다. 특히, 공격 초기 단계(정찰·전달)에서 차단할수록 방어 비용이 낮고 효과가 크다는 원리가 핵심이다.

MITRE Corporation의 **ATT&CK 프레임워크**는 2013년부터 축적된 실제 침해 사례를 기반으로, 공격 그룹이 사용한 전술(Tactic)과 기법(Technique)을 체계적으로 정리한 공개 지식 베이스다. Enterprise, Mobile, ICS (Industrial Control System, 산업제어시스템) 도메인을 커버하며, 전 세계 수천 개의 기업과 정부 기관이 방어 갭(Gap) 분석과 탐지 룰셋 작성에 활용한다.

📢 **섹션 요약 비유**: 사이버 킬체인은 범인이 은행을 터는 전체 시나리오이고, MITRE ATT&CK는 그 범인이 사용한 모든 도구와 수법을 정리한 경찰 수사 데이터베이스다. 둘을 함께 보면 "언제, 어디서, 무엇으로" 막을지 정확히 알 수 있다.

---

## 2. 구성요소

### 2-1. 사이버 킬체인 7단계 구조

| 단계 | 명칭 | 설명 | 방어 대응 수단 |
|:---:|:---|:---|:---|
| 1 | Reconnaissance (정찰) | OSINT, 포트스캔, 소셜 엔지니어링 정보 수집 | 공개 정보 최소화, 허니팟 |
| 2 | Weaponization (무기화) | 익스플로잇 + 악성 페이로드 결합 | 취약점 패치, 위협 인텔리전스 |
| 3 | Delivery (전달) | 이메일·USB·웹을 통한 무기 전달 | 이메일 필터링, 웹 게이트웨이 |
| 4 | Exploitation (익스플로잇) | 취약점 실행, 공격 코드 동작 | EDR (Endpoint Detection & Response) |
| 5 | Installation (설치) | 백도어·RAT (Remote Access Trojan) 설치 | 파일 무결성 모니터링 |
| 6 | C2 (Command & Control) | 공격자 서버와 비밀 통신 채널 확립 | DNS 필터링, 네트워크 이상 탐지 |
| 7 | Actions on Objectives (목표달성) | 데이터 유출, 랜섬웨어 실행, 파괴 | DLP (Data Loss Prevention), 백업 |

### 2-2. MITRE ATT&CK 매트릭스 구조

```text
┌──────────────────────────────────────────────────────────────────────┐
│          MITRE ATT&CK Enterprise Matrix (주요 Tactic)                │
├─────────────┬────────────────────────────────────────────────────────┤
│  TA0043     │  Reconnaissance      (정찰)                            │
│  TA0042     │  Resource Development(자원 개발)                       │
│  TA0001     │  Initial Access      (초기 침투)                       │
│  TA0002     │  Execution           (실행)                            │
│  TA0003     │  Persistence         (지속성 확보)                     │
│  TA0004     │  Privilege Escalation(권한 상승)                       │
│  TA0005     │  Defense Evasion     (방어 우회)                       │
│  TA0006     │  Credential Access   (자격증명 탈취)                   │
│  TA0007     │  Discovery           (내부 탐색)                       │
│  TA0008     │  Lateral Movement    (횡적 이동)                       │
│  TA0009     │  Collection          (데이터 수집)                     │
│  TA0011     │  Command and Control (C2)                              │
│  TA0010     │  Exfiltration        (데이터 유출)                     │
│  TA0040     │  Impact              (영향·파괴)                       │
├─────────────┴────────────────────────────────────────────────────────┤
│  각 Tactic 아래 → Technique (예: T1059 Command Scripting)            │
│  각 Technique 아래 → Sub-technique (예: T1059.001 PowerShell)        │
└──────────────────────────────────────────────────────────────────────┘
```

### 2-3. 킬체인 단계와 ATT&CK Tactic 매핑

킬체인 7단계와 ATT&CK의 14개 Tactic은 1:1 매핑이 아니라 다대다 관계다. 예를 들어 킬체인의 Exploitation 단계는 ATT&CK의 Initial Access·Execution·Privilege Escalation 여러 Tactic에 걸쳐 있다. 이 차이를 이해하는 것이 두 프레임워크를 통합 운영하는 핵심이다.

📢 **섹션 요약 비유**: MITRE ATT&CK는 "도둑이 문을 따는 방법 14가지 카테고리"고, 각 카테고리 아래에 수백 가지 세부 기법이 있다. 킬체인이 도둑이 집에 들어오는 순서를 알려준다면, ATT&CK는 각 순서에서 어떤 도구를 쓰는지 알려준다.

---

## 3. 구조 및 동작 원리

### 3-1. 킬체인 vs. ATT&CK 프레임워크 비교

| 구분 | Cyber Kill Chain | MITRE ATT&CK |
|:---|:---|:---|
| 출처 | Lockheed Martin (2011) | MITRE Corporation (2013~) |
| 관점 | 공격자 선형 흐름 모델 | 공격자 행동 지식 베이스 |
| 구조 | 7단계 순차 모델 | Tactic × Technique 2차원 매트릭스 |
| 강점 | 전략적 방어 계층(Defense-in-Depth) 설계 | 세부 탐지 룰셋 작성, 레드팀 시나리오 |
| 약점 | 내부 횡적 이동 세분화 부족 | 방대하여 우선순위 설정 어려움 |
| 활용 | 보안 아키텍처 설계, 경영진 보고 | SOC 탐지 엔지니어링, 레드팀/블루팀 |

### 3-2. TTP 기반 위협 인텔리전스 연계

| 지표 유형 | 설명 | 수명 | 방어 가치 |
|:---|:---|:---|:---|
| IOC (Indicator of Compromise, 침해 지표) | 악성 IP·도메인·파일 해시 등 | 수 시간~수 일 | 낮음 (공격자가 쉽게 변경) |
| TTP | 공격 그룹의 행동 패턴·기법 | 수 개월~수 년 | 높음 (변경에 비용 발생) |

STIX (Structured Threat Information eXpression) / TAXII (Trusted Automated eXchange of Indicator Information) 표준으로 TTP 정보를 자동 교환하고, SIEM 룰셋에 연동하여 실시간 탐지를 자동화한다.

📢 **섹션 요약 비유**: 악성 IP 차단(IOC)은 변장한 도둑의 오늘 모자를 막는 것이고, TTP 차단은 도둑이 항상 쓰는 특별한 자물쇠 따기 기술 자체를 막는 것이다. 모자는 내일 바뀌지만 손버릇은 쉽게 바뀌지 않는다.

---

## 4. 비교 및 트레이드오프

### 4-1. ATT&CK Navigator를 활용한 SOC 갭 분석

SOC 팀은 MITRE ATT&CK Navigator 도구를 사용하여 현재 탐지 커버리지를 컬러 히트맵으로 시각화한다. 탐지되지 않는 Technique(흰색 영역)을 식별하고, 우선순위에 따라 SIEM 룰셋 보강 또는 EDR 정책을 조정한다. 성숙도 모델은 레벨 1(IOC 차단) → 레벨 2(TTP 탐지) → 레벨 3(행동 분석 기반 이상 탐지) 순으로 발전한다.

### 4-2. 레드팀/블루팀 훈련(Adversary Emulation)

레드팀은 알려진 APT 그룹(예: Lazarus Group, APT41)의 ATT&CK 매핑 TTP를 기반으로 모의 공격 시나리오를 설계한다. 블루팀은 SIEM·EDR·NDR (Network Detection and Response, 네트워크 탐지 및 대응)이 해당 TTP를 실제로 탐지하는지 검증한다. 탐지 실패 항목은 개선 백로그로 관리하고, 다음 훈련에서 재검증한다.

### 4-3. 컴플라이언스 연계 활용

| 표준/제도 | ATT&CK 활용 방법 |
|:---|:---|
| ISO/IEC 27001 | 위협 모델링 근거 자료로 활용, 통제 적절성 입증 |
| NIST CSF (Cybersecurity Framework) | Identify·Protect·Detect·Respond·Recover에 TTP 매핑 |
| ISMS-P (정보보호 및 개인정보보호 관리체계) | 관리적·기술적·물리적 보호조치 실효성 검증 |
| PCI-DSS | 침투테스트 시나리오 작성 근거 |

📢 **섹션 요약 비유**: ATT&CK는 보안팀의 훈련 교본이다. 레드팀은 교본대로 공격하고, 블루팀은 같은 교본을 보며 방어를 준비한다. 교본이 없으면 훈련도 없고, 실전에서도 무방비 상태가 된다.

---

## 5. 실무 적용 및 최적화 기법

사이버 킬체인과 MITRE ATT&CK를 통합 운영하면, 조직의 방어 커버리지 공백을 정량화하여 보안 투자 우선순위를 근거 있게 결정할 수 있다. 특히 APT 대응에서 단순 IOC 차단에서 TTP 기반 행동 분석으로 방어 수준을 격상시켜, 끊임없이 변화하는 공격에도 지속 가능한 방어 체계를 구축한다.

기술사 관점에서는 ① 두 프레임워크의 목적·구조 차이, ② Tactic ID(TA00XX)·Technique ID(T1XXX) 체계, ③ TIP·SIEM 연동을 통한 TTP 자동화, ④ ISMS-P·ISO 27001 컴플라이언스와의 연계 방안을 명확히 서술해야 고득점을 받을 수 있다.

📢 **섹션 요약 비유**: 킬체인이 "범죄 현장 재구성"이라면, ATT&CK는 "범죄자 수법 백과사전"이다. 두 가지를 함께 쓰는 보안팀은 과거 사건을 분석하고 미래 공격을 예측하여 선제적으로 막는 진짜 프로가 된다.

---

### 📌 관련 개념 맵

| 개념 | 설명 | 연관 키워드 |
|:---|:---|:---|
| Cyber Kill Chain | Lockheed Martin 7단계 공격 흐름 모델 | APT, 방어 계층 |
| MITRE ATT&CK | 공격자 행동 TTP 지식 베이스 | Tactic, Technique, Sub-technique |
| TTP | Tactics·Techniques·Procedures, 공격 행동 패턴 | IOC, 위협 인텔리전스 |
| IOC | Indicator of Compromise, 침해 지표 (IP·해시 등) | SIEM, 블랙리스트 |
| SOC | Security Operations Center, 보안 운영 센터 | SIEM, EDR, NDR |
| SIEM | Security Information and Event Management | 로그 분석, 룰셋 자동화 |
| ATT&CK Navigator | 커버리지 히트맵 시각화 도구 | 갭 분석, 우선순위 설정 |
| STIX/TAXII | 위협 정보 표준 교환 형식 | TIP, 자동화 |
| ISMS-P | 정보보호 및 개인정보보호 관리체계 (국내) | 컴플라이언스, 심사 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. 사이버 킬체인은 도둑이 집에 몰래 들어오는 7가지 단계야. 초반에 막을수록 쉽고, 도둑이 이미 방 안에 들어오면 막기가 훨씬 어려워.
2. MITRE ATT&CK는 전 세계 도둑들이 "어떤 방법으로 문을 따고, 자물쇠를 열고, 금고를 부수는지" 다 적어놓은 거대한 수법 사전이야. 경찰(보안팀)이 이 사전을 보며 우리 집 경보기가 제대로 달렸는지 확인해.
3. IOC는 도둑의 발자국(이미 지나간 흔적)이고, TTP는 그 도둑이 항상 쓰는 특별한 자물쇠 따기 기술이야. 발자국은 눈 오면 사라지지만, 손버릇은 평생 남아서 TTP를 막는 게 훨씬 오래가는 방어야.
