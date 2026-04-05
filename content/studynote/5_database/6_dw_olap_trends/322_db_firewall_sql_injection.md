+++
title = "322. DB 방화벽 / SQL 인젝션"
weight = 4322
+++

> **💡 핵심 인사이트**
> DB 방화벽(Database Firewall)은 **"데이터베이스에 접근하는 SQL 트래픽을가로채어, 사전에 정의된 보안 정책 위반 여부를リアルタイム檢查하고 공격을 차단하는 미들웨어"**입니다.
> SQL 인젝션(SQL Injection)은 이 DB 방화벽이防止하는 대표적인 공격 유형으로, **"사용자 입력을 SQL 查询에そのまま 삽입하여 数据库를Manipulate하는 해킹 기법"**입니다. OWASP Top 10에서 매년 반복되는常習犯であり、入力 검증不足から生みます。

---

## Ⅰ. SQL 인젝션의 원리: 입력이 명령이 되는 순간

```
[SQL 인젝션 원리]

  정상な入力:
  사용자: "김철수" 검색
  SQL: SELECT * FROM users WHERE name = '김철수'
  결과: 김철수인 사용자 정보 반환

  SQL 인젝션 공격:
  공격자: "' OR '1'='1" 입력  ← 쿼리 문법 변화!
  SQL: SELECT * FROM users WHERE name = '' OR '1'='1'
  의미: '1'='1'은 항상 TRUE
  결과: users 테이블 전체 데이터 반환 (認証 bypass!)
```

### SQL 인젝션의 4가지 유형

```
[SQL 인젝션 유형]

  1. In-Band SQLi (일반적)
     - 공격자가 같은 채널로 데이터 추출
     - 에러 메시지를利用한 In-Band
     - Union 쿼리를利用한 In-Band

  2. Blind SQLi (블라인드)
     - 에러 메시지 없음
     - "TRUE면 페이지 정상, FALSE면 다르게 표시" 利用
     - 시간 기반 (SLEEP() 利用) 블라인드

  3. Out-of-Band SQLi
     - 정상 채널 대신 우회 채널 (DNS, HTTP 요청)
     - 블라인드 환경에서 우회 채널로 데이터 탈취

  4. Second-Order SQLi
     - 악성 입력 저장 → لاحق에 다른 요청에서 실행
     - 즉각 실행이 아닌 "지연된 인젝션"
```

**실제 공격 코드 예시:**

```python
# 취약한 코드 (Python + SQLite)
user_input = request.form['username']
query = f"SELECT * FROM users WHERE username = '{user_input}'"
# 공격자가 username에 "admin' --" 입력 시
# query = "SELECT * FROM users WHERE username = 'admin' --'"
# -- 이후는 주석처리 → 비밀번호 검증 우회!

# UNION 인젝션 (데이터 탈취)
# "' UNION SELECT credit_card FROM payments --"
# → 기존 쿼리 결과 + 카드번호 테이블 합산
```

---

## Ⅱ. DB 방화벽의 작동 원리

```
[DB 방화벽 아키텍처]

  Application                    DBMS
     │                           │
     │ SELECT * FROM users...    │
     │ ───────────────────────► │  (클라이언트 → DB 직접 아닌)
     │                           │
     │      ┌────────────────────┤
     │      │                    │
     │      ▼                    │
     │ ┌─────────────┐            │
     │ │ DB Firewall │            │
     │ │             │            │
     │ │ 1. SQL 파싱 │            │
     │ │ 2. 정책 체크 │            │
     │ │ 3. 공격 탐지 │            │
     │ │ 4. 로깅/경고 │            │
     │ │ 5. 차단/허용 │            │
     │ └─────────────┘            │
     │      │                    │
     │      ▼                    │
     │ SELECT * FROM users...    │
     │ ───────────────────────► │
     │                           │
     │ ◄─────────────────────── │
     │ [정상 결과 또는 차단 알림]  │
     └───────────────────────────┘

  * Inline 모드: 방화벽이 실제 트래픽을 전달하면서検査
  * Mirror 모드: TAP/SPAN으로 트래픽 복사해서検査 (대량 트래픽)
```

### 방화벽이 탐지하는 패턴

```yaml
# DB 방화벽 탐지 규칙 예시
rules:
  # 1. SQL 문법 이상 탐지
  - name: "unterminated_string"
    pattern: "SELECT.*FROM.*WHERE.*'$"
    severity: HIGH

  # 2. 주석亂用 탐지 (-- 주석으로 필터 우회)
  - name: "comment_injection"
    pattern: ".*--.*"
    severity: MEDIUM

  # 3. 시스템 테이블 접근 탐지
  - name: "system_table_access"
    pattern: ".*(mysql\.|pg_|sys\.|information_schema).*"
    severity: HIGH

  # 4. 비정상적으로 긴 SQL 탐지
  - name: " oversized_query"
    max_length: 10000
    severity: MEDIUM

  # 5. 다중 SQL 문 (세미콜론으로 분리)
  - name: "multiple_statements"
    pattern: ".*;.*(DROP|DELETE|INSERT|UPDATE).*"
    severity: CRITICAL

  # 6. 시간 지연 기반 블라인드 SQLi 탐지 (SLEEP/BENCHMARK)
  - name: "time_based_blind_injection"
    pattern: ".*(SLEEP\(|BENCHMARK\().*"
    severity: HIGH
```

