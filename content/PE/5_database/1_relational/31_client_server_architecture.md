+++
title = "클라이언트-서버 DBMS 아키텍처 (2-Tier, 3-Tier)"
date = "2026-03-05"
[extra]
categories = "studynotes-database"
+++

# 클라이언트-서버 DBMS 아키텍처 (2-Tier, 3-Tier)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 클라이언트-서버 DBMS 아키텍처는 데이터베이스 처리 로직을 프레젠테이션 계층(클라이언트), 비즈니스 로직 계층(애플리케이션 서버), 데이터 계층(DB 서버)으로 분리하여 관심사의 분리(Separation of Concerns)를 실현하는 시스템 구조입니다.
> 2. **가치**: 2-Tier는 단순성과 빠른 응답성을, 3-Tier는 확장성, 보안성, 유지보수성을 제공하며, 비즈니스 요구사항에 따라 적절한 아키텍처 선택이 TCO(Total Cost of Ownership) 40% 이상 절감 효과를 창출합니다.
> 3. **융합**: OSI 7계층 모델의 애플리케이션 계층 구조화, 웹 아키텍처의 MVC 패턴, 그리고 현대 마이크로서비스 아키텍처의 근간이 되는 분산 시스템 설계 원칙입니다.

---

### Ⅰ. 개요 (Context & Background)

#### 1. 개념 및 기술적 정의
**클라이언트-서버 DBMS 아키텍처**는 데이터베이스 시스템의 구성 요소를 클라이언트(Client), 서버(Server), 그리고 선택적으로 미들웨어(Middleware) 계층으로 나누어 배치하는 분산 컴퓨팅 아키텍처입니다.

**2-Tier 아키텍처**:
- 클라이언트가 직접 데이터베이스 서버에 연결
- 클라이언트에 프레젠테이션 로직과 비즈니스 로직이 공존
- DB 서버는 데이터 저장 및 SQL 처리만 담당
- "Fat Client, Thin Server" 구조

**3-Tier 아키텍처**:
- 프레젠테이션 계층(클라이언트), 비즈니스 로직 계층(애플리케이션 서버), 데이터 계층(DB 서버)으로 명확히 분리
- 애플리케이션 서버가 클라이언트와 DB 서버 사이에서 중개 역할
- "Thin Client, Fat Server" 구조
- 현대 웹 애플리케이션의 표준 아키텍처

#### 2. 💡 비유를 통한 이해
**2-Tier**는 **'직통 전화'**와 같습니다.
- 고객(클라이언트)이 창구 담당자(DB 서버)에게 직접 전화를 걸어 요청합니다.
- 빠르고 간단하지만, 모든 고객이 창구 담당자에게 직접 연락하므로 담당자가 바쁩니다.
- 고객이 업무 규칙(비즈니스 로직)을 모두 알고 있어야 합니다.

**3-Tier**는 **'콜센터'**와 같습니다.
- 고객(클라이언트)이 콜센터 상담원(애플리케이션 서버)에게 요청합니다.
- 상담원은 고객의 요청을 검증하고, 필요한 경우 내부 부서(DB 서버)에 조회합니다.
- 상담원이 업무 규칙을 모두 처리하므로 고객은 단순한 요청만 하면 됩니다.
- 상담원을 여러 명 둬서 대규모 고객 응대가 가능합니다.

#### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계**: 메인프레임 시대의 터미널-호스트(Terminal-Host) 아키텍처는 중앙 집중식 처리로 인해 확장성에 한계가 있었습니다. PC의 보급과 함께 데스크톱 애플리케이션이 등장했으나, 파일 서버 방식은 네트워크 트래픽 과부하와 데이터 무결성 문제를 야기했습니다.

2. **혁신적 패러다임의 도입**: 1990년대 클라이언트-서버 아키텍처가 도입되면서, 처리 부하를 분산시키고 GUI 기반의 사용자 친화적 인터페이스를 제공할 수 있게 되었습니다. 인터넷의 보급과 함께 3-Tier 웹 아키텍처가 표준으로 자리잡았습니다.

