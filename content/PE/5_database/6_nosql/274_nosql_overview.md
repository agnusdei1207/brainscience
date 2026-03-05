+++
title = "NoSQL 데이터베이스 (Not Only SQL)"
date = "2026-03-05"
[extra]
categories = "studynotes-database"
+++

# NoSQL 데이터베이스 (Not Only SQL)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: NoSQL은 관계형 데이터베이스(RDBMS)의 한계를 극복하기 위해 등장한 **스키마리스(Schemaless), 수평 확장(Scale-out), 분산 아키텍처**를 특징으로 하는 비관계형 데이터베이스의 총칭입니다.
> 2. **가치**: 빅데이터, 실시간 웹 애플리케이션, IoT 환경에서 페타바이트급 데이터를 처리하며, RDBMS 대비 10~100배의 쓰기 성능과 선형 확장성을 제공합니다.
> 3. **융합**: CAP 정리에 기반하여 일관성(C), 가용성(A), 분할 내성(P) 중 선택적으로 최적화하며, Key-Value, Document, Column-Family, Graph 등 다양한 데이터 모델을 지원합니다.

---

### I. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**NoSQL(Not Only SQL)**은 전통적인 관계형 데이터베이스(RDBMS)의 테이블-행-열 구조를 따르지 않는 데이터베이스 관리 시스템의 통칭입니다. 2000년대 중반 구글(Bigtable), 아마존(Dynamo)의 논문이 발표된 후, 웹 2.0 시대의 대용량 데이터 처리 요구사항에 대응하여 급속도로 발전했습니다.

**NoSQL의 핵심 특성 (BASE)**:
- **B (Basically Available)**: 기본적으로 항상 사용 가능 (가용성 우선)
- **S (Soft State)**: 상태가 시간에 따라 변할 수 있음 (일관성 완화)
- **E (Eventually Consistent)**: 최종적으로는 일관성 확보 (즉시 일관성 X)

**NoSQL vs RDBMS 비교**:

| 특성 | RDBMS | NoSQL |
|:---|:---|:---|
| **스키마** | 고정 (Schema-on-Write) | 유연 (Schema-on-Read) |
| **확장성** | 수직 확장 (Scale-up) | 수평 확장 (Scale-out) |
| **트랜잭션** | ACID | BASE / Eventual Consistency |
| **조인** | 지원 | 미지원 (애플리케이션에서 처리) |
| **데이터 모델** | 테이블 (정형) | 다양 (반정형, 비정형) |

#### 2. 비유를 통한 이해
NoSQL은 **'주방의 다양한 조리 도구'**에 비유할 수 있습니다.

- **RDBMS**: 모든 요리를 만드는 만능 냄비. 하나로 국, 찌개, 볶음을 다 만들 수 있지만, 대량의 요리가 필요하면 냄비를 더 큰 것으로 교체해야 함 (Scale-up).

- **NoSQL**: 각 요리에 특화된 도구들.
  - **압력밥솥(Key-Value)**: 빠르게 밥을 짓는 데 특화
  - **믹서기(Document)**: 다양한 재료를 섞어 주스/스무디 만듦
  - **대형 찜기(Column-Family)**: 대량의 만두를 한꺼번에 찜
  - **튜브(Graph)**: 복잡한 파이프라인 연결로 관계 표현

  도구가 부족하면 같은 도구를 여러 개 추가 (Scale-out).

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계**: 2000년대 후반, 구글, 페이스북, 아마존 등은 일일 수억 건의 트랜잭션과 페타바이트급 데이터를 처리해야 했습니다. RDBMS의 수직 확장은 비용이 기하급수적으로 증가했고, 샤딩(Sharding)은 복잡도가 너무 높았습니다.

2. **혁신적 패러다임의 도입**:
   - 2003년: 구글 File System (GFS) 논문
   - 2004년: 구글 MapReduce 논문
   - 2006년: 구글 Bigtable 논문 → HBase, Cassandra 탄생
   - 2007년: 아마존 Dynamo 논문 → Riak, DynamoDB 탄생
   - 2009년: MongoDB 최초 릴리즈
   - 2009년: "NoSQL" 용어 공식화 (Johan Oskarsson)

