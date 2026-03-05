+++
title = "166. MoSCoW 기법 (MoSCoW Prioritization)"
description = "요구사항 우선순위 결정을 위한 필수-희망 분류 기법, 제한된 자원 내 가치 극대화 전략"
date = "2026-03-04"
[taxonomies]
tags = ["moscow", "prioritization", "requirements", "scope-management", "agile"]
categories = ["studynotes-4_software_engineering"]
+++

# 166. MoSCoW 기법 (MoSCoW Prioritization)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: MoSCoW 기법은 프로젝트의 제한된 시간과 자원 내에서 **요구사항을 Must(필수), Should(중요), Could(희망), Won't(제외)의 4단계로 분류**하여, 핵심 기능을 먼저 개발하고 범위 크리프(Scope Creep)를 방지하는 요구사항 우선순위 결정 기법입니다.
> 2. **가치**: 프로젝트 실패의 주요 원인인 **범위 팽창(Scope Creep)을 60% 이상 감소**시키며, 이해관계자 간의 **명확한 기대치 합의**를 통해 "모든 것이 중요하다"는 딜레마를 해결하고 **필수 기능 100% 완료율**을 보장합니다.
> 3. **융합**: DSDM(Dynamic Systems Development Method)에서 처음 도입된 후 **애자일 스프린트 백로그 우선순위, MVP(최소 기능 제품) 정의, 릴리스 계획 수립**에 필수적으로 활용되며, Kano 모델, 가치 기반 우선순위(Value-Based Prioritization)와 결합하여 더 정교한 의사결정을 지원합니다.

---

### I. 개요 (Context & Background) - [최소 500자]

#### 1. 개념 정의

MoSCoW 기법(또는 MoSCoW 우선순위 결정법)은 소프트웨어 프로젝트의 요구사항, 기능, 작업을 **4가지 우선순위 카테고리로 분류**하는 간단하면서도 강력한 기법입니다. 이름의 대문자 M, S, C, W가 각 카테고리를 나타내며, o는 가독성을 위해 삽입되었습니다.

**MoSCoW의 4가지 카테고리**:

| 카테고리 | 의미 | 한국어 | 정의 | 실패 시 영향 |
|:---:|:---|:---:|:---|:---|
| **M** | **Must have** | 필수 | 없으면 프로젝트가 실패하는 핵심 기능 | 프로젝트 실패 |
| **S** | **Should have** | 중요 | 중요하지만 일시적으로 없어도 운영 가능 | 심각한 불편 |
| **C** | **Could have** | 희망 | 있으면 좋지만 없어도 지장 없음 | 약간의 불편 |
| **W** | **Won't have** | 제외 | 이번 릴리스에 포함하지 않음 (향후 고려) | 없음 |

핵심 원칙은 **"모든 것이 중요할 수는 없다"**는 현실 인식에서 출발합니다. 모든 이해관계자는 자신의 요구사항이 가장 중요하다고 주장하지만, 제한된 자원 내에서는 **명확한 우선순위**가 필수적입니다.

#### 2. 비유: 이삿짐 싸기 전략

이사를 갈 때 짐을 싸야 합니다. 트럭 용량은 한정되어 있고, 시간도 제한되어 있습니다.

- **Must (필수)**: 여권, 지갑, 약, 내일 입을 옷 → 없으면 큰일 나는 것
- **Should (중요)**: 노트북, TV, 침대 → 있어야 일상생활 가능
- **Could (희망)**: 책, 게임기, 여분의 담요 → 있으면 좋지만 없어도 됨
- **Won't (제외)**: 10년 전 옷, 부서진 가구 → 이사 후 버리거나 다음에

트럭이 꽉 차면 **Could부터 내리고, 그래도 부족하면 Should 중 덜 중요한 것**을 내립니다. **Must는 절대 내리지 않습니다.** MoSCoW 기법도 같은 원리로 프로젝트 범위를 관리합니다.

#### 3. 등장 배경 및 발전 과정

**1) 1990년대 DSDM(Dynamic Systems Development Method)에서 창안**

MoSCoW 기법은 1994년 영국의 DSDM 컨소시엄에서 개발된 애자일 방법론인 DSDM의 일부로 처음 도입되었습니다. DSDM의 **"시간은 고정, 범위는 유연(Fixed Time, Variable Scope)"** 원칙을 실현하기 위한 도구로 설계되었습니다.