3. **비즈니스적 요구사항**: 현대 기업은 수백만 명의 동시 사용자, 24x7 가용성, 글로벌 서비스를 요구합니다. 3-Tier 아키텍처의 수평적 확장(Scale-out) 능력과 로드 밸런싱 기능은 이러한 요구사항을 충족하는 핵심 기술입니다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 아키텍처 구성 요소 비교 (표)

| 계층 | 2-Tier 구성 | 3-Tier 구성 | 상세 역할 | 비유 |
|:---|:---|:---|:---|:---|
| **프레젠테이션** | 클라이언트 (Fat Client) | 웹 브라우저/모바일 앱 | UI 렌더링, 사용자 입력 처리 | 고객 |
| **비즈니스 로직** | 클라이언트 내 포함 | 애플리케이션 서버 (WAS) | 업무 규칙 처리, 트랜잭션 관리 | 상담원 |
| **데이터** | DB 서버 | DB 서버 | 데이터 저장, SQL 처리, 무결성 보장 | 창고 |
| **통신 프로토콜** | DB 전용 프로토콜 (OCI, TDS) | HTTP/HTTPS + JDBC/ODBC | 계층 간 데이터 교환 | 전화/이메일 |
| **미들웨어** | 없음 | 웹 서버, 로드 밸런서 | 요청 라우팅, 캐싱, 보안 | 교환원 |

#### 2. 2-Tier vs 3-Tier 아키텍처 다이어그램

```text
================================================================================
                    [ 2-Tier Client-Server Architecture ]
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                              [ Client Tier ]                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        Fat Client Application                          │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  [Presentation Layer]                                           │  │  │
│  │  │  - Windows Forms / Java Swing / Delphi VCL                     │  │  │
│  │  │  - UI Event Handling                                            │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  [Business Logic Layer] ⚠️ 클라이언트에 포함                    │  │  │
│  │  │  - Data Validation                                              │  │  │
│  │  │  - Business Rules                                               │  │  │
│  │  │  - Application State Management                                 │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  [Data Access Layer]                                            │  │  │
│  │  │  - JDBC / ODBC / OCI / ADO.NET                                  │  │  │
│  │  │  - SQL Generation                                               │  │  │
│  │  │  - Connection Pool (Client-side)                                │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                    │                           │
                    │  DB Protocol (OCI, TDS)   │
                    │  (Direct DB Connection)   │
                    │                           │
                    ▼                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            [ Database Server ]                               │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         Thin Server                                    │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │  │
│  │  │ Query Processor │  │ Storage Engine  │  │ Transaction Manager │   │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘   │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  [Data Files] [Index Files] [Log Files] [Control Files]        │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘

[2-Tier 특징]
✅ 장점: 단순한 구조, 빠른 응답 속도, 적은 네트워크 홉(Hop)
❌ 단점: 보안 취약(DB 직접 접근), 확장성 부족, 클라이언트 배포 복잡


================================================================================
                    [ 3-Tier Client-Server Architecture ]
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                        [ Tier 1: Presentation Layer ]                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        Thin Client                                     │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  [Web Browser] / [Mobile App] / [Desktop Client]               │  │  │
│  │  │                                                                 │  │  │
│  │  │  - HTML/CSS/JavaScript (SPA Framework)                         │  │  │
│  │  │  - iOS/Android Native UI                                       │  │  │
│  │  │  - User Input Validation (Client-side)                         │  │  │
│  │  │  - State Management (Redux, Vuex, etc.)                        │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                    │
                    │  HTTP/HTTPS (REST API, GraphQL)
                    │  WebSocket (Real-time)
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      [ Tier 2: Business Logic Layer ]                        │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    Application Server (WAS)                            │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  [Web Server]                    [Load Balancer]                │  │  │
│  │  │  - Nginx / Apache                - L4/L7 Switch                 │  │  │
│  │  │  - SSL Termination               - Round Robin / Least Conn     │  │  │
│  │  │  - Static Content Serving        - Health Check                 │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  [Application Server Instances]                                  │  │  │
│  │  │  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐         │  │  │
│  │  │  │ Spring Boot   │ │ Node.js       │ │ Django/Flask  │         │  │  │
│  │  │  │ (Java)        │ │ (Express)     │ │ (Python)      │         │  │  │
│  │  │  └───────────────┘ └───────────────┘ └───────────────┘         │  │  │
│  │  │                                                                   │  │  │
│  │  │  [Business Logic Components]                                     │  │  │
│  │  │  - Service Layer (Business Rules)                                │  │  │
│  │  │  - Domain Model (Entity, Value Object)                           │  │  │
│  │  │  - Transaction Management (Spring @Transactional)                │  │  │
│  │  │  - Security (Authentication, Authorization)                      │  │  │
│  │  │  - Caching (Redis, Ehcache)                                      │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  [Data Access Layer]                                             │  │  │
│  │  │  - ORM (Hibernate, JPA, TypeORM, SQLAlchemy)                     │  │  │
│  │  │  - Connection Pool (HikariCP, c3p0)                              │  │  │
│  │  │  - Repository Pattern                                            │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                    │
                    │  JDBC / ODBC (Connection Pool)
                    │  Database Protocol
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         [ Tier 3: Data Layer ]                               │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        Database Server(s)                              │  │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │  │
│  │  │ Primary DB      │  │ Read Replica    │  │ Cache Layer         │   │  │
│  │  │ (Write)         │  │ (Read)          │  │ (Redis, Memcached)  │   │  │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────┘   │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  [Storage: SSD/NVMe] [Backup: S3/NFS] [Archive: Glacier]       │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘

[3-Tier 특징]
✅ 장점: 수평 확장성(Scale-out), 보안성(간접 접근), 유지보수성, 로드 밸런싱
❌ 단점: 복잡한 구조, 네트워크 지연(Latency), 높은 초기 구축 비용
================================================================================
```

