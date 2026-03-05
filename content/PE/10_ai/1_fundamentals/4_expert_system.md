+++
title = "전문가 시스템 (Expert System)"
date = "2026-03-05"
[extra]
categories = ["studynotes-10_ai"]
+++

# 전문가 시스템 (Expert System)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 특정 분야 전문가의 지식과 추론 능력을 컴퓨터에 구현한 시스템으로, 지식 베이스(Knowledge Base)와 추론 엔진(Inference Engine)의 두 가지 핵심 구성 요소로 이루어집니다. 인간 전문가가 수행하던 의사결정, 진단, 설계 등의 작업을 규칙 기반(Rule-based)으로 자동화합니다.
> 2. **가치**: 1970-80년대 AI의 상업적 성공 사례로, 의료 진단(MYCIN), 화학 분석(DENDRAL), 장비 고장 진단 등에서 전문가 수준의 성능을 달성했습니다. 현대 XAI(설명 가능한 AI), 의사결정 지원 시스템, 규칙 기반 챗봇의 기술적 원형입니다.
> 3. **융합**: 지식 표현(논리학, 철학), 추론(수학, 논리학), 인간-컴퓨터 상호작용(Cognitive Science), 데이터베이스(컴퓨터과학)의 융합 기술입니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**전문가 시스템 (Expert System)**은 특정 전문 분야(의료, 법률, 공학, 금융 등)에서 인간 전문가가 수행하는 고도의 지적 작업을 컴퓨터 시스템으로 구현한 것입니다. 1970년대 스탠퍼드 대학의 에드워드 파이젠바움(Edward Feigenbaum)이 이끄는 연구팀이 개발했습니다.

**핵심 구성 요소**:

```
전문가 시스템 = 지식 베이스 + 추론 엔진 + 사용자 인터페이스

┌─────────────────────────────────────────────────────┐
│                  Expert System                      │
│                                                     │
│  ┌─────────────┐         ┌─────────────────────┐  │
│  │ Knowledge   │         │   Inference Engine  │  │
│  │ Base        │◄───────►│                     │  │
│  │             │         │   - Forward Chain   │  │
│  │ - Facts     │         │   - Backward Chain  │  │
│  │ - Rules     │         │   - Uncertainty     │  │
│  │ - Heuristics│         │                     │  │
│  └─────────────┘         └──────────┬──────────┘  │
│         ▲                           │              │
│         │                           ▼              │
│  ┌──────┴──────┐          ┌─────────────────────┐ │
│  │ Knowledge   │          │   User Interface    │ │
│  │ Engineer    │          │   (Explanation)     │ │
│  │ (인간)      │          │                     │ │
│  └─────────────┘          └─────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**지식 베이스 (Knowledge Base)**:
- **사실 (Facts)**: "환자의 체온이 39도이다", "기계의 압력이 비정상이다"
- **규칙 (Rules)**: "IF 체온 > 38도 AND 기침 = 있음 THEN 감기일 확률 = 0.8"
- **휴리스틱 (Heuristics)**: 전문가의 경험적 지식, 경험 법칙

**추론 엔진 (Inference Engine)**:
- **전향 추론 (Forward Chaining)**: 데이터 → 결론 (데이터 주도)
- **후향 추론 (Backward Chaining)**: 가설 → 데이터 검증 (목표 주도)
- **불확실성 처리**: 확률, 확신도(Certainty Factor), 퍼지 논리

#### 2. 비유를 통한 이해

전문가 시스템은 **"요리책을 가진 요리사"** 또는 **"체크리스트를 가진 검사관"**에 비유할 수 있습니다:

**요리책 비유**:
```
[요리사]
- 재료 확인: "계란, 밀가루, 설탕이 있다"
- 요리책 규칙 조회: "IF 재료 = 계란+밀가루+설탕 THEN 케이크를 만들 수 있다"
- 결과: "케이크를 만들겠습니다"
- 설명: "요리책 12페이지에 따르면..."

[전문가 시스템]
- 데이터 확인: "환자의 체온이 39도, 기침 있음"
- 지식 베이스 규칙 조회: "IF 체온>38 AND 기침 THEN 감기일 확률=0.8"
- 결과: "감기 진단 (확신도 0.8)"
- 설명: "규칙 R-127에 따르면..."
```

**의사 비유**:
```
숙련된 의사:
"환자가 열이 있고 기침을 하네. 이 시기에 유행하는 독감 증상이야.
 독감 의심되니 독감 검사를 하자."