**2) 애자일 방법론으로 확산**

2000년대 들어 스크럼, XP 등 애자일 방법론이 보급되면서 MoSCoW는 **백로그 우선순위 결정의 사실상 표준**이 되었습니다. 제품 책임자(PO)가 스프린트 계획 시 필수적으로 활용합니다.

**3) MVP(최소 기능 제품) 개념과 결합**

린 스타트업의 MVP 개념이 부상하면서, **"Must have만으로 구성된 제품 = MVP"**라는 공식이 성립되었습니다. MoSCoW는 MVP 정의에 필수적인 도구가 되었습니다.

**4) 최신 트렌드: 가치 기반 우선순위와 결합**

단순한 4분류를 넘어, **비즈니스 가치, 기술 복잡도, 리스크**를 종합적으로 고려하는 WSJF(Weighted Shortest Job First) 등의 고급 기법과 결합하여 진화하고 있습니다.

---

### II. 아키텍처 및 핵심 원리 (Deep Dive) - [최소 1,000자]

#### 1. MoSCoW 카테고리 상세 분석

| 카테고리 | 판단 기준 | 예시 (전자상거래) | 비율 권장사항 | 특징 |
|:---:|:---|:---|:---:|:---|
| **Must** | - 없으면 출시 불가<br>- 법적/규제 요구사항<br>- 핵심 비즈니스 로직 | 상품 등록, 검색, 장바구니, 결제 | 20~30% | 타협 불가, 반드시 완료 |
| **Should** | - 있으면 큰 경쟁력<br>- 없으면 사용자 불만<br>- 핵심 UX 개선 | 상품 리뷰, 찜하기, 최근 본 상품 | 20~30% | 가능하면 완료, 대체책 가능 |
| **Could** | - 있으면 사용자 만족도 향상<br>- 차별화 포인트<br>- Nice-to-have | 소셜 공유, 추천 상품, 쿠폰 | 20~30% | 시간 남으면 완료 |
| **Won't** | - 이번 릴리스 불필요<br>- 기술적 미성숙<br>- 낮은 ROI | AR 피팅, 음성 검색, 국제 배송 | 20~40% | 다음 릴리스 고려 |

#### 2. 정교한 ASCII 다이어그램: MoSCoW 의사결정 흐름

```
================================================================================
|                    MoSCoW PRIORITIZATION DECISION FLOW                        |
================================================================================

    [ 요구사항 입력 ]  <----------------------------------------------------+
           |                                                                |
           v                                                                |
    +------+--------------------------------------------------------+       |
    |  Q1: 이 요구사항이 없으면 제품 출시가 불가능한가?               |       |
    +------+--------------------------------------------------------+       |
           |                                                                |
     +-----+-----+                                                          |
     | YES       | NO                                                       |
     v           v                                                          |
  [ MUST ]   +--+--------------------------------------------------------+  |
             |  Q2: 이 요구사항이 있으면 큰 경쟁력/사용자 만족을 주는가?  |  |
             +--+--------------------------------------------------------+  |
                |                                                           |
          +-----+-----+                                                     |
          | YES       | NO                                                  |
          v           v                                                     |
      [ SHOULD ]   +--+--------------------------------------------------+  |
                    |  Q3: 이 요구사항이 있으면 좋지만, 없어도 되는가?   |  |
                    +--+--------------------------------------------------+  |
                       |                                                    |
                 +------+------+                                             |
                 | YES         | NO                                          |
                 v             v                                             |
             [ COULD ]    [ WON'T (이번 릴리스 제외) ]                       |
                                                                            |
    [ 분포 권장사항 ]                                                        |
    ================                                                        |
    MUST    : ████░░░░░░░░░░░░░░░░  20-30%                                  |
    SHOULD  : ████░░░░░░░░░░░░░░░░  20-30%                                  |
    COULD   : ████░░░░░░░░░░░░░░░░  20-30%                                  |
    WON'T   : ████████░░░░░░░░░░░░  20-40%                                  |
                                                                            |
    [ 주의사항 ]                                                             |
    - MUST가 50%를 넘으면 재검토 필요 (범위 과다)                            |
    - 모든 것이 MUST라면 아무것도 MUST가 아님                                |
    - 이해관계자 합의 필수 (PO 단독 결정 지양)                               |
                                                                            |
    +-----------------------------------------------------------------------+

================================================================================
```

