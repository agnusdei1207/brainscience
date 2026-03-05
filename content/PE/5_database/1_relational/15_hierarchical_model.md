+++
title = "계층형 데이터 모델 (Hierarchical Data Model)"
description = "트리 구조 기반 데이터 모델의 원리, IMS, 부모-자식 관계 심층 분석"
date = "2026-03-05"
[taxonomies]
tags = ["database", "hierarchical-model", "ims", "tree-structure", "legacy-db"]
categories = ["studynotes-5_database"]
+++

# 15. 계층형 데이터 모델 (Hierarchical Data Model)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터를 트리(Tree) 구조로 조직화하여 부모-자식(Parent-Child) 관계로 표현하는 데이터 모델로, 1960년대 IBM IMS(Information Management System)에서 최초로 상용화되었습니다.
> 2. **가치**: 1:N 관계에 최적화되어 있어 조직도, 제품 BOM(Bill of Materials), 파일 시스템 등 계층적 데이터에서 높은 검색 성능을 제공합니다.
> 3. **융합**: 현대 XML 데이터베이스, JSON 문서 구조, LDAP 디렉터리 서비스, 그리고 파일 시스템의 디렉터리 구조에 그 개념이 계승되어 있습니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**계층형 데이터 모델(Hierarchical Data Model)**은 데이터를 부모-자식 관계로 구성된 트리(Tree) 구조로 표현하는 데이터베이스 모델입니다. 각 노드(Record)는 최대 하나의 부모 노드만 가질 수 있으며, 여러 개의 자식 노드를 가질 수 있는 1:N 관계의 전형적인 구조입니다.

**핵심 특성**:
1. **트리 구조(Tree Structure)**: 루트(Root) 노드에서 시작하여 계층적으로 확장
2. **1:N 관계**: 한 부모가 여러 자식을 가질 수 있으나, 자식은 하나의 부모만 가짐
3. **부모 우선 탐색**: 데이터 접근 시 반드시 부모 노드를 거쳐야 함 (네비게이션 방식)
4. **세그먼트(Segment)**: 계층형 모델에서의 레코드 단위

**구조적 한계**:
- M:N 관계 표현 불가 (다중 부모 불가)
- 데이터 중복 발생 가능
- 구조 변경이 어려움 (강한 결합도)

#### 2. 💡 비유를 통한 이해

**가족 족보(家譜)**로 비유할 수 있습니다:
- **루트 노드** = 시조(始祖): 가문의 시작점
- **부모-자식 관계** = 부모-자식 혈연관계: 한 사람은 부모가 한 쌍뿐
- **형제 노드** = 형제자매: 같은 부모를 공유
- **깊이(Depth)** = 대수(代): 시조로부터 몇 대인지

**파일 시스템**으로도 비유:
- **루트 디렉터리** = / (C:\)
- **폴더** = 부모 노드
- **하위 폴더/파일** = 자식 노드

```
/ (루트)
├── 사용자/
│   ├── 홍길동/
│   │   ├── 문서/
│   │   └── 사진/
│   └── 김철수/
└── 시스템/
    ├── 설정/
    └── 로그/
```

#### 3. 등장 배경 및 발전 과정

**1단계: 탄생 배경 (1960년대)**
- **1966년**: IBM이 아폴로 우주선 프로젝트를 위해 IMS(Information Management System) 개발
- 목적: 복잡한 부품 구조(BOM)와 미션 데이터 관리
- 특징: 대용량 데이터의 효율적 저장과 빠른 접근

**2단계: 전성기 (1960~1980년대)**
- IBM 메인프레임 환경에서 사실상 표준
- 항공사 예약 시스템, 은행 시스템, 재고 관리 시스템
- 대량 트랜잭션 처리에 뛰어난 성능

**3단계: 관계형 모델의 등장과 쇠퇴 (1980~1990년대)**
- E.F. Codd의 관계형 모델이 유연성에서 압도
- M:N 관계 표현의 어려움
- 복잡한 네비게이션 코드

