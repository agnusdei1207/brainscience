+++
weight = 43
title = "43. 043. Re-platform — 클라우드 관리형 서비스 전환"
date = "2026-04-05"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: 043. Re-platform — 클라우드 관리형 서비스 전환는 클라우드 아키텍처에서 자원, 데이터, 운영 방식을 더 탄력적이고 일관되게 만들기 위한 핵심 개념이다.
> **비유**: Re-platform은 이사 후 가구 재배치 — 집(아키텍처)은 그대로인데, 낡은 장롱(자체 DB)을 빌트인 붙박이장(관리형 RDS)으로 교체. 인테리어 공사는 아님.

---

> 📝 모범 답안

## 1. 개요 및 필요성

```
6R 전략 내 Re-platform 위치:

Retire → Retain → Rehost → Re-platform → Repurchase → Re-architect
                   (리프트앤시프트)     ↑           (SaaS 전환)   (클라우드 네이티브)
                                       오늘 주제

Re-platform 특징:
  최소한의 코드 변경
  플랫폼/미들웨어 교체
  클라우드 관리형 서비스 활용
  
  변경 범위:
    ✓ DB 엔진 → 클라우드 관리형 DB (RDS, Cloud SQL)
    ✓ 앱 서버 → 컨테이너 (ECS, EKS, Cloud Run)
    ✓ 캐시 → 관리형 Redis (ElastiCache, Memorystore)
    ✓ 메시지 큐 → 관리형 (SQS, Pub/Sub)
    ✗ 앱 비즈니스 로직 변경 없음
    ✗ 마이크로서비스 분리 없음 (Re-architect 영역)

Rehost vs Re-platform vs Re-architect:

항목            | Rehost    | Re-platform | Re-architect
----------------+-----------+-------------+------------------
코드 변경       | 없음      | 최소        | 전면 재설계
클라우드 이점   | 낮음      | 중간        | 높음
위험도          | 낮음      | 중간        | 높음
비용 절감       | 없거나 증가| 15~30%     | 40~60%
기간            | 빠름      | 수주~수개월 | 수개월~수년
```

> 📢 **섹션 요약 비유**: Re-platform은 이사 후 가구 재배치 — 집(아키텍처)은 그대로인데, 낡은 장롱(자체 DB)을 빌트인 붙박이장(관리형 RDS)으로 교체. 인테리어 공사는 아님.

---

## 2. 구성요소

```
Re-platform 주요 패턴:

1. DB 서버 → 관리형 DB 서비스:
   온프레미스 MySQL → AWS RDS for MySQL
   온프레미스 PostgreSQL → Amazon RDS for PostgreSQL
   Oracle → AWS Aurora PostgreSQL (Oracle 탈피)
   
   획득 이점:
     자동 백업 + Point-in-Time Recovery
     멀티 AZ 고가용성 자동 구성
     보안 패치 자동 적용
     성능 인사이트 (DBA 작업 80% 감소)

2. 앱 서버 → 컨테이너 서비스:
   VM(Apache Tomcat) → AWS ECS/EKS
   
   코드 변경: Dockerfile 작성만 필요
   획득 이점:
     오토스케일링
     블루/그린 배포
     컨테이너 오케스트레이션

3. 자체 Elasticsearch → OpenSearch Service:
   운영 부담 제거
   자동 확장, 백업

4. Nginx + 자체 SSL → ALB (Application Load Balancer):
   SSL 인증서 자동 갱신 (ACM)
   WAF 통합

5. 자체 Kafka → MSK (Managed Streaming for Kafka):
   Kafka 운영 복잡성 제거
   Auto Scaling, 모니터링 통합

Re-platform 시 주의:
  RDS 파라미터 그룹 최적화 필요
  연결 풀링 설정 (RDS Proxy 활용)
  마이그레이션 다운타임 계획 (AWS DMS 활용)
```

