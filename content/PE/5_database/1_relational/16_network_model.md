+++
title = "망형 데이터 모델 (Network Data Model)"
description = "그래프 구조, CODASYL DBTG, M:N 관계 표현, SET 개념 심층 분석"
date = "2026-03-05"
[taxonomies]
tags = ["database", "network-model", "codasyl", "graph-structure", "legacy-db"]
categories = ["studynotes-5_database"]
+++

# 16. 망형 데이터 모델 (Network Data Model)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터를 그래프(Graph) 구조로 조직화하여 다중 부모(Multiple Parents)와 M:N 관계를 표현할 수 있는 데이터 모델로, 1969년 CODASYL DBTG(Data Base Task Group)에서 표준화되었습니다.
> 2. **가치**: 계층형 모델의 한계(1:N 제약)를 극복하여 복잡한 현실 세계의 관계를 보다 자연스럽게 모델링할 수 있으며, 데이터 중복을 50~70% 감소시킵니다.
> 3. **융합**: 현대 그래프 데이터베이스(Neo4j), 지식 그래프, ER 모델의 다대다 관계 표현의 이론적 기반이 되었습니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의

**망형 데이터 모델(Network Data Model)**은 데이터를 레코드 타입(Record Type)과 이들을 연결하는 SET로 구성된 그래프 구조로 표현하는 데이터베이스 모델입니다. 계층형 모델이 트리 구조(단일 부모)인 반면, 망형 모델은 레코드가 여러 부모를 가질 수 있는 그래프 구조를 허용합니다.

**핵심 개념 정의**:

1. **레코드 타입(Record Type)**: 데이터의 논리적 단위
   - 계층형의 세그먼트와 유사
   - 필드(Field)들의 집합
   - 예: 학생, 과목, 교수

2. **SET**: 두 레코드 타입 간의 1:N 관계
   - 오너(Owner) 레코드 타입: 1 측
   - 멤버(Member) 레코드 타입: N 측
   - 예: 학생-수강(학생이 오너, 수강이 멤버)

3. **SET 타입(Set Type)**: SET의 명명된 정의
   - 오너와 멤버 간의 관계 이름
   - 순서(ORDER) 정의 가능

4. **다중 부모(Multiple Parents)**: 한 레코드가 여러 SET에 멤버로 참여 가능
   - M:N 관계 표현의 핵심
   - 계층형과의 결정적 차이

**CODASYL DBTG의 역사적 의의**:
- 1969년: CODASYL(Data Base Task Group) 보고서 발간
- 1971년: COBOL JOD(Journal of Development) 채택
- 주요 구현: IDMS, Raima Database Manager, TurboIMAGE

#### 2. 💡 비유를 통한 이해

**소셜 네트워크**로 비유할 수 있습니다:
- **레코드 타입** = 사람 (개별 프로필)
- **SET** = "친구" 관계, "팔로우" 관계
- **오너/멤버** = 내가 팔로우하는 사람 / 나를 팔로우하는 사람
- **다중 부모** = 한 사람이 여러 그룹에 속할 수 있음

**대학 수강 시스템**으로 비유:
```
학생 '홍길동'은:
- '데이터베이스' 과목을 수강 (SET 1: 학생-수강)
- '알고리즘' 과목을 수강 (SET 2: 학생-수강)
- '컴퓨터공학과' 소속 (SET 3: 학과-학생)

과목 '데이터베이스'는:
- '홍길동'이 수강 (SET 1)
- '김철수'가 수강 (SET 1)
- '이교수'가 강의 (SET 4: 교수-과목)
```

이렇게 한 레코드가 여러 관계(SET)에 동시에 참여할 수 있는 것이 망형 모델의 핵심입니다.

#### 3. 등장 배경 및 발전 과정

**1단계: 계층형 모델의 한계 인식 (1960년대 중반)**
- IBM IMS의 1:N 제약이 복잡한 현실을 반영하지 못함
- M:N 관계 표현을 위한 데이터 중복 문제
- 예: 학생-과목, 부서-프로젝트 등

**2단계: CODASYL DBTG 표준화 (1969~1971년)**
- Charles Bachman이 GE에서 개발한 IDS(Integrated Data Store) 기반
- 그래프 구조로 M:N 관계 자연스럽게 표현
- "Bachman Diagram"으로 시각화

