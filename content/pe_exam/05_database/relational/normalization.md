+++
title = "데이터베이스 정규화 (Normalization)"
date = 2025-03-02

[extra]
categories = "pe_exam-database"
+++

# 데이터베이스 정규화 (Normalization)

## 핵심 인사이트 (3줄 요약)
> **데이터 중복을 제거하고 이상 현상을 방지하는 관계형 데이터베이스 설계 기법**. 함수 종속성을 분석하여 테이블을 무손실 분해. 1NF부터 5NF/BCNF까지 단계적 정규형 적용으로 데이터 무결성 보장.

---

### Ⅰ. 개요 (필수: 200자 이상)

**개념**: 데이터베이스 정규화(Normalization)는 **관계형 데이터베이스에서 데이터 중복을 최소화하고, 데이터 이상 현상(Anomaly)을 방지하기 위해 테이블을 체계적으로 분해하는 설계 기법**이다.

> 💡 **비유**: 정규화는 **"잘 정리된 도서관"** 같아요. 모든 책이 정해진 위치에 하나만 있고, 책 정보는 별도의 카드목록에서 관리하죠. 책을 여러 곳에 두지 않으니 공간도 절약하고, 정보 변경 시 한 곳만 수정하면 됩니다.

**등장 배경** (필수: 3가지 이상 기술):
1. **기존 문제점 - 이상 현상(Anomaly)**: 비정규화된 테이블에서 삽입/삭제/갱신 시 데이터 불일치 발생
2. **기술적 필요성 - 저장 공간 낭비**: 동일 데이터가 여러 행에 중복 저장되어 디스크 공간 비효율
3. **시장/산업 요구 - 데이터 무결성**: 기업 데이터가 급증하며 정합성 유지의 중요성 대두

**핵심 목적**: 데이터 중복 최소화를 통한 **저장 효율성 향상**과 **데이터 무결성 보장**

---

### Ⅱ. 구성 요소 및 핵심 원리 (필수: 가장 상세하게)

**구성 요소** (필수: 최소 4개 이상):
| 구성 요소 | 역할/기능 | 특징 | 비유 |
|----------|----------|------|------|
| **함수 종속 (FD)** | 속성 간 의존 관계 정의 | A → B (A가 B를 결정) | 우편번호 → 주소 |
| **정규형 (NF)** | 정규화 완료 기준 | 1NF ~ 5NF, BCNF | 건물 층수 |
| **결정자/종속자** | 종속 관계의 주체 | 결정자가 종속자를 결정 | 열쇠와 자물쇠 |
| **후보키 (CK)** | 튜플 식별 최소 속성 집합 | 슈퍼키의 최소성 | 학번, 주민번호 |
| **무손실 분해** | 정보 손실 없는 테이블 분해 | 자연 조인 시 원본 복원 | 퍼즐 조각 |