3. **비즈니스적 요구사항**: 현대 디지털 서비스는 실시간 개인화 추천, 소셜 그래프 분석, IoT 센서 데이터 수집, 로그 분석 등 RDBMS로 처리하기 어려운 다양한 요구사항을 가집니다. NoSQL은 이러한 다양성(Variety)과 속도(Velocity)를 처리하기 위한 필수 인프라입니다.

---

### II. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. NoSQL 데이터 모델 4가지 (표)

| 데이터 모델 | 상세 구조 | 대표 제품 | 적합한 사용 사례 | 비유 |
|:---|:---|:---|:---|:---|
| **Key-Value** | Key → Value (단순 매핑) | Redis, Memcached, DynamoDB | 캐싱, 세션, 실시간 데이터 | 사물함 |
| **Document** | JSON/XML 문서 저장 | MongoDB, CouchDB, Elasticsearch | 콘텐츠 관리, 카탈로그 | 서류철 |
| **Column-Family** | 컬럼 패밀리 단위 저장 | Cassandra, HBase, Bigtable | 시계열, 로그, IoT 데이터 | 엑셀 시트 |
| **Graph** | 노드-엣지-프로퍼티 | Neo4j, Neptune, JanusGraph | 소셜 네트워크, 추천, 사기 탐지 | 지도 |

#### 2. NoSQL 아키텍처 다이어그램

```text
================================================================================
                    [ NoSQL Distributed Architecture ]
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                         [ Client Application ]                               │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  Write: PUT user:1001 → {"name": "Alice", "age": 30}                  │ │
│  │  Read:  GET user:1001                                                  │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ API Request
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       [ Coordinator / Router ]                               │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  Consistent Hashing:                                                    │ │
│  │                                                                         │ │
│  │          [ Hash Ring ]                                                  │ │
│  │                    Node3                                               │ │
│  │                   /        \                                           │ │
│  │             Node1            Node5                                     │ │
│  │               |                |                                       │ │
│  │             Node2            Node4                                     │ │
│  │                                                                         │ │
│  │  Key "user:1001" → Hash: 3847 → Node3                                  │ │
│  │                                                                         │ │
│  │  Replication Factor: 3                                                 │ │
│  │  → Node3 (Primary), Node4 (Replica 1), Node5 (Replica 2)              │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                              │
                              │ Write Replication
                              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        [ Distributed Nodes ]                                 │
│                                                                              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                     [ Shared-Nothing Architecture ]                   │   │
│  │                                                                       │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │   Node 1    │  │   Node 2    │  │   Node 3    │  │   Node 4    │ │   │
│  │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │ │   │
│  │  │ │ Memory  │ │  │ │ Memory  │ │  │ │ Memory  │ │  │ │ Memory  │ │ │   │
│  │  │ │ (Cache) │ │  │ │ (Cache) │ │  │ │ (Cache) │ │  │ │ (Cache) │ │ │   │
│  │  │ └────┬────┘ │  │ └────┬────┘ │  │ └────┬────┘ │  │ └────┬────┘ │ │   │
│  │  │      │      │  │      │      │  │      │      │  │      │      │ │   │
│  │  │ ┌────▼────┐ │  │ ┌────▼────┐ │  │ ┌────▼────┐ │  │ ┌────▼────┐ │ │   │
│  │  │ │  Disk   │ │  │ │  Disk   │ │  │ │  Disk   │ │  │ │  Disk   │ │ │   │
│  │  │ │ (SSTable│ │  │ │ (SSTable│ │  │ │ (SSTable│ │  │ │ (SSTable│ │ │   │
│  │  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  │                                                                       │   │
│  │  ※ 각 노드는 독립적인 CPU, 메모리, 디스크 보유                        │   │
│  │  ※ 노드 간 네트워크로만 통신 (공유 저장소 없음)                        │   │
│  │  ※ 노드 추가 시 선형적 성능 향상                                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
                     [ CAP Theorem Visualization ]
================================================================================

                           [ Consistency ]
                                /\
                               /  \
                              / C  \
                             /      \
                            /________\
                           /    CP    \
                          /            \
                         /              \
                        /________________\
                   [ Partition          [ Availability
                     Tolerance ]          ]

    ┌────────────────────────────────────────────────────────────────────────┐
    │  CP (Consistency + Partition Tolerance):                               │
    │  - MongoDB, HBase, Redis Cluster                                      │
    │  - 네트워크 분할 시 가용성 희생, 일관성 유지                           │
    │                                                                         │
    │  AP (Availability + Partition Tolerance):                              │
    │  - Cassandra, DynamoDB, CouchDB                                        │
    │  - 네트워크 분할 시 가용성 유지, 일관성 희생 (최종 일관성)              │
    │                                                                         │
    │  CA (Consistency + Availability) - 이론적, 네트워크 분할 없는 환경:    │
    │  - 단일 노드 RDBMS                                                     │
    └────────────────────────────────────────────────────────────────────────┘

================================================================================
                     [ Data Distribution Strategy ]
================================================================================

    [ Sharding / Partitioning ]

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  Range Sharding:                                                        │
    │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                    │
    │  │ Shard 1      │ │ Shard 2      │ │ Shard 3      │                    │
    │  │ A-M          │ │ N-S          │ │ T-Z          │                    │
    │  └──────────────┘ └──────────────┘ └──────────────┘                    │
    │  장점: 범위 쿼리 효율  단점: 핫스팟 발생 가능                          │
    │                                                                         │
    │  Hash Sharding:                                                         │
    │  key % N = shard_id                                                    │
    │  장점: 균등 분배  단점: 범위 쿼리 비효율                                │
    │                                                                         │
    │  Consistent Hashing:                                                    │
    │  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐                     │
    │  │ 0 │─│ 1 │─│ 2 │─│ 3 │─│ 4 │─│ 5 │─│ 6 │─│ 7 │ → Ring              │
    │  └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘ └───┘                     │
    │  장점: 노드 추가/삭제 시 재배치 최소화                                  │
    └─────────────────────────────────────────────────────────────────────────┘

================================================================================
```