> 📢 **섹션 요약 비유**: Re-platform 패턴은 가전제품 업그레이드 — 냉장고(DB)를 자체 수리에서 삼성 서비스센터 AS 계약으로 바꾸는 것. 냉장고 안의 음식(데이터)은 그대로, 관리만 전문가에게.

---

## 3. 구조 및 원리

**핵심 조건**: 자원 추상화, 격리 수준, 자동 프로비저닝, 보안 경계, 비용 통제가 함께 설계되어야 안정적인 서비스 가치가 나온다.

동작 순서:
1. 요구사항과 책임 경계를 먼저 정의한다.
2. 추상화 계층에서 컴퓨팅·스토리지·네트워크 자원을 논리적으로 분리하고 격리 수준을 결정한다.
3. 제어 평면이 정책에 맞는 자원을 프로비저닝하고 서비스 모델에 따라 사용자에게 노출한다.
4. 운영 중에는 확장, 가용성, 백업, 보안 정책을 지속적으로 적용해 상태를 안정화한다.
5. 마지막으로 비용·성능·벤더 종속성을 함께 평가해 구조를 최적화한다.

```
온프레미스 DB → RDS 마이그레이션:

전략 선택:
  1. 기존 방식 + RDS로 이전
     mysqldump → S3 → RDS 복원
     다운타임: 데이터 크기에 따라 수 시간
  
  2. AWS DMS (Database Migration Service):
     지속적 복제 (Change Data Capture)
     다운타임 최소화 (수분 컷오버)
     이기종 DB 마이그레이션 지원 (Oracle → Aurora)

DMS 마이그레이션 단계:
  1. 소스 DB 연결 설정
  2. 타겟 RDS 생성 및 연결 설정
  3. 초기 전체 로드 (Full Load)
  4. 지속적 CDC (Change Data Capture) 복제
  5. 지연 최소화 확인 (수 초 이내)
  6. 컷오버 (애플리케이션 연결 변경)
  7. DMS 복제 태스크 중지

RDS 최적화:
  인스턴스 유형:
    범용: db.t3/m6g (소규모)
    메모리 최적화: db.r6g (DB 서버)
    
  스토리지:
    gp3 (기본): 범용 SSD
    io2: 고 IOPS (OLTP, 금융)
    
  읽기 복제본:
    읽기 쿼리를 Read Replica로 분산
    → Primary 부하 감소 50~80%

비용 비교:
  온프레미스: EC2(DB) = $500/월 + DBA 인건비 $5,000/월
  RDS: $800/월 (관리형) + DBA 부분 감소
  실질: 인건비 절감 시 총비용 40% 감소
```

> 📢 **섹션 요약 비유**: DMS 마이그레이션은 물 흐르게 하면서 파이프 교체 — 물 공급 끊지 않고(서비스 지속), 새 파이프(RDS)로 조금씩 물을 유도해서 최종 전환.

---

## 4. 비교 및 연결

```
VM 앱 → EKS/ECS 컨테이너화:

ECS vs EKS 선택:

  ECS (Elastic Container Service):
    AWS 전용 오케스트레이터
    설정 간단, AWS 서비스 통합 우수
    소규모 / AWS 전용 팀 적합
    
  EKS (Elastic Kubernetes Service):
    Kubernetes 표준 API
    이식성 높음 (멀티 클라우드)
    Kubernetes 경험 팀 적합

Re-platform 컨테이너화 단계:

  1. Dockerfile 작성:
     FROM adoptopenjdk:11-jre-hotspot
     COPY target/app.jar /app/app.jar
     ENTRYPOINT ["java", "-jar", "/app/app.jar"]
     
  2. ECR(Elastic Container Registry)에 이미지 푸시
  
  3. ECS Task Definition 정의:
     CPU: 1vCPU, Memory: 2GB
     환경변수: DB_URL, API_KEY (Secrets Manager 연동)
     
  4. ECS Service 생성:
     Desired Count: 3 (최소 인스턴스)
     Auto Scaling: CPU 70% 이상 → 스케일 아웃
     
  5. ALB (Application Load Balancer) 연동
  
  6. CI/CD 파이프라인 연결 (CodePipeline/GitHub Actions)

Fargate 활용:
  EC2 서버 관리 없이 컨테이너 실행
  = Serverless Container
  추가 Re-platform: EC2 기반 ECS → Fargate 이전
  서버 패치, 용량 관리 부담 제거
```

