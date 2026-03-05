+++
title = "WBS (Work Breakdown Structure)"
date = 2024-05-24
description = "프로젝트 목표를 달성하기 위해 수행해야 할 작업을 계층적으로 분해한 구조, 프로젝트 범위 관리와 일정/비용 산정의 기준이 되는 핵심 산출물"
weight = 20
categories = ["studynotes-se"]
+++

# WBS (Work Breakdown Structure)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: WBS(Work Breakdown Structure, 작업 분할 구조도)는 프로젝트 전체 작업을 **관리 가능한 수준까지 계층적으로 분해**한 구조로, 프로젝트 범위를 시각화하고 **각 작업 단위의 책임과 일정, 비용을 명확히** 정의하는 프로젝트 관리의 핵심 도구입니다.
> 2. **가치**: 체계적인 WBS 작성을 통해 **프로젝트 누락 작업 90% 이상 예방**, 정확한 일정/비용 산정이 가능하며, 이해관계자 간 **범위 합의 및 변경 관리의 기준점**이 됩니다.
> 3. **융합**: PMBOK 범위 관리의 핵심 도구로, **EVM(성과 측정), CPM(주공정법), PERT** 등의 프로젝트 관리 기법과 연계되며, 애자일에서는 **백로그(Backlog) 구조화**에 활용됩니다.

---

## I. 개요 (Context & Background)

### 1. 명확한 개념 및 정의

**WBS(Work Breakdown Structure, 작업 분할 구조도)**는 프로젝트에서 수행해야 할 모든 작업을 체계적으로 식별하고, 이를 계층적으로 분해하여 표현한 구조입니다. PMBOK(Project Management Body of Knowledge)에서는 WBS를 다음과 같이 정의합니다:

> "WBS는 팀이 프로젝트 범위를 관리하기 위해 수행해야 할 총 작업을 **작업 크기와 복잡도에 상관없이 계층적으로 분해**하여 조직하고 정의한 것이다."

**WBS의 핵심 원칙**:

| 원칙 | 설명 | 실무적 의미 |
|:---|:---|:---|
| **100% 규칙** | WBS는 프로젝트 범위의 **100%를 포함**해야 함 | 누락 작업 방지, 범위 합의 |
| **상호 배타성** | 각 WBS 요소는 **중복되지 않고 독립적**이어야 함 | 책임 소재 명확화 |
| **결과물 중심** | 활동(Activity)이 아닌 **산출물(Deliverable) 중심**으로 분해 | 완료 기준 명확화 |
| **관리 가능성** | 최하위 수준은 **관리/통제 가능한 크기**여야 함 | 8/80 규칙 (8시간~80시간) |

**WBS 계층 구조**:

```
[WBS 계층 구조]

Level 1: 프로젝트 (Project)
    |
    +-- Level 2: 주요 산출물/단계 (Major Deliverables/Phases)
            |
            +-- Level 3: 하위 산출물 (Sub-Deliverables)
                    |
                    +-- Level 4: 작업 패키지 (Work Packages)
                            |
                            +-- Level 5: 활동 (Activities) - WBS 외부

[작업 패키지(Work Package) 기준]
- 8/80 규칙: 8시간 이상, 80시간 이내의 작업 단위
- 또는 단일 책임자가 관리 가능한 단위
- 비용과 일정을 추정할 수 있는 최소 단위
```

### 2. 비유: 건축 설계도

```
[WBS = 건축 설계도의 방 구조도]

프로젝트: 집 짓기
    |
    +-- 1. 기초 공사
    |       |
    |       +-- 1.1 필로티 기초
    |       +-- 1.2 방수 공사
    |
    +-- 2. 구조 공사
    |       |
    |       +-- 2.1 기둥 설치
    |       +-- 2.2 보 설치
    |       +-- 2.3 슬래브 타설
    |
    +-- 3. 외장 공사
    |       |
    |       +-- 3.1 외벽 시공
    |       +-- 3.2 지붕 공사
    |       +-- 3.3 창호 설치
    |
    +-- 4. 내장 공사
            |
            +-- 4.1 바닥 마감
            +-- 4.2 벽지 도장
            +-- 4.3 조명 설치

이 설계도가 있어야:
- 자재를 얼마나 주문할지 알 수 있음 (비용 산정)
- 얼마나 걸릴지 알 수 있음 (일정 산정)
- 누가 무엇을 할지 정할 수 있음 (책임 할당)
- 무엇이 빠졌는지 확인할 수 있음 (범위 검증)
```