**3단계: 전성기 (1970~1980년대)**
- IDMS (Cullinane Corp): 가장 성공적인 상용 망형 DBMS
- DEC DBMS-10, Honeywell IDS/2
- 은행, 보험, 항공사 등 대형 시스템

**4단계: 관계형 모델에 의한 쇠퇴 (1980~1990년대)**
- SQL의 선언적 접근이 네비게이션 방식보다 우위
- 복잡한 SET 조작 코드 vs 단순한 SQL
- 표준화 부재로 벤더 종속 심화

**5단계: 현대적 계승 (2000년대~현재)**
- 그래프 데이터베이스의 이론적 기반
- ER 모델의 M:N 관계 표현
- 지식 그래프, 소셜 네트워크 분석

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 망형 모델 핵심 구성요소 (표)

| 구성요소 | 정의 | 특성 | CODASYL 용어 | 예시 |
|:---|:---|:---|:---|:---|
| **레코드 타입** | 데이터 저장 단위 | 필드들의 집합 | Record Type | 학생, 과목 |
| **필드** | 레코드 내 데이터 항목 | 원자값 | Data Item | 학번, 이름 |
| **SET 타입** | 1:N 관계 정의 | 오너-멤버 구조 | Set Type | 학생-수강 |
| **오너(Owner)** | SET의 1 측 레코드 | 상위 레코드 | Owner Record | 학생 |
| **멤버(Member)** | SET의 N 측 레코드 | 하위 레코드 | Member Record | 수강 |
| **SET 발생** | 실제 연결 인스턴스 | 오너 1:멤버 N | Set Occurrence | 홍길동의 수강 목록 |
| **SET 모드** | 멤버 삽입 순서 | FIRST, LAST, NEXT, PRIOR | Set Order | LAST |
| **SET 멤버십** | 멤버 참여 방식 | AUTOMATIC, MANUAL | Set Membership | 자동/수동 연결 |

#### 2. 망형 데이터 모델 구조 다이어그램

```text
+============================================================================+
|                      NETWORK DATA MODEL ARCHITECTURE                        |
+============================================================================+
|                                                                             |
|    [레코드 타입: STUDENT]           [레코드 타입: COURSE]                    |
|    +------------------+            +------------------+                     |
|    | 학번 (PK)        |            | 과목코드 (PK)    |                     |
|    | 이름             |            | 과목명           |                     |
|    | 학과             |            | 학점             |                     |
|    +--------+---------+            +--------+---------+                     |
|             |                               |                              |
|             |  SET: ENROLLMENT              |                              |
|             |  (학생-수강관계)                |  SET: TEACHES                |
|             |                               |  (과목-교수관계)              |
|             v                               v                              |
|    +------------------+            +------------------+                     |
|    | [레코드: ENROLL] |            | [레코드: PROF]   |                     |
|    | 학번 (FK)        |            | 교수번호 (PK)    |                     |
|    | 과목코드 (FK)    |<---------->| 교수명           |                     |
|    | 성적             |  SET       | 학과             |                     |
|    +------------------+  TEACHES   +------------------+                     |
|             ^                                                               |
|             |                                                               |
|             +-------------------+                                           |
|                                 |                                           |
|                    [SET: DEPT-STUDENT]  (학과-학생관계)                      |
|                                 |                                           |
|                    +------------v------------+                              |
|                    | [레코드: DEPARTMENT]    |                              |
|                    | 학과코드 (PK)           |                              |
|                    | 학과명                  |                              |
|                    +-------------------------+                              |
|                                                                             |
+============================================================================+

[Bachman Diagram 표기법]

     STUDENT                ENROLLMENT               COURSE
    +--------+             +------------+           +--------+
    | 학번   |---SET1----->| 학번,과목코드|<---SET2---|과목코드|
    | 이름   |             | 성적       |           |과목명  |
    | 학과   |             +------------+           |학점    |
    +--------+                                         ^     |
                                                       |     |
                                                       +--+  |
                                                          |  |
                     DEPARTMENT                         SET3|
                    +-----------+                          |  |
                    | 학과코드  |--------------------------+  |
                    | 학과명    |   SET: DEPT-COURSE          |
                    +-----------+
```

#### 3. 심층 동작 원리: SET와 네비게이션

