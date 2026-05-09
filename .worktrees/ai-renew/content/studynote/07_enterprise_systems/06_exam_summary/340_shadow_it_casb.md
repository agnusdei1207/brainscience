+++
weight = 340
title = "340. 섀도우 IT CASB 솔루션 통제 (Shadow IT CASB)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: 섀도우 IT (Shadow IT)는 IT 부서의 승인 없이 사용되는 클라우드 앱·서비스를 의미하며, CASB (Cloud Access Security Broker)는 기업 데이터가 미승인 클라우드로 유출되지 않도록 가시성·컴플라이언스·데이터 보안·위협 방어를 제공하는 보안 솔루션이다.
> 2. **가치**: 기업 평균 1,000개 이상의 섀도우 IT 앱이 존재하며, CASB는 이를 가시화하고 통제함으로써 데이터 유출 위험을 70% 이상 감소시키고 GDPR, HIPAA 등 컴플라이언스 위반을 방지한다.
> 3. **판단 포인트**: CASB는 금지(Block) 위주가 아닌 "허용-모니터링-조건부 허용"의 균형 정책으로 운영해야 직원 생산성을 해치지 않으면서 보안을 달성할 수 있으며, Zero Trust 아키텍처와 연계가 필수다.

## Ⅰ. 개요 및 필요성

Shadow IT는 HR(Slack, Google Forms), 마케팅(HubSpot, Canva), 개발팀(GitHub, AWS 개인 계정) 등 각 부서가 IT 부서 승인 없이 사용하는 클라우드 서비스를 지칭한다. Gartner 연구에 따르면 기업의 IT 지출 중 40% 이상이 Shadow IT이며, 평균 1,000개 이상의 미승인 앱이 동시에 사용된다.

**Shadow IT의 보안 위험**:
1. **데이터 유출**: 고객 정보·기밀 문서가 개인 클라우드 스토리지에 업로드
2. **컴플라이언스 위반**: GDPR, HIPAA, PCI-DSS 적용 데이터의 미승인 앱 처리
3. **계정 탈취**: 미관리 앱의 취약점 → 내부 데이터 접근 경로
4. **가시성 부재**: IT 부서가 어떤 데이터가 어디로 가는지 파악 불가

CASB (Cloud Access Security Broker)는 Gartner가 2012년 정의한 보안 솔루션 카테고리로, 기업 사용자와 클라우드 서비스 사이에 위치하여 접근 정책을 적용한다.

**SSPM (SaaS Security Posture Management)**: CASB의 진화 형태로, 승인된 SaaS 앱(Salesforce, Microsoft 365 등)의 보안 설정·구성 오류를 자동 탐지·교정한다.

📢 **섹션 요약 비유**: Shadow IT는 회사 보안 카드 없이 뒷문으로 들어오는 직원처럼 — 편리하지만 누가 들어오는지, 무엇을 들고 나가는지 아무도 모르는 상태다. CASB는 그 뒷문에 설치된 카메라와 잠금장치다.

## Ⅱ. 아키텍처 및 핵심 원리

### CASB 4가지 핵심 기둥 (Gartner)

| 기둥 | 기능 | 예시 |
|:---|:---|:---|
| 가시성 (Visibility) | Shadow IT 앱 발견, 리스크 평가 | 1,200개 앱 중 고위험 앱 150개 식별 |
| 컴플라이언스 (Compliance) | GDPR, HIPAA, PCI-DSS 정책 적용 | 의료 데이터의 미인증 앱 업로드 차단 |
| 데이터 보안 (Data Security) | DLP (Data Loss Prevention) 연계 | 신용카드 번호 클라우드 업로드 차단 |
| 위협 방어 (Threat Protection) | 악성 파일, 계정 탈취 탐지 | 비정상 접근 패턴(새벽 3시, 해외 IP) 차단 |

### CASB 배포 모드 3가지