전문가 시스템:
Rule 1: IF 체온 > 38 AND 기침 = 있음 THEN 감염의심 (CF=0.7)
Rule 2: IF 감염의심 AND 계절 = 겨울 THEN 독감의심 (CF=0.8)
Rule 3: IF 독감의심 THEN 독감검사 권장 (CF=0.9)

결론: 독감검사 권장 (CF=0.504)
```

#### 3. 등장 배경 및 발전 과정

**역사적 이정표**:

| 연도 | 시스템 | 개발자 | 분야 | 의미 |
|:---|:---|:---|:---|:---|
| 1965 | DENDRAL | 스탠퍼드 대학 | 화학 | 최초의 전문가 시스템, 분자 구조 추론 |
| 1972 | MYCIN | 스탠퍼드 대학 | 의료 | 혈액 감염 진단, 전문가 수준 성능 |
| 1978 | PROSPECTOR | SRI | 지질 | 광물 탐사, 몰리브덴 광상 발견 |
| 1980 | XCON (R1) | CMU/DEC | 컴퓨터 | VAX 컴퓨터 구성, 상업적 성공 |
| 1984 | CLIPS | NASA | 범용 | 공개 소스 전문가 시스템 도구 |
| 1980s | 상업화 | 다수 | 다양 | 연간 수십억 달러 시장 형성 |
| 1990s | 쇠퇴 | - | - | 유지보수 문제, 지식 획득 병목 |
| 2010s | 부활 | - | - | XAI, 규칙 기반 시스템, 하이브리드 AI |

**AI의 겨울과 전문가 시스템**:
```
1차 AI 붐 (1950s-60s): 일반 문제 해결기 (GPS), 퍼셉트론
1차 AI 겨울 (1974-1980): 과대 광고, 한계 노출

2차 AI 붐 (1980-87): 전문가 시스템 붐!
- 일본 Fifth Generation Computer Systems
- 미국, 유럽의 대규모 투자
- 상업적 성공: XCON, 유전자 분석 등

2차 AI 겨울 (1987-1993):
- 지식 획득 병목 (Knowledge Acquisition Bottleneck)
- 유지보수 비용 증가
- 규칙 폭발 (Rule Explosion)
- 기계 학습의 부상
```

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 전문가 시스템 구성 요소 상세 (표)

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술 | 비유 |
|:---|:---|:---|:---|:---|
| **지식 베이스** | 도메인 지식 저장 | 규칙, 프레임, 의미망 표현 | Prolog, OPS5 | 요리책 |
| **추론 엔진** | 논리적 결론 도출 | 패턴 매칭, 탐색, 충돌 해결 | Rete 알고리즘 | 요리사 |
| **지식 획득** | 지식 입력/수정 | 인터뷰, 기계 학습 | KE 도구 | 요리 연구가 |
| **사용자 인터페이스** | 질문-답변 상호작용 | 자연어, 메뉴, 그래픽 | GUI, NLP | 웨이터 |
| **설명 기능** | 추론 과정 설명 | 규칙 추적, Why/How 질문 | 트리 탐색 | 요리 강사 |
| **작업 기억** | 현재 상태 저장 | 사실 추가/수정/삭제 | 팩트 베이스 | 조리대 |

#### 2. 전문가 시스템 아키텍처 다이어그램

```text
<<< Expert System Architecture >>>