### 3. 등장 배경 및 발전 과정

#### 1) WBS 등장 이전의 문제점

**전통적 프로젝트 관리의 한계**:
- 작업 항목이 체계적으로 정리되지 않아 누락 발생
- "이것도 해야 했어요?" 사례 빈발
- 책임 소재 불명확
- 일정/비용 산정의 근거 부족

```
[문제 사례: 소프트웨어 개발 프로젝트]

초기 계획:
"웹사이트 개발 - 3개월, 1억 원"

개발 중 발견된 누락 항목:
- 보안 인증 구현 (2주 추가)
- 모바일 반응형 (3주 추가)
- 데이터베이스 백업 시스템 (1주 추가)
- 로깅 시스템 (1주 추가)
- 관리자 페이지 (2주 추가)
- ...

결과: 5개월 소요, 1.5억 원 지출

원인: WBS 없이 "웹사이트 개발" 하나로만 계획
```

#### 2) WBS의 역사적 발전

| 시기 | 발전 내용 | 기여자 |
|:---|:---|:---|
| 1950년대 | PERT/CPM 개발 | 미 해군, DuPont |
| 1960년대 | WBS 개념 정립 | 미 국방부 (DoD) |
| 1968 | WBS 군사 표준화 | MIL-STD-881 |
| 1987 | PMBOK에 통합 | PMI |
| 1990년대 | 소프트웨어 프로젝트 적용 | SEI, IEEE |
| 2000년대~ | 애자일 백로그와 연계 | 애자일 커뮤니티 |

#### 3) 현대적 적용

- **전통적 프로젝트**: 폭포수, V-모델 등에서 범위 관리 핵심 도구
- **애자일 프로젝트**: 에픽(Epic) > 스토리(Story) > 태스크(Task) 구조
- **하이브리드**: 프로젝트 레벨 WBS + 스프린트 레벨 백로그

---

## II. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 구성 요소 상세 분석

| 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/도구 | 비유 |
|:---|:---|:---|:---|:---|
| **WBS 사전** | 각 WBS 요소의 상세 정의 | ID, 명칭, 설명, 책임자, 완료 기준 | Excel, WBS 소프트웨어 | 재료 목록 |
| **작업 패키지** | WBS 최하위 관리 단위 | 8~80시간, 단일 책임자, 산출물 중심 | 프로젝트 관리 도구 | 레고 블록 |
| **WBS 코드** | 각 요소의 고유 식별자 | 1.0, 1.1, 1.1.1 등 계층적 번호 | 코딩 규칙 | 바코드 |
| **완료 기준** | 작업 완료 판단 기준 | 검증 가능한 산출물, 품질 기준 | 체크리스트 | 줄자 |
| **책임 매트릭스** | 작업별 책임자 할당 | RACI 차트 연계 | RACI 도구 | 명패 |

### 2. 정교한 구조 다이어그램

