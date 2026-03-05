+++
title = "16. 프로세스 자산 (Process Assets)"
description = "조직의 소프트웨어 개발 역량을 체계화하여 재사용 가능한 지식, 문서, 도구의 집합체"
date = "2026-03-05"
[taxonomies]
tags = ["process-assets", "pal", "organizational-wealth", "knowledge-management", "cmmi"]
categories = ["studynotes-4_software_engineering"]
+++

# 16. 프로세스 자산 (Process Assets)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 프로세스 자산은 조직이 수행한 소프트웨어 개발 활동에서 **축적된 지식, 문서, 템플릿, 도구, 교육 자료** 등을 체계적으로 정리하여 **재사용 가능한 형태**로 보관한 조직의 지적 자산입니다.
> 2. **가치**: 프로세스 자산 라이브러리(PAL) 활용 시 **프로젝트 기획 단계 시간 30% 단축, 유사 실수 50% 감소, 신규 팀원 온보딩 40% 효율화** 등 정량적 효과가 입증됩니다.
> 3. **융합**: CMMI Level 3의 핵심 구성 요소이며, **지식 경영(KM), 학습 조직(Learning Organization), AI 기반 지식 검색** 등과 융합하여 진화 중입니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**프로세스 자산(Process Assets)**이란 조직이 소프트웨어 개발 프로세스를 수행하면서 생성, 수집, 검증한 **모든 유형/무형의 자산**을 의미합니다. 이는 CMMI에서 **조직 프로세스 자산(Organizational Process Assets)**로 정의되며, Level 3(Defined) 달성을 위한 필수 요건입니다.

**프로세스 자산의 5대 구성 요소**:

| 구분 | 내용 | 예시 |
|:---|:---|:---|
| **프로세스 정의서** | 표준 프로세스, 절차, 가이드라인 | SDLC 절차서, 코딩 표준 |
| **템플릿/양식** | 산출물 작성용 표준 양식 | 요구사항 명세서 템플릿, 테스트 계획서 양식 |
| **체크리스트** | 검증/확인용 점검 항목 | 코드 리뷰 체크리스트, 인수 테스트 체크리스트 |
| **메트릭/데이터** | 과거 프로젝트 성과 데이터 | 생산성 DB, 결함 DB, 일정 DB |
| **교육/지식** | 역량 강화 자료 | 온보딩 교육 자료, 기술 백서, 레슨런드 |

### 2. 비유: 요리 레시피와 주방 도구

```
[프로세스 자산 = 미슐랭 레스토랑의 비법 노트]

미슐랭 레스토랑                        소프트웨어 조직
─────────────────                    ─────────────────
요리 레시피북      ───────────────>  프로세스 정의서
 (어떻게 만드는가)                     (어떻게 개발하는가)

재료 손질 가이드    ───────────────>  템플릿/양식
 (표준화된 준비 방법)                  (표준화된 문서 형식)

품질 체크리스트    ───────────────>  검토 체크리스트
 (맛, 온도, 플레이팅)                   (품질, 보안, 성능)

과거 주문 데이터    ───────────────>  메트릭 DB
 (인기 메뉴, 조리 시간)                 (생산성, 결함률)

주방장 노트       ───────────────>  레슨런드(Learned Lessons)
 (실패 경험, 성공 비법)                  (성공/실패 사례)

──────────────────────────────────────────────────────
신입 요리사도 레시피만 보면        신입 개발자도 자산만 보면
미슐랭 수준의 요리를 낼 수 있음     일정 수준의 산출물을 낼 수 있음
```

### 3. 등장 배경 및 발전 과정

**1) 1990년대: CMM과 함께 등장**
- CMM Level 3(Defined)에서 "조직 표준 소프트웨어 프로세스" 개념 도입
- 프로세스 정의서, 템플릿 등 기본 자산 체계화

**2) 2000년대: 지식 경영(KM)과 융합**
- 지식 관리 시스템(KMS)과 프로세스 자산 라이브러리 통합
- Wiki, 전자 결재 시스템을 통한 자산 공유

