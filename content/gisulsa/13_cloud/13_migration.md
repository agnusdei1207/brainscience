+++
weight = 13
title = "13. 클라우드 마이그레이션 실무"
date = "2026-05-17"
[extra]
categories = "gisulsa-cloud"
+++

# 클라우드 마이그레이션 실무 & Well-Architected

> 별점: ★★★★★ | ★135회 기출

---

## 답안.

### Ⅰ. 개요

1. 운영 우수성 (Operational Excellence):
   운영 자동화, 소규모 반복 변경, 실패에서 학습
   공유 책임, 최소 권한, 추적 가능성

### Ⅱ. 핵심 구성요소

```
[6대 원칙]
1. 운영 우수성 (Operational Excellence):
   운영 자동화, 소규모 반복 변경, 실패에서 학습

2. 보안 (Security):
   공유 책임, 최소 권한, 추적 가능성

3. 신뢰성 (Reliability):
   자동 복구, 수평 확장, 비상 사태 테스트

4. 성능 효율성 (Performance Efficiency):
   최신 기술, 서버리스, 다중 지역

5. 비용 최적화 (Cost Optimization):
   FinOps, Right-Sizing, 예약 인스턴스

6. 지속가능성 (Sustainability):
   탄소 최소화, 효율적 자원 사용
```
```
[AWS 마이그레이션 서비스]
Migration Hub: 마이그레이션 중앙 추적
Application Discovery Service: 온프레미스 인벤토리
DMS (Database Migration Service): DB 이전
SMS (Server Migration Service): VM 이전
Snowball: 대용량 데이터 물리 이전

[마이그레이션 체크리스트]
① 발견: 현행 인벤토리, 의존성 파악


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