---

## III. SQL 인젝션 방어 전략: Defense in Depth

```
[SQL 인젝션 방어 5단계]

  Layer 1: 입력 검증 (Input Validation) ★가장 중요
  ┌──────────────────────────────────────────────┐
  │ - 화이트리스트 방식: 허용된 문자만 입력 가능    │
  │ - 사용자名的: "'", ";", "--", "/*" 等 차단   │
  │ - 타입 검증: username은 alphanumeric만 허용   │
  └──────────────────────────────────────────────┘
                    │
  Layer 2: Prepared Statement (파라미터화 쿼리)
  ┌──────────────────────────────────────────────┐
  │ # 취약한 코드                                  │
  │ query = f"SELECT * FROM users WHERE id={id}" │
  │                                              │
  │ # 안전한 코드 (Prepared Statement)             │
  │ cursor.execute("SELECT * FROM users WHERE id=?", (id,)) │
  │ # 파라미터가 문자열로 escaping되어 삽입       │
  └──────────────────────────────────────────────┘
                    │
  Layer 3: Stored Procedure (파라미터 자동 이스케이프)
  ┌──────────────────────────────────────────────┐
  │ - 애플리케이션에서 직접 SQL 미작성              │
  │ - DB에 사전 정의된 프로시저만 호출               │
  │ - 단, 프로시저 내부 문자열 동적 생성 시 주의     │
  └──────────────────────────────────────────────┘
                    │
  Layer 4: ORM (Object-Relational Mapping)
  ┌──────────────────────────────────────────────┐
  │ - SQL을 개발자가 직접 작성하지 않음             │
  │ - Django ORM, Hibernate 등이 파라미터 처리     │
  │ - But: 복잡한 쿼리에서는 Native SQL 불가피     │
  └──────────────────────────────────────────────┘
                    │
  Layer 5: DB 방화벽 +最小 권한 원칙
  ┌──────────────────────────────────────────────┐
  │ - DB 방화벽으로 알려진 공격 패턴 실시간 차단     │
  │ - 애플리케이션 계정은 DDL 권한 없음            │
  │ - 읽기 전용 계정과 쓰기 계정 분리               │
  └──────────────────────────────────────────────┘
```

---

## Ⅳ. Prepared Statement의重要性

```python
# 취약한 코드 vs 안전한 코드 비교

# ❌ 취약한 코드 (Python)
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    # username에 "admin' --" 입력 시 → 전체 사용자 노출

# ✅ 안전한 코드 (Prepared Statement)
def get_user(username):
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    # 파라미터가 자동으로 이스케이프 처리됨

# ❌ 취약한 코드 (PHP)
$query = "SELECT * FROM users WHERE id = " . $_GET['id'];
// http://site.com/?id=1 OR 1=1 → 전체 데이터 노출

# ✅ 안전한 코드 (PHP PDO)
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = :id");
$stmt->execute(['id' => $_GET['id']]);
```

---

## Ⅴ. 실제 공격 시나리오と 📢 비유

**실제 SQL 인젝션으로 인한 피해 사례:**

```
[대규모 데이터 유출 사례]

  2017년 Equifax 데이터 유출:
  - Apache Struts 취약점 (SQL 인젝션과 유사한Injection 계열)
  - 1억 4,700만 명 정보 유출

  2022년 Log4j (Log4Shell):
  - 로그 메시지 내Injection → 시스템 명령 실행
  - SQL 인젝션과 같은 "입력값이 실행 코드로 변하는" 원리

 SQL 인젝션 피해:
  1. 데이터 베이스 전체 데이터 유출
  2. 관리자 계정 탈취 (認証 bypass)
  3. 테이블 삭제/변조 (DROP, UPDATE)
  4. 백도어 설치 ( INTO OUTFILE)
  5. 대상 서버 제어권 취득 ( xp_cmdshell)
```

> 📢 **섹션 요약 비유:** SQL 인젝션은 **"은행 창구의 작은 틈새"**와 같습니다. 은행원이 "이름을 말해주세요"라고 하면 정직한 사람은 "김철수"라고 답합니다. 그런데 악의적인 사람이 "김철수라고 말하고, 그리고 오늘 편한 금액으로 다 찾아가겠습니다"라고 이어서 말하면, 은행원이 "네?" 하고全部 그대로 처리해버리는 것이죠. DB 방화벽은 이 **"창구 직원이 받는 모든 말에서 부적절한 지시를 솎아내는 교육과 자동 시스템"**이고, Prepared Statement는 **"은행원이 고객의 말과 지시를 분리해서 받아들이는 창구 규칙"**입니다. **"사용자 입력을 절대로 SQL 명령어와混淆하지 않는"** 것이 핵심입니다.
