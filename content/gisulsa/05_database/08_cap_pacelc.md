+++
weight = 8
title = "08. CAP 정리 & PACELC"
date = "2026-05-17"
[extra]
categories = "gisulsa-database"
+++

# CAP 정리 & PACELC 이론

> 별점: ★★★★★ | ★134회 기출

---

## 답안.

### Ⅰ. 개요

분산 시스템은 **동시에 3가지를 모두 보장할 수 없다**.
CA 시스템: 단일 서버 RDBMS (분산 환경 불가)
CP 시스템: HBase, Zookeeper, MongoDB (일관성 우선, 분할 시 가용성 포기)

### Ⅱ. 핵심 구성요소

```
[분산 DB 선택]
CA 시스템: 단일 서버 RDBMS (분산 환경 불가)
CP 시스템: HBase, Zookeeper, MongoDB (일관성 우선, 분할 시 가용성 포기)
AP 시스템: Cassandra, DynamoDB, CouchDB (가용성 우선, 최종 일관성)

실제: P는 필수 → CP vs AP 선택이 핵심
```
```
[PACELC 모델]
P가 있을 때 (Partition): A(가용성) vs C(일관성)
P가 없을 때 (Else):      L(지연) vs C(일관성)

예시:
- MySQL (PA/EL): 분산 시 가용성, 정상 시 지연 낮음
- DynamoDB (PA/EL): 가용성 + 낮은 지연 우선
- HBase (PC/EC): 일관성 + 일관성 (항상 강한 일관성)
- CockroachDB (PC/EC): NewSQL, 강한 일관성
```
```
AP 시스템의 일관성 보장 방식:
- 모든 업데이트는 결국 모든 노드에 전파됨
- 읽기 시 일시적 불일치 허용
- 벡터 클럭 / 버전 벡터로 충돌 해결
```


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