**3) 2010년대: 클라우드 및 협업 도구 발전**
- Confluence, SharePoint, Notion 등 협업 플랫폼으로 이동
- 실시간 협업, 버전 관리 가능

**4) 2020년대: AI 기반 지식 검색**
- LLM을 활용한 자연어 질의로 자산 검색
- "이번 프로젝트와 유사한 과거 사례 찾아줘" → 자동 추천

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 프로세스 자산 라이브러리(PAL) 구조

```
================================================================================
|              PROCESS ASSET LIBRARY (PAL) ARCHITECTURE                         |
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                        PROCESS ASSET LIBRARY (PAL)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    LAYER 1: POLICIES & STANDARDS                     │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │  • 조직 프로세스 정책 (Process Policy)                               │   │
│  │  • 표준 프로세스 프레임워크 (Standard Process Framework)              │   │
│  │  • 라이프사이클 모델 (Lifecycle Models)                              │   │
│  │  • 테일러링 가이드 (Tailoring Guidelines)                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    v                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    LAYER 2: PROCESS DEFINITIONS                      │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │  • 요구사항 공학 프로세스                                            │   │
│  │  • 설계 프로세스                                                     │   │
│  │  • 구현 프로세스                                                     │   │
│  │  • 테스트 프로세스                                                   │   │
│  │  • 형상 관리 프로세스                                                │   │
│  │  • 품질 보증 프로세스                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    v                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    LAYER 3: SUPPORTING ASSETS                        │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │  TEMPLATES   │  │ CHECKLISTS   │  │   EXAMPLES   │              │   │
│  │  │  템플릿/양식  │  │  체크리스트   │  │    예시      │              │   │
│  │  ├──────────────┤  ├──────────────┤  ├──────────────┤              │   │
│  │  │• SRS 템플릿  │  │• 설계 검토   │  │• 우수 SRS    │              │   │
│  │  │• 설계서 양식 │  │• 코드 리뷰   │  │• 우수 코드   │              │   │
│  │  │• 테스트 계획 │  │• 테스트 완료 │  │• 우수 설계   │              │   │
│  │  │• 프로젝트계획│  │• 인수 검사   │  │  사례        │              │   │
│  │  └──────────────┘  └──────────────┘  └──────────────┘              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    v                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    LAYER 4: MEASUREMENT REPOSITORY                   │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │  • 프로젝트 성과 DB (일정, 비용, 품질)                                │   │
│  │  • 생산성 데이터 (FP/인월, LOC/일)                                   │   │
│  │  • 결함 DB (유형, 원인, 수정 비용)                                   │   │
│  │  • 리스크 DB (발생 빈도, 대응 방안)                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    v                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    LAYER 5: LESSONS LEARNED                          │   │
│  ├─────────────────────────────────────────────────────────────────────┤   │
│  │  • 성공 사례 (Best Practices)                                        │   │
│  │  • 실패 사례 (Pitfalls to Avoid)                                     │   │
│  │  • 프로젝트 회고 보고서                                              │   │
│  │  • 기술적 교훈                                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
|                           ACCESS LAYER                                       |
|  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    |
|  │   Portal     │  │   Search     │  │   Training   │  │    AI        │    |
|  │   포털       │  │   검색       │  │   교육       │  │   추천       │    |
|  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    |
================================================================================
```

### 2. 테일러링 프로세스 다이어그램