#### 3. 심층 동작 원리: MoSCoW 워크샵 프로세스

**Step 1: 요구사항 수집 및 초기 분류**
```
[요구사항 수집]
    |
    v
[후보 목록 작성]
    - 기능 요구사항
    - 비기능 요구사항
    - 기술 부채 항목
    - 버그 수정
    |
    v
[각 요구사항에 대한 기본 정보]
    - 요구사항 ID
    - 설명
    - 요청자
    - 예상 소요 시간
```

**Step 2: MoSCoW 분류 워크샵**
```
[워크샵 참가자]
- 제품 책임자 (PO)
- 개발팀 대표
- 비즈니스 이해관계자
- 사용자 대표 (가능한 경우)

[워크샵 진행]
1. 각 요구사항 소개 (5분/항목)
2. Q1~Q3 질문을 통한 분류
3. 이해관계자 간 토론 및 합의
4. 분류 결과 기록
```

**Step 3: 분포 검증 및 조정**
```
[분포 검증]
    |
    v
[MUST 비율 확인]
    - 30% 이하: OK
    - 30~50%: 재검토 권장
    - 50% 이상: 반드시 축소 필요
    |
    v
[SHOULD/COULD 균형 확인]
    |
    v
[WON'T 명확화]
    - 향후 언제 고려할지 명시
```

#### 4. 핵심 코드 예시: MoSCoW 우선순위 관리 시스템

