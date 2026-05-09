+++
weight = 14
title = "14. 데이터 엔지니어링 (Data Engineering)"
[extra]
categories = "gisulsa-data-engineering"
+++
# 14. 데이터 엔지니어링 (Data Engineering)

> **섹션 목표**: 데이터 수집·저장·처리·거버넌스를 묶어 데이터 플랫폼 설계 답안을 만드는 훈련이다.

## 학습 전략

- **30초 훈련**: 정의 1문장, 비교축 1개, 적용사례 1개를 말로 바로 꺼내는 연습을 한다.
- **5분 훈련**: 개요-구성요소-비교-사례의 4단 구조로 압축 답안을 손으로 써본다.
- **25분 훈련**: 비교표를 먼저 그린 뒤, 장단점과 실무 판단을 연결하는 기술사형 서술을 완성한다.

## 과목 공략 포인트

- 데이터 엔지니어링 문제는 ETL, DW, 스트리밍을 각각 보지 말고 파이프라인 전체로 서술해야 한다.
- 데이터 품질과 거버넌스는 기술이 아니라 운영 체계라는 점을 분명히 해야 한다.
- 실무 사례는 분석계, 실시간 서비스, 데이터 조직 모델로 나누면 좋다.

## 키워드 마스터 리스트

| 번호 | 파일 | 키워드 클러스터 | 훈련 포인트 |
|------|------|----------------|-------------|
| 01 | [데이터 파이프라인·ETL/ELT](/gisulsa/14_data_engineering/01_data_pipeline/) | 데이터 파이프라인 (Data Pipeline), ETL (Extract Transform Load), ELT (Extract Load Transform) | 수집-변환-적재 순서를 사례와 함께 말하는 연습 |
| 02 | [DW·데이터마트·데이터레이크](/gisulsa/14_data_engineering/02_data_warehouse/) | DW (Data Warehouse), 데이터 마트 (Data Mart), 데이터 레이크 (Data Lake) | 정제 수준과 사용자 목적을 기준으로 비교하는 연습 |
| 03 | [스트리밍·Kafka·Flink](/gisulsa/14_data_engineering/03_streaming/) | 스트리밍 처리 (Streaming), Kafka, Flink | 토픽-스트림-상태 저장 흐름을 설명하는 연습 |
| 04 | [데이터 품질·라인리지·카탈로그](/gisulsa/14_data_engineering/04_data_quality/) | 데이터 품질 (Data Quality), 라인리지 (Lineage), 데이터 카탈로그 (Data Catalog) | 신뢰성, 추적성, 탐색성 3축으로 구분해 말하는 연습 |
| 05 | [데이터 메시·데이터 패브릭](/gisulsa/14_data_engineering/05_data_mesh/) | 데이터 메시 (Data Mesh), 데이터 패브릭 (Data Fabric), 데이터 제품 (Data Product) | 조직 관점과 기술 관점을 분리해 설명하는 연습 |

## 실전 사용법

1. 가장 자주 출제되는 파일부터 3일 주기로 회독한다.
2. 비교표는 소리 내어 암기하고, 목차 템플릿은 빈 종이에 재현한다.
3. 실무 사례는 자신이 경험한 프로젝트로 치환해 1분 면접 답변까지 연결한다.