#### 3. 심층 동작 원리: NoSQL 별 핵심 메커니즘

**① Key-Value Store (Redis)**
```
데이터 구조:
- String, List, Set, Hash, Sorted Set, Stream, HyperLogLog, Geo

내부 동작:
1. 클라이언트가 SET user:1001 "Alice" 명령 전송
2. 키 해싱 → 슬롯 결정 (Cluster 모드: 16384 슬롯)
3. 인메모리 해시 테이블에 저장
4. 필요 시 AOF(Append Only File) 또는 RDB로 영속화

성능 특성:
- 읽기/쓰기: O(1) 평균
- 메모리 기반: 마이크로초 단위 응답
- 싱글 스레드: 컨텍스트 스위칭 없음
```

**② Document Store (MongoDB)**
```
데이터 구조:
- BSON (Binary JSON): JSON + Binary + 추가 타입

내부 동작:
1. 클라이언트가 db.users.insertOne({name: "Alice", age: 30}) 전송
2. BSON 인코딩 → 문서 크기 계산
3. 샤드 키(Shard Key) 기반 샤드 결정
4. WiredTiger 스토리지 엔진이 디스크에 기록
5. 인덱스(B+Tree) 업데이트

쓰기 경로:
Application → Mongos → Config Server (메타데이터) → Shard (Primary) → Oplog → Secondaries
```

**③ Column-Family Store (Cassandra)**
```
데이터 구조:
- Keyspace → Column Family → Row Key → Column (Name, Value, Timestamp)

내부 동작 (LSM Tree 기반):
1. 쓰기 요청 → MemTable (메모리)에 기록
2. Commit Log에도 기록 (장애 복구용)
3. MemTable이 임계치 도달 → SSTable로 Flush
4. 다수 SSTable → Compaction으로 병합

읽기 경로:
1. Row Key 해싱 → 노드 결정
2. MemTable → Row Cache → Key Cache → SSTable 순서로 검색
3. Bloom Filter로 불필요 SSTable 스킵

툼스톤(Tombstone):
- 삭제 시 실제 제거 대신 툼스톤 마커 기록
- Compaction 시 실제 제거
```

**④ Graph Store (Neo4j)**
```
데이터 구조:
- Node (정점) - 레이블, 프로퍼티
- Relationship (간선) - 타입, 방향, 프로퍼티
- Property (속성) - 키-값 쌍

내부 동작:
1. 노드 생성: CREATE (p:Person {name: "Alice"})
2. 관계 생성: CREATE (p1)-[:KNOWS {since: 2020}]->(p2)
3. 인덱스-프리 인접성: 각 노드가 직접 연결된 노드에 대한 포인터 보유
4. 순회: 포인터 따라 이동, JOIN 없이 관계 탐색

성능 특성:
- 관계 탐색: O(1) per hop (인덱스 불필요)
- 깊이 우선/너비 우선 탐색 지원
- n-홉 쿼리: RDBMS 대비 수십~수백 배 빠름
```

