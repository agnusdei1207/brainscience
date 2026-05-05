+++
weight = 199
title = "199. 사이버 킬체인 (Cyber Kill Chain) 방어 및 마이터 어택 (MITRE ATT&CK) 프레임워크 기반 관제"
date = "2026-04-21"
[extra]
categories = "studynote-it-management"
+++

## 0. 핵심 인사이트

> **핵심**: 사이버 킬체인 (Cyber Kill Chain) 방어 및 마이터 어택 (MITRE ATT&CK) 프레임워크 기반 관제의 본질은 사이버 킬체인 (Cyber Kill Chain) 방어 및 마이터 어택 (MITRE ATT&CK) 프레임워크 기반 관제의 목적·구성·운영 기준을 명확히 설명하는 주제를 비즈니스 가치, 통제, 실행 관점에서 일관되게 연결하는 데 있다.
> **비유**: 대형 프로젝트의 건강 상태를 수치로 읽어 내는 계기판과 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

현대의 사이버 공격, 특히 APT (Advanced Persistent Threat, 지능형 지속 위협) 공격은 단순한 단발성 침입이 아니라 정찰·무기화·전달·익스플로잇·설치·C2 확립·목표 달성까지 체계적인 단계를 거친다. 방어자가 이 과정을 이해하지 못하면, 공격이 이미 깊숙이 침투한 뒤에야 발견하게 되어 막대한 피해를 초래한다.

Lockheed Martin이 2011년 발표한 **사이버 킬체인(Cyber Kill Chain)**은 이 공격 과정을 7단계로 정의하여, 방어자가 각 단계에서 어떤 통제 수단을 적용해야 하는지 명확한 기준을 제공한다. 특히, 공격 초기 단계(정찰·전달)에서 차단할수록 방어 비용이 낮고 효과가 크다는 원리가 핵심이다.

MITRE Corporation의 **ATT&CK 프레임워크**는 2013년부터 축적된 실제 침해 사례를 기반으로, 공격 그룹이 사용한 전술(Tactic)과 기법(Technique)을 체계적으로 정리한 공개 지식 베이스다. Enterprise, Mobile, ICS (Industrial Control System, 산업제어시스템) 도메인을 커버하며, 전 세계 수천 개의 기업과 정부 기관이 방어 갭(Gap) 분석과 탐지 룰셋 작성에 활용한다.

---

## 2. 구성요소

| 단계 | 명칭 | 설명 | 방어 대응 수단 |
|:---:|:---|:---|:---|
| 1 | Reconnaissance (정찰) | OSINT, 포트스캔, 소셜 엔지니어링 정보 수집 | 공개 정보 최소화, 허니팟 |
| 2 | Weaponization (무기화) | 익스플로잇 + 악성 페이로드 결합 | 취약점 패치, 위협 인텔리전스 |
| 3 | Delivery (전달) | 이메일·USB·웹을 통한 무기 전달 | 이메일 필터링, 웹 게이트웨이 |
| 4 | Exploitation (익스플로잇) | 취약점 실행, 공격 코드 동작 | EDR (Endpoint Detection & Response) |
| 5 | Installation (설치) | 백도어·RAT (Remote Access Trojan) 설치 | 파일 무결성 모니터링 |
| 6 | C2 (Command & Control) | 공격자 서버와 비밀 통신 채널 확립 | DNS 필터링, 네트워크 이상 탐지 |
| 7 | Actions on Objectives (목표달성) | 데이터 유출, 랜섬웨어 실행, 파괴 | DLP (Data Loss Prevention), 백업 |

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

킬체인 7단계와 ATT&CK의 14개 Tactic은 1:1 매핑이 아니라 다대다 관계다. 예를 들어 킬체인의 Exploitation 단계는 ATT&CK의 Initial Access·Execution·Privilege Escalation 여러 Tactic에 걸쳐 있다. 이 차이를 이해하는 것이 두 프레임워크를 통합 운영하는 핵심이다.

---

## 3. 구조 및 원리

| 구분 | Cyber Kill Chain | MITRE ATT&CK |
|:---|:---|:---|
| 출처 | Lockheed Martin (2011) | MITRE Corporation (2013~) |
| 관점 | 공격자 선형 흐름 모델 | 공격자 행동 지식 베이스 |
| 구조 | 7단계 순차 모델 | Tactic × Technique 2차원 매트릭스 |
| 강점 | 전략적 방어 계층(Defense-in-Depth) 설계 | 세부 탐지 룰셋 작성, 레드팀 시나리오 |
| 약점 | 내부 횡적 이동 세분화 부족 | 방대하여 우선순위 설정 어려움 |
| 활용 | 보안 아키텍처 설계, 경영진 보고 | SOC 탐지 엔지니어링, 레드팀/블루팀 |