┌─────────────────────────────────────────────────────────────────┐
│                     EXPERT SYSTEM SHELL                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    ┌───────────────────────────────────────────────────────┐   │
│    │                 USER INTERFACE                         │   │
│    │   ┌─────────┐  ┌─────────┐  ┌─────────────────────┐  │   │
│    │   │ Query   │  │ Result  │  │   Explanation       │  │   │
│    │   │ Input   │  │ Display │  │   - Why?            │  │   │
│    │   └────┬────┘  └────▲────┘  │   - How?            │  │   │
│    │        │            │       │   - Trace           │  │   │
│    │        └────────────┼───────┴─────────────────────┘  │   │
│    │                     │                                  │   │
│    └─────────────────────┼──────────────────────────────────┘   │
│                          │                                      │
│    ┌─────────────────────┼──────────────────────────────────┐   │
│    │            INFERENCE ENGINE                              │   │
│    │                                                          │   │
│    │   ┌──────────────┐      ┌──────────────────────────┐   │   │
│    │   │   Pattern    │◄────►│      Rule Selection      │   │   │
│    │   │   Matcher    │      │   - Conflict Resolution  │   │   │
│    │   │              │      │   - Agenda               │   │   │
│    │   └──────┬───────┘      └────────────┬─────────────┘   │   │
│    │          │                           │                  │   │
│    │          │  ┌────────────────────────┘                  │   │
│    │          │  │                                           │   │
│    │          ▼  ▼                                           │   │
│    │   ┌─────────────────┐      ┌─────────────────────┐     │   │
│    │   │ Forward Chaining│◄────►│  Backward Chaining  │     │   │
│    │   │ (Data-driven)   │      │  (Goal-driven)      │     │   │
│    │   └────────┬────────┘      └──────────┬──────────┘     │   │
│    │            │                          │                 │   │
│    └────────────┼──────────────────────────┼─────────────────┘   │
│                 │                          │                     │
│    ┌────────────┼──────────────────────────┼─────────────────┐   │
│    │    WORKING MEMORY (Fact Base)         │                 │   │
│    │                                       │                 │   │
│    │   Fact 1: (patient fever 39)          │                 │   │
│    │   Fact 2: (patient cough yes)         │                 │   │
│    │   Fact 3: (diagnosis ?x)              │                 │   │
│    │                                       │                 │   │
│    └───────────────────┬───────────────────┘                 │   │
│                        │                                     │   │
│    ┌───────────────────┼─────────────────────────────────────┐   │
│    │            KNOWLEDGE BASE                                │   │
│    │                                                          │   │
│    │   ┌─────────────────────────────────────────────────┐   │   │
│    │   │   RULE BASE (Production Rules)                  │   │   │
│    │   │                                                  │   │   │
│    │   │   R1: IF fever > 38 AND cough = yes             │   │   │
│    │   │       THEN infection_suspected (CF=0.7)         │   │   │
│    │   │                                                  │   │   │
│    │   │   R2: IF infection_suspected AND season=winter  │   │   │
│    │   │       THEN flu_suspected (CF=0.8)               │   │   │
│    │   │                                                  │   │   │
│    │   │   R3: IF flu_suspected                          │   │   │
│    │   │       THEN recommend flu_test (CF=0.9)          │   │   │
│    │   └─────────────────────────────────────────────────┘   │   │
│    │                                                          │   │
│    │   ┌─────────────────────────────────────────────────┐   │   │
│    │   │   FACT BASE (Domain Facts)                      │   │   │
│    │   │                                                  │   │   │
│    │   │   F1: normal_body_temp = 36.5                    │   │   │
│    │   │   F2: flu_season = winter                        │   │   │
│    │   └─────────────────────────────────────────────────┘   │   │
│    │                                                          │   │
│    └──────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

<<< 추론 방식 비교 >>>

    [Forward Chaining - 전향 추론]     [Backward Chaining - 후향 추론]
            (데이터 주도)                      (목표 주도)

    Data ──► Rule ──► New Fact          Goal ◄── Rule ◄── Sub-goal
     │                     │              │                        │
     ▼                     ▼              ▼                        ▼
    (체온 39도)         (감염 의심)    (독감 진단?)           (체온 확인 필요)
     │                     │              │                        │
     ▼                     ▼              ▼                        ▼
    (기침 있음) ────► (독감 의심)      (검사 권장?)           (계절 확인 필요)
```

#### 3. 심층 동작 원리: 추론 과정

**전향 추론 (Forward Chaining) 예시**:

```
초기 사실:
- F1: (patient temperature 39)
- F2: (patient cough yes)
- F3: (current_season winter)

규칙:
- R1: IF (patient temperature ?t) AND (> ?t 38) AND (patient cough yes)
      THEN (infection_suspected CF=0.7)
- R2: IF (infection_suspected) AND (current_season winter)
      THEN (flu_suspected CF=0.8)
- R3: IF (flu_suspected)
      THEN (recommend flu_test CF=0.9)

추론 과정:
1. 패턴 매칭: R1의 조건이 F1, F2와 매칭
   - ?t = 39, 39 > 38 = true
2. 규칙 발화 (Fire R1):
   - 새로운 사실 추가: (infection_suspected CF=0.7)
3. 패턴 매칭: R2의 조건이 매칭
   - infection_suspected 있음, season = winter
4. 규칙 발화 (Fire R2):
   - 새로운 사실 추가: (flu_suspected CF=0.56)  // 0.7 * 0.8
5. 패턴 매칭: R3의 조건이 매칭
6. 규칙 발화 (Fire R3):
   - 새로운 사실 추가: (recommend flu_test CF=0.504)  // 0.56 * 0.9

최종 결론: 독감 검사 권장 (확신도 50.4%)
```

**후향 추론 (Backward Chaining) 예시**:

```
목표: (recommend flu_test)가 참인가?

