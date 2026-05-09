+++
weight = 5
title = "5. 데이터베이스 (Database)"
[extra]
categories = "gisulsa-database"
+++
# 05. 데이터베이스 (Database)

> **섹션 목표**: 정규화, 트랜잭션, 성능 최적화, 분산 저장을 연결해 데이터 일관성과 처리 성능을 동시에 설명하는 훈련이다.

## 학습 전략

- **30초 훈련**: 정의 1문장, 비교축 1개, 적용사례 1개를 말로 바로 꺼내는 연습을 한다.
- **5분 훈련**: 개요-구성요소-비교-사례의 4단 구조로 압축 답안을 손으로 써본다.
- **25분 훈련**: 비교표를 먼저 그린 뒤, 장단점과 실무 판단을 연결하는 기술사형 서술을 완성한다.

## 과목 공략 포인트

- DB 답안은 이론 정의만 쓰지 말고 정합성, 동시성, 성능을 동시에 다뤄야 완성도가 올라간다.
- 인덱스와 트랜잭션은 별개 주제가 아니라 읽기/쓰기 트레이드오프 관점에서 함께 기술하면 좋다.
- 실무 사례는 OLTP, 분석계, 분산계로 나누어 설명하면 선택 근거가 선명해진다.

## 키워드 마스터 리스트

| 번호 | 파일 | 키워드 클러스터 | 훈련 포인트 |
|------|------|----------------|-------------|
| 01 | [관계형·함수종속·정규화](/gisulsa/05_database/01_relational_normalization/) | 관계형 모델 (Relational Model), 함수 종속 (Functional Dependency), 정규화 (Normalization) | 정규형 이름보다 왜 분해하는지를 사례로 말하는 연습 |
| 02 | [트랜잭션·ACID·격리수준](/gisulsa/05_database/02_transaction_acid/) | 트랜잭션 (Transaction), ACID, 격리 수준 (Isolation Level) | 이상 현상 이름과 격리 수준을 짝지어 말하는 연습 |
| 03 | [인덱스·옵티마이저·튜닝](/gisulsa/05_database/03_index_optimization/) | 인덱스 (Index), 옵티마이저 (Optimizer), 실행 계획 (Execution Plan) | 실행 계획에서 Full Scan, Index Scan, Join 방식을 읽는 연습 |
| 04 | [NoSQL·NewSQL](/gisulsa/05_database/04_nosql_newsql/) | NoSQL, NewSQL, 스키마 유연성 (Schema Flexibility) | 확장성, 일관성, 질의 편의성 3축으로 비교하는 연습 |
| 05 | [분산DB·CAP·샤딩·복제](/gisulsa/05_database/05_distributed_db/) | 분산 데이터베이스 (Distributed Database), CAP 정리 (CAP Theorem), 샤딩 (Sharding), 복제 (Replication) | CAP 세 축과 샤딩·복제 역할을 연결해서 말하는 연습 |

## 실전 사용법

1. 가장 자주 출제되는 파일부터 3일 주기로 회독한다.
2. 비교표는 소리 내어 암기하고, 목차 템플릿은 빈 종이에 재현한다.
3. 실무 사례는 자신이 경험한 프로젝트로 치환해 1분 면접 답변까지 연결한다.