```python
"""
MoSCoW 우선순위 관리 시스템
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime

class Priority(Enum):
    MUST = "Must Have"
    SHOULD = "Should Have"
    COULD = "Could Have"
    WONT = "Won't Have"

    def emoji(self) -> str:
        return {
            Priority.MUST: "🔴",
            Priority.SHOULD: "🟠",
            Priority.COULD: "🟢",
            Priority.WONT: "⚪"
        }[self]

@dataclass
class Requirement:
    """요구사항 클래스"""
    req_id: str
    title: str
    description: str
    priority: Priority
    requested_by: str
    story_points: int  # 예상 소요 시간
    business_value: int  # 1-10 비즈니스 가치
    technical_risk: int  # 1-10 기술적 위험
    category: str = ""  # 기능/비기능/버그 등
    status: str = "NEW"
    created_date: datetime = field(default_factory=datetime.now)

    @property
    def priority_score(self) -> float:
        """
        우선순위 점수 계산
        높은 점수 = 높은 우선순위
        """
        priority_weight = {
            Priority.MUST: 1000,
            Priority.SHOULD: 100,
            Priority.COULD: 10,
            Priority.WONT: 0
        }

        # 기본 우선순위 가중치 + 비즈니스 가치 - 기술 위험
        return (priority_weight[self.priority] +
                self.business_value * 10 -
                self.technical_risk * 5)

@dataclass
class MoSCoWAnalysis:
    """MoSCoW 분석 결과"""
    requirements: List[Requirement] = field(default_factory=list)

    def add_requirement(self, req: Requirement):
        self.requirements.append(req)

    def get_statistics(self) -> Dict:
        """통계 분석"""
        total = len(self.requirements)
        if total == 0:
            return {"error": "요구사항이 없습니다."}

        stats = {
            "total_count": total,
            "total_story_points": sum(r.story_points for r in self.requirements),
            "priority_distribution": {},
            "category_distribution": {},
            "must_percentage": 0,
            "recommendations": []
        }

        # 우선순위별 분포
        for priority in Priority:
            count = sum(1 for r in self.requirements if r.priority == priority)
            points = sum(r.story_points for r in self.requirements
                        if r.priority == priority)
            stats["priority_distribution"][priority.value] = {
                "count": count,
                "percentage": round(count / total * 100, 1),
                "story_points": points
            }

        # MUST 비율 확인
        stats["must_percentage"] = stats["priority_distribution"][Priority.MUST.value]["percentage"]

        # 권장사항 생성
        if stats["must_percentage"] > 50:
            stats["recommendations"].append(
                "⚠️ MUST가 50%를 초과합니다. 범위 축소를 권장합니다."
            )
        elif stats["must_percentage"] > 30:
            stats["recommendations"].append(
                "💡 MUST가 30%를 초과합니다. 재검토를 권장합니다."
            )
        else:
            stats["recommendations"].append(
                "✅ MUST 비율이 적절합니다."
            )

        # SHOULD vs COULD 균형
        should_pct = stats["priority_distribution"][Priority.SHOULD.value]["percentage"]
        could_pct = stats["priority_distribution"][Priority.COULD.value]["percentage"]

        if should_pct + could_pct < 20:
            stats["recommendations"].append(
                "⚠️ SHOULD와 COULD가 너무 적습니다. 우선순위 재분배를 고려하세요."
            )

        return stats

    def get_sorted_backlog(self) -> List[Requirement]:
        """우선순위별 정렬된 백로그 반환"""
        return sorted(self.requirements,
                     key=lambda r: r.priority_score,
                     reverse=True)

    def scope_capacity_check(self, capacity: int) -> Dict:
        """
        용량 기반 범위 검사
        capacity: 가능한 총 스토리 포인트
        """
        result = {
            "capacity": capacity,
            "must_points": 0,
            "should_points": 0,
            "could_points": 0,
            "feasible_items": [],
            "at_risk_items": [],
            "excluded_items": []
        }

        # MUST 합산
        result["must_points"] = sum(
            r.story_points for r in self.requirements
            if r.priority == Priority.MUST
        )

        # 용량 체크
        remaining = capacity - result["must_points"]

        if remaining < 0:
            result["at_risk_items"] = [
                r for r in self.requirements if r.priority == Priority.MUST
            ]
            result["recommendations"] = [
                f"❌ MUST만으로도 용량을 {-remaining}포인트 초과합니다.",
                "용량 증가 또는 MUST 축소가 필요합니다."
            ]
            return result

        # SHOULD 추가
        for req in sorted([r for r in self.requirements
                          if r.priority == Priority.SHOULD],
                         key=lambda r: r.priority_score, reverse=True):
            if remaining >= req.story_points:
                result["should_points"] += req.story_points
                result["feasible_items"].append(req)
                remaining -= req.story_points
            else:
                result["at_risk_items"].append(req)

        # COULD 추가
        for req in sorted([r for r in self.requirements
                          if r.priority == Priority.COULD],
                         key=lambda r: r.priority_score, reverse=True):
            if remaining >= req.story_points:
                result["could_points"] += req.story_points
                result["feasible_items"].append(req)
                remaining -= req.story_points
            else:
                result["excluded_items"].append(req)

        result["utilization"] = round(
            (capacity - remaining) / capacity * 100, 1
        )
        result["recommendations"] = [
            f"✅ 용량 활용률: {result['utilization']}%",
            f"📝 MUST: {result['must_points']}pt, SHOULD: {result['should_points']}pt, COULD: {result['could_points']}pt"
        ]

        return result

    def generate_report(self) -> str:
        """MoSCoW 분석 보고서 생성"""
        stats = self.get_statistics()

        report = ["=" * 60]
        report.append("        MoSCoW 우선순위 분석 보고서")
        report.append("=" * 60)
        report.append(f"\n[요약]")
        report.append(f"  총 요구사항: {stats['total_count']}개")
        report.append(f"  총 스토리 포인트: {stats['total_story_points']}pt")
        report.append(f"  MUST 비율: {stats['must_percentage']}%")

        report.append(f"\n[우선순위 분포]")
        for priority in Priority:
            dist = stats["priority_distribution"][priority.value]
            bar = "█" * int(dist["percentage"] / 5)
            report.append(
                f"  {priority.emoji()} {priority.value:12s}: "
                f"{dist['count']:3d}개 ({dist['percentage']:5.1f}%) {bar}"
            )

        report.append(f"\n[권장사항]")
        for rec in stats["recommendations"]:
            report.append(f"  {rec}")

        report.append(f"\n[우선순위 정렬 백로그 (상위 10개)]")
        for i, req in enumerate(self.get_sorted_backlog()[:10], 1):
            report.append(
                f"  {i:2d}. [{req.priority.emoji()}] {req.req_id}: "
                f"{req.title} ({req.story_points}pt)"
            )

        return "\n".join(report)

# 사용 예시
if __name__ == "__main__":
    analysis = MoSCoWAnalysis()

    # 요구사항 추가
    requirements = [
        Requirement("REQ-001", "상품 등록", "판매자가 상품을 등록한다",
                   Priority.MUST, "사업팀", 8, 10, 3, "핵심기능"),
        Requirement("REQ-002", "상품 검색", "구매자가 상품을 검색한다",
                   Priority.MUST, "사업팀", 5, 9, 2, "핵심기능"),
        Requirement("REQ-003", "장바구니", "상품을 장바구니에 담는다",
                   Priority.MUST, "사업팀", 8, 10, 4, "핵심기능"),
        Requirement("REQ-004", "결제 연동", "결제를 처리한다",
                   Priority.MUST, "사업팀", 13, 10, 7, "핵심기능"),
        Requirement("REQ-005", "상품 리뷰", "리뷰를 작성한다",
                   Priority.SHOULD, "마케팅팀", 5, 7, 3, "UX개선"),
        Requirement("REQ-006", "찜하기", "관심 상품을 저장한다",
                   Priority.SHOULD, "마케팅팀", 3, 6, 2, "UX개선"),
        Requirement("REQ-007", "쿠폰 발급", "쿠폰을 발급한다",
                   Priority.COULD, "마케팅팀", 8, 5, 4, "마케팅"),
        Requirement("REQ-008", "소셜 공유", "SNS에 공유한다",
                   Priority.COULD, "마케팅팀", 3, 3, 2, "마케팅"),
        Requirement("REQ-009", "AR 피팅", "AR로 입어본다",
                   Priority.WONT, "R&D팀", 21, 8, 9, "혁신"),
    ]

    for req in requirements:
        analysis.add_requirement(req)

    # 보고서 출력
    print(analysis.generate_report())

    # 용량 체크
    print("\n" + "=" * 60)
    print("용량 기반 범위 검사 (가용: 30pt)")
    print("=" * 60)
    capacity_result = analysis.scope_capacity_check(30)
    for rec in capacity_result["recommendations"]:
        print(f"  {rec}")
```

