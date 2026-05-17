+++
weight = 8
title = "08. UML 다이어그램"
date = "2026-05-17"
[extra]
categories = "gisulsa-design"
+++

# UML 다이어그램 (구조/행위 13종)

> 별점: ★★★★★ | 매회 기본 필출

---

## 답안.

### Ⅰ. 개요

   Actor ───→ (상품 주문) ──include──→ (재고 확인)
                          ──extend───→ (쿠폰 적용)
Client      WebServer    Database

### Ⅱ. 핵심 구성요소

```
[유스케이스 다이어그램]
   Actor ───→ (로그인)
   Actor ───→ (상품 주문) ──include──→ (재고 확인)
                          ──extend───→ (쿠폰 적용)

[시퀀스 다이어그램]
Client      WebServer    Database
  │─request──→│              │
  │           │──query──────→│
  │           │←─result──────│
  │←response──│              │

[클래스 관계]
연관(Association): 일반 관계
집합(Aggregation): 부분-전체 (part-of, 독립 존재 가능)
합성(Composition): 강한 전체-부분 (독립 불가)
상속(Inheritance): Is-A
의존(Dependency): 사용 관계
실현(Realization): 인터페이스 구현
```


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