#### 4. 실무 수준의 NoSQL 코드 예시

```python
# ==============================================================================
# NoSQL 데이터베이스 실무 코드 예시
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Redis (Key-Value Store)
# ------------------------------------------------------------------------------
import redis

# Redis 연결
r = redis.Redis(host='localhost', port=6379, db=0)

# String 조작
r.set('user:1001:name', 'Alice')
r.set('user:1001:age', 30)
r.setex('session:abc123', 3600, 'user:1001')  # TTL 1시간

# Hash 조작
r.hset('user:1001', mapping={'name': 'Alice', 'age': 30, 'email': 'alice@example.com'})
user = r.hgetall('user:1001')  # {b'name': b'Alice', ...}

# List 조작 (메시지 큐)
r.lpush('queue:emails', json.dumps({'to': 'bob@example.com', 'subject': 'Hello'}))
email = r.rpop('queue:emails')

# Sorted Set (리더보드)
r.zadd('leaderboard', {'Alice': 1000, 'Bob': 950, 'Charlie': 1100})
top_10 = r.zrevrange('leaderboard', 0, 9, withscores=True)

# Pub/Sub
pubsub = r.pubsub()
pubsub.subscribe('notifications')
for message in pubsub.listen():
    print(message)

# ------------------------------------------------------------------------------
# 2. MongoDB (Document Store)
# ------------------------------------------------------------------------------
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.objectid import ObjectId

# MongoDB 연결
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']
users = db['users']

# 문서 삽입
user_doc = {
    'name': 'Alice',
    'age': 30,
    'email': 'alice@example.com',
    'address': {
        'city': 'Seoul',
        'zip': '12345'
    },
    'hobbies': ['reading', 'hiking']
}
result = users.insert_one(user_doc)
print(f"Inserted ID: {result.inserted_id}")

# 대량 삽입
users.insert_many([
    {'name': 'Bob', 'age': 25},
    {'name': 'Charlie', 'age': 35}
])

# 조회
alice = users.find_one({'name': 'Alice'})
seoul_users = list(users.find({'address.city': 'Seoul'}))

# 복잡한 쿼리
query = {
    'age': {'$gte': 25, '$lte': 35},
    'hobbies': 'reading'
}
projection = {'name': 1, 'age': 1, '_id': 0}
results = users.find(query, projection).sort('age', DESCENDING).limit(10)

# 업데이트
users.update_one(
    {'name': 'Alice'},
    {'$set': {'age': 31}, '$push': {'hobbies': 'cooking'}}
)

# 집계 파이프라인
pipeline = [
    {'$match': {'age': {'$gte': 25}}},
    {'$group': {'_id': '$address.city', 'avg_age': {'$avg': '$age'}, 'count': {'$sum': 1}}},
    {'$sort': {'count': -1}}
]
for doc in users.aggregate(pipeline):
    print(doc)

# 인덱스 생성
users.create_index([('name', ASCENDING)])
users.create_index([('address.city', ASCENDING), ('age', DESCENDING)])

# ------------------------------------------------------------------------------
# 3. Cassandra (Column-Family Store)
# ------------------------------------------------------------------------------
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

# Cassandra 연결
cluster = Cluster(['localhost'])
session = cluster.connect()

# Keyspace 생성
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS myapp
    WITH REPLICATION = { 'class': 'SimpleStrategy', 'replication_factor': 3 }
""")

session.set_keyspace('myapp')

# 테이블 생성
session.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id UUID PRIMARY KEY,
        name text,
        email text,
        created_at timestamp
    )
""")

# 데이터 삽입
import uuid
user_id = uuid.uuid4()
session.execute(
    "INSERT INTO users (user_id, name, email, created_at) VALUES (?, ?, ?, ?)",
    (user_id, 'Alice', 'alice@example.com', datetime.now())
)

# 배치 쓰기 (Atomic)
batch = """
    BEGIN BATCH
        INSERT INTO users (user_id, name, email) VALUES (?, ?, ?);
        INSERT INTO user_activity (user_id, action, timestamp) VALUES (?, ?, ?);
    APPLY BATCH
"""
session.execute(batch, (uuid.uuid4(), 'Bob', 'bob@example.com',
                        uuid.uuid4(), 'login', datetime.now()))

# 조회
rows = session.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))

# ------------------------------------------------------------------------------
# 4. Neo4j (Graph Database)
# ------------------------------------------------------------------------------
from neo4j import GraphDatabase

class SocialGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_user(self, name, email):
        with self.driver.session() as session:
            session.run(
                "CREATE (u:User {name: $name, email: $email})",
                name=name, email=email
            )

    def create_friendship(self, user1, user2, since):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (u1:User {name: $user1})
                MATCH (u2:User {name: $user2})
                CREATE (u1)-[:FRIENDS_WITH {since: $since}]->(u2)
                """,
                user1=user1, user2=user2, since=since
            )

    def find_friends_of_friends(self, name, depth=2):
        """친구의 친구 찾기 (2홉)"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u:User {name: $name})-[:FRIENDS_WITH*1..2]-(friend)
                WHERE friend.name <> $name
                RETURN DISTINCT friend.name
                """,
                name=name
            )
            return [record['friend.name'] for record in result]

    def shortest_path(self, user1, user2):
        """두 사용자 간 최단 경로"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (u1:User {name: $user1}), (u2:User {name: $user2})
                MATCH path = shortestPath((u1)-[*]-(u2))
                RETURN [node in nodes(path) | node.name] as path
                """,
                user1=user1, user2=user2
            )
            return result.single()['path']

# 사용 예시
graph = SocialGraph('bolt://localhost:7687', 'neo4j', 'password')

graph.create_user('Alice', 'alice@example.com')
graph.create_user('Bob', 'bob@example.com')
graph.create_user('Charlie', 'charlie@example.com')

graph.create_friendship('Alice', 'Bob', 2020)
graph.create_friendship('Bob', 'Charlie', 2021)

fof = graph.find_friends_of_friends('Alice')  # ['Bob', 'Charlie']
path = graph.shortest_path('Alice', 'Charlie')  # ['Alice', 'Bob', 'Charlie']

graph.close()
```

