+++
title = "요구사항 공학 (Requirements Engineering)"
description = "소프트웨어 생명주기 성공의 열쇠, 요구사항 공학의 5단계 프로세스와 SRS 검증 심층 분석"
date = 2024-05-24
[taxonomies]
categories = ["studynotes-software_engineering"]
tags = ["Requirements Engineering", "Elicitation", "Analysis", "Specification", "Validation", "SRS"]
+++

# 요구사항 공학 (Requirements Engineering)

#### ## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 사용자의 모호하고 상충되는 비즈니스 니즈를 추출(Elicitation), 분석(Analysis), 명세(Specification), 검증(Validation) 과정을 거쳐 시스템이 구현해야 할 명확하고 검증 가능한 계약 조건(SRS)으로 변환하는 체계적 공학 기법입니다.
> 2. **가치**: 소프트웨어 결함의 60% 이상이 요구사항 단계에서 발생하며, 이 단계에서 결함을 발견하여 수정하는 비용은 구현/운영 단계에서 수정하는 비용의 1/100 수준으로 강력한 비용 절감 및 프로젝트 실패 방지 효과가 있습니다.
> 3. **융합**: 최근에는 자연어 처리(NLP) AI를 활용하여 SRS 문서 내의 모호성(Ambiguity)이나 상충(Conflict)을 자동 검출하고, MBSE(Model-Based Systems Engineering)와 결합하여 요구사항을 실행 가능한 모델로 시뮬레이션하는 방향으로 진화하고 있습니다.

---

### Ⅰ. 개요 (Context & Background)

- **개념**: 요구사항 공학(Requirements Engineering, RE)은 이해관계자의 요구를 식별하고, 이를 바탕으로 시스템의 제약 조건과 기능/비기능 요구사항을 도출하여 시스템 요구사항 명세서(SRS, Software Requirements Specification)를 작성하며, 이를 베이스라인으로 지속적으로 유지보수하고 관리하는 일련의 체계적 프로세스입니다. 단순한 '요청 수집'이 아니라, 숨겨진 니즈를 발굴하고 기술적 타당성을 검증하는 '공학적 분석'의 영역입니다.
- **💡 비유**: 건축가가 집을 지을 때 단순히 "예쁜 집을 지어주세요"라는 고객의 말을 듣고 바로 벽돌을 쌓지 않습니다. 요구사항 공학은 고객의 모호한 요청을 "방 3개, 남향, 진도 7 내진 설계, 예산 5억"이라는 구체적인 청사진과 건축 허가 도면으로 바꾸는 과정입니다. 이 도면이 잘못되면 나중에 지붕을 뜯어내야 하듯, SW에서도 이 단계가 틀어지면 프로젝트 전체가 붕괴됩니다.
- **등장 배경 및 발전 과정**:
  1. **기존 기술의 치명적 한계점**: 1970~80년대의 초기 소프트웨어 공학에서는 코딩 중심의 개발이 주를 이루었습니다. 그 결과, "사용자가 설명한 것", "프로젝트 리더가 이해한 것", "프로그래머가 작성한 것"이 완전히 달라지는 고질적인 '그네 타는 나무(Tree Swing) 만화' 현상이 발생했고, Standish Group의 Chaos Report에 따르면 프로젝트 실패 원인 1위가 '불완전한 요구사항'이었습니다.
  2. **혁신적 패러다임 변화**: 이를 해결하기 위해 IEEE Std 830(SRS 작성 표준)이 제정되었으며, 요구사항을 생명주기의 가장 앞단에 배치하여 강력하게 통제하는 Requirements Engineering 프레임워크가 정립되었습니다.
  3. **비즈니스적 요구사항**: 최근에는 마이크로서비스(MSA), 클라우드 보안, AI 윤리 등 고려해야 할 비기능 요구사항(NFR)이 기하급수적으로 증가하여, 이를 빠짐없이 추적할 수 있는 요구사항 추적 매트릭스(RTM)와 공학적 도구의 도입이 필수적이 되었습니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