```text
================================================================================
|                    WBS HIERARCHICAL STRUCTURE                                 |
================================================================================

PROJECT: E-Commerce Platform Development
+==============================================================================+
|                                                                              |
|  1.0 E-Commerce Platform                                                     |
|  +--------------------------------------------------------------------------+
|  |                                                                          |
|  |  1.1 Requirements Phase                                                  |
|  |  +--------------------------------------------------------------------+ |
|  |  |  1.1.1 Business Analysis           [Work Package]                   | |
|  |  |  1.1.2 User Requirements           [Work Package]                   | |
|  |  |  1.1.3 Technical Requirements      [Work Package]                   | |
|  |  |  1.1.4 Requirements Review         [Work Package]                   | |
|  |  +--------------------------------------------------------------------+ |
|  |                                                                          |
|  |  1.2 Design Phase                                                       |
|  |  +--------------------------------------------------------------------+ |
|  |  |  1.2.1 Architecture Design         [Work Package]                   | |
|  |  |  1.2.2 Database Design             [Work Package]                   | |
|  |  |  1.2.3 UI/UX Design                [Work Package]                   | |
|  |  |    +-- 1.2.3.1 Wireframe           [Sub-Package]                    | |
|  |  |    +-- 1.2.3.2 Mockup              [Sub-Package]                    | |
|  |  |    +-- 1.2.3.3 Prototype           [Sub-Package]                    | |
|  |  |  1.2.4 API Design                  [Work Package]                   | |
|  |  |  1.2.5 Design Review               [Work Package]                   | |
|  |  +--------------------------------------------------------------------+ |
|  |                                                                          |
|  |  1.3 Development Phase                                                  |
|  |  +--------------------------------------------------------------------+ |
|  |  |  1.3.1 Backend Development         [Work Package]                   | |
|  |  |    +-- 1.3.1.1 Auth Module         [Sub-Package]                    | |
|  |  |    +-- 1.3.1.2 Product Module      [Sub-Package]                    | |
|  |  |    +-- 1.3.1.3 Order Module        [Sub-Package]                    | |
|  |  |    +-- 1.3.1.4 Payment Module      [Sub-Package]                    | |
|  |  |  1.3.2 Frontend Development        [Work Package]                   | |
|  |  |  1.3.3 Database Implementation     [Work Package]                   | |
|  |  |  1.3.4 Integration                 [Work Package]                   | |
|  |  +--------------------------------------------------------------------+ |
|  |                                                                          |
|  |  1.4 Testing Phase                                                      |
|  |  +--------------------------------------------------------------------+ |
|  |  |  1.4.1 Unit Testing                [Work Package]                   | |
|  |  |  1.4.2 Integration Testing         [Work Package]                   | |
|  |  |  1.4.3 System Testing              [Work Package]                   | |
|  |  |  1.4.4 UAT                         [Work Package]                   | |
|  |  +--------------------------------------------------------------------+ |
|  |                                                                          |
|  |  1.5 Deployment Phase                                                   |
|  |  +--------------------------------------------------------------------+ |
|  |  |  1.5.1 Infrastructure Setup        [Work Package]                   | |
|  |  |  1.5.2 Production Deployment       [Work Package]                   | |
|  |  |  1.5.3 Go-Live Support             [Work Package]                   | |
|  |  +--------------------------------------------------------------------+ |
|  |                                                                          |
|  |  1.6 Project Management                                                 |
|  |  +--------------------------------------------------------------------+ |
|  |  |  1.6.1 Planning                     [Work Package]                   | |
|  |  |  1.6.2 Monitoring & Control        [Work Package]                   | |
|  |  |  1.6.3 Communication               [Work Package]                   | |
|  |  +--------------------------------------------------------------------+ |
|  |                                                                          |
+--+--------------------------------------------------------------------------+
   |
   v
[WBS Dictionary Example]

+==============================================================================+
| WBS Dictionary Entry                                                          |
+==============================================================================+
| WBS Code: 1.3.1.3                                                             |
| Name: Order Module Development                                                |
| Description: 주문 생성, 수정, 취소, 조회 기능 개발                              |
|                                                                              |
| Work Package Details:                                                         |
| - Estimated Effort: 120 person-hours                                         |
| - Duration: 2 weeks                                                          |
| - Responsible: Backend Team Lead                                             |
| - Resources: 2 Senior Developers                                             |
|                                                                              |
| Acceptance Criteria:                                                          |
| 1. All CRUD operations functional                                            |
| 2. Unit test coverage >= 80%                                                 |
| 3. Code review passed                                                        |
| 4. API documentation complete                                                |
|                                                                              |
| Deliverables:                                                                 |
| - Source code (Git repository)                                               |
| - Unit test code                                                             |
| - API documentation                                                          |
| - Technical specification                                                    |
+==============================================================================+

================================================================================
```

### 3. 심층 동작 원리: WBS 작성 프로세스

```
[WBS 작성 5단계 프로세스]

STEP 1: 프로젝트 범위 정의
        |
        ├── 프로젝트 헌장(Project Charter) 검토
        ├── 요구사항 문서 분석
        ├── 범위 기술서(Scope Statement) 작성
        └── 제약사항 및 가정사항 식별
        |
        v
STEP 2: 상위 수준 분해 (Level 2)
        |
        ├── 분해 접근법 선택
        │   ├── 산출물 중심 (Deliverable-oriented) - 권장
        │   └── 단계 중심 (Phase-oriented)
        ├── 주요 산출물/단계 식별
        └── 100% 규칙 검증
        |
        v
STEP 3: 하위 수준 분해 (Level 3, 4...)
        |
        ├── 각 상위 요소를 하위 요소로 분해
        ├── 상호 배타성 확인
        ├── 관리 가능성 확인 (8/80 규칙)
        └── 작업 패키지 수준까지 분해
        |
        v
STEP 4: WBS 사전 작성
        |
        ├── 각 WBS 요소의 상세 정의
        ├── 완료 기준 정의
        ├── 책임자 지정
        └── 자원 및 비용 추정
        |
        v
STEP 5: 검증 및 승인
        |
        ├── 100% 규칙 최종 검증
        ├── 이해관계자 리뷰
        ├── 누락 항목 식별 및 추가
        └── 베이스라인 승인
```