**1단계: 스키마 정의 (DDL - CODASYL)**
```cobol
* CODASYL Data Schema Definition
* 대학 수강 관리 데이터베이스

SCHEMA NAME IS UNIVERSITY-DB.

* 레코드 타입 정의
RECORD NAME IS STUDENT.
    02 STUDENT-ID      TYPE PIC X(10).
    02 STUDENT-NAME    TYPE PIC X(30).
    02 DEPT-CODE       TYPE PIC X(5).

RECORD NAME IS COURSE.
    02 COURSE-CODE     TYPE PIC X(8).
    02 COURSE-NAME     TYPE PIC X(50).
    02 CREDITS         TYPE PIC 9.

RECORD NAME IS ENROLLMENT.
    02 STUDENT-ID      TYPE PIC X(10).
    02 COURSE-CODE     TYPE PIC X(8).
    02 GRADE           TYPE PIC X(2).

* SET 타입 정의
SET NAME IS STUDENT-ENROLL
    OWNER IS STUDENT
    MEMBER IS ENROLLMENT
    ORDER IS LAST
    SET MODE IS CHAIN
    MEMBER AUTOMATIC
    LINKED TO OWNER.

SET NAME IS COURSE-ENROLL
    OWNER IS COURSE
    MEMBER IS ENROLLMENT
    ORDER IS LAST
    SET MODE IS CHAIN
    MEMBER AUTOMATIC
    LINKED TO OWNER.
```

**2단계: 데이터 조작 (DML - 네비게이션)**
```cobol
* CODASYL DML 예시
* 학생의 모든 수강 과목 조회

* 1. 특정 학생 레코드 찾기
MOVE '20260001' TO STUDENT-ID.
FIND ANY STUDENT USING STUDENT-ID.
IF NOT FOUND GO TO STUDENT-NOT-FOUND.

* 2. 학생의 첫 번째 수강 레코드로 이동
FIND FIRST ENROLLMENT WITHIN STUDENT-ENROLL.
PERFORM UNTIL DB-STATUS NOT = '00000'
    * 3. 수강 레코드에서 과목 정보 가져오기
    GET ENROLLMENT
    * 4. 과목 오너로 이동
    FIND OWNER WITHIN COURSE-ENROLL
    GET COURSE
    DISPLAY COURSE-NAME, GRADE
    * 5. 다음 수강 레코드로 이동
    FIND NEXT ENROLLMENT WITHIN STUDENT-ENROLL
END-PERFORM.
```

**3단계: 망형 모델의 네비게이션 알고리즘 구현**