요구사항 공학은 크게 요구사항 개발(Development) 4단계와 요구사항 관리(Management)로 나뉘는 CMMI 기반 프로세스 아키텍처를 가집니다.

#### 1. 요구사항 공학 프로세스 핵심 구성 요소

| 프로세스 단계 | 상세 역할 | 내부 동작 메커니즘 / 기법 | 관련 산출물 | 비유 |
|---|---|---|---|---|
| **도출 (Elicitation)** | 시스템의 목적과 사용자의 숨겨진 니즈, 이해관계자 간의 제약사항 수집 | 인터뷰, 설문조사, 브레인스토밍, Use Case 분석, 프로토타이핑, 관찰(Ethnography) | 사용자 니즈 목록, Use Case | 형사가 목격자를 심문하여 단서 수집 |
| **분석 (Analysis)** | 수집된 요구사항의 타당성 조사, 상충(Conflict) 해결, 우선순위 부여 | 자료흐름도(DFD), ER 다이어그램, 상태 전이도, 도메인 모델링, 협상 및 타협 | 요구사항 분석서, 논리 모델 | 수집된 단서의 모순점을 찾고 재구성 |
| **명세 (Specification)** | 분석된 요구사항을 개발자와 고객이 모두 이해할 수 있는 완전하고 일관된 문서로 작성 | 정형화된 템플릿(IEEE 830), 정형 명세(Z, VDM) 또는 비정형 명세(자연어) | **SRS (소프트웨어 요구사항 명세서)** | 정식 법적 계약서 작성 |
| **검증 (Validation)** | 작성된 SRS가 사용자의 원래 의도를 정확히 반영했는지, 개발 가능한지 확인 | 동료 검토(Peer Review), 워크스루, 인스펙션(Inspection), 추적성 매트릭스(RTM) 검증 | 검토 보고서, 승인된 베이스라인 | 작성된 계약서를 변호사와 함께 최종 검토 |
| **관리 (Management)** | 프로젝트 진행 중 발생하는 요구사항의 변경(Volatility)을 통제 및 추적 | CCB(형상통제위원회)를 통한 변경 통제, 버전에 따른 요구사항 이력 관리 | 변경 요청서(CR), 업데이트된 RTM | 계약 변경에 따른 부록 작성 및 도장 찍기 |

#### 2. 요구사항 공학 라이프사이클 다이어그램 (ASCII)

```text
[ Requirements Engineering Lifecycle & Data Flow ]

  [Stakeholders] ---> (Business Needs, Constraints, Rules)
       |
       v
+---------------------------------------------------+
| 1. Elicitation (도출)                             |
|  - Techniques: Interviews, Prototyping, JAD     |
+---------------------------------------------------+
       | (Raw Requirements)
       v
+---------------------------------------------------+
| 2. Analysis & Negotiation (분석 및 협상)          | <---+
|  - Resolve Conflicts, Prioritize (MoSCoW)       |     | (Unresolved Conflicts/Errors)
|  - Modeling: UML, DFD, ERD                      |     |
+---------------------------------------------------+     |
       | (Validated, Prioritized Requirements)          |
       v                                                |
+---------------------------------------------------+     |
| 3. Specification (명세)                           |     |
|  - IEEE 830 Standard, Functional & NFRs         |     |
|  - Formal / Informal Methods                    |     |
+---------------------------------------------------+     |
       | (Draft SRS)                                    |
       v                                                |
+---------------------------------------------------+     |
| 4. Validation (검증)                              | ----+
|  - Inspections, Checklists, Prototyping         | 
|  - Criteria: Consistency, Completeness, Testability|
+---------------------------------------------------+
       | (Approved)
       v
  =================================================
  |    Software Requirements Specification (SRS)  |  <-- [Baseline]
  =================================================
       |
       v
+---------------------------------------------------+
| 5. Management (관리)                              |
|  - Change Control, Traceability Matrix (RTM)    |
+---------------------------------------------------+
```