#### 3. 심층 동작 원리: 3-Tier 요청 처리 흐름

1. **클라이언트 요청**: 사용자가 브라우저에서 "주문 내역 조회" 버튼을 클릭합니다.
   ```
   GET /api/orders?userId=123 HTTP/1.1
   Host: api.example.com
   Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
   ```

2. **로드 밸런서 라우팅**: L7 로드 밸런서가 요청을 받아, 헬스 체크가 완료된 애플리케이션 서버 중 하나로 전달합니다. (Round Robin 또는 Least Connection 알고리즘)

3. **웹 서버 처리**: Nginx가 정적 리소스가 아님을 확인하고, 애플리케이션 서버(Tomcat, Node.js)로 프록시 패스합니다.

4. **인증/인가**: Spring Security 또는 Passport.js가 JWT 토큰을 검증하고, 사용자 권한을 확인합니다.

5. **비즈니스 로직 실행**: OrderService가 주문 조회 비즈니스 로직을 실행합니다.
   - 캐시 확인: Redis에서 먼저 조회
   - 캐시 미스 시: DB 조회

6. **데이터베이스 쿼리**: Connection Pool에서 커넥션을 획득하고, SQL을 실행합니다.
   ```sql
   SELECT o.order_id, o.order_date, o.total_amount, oi.product_name
   FROM orders o
   JOIN order_items oi ON o.order_id = oi.order_id
   WHERE o.user_id = 123
   ORDER BY o.order_date DESC;
   ```

7. **결과 반환**: DB 결과를 DTO로 변환하고, JSON으로 직렬화하여 클라이언트에 반환합니다.
   ```json
   {
     "orders": [
       {"orderId": "ORD-001", "orderDate": "2026-03-05", "totalAmount": 150000}
     ]
   }
   ```

#### 4. 실무 수준의 아키텍처 구성 예시