### 4. WBS 분해 접근법 비교

| 접근법 | 설명 | 장점 | 단점 | 적용 사례 |
|:---|:---|:---|:---|:---|
| **산출물 중심** | 최종 결과물 기준 분해 | 범위 명확, 완료 기준 명확 | 활동 파악 어려울 수 있음 | **권장**, 일반적 |
| **단계 중심** | 프로젝트 단계 기준 분해 | 프로세스 이해 쉬움 | 산출물 간과 가능 | 폭포수 프로젝트 |
| **조직 중심** | 담당 조직 기준 분해 | 책임 명확 | 조직 간 의존성 간과 | 조직별 독립 프로젝트 |
| **기능 중심** | 시스템 기능 기준 분해 | 기능별 관리 용이 | 통합 간과 가능 | 소프트웨어 개발 |

### 5. 실무 코드 예시: WBS 관리 시스템

```python
"""
WBS (Work Breakdown Structure) 관리 시스템
Project Scope Management Implementation
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from enum import Enum
from datetime import datetime

class WBSStatus(Enum):
    PLANNED = "계획됨"
    IN_PROGRESS = "진행중"
    COMPLETED = "완료"
    ON_HOLD = "보류"
    CANCELLED = "취소"

@dataclass
class WorkPackage:
    """작업 패키지 (WBS 최하위 요소)"""
    wbs_code: str
    name: str
    description: str
    estimated_hours: float
    actual_hours: float = 0.0
    responsible: Optional[str] = None
    status: WBSStatus = WBSStatus.PLANNED
    acceptance_criteria: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # 의존 WBS 코드

    @property
    def progress_percentage(self) -> float:
        """진행률 계산"""
        if self.estimated_hours == 0:
            return 0.0
        return min(100.0, (self.actual_hours / self.estimated_hours) * 100)

    def is_work_package(self) -> bool:
        """작업 패키지 여부 (8~80시간 규칙)"""
        return 8 <= self.estimated_hours <= 80


@dataclass
class WBSNode:
    """WBS 노드 (계층 구조)"""
    wbs_code: str
    name: str
    description: str
    level: int                           # 계층 레벨 (1: 프로젝트, 2: 단계...)
    children: List['WBSNode'] = field(default_factory=list)
    work_package: Optional[WorkPackage] = None
    parent_code: Optional[str] = None

    @property
    def is_leaf(self) -> bool:
        """말단 노드 여부"""
        return len(self.children) == 0

    @property
    def total_estimated_hours(self) -> float:
        """하위 모든 작업 패키지의 총 추정 시간"""
        if self.work_package:
            return self.work_package.estimated_hours
        return sum(child.total_estimated_hours for child in self.children)

    @property
    def total_actual_hours(self) -> float:
        """하위 모든 작업 패키지의 총 실적 시간"""
        if self.work_package:
            return self.work_package.actual_hours
        return sum(child.total_actual_hours for child in self.children)

    @property
    def overall_progress(self) -> float:
        """전체 진행률"""
        if self.total_estimated_hours == 0:
            return 0.0
        return (self.total_actual_hours / self.total_estimated_hours) * 100

    def add_child(self, child: 'WBSNode') -> None:
        """자식 노드 추가"""
        child.parent_code = self.wbs_code
        child.level = self.level + 1
        self.children.append(child)

    def get_all_work_packages(self) -> List[WorkPackage]:
        """모든 작업 패키지 조회"""
        packages = []
        if self.work_package:
            packages.append(self.work_package)
        for child in self.children:
            packages.extend(child.get_all_work_packages())
        return packages

    def validate_100_percent(self) -> bool:
        """100% 규칙 검증"""
        # 모든 작업 패키지의 합이 상위 노드의 합과 일치하는지 확인
        children_sum = sum(
            child.total_estimated_hours for child in self.children
        )
        if self.work_package:
            return True  # Leaf 노드는 항상 True
        if len(self.children) == 0:
            return True
        # 자식들의 합과 현재 노드의 합 비교 (허용 오차 1%)
        return abs(children_sum - self.total_estimated_hours) < self.total_estimated_hours * 0.01


class WBSManager:
    """
    WBS 관리자
    WBS 생성, 수정, 분석 기능 제공
    """

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.root: Optional[WBSNode] = None
        self.nodes: Dict[str, WBSNode] = {}  # WBS 코드로 노드 조회

    def create_wbs(self, root_name: str, root_description: str) -> WBSNode:
        """WBS 루트 생성"""
        self.root = WBSNode(
            wbs_code="1.0",
            name=root_name,
            description=root_description,
            level=1
        )
        self.nodes["1.0"] = self.root
        return self.root

    def add_node(
        self,
        parent_code: str,
        wbs_code: str,
        name: str,
        description: str
    ) -> WBSNode:
        """WBS 노드 추가"""
        if parent_code not in self.nodes:
            raise ValueError(f"부모 노드 {parent_code}가 존재하지 않습니다")
        if wbs_code in self.nodes:
            raise ValueError(f"WBS 코드 {wbs_code}가 이미 존재합니다")

        parent = self.nodes[parent_code]
        new_node = WBSNode(
            wbs_code=wbs_code,
            name=name,
            description=description,
            level=parent.level + 1,
            parent_code=parent_code
        )
        parent.add_child(new_node)
        self.nodes[wbs_code] = new_node
        return new_node

    def add_work_package(
        self,
        wbs_code: str,
        name: str,
        description: str,
        estimated_hours: float,
        responsible: str,
        acceptance_criteria: List[str] = None,
        deliverables: List[str] = None
    ) -> WorkPackage:
        """작업 패키지 추가"""
        if wbs_code not in self.nodes:
            raise ValueError(f"WBS 노드 {wbs_code}가 존재하지 않습니다")

        node = self.nodes[wbs_code]
        work_package = WorkPackage(
            wbs_code=wbs_code,
            name=name,
            description=description,
            estimated_hours=estimated_hours,
            responsible=responsible,
            acceptance_criteria=acceptance_criteria or [],
            deliverables=deliverables or []
        )
        node.work_package = work_package
        return work_package

    def update_progress(
        self,
        wbs_code: str,
        actual_hours: float
    ) -> None:
        """진행 실적 업데이트"""
        if wbs_code not in self.nodes:
            raise ValueError(f"WBS 노드 {wbs_code}가 존재하지 않습니다")

        node = self.nodes[wbs_code]
        if node.work_package:
            node.work_package.actual_hours = actual_hours
            if actual_hours >= node.work_package.estimated_hours:
                node.work_package.status = WBSStatus.COMPLETED
            else:
                node.work_package.status = WBSStatus.IN_PROGRESS

    def get_wbs_tree(self) -> Dict:
        """WBS 트리 구조 반환"""
        if not self.root:
            return {}

        def build_tree(node: WBSNode) -> Dict:
            tree = {
                "wbs_code": node.wbs_code,
                "name": node.name,
                "level": node.level,
                "estimated_hours": node.total_estimated_hours,
                "actual_hours": node.total_actual_hours,
                "progress": f"{node.overall_progress:.1f}%",
                "children": []
            }
            for child in node.children:
                tree["children"].append(build_tree(child))
            return tree

        return build_tree(self.root)

    def get_wbs_dictionary(self) -> List[Dict]:
        """WBS 사전 생성"""
        dictionary = []
        for code, node in self.nodes.items():
            entry = {
                "wbs_code": code,
                "name": node.name,
                "description": node.description,
                "level": node.level,
                "parent": node.parent_code,
            }
            if node.work_package:
                entry.update({
                    "estimated_hours": node.work_package.estimated_hours,
                    "actual_hours": node.work_package.actual_hours,
                    "responsible": node.work_package.responsible,
                    "status": node.work_package.status.value,
                    "acceptance_criteria": node.work_package.acceptance_criteria,
                    "deliverables": node.work_package.deliverables
                })
            dictionary.append(entry)
        return dictionary

    def validate_wbs(self) -> Dict:
        """WBS 검증"""
        issues = []

        # 100% 규칙 검증
        for code, node in self.nodes.items():
            if not node.validate_100_percent():
                issues.append(f"100% 규칙 위반: {code}")

        # 8/80 규칙 검증
        for code, node in self.nodes.items():
            if node.work_package and not node.work_package.is_work_package():
                hours = node.work_package.estimated_hours
                if hours < 8:
                    issues.append(f"작업 패키지가 너무 작음: {code} ({hours}시간)")
                elif hours > 80:
                    issues.append(f"작업 패키지가 너무 큼: {code} ({hours}시간)")

        # 누락 항목 검증
        leaf_nodes = [
            node for node in self.nodes.values()
            if node.is_leaf and not node.work_package
        ]
        if leaf_nodes:
            issues.append(
                f"작업 패키지가 없는 말단 노드: {[n.wbs_code for n in leaf_nodes]}"
            )

        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "total_nodes": len(self.nodes),
            "total_work_packages": len(self.get_all_work_packages())
        }

    def get_all_work_packages(self) -> List[WorkPackage]:
        """모든 작업 패키지 조회"""
        if not self.root:
            return []
        return self.root.get_all_work_packages()

    def generate_report(self) -> Dict:
        """WBS 보고서 생성"""
        if not self.root:
            return {"message": "WBS가 생성되지 않았습니다"}

        work_packages = self.get_all_work_packages()
        total_estimated = sum(wp.estimated_hours for wp in work_packages)
        total_actual = sum(wp.actual_hours for wp in work_packages)

        by_status = {}
        for wp in work_packages:
            status = wp.status.value
            if status not in by_status:
                by_status[status] = 0
            by_status[status] += 1

        return {
            "project_name": self.project_name,
            "total_nodes": len(self.nodes),
            "total_work_packages": len(work_packages),
            "total_estimated_hours": total_estimated,
            "total_actual_hours": total_actual,
            "overall_progress": f"{(total_actual/total_estimated*100) if total_estimated > 0 else 0:.1f}%",
            "work_packages_by_status": by_status,
            "validation": self.validate_wbs()
        }


# ===== 실제 사용 예시 =====
if __name__ == "__main__":
    # WBS 관리자 생성
    wbs = WBSManager("이커머스 플랫폼 개발")

    # WBS 루트 생성
    wbs.create_wbs(
        "이커머스 플랫폼 개발",
        "온라인 쇼핑몰 플랫폼 개발 프로젝트"
    )

    # Level 2: 주요 단계
    wbs.add_node("1.0", "1.1", "요구사항 분석", "사용자 요구사항 수집 및 분석")
    wbs.add_node("1.0", "1.2", "설계", "시스템 설계")
    wbs.add_node("1.0", "1.3", "개발", "애플리케이션 개발")
    wbs.add_node("1.0", "1.4", "테스트", "품질 검증")
    wbs.add_node("1.0", "1.5", "배포", "운영 환경 구축")

    # Level 3: 세부 산출물
    wbs.add_node("1.1", "1.1.1", "비즈니스 분석", "비즈니스 요구사항 분석")
    wbs.add_node("1.1", "1.1.2", "기술 요구사항", "기술적 요구사항 정의")

    wbs.add_node("1.3", "1.3.1", "백엔드 개발", "서버 사이드 개발")
    wbs.add_node("1.3", "1.3.2", "프론트엔드 개발", "클라이언트 사이드 개발")

    # Level 4: 작업 패키지
    wbs.add_work_package(
        "1.1.1",
        "비즈니스 분석",
        "이해관계자 인터뷰 및 요구사항 정리",
        estimated_hours=40,
        responsible="김분석",
        acceptance_criteria=["요구사항 명세서 승인", "이해관계자 사인"],
        deliverables=["요구사항 명세서", "유스케이스 다이어그램"]
    )

    wbs.add_work_package(
        "1.3.1",
        "백엔드 개발",
        "API 서버 개발",
        estimated_hours=160,
        responsible="이백엔드",
        acceptance_criteria=["API 테스트 통과", "코드 리뷰 완료"],
        deliverables=["소스 코드", "API 문서", "단위 테스트"]
    )

    wbs.add_work_package(
        "1.3.2",
        "프론트엔드 개발",
        "웹 UI 개발",
        estimated_hours=120,
        responsible="박프론트",
        acceptance_criteria=["크로스 브라우저 테스트 통과", "반응형 구현"],
        deliverables=["소스 코드", "UI 컴포넌트 라이브러리"]
    )

    # 진행 상황 업데이트
    wbs.update_progress("1.1.1", 40)  # 완료
    wbs.update_progress("1.3.1", 80)  # 50% 진행
    wbs.update_progress("1.3.2", 30)  # 25% 진행

    # 보고서 생성
    report = wbs.generate_report()
    print("=== WBS 보고서 ===")
    print(f"총 노드 수: {report['total_nodes']}")
    print(f"총 작업 패키지 수: {report['total_work_packages']}")
    print(f"총 추정 시간: {report['total_estimated_hours']}시간")
    print(f"총 실적 시간: {report['total_actual_hours']}시간")
    print(f"전체 진행률: {report['overall_progress']}")
    print(f"상태별: {report['work_packages_by_status']}")
    print(f"검증 결과: {report['validation']}")
```

