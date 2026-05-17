+++
weight = 6
title = "06. 데이터 파이프라인 고도화"
date = "2026-05-17"
[extra]
categories = "gisulsa-data-engineering"
+++

# 🎯 데이터 파이프라인 고도화 & CDC

> **별점**: ★★★★★ | 기본 필수

## 1. CDC (Change Data Capture)

```
정의: 데이터베이스 변경 사항을 실시간으로 캡처하여
     다른 시스템에 전달하는 기술

[CDC 방식]
로그 기반 (Log-Based) — 권장:
  DB 트랜잭션 로그 (binlog) 읽기
  MySQL binlog, PostgreSQL WAL
  오버헤드 최소 (프로덕션 부하 없음)

트리거 기반:
  DB 트리거가 변경 감지 → 별도 테이블 기록
  오버헤드 높음, 관리 복잡

폴링 기반:
  주기적으로 updated_at 컬럼 조회
  단순하지만 삭제 감지 불가

[Debezium]
오픈소스 CDC 플랫폼
MySQL/PostgreSQL/MongoDB binlog → Kafka
Kafka Connect 기반 커넥터
```

## 2. 데이터 파이프라인 설계 원칙

```
[멱등성 (Idempotency)]
같은 데이터를 여러 번 처리해도 같은 결과
네트워크 재전송, 재처리 시 중복 방지

[순서 보장]
파티션 내 순서 보장 (Kafka)
글로벌 순서 보장은 어려움 → 이벤트 타임스탬프

[지연 허용 (Late Data)]
이벤트 시간 vs 처리 시간 차이
워터마크로 허용 지연 설정 (Flink)

[데이터 계보 (Lineage)]
원본 데이터 → 변환 → 목적지 추적
Apache Atlas, DataHub로 자동 추적
```

## 3. ELT 현대화 (dbt)

```
[dbt (data build tool)]
SQL로 데이터 변환 코드 작성
  - SELECT 기반 변환 모델
  - 테스트 자동화 (not null, unique)
  - 문서 자동 생성
  - 의존성 그래프 (DAG)

[dbt 워크플로우]
소스 → Raw → Staging → Intermediate → Mart
각 레이어에서 dbt 모델 실행

[dbt Cloud vs Core]
dbt Core: 오픈소스, CLI
dbt Cloud: 관리형 서비스, 스케줄러, IDE
```

## 4. 답안 포인트

**3단락**: ① CDC 정의 & 로그 기반(Debezium+Kafka) → ② 파이프라인 설계 원칙(멱등성/순서/지연허용) → ③ dbt ELT 현대화 & 레이어 구조

## 5. 관련 개념

`Kafka(16_bigdata)` → CDC 전달 플랫폼 | `데이터 메시(05번)` → 도메인 CDC 파이프라인 | `레이크하우스(05_db)` → ELT + dbt 통합