| 지표 유형 | 설명 | 수명 | 방어 가치 |
|:---|:---|:---|:---|
| IOC (Indicator of Compromise, 침해 지표) | 악성 IP·도메인·파일 해시 등 | 수 시간~수 일 | 낮음 (공격자가 쉽게 변경) |
| TTP | 공격 그룹의 행동 패턴·기법 | 수 개월~수 년 | 높음 (변경에 비용 발생) |

STIX (Structured Threat Information eXpression) / TAXII (Trusted Automated eXchange of Indicator Information) 표준으로 TTP 정보를 자동 교환하고, SIEM 룰셋에 연동하여 실시간 탐지를 자동화한다.

---

## 4. 비교 및 연결

SOC 팀은 MITRE ATT&CK Navigator 도구를 사용하여 현재 탐지 커버리지를 컬러 히트맵으로 시각화한다. 탐지되지 않는 Technique(흰색 영역)을 식별하고, 우선순위에 따라 SIEM 룰셋 보강 또는 EDR 정책을 조정한다. 성숙도 모델은 레벨 1(IOC 차단) → 레벨 2(TTP 탐지) → 레벨 3(행동 분석 기반 이상 탐지) 순으로 발전한다.

레드팀은 알려진 APT 그룹(예: Lazarus Group, APT41)의 ATT&CK 매핑 TTP를 기반으로 모의 공격 시나리오를 설계한다. 블루팀은 SIEM·EDR·NDR (Network Detection and Response, 네트워크 탐지 및 대응)이 해당 TTP를 실제로 탐지하는지 검증한다. 탐지 실패 항목은 개선 백로그로 관리하고, 다음 훈련에서 재검증한다.

| 표준/제도 | ATT&CK 활용 방법 |
|:---|:---|
| ISO/IEC 27001 | 위협 모델링 근거 자료로 활용, 통제 적절성 입증 |
| NIST CSF (Cybersecurity Framework) | Identify·Protect·Detect·Respond·Recover에 TTP 매핑 |
| ISMS-P (정보보호 및 개인정보보호 관리체계) | 관리적·기술적·물리적 보호조치 실효성 검증 |
| PCI-DSS | 침투테스트 시나리오 작성 근거 |

---

## 5. 실무 적용 및 판단

사이버 킬체인과 MITRE ATT&CK를 통합 운영하면, 조직의 방어 커버리지 공백을 정량화하여 보안 투자 우선순위를 근거 있게 결정할 수 있다. 특히 APT 대응에서 단순 IOC 차단에서 TTP 기반 행동 분석으로 방어 수준을 격상시켜, 끊임없이 변화하는 공격에도 지속 가능한 방어 체계를 구축한다.

기술사 관점에서는 ① 두 프레임워크의 목적·구조 차이, ② Tactic ID(TA00XX)·Technique ID(T1XXX) 체계, ③ TIP·SIEM 연동을 통한 TTP 자동화, ④ ISMS-P·ISO 27001 컴플라이언스와의 연계 방안을 명확히 서술해야 고득점을 받을 수 있다.

---

## 6. 기대효과 및 결론

사이버 킬체인 (Cyber Kill Chain) 방어 및 마이터 어택 (MITRE ATT&CK) 프레임워크 기반 관제를 올바르게 적용하면 의사결정의 일관성, 운영의 재현성, 통제의 추적성이 동시에 향상된다. 즉 “누가 무엇을 왜 했는가”가 남기 때문에 조직이 커질수록 효과가 커진다.

다만 사이버 킬체인 (Cyber Kill Chain) 방어 및 마이터 어택 (MITRE ATT&CK) 프레임워크 기반 관제는 문서만 잘 만들어도 성공하는 영역이 아니다. 정의와 실행이 분리되면 형식주의가 되고, 자동화만 앞서면 통제 목적이 사라진다. 따라서 표준화와 민첩성, 통제와 생산성 사이의 균형이 항상 필요하다.

향후에는 정책 코드화(Policy as Code), 실시간 관측성(Observability), AI 기반 이상 탐지와 의사결정 지원이 결합되면서 관리 체계가 더 자동화되고 증거 중심으로 진화할 가능성이 크다. 결론적으로 핵심은 도구가 아니라 기준선이며, 기준선이 명확할 때만 자동화와 확장이 의미를 가진다.

---

## 7. 발전 흐름도

```text
수작업 보고
    ↓
표준 지표 정의
    ↓
사이버 킬체인 (Cyber Kill Chain) 방어 및 마이터 어택 (MITRE ATT&CK) 프레임워크 기반 관제 정착
    ↓
대시보드 기반 모니터링
    ↓
예측형 의사결정
```

---

## 8. 관련 개념 맵

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