```
================================================================================
|                    PROCESS TAILORING WORKFLOW                                |
================================================================================

    ┌─────────────────────────────────────────────────────────────────────┐
    │                 ORGANIZATIONAL STANDARD PROCESS (OSP)                │
    │                      조직 표준 프로세스                               │
    └──────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   v
    ┌─────────────────────────────────────────────────────────────────────┐
    │                      TAILORING GUIDELINES                            │
    │                         테일러링 가이드                              │
    │  ┌─────────────────────────────────────────────────────────────┐   │
    │  │  Project Characteristics (프로젝트 특성):                    │   │
    │  │  • 규모: 소(5인 이하) / 중(5-20인) / 대(20인 이상)           │   │
    │  │  • 위험도: 저 / 중 / 고                                      │   │
    │  │  • 도메인: 공공 / 금융 / 제조 / 모바일 / 웹                   │   │
    │  │  • 고객: 내부 / 외부 / 해외                                   │   │
    │  └─────────────────────────────────────────────────────────────┘   │
    └──────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   v
    ┌─────────────────────────────────────────────────────────────────────┐
    │                    PROJECT-SPECIFIC PROCESS (PSP)                    │
    │                       프로젝트 맞춤형 프로세스                        │
    │  ┌─────────────────────────────────────────────────────────────┐   │
    │  │  Tailoring Decisions:                                        │   │
    │  │  • 추가(Add): 보안 검토 추가 (금융 프로젝트)                   │   │
    │  │  • 삭제(Omit): 상세 설계서 생략 (애자일 프로젝트)              │   │
    │  │  • 수정(Modify): 코드 리뷰 → 페어 프로그래밍                  │   │
    │  │  • 강화(Amplify): 회귀 테스트 3회 → 5회 (안전 중요 시스템)     │   │
    │  └─────────────────────────────────────────────────────────────┘   │
    └──────────────────────────────┬──────────────────────────────────────┘
                                   │
                                   v
    ┌─────────────────────────────────────────────────────────────────────┐
    │                      TAILORED ASSET PACKAGE                          │
    │                        맞춤형 자산 패키지                             │
    │  ┌─────────────────────────────────────────────────────────────┐   │
    │  │  • 프로젝트 계획서 템플릿 (간소화 버전)                       │   │
    │  │  • 체크리스트 (선택된 항목만)                                  │   │
    │  │  • 메트릭 (프로젝트 규모에 맞는 지표)                          │   │
    │  │  • 예시 (유사 프로젝트 산출물)                                 │   │
    │  └─────────────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────────────┘

================================================================================
```

### 3. 심층 동작 원리: 자산 활용 프로세스 (5단계)

```
Step 1: 자산 검색 및 발견 (Asset Discovery)
        ┌────────────────────────────────────────┐
        │ 사용자 질의: "요구사항 명세서 작성    │
        │              방법이 필요해"            │
        │                │                       │
        │                v                       │
        │ 검색 엔진: 키워드, 태그, 유사도 기반   │
        │ 결과: SRS 템플릿, 작성 가이드,        │
        │       우수 사례 3건                   │
        └────────────────────────────────────────┘
                         │
                         v
Step 2: 자산 평가 및 선택 (Evaluation & Selection)
        ┌────────────────────────────────────────┐
        │ 후보 자산 비교:                        │
        │ - 최신성: 2024년 갱신 vs 2019년        │
        │ - 신뢰성: 검증된 자산 vs 초안          │
        │ - 적합성: 공공용 vs 상용               │
        │                │                       │
        │ 선택: "공공 SRS 템플릿 v3.0"          │
        └────────────────────────────────────────┘
                         │
                         v
Step 3: 자산 맞춤화 (Customization)
        ┌────────────────────────────────────────┐
        │ 템플릿 다운로드                        │
        │ 프로젝트 특성에 맞게 수정:             │
        │ - 회사명, 프로젝트명 입력              │
        │ - 불필요한 섹션 삭제                   │
        │ - 추가 필요 섹션 삽입                  │
        └────────────────────────────────────────┘
                         │
                         v
Step 4: 활용 및 피드백 (Usage & Feedback)
        ┌────────────────────────────────────────┐
        │ 실제 프로젝트에 적용                   │
        │ 사용 후 평가:                          │
        │ - 유용했는가? (별점 1-5)               │
        │ - 개선 제안 사항                       │
        │ - 누락된 항목                          │
        │                │                       │
        │ 피드백 제출 → 자산 소유자              │
        └────────────────────────────────────────┘
                         │
                         v
Step 5: 자산 갱신 및 개선 (Update & Improvement)
        ┌────────────────────────────────────────┐
        │ 자산 소유자 검토                       │
        │ 피드백 반영하여 버전 업데이트          │
        │ v3.0 → v3.1                           │
        │                │                       │
        │ 변경 사항 공지 및 재공유               │
        └────────────────────────────────────────┘
```