---

### III. 융합 비교 및 다각도 분석 - [비교표 2개 이상]

#### 1. 심층 기술 비교표: MoSCoW vs Kano vs WSJF

| 비교 항목 | MoSCoW | Kano 모델 | WSJF (SAFe) |
|:---|:---|:---|:---|
| **분류 체계** | 4단계 (Must/Should/Could/Won't) | 5단계 (당연/일원/매력/무관관/역품질) | 수치화된 점수 |
| **주요 관점** | 프로젝트 범위 관리 | **고객 만족도** 기반 | **경제적 가치** 기반 |
| **복잡도** | 낮음 (간단) | 중간 | 높음 (계산 필요) |
| **주요 활용** | 스프린트 계획, MVP 정의 | 제품 기획, UX 설계 | 대규모 백로그 우선순위 |
| **정량화** | 없음 (범주형) | 없음 (범주형) | 있음 (점수형) |
| **시간 고려** | 없음 | 없음 | 있음 (Job Duration) |
| **적합 규모** | 소~중형 프로젝트 | 제품 기획 | 대형 프로그램 |

#### 2. 상황별 적합한 우선순위 기법 선택 매트릭스

| 상황 | 추천 기법 | 이유 |
|:---|:---|:---|
| **스프린트 계획** | MoSCoW | 간단하고 빠른 분류 |
| **MVP 정의** | MoSCoW + Kano | Must + 매력적 품질 결합 |
| **제품 로드맵** | Kano | 고객 만족도 기반 장기 계획 |
| **대규모 백로그** | WSJF | 정량화된 의사결정 |
| **이해관계자 합의** | MoSCoW | 직관적 이해 용이 |
| **기술 부채 관리** | WSJF | 비용-가치 분석 용이 |

#### 3. 과목 융합 관점 분석

**MoSCoW + 애자일 스크럼**
```
[스크럼에서의 MoSCoW 활용]

제품 백로그
    |
    +-- [Must Have] -----> 스프린트 1, 2 (반드시 완료)
    +-- [Should Have] ---> 스프린트 3, 4 (가능하면 완료)
    +-- [Could Have] ----> 스프린트 5+ (시간 남으면)
    +-- [Won't Have] ----> 다음 릴리스 백로그로 이관

[Definition of Ready]
- 각 백로그 아이템은 MoSCoW 분류가 완료되어야 함

[스프린트 목표]
- 스프린트 내 모든 Must는 완료 보장
```

**MoSCoW + MVP (Minimum Viable Product)**
```
[MVP 정의에 MoSCoW 활용]

MVP = Must Have만으로 구성된 최소 제품

[MVP 검증 루프]
1. Must Have만으로 제품 출시
2. 사용자 반응 수집
3. Kano 분석으로 매력적 품질 식별
4. Should/Could 중 매력적 품질을 다음 버전 Must로 승격

[장점]
- 빠른 시장 출시
- 리스크 최소화
- 실제 사용자 피드백 기반 개선
```

---

### IV. 실무 적용 및 기술사적 판단 - [최소 800자]

#### 1. 기술사적 판단 (실무 시나리오)

**[시나리오 1] 스타트업 MVP 개발**

*   **상황**:
    - 핀테크 스타트업의 P2P 송금 앱 개발
    - 투자 유치를 위한 3개월 내 MVP 출시 필요
    - 요구사항 50개, 개발팀 5명

*   **기술사적 판단**: **MoSCoW 엄격 적용**

*   **실행 전략**:
    1. **워크샵 진행**: CEO, 개발리드, 디자이너 참여
    2. **Must 선정 기준**: "없으면 앱이 아니다" 테스트
    3. **결과**: Must 10개(20%), Should 15개, Could 15개, Won't 10개
    4. **MVP 범위**: Must 10개만 3개월 내 개발

*   **핵심 의사결정 포인트**:
    - "소셜 로그인"은 Should → 이메일 회원가입만 Must
    - "알림 푸시"는 Could → MVP에서 제외
    - "송금 취소"는 Must → 법적 요구사항

**[시나리오 2] 대기업 통합 시스템 구축**

*   **상황**:
    - 그룹사 ERP 통합 프로젝트
    - 5개 사업부 간 요구사항 충돌
    - 각 사업부는 자신의 요구가 가장 중요하다고 주장

*   **기술사적 판단**: **MoSCoW + 거버넌스 위원회**

*   **실행 전략**:
    1. **거버넌스 위원회 구성**: 각 사업부 대표 + CIO
    2. **MoSCoW 워크샵**: 사업부별 요구사항 분류
    3. **합의 메커니즘**: Must는 전사 합의, Should는 사업부별
    4. **분포 제한**: 전체 Must ≤ 30%

*   **핵심 의사결정 포인트**:
    - 모든 사업부 Must 총합이 70% → 재협상 필수
    - "공통 기능"과 "사업부 고유 기능" 분리

**[시나리오 3] 레거시 시스템 마이그레이션**

*   **상황**:
    - 20년 된 메인프레임을 클라우드로 이관
    - 1,000개 화면, 5,000개 기능
    - 모든 기능을 그대로 이관하면 3년 소요

*   **기술사적 판단**: **MoSCoW + 사용 빈도 분석**

*   **실행 전략**:
    1. **사용 빈도 데이터 수집**: 로그 분석
    2. **빈도 기반 1차 분류**: 상위 20% 기능 = Must 후보
    3. **비즈니스 임팩트 분석**: 법적/규제 기능 추가
    4. **최종 Must**: 30% 기능 (나머지는 단계적 이관)

#### 2. 도입 시 고려사항 체크리스트

**분류 기준 명확화**:
- [ ] **Must 정의**: "없으면 출시 불가"의 구체적 기준
- [ ] **비율 제한**: Must 비율 상한선 설정 (30% 권장)
- [ ] **승격/강등 규칙**: Should→Must, Must→Should 조건 정의
- [ ] **이해관계자 합의**: 분류 결과에 대한 동의 프로세스

**프로세스 정의**:
- [ ] **워크샵 주기**: MoSCoW 재평가 시점 (스프린트별? 릴리즈별?)
- [ ] **의사결정 권한**: 최종 분류 결정권자 (PO? 위원회?)
- [ ] **이의 제기 절차**: 분류에 반대하는 경우의 프로세스
- [ ] **변경 통제**: 분류 변경 시 승인 절차

**측정 및 모니터링**:
- [ ] **분포 추적**: 각 우선순위별 비율 모니터링
- [ ] **완료율 추적**: Must 100% 완료 여부
- [ ] **범위 변경 추적**: 분류 변경 이력 관리

#### 3. 주의사항 및 안티패턴 (Anti-patterns)

*   **"모든 것이 Must다" (Everything is Must)**:
    - 가장 흔한 안티패턴
    - 이해관계자가 자신의 요구사항을 Must로 주장
    - **해결**: Must 비율 제한(30%) 설정 및 거버넌스

*   **MoSCoW 고정 (Static MoSCoW)**:
    - 프로젝트 초기에 분류 후 재평가 없음
    - 비즈니스 환경 변화에 따라 우선순위도 변화해야 함
    - **해결**: 스프린트마다 또는 분기마다 재평가

*   **Won't의 무시 (Ignoring Won't)**:
    - Won't로 분류된 요구사항을 완전히 잊어버림
    - **해결**: Won't는 "향후 릴리즈 고려"이므로 백로그에 유지

