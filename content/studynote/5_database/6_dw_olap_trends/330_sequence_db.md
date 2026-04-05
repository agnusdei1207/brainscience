+++
title = "330. 시퀀스 데이터베이스"
weight = 4330
+++

> **💡 핵심 인사이트**
> 시퀀스 데이터베이스(Sequence Database)는 **"문자열이나 수열처럼 순서가 있는 연속적 데이터를 저장·검색·분석하는 데特화된 데이터베이스"**입니다.
> 전통적인 관계형 DB가 "행vs열" 구조에 특화되어 있다면, 시퀀스 DB는 **"앞뒤 관계와局所적 패턴이 중요한 데이터(유전자, 음성, 웹 로그, 고속도로 통행 기록)"를stored in a way that enables高效的 pattern matching and similarity search**합니다. 유전자 분석(BLAST), 음성 인식, 금융 시계열 패턴 Mining 등에 핵심적인 역할을 합니다.

---

## Ⅰ. 시퀀스 데이터의特殊性

시퀀스 데이터는 기존 RDB와 근본적으로 다른 특성을 가집니다:

```
[시퀀스 데이터 vs 테이블 형식]

  테이블 형식 (RDB):
  ┌──────┬───────┬────────┐
  │ ID   │ 이름   │ 부서   │
  ├──────┼───────┼────────┤
  │ 1    │ 김철수 │ 영업   │
  │ 2    │ 이영희 │ 개발   │
  │ 3    │ 박지민 │ 개발   │
  └──────┴───────┴────────┘
  → 각 행은 독립적 (순서 중요하지 않음)
  → 키-값 기반 접근이 자연스러움

  시퀀스 형식:
  ┌──────────────────────────────────────────┐
  │  ACCGTAATGC... (유전자 서열)             │
  │  0123456789... (인덱스 위치)             │
  │                                          │
  │  사용자가/foo/bar이 발견된 위치: 3, 15, 27 │
  │  → 인덱스 자체가값어치 (순서가洞見)        │
  └──────────────────────────────────────────┘
  → 순서와 위치가 정보의 핵심
  → 부분열(subsequence) 검색이 主要 操作
```

**시퀀스 데이터의 예:**
- **유전자 서열**: A, C, G, T의 조합 (인간 유전체: 30억 문자)
- **음성 데이터**: 시간에 따른 파형/스펙트로그램
- **웹 클릭 스트림**: 사용자의 사이트 방문 순서
- **주식 거래 로그**: 매수/매도 순서 패턴
- **고속도로 통행 기록**: 차량의 gates 통과 순서

---

## II. 시퀀스 DB의 핵심 操作

```
[시퀀스 DB의 주요 연산]

  1. 부분 일치 (Substring/Subsequence Search)
     "ACGT"가 서열中で初めて出現する 위치는?
     → O(n) 또는 O(n+m) (KMP, Boyer-Moore 등)

  2. 유사 서열 검색 (Similarity Search)
     "ACGT"와 비슷한 서열을 가진 모든 레코드 찾기
     → 편집 거리(Edit Distance) 기반
     → 동적 프로그래밍 (Needleman-Wunsch, Smith-Waterman)

  3. 반복 패턴 발견 (Repeat Discovery)
     "AC"가 10회 이상 반복되는 영역 찾기
     → 접미사 트리/배열 활용

  4. Sequence Alignment (정렬)
     두 서열을 정렬하여similarity 점수 산출
     → 생물정보학의 핵심 연산 (BLAST, ClustalW)
```

### 정렬(Alignment) 알고리즘 예시

```python
# Needleman-Wunsch 알고리즘: 전역 정렬
def needleman_wunsch(seq1, seq2, match_score=1, gap_penalty=-1):
    m, n = len(seq1), len(seq2)

    # DP 테이블 초기화
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 첫 행/열: Gap 패널티 누적
    for i in range(m + 1):
        dp[i][0] = i * gap_penalty
    for j in range(n + 1):
        dp[0][j] = j * gap_penalty

    # DP 채우기
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = dp[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else 0)
            delete = dp[i-1][j] + gap_penalty
            insert = dp[i][j-1] + gap_penalty
            dp[i][j] = max(match, delete, insert)

    return dp[m][n]  # 정렬 점수
```

---

## III. 시퀀스 DB 저장 구조: 접미사 트리/배열

### 접미사 트리 (Suffix Tree)