```yaml
# ========================================
# 3-Tier 아키텍처 구성 예시 (Kubernetes)
# ========================================

# Tier 1: Ingress (Presentation Layer Entry Point)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
    - hosts: [app.example.com]
      secretName: tls-secret
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend-service
                port: { number: 80 }
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: backend-service
                port: { number: 8080 }

---
# Tier 2: Application Server (Business Logic Layer)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-deployment
spec:
  replicas: 3  # 수평 확장
  selector:
    matchLabels: { app: backend }
  template:
    metadata:
      labels: { app: backend }
    spec:
      containers:
        - name: backend
          image: myapp/backend:v1.0.0
          ports:
            - containerPort: 8080
          env:
            - name: SPRING_DATASOURCE_URL
              value: jdbc:postgresql://db-service:5432/mydb
            - name: SPRING_DATASOURCE_USERNAME
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: username
            - name: SPRING_REDIS_HOST
              value: redis-service
          resources:
            requests: { memory: "512Mi", cpu: "500m" }
            limits: { memory: "1Gi", cpu: "1000m" }
          livenessProbe:
            httpGet: { path: /actuator/health, port: 8080 }
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet: { path: /actuator/health/readiness, port: 8080 }
            initialDelaySeconds: 10
            periodSeconds: 5

---
# Tier 3: Database (Data Layer)
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-statefulset
spec:
  serviceName: db-service
  replicas: 1  # Primary (Read Replica는 별도 배포)
  selector:
    matchLabels: { app: postgres }
  template:
    metadata:
      labels: { app: postgres }
    spec:
      containers:
        - name: postgres
          image: postgres:15
          ports:
            - containerPort: 5432
          env:
            - name: POSTGRES_DB
              value: mydb
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: username
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: password
          volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: postgres-storage
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests: { storage: 100Gi }
```

```java
// ========================================
// 3-Tier: Business Logic Layer (Spring Boot)
// ========================================

@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;

    @GetMapping
    public ResponseEntity<ApiResponse<List<OrderDto>>> getOrders(
            @RequestParam Long userId,
            @RequestHeader("Authorization") String authHeader) {

        // 1. 인증/인가는 Filter 레벨에서 처리됨
        // 2. 비즈니스 로직 호출
        List<OrderDto> orders = orderService.getOrdersByUserId(userId);

        return ResponseEntity.ok(ApiResponse.success(orders));
    }
}

@Service
@Transactional
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;
    private final RedisTemplate<String, Object> redisTemplate;
    private final CacheManager cacheManager;

    @Cacheable(value = "orders", key = "#userId")
    @Transactional(readOnly = true)
    public List<OrderDto> getOrdersByUserId(Long userId) {
        // 1. 캐시 확인 (Redis) - @Cacheable이 자동 처리
        // 2. DB 조회 (캐시 미스 시)
        List<Order> orders = orderRepository.findByUserIdWithItems(userId);

        // 3. DTO 변환
        return orders.stream()
                .map(OrderDto::from)
                .collect(Collectors.toList());
    }
}

@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("SELECT DISTINCT o FROM Order o " +
           "LEFT JOIN FETCH o.orderItems oi " +
           "WHERE o.userId = :userId " +
           "ORDER BY o.orderDate DESC")
    List<Order> findByUserIdWithItems(@Param("userId") Long userId);
}

// ========================================
// Application.yml (Data Access Configuration)
// ========================================
/*
spring:
  datasource:
    url: jdbc:postgresql://${DB_HOST:localhost}:5432/mydb
    username: ${DB_USERNAME:appuser}
    password: ${DB_PASSWORD:secret}
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000

  jpa:
    hibernate:
      ddl-auto: validate
    properties:
      hibernate:
        format_sql: true
        default_batch_fetch_size: 100

  cache:
    type: redis
    redis:
      time-to-live: 600000  # 10분

  redis:
    host: ${REDIS_HOST:localhost}
    port: 6379
*/
```

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

#### 1. 2-Tier vs 3-Tier 상세 비교

| 비교 항목 | 2-Tier 아키텍처 | 3-Tier 아키텍처 |
|:---|:---|:---|
| **구조 복잡도** | 단순 (2개 계층) | 복잡 (3개 계층 + 미들웨어) |
| **개발 생산성** | 빠른 초기 개발 | 초기 개발 느리나 장기적 생산성 높음 |
| **확장성** | 수직 확장(Scale-up) 위주 | 수평 확장(Scale-out) 용이 |
| **보안성** | DB 직접 노출 위험 | 애플리케이션 계층에서 접근 통제 |
| **성능** | 네트워크 홉 적어 빠름 | 네트워크 홉 증가하나 캐싱으로 보완 |
| **유지보수성** | 클라이언트 재배포 필요 | 서버 측 변경만으로 가능 |
| **비용** | 초기 비용 낮음, 확장 비용 높음 | 초기 비용 높음, 확장 비용 낮음 |
| **적합 시스템** | 소규모, 높은 보안 요구, 실시간성 | 대규모, 웹/모바일, 글로벌 서비스 |