*   **기술적 고려사항 무시 (Ignoring Technical Factors)**:
    - 비즈니스 가치만 고려하고 기술적 복잡도/리스크 무시
    - **해결**: MoSCoW + 기술적 요소 결합 (WSJF 등)

---

### V. 기대효과 및 결론 - [최소 400자]

#### 1. 정량적/정성적 기대효과

| 구분 | 효과 내용 | 기대 수치 |
|:---:|:---|:---|
| **범위 관리** | 범위 크리프(Scope Creep) 방지 | 60% 감소 |
| **의사결정 속도** | 우선순위 결정 시간 단축 | 50% 감소 |
| **이해관계자 만족** | 명확한 기대치 설정 | 만족도 30% 향상 |
| **MVP 성공률** | 핵심 기능 완료 보장 | Must 100% 완료 |
| **프로젝트 예측성** | 일정 준수율 향상 | 25% 향상 |
| **팀 집중도** | 명확한 우선순위로 집중 업무 | 생산성 20% 향상 |

#### 2. 미래 전망 및 진화 방향

1.  **AI 기반 자동 분류**:
    - LLM이 요구사항 설명을 분석하여 자동으로 MoSCoW 분류 제안
    - "이 요구사항은 [핵심 기능]이므로 Must 제안"

2.  **실시간 동적 우선순위**:
    - 시장 상황, 경쟁사 동향, 사용자 피드백을 실시간 반영
    - 자동으로 Should→Must 승격 제안