**4단계: 현대적 계승 (2000년대~현재)**
- XML 데이터베이스: 계층적 문서 구조
- JSON/NoSQL: 중첩 문서 구조
- LDAP: 디렉터리 서비스
- Graph DB: 트리 구조 확장

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 계층형 모델 구성 요소 (표)

| 구성요소 | 정의 | 특성 | IMS 용어 | 비고 |
|:---|:---|:---|:---|:---|
| **루트(Root)** | 최상위 노드 | 부모 없음, 단일 존재 | Root Segment | 트리의 시작점 |
| **세그먼트(Segment)** | 데이터 저장 단위 | 필드들의 집합 | Segment | 레코드와 유사 |
| **부모-자식 관계** | 계층적 연결 | 1:N, 단방향 참조 | Parent-Child | 물리적 포인터 |
| **트win(Twin)** | 같은 부모의 형제 노드 | 순서 존재 | Twin Segment | 좌→우 순회 |
| **경로(Path)** | 루트에서 특정 노드까지의 경로 | 유일한 접근 경로 | Hierarchical Path | 검색 키 |
| **깊이(Depth)** | 루트에서 해당 노드까지의 거리 | 계층 레벨 | Level | 최대 15~255 |

#### 2. 계층형 데이터 모델 구조 다이어그램

```text
+============================================================================+
|                    HIERARCHICAL DATA MODEL ARCHITECTURE                     |
+============================================================================+
|                                                                             |
|                        +------------------+                                 |
|                        |   ROOT SEGMENT   |  <-- Level 1 (조직)            |
|                        |   ORG (조직)     |                                 |
|                        |   - org_id (PK)  |                                 |
|                        |   - org_name     |                                 |
|                        +--------+---------+                                 |
|                                 |                                           |
|              +------------------+------------------+                        |
|              |                                     |                        |
|    +---------v----------+               +---------v----------+              |
|    |  DEPT (부서)       |               |  DEPT (부서)       |  <-- Level 2 |
|    |  - dept_id         |               |  - dept_id         |              |
|    |  - dept_name       |               |  - dept_name       |              |
|    +---------+----------+               +---------+----------+              |
|              |                                     |                        |
|    +---------+---------+                 +---------+---------+              |
|    |                   |                 |                   |              |
| +--v--+            +---v---+          +--v--+            +---v---+          |
| | EMP |            | EMP   |          | EMP |            | PROJ  |  Lvl 3  |
| |사원1 |            |사원2   |          |사원3 |            |프로젝트|          |
| +-----+            +-------+          +-----+            +-------+          |
|                                                                             |
| [특징]                                                                      |
| 1. 각 노드는 최대 1개의 부모만 가짐 (1:N 관계)                               |
| 2. 데이터 접근은 루트에서 시작하여 순차적 네비게이션                           |
| 3. M:N 관계 표현 불가 - 데이터 중복으로 해결                                  |
|                                                                            |
+============================================================================+

[IMS Physical Storage Structure]

+----------------+     +----------------+     +----------------+
| Database       | --> | Record Type    | --> | Segment        |
| (데이터베이스)   |     | (레코드 타입)    |     | (세그먼트)      |
+----------------+     +----------------+     +----------------+
                                                    |
                              +---------------------+---------------------+
                              |                     |                     |
                        +-----v-----+         +-----v-----+         +-----v-----+
                        |  Field 1  |         |  Field 2  |         |  Field N  |
                        |  (필드)   |         |  (필드)   |         |  (필드)   |
                        +-----------+         +-----------+         +-----------+
```

#### 3. 심층 동작 원리: 계층형 모델의 데이터 조작

