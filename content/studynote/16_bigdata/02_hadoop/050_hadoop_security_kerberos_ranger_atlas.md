+++
weight = 50
title = "28. Hadoop 보안 — Kerberos, Ranger, Atlas"
date = "2026-04-29"
[extra]
categories = "studynote-bigdata"
+++

## 0. 핵심 인사이트

> **핵심**: Hadoop 보안은 3개 레이어로 구성된다. Kerberos(인증 — 누구인가?), Apache Ranger(권한 부여 — 무엇을 할 수 있는가?), Apache Atlas(데이터 거버넌스 — 어떤 데이터인가·어떻게 이동하는가?)가 완전한 엔터프라이즈 보안 스택을 형성한다.
> **비유**: 대형 물류창고에 재고를 나눠 보관하고 작업 지시서를 현장 직원에게 보내는 체계와 같다.

📝 모범 답안

## 1. 개요 및 필요성

```text
┌──────────────────────────────────────────────────────────┐
│           Hadoop 보안 3개 레이어                          │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  레이어 1: 인증 (Authentication)                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Kerberos KDC (Key Distribution Center)          │   │
│  │  → TGT 티켓 발급 → 서비스 티켓으로 HDFS/YARN 접근│   │
│  └──────────────────────────────────────────────────┘   │
│                    ↓                                      │
│  레이어 2: 권한 부여 (Authorization)                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Apache Ranger — 정책 기반 세밀한 접근 제어       │   │
│  │  (DB·테이블·컬럼·행 레벨 정책)                   │   │
│  └──────────────────────────────────────────────────┘   │
│                    ↓                                      │
│  레이어 3: 데이터 거버넌스 (Governance)                    │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Apache Atlas — 메타데이터·계보·분류·태그         │   │
│  │  (개인정보 컬럼 자동 태그, 데이터 흐름 추적)      │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

### Kerberos 인증 흐름

```text
사용자     KDC(AS)           KDC(TGS)        서비스
  │         │                  │               │
  │ kinit   │                  │               │
  │────────→│ TGT 발급         │               │
  │←────────│                  │               │
  │         │ TGT + 서비스 요청 │               │
  │────────────────────────────→ 서비스 티켓 발급│
  │←──────────────────────────────────────────│
  │                                서비스 티켓으로 HDFS 접근│
  │──────────────────────────────────────────→│
```

### Apache Ranger 세밀한 접근 제어

```text
정책 예시 (Hive 테이블):
  - 데이터 분석팀: sales_db.orders 테이블 SELECT
  - 개인정보팀: customer_db.users.phone 컬럼 마스킹 처리
  - 감사팀: 모든 쿼리 감사 로그 활성화
  - DBA: DDL 권한

행 레벨 필터:
  - 지역 관리자: WHERE region = '${user.region}' 자동 적용
```

---

## 3. 구조 및 원리

**핵심 조건**: 데이터 배치 위치, 메타데이터 관리, 병렬 실행, 장애 복구가 함께 맞물려야 한다.

동작 순서:
| 비교 | 온프레미스 Hadoop | 클라우드 레이크하우스 |
|:---|:---|:---|
| 인증 | Kerberos | IAM (AWS/Azure/GCP) |
| 권한 부여 | Ranger | LakeFormation / Unity Catalog |
| 거버넌스 | Atlas | AWS Glue Catalog / Purview |

---

## 4. 비교 및 연결

### Apache Atlas 데이터 계보 (Data Lineage)

```text
데이터 소스 → ETL 변환 → DW 테이블 → 분석 보고서

Atlas 자동 추적:
  orders.csv → (Spark ETL) → sales_fact → (HiveQL) → monthly_report

규제 준수 활용:
  "이 개인정보 컬럼이 어느 다운스트림 테이블에 흘렀는가?"
  → GDPR 데이터 파악, 개인정보 삭제 영향 범위 분석
```

### 실무 배포 구성
```text
HDP (Hortonworks Data Platform) / CDP (Cloudera Data Platform):
  Kerberos + Ranger + Atlas + Knox(게이트웨이) 번들 제공

Knox Gateway:
  → 외부에서 Hadoop 클러스터 접근 시 단일 진입점 (API Gateway)
  → TLS 종단, SSO 통합
```

---

## 5. 실무 적용 및 판단

| 기대효과 | 내용 |
|:---|:---|
| **규제 준수** | GDPR·개인정보보호법·금융 규제 충족 |
| **세밀한 접근 제어** | 컬럼·행 레벨 정책으로 최소 권한 |
| **데이터 신뢰성** | 계보 추적으로 데이터 품질·영향 파악 |

현대 데이터 레이크하우스에서 Hadoop Kerberos는 클라우드 IAM으로, Ranger는 Unity Catalog/LakeFormation으로, Atlas는 Microsoft Purview/OpenMetadata로 대체되는 추세다. 온프레미스 Hadoop 클러스터 유지 조직에서는 Kerberos+Ranger+Atlas 스택이 여전히 표준 보안 아키텍처다.

---

## 6. 기대효과 및 결론

Hadoop 보안 — Kerberos, Ranger, Atlas은(는) 해당 영역의 성능, 확장성, 운영 안정성, 거버넌스 수준을 직접 좌우하는 핵심 요소다. 따라서 도입 여부는 기능 비교를 넘어 데이터 특성, 팀 역량, 비용 구조, 규제 요구를 함께 보는 아키텍처 판단이어야 한다.

실무에서는 초기 효과보다 지속 운영 가능성과 연계 확장성이 더 중요하다. 하둡 계열 기술의 가치는 개별 컴포넌트보다 저장·자원·처리 계층이 얼마나 안정적으로 결합되는가에 달려 있다.

---

## 7. 발전 흐름도

```text
[Simple Security Mode — 인증 없는 초기 Hadoop]
    │
    ▼
[Kerberos 통합 — 네트워크 신원 인증]
    │
    ▼
[Apache Ranger — 정책 기반 세밀한 접근 제어]
    │
    ▼
[Apache Atlas — 데이터 거버넌스·계보 추적]
    │
    ▼
[Unity Catalog/LakeFormation — 클라우드 통합 거버넌스]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **Kerberos** | Hadoop 네트워크 인증 프로토콜 |
| **Apache Ranger** | 정책 기반 세밀한 접근 제어 |
| **Apache Atlas** | 메타데이터·계보·분류·태그 |
| **Knox Gateway** | Hadoop 클러스터 단일 진입점 |
| **Unity Catalog** | 클라우드 레이크하우스 통합 거버넌스 |
