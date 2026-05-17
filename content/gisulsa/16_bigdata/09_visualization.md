+++
weight = 9
title = "09. 빅데이터 시각화"
date = "2026-05-17"
[extra]
categories = "gisulsa-bigdata"
+++

# 🎯 데이터 시각화 & 비즈니스 인텔리전스

> **별점**: ★★★★☆ | 기본 필수

## 1. 데이터 시각화 원칙

```
[차트 유형 선택 기준]
비교: 막대 차트 (Bar Chart)
추세: 선 차트 (Line Chart), 면적 차트
구성비: 파이 차트, 도넛 차트
분포: 히스토그램, 박스 플롯
상관: 산점도 (Scatter Plot)
공간: 지도 시각화 (Choropleth Map)
관계: 네트워크 그래프

[시각화 설계 원칙 (Edward Tufte)]
Data-Ink Ratio: 잉크 최소화, 데이터 최대화
Chartjunk 제거: 불필요한 장식 제거
Small Multiples: 여러 소형 차트 비교
```

## 2. BI 플랫폼

```
[주요 BI 도구]
Tableau: 드래그&드롭, 강력한 시각화, 비쌈
Power BI: Microsoft 생태계, 저비용
Looker: Google 인수, LookML 기반
Superset: Apache 오픈소스, SQL 기반
Metabase: 쉬운 셀프서비스, 오픈소스

[Self-Service BI 트렌드]
비기술자가 직접 데이터 탐색·분석
데이터 민주화 실현 도구
GenAI 통합: 자연어로 차트 생성 ("매출 추이 보여줘")
```

## 3. 대시보드 설계

```
[대시보드 유형]
운영(Operational): 실시간 KPI 모니터링
  예) 서버 CPU, 주문 수, 오류율
분석(Analytical): 인사이트 발견
  예) 매출 원인 분석, 세그먼트 비교
전략(Strategic): 경영진 의사결정
  예) 시장 점유율, 성장률, ROI

[좋은 대시보드 원칙]
5초 규칙: 5초 안에 핵심 파악 가능
3클릭 규칙: 원하는 정보까지 3번 이내
모바일 반응형: 스마트폰에서도 가독성
```

## 4. 답안 포인트

**3단락**: ① 차트 유형 선택 원칙 & Tufte 원칙 → ② BI 플랫폼 비교(Tableau/Power BI/Looker) → ③ 대시보드 유형 & 좋은 설계 원칙

## 5. 관련 개념

`데이터 기반 경영(12_it 11번)` → BI가 DDDM 실현 도구 | `CDO(12_it)` → BI 전략 담당 | `GenAI(10_ai)` → 자연어 쿼리 기반 BI