1. 목표를 만족시키는 규칙 찾기: R3
   - R3의 결론이 (recommend flu_test)

2. R3의 조건을 서브목표로 설정: (flu_suspected)?

3. (flu_suspected)를 만족시키는 규칙 찾기: R2
   - R2의 결론이 (flu_suspected)

4. R2의 조건을 서브목표로 설정:
   - (infection_suspected)?
   - (current_season winter)?

5. (current_season winter) 확인: F3에서 참
   (infection_suspected)를 만족시키는 규칙 찾기: R1

6. R1의 조건을 서브목표로 설정:
   - (patient temperature ?t) AND (> ?t 38) AND (patient cough yes)?

7. 조건 확인:
   - F1: (patient temperature 39) → ?t = 39
   - 39 > 38 → 참
   - F2: (patient cough yes) → 참

8. 역순으로 결론 도출:
   - R1 발화 → (infection_suspected)
   - R2 발화 → (flu_suspected)
   - R3 발화 → (recommend flu_test)

최종 결론: 독감 검사 권장 (목표 달성)
```

#### 4. 실무 수준의 전문가 시스템 구현

```python
"""
Production-Ready Expert System Implementation
- 규칙 기반 추론 엔진
- 전향/후향 추론 지원
- 확신도(Certainty Factor) 계산
- 설명 기능
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Any, Callable
from enum import Enum
from collections import defaultdict
import re

class FactType(Enum):
    BOOLEAN = "boolean"
    NUMERIC = "numeric"
    SYMBOLIC = "symbolic"

@dataclass
class Fact:
    """사실 (Fact) 표현"""
    name: str
    value: Any
    certainty: float = 1.0  # 확신도 (0.0 ~ 1.0)
    source: str = "user"    # 출처: user, derived

    def __hash__(self):
        return hash((self.name, str(self.value)))

    def __eq__(self, other):
        if not isinstance(other, Fact):
            return False
        return self.name == other.name and self.value == other.value

@dataclass
class Condition:
    """규칙 조건"""
    fact_name: str
    operator: str  # "=", ">", "<", ">=", "<=", "!=", "exists"
    value: Any

    def evaluate(self, facts: Dict[str, Fact]) -> Tuple[bool, float]:
        """조건 평가"""
        if self.fact_name not in facts:
            if self.operator == "exists":
                return False, 0.0
            return False, 0.0

        fact = facts[self.fact_name]

        if self.operator == "exists":
            return True, fact.certainty
        elif self.operator == "=":
            result = fact.value == self.value
            return result, fact.certainty if result else 0.0
        elif self.operator == ">":
            try:
                result = float(fact.value) > float(self.value)
                return result, fact.certainty if result else 0.0
            except (TypeError, ValueError):
                return False, 0.0
        elif self.operator == "<":
            try:
                result = float(fact.value) < float(self.value)
                return result, fact.certainty if result else 0.0
            except (TypeError, ValueError):
                return False, 0.0
        elif self.operator == ">=":
            try:
                result = float(fact.value) >= float(self.value)
                return result, fact.certainty if result else 0.0
            except (TypeError, ValueError):
                return False, 0.0
        elif self.operator == "<=":
            try:
                result = float(fact.value) <= float(self.value)
                return result, fact.certainty if result else 0.0
            except (TypeError, ValueError):
                return False, 0.0
        elif self.operator == "!=":
            result = fact.value != self.value
            return result, fact.certainty if result else 0.0

        return False, 0.0

@dataclass
class Rule:
    """생산 규칙 (Production Rule)"""
    name: str
    conditions: List[Condition]
    conclusion_name: str
    conclusion_value: Any
    certainty_factor: float = 1.0
    description: str = ""

    def evaluate_conditions(self, facts: Dict[str, Fact]) -> Tuple[bool, float]:
        """모든 조건 평가"""
        if not self.conditions:
            return True, 1.0

        all_met = True
        min_certainty = 1.0

        for condition in self.conditions:
            met, certainty = condition.evaluate(facts)
            if not met:
                all_met = False
                break
            min_certainty = min(min_certainty, certainty)

        return all_met, min_certainty

class WorkingMemory:
    """작업 기억 (Working Memory)"""

    def __init__(self):
        self.facts: Dict[str, Fact] = {}
        self.fact_history: List[Tuple[str, Fact, str]] = []  # (action, fact, rule)

    def add_fact(self, fact: Fact, source_rule: str = "user"):
        """사실 추가"""
        key = fact.name
        if key in self.facts:
            # 확신도 결합 (CF combination)
            old_cf = self.facts[key].certainty
            new_cf = fact.certainty
            combined_cf = old_cf + new_cf * (1 - old_cf)
            fact.certainty = combined_cf

        self.facts[key] = fact
        self.fact_history.append(("add", fact, source_rule))

    def remove_fact(self, fact_name: str):
        """사실 제거"""
        if fact_name in self.facts:
            del self.facts[fact_name]

    def get_fact(self, name: str) -> Optional[Fact]:
        """사실 조회"""
        return self.facts.get(name)

    def get_all_facts(self) -> Dict[str, Fact]:
        """모든 사실 반환"""
        return self.facts.copy()

class KnowledgeBase:
    """지식 베이스"""

    def __init__(self):
        self.rules: List[Rule] = []
        self.domain_facts: Dict[str, Fact] = {}

    def add_rule(self, rule: Rule):
        """규칙 추가"""
        self.rules.append(rule)

    def add_domain_fact(self, fact: Fact):
        """도메인 사실 추가"""
        self.domain_facts[fact.name] = fact

    def get_applicable_rules(self, facts: Dict[str, Fact]) -> List[Tuple[Rule, float]]:
        """적용 가능한 규칙 반환"""
        applicable = []
        for rule in self.rules:
            met, certainty = rule.evaluate_conditions(facts)
            if met:
                applicable.append((rule, certainty))
        return applicable

class InferenceEngine:
    """추론 엔진"""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.working_memory = WorkingMemory()
        self.explanation_trace: List[str] = []
        self.conflict_resolution_strategy = "specificity"  # specificity, recency, random

    def initialize(self, initial_facts: Dict[str, Fact]):
        """초기화"""
        self.working_memory.facts.clear()
        self.working_memory.fact_history.clear()
        self.explanation_trace.clear()

        # 도메인 사실 추가
        for fact in self.kb.domain_facts.values():
            self.working_memory.add_fact(fact, "domain")

        # 초기 사실 추가
        for fact in initial_facts.values():
            self.working_memory.add_fact(fact, "user")

    def forward_chaining(self, max_iterations: int = 100) -> Dict[str, Fact]:
        """전향 추론"""
        iteration = 0
        new_facts_added = True

        while new_facts_added and iteration < max_iterations:
            new_facts_added = False
            iteration += 1

            # 현재 사실로 적용 가능한 규칙 찾기
            applicable = self.kb.get_applicable_rules(
                self.working_memory.get_all_facts()
            )

            # 충돌 해결
            if self.conflict_resolution_strategy == "specificity":
                # 조건이 많은 규칙 우선
                applicable.sort(key=lambda x: len(x[0].conditions), reverse=True)

            # 규칙 적용
            for rule, condition_certainty in applicable:
                # 결론의 확신도 계산
                conclusion_certainty = condition_certainty * rule.certainty_factor

                # 이미 결론 사실이 있는지 확인
                existing = self.working_memory.get_fact(rule.conclusion_name)

                if existing is None or existing.certainty < conclusion_certainty:
                    # 새 사실 생성
                    new_fact = Fact(
                        name=rule.conclusion_name,
                        value=rule.conclusion_value,
                        certainty=conclusion_certainty,
                        source=f"rule:{rule.name}"
                    )

                    # 설명 기록
                    self.explanation_trace.append(
                        f"[{rule.name}] 적용: {rule.conclusion_name}={rule.conclusion_value} "
                        f"(CF={conclusion_certainty:.2f})"
                    )

                    # 사실 추가
                    self.working_memory.add_fact(new_fact, rule.name)
                    new_facts_added = True

        return self.working_memory.get_all_facts()

    def backward_chaining(self, goal_name: str, goal_value: Any = None) -> Tuple[bool, float, List[str]]:
        """후향 추론"""
        trace = []

        def prove(name: str, value: Any = None, depth: int = 0) -> Tuple[bool, float]:
            indent = "  " * depth

            # 이미 사실로 존재하는지 확인
            existing = self.working_memory.get_fact(name)
            if existing is not None:
                if value is None or existing.value == value:
                    trace.append(f"{indent}✓ {name}={existing.value} (기존 사실, CF={existing.certainty:.2f})")
                    return True, existing.certainty
                else:
                    trace.append(f"{indent}✗ {name}={value} (기존 사실과 불일치)")
                    return False, 0.0

            # 이 결론을 도출하는 규칙 찾기
            matching_rules = [
                rule for rule in self.kb.rules
                if rule.conclusion_name == name
            ]

            if not matching_rules:
                trace.append(f"{indent}✗ {name} (증명할 규칙 없음)")
                return False, 0.0

            # 각 규칙 시도
            best_result = (False, 0.0)

            for rule in matching_rules:
                if value is not None and rule.conclusion_value != value:
                    continue

                trace.append(f"{indent}[{rule.name}] 시도: {name}={rule.conclusion_value}")

                # 모든 조건 증명
                all_conditions_met = True
                min_certainty = 1.0

                for condition in rule.conditions:
                    condition_met, condition_cf = prove(
                        condition.fact_name,
                        condition.value if condition.operator == "=" else None,
                        depth + 1
                    )

                    if not condition_met:
                        all_conditions_met = False
                        break

                    min_certainty = min(min_certainty, condition_cf)

                if all_conditions_met:
                    conclusion_cf = min_certainty * rule.certainty_factor
                    trace.append(f"{indent}✓ {rule.name} 성공 (CF={conclusion_cf:.2f})")

                    # 사실로 추가
                    new_fact = Fact(
                        name=name,
                        value=rule.conclusion_value,
                        certainty=conclusion_cf,
                        source=f"rule:{rule.name}"
                    )
                    self.working_memory.add_fact(new_fact, rule.name)

                    if conclusion_cf > best_result[1]:
                        best_result = (True, conclusion_cf)

            if not best_result[0]:
                trace.append(f"{indent}✗ {name} (모든 규칙 실패)")

            return best_result

        success, certainty = prove(goal_name, goal_value)
        return success, certainty, trace

    def explain(self) -> str:
        """추론 과정 설명"""
        explanation = ["=== 추론 과정 설명 ===\n"]

        for entry in self.explanation_trace:
            explanation.append(f"  {entry}")

        explanation.append("\n=== 최종 결론 ===\n")

        for name, fact in self.working_memory.get_all_facts().items():
            if fact.source.startswith("rule:"):
                explanation.append(f"  {name} = {fact.value} (확신도: {fact.certainty:.1%})")

        return "\n".join(explanation)

    def get_conclusions(self) -> List[Fact]:
        """결론 사실만 반환"""
        return [
            fact for fact in self.working_memory.get_all_facts().values()
            if fact.source.startswith("rule:")
        ]


# 의료 진단 전문가 시스템 예시
def create_medical_diagnosis_system() -> Tuple[KnowledgeBase, InferenceEngine]:
    """의료 진단 전문가 시스템 생성"""

    kb = KnowledgeBase()

    # 규칙 정의
    rules = [
        Rule(
            name="R1",
            conditions=[
                Condition("fever", ">", 38),
                Condition("cough", "=", "yes")
            ],
            conclusion_name="infection_suspected",
            conclusion_value="true",
            certainty_factor=0.7,
            description="발열 + 기침 → 감염 의심"
        ),
        Rule(
            name="R2",
            conditions=[
                Condition("infection_suspected", "=", "true"),
                Condition("season", "=", "winter")
            ],
            conclusion_name="flu_suspected",
            conclusion_value="true",
            certainty_factor=0.8,
            description="감염 의심 + 겨울 → 독감 의심"
        ),
        Rule(
            name="R3",
            conditions=[
                Condition("flu_suspected", "=", "true"),
                Condition("body_ache", "=", "yes")
            ],
            conclusion_name="flu_diagnosis",
            conclusion_value="high_probability",
            certainty_factor=0.85,
            description="독감 의심 + 근육통 → 독감 진단"
        ),
        Rule(
            name="R4",
            conditions=[
                Condition("flu_suspected", "=", "true")
            ],
            conclusion_name="recommend_flu_test",
            conclusion_value="yes",
            certainty_factor=0.9,
            description="독감 의심 → 독감 검사 권장"
        ),
        Rule(
            name="R5",
            conditions=[
                Condition("fever", ">", 39),
                Condition("headache", "=", "severe"),
                Condition("neck_stiffness", "=", "yes")
            ],
            conclusion_name="meningitis_suspected",
            conclusion_value="urgent",
            certainty_factor=0.9,
            description="고열 + 심한 두통 + 목 뻣뻣함 → 수막염 의심 (응급)"
        ),
    ]

    for rule in rules:
        kb.add_rule(rule)

    # 도메인 사실
    kb.add_domain_fact(Fact("season", "winter", 1.0, "domain"))
    kb.add_domain_fact(Fact("normal_body_temp", 36.5, 1.0, "domain"))

    engine = InferenceEngine(kb)
    return kb, engine


# 사용 예시
if __name__ == "__main__":
    kb, engine = create_medical_diagnosis_system()

    # 환자 데이터
    patient_facts = {
        "fever": Fact("fever", 39.2, 1.0, "user"),
        "cough": Fact("cough", "yes", 1.0, "user"),
        "body_ache": Fact("body_ache", "yes", 1.0, "user"),
        "headache": Fact("headache", "mild", 1.0, "user"),
        "neck_stiffness": Fact("neck_stiffness", "no", 1.0, "user"),
    }

    # 초기화 및 전향 추론
    engine.initialize(patient_facts)
    conclusions = engine.forward_chaining()

    print("\n" + "="*50)
    print("환자 데이터:")
    for name, fact in patient_facts.items():
        print(f"  {name}: {fact.value}")

    print("\n" + "="*50)
    print("진단 결과:")
    for conclusion in engine.get_conclusions():
        print(f"  {conclusion.name}: {conclusion.value} (확신도: {conclusion.certainty:.1%})")

    print("\n" + engine.explain())

    # 후향 추론 테스트
    print("\n" + "="*50)
    print("후향 추론 테스트: 'flu_diagnosis'가 참인가?")

    engine.initialize(patient_facts)
    success, certainty, trace = engine.backward_chaining("flu_diagnosis", "high_probability")

    print(f"\n결과: {'성공' if success else '실패'} (확신도: {certainty:.1%})")
    print("\n추론 경로:")
    for line in trace:
        print(line)
```

---

### III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 지식 표현 방식 비교

| 방식 | 장점 | 단점 | 적용 분야 |
|:---|:---|:---|:---|
| **규칙 (Rules)** | 직관적, 수정 용이 | 규칙 폭발, 일관성 유지 어려움 | 진단, 구성 |
| **프레임 (Frames)** | 객체 지향적, 상속 | 유연성 부족 | 분류, 설명 |
| **의미망 (Semantic Net)** | 관계 표현 용이 | 추론 복잡 | 자연어 이해 |
| **온톨로지 (Ontology)** | 표준화, 공유 가능 | 구축 비용 | 지식 공유 |
| **논리 (Logic)** | 엄밀한 추론 | 불확실성 처리 어려움 | 수학적 증명 |

#### 2. 전문가 시스템 vs 머신러닝 비교

| 특성 | 전문가 시스템 | 머신러닝 |
|:---|:---|:---|
| **지식 획득** | 인간 전문가 인터뷰 | 데이터에서 자동 학습 |
| **설명 가능성** | 높음 (규칙 추적) | 낮음 (블랙박스) |
| **데이터 요구** | 낮음 | 높음 |
| **적응성** | 낮음 (수동 업데이트) | 높음 (재학습) |
| **불확실성 처리** | CF, 퍼지 논리 | 확률적 방법 |
| **유지보수** | 어려움 (규칙 폭발) | 재학습으로 해결 |
| **현재 활용** | 규제, 설명 필요 분야 | 일반적 AI 응용 |

#### 3. 과목 융합 관점 분석

**[전문가 시스템 + 데이터베이스]**:
- 지식 베이스 저장 및 관리
- 규칙 인덱싱으로 빠른 검색
- 대규모 팩트 베이스 관리

**[전문가 시스템 + NLP]**:
- 자연어로 규칙 입력
- 질문-답변 인터페이스
- 설명 생성 자연화

**[전문가 시스템 + 머신러닝]**:
- 하이브리드 AI: 규칙 + 학습
- 규칙 자동 생성 (Rule Extraction)
- 지식 베이스 자동 갱신

---

### IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단: 실무 시나리오

**시나리오 A: 금융 규제 준수 시스템**
- **상황**: 은행의 대출 심사 자동화
- **요구사항**: 규제 요건 준수, 결정 이유 설명 가능
- **기술사 판단**:
  1. **전문가 시스템 적합**: 규제는 규칙 기반, 설명 필수
  2. **하이브리드 접근**:
     - 규칙 기반: 규제 준수 체크 (전문가 시스템)
     - ML 기반: 신용 점수 예측 (머신러닝)
  3. **구현**: 규칙 우선 → ML 보조
  4. **감사 추적**: 모든 결정에 규칙 적용 기록

**시나리오 B: 의료 진단 보조 시스템**
- **상황**: 병원의 진단 보조 시스템
- **기술사 판단**:
  1. **설명 가능성 필수**: 의사가 이해해야 함
  2. **불확실성 처리**: 환자마다 다른 증상
  3. **하이브리드**:
     - 증상-질병 매핑: 전문가 시스템
     - 의료 영상 분석: 딥러닝
  4. **최종 판단**: 인간 의사

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **지식 획득 가능성**: 전문가 지식을 규칙로 표현할 수 있는가?
- [ ] **규칙 수**: 관리 가능한 수준인가? (< 10,000개 권장)
- [ ] **설명 필요성**: 결정 이유 설명이 필요한가?
- [ ] **데이터 가용성**: 학습 데이터가 충분한가?
- [ ] **유지보수**: 지식 갱신 빈도와 비용
- [ ] **규제 요건**: 설명 가능성 법적 요구사항

#### 3. 안티패턴 (Anti-patterns)

**안티패턴 1: 규칙 폭발**
- 문제: 규칙이 너무 많아 관리 불가능
- 예: 10년 운영 시스템에 50,000개 규칙
- 해결: 규칙 그룹화, 계층화, ML 대체

**안티패턴 2: 지식 획득 병목**
- 문제: 전문가 지식 추출이 어려움
- 예: "그냥 느낌이 그래요"라는 암묵지
- 해결: 머신러닝으로 패턴 학습

**안티패턴 3: 취약한 추론**
- 문제: 예상치 못한 입력에 잘못된 결론
- 예: 훈련되지 않은 증상 조합
- 해결: 기본 규칙, 불확실성 표시

---

### V. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 레거시 시스템 | 전문가 시스템 | 향상 |
|:---|:---|:---|:---|
| **의사결정 속도** | 30분 (인간 전문가) | 1분 | 30x |
| **일관성** | 70% (사람마다 다름) | 100% | +30% |
| **가용성** | 8시간/일 | 24시간/일 | 3x |
| **설명 가능성** | 높음 (구두) | 높음 (자동 기록) | 유지 |
| **유지보수 비용** | 중간 | 높음 (규칙 관리) | - |

#### 2. 미래 전망 및 진화 방향

**단기 (2024~2027)**:
- **XAI (설명 가능한 AI)**: 딥러닝 + 규칙 추출
- **하이브리드 시스템**: ML + 규칙 결합
- **규제 준수**: 금융, 의료 분야 필수

**중기 (2028~2035)**:
- **자동 지식 획득**: ML에서 규칙 자동 추출
- **자연어 규칙 입력**: "만약 ~하면 ~해"로 규칙 추가
- **실시간 적응**: 상황에 따른 규칙 우선순위 조정

**장기 (2035~)**:
- **AGI와 통합**: 규칙 학습 + 추론 능력
- **자가 진화 시스템**: 스스로 규칙 생성/수정

#### 3. 참고 표준 및 가이드라인

- **CLIPS (C Language Integrated Production System)**: NASA 개발 표준 도구
- **Drools**: Java 기반 오픈소스 규칙 엔진
- **PROLOG**: 논리 프로그래밍 표준 언어
- **ISO/IEC 24765**: 시스템 및 소프트웨어 공학 용어

---

### 관련 개념 맵 (Knowledge Graph)

- **[지식 표현](@/studynotes/10_ai/1_fundamentals/5_knowledge_representation.md)**: 지식 베이스의 다양한 표현 방식
- **[전향/후향 추론](@/studynotes/10_ai/1_fundamentals/6_forward_backward_chaining.md)**: 추론 엔진의 핵심 알고리즘
- **[퍼지 논리](@/studynotes/10_ai/1_fundamentals/7_fuzzy_logic.md)**: 불확실성 처리 기법
- **[XAI (설명 가능한 AI)](@/studynotes/10_ai/3_ethics/xai.md)**: 현대적 설명 가능 AI
- **[의사결정 지원 시스템](@/studynotes/10_ai/5_mlops/decision_support_system.md)**: 기업 의사결정 자동화

---

### 어린이를 위한 3줄 비유 설명

1. **요리책 같은 컴퓨터**: 전문가 시스템은 요리책을 가진 요리사 같아요. 요리책에 "재료가 이렇게 있으면 이 요리를 만드세요"라고 적혀 있으면, 컴퓨터가 그대로 따라서 요리해요!

2. **똑똑한 질문자**: 컴퓨터가 "열이 있나요?", "기침하나요?"라고 계속 물어봐요. 그리고 대답을 모으면 "독감이네요!"라고 진단해요. 의사 선생님이 하는 것처럼요!

3. **왜 그런지 설명해줘요**: 컴퓨터가 "독감이에요!"라고 하면, "왜요?"라고 물어볼 수 있어요. 그러면 "열이 39도고, 기침하고, 겨울이니까요!"라고 이유를 설명해줘요!