### 4. 핵심 코드 예시: 프로세스 자산 관리 시스템

```python
"""
Process Asset Management System (PAMS)
프로세스 자산 라이브러리 관리 시스템
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime

class AssetType(Enum):
    TEMPLATE = "템플릿"
    CHECKLIST = "체크리스트"
    GUIDELINE = "가이드라인"
    EXAMPLE = "예시"
    METRIC = "메트릭"
    LESSON_LEARNED = "레슨런드"

class AssetStatus(Enum):
    DRAFT = "초안"
    REVIEW = "검토중"
    APPROVED = "승인됨"
    DEPRECATED = "폐기됨"

@dataclass
class ProcessAsset:
    """프로세스 자산"""
    asset_id: str
    name: str
    asset_type: AssetType
    version: str
    status: AssetStatus
    owner: str  # 자산 소유자
    created_date: datetime
    last_updated: datetime
    description: str
    tags: List[str] = field(default_factory=list)
    usage_count: int = 0
    rating: float = 0.0  # 사용자 평균 평점
    file_path: str = ""
    related_processes: List[str] = field(default_factory=list)

    def increment_usage(self):
        """사용 횟수 증가"""
        self.usage_count += 1

    def update_rating(self, new_rating: float):
        """평점 업데이트 (평균)"""
        # 단순화된 평균 계산
        self.rating = round((self.rating + new_rating) / 2, 1)

@dataclass
class TailoringDecision:
    """테일러링 결정 사항"""
    project_id: str
    asset_id: str
    decision_type: str  # ADD, OMIT, MODIFY, AMPLIFY
    reason: str
    approver: str
    approved_date: datetime

class ProcessAssetLibrary:
    """프로세스 자산 라이브러리"""

    def __init__(self, organization_name: str):
        self.organization_name = organization_name
        self.assets: Dict[str, ProcessAsset] = {}
        self.tailoring_decisions: List[TailoringDecision] = []

    def add_asset(self, asset: ProcessAsset) -> bool:
        """자산 추가"""
        if asset.asset_id in self.assets:
            return False
        self.assets[asset.asset_id] = asset
        return True

    def search_assets(self, query: str, asset_type: Optional[AssetType] = None) -> List[ProcessAsset]:
        """자산 검색"""
        results = []
        query_lower = query.lower()

        for asset in self.assets.values():
            # 상태 필터 (승인된 것만)
            if asset.status != AssetStatus.APPROVED:
                continue

            # 타입 필터
            if asset_type and asset.asset_type != asset_type:
                continue

            # 키워드 매칭
            if (query_lower in asset.name.lower() or
                query_lower in asset.description.lower() or
                any(query_lower in tag.lower() for tag in asset.tags)):
                results.append(asset)

        # 사용 횟수 기준 정렬 (인기순)
        results.sort(key=lambda x: x.usage_count, reverse=True)
        return results

    def get_recommended_assets(self, project_type: str, domain: str) -> List[ProcessAsset]:
        """프로젝트 특성에 따른 추천 자산"""
        recommendations = []

        for asset in self.assets.values():
            if asset.status != AssetStatus.APPROVED:
                continue

            # 도메인 태그 매칭
            if domain.lower() in [t.lower() for t in asset.tags]:
                recommendations.append(asset)

        # 평점 기준 정렬
        recommendations.sort(key=lambda x: x.rating, reverse=True)
        return recommendations[:5]  # 상위 5개

    def record_tailoring(self, decision: TailoringDecision):
        """테일러링 결정 기록"""
        self.tailoring_decisions.append(decision)

    def get_asset_statistics(self) -> Dict:
        """자산 통계"""
        stats = {
            "total_assets": len(self.assets),
            "by_type": {},
            "by_status": {},
            "most_used": [],
            "highest_rated": []
        }

        # 타입별 통계
        for asset_type in AssetType:
            count = sum(1 for a in self.assets.values()
                       if a.asset_type == asset_type)
            stats["by_type"][asset_type.value] = count

        # 상태별 통계
        for status in AssetStatus:
            count = sum(1 for a in self.assets.values()
                       if a.status == status)
            stats["by_status"][status.value] = count

        # 가장 많이 사용된 자산
        sorted_by_usage = sorted(self.assets.values(),
                                 key=lambda x: x.usage_count,
                                 reverse=True)
        stats["most_used"] = [(a.name, a.usage_count)
                              for a in sorted_by_usage[:5]]

        # 가장 높은 평점 자산
        sorted_by_rating = sorted(self.assets.values(),
                                  key=lambda x: x.rating,
                                  reverse=True)
        stats["highest_rated"] = [(a.name, a.rating)
                                  for a in sorted_by_rating[:5]]

        return stats

# 사용 예시
if __name__ == "__main__":
    # 라이브러리 생성
    pal = ProcessAssetLibrary("ABC소프트웨어")

    # 샘플 자산 추가
    asset1 = ProcessAsset(
        asset_id="TPL-SRS-001",
        name="공공 SRS 템플릿",
        asset_type=AssetType.TEMPLATE,
        version="3.0",
        status=AssetStatus.APPROVED,
        owner="품질관리팀",
        created_date=datetime(2022, 1, 1),
        last_updated=datetime(2024, 6, 15),
        description="공공 사업용 요구사항 명세서 템플릿",
        tags=["공공", "요구사항", "SRS", "문서"],
        usage_count=45,
        rating=4.5,
        related_processes=["요구사항 공학", "요구사항 관리"]
    )

    pal.add_asset(asset1)

    # 검색 테스트
    results = pal.search_assets("요구사항")
    print(f"검색 결과: {len(results)}건")
    for r in results:
        print(f"  - {r.name} (v{r.version}, 평점: {r.rating})")

    # 통계 출력
    stats = pal.get_asset_statistics()
    print(f"\n총 자산 수: {stats['total_assets']}개")
    print(f"타입별: {stats['by_type']}")
```