```python
"""
망형 데이터 모델의 SET 기반 네비게이션 구현
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

class SetOrder(Enum):
    """SET 멤버 순서 옵션"""
    FIRST = "FIRST"    # 새 멤버를 첫 번째에
    LAST = "LAST"      # 새 멤버를 마지막에
    NEXT = "NEXT"      # 현재 위치 다음에
    PRIOR = "PRIOR"    # 현재 위치 이전에
    SORTED = "SORTED"  # 정렬 순서

class MembershipOption(Enum):
    """SET 멤버십 옵션"""
    AUTOMATIC = "AUTOMATIC"  # 레코드 생성 시 자동 연결
    MANUAL = "MANUAL"        # 명시적 CONNECT 필요

@dataclass
class Record:
    """망형 모델의 레코드"""
    record_type: str
    data: dict
    record_id: str
    # 포인터들 (SET 연결용)
    owner_pointers: dict = field(default_factory=dict)  # SET이름 -> 오너 레코드
    member_pointers: dict = field(default_factory=dict)  # SET이름 -> [멤버 레코드들]
    next_pointers: dict = field(default_factory=dict)    # SET이름 -> 다음 멤버
    prior_pointers: dict = field(default_factory=dict)   # SET이름 -> 이전 멤버

@dataclass
class SetType:
    """SET 타입 정의"""
    set_name: str
    owner_type: str
    member_type: str
    order: SetOrder = SetOrder.LAST
    membership: MembershipOption = MembershipOption.AUTOMATIC

class NetworkDatabase:
    """망형 데이터베이스 시뮬레이션"""

    def __init__(self, name: str):
        self.name = name
        self.record_types: dict[str, list[Record]] = {}
        self.set_types: dict[str, SetType] = {}
        self.current_of_run_unit: Optional[Record] = None  # 현재 레코드

    def define_record_type(self, type_name: str) -> None:
        """레코드 타입 정의"""
        self.record_types[type_name] = []

    def define_set_type(self, set_type: SetType) -> None:
        """SET 타입 정의"""
        self.set_types[set_type.set_name] = set_type

    def store_record(self, record: Record) -> Record:
        """레코드 저장 (STORE 명령)"""
        if record.record_type not in self.record_types:
            self.record_types[record.record_type] = []

        self.record_types[record.record_type].append(record)
        self.current_of_run_unit = record

        # AUTOMATIC 멤버십 처리
        for set_name, st in self.set_types.items():
            if st.member_type == record.record_type:
                if st.membership == MembershipOption.AUTOMATIC:
                    # 해당 오너 레코드 찾아 자동 연결
                    pass  # 실제로는 오너 찾는 로직 필요

        return record

    def find_any(self, record_type: str, key_field: str, key_value: str) -> Optional[Record]:
        """FIND ANY - 임의 검색"""
        for record in self.record_types.get(record_type, []):
            if record.data.get(key_field) == key_value:
                self.current_of_run_unit = record
                return record
        return None

    def find_first_within_set(self, set_name: str) -> Optional[Record]:
        """FIND FIRST WITHIN SET - SET 내 첫 번째 멤버"""
        if self.current_of_run_unit is None:
            return None

        owner = self.current_of_run_unit
        members = owner.member_pointers.get(set_name, [])
        if members:
            self.current_of_run_unit = members[0]
            return members[0]
        return None

    def find_next_within_set(self, set_name: str) -> Optional[Record]:
        """FIND NEXT WITHIN SET - SET 내 다음 멤버"""
        if self.current_of_run_unit is None:
            return None

        current = self.current_of_run_unit
        next_member = current.next_pointers.get(set_name)
        if next_member:
            self.current_of_run_unit = next_member
            return next_member
        return None

    def find_owner_within_set(self, set_name: str) -> Optional[Record]:
        """FIND OWNER WITHIN SET - SET의 오너 찾기"""
        if self.current_of_run_unit is None:
            return None

        current = self.current_of_run_unit
        owner = current.owner_pointers.get(set_name)
        if owner:
            self.current_of_run_unit = owner
            return owner
        return None

    def connect_to_set(self, set_name: str, owner: Record, member: Record) -> None:
        """CONNECT - 멤버를 SET에 연결"""
        set_type = self.set_types[set_name]

        # 오너의 멤버 리스트에 추가
        if set_name not in owner.member_pointers:
            owner.member_pointers[set_name] = []

        members = owner.member_pointers[set_name]

        # 포인터 연결 (이중 연결 리스트)
        if members:
            last_member = members[-1]
            last_member.next_pointers[set_name] = member
            member.prior_pointers[set_name] = last_member

        members.append(member)
        member.owner_pointers[set_name] = owner

    def traverse_set(self, set_name: str, owner: Record) -> list[Record]:
        """SET 순회 - 오너의 모든 멤버 반환"""
        return owner.member_pointers.get(set_name, [])

# 사용 예시: 대학 수강 관리 시스템
db = NetworkDatabase("UniversityDB")

# 레코드 타입 정의
db.define_record_type("STUDENT")
db.define_record_type("COURSE")
db.define_record_type("ENROLLMENT")

# SET 타입 정의
db.define_set_type(SetType("STUDENT-ENROLL", "STUDENT", "ENROLLMENT"))
db.define_set_type(SetType("COURSE-ENROLL", "COURSE", "ENROLLMENT"))

# 레코드 생성
student1 = db.store_record(Record("STUDENT",
    {"STUDENT_ID": "S001", "NAME": "홍길동", "DEPT": "컴퓨터공학"}, "S001"))
student2 = db.store_record(Record("STUDENT",
    {"STUDENT_ID": "S002", "NAME": "김철수", "DEPT": "컴퓨터공학"}, "S002"))

course1 = db.store_record(Record("COURSE",
    {"COURSE_ID": "C001", "NAME": "데이터베이스", "CREDITS": 3}, "C001"))
course2 = db.store_record(Record("COURSE",
    {"COURSE_ID": "C002", "NAME": "알고리즘", "CREDITS": 3}, "C002"))

# 수강 레코드 (M:N 관계 표현)
enroll1 = db.store_record(Record("ENROLLMENT",
    {"GRADE": "A"}, "E001"))
enroll2 = db.store_record(Record("ENROLLMENT",
    {"GRADE": "B+"}, "E002"))
enroll3 = db.store_record(Record("ENROLLMENT",
    {"GRADE": "A+"}, "E003"))

# SET 연결 (M:N 관계 구현)
db.connect_to_set("STUDENT-ENROLL", student1, enroll1)
db.connect_to_set("COURSE-ENROLL", course1, enroll1)  # enroll1은 두 SET에 참여!

db.connect_to_set("STUDENT-ENROLL", student1, enroll2)
db.connect_to_set("COURSE-ENROLL", course2, enroll2)

db.connect_to_set("STUDENT-ENROLL", student2, enroll3)
db.connect_to_set("COURSE-ENROLL", course1, enroll3)  # course1은 두 학생이 수강!

# 네비게이션: 학생1의 모든 수강 과목 조회
print("홍길동의 수강 과목:")
db.find_any("STUDENT", "STUDENT_ID", "S001")  # 학생1 위치
enroll = db.find_first_within_set("STUDENT-ENROLL")
while enroll:
    db.find_owner_within_set("COURSE-ENROLL")  # 과목 오너로 이동
    print(f"  - {db.current_of_run_unit.data['NAME']}: {enroll.data['GRADE']}")
    db.current_of_run_unit = enroll  # 다시 수강 레코드로
    enroll = db.find_next_within_set("STUDENT-ENROLL")
```