**1단계: 데이터 정의 (DDL in IMS)**
```cobol
* IMS Database Definition (DBD)
* 계층형 데이터베이스 구조 정의

DBD NAME=ORGDB, ACCESS=HISAM
  SEGM NAME=ORG, BYTES=50
    FIELD NAME=(ORG_ID, SEQ), BYTES=4, START=1
    FIELD NAME=ORG_NAME, BYTES=30, START=5
  SEGM NAME=DEPT, PARENT=ORG, BYTES=100
    FIELD NAME=(DEPT_ID, SEQ), BYTES=4, START=1
    FIELD NAME=DEPT_NAME, BYTES=50, START=5
  SEGM NAME=EMP, PARENT=DEPT, BYTES=80
    FIELD NAME=(EMP_ID, SEQ), BYTES=4, START=1
    FIELD NAME=EMP_NAME, BYTES=30, START=5
    FIELD NAME=SALARY, BYTES=8, START=35
DBDGEN
```

**2단계: 데이터 조작 (DML - 네비게이션 방식)**
```cobol
* IMS Data Manipulation - 네비게이션 기반 접근

* 1. 루트에서 특정 조직 찾기
CALL 'CBLTDLI' USING GU, PCB, IOAREA, ORG-SSA
* GU = Get Unique (직접 검색)
* ORG-SSA = Segment Search Argument (검색 조건)

* 2. 부모를 통한 자식 순회
CALL 'CBLTDLI' USING GN, PCB, IOAREA, DEPT-SSA
* GN = Get Next (순차 검색)

* 3. 경로를 통한 특정 데이터 접근
* ORG(ORG_ID=001) -> DEPT(DEPT_ID=D10) -> EMP(EMP_ID=E1001)
MOVE 'ORG(ORG_ID=001)' TO SSA-1
MOVE 'DEPT(DEPT_ID=D10)' TO SSA-2
MOVE 'EMP(EMP_ID=E1001)' TO SSA-3
CALL 'CBLTDLI' USING GU, PCB, IOAREA, SSA-LIST
```

**3단계: 계층형 순회 알고리즘**