---

## III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교: 프로젝트 분해 도구 비교

| 비교 항목 | WBS | OBS | CBS | PBS |
|:---|:---|:---|:---|:---|
| **Full Name** | Work Breakdown Structure | Organization Breakdown | Cost Breakdown | Product Breakdown |
| **분해 기준** | 작업/산출물 | 조직 | 비용 | 제품 구성요소 |
| **주요 목적** | 범위 관리 | 책임 할당 | 비용 관리 | 제품 구조 |
| **프로젝트 관리 연계** | 일정, 비용 산정 | 인력 배치 | 예산 통제 | 요구사항 추적 |

### 2. WBS와 타 프로젝트 관리 기법 연계

```
[WBS + 프로젝트 관리 기법 연계]

WBS (범위)
    |
    +-- 연계 --> [일정 관리]
    |            - 각 작업 패키지의 기간 추정
    |            - CPM/PERT 네트워크 구성
    |            - 간트 차트 작성
    |
    +-- 연계 --> [비용 관리]
    |            - 각 작업 패키지별 비용 산정
    |            - EVM 성과 측정 기준
    |
    +-- 연계 --> [자원 관리]
    |            - 각 작업 패키지별 자원 할당
    |            - RACI 매트릭스 작성
    |
    +-- 연계 --> [위험 관리]
                 - 각 작업 패키지별 위험 식별
                 - 위험 등록부 구성
```