#### 4. M:N 관계 표현 메커니즘

```text
[계층형 모델에서의 M:N 표현 문제]

학생 --- ??? --- 과목
  |              |
  +-- 수강1 ----+
  +-- 수강2 ----+ (중복 불가피)

[망형 모델에서의 M:N 표현 해결]

         STUDENT-ENROLL SET
    STUDENT <=============> ENROLLMENT <=============> COURSE
         (1:N)                  (N:1)         COURSE-ENROLL SET

    - 학생1 --SET1--> 수강A <--SET2-- 과목1
           |                  ^
           +--> 수강B <-------+
                          |
    - 학생2 --SET1--> 수강C <-+
                          |
           +--> 수강D <--SET2-- 과목2

[핵심 포인트]
1. 연결 레코드(ENROLLMENT)가 두 개의 SET에 동시에 참여
2. STUDENT-ENROLL SET: 학생이 오너, 수강이 멤버 (1:N)
3. COURSE-ENROLL SET: 과목이 오너, 수강이 멤버 (1:N)
4. 두 SET의 조합으로 M:N 관계 표현
5. 데이터 중복 없이 관계만 저장
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 계층형 vs 망형 vs 관계형 모델 심층 비교

| 비교 항목 | 계층형 모델 | 망형 모델 | 관계형 모델 |
|:---|:---|:---|:---|
| **데이터 구조** | 트리 (Tree) | 그래프 (Graph) | 테이블 (Table) |
| **부모 수** | 최대 1개 | 여러 개 | 없음 (FK 참조) |
| **M:N 관계** | 불가 (중복 해결) | SET 조합으로 가능 | 조인 테이블로 자연스럽게 |
| **데이터 접근** | 경로 네비게이션 | SET 네비게이션 | 선언적 SQL |
| **포인터** | 물리적 포인터 | 물리적 포인터 | 논리적 참조 (FK) |
| **데이터 독립성** | 낮음 | 낮음 | 높음 |
| **표준화** | IBM IMS | CODASYL DBTG | ANSI/ISO SQL |
| **학습 곡선** | 중간 | 높음 | 낮음 |
| **성능 (순차)** | 우수 | 우수 | 중간 |
| **유연성** | 낮음 | 중간 | 높음 |

#### 2. 망형 모델 vs 현대 그래프 DB 비교

| 비교 항목 | 망형 모델 (CODASYL) | 그래프 DB (Neo4j) |
|:---|:---|:---|
| **데이터 구조** | 레코드 + SET | 노드 + 엣지 |
| **관계 표현** | 1:N SET만 | N:N 엣지 자유롭게 |
| **쿼리 언어** | 네비게이션 DML | Cypher, Gremlin |
| **스키마** | 강한 스키마 | 유연한 스키마 |
| **방향성** | 오너→멤버 단방향 | 양방향 가능 |
| **순회 효율** | 높음 (포인터) | 높음 (인덱스) |
| **적용 분야** | 트랜잭션 처리 | 관계 분석, 추천 |

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

**시나리오 1: 레거시 IDMS 마이그레이션**
- 상황: 보험사의 30년 된 IDMS 시스템
- 판단: 관계형 DB로의 완전 마이그레이션
- 전략:
  1. SET 구조를 FK 관계로 매핑
  2. 연결 레코드를 조인 테이블로 변환
  3. 네비게이션 코드를 SQL 쿼리로 재작성
  4. 성능 검증 후 단계적 전환

**시나리오 2: 복잡한 관계 분석 시스템**
- 상황: 사회관계망분석(SNA), 추천 시스템
- 판단: 망형 개념을 그래프 DB로 구현
- 전략:
  - 노드 = 레코드 타입
  - 엣지 = SET (양방향으로 확장)
  - Cypher 쿼리로 관계 분석

#### 2. 도입 시 고려사항 (체크리스트)

**망형 모델 적용 판별**:
- [ ] M:N 관계가 핵심적인가?
- [ ] 순차 네비게이션이 주요 패턴인가?
- [ ] 관계가 비교적 안정적인가?
- [ ] 레거시 시스템과의 호환성이 필요한가?

**현대적 대안 검토**:
- [ ] 관계형 + 조인 테이블 (가장 일반적)
- [ ] 그래프 DB (관계 분석 중심)
- [ ] NoSQL + 임베디드/참조 (유연성)

#### 3. 안티패턴 (Anti-patterns)

1. **과도한 SET 복잡도**: SET 관계가 너무 복잡하면 관리 불가능
   - 해결: 관계형으로 재설계

2. **포인터 남용**: 모든 것을 포인터로 연결
   - 해결: 필요한 관계만 SET로 정의

3. **무분별한 AUTOMATIC**: 자동 연결로 의도치 않은 관계
   - 해결: MANUAL 멤버십으로 명시적 제어

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 정량적/정성적 기대효과

| 구분 | 계층형 모델 | 망형 모델 | 관계형 모델 |
|:---|:---|:---|:---|
| **M:N 표현** | 불가능 | 가능 | 자연스러움 |
| **데이터 중복** | 높음 | 중간 | 낮음 |
| **개발 복잡도** | 중간 | 높음 | 낮음 |
| **순차 접근 성능** | 높음 | 높음 | 중간 |
| **유지보수성** | 낮음 | 낮음 | 높음 |

#### 2. 미래 전망 및 진화 방향

**망형 모델의 현대적 계승**:
- **그래프 데이터베이스**: SET → 엣지, 레코드 → 노드
- **ER 모델의 M:N**: 연결 엔티티 패턴
- **객체지향 모델**: 객체 참조의 원리

**학습 가치**:
- 데이터 모델링의 역사적 맥락
- 관계형 모델의 등장 배경 이해
- 그래프 DB의 이론적 기반

#### 3. 참고 표준/가이드

| 표준 | 내용 | 적용 범위 |
|:---|:---|:---|
| **CODASYL DBTG** | 망형 DB 표준 (1969) | 역사적 표준 |
| **IDMS** | 상용 망형 DBMS | 메인프레임 |
| **ISO 9075** | SQL 표준 (관계형) | 현대 표준 |
| **Neo4j Cypher** | 그래프 쿼리 언어 | 현대 계승 |

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[계층형 데이터 모델](@/studynotes/5_database/1_relational/15_hierarchical_model.md)**: 망형 모델의 전신, 트리 구조
- **[관계형 데이터 모델](@/studynotes/5_database/1_relational/relational_model.md)**: 망형의 한계를 극복한 혁신
- **[ER 모델](@/studynotes/5_database/1_relational/er_model.md)**: M:N 관계의 개념적 모델링
- **[외래 키](@/studynotes/5_database/1_relational/foreign_key.md)**: 관계형에서의 SET 대체
- **[그래프 데이터베이스](@/studynotes/5_database/6_nosql/graph_database.md)**: 망형 모델의 현대적 계승

---

### 👶 어린이를 위한 3줄 비유 설명

1. **친구들의 관계망**: 나는 학교 친구도 있고, 학원 친구도 있고, 이웃 친구도 있어요. 한 친구가 여러 그룹에 동시에 속할 수 있는 게 망형 모델이에요. 계층형은 한 그룹에만 속해야 했는데 말이죠!

2. **수업 시간표**: 국어 시간에는 홍길동, 김철수가 같이 듣고, 수학 시간에는 홍길동, 이영희가 같이 들어요. 한 학생이 여러 과목을 듣고, 한 과목에 여러 학생이 듣는 게 망형 모델로 표현돼요!

3. **거미줄 같은 연결**: 거미줄처럼 이리저리 여러 방향으로 연결되어 있어서, 어디서든 원하는 정보를 찾아갈 수 있어요. 단방향 길만 있는 계층형보다 훨씬 자유로워요!
