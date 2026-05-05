+++
weight = 69
title = "69. 직접 수열 확산 스펙트럼 (DSSS, Direct Sequence Spread Spectrum) - PN 시퀀스"
date = "2024-05-24"
[extra]
categories = "studynote-network"
+++

## 0. 핵심 인사이트

> **핵심**: DSSS는 PN 시퀀스로 데이터를 직접 확산해 넓은 대역에 퍼뜨리는 방식이다.
> **비유**: 직접 수열 확산 스펙트럼 (DSSS, Direct Sequence Spread Spectrum) - PN 시퀀스은(는) 데이터통신 기초와 신호 처리 안에서 데이터와 제어 규칙을 질서 있게 맞춰 주는 교통 체계와 같다.

> 📝 모범 답안

## 1. 개요 및 필요성

좁은 대역 신호는 간섭에 취약하다. DSSS는 데이터를 넓게 퍼뜨려 이를 완화한다.

그래서 CDMA 같은 다중 접속 기술의 핵심 개념이 된다.

---

## 2. 구성요소

```text
Data
  ↓ XOR / Multiply
PN Sequence
  ↓
Spread Signal
  ↓
Despread with Same PN
```

| 요소 | 역할 |
| :-- | :-- |
| PN Sequence | 의사난수 확산 코드 |
| Spreading | 대역 확장 |
| Despreading | 원 신호 복원 |

DSSS는 송신 측에서 원 신호를 PN 코드로 확산하고, 수신 측에서 같은 코드로 다시 좁혀 복원한다.

---

## 3. 구조 및 원리

**핵심 조건**: 직접 수열 확산 스펙트럼 (DSSS, Direct Sequence Spread Spectrum) - PN 시퀀스은(는) 대역폭, 지연, 신호 대 잡음비 조건을 함께 만족할 때 안정적으로 동작한다.

동작 순서:

| 방식 | 특징 | 장점 |
| :-- | :-- | :-- |
| DSSS | 코드 기반 확산 | 처리 이득 |
| FHSS | 주파수 점프 | 재밍 회피 |

| 개념 | 의미 |
| :-- | :-- |
| Processing Gain | 잡음 저항성 향상 |
| PN Code | 확산/복원 핵심 |

DSSS는 잡음에 강하고, 동기화가 맞으면 복원이 정확하다.

---

## 4. 비교 및 연결

### 체크리스트

1. PN 시퀀스 동기화가 가능한가?
2. 처리 이득을 설명할 수 있는가?
3. DSSS와 FHSS 차이를 아는가?
4. 다중 사용자 환경에서 활용 가능한가?
5. 잡음/간섭 환경을 고려했는가?

### 안티패턴

- DSSS를 단순 대역 확장으로 보는 설계
- 동기화 문제를 무시하는 설계
- PN 코드의 역할을 이해하지 않는 설계
- 보안성과 성능을 혼동하는 설계

기술사 관점에서는 DSSS를 "PN 코드 기반 확산 통신"으로 설명해야 한다.

---

## 5. 실무 적용 및 판단

DSSS는 간섭에 강하고 다중 사용자 환경에서 유리하다. 그래서 무선 통신의 중요한 기초가 된다.

---

## 6. 기대효과 및 결론

결론적으로 DSSS는 PN 시퀀스로 데이터를 직접 확산하는 방식이다.

## 7. 발전 흐름도

```text
Spread Spectrum
  ↓
DSSS
  ↓
Processing Gain
  ↓
CDMA
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 대역폭 | 직접 수열 확산 스펙트럼 (DSSS, Direct Sequence Spread Spectrum) - PN 시퀀스를 이해할 때 함께 봐야 하는 데이터통신 기초와 신호 처리 핵심 개념 |
| 지연 | 직접 수열 확산 스펙트럼 (DSSS, Direct Sequence Spread Spectrum) - PN 시퀀스를 이해할 때 함께 봐야 하는 데이터통신 기초와 신호 처리 핵심 개념 |
| 신호 대 잡음비 | 직접 수열 확산 스펙트럼 (DSSS, Direct Sequence Spread Spectrum) - PN 시퀀스를 이해할 때 함께 봐야 하는 데이터통신 기초와 신호 처리 핵심 개념 |
| 변조/복조 | 직접 수열 확산 스펙트럼 (DSSS, Direct Sequence Spread Spectrum) - PN 시퀀스를 이해할 때 함께 봐야 하는 데이터통신 기초와 신호 처리 핵심 개념 |
| 라인 코딩 | 직접 수열 확산 스펙트럼 (DSSS, Direct Sequence Spread Spectrum) - PN 시퀀스를 이해할 때 함께 봐야 하는 데이터통신 기초와 신호 처리 핵심 개념 |