---

### III. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. NoSQL 유형별 상세 비교

| 비교 항목 | Key-Value | Document | Column-Family | Graph |
|:---|:---|:---|:---|:---|
| **유연성** | 낮음 (단순) | 높음 (중첩 구조) | 중간 | 높음 (관계 중심) |
| **쿼리 복잡도** | Key만 | 필터, 집계 | 범위, 슬라이스 | 패턴 매칭 |
| **조인** | 불가 | 제한적 ($lookup) | 불가 | 핵심 기능 |
| **확장성** | 매우 높음 | 높음 | 매우 높음 | 중간 |
| **일관성** | configurable | configurable | 튜너블 | ACID (Neo4j) |
| **대표 사용 사례** | 캐시, 세션 | CMS, 카탈로그 | IoT, 시계열 | SNS, 추천 |

#### 2. CAP 정리 기반 분류

| 제품 | CAP 분류 | 일관성 모델 | 특징 |
|:---|:---|:---|:---|
| **MongoDB** | CP | Strong (기본) | 자동 페일오버, 샤딩 |
| **Cassandra** | AP | Eventual (튜너블) | 높은 쓰기 성능, 멀티 DC |
| **DynamoDB** | AP | Eventual/Strong 선택 | 관리형, 오토 스케일링 |
| **Redis Cluster** | CP | Strong | 인메모리, 복제 |
| **HBase** | CP | Strong | Hadoop 생태계 |
| **CouchDB** | AP | Eventual | MVCC, 오프라인 동기화 |

#### 3. 과목 융합 관점 분석

- **[분산 시스템 융합] CAP 정리**: NoSQL은 Eric Brewer의 CAP 정리에 기반합니다. 네트워크 분할(P)은 피할 수 없으므로, 일관성(C)과 가용성(A) 사이의 선택이 필요합니다.

- **[알고리즘 융합] Consistent Hashing**: 노드 추가/삭제 시 데이터 재배치를 최소화하는 알고리즘. Ketama 해시 함수가 널리 사용됩니다.