```
[접미사 트리 예시: "ATCAT$"]

  전체 문자열: ATCAT$
  접미사들:
    0: ATCAT$
    1: TCAT$
    2: CAT$
    3: AT$
    4: T$
    5: $

  ATCAT$
  ├─ A ─┬─ T ─ C ─ A ─ T ─ $
  │     └─ T ─ C ─ A ─ T ─ $
  ├─ C ─ A ─ T ─ $
  ├─ T ─ C ─ A ─ T ─ $
  │     └─ T ─ $
  └─ $

  활용:
  - 부분 문자열 검색: O(m) (m = 패턴 길이)
  - 최장 반복 부분 문자열 찾기
  - 두 접미사의 공통 접두사 찾기
```

### 접미사 배열 (Suffix Array)

```python
# 접미사 배열: 모든 접미사를 정렬한 것
text = "ATCAT$"

# 접미사 생성
suffixes = [
    (0, "ATCAT$"),
    (1, "TCAT$"),
    (2, "CAT$"),
    (3, "AT$"),
    (4, "T$"),
    (5, "$")
]

# 정렬
suffix_array = sorted(suffixes, key=lambda x: x[1])
# 결과: [(5, '$'), (3, 'AT$'), (0, 'ATCAT$'), (2, 'CAT$'), (4, 'T$'), (1, 'TCAT$')]

# 순서만 저장 (정렬된 위치 인덱스)
suffix_array_positions = [5, 3, 0, 2, 4, 1]
# → 메모리 70% 절감 (정렬된 위치만 저장)
```

---

## IV. 시퀀스 DBMS의 실제 시스템

**주요 시퀀스/시계열 DB:**

| 시스템 | 개발사 | 특징 |
|--------|--------|------|
| **BLAST** | NCBI | 유전자 서열 유사성 검색 |
| **UCSC Genome Browser DB** | UCSC | 인간 유전체 브라우저 |
| **SAMtools** | | NGS 시퀀스 데이터 처리 |
| **MUMmer** | | 게놈 비교 알고리즘 |
| **GATK** | Broad Institute | 유전체 분석 파이프라인 |

**관계형 DB의 시퀀스 기능:**

```sql
-- Oracle Sequences (시퀀스 객체)
CREATE SEQUENCE order_seq
  START WITH 1000
  INCREMENT BY 1
  NOMAXVALUE
  NOCYCLE;

-- 사용
INSERT INTO orders (order_id, amount)
VALUES (order_seq.NEXTVAL, 50000);

-- 현재 값 확인
SELECT order_seq.CURRVAL FROM DUAL;

-- PostgreSQL 시퀀스
CREATE SEQUENCE user_id_seq START 1;
SELECT nextval('user_id_seq');  -- 1, 2, 3, ...
```

**MongoDB의 시퀀스 패턴:**

```javascript
// MongoDB: 시퀀스를 구현하는 패턴
// 각 컬렉션에 counter 문서를 두어 순번 관리
db.counters.insertOne({ _id: "order_id", current: 1000 });

function getNextSequence(seqName) {
    const result = db.counters.findOneAndUpdate(
        { _id: seqName },
        { $inc: { current: 1 } },
        { returnNewDocument: true }
    );
    return result.current;
}

// 사용
db.orders.insertOne({
    order_id: getNextSequence("order_id"),
    amount: 50000
});
```

---

## Ⅴ. Sequence Mining과 📢 비유

**频繁 패턴 마이닝 (Frequent Pattern Mining):**

```
[Sequential Pattern Mining]

  상황: 웹 로그에서 사용자들의 구매 패턴 발견

  사용자 A 경로: 메인 → 사과 →香蕉 → 注文完了
  사용자 B 경로: 메인 → 香蕉 → 注文完了
  사용자 C 경로: 메인 → 사과 → 注文完了

  발견된 순차 패턴:
  - "사과 → 注文完了" (A, C 공통)
  - "→ 香蕉 → 注文完了" (B)

  활용:
  - "사과를 본 고객에게香蕉도 추천하면 구매율이提升"
  - 사용자의 다음 행동 예측
```

> 📢 **섹션 요약 비유:** 시퀀스 DB는 **"음악 악보 数据库"**와 같습니다. 음악에서 각 음표(도, 레, 미...)의 위치와 순서가曲の个性을決定하듯이, 시퀀스 데이터도 **"문자의 위치와 순서가情報의核心"**입니다. 전통적 DB가 "이곡의 작곡가는 누구인가?" (키-값 查询)에特化되어 있다면, 시퀀스 DB는 **"이곡과비슷한 멜로디의曲は有哪些인가?"** (유사도 검색)과 **"이旋律에서 4번째 음표부터 8번째 음표까지는?"** (부분 검색)에特化되어 있습니다. 유전자 분석에서 "이 유전자 서열과비슷한 것이 있는가?"를 찾는 것이 바로 이러한 시퀀스 매칭이며, 시퀀스 DB는 그検索을高速化하는専用 도구입니다. **"순서가値어치다"**는 것이 시퀀스 데이터의 핵심 통찰입니다.