---

## III. 융합 비교 및 다각도 분석

### 1. 심층 기술 비교: 자산 관리 도구

| 비교 항목 | Confluence | SharePoint | Notion | Git Wiki | 전용 PAL 시스템 |
|:---|:---|:---|:---|:---|:---|
| **협업** | 매우 강함 | 강함 | 매우 강함 | 보통 | 보통 |
| **버전 관리** | 기본 | 강함 | 기본 | 매우 강함 | 강함 |
| **검색 기능** | 강함 | 강함 | 보통 | 보통 | 매우 강함 |
| **메타데이터** | 보통 | 강함 | 보통 | 약함 | 매우 강함 |
| **워크플로우** | 기본 | 강함 | 기본 | 없음 | 매우 강함 |
| **비용** | 중간 | 높음 | 낮음 | 무료 | 높음 |
| **커스터마이징** | 보통 | 강함 | 강함 | 강함 | 매우 강함 |

### 2. 과목 융합 관점 분석

**프로세스 자산 + 지식 경영 (KM)**
```
[융합 포인트]

1. SECI 모델과 프로세스 자산
   ┌──────────────────────────────────────────────────┐
   │  Socialization (사회화)                           │
   │  → 멘토링, OJT, 페어 프로그래밍                   │
   │  → 비공식 지식을 공유                              │
   │                                                  │
   │  Externalization (외면화)                         │
   │  → 레슨런드 작성, 프로세스 정의서화                │
   │  → 암묵지를 형식지로 변환                          │
   │                                                  │
   │  Combination (결합)                              │
   │  → 템플릿, 가이드라인 통합                        │
   │  → 형식지 간 연결                                 │
   │                                                  │
   │  Internalization (내면화)                         │
   │  → 교육, 실무 적용                                │
   │  → 형식지를 개인 역량으로                          │
   └──────────────────────────────────────────────────┘

[시너지]
- 프로세스 자산: 지식의 "저장소"
- KM: 지식의 "흐름" 관리
- 결합: 지식이 축적되고 순환하는 생태계
```

---

## IV. 실무 적용 및 기술사적 판단

### 1. 기술사적 판단 (실무 시나리오)

**[시나리오] 중견 SI 기업의 PAL 구축**

