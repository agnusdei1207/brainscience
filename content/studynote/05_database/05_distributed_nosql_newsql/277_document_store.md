+++
weight = 277
title = "문서 저장소 (Document Store)"
date = "2024-03-21"
[extra]
categories = "studynote-database"
+++
## 0. 핵심 인사이트

> | <---[ Metadata Lookup ]---+

> 📝 모범 답안

1. 데이터를 JSON, BSON, XML 등의 계층적 문서 형태로 저장하여 스키마 유연성(Schema-less)과 개발 생산성을 극대화한 NoSQL 데이터베이스입니다.
2. 복잡한 조인(Join) 대신 객체 내 중첩(Embedding)과 참조(Referencing)를 통해 관계를 표현하며, 수평적 확장(Sharding)에 최적화되어 있습니다.
3. 이커머스, 콘텐츠 관리 시스템(CMS), 실시간 로그 분석 등 데이터 구조가 가변적인 현대적 웹 애플리케이션의 메인 저장소로 널리 활용됩니다.

### 1. 개요 및 필요성
- **배경**: 전통적인 RDBMS는 엄격한 스키마 정의로 인해 필드 추가 시 다운타임이 발생하고, 객체-관계 임피던스 불일치(Impedance Mismatch)로 개발 복잡도가 높았습니다.
- **정의**: 데이터를 반정형 문서(Document) 단위로 관리하며, 각 문서는 고유한 ID를 가지고 독립적인 구조를 가질 수 있는 저장 방식입니다.

### 2. 구성요소
- **핵심 원리**: 애플리케이션 레이어의 객체 모델을 변환 없이 그대로 저장 가능하며, 인덱싱을 통해 문서 내부 필드까지 고속 검색을 지원합니다.

```text
[ Document Store Architecture ]

  Client (App)           Query Router (mongos)         Config Server
       |                        |                           |
       +----[ JSON Query ]----                                |
        +-----------------------+-----------------------+
        |                       |                       |
  [ Shard A ]             [ Shard B ]             [ Shard C ]
  +-----------+           +-----------+           +-----------+
  | Document  |           | Document  |           | Document  |
  | {id: 1,   |           | {id: 2,   |           | {id: 3,   |
  |  name: "A"|           |  tags: []}|           |  type: "B"|
  +-----------+           +-----------+           +-----------+
  (Replica Set)           (Replica Set)           (Replica Set)

* Sharding (수평 확장): 데이터를 샤드 키 기준으로 분산 저장
* Replica Set (고가용성): 자동 복제 및 장애 조치 (Failover)
```

### 3. 구조 및 동작 원리
- **RDBMS vs Document Store**

| 비교 항목 | RDBMS (Relational) | 문서 저장소 (Document Store) |
| :--- | :--- | :--- |
| 데이터 모델 | 테이블/행 (Table/Row) | 문서/컬렉션 (Document/Collection) |
| 스키마 | 엄격함 (Fixed Schema) | 유연함 (Schema-less/Dynamic) |
| 관계 표현 | 조인 (Normalization) | 중첩 및 참조 (Denormalization) |
| 확장성 | 수직 확장 (Scale-up) | 수평 확장 (Scale-out/Sharding) |
| 주요 사례 | 금융, ERP, 트랜잭션 | 웹 서비스, CMS, 소셜 미디어 |

### 4. 비교 및 트레이드오프
- **기술사적 판단**: 단순 조회 성능보다는 **개발 기민성(Agility)**과 **데이터 가변성** 대응력이 핵심입니다. 데이터 정합성이 극도로 중요한 금융 핵심 원장보다는 사용자 프로필, 상품 정보, 카탈로그 등 'Read' 비중이 높고 구조가 자주 변하는 영역에 우선 도입을 권고합니다.
- **실무 전략**: 대량의 데이터 처리 시 적절한 **샤드 키(Shard Key)** 설계가 성능의 성패를 좌우합니다. 핫스팟(Hotspot) 방지를 위해 카디널리티(Cardinality)가 높은 필드를 선택해야 합니다.

### 5. 실무 적용 및 최적화 기법
- **미래 전망**: 단순 NoSQL을 넘어 트랜잭션 지원 강화(ACID 준수)를 통해 NewSQL의 영역까지 넘보고 있습니다. 또한 클라우드 네이티브 환경에서 Atlas와 같은 관리형 서비스(DBaaS)로의 전환이 가속화될 것입니다.
- **결론**: 문서 저장소는 현대 소프트웨어 개발의 '표준' 저장소 중 하나로 자리 잡았으며, 폴리글랏 퍼시스턴스 아키텍처의 핵심 요소입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
1. **BSON (Binary JSON)**: MongoDB에서 사용하는 이진 인코딩 직렬화 포맷
2. **Aggregation Framework**: 문서 그룹화 및 분석을 위한 파이프라인 연산
3. **CAP Theorem**: 분산 시스템의 일관성, 가용성, 분단 허용성 사이의 균형

### 👶 어린이를 위한 3줄 비유 설명
1. RDBMS는 칸이 딱 정해진 '약 상자' 같아서 정해진 것만 넣어야 해요.
2. 문서 저장소는 아무거나 담을 수 있는 '커다란 주머니' 같아서 내용물이 달라도 괜찮아요.
3. 그래서 새로운 장난감이 생겨도 주머니에 쏙 넣기만 하면 되니까 아주 편하답니다!