#### 2. N-Tier 확장 아키텍처 비교

| 아키텍처 | 계층 수 | 특징 | 적합 사례 |
|:---|:---|:---|:---|
| **1-Tier** | 1 | 단일 머신에 모든 것 통합 (메인프레임) | 임베디드, 데스크톱 앱 |
| **2-Tier** | 2 | 클라이언트-DB 직접 연결 | 사내 전용 앱, 높은 보안 요구 |
| **3-Tier** | 3 | 프레젠테이션-비즈니스-데이터 분리 | 일반 웹 애플리케이션 |
| **N-Tier** | 4+ | 마이크로서비스, API 게이트웨이, 서비스 메시 | 대규모 플랫폼, MSA |

#### 3. 과목 융합 관점 분석

- **[네트워크 융합] OSI 7계층과의 매핑**: 3-Tier 아키텍처는 OSI 7계층 모델의 애플리케이션 계층 내부를 세분화한 것입니다. 프레젠테이션 계층 = HTTP/HTML, 비즈니스 계층 = 애플리케이션 프로토콜, 데이터 계층 = SQL 프로토콜.

- **[보안 융합] 다층 방어(Defense in Depth)**: 3-Tier 아키텍처는 각 계층마다 보안 통제를 적용할 수 있습니다. WAF(Web Application Firewall) at 프레젠테이션, 인증/인가 at 비즈니스, TDE/감사 at 데이터 계층.

- **[소프트웨어 공학 융합] MVC 패턴과의 연계**: 3-Tier 아키텍처는 MVC(Model-View-Controller) 패턴의 확장입니다. View = 프레젠테이션 계층, Controller + Service = 비즈니스 계층, Model + Repository = 데이터 계층.

---

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

#### 1. 기술사적 판단 (실무 시나리오)

- **시나리오 1: 중견 제조업 ERP 시스템 구축**
  - 상황: 500명 직원, 사내 네트워크만 사용, 높은 데이터 보안 요구.
  - 판단: 2-Tier 아키텍처 선택. 클라이언트-DB 직접 연결로 네트워크 홉 최소화, 사내망이므로 보안 위험 낮음, 빠른 응답성으로 생산성 향상. 단, 향후 원격 근무 확대 시 3-Tier로 마이그레이션 계획.

- **시나리오 2: 이커머스 플랫폼 글로벌 확장**
  - 상황: 일일 방문자 100만 명, 블랙프라이데이 트래픽 10배 급증, 글로벌 CDN 필요.
  - 판단: 3-Tier 아키텍처 + 마이크로서비스. 로드 밸런서로 트래픽 분산, Auto Scaling으로 급증 트래픽 대응, Redis 캐싱으로 DB 부하 감소, 글로벌 CDN으로 지연 시간 최소화.

- **시나리오 3: 핀테크 앱 성능 병목 해결**
  - 상황: 3-Tier 아키텍처 사용 중, 거래 조회 API 응답 시간 3초로 느림.
  - 판단: 병목 지점 분석 결과, DB 쿼리가 아닌 애플리케이션-DB 간 네트워크 왕복 횟수가 문제. N+1 쿼리 문제 해결(Fetch Join), Redis 캐싱 도입, Connection Pool 튜닝으로 응답 시간 200ms로 개선.

#### 2. 도입 시 고려사항 (체크리스트)

- [ ] **사용자 규모**: 동시 접속자 수, 피크 트래픽 예상치
- [ ] **네트워크 환경**: 사내망 vs 인터넷 노출, 지역 분산 여부
- [ ] **보안 요구사항**: 개인정보 처리, 규제 준수(ISMS, PCI-DSS)
- [ ] **개발/운영 역량**: 팀의 기술 스택, 운영 경험
- [ ] **비용 제약**: 초기 구축 비용 vs 운영 비용, 확장 비용
- [ ] **성능 요구사항**: 응답 시간, 처리량(TPS), 가용성(SLA)