#### 3. 핵심 검증 로직 및 실무 적용 코드 (Python NLP 응용)

요구사항 명세서 작성 시 가장 흔한 오류는 **'모호성(Ambiguity)'**입니다. 기술사 관점에서는 "시스템은 매우 빠르게 반응해야 한다"와 같은 비정량적 단어가 포함된 문장을 차단해야 합니다. 다음은 정규 표현식과 간단한 NLP 규칙을 활용하여 요구사항 문장 내의 모호한 단어(Weak Words)를 검출하는 스크립트 예시입니다.

```python
import re
from typing import List, Dict

class RequirementValidator:
    def __init__(self):
        # IEEE 규격이나 실무 가이드에서 금지하는 모호한 단어 목록 (Weak/Ambiguous Words)
        self.ambiguous_words = [
            r'\b(빨리|빠르게|신속히)\b', 
            r'\b(적절히|적당히|충분히)\b',
            r'\b(쉽게|편리하게|직관적으로)\b',
            r'\b(최적화된|효율적인)\b',
            r'\b(가능한 한|필요 시)\b',
            r'\b(대략|약)\b'
        ]
        
    def analyze_requirement(self, req_id: str, text: str) -> Dict[str, any]:
        found_issues = []
        for pattern in self.ambiguous_words:
            matches = re.findall(pattern, text)
            if matches:
                found_issues.extend(matches)
                
        # 완전성(Completeness) 검증: 주어(System/User)와 조동사(Shall/Should/Must) 확인
        has_modal = bool(re.search(r'\b(해야 한다|할 수 있다|한다|이어야 한다)\b', text))
        
        return {
            "req_id": req_id,
            "text": text,
            "status": "FAIL" if found_issues or not has_modal else "PASS",
            "ambiguous_terms_found": list(set(found_issues)),
            "missing_modal_verb": not has_modal
        }

# 실무 SRS 문장 검증 테스트
validator = RequirementValidator()

reqs = [
    ("REQ-001", "시스템은 사용자가 로그인 버튼을 누르면 신속히 메인 화면을 보여주어야 한다."), # FAIL (신속히)
    ("REQ-002", "결제 모듈은 카드사 API로부터 응답을 받은 후 2초 이내에 트랜잭션을 완료해야 한다."), # PASS (정량적)
    ("REQ-003", "관리자 대시보드는 직관적으로 구성되어 쉽게 사용할 수 있어야 한다.") # FAIL (직관적, 쉽게)
]

print("--- 요구사항 명세 검증 리포트 ---")
for r_id, r_text in reqs:
    result = validator.analyze_requirement(r_id, r_text)
    if result["status"] == "FAIL":
        print(f"❌ [{result['req_id']}] 검증 실패: 모호한 단어 포함 {result['ambiguous_terms_found']}")
    else:
        print(f"✅ [{result['req_id']}] 검증 통과")
        
# 출력:
# ❌ [REQ-001] 검증 실패: 모호한 단어 포함 ['신속히']
# ✅ [REQ-002] 검증 통과
# ❌ [REQ-003] 검증 실패: 모호한 단어 포함 ['쉽게', '직관적으로']
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 요구사항 명세 기법 심층 비교: 정형(Formal) vs 비정형(Informal) 명세

| 비교 지표 | 비정형 명세 (Informal Specification) | 정형 명세 (Formal Specification) |
|---|---|---|
| **표현 수단** | 자연어(Natural Language), 자유 형식의 다이어그램 | 수학적 논리 기호, Z, VDM, Petri-Nets |
| **장점** | 고객 및 비기술 직군과의 의사소통이 매우 원활함 | 모호성이 0%에 수렴, 기계를 통한 논리적 증명 및 검증 가능 |
| **단점 / 한계** | 작성자의 주관 개입, 모호성 및 일관성 오류 발생 확률 높음 | 수학적 배경 지식 필요, 작성 비용과 시간이 기하급수적으로 높음 |
| **적용 도메인** | 일반적인 웹/앱 서비스, 엔터프라이즈 ERP/CRM | 항공우주 제어, 원자력 발전소, 인공심박동기 제어 등 생명/안전 직결 (Safety-Critical) 시스템 |
| **품질 확보 방안** | 철저한 인스펙션, IEEE 830 템플릿 엄수, 표준 용어집(Glossary) 운영 | 자동화된 정형 검증(Model Checking, Theorem Proving) 도구 활용 |

#### 2. 과목 융합 관점 분석: 비기능 요구사항(NFR)의 시스템 아키텍처 연계
*   **[요구사항 공학 + OS/컴퓨터구조]**: 요구사항 도출 시 "동시 접속자 10만 명을 지연율 50ms 이내로 처리"라는 NFR(성능 요구사항)이 도출되면, 이는 아키텍처 단계에서 OS의 Non-blocking I/O(epoll, kqueue) 도입 및 분산 캐시(Redis) 계층 설계로 직결됩니다.
*   **[요구사항 공학 + 보안(Security)]**: "GDPR 및 개인정보보호법 준수" 요구사항은 데이터 명세 시 DB의 컬럼 레벨 양방향 암호화(AES-256) 및 전송 구간 암호화(TLS 1.3)라는 구체적 시스템 스펙으로 맵핑(Mapping)되어야 합니다.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오): 끊임없는 요구사항 변경(Scope Creep) 통제
*   **상황 시나리오**: 공공기관 차세대 시스템 구축 프로젝트에서, 고객이 프로젝트 후반부(테스트 단계)에 "타 부처 연계 인터페이스 10종 추가"라는 대규모 요구사항 변경을 요청했습니다. 이를 거부하면 인수 테스트 통과가 어렵고, 수용하면 납기 지연 및 적자가 확정적입니다.
*   **의사결정 프로세스 (기술사 전략)**:
    1.  **CCB (형상통제위원회) 즉각 소집**: PM 단독으로 거절하거나 수용하는 것을 엄격히 금지.
    2.  **영향도 분석 (Impact Analysis)**: RTM(요구사항 추적 매트릭스)을 기반으로 해당 변경이 미치는 모듈 파급 효과, 수정 코드 라인 수, 추가 소요 M/M, 비용 및 회귀 테스트(Regression Test) 일정을 정량적으로 산출합니다.
    3.  **대안 제시 및 협상**: 
        - 대안 A: 비용 증액 및 납기 2개월 연장을 전제로 요구사항 10종 전면 수용 (공공 특성상 예산 증액이 불가할 확률 높음).
        - 대안 B: 핵심 기능 2종만 본 사업 내 수용(잔여 Float 활용), 나머지 8종은 2차 고도화 사업 또는 유지보수(SLA) 범위로 이관하여 문서화 합의.
    4.  **Baseline 업데이트**: 협의된 결과를 바탕으로 SRS 및 RTM을 리비전(v1.1 -> v1.2)하고 이해관계자 전원의 서명을 받아 베이스라인을 재설정합니다.

#### 2. 도입 시 고려사항 및 안티패턴 (Anti-patterns)
*   **안티패턴 1: 'How'를 요구사항에 적는 것**: 요구사항은 시스템이 '무엇(What)'을 해야 하는지 기술해야 합니다. 예: "시스템은 Oracle 19c의 해시 조인을 사용하여 데이터를 검색해야 한다" (X) -> "시스템은 1억 건의 데이터 검색을 3초 이내에 완료해야 한다" (O). 구현 기술(How)은 아키텍처/설계 단계의 몫입니다.
*   **안티패턴 2: 금도금 (Gold Plating)**: 고객이 요구하지도 않은 화려한 UI 애니메이션이나 부가 기능을 개발자가 임의로 추가하는 현상. 이는 예산 낭비, 복잡성 증가, 잠재적 버그의 온상이 되므로 요구사항 관리 통제(RTM)를 통해 철저히 차단해야 합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 도입 전 (Ad-hoc 개발) | 도입 후 (체계적 요구사항 공학) | 향상 수치 |
|---|---|---|---|
| **결함 수정 비용** | 운영 단계에서 구조적 결함 발견 시 재작업 비용 막대 | 요구사항 단계 동료 검토로 조기 결함 발견 | 운영 단계 결함 수정 비용 대비 **1/100 ~ 1/200 비용 절감** |
| **프로젝트 인도율** | 요구사항 누락으로 인한 재작업, 빈번한 납기 지연 | RTM 기반 추적을 통한 스펙 누락 방지 (Completeness 99%) | 납기 준수율 40% 이상 향상 |
| **고객 만족도** | "내가 원한 시스템이 아님" (Tree Swing 현상) | 고객이 직접 서명한 SRS 기반 개발로 기대치 일치 | 인수 테스트 통과 소요 시간 30% 단축 |

#### 2. 미래 전망 및 진화 방향
전통적인 문서 기반의 요구사항 관리(Document-Centric) 패러다임에서, 시스템 요구사항 전체를 메타데이터 모델로 관리하는 **MBSE(Model-Based Systems Engineering)**로 진화하고 있습니다. SysML과 같은 모델링 언어를 통해 요구사항 자체를 컴퓨터가 시뮬레이션할 수 있게 되어, 코딩을 시작하기도 전에 요구사항 간의 논리적 모순이나 데드락(Deadlock)을 AI가 자동으로 검증하는 시대로 나아가고 있습니다.

#### ※ 참고 표준/가이드
*   **IEEE Std 830-1998**: 소프트웨어 요구사항 명세서(SRS) 작성 가이드라인 (최신 IEEE/ISO/IEC 29148로 대체/통합).
*   **ISO/IEC/IEEE 29148:2018**: 시스템 및 소프트웨어 공학 - 라이프사이클 프로세스 - 요구사항 공학 국제 표준.

---

### 📌 관련 개념 맵 (Knowledge Graph)
*   [`[소프트웨어 생명주기 모델 (SDLC)]`](@/studynotes/04_software_engineering/01_sdlc_methodology/sdlc_models.md) : 요구사항 공학은 모든 SDLC(폭포수, 나선형 등)의 가장 첫 번째이자 핵심 기반이 되는 프로세스입니다.
*   [`[형상 관리 (Configuration Management)]`](@/studynotes/04_software_engineering/02_quality_management/configuration_management.md) : 확정된 요구사항(Baseline)의 변경 이력을 통제하고 관리하는 필수 연계 체계입니다.
*   [`[테스트 공학 (Software Testing)]`](@/studynotes/04_software_engineering/02_quality_management/software_testing.md) : V-Model에 따라, 요구사항 명세서(SRS)는 시스템 테스트 및 인수 테스트의 절대적인 기준(Test Oracle)이 됩니다.
*   [`[애자일 스크럼 (Agile Scrum)]`](@/studynotes/04_software_engineering/01_sdlc_methodology/agile_scrum.md) : 애자일에서는 무거운 SRS 대신 User Story와 Backlog 형태로 요구사항을 관리하며, 이를 지속적으로 다듬는(Grooming) 활동을 합니다.

---

### 👶 어린이를 위한 3줄 비유 설명
1. **요구사항 도출**: 산타클로스가 어린이들에게 "크리스마스에 무슨 선물을 갖고 싶니?" 하고 편지를 모으는 과정이에요.
2. **요구사항 분석과 명세**: 산타할아버지가 "장난감 자동차는 건전지가 2개 필요하고 빨간색으로 만든다"라고 요정들이 만들 수 있게 정확한 설계도와 작업 지시서를 그리는 거예요.
3. **요구사항 검증과 관리**: 요정들이 만들기 전에 설계도가 완벽한지 다시 확인하고, 중간에 어린이가 마음이 바뀌어 선물을 바꾸고 싶다고 편지를 보내면 규칙에 따라 변경해 주는 과정이랍니다.