```python
"""
계층형 데이터 모델의 순회(Traversal) 알고리즘 구현
전위 순회(Pre-order Traversal) 방식
"""

class HierarchicalNode:
    """계층형 모델의 노드(세그먼트)"""
    def __init__(self, segment_type: str, data: dict):
        self.segment_type = segment_type
        self.data = data
        self.children: list['HierarchicalNode'] = []
        self.parent: 'HierarchicalNode' = None
        self.twin_next: 'HierarchicalNode' = None  # 형제 노드

class HierarchicalDatabase:
    """계층형 데이터베이스 시뮬레이션"""

    def __init__(self, name: str):
        self.name = name
        self.root: HierarchicalNode = None
        self.current_position: HierarchicalNode = None

    def insert(self, parent: HierarchicalNode, node: HierarchicalNode) -> HierarchicalNode:
        """계층적 삽입 - 부모 노드 하위에 자식 추가"""
        node.parent = parent

        if parent is None:
            # 루트 노드 설정
            self.root = node
        else:
            # 자식 리스트에 추가
            if parent.children:
                # 마지막 형제의 twin_next 설정
                last_sibling = parent.children[-1]
                last_sibling.twin_next = node
            parent.children.append(node)

        return node

    def get_unique(self, path: list[tuple]) -> HierarchicalNode:
        """
        GU (Get Unique) - 특정 경로로 직접 접근
        path: [(segment_type, condition), ...]
        예: [('ORG', 'ORG_ID=001'), ('DEPT', 'DEPT_ID=D10')]
        """
        current = self.root

        for segment_type, condition in path:
            # 현재 레벨에서 조건 확인
            if current.segment_type != segment_type:
                return None

            # 조건 파싱 (예: "ORG_ID=001")
            field, value = condition.split('=')
            if str(current.data.get(field)) != value:
                return None

            # 다음 레벨로 이동 (있다면)
            if path.index((segment_type, condition)) < len(path) - 1:
                if not current.children:
                    return None
                # 첫 번째 자식으로 이동
                current = current.children[0]

        self.current_position = current
        return current

    def get_next(self) -> HierarchicalNode:
        """
        GN (Get Next) - 현재 위치에서 다음 세그먼트 순차 검색
        전위 순회(Pre-order) 방식: 부모 -> 첫 자식 -> 형제
        """
        if self.current_position is None:
            self.current_position = self.root
            return self.current_position

        # 1. 자식이 있으면 첫 번째 자식으로
        if self.current_position.children:
            self.current_position = self.current_position.children[0]
            return self.current_position

        # 2. 형제가 있으면 다음 형제로
        if self.current_position.twin_next:
            self.current_position = self.current_position.twin_next
            return self.current_position

        # 3. 부모로 거슬러 올라가 형제 찾기
        current = self.current_position.parent
        while current:
            if current.twin_next:
                self.current_position = current.twin_next
                return self.current_position
            current = current.parent

        # 더 이상 없음
        return None

    def get_next_in_parent(self, parent_type: str) -> HierarchicalNode:
        """
        GNP (Get Next within Parent) - 특정 부모 하위에서만 순회
        """
        while True:
            node = self.get_next()
            if node is None:
                return None
            # 부모 타입 확인
            current = node.parent
            while current:
                if current.segment_type == parent_type:
                    return node
                current = current.parent
            # 해당 부모 타입이 아니면 계속

    def traverse_preorder(self) -> list[HierarchicalNode]:
        """전위 순회로 모든 노드 반환"""
        result = []

        def _traverse(node: HierarchicalNode):
            if node is None:
                return
            result.append(node)
            for child in node.children:
                _traverse(child)

        _traverse(self.root)
        return result

    def find_path(self, node: HierarchicalNode) -> list[HierarchicalNode]:
        """루트에서 특정 노드까지의 경로 반환"""
        path = []
        current = node
        while current:
            path.insert(0, current)
            current = current.parent
        return path

# 사용 예시
db = HierarchicalDatabase("CompanyDB")

# 계층적 데이터 구축
org = db.insert(None, HierarchicalNode("ORG", {"ORG_ID": "001", "ORG_NAME": "본사"}))

dept1 = db.insert(org, HierarchicalNode("DEPT", {"DEPT_ID": "D10", "DEPT_NAME": "개발팀"}))
dept2 = db.insert(org, HierarchicalNode("DEPT", {"DEPT_ID": "D20", "DEPT_NAME": "영업팀"}))

emp1 = db.insert(dept1, HierarchicalNode("EMP", {"EMP_ID": "E001", "EMP_NAME": "홍길동"}))
emp2 = db.insert(dept1, HierarchicalNode("EMP", {"EMP_ID": "E002", "EMP_NAME": "김철수"}))
emp3 = db.insert(dept2, HierarchicalNode("EMP", {"EMP_ID": "E003", "EMP_NAME": "이영희"}))

# 네비게이션 방식 검색
path = [
    ("ORG", "ORG_ID=001"),
    ("DEPT", "DEPT_ID=D10"),
    ("EMP", "EMP_ID=E001")
]
found = db.get_unique(path)
print(f"찾은 직원: {found.data}")

# 전위 순회
print("\n전체 순회:")
for node in db.traverse_preorder():
    indent = "  " * len(db.find_path(node))[:-1] if db.find_path(node) else ""
    print(f"{indent}{node.segment_type}: {node.data}")
```

#### 4. M:N 관계 표현의 한계와 해결방안

