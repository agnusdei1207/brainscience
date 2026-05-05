+++
weight = 70
title = "70. 주파수 도약 확산 스펙트럼 (FHSS, Frequency Hopping Spread Spectrum)"
date = "2024-05-20"
[extra]
categories = "studynote-network"
+++

## 0. 핵심 인사이트

> **핵심**: FHSS는 주파수를 빠르게 바꾸며 신호를 분산시켜 재밍과 간섭에 강하게 만드는 방식이다.
> **비유**: 주파수 도약 확산 스펙트럼 (FHSS, Frequency Hopping Spread Spectrum)은(는) 데이터통신 기초와 신호 처리 안에서 데이터와 제어 규칙을 질서 있게 맞춰 주는 교통 체계와 같다.

> 📝 모범 답안

## 1. 개요 및 필요성

고정 주파수는 간섭에 약하다. FHSS는 주파수를 계속 바꿔서 공격과 잡음의 영향을 줄인다.

그래서 무선 통신과 블루투스 계열에서 자주 언급된다.

---

## 2. 구성요소

```text
Carrier Frequency
  ↓ hop pattern
Frequency Hop
  ↓
Spread Transmission
```

| 요소 | 의미 |
| :-- | :-- |
| Hop Pattern | 주파수 이동 규칙 |
| Synchronization | 송수신 동기 |
| Anti-jamming | 재밍 회피 |

FHSS는 일정한 규칙에 따라 주파수를 바꾸며 전송한다. 수신기는 같은 패턴을 따라가며 복원한다.

---

## 3. 구조 및 원리

**핵심 조건**: 주파수 도약 확산 스펙트럼 (FHSS, Frequency Hopping Spread Spectrum)은(는) 대역폭, 지연, 신호 대 잡음비 조건을 함께 만족할 때 안정적으로 동작한다.

동작 순서:

| 방식 | 특징 | 장점 |
| :-- | :-- | :-- |
| FHSS | 주파수 점프 | 재밍 회피 |
| DSSS | 코드 확산 | 처리 이득 |

| 개념 | 의미 |
| :-- | :-- |
| Hop Sequence | 이동 순서 |
| Spread Spectrum | 확산 통신 |

FHSS와 DSSS는 둘 다 확산 스펙트럼이지만, 확산하는 방법이 다르다.

---

## 4. 비교 및 연결

### 체크리스트

1. 동기화가 가능한가?
2. 홉 패턴이 관리되는가?
3. 재밍 대응이 필요한가?
4. DSSS와 차이를 설명할 수 있는가?
5. 주파수 자원 정책을 고려하는가?

### 안티패턴

- 홉 패턴 없이 무작정 바꾸는 설계
- 동기화 실패를 무시하는 설계
- DSSS와 혼동하는 설계
- 주파수 규제를 고려하지 않는 설계

기술사 관점에서는 FHSS를 "주파수 이동 기반 확산 통신"으로 설명해야 한다.

---

## 5. 실무 적용 및 판단

FHSS는 재밍과 간섭을 줄이는 데 유리하다. 그래서 무선 신뢰성을 높인다.

---

## 6. 기대효과 및 결론

결론적으로 FHSS는 주파수를 도약하며 전송하는 확산 방식이다.

## 7. 발전 흐름도

```text
Spread Spectrum
  ↓
FHSS
  ↓
Bluetooth
  ↓
Wireless Robustness
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 대역폭 | 주파수 도약 확산 스펙트럼 (FHSS, Frequency Hopping Spread Spectrum)를 이해할 때 함께 봐야 하는 데이터통신 기초와 신호 처리 핵심 개념 |
| 지연 | 주파수 도약 확산 스펙트럼 (FHSS, Frequency Hopping Spread Spectrum)를 이해할 때 함께 봐야 하는 데이터통신 기초와 신호 처리 핵심 개념 |
| 신호 대 잡음비 | 주파수 도약 확산 스펙트럼 (FHSS, Frequency Hopping Spread Spectrum)를 이해할 때 함께 봐야 하는 데이터통신 기초와 신호 처리 핵심 개념 |
| 변조/복조 | 주파수 도약 확산 스펙트럼 (FHSS, Frequency Hopping Spread Spectrum)를 이해할 때 함께 봐야 하는 데이터통신 기초와 신호 처리 핵심 개념 |
| 라인 코딩 | 주파수 도약 확산 스펙트럼 (FHSS, Frequency Hopping Spread Spectrum)를 이해할 때 함께 봐야 하는 데이터통신 기초와 신호 처리 핵심 개념 |