```
┌──────────────────────────────────────────────────────┐
│              CASB 배포 모드 비교                      │
│                                                      │
│  사용자          CASB              클라우드 앱       │
│  ┌──────┐       ┌──────┐          ┌──────────────┐  │
│  │ PC   │──────▶│  API │◀────────▶│  Salesforce  │  │
│  └──────┘       │ Mode │          │  M365, Box   │  │
│                 └──────┘          └──────────────┘  │
│  ┌──────┐       ┌──────┐                             │
│  │ PC   │──────▶│Forward│──▶ Internet ──▶ 클라우드  │
│  └──────┘       │Proxy │                             │
│                 └──────┘                             │
│  ┌──────┐       ┌──────┐                             │
│  │외부  │──────▶│Reverse│── IdP 연계 ──▶ 클라우드  │
│  │사용자│       │Proxy │                             │
│  └──────┘       └──────┘                             │
└──────────────────────────────────────────────────────┘
```

**배포 모드 비교**:
- **API Mode**: 승인된 앱과 직접 API 연동 → 광범위한 가시성, 인라인 차단 불가
- **Forward Proxy**: 모든 아웃바운드 트래픽 검사 → 실시간 차단 가능, 에이전트 필요
- **Reverse Proxy**: 에이전트 없이 외부 사용자 BYOD 환경 적용 → IdP(Identity Provider) 연계

**Gartner SSE (Security Service Edge)**:
CASB + SWG (Secure Web Gateway) + ZTNA (Zero Trust Network Access)를 통합한 클라우드 기반 보안 플랫폼. Zscaler, Netskope, Microsoft Defender for Cloud Apps가 대표 제품.

�� **섹션 요약 비유**: CASB의 3가지 배포 모드는 건물 보안 시스템처럼 — API Mode는 CCTV(사후 모니터링), Forward Proxy는 정문 보안 검색대(실시간 통제), Reverse Proxy는 손님이 직접 오지 않고 대리인이 대신 들어오는 방식(외부 접속 통제)이다.

## Ⅲ. 비교 및 연결

| 비교 항목 | CASB | SWG | ZTNA | DLP |
|:---|:---|:---|:---|:---|
| 초점 | 클라우드 앱 보안 | 웹 트래픽 필터링 | 네트워크 접근 통제 | 데이터 유출 방지 |
| 적용 대상 | SaaS·IaaS·PaaS | 인터넷 전반 | 내부 앱·리소스 | 모든 채널 |
| 가시성 | 클라우드 앱 리스크 | URL 카테고리 | 사용자-앱 접근 | 데이터 콘텐츠 |
| SSE 포함 | 포함 | 포함 | 포함 | 별도 또는 연계 |
| 대표 제품 | Netskope, MCAS | Zscaler SWG | Zscaler ZPA | Symantec DLP |

**Zero Trust와 CASB 연계**:
- Zero Trust 원칙: "Never Trust, Always Verify"
- CASB는 클라우드 앱 접근의 신원(Identity)·기기(Device)·행동(Behavior) 기반 연속 인증 제공
- ZTNA + CASB + SWG = SSE (Security Service Edge) → SASE (Secure Access Service Edge) 구성

**Shadow IT 통제 정책 3단계**:
1. **발견(Discover)**: 모든 클라우드 앱 목록화 + 리스크 스코어링 (1~10점)
2. **평가(Evaluate)**: 고위험 앱(점수 > 7) 사용 부서·데이터 유형 분석
3. **제어(Govern)**: 허용/조건부 허용(MFA 필수)/차단 정책 적용

📢 **섹션 요약 비유**: CASB는 공항 보안대처럼 — 모든 승객(앱 트래픽)을 검사하되, 일반 승객(승인 앱)은 빠르게 통과시키고 위험 물질(민감 데이터 유출)은 차단한다.

## Ⅳ. 실무 적용 및 기술사 판단

