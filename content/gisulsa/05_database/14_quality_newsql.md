+++
weight = 14
title = "14. 데이터 품질 관리"
date = "2026-05-17"
[extra]
categories = "gisulsa-database"
+++

# 데이터 품질 관리 & NewSQL

> 별점: ★★★★☆ | 기본 필수

---

## 답안.

### Ⅰ. 개요

① 프로파일링: 현황 파악 (NULL, 중복, 분포)
② 규칙 정의: 품질 기준 수립 (사업 규칙)
③ 측정: 지표 자동 측정 (DQ 대시보드)

### Ⅱ. 핵심 구성요소

```
[데이터 품질 관리 사이클]
① 프로파일링: 현황 파악 (NULL, 중복, 분포)
② 규칙 정의: 품질 기준 수립 (사업 규칙)
③ 측정: 지표 자동 측정 (DQ 대시보드)
④ 개선: 원인 분석 → 소스 시스템 수정
⑤ 모니터링: 지속적 품질 감시

도구: AWS Glue DataBrew, Great Expectations,
     Informatica DQ, Talend Data Quality
```
```
정의: ACID 보장 + 수평 확장의 결합
→ RDB의 일관성 + NoSQL의 확장성

특징:
- SQL 인터페이스 유지 (기존 앱 호환)
- 분산 트랜잭션 ACID 보장
- 자동 샤딩 + 복제

대표 제품:
- CockroachDB: PostgreSQL 호환, 자동 분산
- TiDB: MySQL 호환, HTAP (OLTP+OLAP)
- Google Spanner: 글로벌 분산, TrueTime
- YugabyteDB: PostgreSQL 호환, 오픈소스

적합 용도:
- 금융 결제 (전 세계 ACID)
- 글로벌 재고 관리
```


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