### 3. WBS vs 애자일 백로그

| 비교 항목 | WBS (전통적) | 애자일 백로그 |
|:---|:---|:---|
| **구조** | 계층적 (Tree) | 평면적 (List) |
| **분해 단위** | 작업 패키지 | 사용자 스토리 |
| **변경 빈도** | 낮음 (베이스라인) | 높음 (지속적) |
| **완료 기준** | 산출물 중심 | 가치 중심 |
| **계획 시점** | 초기에 상세 계획 | 스프린트마다 계획 |
| **적합 프로젝트** | 범위 확정적 | 범위 진화적 |

---

## IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 기술사적 판단 (실무 시나리오)

#### [시나리오 1] 대형 공공 SI 프로젝트

**상황**:
- 프로젝트: 관공서 전자결재 시스템 구축
- 규모: 100억 원, 30인, 18개월
- 특성: 범위 확정, 감사 대상

**기술사적 판단**:

```
선택: 상세 WBS 필수 작성

근거:
1. 감사 대상: WBS가 비용 집행의 근거
2. 범위 확정: 초기에 범위가 명확함
3. 계약 준거: WBS 기반 진척률 보고

WBS 작성 전략:
┌─────────────────────────────────────────────────────┐
│ Level 1: 프로젝트                                   │
│ Level 2: 7개 주요 단계 (계약 단위)                  │
│ Level 3: 35개 세부 산출물                          │
│ Level 4: 150+ 작업 패키지                          │
└─────────────────────────────────────────────────────┘

각 작업 패키지:
- 8~40시간 단위 (엄격한 8/80 규칙)
- 명확한 산출물 정의
- 승인 기준 명시
```