> 📢 **섹션 요약 비유**: ECS/EKS 컨테이너화는 배달 표준 박스 포장 — 어느 차(서버)에도 실을 수 있는 표준 박스(컨테이너)에 물건(앱)을 담으면, 배달 차(서버)만 바꿔도 됨.

---

## 5. 실무 적용 및 판단

```
이커머스 플랫폼 Re-platform 사례:

현황 (Rehost 완료 후):
  EC2: 온프레미스 VM → AWS EC2 이전 완료 (Rehost)
  RDS: 자체 MySQL → 자체 운영 MySQL on EC2 (아직 비최적)
  문제: DB 패치/백업 수동, 고가용성 없음

Re-platform 목표:
  MySQL on EC2 → RDS for MySQL (Multi-AZ)
  Apache Tomcat on EC2 → ECS Fargate
  Nginx → ALB + WAF
  Redis on EC2 → ElastiCache

단계별 실행:

  Week 1-2: RDS 마이그레이션
    DMS 설정 → 지속 복제 → 피크 시간 외 컷오버
    다운타임: 15분
    
  Week 3-4: Redis → ElastiCache
    설정 변경: redis://old-host → cluster-endpoint
    코드 변경: 없음 (Redis 클라이언트 호환)
    
  Week 5-8: Tomcat → ECS Fargate
    Dockerfile 작성 → 테스트 → 스테이징 → 운영
    ALB 생성 → ECS Service 연결
    
  Week 9-10: WAF 적용
    OWASP Top 10 규칙 활성화
    
  Week 11-12: 모니터링 최적화
    RDS Performance Insights, CloudWatch 대시보드

결과:
  가용성: 99.5% → 99.95% (멀티 AZ RDS)
  DB 관리 시간: DBA 40시간/월 → 5시간/월
  인프라 비용: $8,000/월 → $5,500/월 (-31%)
  스케일링: 수동 → 오토스케일링 (트래픽 5배 급증 자동 대응)
```

> 📢 **섹션 요약 비유**: Re-platform은 집 수리 공정표 — 전기(DB), 수도(캐시), 방화(WAF) 공사를 순서대로 하나씩 진행. 동시에 다 하면 집에서 못 살아요.

---

## 6. 기대효과 및 결론

043. Re-platform — 클라우드 관리형 서비스 전환를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 043. Re-platform — 클라우드 관리형 서비스 전환의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```
[클라우드 도입 초기 (2010~)]
Rehost(리프트앤시프트) 중심
빠른 데이터센터 이전
      |
      v
[관리형 서비스 확대 (2013~)]
RDS, ElastiCache, SQS 성숙
Re-platform 경제성 확보
      |
      v
[컨테이너 혁명 (2014~)]
Docker, Kubernetes 등장
ECS/EKS Re-platform 표준화
      |
      v
[서버리스 Re-platform (2017~)]
Fargate, Lambda
서버 관리 완전 제거
      |
      v
[현재: AI/ML 관리형 서비스]
SageMaker, Vertex AI
AI 인프라 Re-platform
FinOps + 지속적 최적화
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 가상화 | 물리 자원을 논리 자원으로 분리하는 기반 개념 |
| 하이퍼바이저 | 격리와 자원 스케줄링을 수행하는 핵심 계층 |
| 오토스케일링 | 수요 변화에 따라 자원 수를 자동으로 조절 |
| VPC | 클라우드 내 네트워크 격리와 보안 경계 제공 |
| FinOps | 비용 가시성과 최적화를 통해 클라우드 효율을 관리 |

---