```text
[문제 상황]
학생(Student)과 과목(Course)의 M:N 관계
- 한 학생은 여러 과목 수강 가능
- 한 과목은 여러 학생이 수강 가능

[계층형 모델의 한계]
루트가 학생인 경우: 과목 데이터 중복
       학생1 ─┬─ 과목A (중복)
              └─ 과목B (중복)
       학생2 ─┬─ 과목A (중복!)
              └─ 과목C

루트가 과목인 경우: 학생 데이터 중복
       과목A ─┬─ 학생1 (중복)
              └─ 학생2 (중복)
       과목B ─── 학생1 (중복!)

[해결방안: 가상 세그먼트 (Logical Relationship)]

       학생1 ─┬─ 과목A (물리적)
              └─ [과목Bへの포인터] (논리적)
                      ↓
       과목B (물리적 저장)

또는 두 개의 별도 트리 구성 + 애플리케이션 레벨 조인
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 계층형 vs 망형 vs 관계형 모델 비교

| 비교 항목 | 계층형 모델 | 망형 모델 | 관계형 모델 |
|:---|:---|:---|:---|
| **데이터 구조** | 트리(Tree) | 그래프(Graph) | 테이블(Table) |
| **관계 표현** | 1:N만 가능 | M:N 가능 | M:N 자연스럽게 |
| **부모 수** | 최대 1개 | 여러 개 가능 | 없음 (참조 기반) |
| **데이터 접근** | 네비게이션 | 네비게이션 | 선언적(SQL) |
| **데이터 중복** | 높음 (M:N 불가) | 중간 | 낮음 (정규화) |
| **구조 유연성** | 낮음 (변경 어려움) | 중간 | 높음 |
| **쿼리 복잡도** | 높음 (경로 지정) | 높음 (SET 명령) | 낮음 (SQL) |
| **표준화** | IBM IMS | CODASYL DBTG | ANSI/ISO SQL |
| **현대 적용** | XML, JSON, LDAP | 드묾 | RDBMS 표준 |

#### 2. 계층형 모델의 현대적 계승 비교

| 현대 기술 | 계층형 모델과의 유사점 | 차이점 |
|:---|:---|:---|
| **XML** | 계층적 태그 구조, 부모-자식 관계 | M:N 표현 가능 (IDREF) |
| **JSON** | 중첩 객체 구조 | 스키마 없음, 유연함 |
| **LDAP** | DIT(Directory Information Tree) | 속성-값 쌍, 검색 최적화 |
| **파일 시스템** | 디렉터리 계층 구조 | 파일 내용은 비구조적 |
| **MongoDB** | 중첩 문서 (Embedded Document) | 참조(Reference) 패턴으로 M:N 해결 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 레거시 IMS 시스템 현대화**
- 상황: 30년 된 IBM IMS 기반 항공 예약 시스템
- 판단: 완전 교체보다 점진적 마이그레이션
- 전략:
  1. IMS ↔ RDBMS 게이트웨이 구축
  2. 신규 기능은 RDBMS로 개발
  3. 코어 트랜잭션은 IMS 유지
  4. 최종적으로 NewSQL로 이관

**시나리오 2: XML 데이터의 관계형 변환**
- 상황: 복잡한 계층형 XML 데이터를 RDBMS에 저장
- 판단: Shredding(분해) vs Native XML DB
- 전략:
  - 단순 계층: 부모-자식 테이블로 분해
  - 복잡 계층: JSON/XML 컬럼 타입 활용
  - 검색 빈도 높으면: XPath/XQuery 인덱싱

**시나리오 3: 조직도/카테고리 데이터 모델링**
- 상황: 깊은 계층의 조직도 데이터
- 판단: 관계형으로 표현하되 계층형 패턴 활용
- 전략:
  - Adjacency List: parent_id 컬럼
  - Path Enumeration: /1/2/3 경로 문자열
  - Nested Set: left/right 값
  - Closure Table: 별도 경로 테이블

#### 2. 도입 시 고려사항 (체크리스트)

**계층형 데이터 판별 체크리스트**:
- [ ] 데이터가 본질적으로 1:N 계층 구조인가?
- [ ] M:N 관계가 거의 없는가?
- [ ] 부모-자식 순회가 주요 접근 패턴인가?
- [ ] 구조 변경이 거의 없는가?

**현대적 대안 고려**:
- [ ] JSON 컬럼 (PostgreSQL, MySQL)
- [ ] CTE 재귀 쿼리 (WITH RECURSIVE)
- [ ] 그래프 DB (Neo4j) - 복잡한 관계
- [ ] LDAP - 디렉터리 서비스

#### 3. 안티패턴 (Anti-patterns)

1. **강제 계층화**: 본질적으로 계층이 아닌 데이터를 계층으로 표현
   - 해결: 관계형 또는 그래프 모델 사용

2. **과도한 중첩**: JSON/XML에서 무제한 중첩
   - 해결: 참조 패턴으로 분리

3. **경로 하드코딩**: 계층 경로를 코드에 하드코딩
   - 해결: 메타데이터 기반 동적 네비게이션

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 계층형 모델 | 관계형 모델 | 비고 |
|:---|:---|:---|:---|
| **계층 순회 성능** | 매우 빠름 (O(depth)) | 느림 (재귀 쿼리) | 계층형 우위 |
| **M:N 표현** | 불가/중복 | 자연스러움 | 관계형 우위 |
| **구조 변경** | 어려움 | 쉬움 | 관계형 우위 |
| **데이터 중복** | 높음 | 낮음 | 관계형 우위 |
| **표준화** | IMS 전용 | SQL 표준 | 관계형 우위 |

#### 2. 미래 전망 및 진화 방향

**계층형 모델의 현대적 재탄생**:
- **JSON/NoSQL**: 계층적 문서 구조의 부활
- **Tree Pattern in Graph**: 그래프 DB에서의 트리 서브그래프
- **Hierarchical Index**: B+Tree, LSM-Tree의 내부 구조

**학습 가치**:
- 데이터 모델링의 역사적 맥락 이해
- 현대 NoSQL의 이론적 기반 파악
- 트리 자료구조의 DB 적용 사례

#### 3. 참고 표준/가이드

| 표준 | 내용 | 적용 범위 |
|:---|:---|:---|
| **IBM IMS** | 계층형 DBMS 원조 | 메인프레임 |
| **XML Schema** | 계층적 문서 구조 정의 | XML DB |
| **LDAP (RFC 4511)** | 디렉터리 서비스 프로토콜 | 인증/조직도 |
| **JSON Schema** | JSON 문서 구조 검증 | NoSQL, API |

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[망형 데이터 모델](@/studynotes/5_database/1_relational/16_network_model.md)**: 계층형의 한계를 극복한 그래프 기반 모델
- **[관계형 데이터 모델](@/studynotes/5_database/1_relational/relational_model.md)**: 계층형/망형의 한계를 극복한 혁신적 모델
- **[데이터 모델 구성요소](@/studynotes/5_database/1_relational/14_data_model_components.md)**: 구조/연산/제약의 3대 요소
- **[B-Tree 인덱스](@/studynotes/5_database/1_relational/b_tree_index.md)**: 계층적 트리 구조의 인덱싱 활용
- **[NoSQL](@/studynotes/5_database/1_relational/nosql.md)**: 계층적 문서 구조의 현대적 계승

---

### 👶 어린이를 위한 3줄 비유 설명

1. **가족 족보**: 할아버지가 최상위에 계시고, 그 밑에 아빠, 그 밑에 나! 이렇게 한 줄기로만 내려가는 게 계층형 모델이에요. 아빠는 한 분이지만 자식은 여러 명일 수 있죠!

2. **폴더 안의 폴더**: 컴퓨터에서 '내 문서' 폴더를 열면 그 안에 또 폴더가 있고, 그 안에 또 폴더가 있어요. 이렇게 위에서 아래로만 내려가는 구조예요!

3. **친구를 두 집에서 살게 못 해요**: 계층형 모델에서는 한 아이가 두 명의 엄마를 가질 수 없어요. 그래서 친구가 두 부서에 속해야 하면 똑같은 친구 정보를 두 번 써야 한답니다. 이게 바로 계층형의 단점이에요!