#### [시나리오 2] 스타트업 애자일 프로젝트

**상황**:
- 프로젝트: AI 챗봇 서비스
- 규모: 5인, 3개월 MVP
- 특성: 범위 불확실, 빠른 변화

**기술사적 판단**:

```
선택: 경량화된 WBS + 백로그

근거:
1. 변화 수용: 상세 WBS는 변경 비용이 높음
2. 애자일 적합: 백로그가 더 적합

하이브리드 접근:
┌─────────────────────────────────────────────────────┐
│ Level 1: 프로젝트 (MVP)                             │
│ Level 2: 에픽 (Epic) 단계                          │
│ Level 3: 사용자 스토리 (백로그)                     │
└─────────────────────────────────────────────────────┘

스프린트마다 백로그 리파인먼트로 진화
```

### 2. 도입 시 고려사항 (체크리스트)

**구조적 고려사항**:
- [ ] **분해 수준**: 어디까지 분해할 것인가? (3~5 level 권장)
- [ ] **작업 패키지 크기**: 8/80 규칙 준수 여부
- [ ] **분해 접근법**: 산출물 중심 vs 단계 중심
- [ ] **코딩 체계**: 일관된 WBS 코드 부여

**프로세스 고려사항**:
- [ ] **참여자**: 누가 WBS 작성에 참여할 것인가?
- [ ] **검증 프로세스**: 100% 규칙 검증 방법
- [ ] **변경 관리**: WBS 변경 시 승인 프로세스
- [ ] **도구**: WBS 작성 도구 선정