**CASB 도입 체크리스트**:
- [ ] 현재 사용 중인 클라우드 앱 인벤토리가 수행되었는가?
- [ ] Shadow IT 리스크 스코어링 기준이 정의되어 있는가?
- [ ] DLP 정책과 CASB가 연계되어 있는가?
- [ ] CASB 정책이 "차단 위주"가 아닌 "허용-모니터링-조건부 허용" 균형인가?
- [ ] IdP (Okta, Azure AD)와 CASB가 연동되어 있는가?
- [ ] 분기별 Shadow IT 현황 보고서가 CISO에게 보고되는가?

**안티패턴**:
1. **전면 차단 정책**: 모든 미승인 앱 차단 → 직원 생산성 저하, 우회(VPN) 사용 증가
2. **API Mode만 의존**: 실시간 인라인 차단 없음 → 이미 유출된 후 탐지
3. **DLP 미연계**: CASB 가시성은 있지만 데이터 분류 정책 없어 차단 기준 불명확
4. **BYOD 정책 미포함**: 직원 개인 기기의 클라우드 접근 미통제 → 최대 Shadow IT 경로

**산업별 주요 컴플라이언스 요구사항**:
- 금융: PCI-DSS → 카드 데이터의 미승인 클라우드 저장 금지
- 의료: HIPAA → PHI (Protected Health Information) 클라우드 처리 규제
- 유럽: GDPR → EU 시민 개인정보의 역외 이전 제한

📢 **섹션 요약 비유**: Shadow IT를 모두 차단하면 직원들이 집에서 WhatsApp으로 업무 파일을 주고받게 된다 — 규제와 편리함의 균형을 잡는 정책이 진짜 보안이다.

## Ⅴ. 기대효과 및 결론

**CASB 도입 기대 효과**:
- 데이터 유출 위험 감소: Shadow IT 데이터 유출 경로 70% 가시화·차단
- 컴플라이언스 준수: GDPR, HIPAA 위반 리스크 자동 탐지·보고
- 비용 최적화: 미사용 SaaS 라이선스 식별 → IT 비용 10~15% 절감
- 보안 문화: Shadow IT 현황 투명화로 현업의 IT 인식 향상

**한계**:
- Forward Proxy 배포 시 성능 오버헤드 (지연 증가 10~20ms)
- SSL Inspection 기술적·법적 복잡성 (직원 프라이버시 vs 기업 보안)
- 신규 앱 출현 속도: 매달 수백 개의 새로운 클라우드 앱 → 지속적 정책 업데이트 필요

**선결 조건**: ① IdP (Identity Provider) 구축 (Okta, Azure AD) ② DLP 정책 수립 ③ Shadow IT 허용 기준 정의

📢 **섹션 요약 비유**: CASB 없는 기업의 클라우드 환경은 사방에 창문이 열린 방에서 비밀 대화를 하는 것 — 어디서 누가 듣는지 모르고, 데이터가 어디로 빠져나가는지 알 수 없다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Shadow IT | CASB 통제 대상 | 미승인 클라우드 앱·서비스 |
| DLP | CASB 연계 보안 | 데이터 유출 방지 정책 연동 |
| Zero Trust | CASB 아키텍처 기반 | 연속 인증·최소 권한 원칙 |
| SSPM | CASB 확장 | 승인된 SaaS 보안 설정 관리 |
| SSE | CASB 포함 플랫폼 | CASB + SWG + ZTNA 통합 |
| SASE | SSE 상위 아키텍처 | SSE + SD-WAN 통합 |

### 👶 어린이를 위한 3줄 비유 설명

1. Shadow IT는 학교에서 선생님 몰래 스마트폰으로 게임을 하는 것 — 편리하지만 개인 정보가 게임 회사에 넘어갈 수 있어요.
2. CASB는 학교 선생님이 교실 와이파이에 연결된 모든 기기를 볼 수 있는 것처럼 — 어떤 앱이 쓰이는지, 어떤 데이터가 오가는지 다 볼 수 있어요.
3. 모든 앱을 다 막으면 숙제도 못 하니까 — 괜찮은 앱은 허용하되 개인 정보가 새는 앱만 차단하는 똑똑한 정책이 필요해요.