3.  **OKR/KPI와의 통합**:
    - 회사 목표(OKR)와 연계하여 자동 우선순위 조정
    - "이번 분기 핵심 OKR과 연관된 요구사항 자동 Must 승격"

#### 3. 참고 표준/가이드

*   **DSDM (Dynamic Systems Development Method)**: MoSCoW의 원천 방법론
*   **Agile Alliance**: 애자일 우선순위 결정 가이드
*   **SAFe (Scaled Agile Framework)**: WSJF를 포함한 우선순위 결정 방법

---

### 관련 개념 맵 (Knowledge Graph)

*   [카노 모델 (Kano Model)](@/studynotes/4_software_engineering/4_requirements/_index.md) : 고객 만족도 기반 품질 분류
*   [MVP (Minimum Viable Product)](@/studynotes/4_software_engineering/1_sdlc/_index.md) : MoSCoW Must로 구성된 최소 제품
*   [제품 백로그](@/studynotes/4_software_engineering/1_sdlc/scrum_framework.md) : MoSCoW가 적용되는 스크럼 산출물
*   [요구사항 공학](@/studynotes/4_software_engineering/4_requirements/requirements_engineering.md) : MoSCoW가 활용되는 분석 단계
*   [WSJF (Weighted Shortest Job First)](@/studynotes/4_software_engineering/1_sdlc/_index.md) : SAFe의 정량화된 우선순위 기법

---

### 어린이를 위한 3줄 비유 설명

1. **문제**: 가방에 짐을 싸는데 가방이 너무 작아서 다 들어가지 않아요.
2. **해결(MoSCoW)**: 짐을 **4가지 상자**에 나눠요. 빨간 상자(없으면 안 되는 것), 주황 상자(있어야 하는 것), 초록 상자(있으면 좋은 것), 흰 상자(이번엔 안 챙기는 것). 가방엔 빨간 상자부터 채워요.
3. **효과**: 여행 갈 때 정말 필요한 건 다 챙기고, 없어도 되는 건 나중에 챙겨서 가방이 터지지 않아요!