### 3. 주의사항 및 안티패턴

| 안티패턴 | 증상 | 원인 | 해결 방안 |
|:---|:---|:---|:---|
| **과도한 분해** | 작업 패키지가 2시간 단위 | 관리 욕심 | 8/80 규칙 준수 |
| **불충분한 분해** | 작업 패키지가 200시간 | 시간 부족 | 추가 분해 |
| **활동 중심 분해** | "회의하기", "검토하기" | 산출물 중심 원칙 미이해 | 산출물 중심 재작성 |
| **100% 규칙 위반** | 하위 합 ≠ 상위 합 | 분해 오류 | 검증 프로세스 도입 |
| **WBS 사전 미작성** | 완료 기준 불명확 | 문서화 게으름 | WBS 사전 의무화 |

---

## V. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 지표 | 적용 전 | 적용 후 | 개선 효과 |
|:---|:---|:---:|:---:|:---:|
| **범위 누락** | 누락 작업 발견률 | 30% | 5% | -83% |
| **일정 정확도** | 일정 준수율 | 50% | 75% | +25%p |
| **비용 정확도** | 예산 준수율 | 55% | 80% | +25%p |
| **책임 명확성** | 책임 소재 분쟁 | 빈번 | 드묾 | -90% |
| **의사소통** | 범위 이해도 | 60% | 95% | +35%p |

### 2. 미래 전망 및 진화 방향

1. **AI 기반 WBS 자동 생성**:
   - 유사 프로젝트 데이터 학습
   - 요구사항에서 WBS 자동 도출

2. **실시간 WBS 동기화**:
   - 클라우드 기반 협업
   - 자동 진행률 계산

3. **애자일-하이브리드 WBS**:
   - Rolling Wave Planning과 결합
   - 동적 WBS 업데이트

### 3. 참고 표준/가이드

| 표준/가이드 | 내용 | 적용 분야 |
|:---|:---|:---|
| **PMBOK Guide** | 범위 관리 - WBS 작성 가이드 | 범용 |
| **MIL-STD-881** | 국방 프로젝트 WBS 표준 | 국방/군사 |
| **ISO 21500** | 프로젝트 관리 - WBS 지침 | 국제 표준 |
| **IEEE 1490** | 소프트웨어 WBS 가이드 | 소프트웨어 |

---

## 관련 개념 맵 (Knowledge Graph)

- [프로젝트 관리](@/studynotes/4_software_engineering/3_project/_index.md) : WBS의 상위 개념
- [EVM](@/studynotes/4_software_engineering/3_project/project_management_evm.md) : WBS 기반 성과 측정
- [CPM/PERT](@/studynotes/4_software_engineering/3_project/_index.md) : WBS 기반 일정 관리
- [요구공학](@/studynotes/4_software_engineering/4_requirements/requirements_engineering.md) : WBS 작성의 입력
- [형상 관리](@/studynotes/4_software_engineering/1_sdlc/configuration_management.md) : WBS 베이스라인 관리
- [애자일 백로그](@/studynotes/4_software_engineering/1_sdlc/scrum_framework.md) : 애자일 방식의 범위 관리

---

## 어린이를 위한 3줄 비유 설명

1. **문제**: 큰 숙제를 해야 하는데 "방 청소하기"라고만 쓰여 있어요. 뭘부터 해야 할지 모르겠어요!

2. **해결(WBS)**: 숙제를 작은 단위로 나누어 써요. "책상 정리" - "옷장 정리" - "바닥 쓸기" - "걸레질". 이렇게 나누면 하나씩 할 수 있죠!

3. **효과**: 뭘 해야 할지 한눈에 보여요! 얼마나 남았는지도 알 수 있고, 엄마한테 "이거 다 했어!" 하고 보여줄 수도 있죠. WBS는 프로젝트를 이렇게 작은 단위로 나누는 방법이에요.