**구조 다이어그램** (필수: ASCII 아트):
```
┌─────────────────────────────────────────────────────────────────────┐
│                    정규화 단계별 진화                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   비정규 테이블                                                     │
│   ┌─────────────────────────────────────────┐                      │
│   │ 학번 │ 이름 │ 학과 │ 학과장 │ 과목 │ 성적 │                      │
│   └─────────────────────────────────────────┘                      │
│                     │                                              │
│                     ▼ 1NF (원자성)                                 │
│   ┌─────────────────────────────────────────┐                      │
│   │ 복합 속성 분해 (반복 그룹 제거)          │                      │
│   └─────────────────────────────────────────┘                      │
│                     │                                              │
│                     ▼ 2NF (부분 함수 종속 제거)                    │
│   ┌─────────────────────────────────────────┐                      │
│   │ 학생(학번, 이름, 학과)                   │                      │
│   │ 수강(학번, 과목, 성적)                   │                      │
│   └─────────────────────────────────────────┘                      │
│                     │                                              │
│                     ▼ 3NF (이행 함수 종속 제거)                    │
│   ┌─────────────────────────────────────────┐                      │
│   │ 학생(학번, 이름, 학과코드)               │                      │
│   │ 학과(학과코드, 학과명, 학과장)           │                      │
│   │ 수강(학번, 과목, 성적)                   │                      │
│   └─────────────────────────────────────────┘                      │
│                     │                                              │
│                     ▼ BCNF (모든 결정자가 후보키)                  │
│   ┌─────────────────────────────────────────┐                      │
│   │ 결정자가 후보키가 아닌 경우 추가 분해    │                      │
│   └─────────────────────────────────────────┘                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**동작 원리** (필수: 단계별 상세 설명):
```
① 요구사항 분석 → ② 개념적 설계(ERD) → ③ 함수 종속 도출 → ④ 정규화 수행 → ⑤ 역정규화 검토
```

- **1단계 - 요구사항 분석**: 저장할 데이터 속성과 비즈니스 규칙 파악
- **2단계 - 개념적 설계**: ERD 작성으로 엔티티와 관계 정의
- **3단계 - 함수 종속 도출**: 속성 간 결정 관계 분석 (A → B)
- **4단계 - 정규화 수행**: 각 정규형 조건에 따라 테이블 분해
- **5단계 - 역정규화 검토**: 성능 요구사항에 따른 중복 허용 여부 결정

**핵심 알고리즘/공식** (해당 시 필수):

```
[함수 종속 공리 - Armstrong's Axioms]

1. 재귀성 (Reflexivity): Y ⊆ X 이면 X → Y
2. 증가성 (Augmentation): X → Y 이면 XZ → YZ
3. 이행성 (Transitivity): X → Y ∧ Y → Z 이면 X → Z

[정규형 조건]

1NF: 모든 속성이 원자값 (Atomic Value)
2NF: 부분 함수 종속 제거 ( Prime → Non-Prime 완전 종속)
3NF: 이행 함수 종속 제거 (X → Y → Z 형태 제거)
BCNF: 모든 결정자가 후보키 (Determinant → Candidate Key)
4NF: 다치 종속 제거 (MVD: X ↠ Y)
5NF: 조인 종속 제거 (JD: 무손실 분해의 최소성)

[무손실 분해 조건]
R1 ∩ R2 → R1 또는 R1 ∩ R2 → R2
(교집합이 어느 한쪽의 결정자여야 함)
```

**코드 예시** (필수: Python 또는 의사코드):
```python
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple
from collections import defaultdict

@dataclass
class FunctionalDependency:
    """함수 종속성 표현: left → right"""
    left: Set[str]      # 결정자
    right: Set[str]     # 종속자

class NormalizationAnalyzer:
    """데이터베이스 정규화 분석기"""

    def __init__(self, attributes: Set[str], fds: List[FunctionalDependency]):
        self.attributes = attributes
        self.fds = fds
        self.candidate_keys: List[Set[str]] = []

    def closure(self, attrs: Set[str]) -> Set[str]:
        """속성 집합의 폐포(closure) 계산"""
        closure = set(attrs)
        changed = True
        while changed:
            changed = False
            for fd in self.fds:
                if fd.left.issubset(closure):
                    new_attrs = fd.right - closure
                    if new_attrs:
                        closure.update(new_attrs)
                        changed = True
        return closure

    def find_candidate_keys(self) -> List[Set[str]]:
        """후보키 탐색 알고리즘"""
        candidate_keys = []
        n = len(self.attributes)
        attrs_list = list(self.attributes)

        # 속성 개수가 작은 순서대로 조합 검사
        for size in range(1, n + 1):
            from itertools import combinations
            for combo in combinations(attrs_list, size):
                key = set(combo)
                # 이미 발견된 후보키의 부분집합이면 스킵
                if any(ck.issubset(key) for ck in candidate_keys):
                    continue
                # 폐포가 모든 속성을 포함하면 후보키
                if self.closure(key) == self.attributes:
                    candidate_keys.append(key)
        self.candidate_keys = candidate_keys
        return candidate_keys

    def check_1nf(self, table_data: List[Dict]) -> Tuple[bool, str]:
        """1NF 검사: 모든 값이 원자값인지 확인"""
        for row in table_data:
            for key, value in row.items():
                if isinstance(value, (list, dict, set)):
                    return False, f"비원자값 발견: {key} = {value}"
        return True, "1NF 만족"

    def check_2nf(self) -> Tuple[bool, List[str]]:
        """2NF 검사: 부분 함수 종속 확인"""
        violations = []
        prime_attrs = set()
        for ck in self.candidate_keys:
            prime_attrs.update(ck)
        non_prime = self.attributes - prime_attrs

        for fd in self.fds:
            # 결정자가 후보키의 진부분집합인지 확인
            for ck in self.candidate_keys:
                if fd.left < ck:  # 진부분집합
                    violations.append(f"부분 함수 종속: {fd.left} → {fd.right}")
        return len(violations) == 0, violations

    def check_3nf(self) -> Tuple[bool, List[str]]:
        """3NF 검사: 이행 함수 종속 확인"""
        violations = []
        prime_attrs = set()
        for ck in self.candidate_keys:
            prime_attrs.update(ck)

        for fd in self.fds:
            # 결정자가 후보키가 아니고, 종속자가 프라임 속성이 아닌 경우
            is_determinant_key = any(fd.left == ck or fd.left > ck
                                     for ck in self.candidate_keys)
            is_right_prime = fd.right.issubset(prime_attrs)

            if not is_determinant_key and not is_right_prime:
                violations.append(f"이행 함수 종속 위반: {fd.left} → {fd.right}")
        return len(violations) == 0, violations

    def check_bcnf(self) -> Tuple[bool, List[str]]:
        """BCNF 검사: 모든 결정자가 후보키인지 확인"""
        violations = []
        for fd in self.fds:
            is_superkey = self.closure(fd.left) == self.attributes
            if not is_superkey:
                violations.append(f"BCNF 위반: {fd.left} → {fd.right}")
        return len(violations) == 0, violations

    def decompose_to_bcnf(self) -> List[Tuple[Set[str], List[FunctionalDependency]]]:
        """BCNF까지 분해 알고리즘"""
        relations = [(self.attributes, self.fds.copy())]
        final_relations = []

        while relations:
            attrs, current_fds = relations.pop()
            analyzer = NormalizationAnalyzer(attrs, current_fds)
            analyzer.find_candidate_keys()
            is_bcnf, violations = analyzer.check_bcnf()

            if is_bcnf:
                final_relations.append((attrs, current_fds))
            else:
                # 위반된 FD로 분해
                fd = violations[0]  # 첫 번째 위반 처리
                violating_fd = next(f for f in current_fds
                                   if str(f.left) in str(fd))

                r1_attrs = violating_fd.left | violating_fd.right
                r2_attrs = attrs - violating_fd.right | violating_fd.left

                r1_fds = [FunctionalDependency(f.left & r1_attrs, f.right & r1_attrs)
                         for f in current_fds if f.left.issubset(r1_attrs)]
                r2_fds = [FunctionalDependency(f.left & r2_attrs, f.right & r2_attrs)
                         for f in current_fds if f.left.issubset(r2_attrs)]

                relations.append((r1_attrs, r1_fds))
                relations.append((r2_attrs, r2_fds))

        return final_relations

# 사용 예시
if __name__ == "__main__":
    # 학생-수강 예제
    attributes = {"학번", "이름", "학과", "학과장", "과목", "성적"}

    fds = [
        FunctionalDependency({"학번"}, {"이름", "학과"}),
        FunctionalDependency({"학과"}, {"학과장"}),
        FunctionalDependency({"학번", "과목"}, {"성적"}),
    ]

    analyzer = NormalizationAnalyzer(attributes, fds)

    # 후보키 찾기
    cks = analyzer.find_candidate_keys()
    print(f"후보키: {[ck for ck in cks]}")

    # 정규형 검사
    print(f"2NF: {analyzer.check_2nf()}")
    print(f"3NF: {analyzer.check_3nf()}")
    print(f"BCNF: {analyzer.check_bcnf()}")

    # BCNF 분해
    decomposed = analyzer.decompose_to_bcnf()
    print(f"\nBCNF 분해 결과: {[r[0] for r in decomposed]}")
```

---

### Ⅲ. 기술 비교 분석 (필수: 2개 이상의 표)

**장단점 분석** (필수: 최소 3개씩):
| 장점 | 단점 |
|-----|------|
| **데이터 중복 최소화**: 저장 공간 절약 (30~70%) | **조인 연산 증가**: 복잡한 쿼리로 인한 성능 저하 |
| **이상 현상 방지**: 삽입/삭제/갱신 무결성 보장 | **설계 복잡도**: 함수 종속 분석에 전문 지식 필요 |
| **유지보수 용이**: 스키마 변경 시 영향 범위 최소화 | **과도한 분해**: 작은 테이블 다수 생성으로 관리 부담 |
| **데이터 일관성**: 단일 위치 수정으로 정합성 확보 | **읽기 성능 저하**: 다중 조인으로 인한 지연 시간 |

**대안 기술 비교** (필수: 최소 2개 대안):
| 비교 항목 | 정규화 (Normalization) | 역정규화 (Denormalization) | NoSQL (Document) |
|---------|----------------------|--------------------------|-----------------|
| **핵심 특성** | ★ 중복 최소화, 무결성 우선 | 읽기 성능 우선, 중복 허용 | 유연한 스키마, 임베딩 |
| **조인 빈도** | 높음 (다중 조인) | 낮음 (단일 테이블) | 없음 (임베디드) |
| **쓰기 성능** | 낮음 (다중 테이블 갱신) | 중간 | ★ 높음 (단일 문서) |
| **읽기 성능** | 낮음 (조인 오버헤드) | ★ 높음 | 높음 |
| **일관성** | ★ 강한 일관성 | 중간 | 결과적 일관성 |
| **적합 환경** | OLTP, 트랜잭션 시스템 | OLAP, 리포팅 | 웹앱, 콘텐츠 관리 |

> **★ 선택 기준**:
> - **정규화 선택**: 트랜잭션 무결성이 중요한 금융/회계 시스템
> - **역정규화 선택**: 읽기 중심의 분석/리포팅 시스템, 실시간 대시보드
> - **NoSQL 선택**: 스키마 유연성이 필요한 IoT/로그/소셜미디어

**정규형 단계별 비교**:
| 정규형 | 조건 | 해결 문제 | 실무 적용 빈도 |
|-------|------|----------|--------------|
| 1NF | 원자값 보장 | 반복 그룹, 복합 속성 | ★ 필수 |
| 2NF | 부분 함수 종속 제거 | 삽입/삭제 이상 | ★ 필수 |
| 3NF | 이행 함수 종속 제거 | 갱신 이상 | ★ 필수 |
| BCNF | 결정자 후보키 | 중복 결정자 | 선택적 |
| 4NF | 다치 종속 제거 | 독립 다치 속성 | 드묾 |
| 5NF | 조인 종속 제거 | 순환 종속 | 매우 드묾 |

---

### Ⅳ. 실무 적용 방안 (필수: 기술사 판단력 증명)

**기술사적 판단** (필수: 3개 이상 시나리오):
| 적용 분야 | 구체적 적용 방법 | 기대 효과 (정량) |
|---------|----------------|-----------------|
| **금융 코어뱅킹** | 3NF/BCNF 적용, ACID 트랜잭션 보장 | 데이터 정합성 100%, 이상 현상 0건 |
| **전자상거래 주문** | 3NF + 부분 역정규화 (인기 상품 캐시) | 쿼리 응답시간 50% 단축 |
| **ERP 시스템** | 마스터 데이터 정규화, 트랜잭션 역정규화 | 저장공간 40% 절약, 리포트 생성 3배 향상 |

**실제 도입 사례** (필수: 구체적 기업/서비스):
- **사례 1 - 은행 코어뱅킹**: 신한은행 차세대 시스템 - BCNF까지 정규화로 계좌 이체 시 데이터 무결성 100% 보장, 이중 출금 방지
- **사례 2 - 쇼핑몰**: 쿠팡 상품 DB - 3NF 기반 설계 후 조회 빈도 상위 100개 상품에 대해 역정규화 적용, 검색 응답시간 80% 단축
- **사례 3 - SaaS ERP**: SAP S/4HANA - 메모리 DB 특성 고려 정규화 최적화, 실시간 분석 지원

**도입 시 고려사항** (필수: 4가지 관점):
1. **기술적**:
   - 함수 종속 분석 정확성
   - 조인 성능 영향도 측정
   - 인덱스 전략 수립
   - 레거시 시스템 연동 방안
2. **운영적**:
   - 쿼리 복잡도 증가 대응
   - DBA 교육 필요
   - 성능 모니터링 체계
   - 정규화 수준 결정 기준
3. **보안적**:
   - 분해된 테이블별 접근 권한
   - 민감 데이터 분리 저장
   - 뷰(View)를 통한 추상화
   - 감사 로그 이력 관리
4. **경제적**:
   - 저장 공간 절약 효과
   - 하드웨어 리소스 영향
   - 개발/유지보수 비용
   - 성능 vs 무결성 트레이드오프

**주의사항 / 흔한 실수** (필수: 최소 3개):
- ❌ **과도한 정규화**: 5NF까지 적용하여 수십 개 테이블 생성 → 복잡도 급증
- ❌ **함수 종속 오분석**: 비즈니스 규칙 이해 없이 기술적 종속만 판단 → 잘못된 분해
- ❌ **역정규화 시점 오류**: 초기 설계부터 역정규화 적용 → 이상 현상 발생
- ❌ **조인 성능 무시**: 정규화만 고려하고 인덱스 설계 누락 → 실제 성능 저하

**관련 개념 / 확장 학습** (필수: 최소 5개 이상 나열):
```
📌 정규화와 밀접하게 연관된 핵심 개념들

┌─────────────────────────────────────────────────────────────────┐
│  정규화 핵심 연관 개념 맵                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   [함수종속] ←──→ [정규화] ←──→ [인덱싱]                        │
│       ↓              ↓              ↓                           │
│   [트랜잭션]     [역정규화]     [쿼리최적화]                     │
│       ↓              ↓              ↓                           │
│   [무결성]       [NoSQL]       [데이터마이닝]                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 관련 개념 | 관계 | 설명 | 문서 링크 |
|----------|------|------|----------|
| **트랜잭션 (Transaction)** | 선행 개념 | 정규화된 테이블의 ACID 보장 | `[트랜잭션](../transaction.md)` |
| **인덱싱 (Indexing)** | 보완 개념 | 정규화로 인한 조인 성능 보완 | `[인덱싱](./indexing.md)` |
| **역정규화 (Denormalization)** | 대안 개념 | 성능을 위한 의도적 중복 허용 | `[역정규화](./denormalization.md)` |
| **NoSQL** | 대안 기술 | 정규화 없는 유연한 스키마 | `[NoSQL](../nosql/nosql_database.md)` |
| **동시성 제어** | 후속 개념 | 정규화 환경의 동시 접근 관리 | `[동시성제어](../concurrency_control.md)` |
| **쿼리 최적화** | 보완 기술 | 조인 쿼리 성능 향상 | `[쿼리최적화](./query_optimization.md)` |

---

### Ⅴ. 기대 효과 및 결론 (필수: 미래 전망 포함)

**정량적 기대 효과** (필수):
| 효과 영역 | 구체적 내용 | 정량적 목표 |
|---------|-----------|------------|
| **저장 효율** | 중복 제거로 디스크 공간 절약 | 기존 대비 40~70% 절감 |
| **무결성** | 이상 현상 100% 방지 | 데이터 정합성 오류 0건 |
| **유지보수** | 스키마 변경 영향 최소화 | 수정 시간 50% 단축 |
| **품질** | 데이터 일관성 보장 | 데이터 품질 99.9% 달성 |

**미래 전망** (필수: 3가지 관점):
1. **기술 발전 방향**: 자동 정규화 도구(AI 기반 스키마 최적화) 발전, HTAP(Hybrid Transactional/Analytical Processing) 환경에서의 적절한 정규화 수준 결정 알고리즘
2. **시장 트렌드**: 클라우드 네이티브 DB에서 정규화보다 샤딩/파티셔닝 우선, 벡터 DB/그래프 DB 등장으로 관계형 정규화 한계 인식
3. **후속 기술**: NewSQL에서 정규화와 수평 확장의 조화, Schema-on-Read 접근으로 정규화 유연화

> **결론**: 데이터베이스 정규화는 50년 이상 관계형 DB 설계의 핵심 원칙으로, 데이터 무결성과 중복 최소화라는 본질적 가치는 변함없다. 다만 NoSQL, NewSQL, 벡터 DB 등 다양한 데이터베이스 등장으로 "무조건 정규화"에서 "용도에 맞는 적절한 정규화 수준"으로 패러다임이 전환되고 있다.

> **※ 참고 표준**: ISO/IEC 9075 (SQL Standard), Codd's 12 Rules, ACM SIGMOD 정규화 이론

---

## 어린이를 위한 종합 설명 (필수)

**데이터베이스 정규화**은(는) 마치 **"책장을 깔끔하게 정리하는 것"** 같아요.

학교 도서관을 상상해보세요. 책이 아무렇게나 여러 곳에 있다면 어떻게 될까요? 같은 책이 여러 군데 있어서 공간도 낭비되고, 책 내용이 바뀌면 모든 책을 찾아다니며 수정해야 해요. 정규화는 이런 문제를 해결하는 거예요.

먼저, **데이터를 종류별로 나누는 것**이에요. 학생 정보는 학생 책장에, 책 정보는 책 책장에 따로 보관하는 것처럼요. 그래서 학생 주소가 바뀌면 학생 책장만 고치면 돼요.

또, **불필요한 중복을 없애는 것**이에요. "홍길동이가 수학책을 빌렸다"는 사실을 기록할 때, 홍길동이의 모든 정보(주소, 전화번호 등)를 매번 적지 않아도 돼요. 학번만 적어두면 되니까요!

마지막으로, **데이터를 안전하게 지키는 것**이에요. 누가 실수로 정보를 지우더라도, 중요한 데이터는 다른 곳에 안전하게 보존되어 있어요. 정규화 덕분에 도서관은 항상 깔끔하고, 책도 쉽게 찾을 수 있어요! 📚