*   **상황**:
    - 직원 300명, 연 매출 1,000억 원
    - 현재: 개인 PC에 흩어진 문서, 검색 불가
    - 목표: 전사 PAL 구축, CMMI Level 3 달성

*   **기술사적 판단**: **단계적 구축, 실용성 우선**

*   **실행 로드맵**:
    ```
    Phase 1 (3개월): 기반 구축
    - 플랫폼 선정 (Confluence + 전용 메타데이터 관리)
    - 자산 분류 체계 정의
    - 핵심 자산 20개 우선 등록

    Phase 2 (6개월): 자산 확충
    - 프로세스 정의서, 템플릿 체계화
    - 과거 프로젝트 메트릭 수집
    - 레슨런드 수집 프로세스 정착

    Phase 3 (3개월): 활성화
    - 검색 고도화 (AI 기반 추천)
    - 사용자 교육 및 홍보
    - 품질 게이트 연동
    ```

### 2. 도입 시 고려사항 체크리스트

**플랫폼 선정**:
- [ ] 검색 기능: 전문 검색, 태그 검색, 유사도 검색
- [ ] 버전 관리: 이력 추적, 롤백 가능
- [ ] 권한 관리: 역할별 접근 통제
- [ ] 통합성: 기존 시스템(Jira, Git 등)과 연동

**운영 체계**:
- [ ] 자산 소유자 지정: 각 자산별 책임자
- [ ] 갱신 주기: 최소 연 1회 검토
- [ ] 품질 검토: 승인 프로세스
- [ ] 폐기 절차: 노후 자산 정리

### 3. 주의사항 및 안티패턴

*   **자산의 무덤 (Asset Graveyard)**:
    - 많은 자산이 등록되지만 아무도 사용하지 않음
    - 해결: 사용자 중심 설계, 지속적 홍보

*   **과도한 문서화 (Over-Documentation)**:
    - 모든 것을 문서화하려다 관리 불가
    - 해결: 핵심 자산에 집중, 80/20 법칙 적용

---

## V. 기대효과 및 결론

### 1. 정량적/정성적 기대효과

| 구분 | 효과 내용 | 기대 수치 |
|:---:|:---|:---|
| **생산성** | 프로젝트 초기 문서 작성 시간 | 30~40% 단축 |
| **품질** | 산출물 품질 일관성 | 25% 향상 |
| **온보딩** | 신규 팀원 적응 기간 | 40% 단축 |
| **재사용** | 유사 프로젝트 자산 활용률 | 60% 증가 |

### 2. 미래 전망

1.  **AI 기반 자산 추천**: LLM 활용 맥락 인식 추천
2.  **자동화된 자산 생성**: 프로젝트 결과물 자동 자산화
3.  **실시간 협업**: 동시 편집, 실시간 피드백

### 3. 참고 표준

*   **CMMI for Development**: Organizational Process Definition
*   **ISO/IEC 12207**: 소프트웨어 생명주기 프로세스
*   **ISO 30401**: 지식경영시스템 가이드라인

---

## 관련 개념 맵 (Knowledge Graph)

*   [CMMI 5단계](@/studynotes/4_software_engineering/1_sdlc/15_cmmi_5_levels.md) : Level 3에서 PAL 구축 필수
*   [소프트웨어 형상 관리](@/studynotes/4_software_engineering/1_sdlc/configuration_management.md) : 자산의 버전 관리
*   [품질 보증](@/studynotes/4_software_engineering/2_quality/software_quality_standards.md) : 품질 관련 자산

---

## 어린이를 위한 3줄 비유 설명

1. **문제**: 요리를 할 때마다 레시피를 다시 찾고, 매번 똑같은 실수를 해요.

2. **해결(프로세스 자산)**: 엄마의 **비법 노트**를 만들어요! 성공한 요리법, 실패한 경험, 좋은 재료 정보를 모아둬요. 이제 그 노트만 보면 누구나 맛있는 요리를 할 수 있어요.

3. **효과**: 친구가 와도 노트만 주면 혼자서도 요리할 수 있고, 엄마가 없어도 맛있는 밥을 할 수 있어요! 회사에서도 이런 "비법 노트"를 만들어서 모두가 함께 써요.