#### 3. 안티패턴 (Anti-patterns)

- **모든 것을 3-Tier로**: 단순한 사내 앱까지 3-Tier로 구축하면 불필요한 복잡도와 비용이 발생합니다. 시스템 규모와 요구사항에 맞는 아키텍처 선택이 중요합니다.

- **비즈니스 로직의 잘못된 배치**: 3-Tier에서 비즈니스 로직을 프레젠테이션 계층(JavaScript)이나 데이터 계층(Stored Procedure)에 구현하면, 계층 분리의 이점을 잃게 됩니다.

- **과도한 추상화**: 각 계층 간의 인터페이스를 지나치게 추상화하면 성능 저하와 디버깅 어려움이 발생합니다. 적절한 수준의 추상화가 필요합니다.

---

### Ⅴ. 기대효과 및 결론 (Future & Standard)

#### 1. 기대효과

| 효과 영역 | 2-Tier | 3-Tier |
|:---|:---|:---|
| **개발 속도** | 초기 개발 30% 빠름 | 장기적 유지보수 50% 효율 |
| **확장성** | 수직 확장 한계 | 수평 확장 10배 이상 가능 |
| **보안** | 기본적 (DB 계정 기반) | 다층 보안 (WAF + 인증 + 암호화) |
| **가용성** | 단일 장애점(SPOF) 위험 | 고가용성(HA) 구축 용이 |

#### 2. 미래 전망

클라이언트-서버 아키텍처는 **서버리스(Serverless)**와 **엣지 컴퓨팅(Edge Computing)**으로 진화하고 있습니다. 3-Tier의 애플리케이션 계층이 FaaS(Function as a Service)로 분해되고, 프레젠테이션 계층이 CDN Edge로 이동하면서, 지연 시간 최소화와 비용 최적화가 동시에 달성되고 있습니다.

또한, **GraphQL**과 **gRPC**의 부상으로 인해 기존 REST API 기반의 통신 방식이 변화하고 있으며, **Service Mesh**(Istio, Linkerd)를 통한 마이크로서비스 간 통신 관리가 표준화되고 있습니다.

#### 3. 참고 표준

- **ISO/IEC 10746**: Open Distributed Processing Reference Model (RM-ODP)
- **TOGAF**: The Open Group Architecture Framework
- **AWS Well-Architected Framework**: 클라우드 아키텍처 모범 사례

---

### 📌 관련 개념 맵 (Knowledge Graph)

- **[트랜잭션 관리](@/studynotes/5_database/2_concurrency/concurrency_control.md)**: 3-Tier의 애플리케이션 계층에서 트랜잭션을 관리하는 방법.
- **[커넥션 풀](@/studynotes/5_database/_index.md)**: 애플리케이션 서버와 DB 서버 간의 연결 관리.
- **[로드 밸런싱](@/studynotes/5_database/_index.md)**: 3-Tier 아키텍처의 확장성을 위한 핵심 기술.
- **[DBMS 언어](@/studynotes/5_database/1_relational/ddl_dml_dcl.md)**: 데이터 계층에서 사용하는 SQL 언어.
- **[분산 데이터베이스](@/studynotes/5_database/2_concurrency/distributed_database_theory.md)**: 3-Tier의 확장형인 분산 DB 아키텍처.

---

### 👶 어린이를 위한 3줄 비유 설명

1. **2-Tier는 직통 전화**: 고객이 창구 담당자에게 직접 전화를 거는 것과 같아요. 빠르지만 담당자가 너무 바빠요.
2. **3-Tier는 콜센터**: 고객이 상담원에게 전화하고, 상담원이 창고 담당자에게 확인하는 거예요. 상담원을 많이 두면 많은 고객을 도울 수 있어요.
3. **계층 분리의 장점**: 고객은 상담원에게만 말하면 되고, 창고 담당자는 물건만 찾으면 돼요. 각자 자기 일만 하면 되니까 효율적이에요!