- **[자료구조 융합] LSM Tree**: Cassandra, RocksDB 등이 사용하는 쓰기 최적화 구조. MemTable → SSTable → Compaction 과정으로 디스크 기록.

---

### IV. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

- **시나리오 1: RDBMS → NoSQL 마이그레이션**
  - 상황: MySQL에 10억 건 로그 데이터, 조회 성능 저하.
  - 판단: 로그 데이터는 시계열 특성이 있으므로 Cassandra 또는 Elasticsearch로 이관을 검토합니다. 조인이 필요 없고, 쓰기 성능이 중요한 워크로드에 적합합니다.

- **시나리오 2: 캐시 계층 설계**
  - 상황: API 응답 시간 개선 필요.
  - 판단: Redis를 Look-aside 캐시로 활용합니다. TTL 설정으로 데이터 신선도 유지, Cache Stampede 방지를 위한 Mutex Lock 구현 필요.

- **시나리오 3: 폴리글랏 퍼시스턴스**
  - 상황: 단일 DB로 모든 요구사항 충족 어려움.
  - 판단: 서비스별로 최적의 DB 선택. 사용자 데이터(MySQL), 캐시(Redis), 검색(Elasticsearch), 추천(Graph)를 조합하여 구성합니다.

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **데이터 모델 적합성**: 정형 vs 반정형 vs 관계형
- [ ] **일관성 요구사항**: Strong vs Eventual
- [ ] **확장성 계획**: 예상 데이터 증가율
- [ ] **쿼리 패턴**: 접근 패턴 분석
- [ ] **운영 복잡도**: 관리형 vs 자체 구축

#### 3. 안티패턴 (Anti-patterns)

- **NoSQL을 RDBMS처럼 사용**: 조인, 트랜잭션에 의존하면 성능 저하
- **과도한 역정규화**: 업데이트 비용 급증
- **잘못된 샤드 키**: 핫스팟 발생으로 확장성 저하
- **TTL 미설정**: 데이터 무한 증가

---

### V. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 효과 영역 | 내용 | 개선 지표 |
|:---|:---|:---|
| **확장성** | 수평 확장으로 무한 증설 | 비용 50% 절감 |
| **성능** | 특화된 데이터 모델 | 처리량 10~100배 향상 |
| **유연성** | 스키마리스 설계 | 개발 속도 2배 향상 |
| **가용성** | 분산 복제 | 가용성 99.99% |

#### 2. 미래 전망

NoSQL은 **NewSQL, 멀티모델, 클라우드 네이티브**로 진화합니다:

1. **NewSQL**: ACID + Scale-out (CockroachDB, TiDB)
2. **멀티모델**: 단일 엔진에서 다양한 데이터 모델 지원 (ArangoDB)
3. **Serverless**: 사용량 기반 과금, 자동 스케일링 (DynamoDB On-Demand)
4. **AI 통합**: Vector Search, ML Pipeline 내장 (MongoDB Atlas Vector Search)

#### 3. 참고 표준

- **CAP Theorem (Eric Brewer, 2000)**: 분산 시스템 트레이드오프
- **Dynamo Paper (DeCandia et al., 2007)**: 아마존 분산 키-값 저장소
- **Bigtable Paper (Chang et al., 2006)**: 구글 컬럼 패밀리 저장소

---

### 관련 개념 맵 (Knowledge Graph)

- **[CAP 정리](@/studynotes/5_database/2_concurrency/distributed_database_theory.md)**: NoSQL의 이론적 기반.
- **[분산 데이터베이스](@/studynotes/5_database/7_distributed/_index.md)**: NoSQL의 아키텍처 기반.
- **[BASE 속성](@/studynotes/5_database/_keyword_list.md)**: NoSQL의 트랜잭션 모델.
- **[샤딩](@/studynotes/5_database/_keyword_list.md)**: 데이터 분산 기법.
- **[LSM Tree](@/studynotes/5_database/_keyword_list.md)**: 쓰기 최적화 저장 구조.

---

### 어린이를 위한 3줄 비유 설명

1. **다양한 도구**: NoSQL은 요리할 때 만능 냄비 대신 각각 특화된 도구를 쓰는 것과 같아요.
2. **많은 양 처리**: 도구를 여러 개 추가해서 한꺼번에 많은 요리를 만들 수 있어요.
3. **빠르고 유연해요**: 어떤 요리든 자유롭게 만들 수 있어요!
