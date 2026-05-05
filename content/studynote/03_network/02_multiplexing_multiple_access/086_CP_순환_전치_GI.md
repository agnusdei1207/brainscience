+++
weight = 86
title = "86. CP (Cyclic Prefix) / GI (Guard Interval) - ISI 방지"
date = "2026-05-05"
[extra]
categories = "studynote-network"
+++

## 0. 핵심 인사이트

> **핵심**: OFDM (Orthogonal Frequency Division Multiplexing)에서 CP (Cyclic Prefix)와 GI (Guard Interval)는 ISI (Inter-Symbol Interference)를 막는 보호 구간이다.
> **비유**: CP (Cyclic Prefix) / GI (Guard Interval) - ISI 방지은(는) 다중화와 다중접속 제어 안에서 데이터와 제어 규칙을 질서 있게 맞춰 주는 교통 체계와 같다.

> 📝 모범 답안

## 1. 개요 및 필요성

무선 채널은 반사와 굴절 때문에 같은 심볼이 여러 경로로 늦게 도착한다. 이때 앞 심볼의 잔상이 다음 심볼을 침범하면 ISI가 생기고, 서브캐리어 직교성이 깨진다.

CP는 이 침범을 흡수하는 쿠션 역할을 한다.
---

## 2. 구성요소

| 요소 | 의미 | 포인트 |
|:---|:---|:---|
| CP | 심볼 끝부분을 앞에 복사 | 다중경로 완충 |
| GI | 보호 구간 | 간섭 흡수 시간 |
| delay spread | 경로 지연 폭 | CP보다 작아야 유리 |
| FFT window | 실제 복조 구간 | CP 뒤에서 시작 |

┌──────────── CP / GI ─────────────┐
│ [tail copy] [  useful symbol  ]  │
│     ↑             ↑             │
│     └── delay spread absorbs ───┘│
└──────────────────────────────────┘
             채널 지연 ↘  ↘  ↘
             FFT 창        [ useful symbol ]
---

## 3. 구조 및 원리

**핵심 조건**: CP (Cyclic Prefix) / GI (Guard Interval) - ISI 방지은(는) 채널 분할, 슬롯 할당, 충돌 제어 조건을 함께 만족할 때 안정적으로 동작한다.

동작 순서:

| 비교 항목 | Normal CP | Extended CP | CP 없음/짧음 |
|:---|:---|:---|:---|
| 길이 | 기본값 | 더 김 | 부족 |
| 적합 환경 | 일반 셀 환경 | 지연 확산이 큰 환경 | 실사용 곤란 |
| 장점 | 속도와 안정성 균형 | 간섭 흡수 여유 | 오버헤드 적음 |
| 단점 | 매우 긴 지연에는 한계 | 효율 저하 | ISI 급증 |

CP 길이는 채널 지연 분포와 시스템 효율 사이의 타협점이다.
---

## 4. 비교 및 연결

- [ ] CP 길이가 최대 delay spread보다 충분히 긴지 확인한다.
- [ ] 동기 오차가 CP 안에 들어오는지 점검한다.
- [ ] 실내/실외, 고속 이동 등 채널 특성에 따라 CP 전략을 구분한다.
- [ ] CP 증가로 인한 전송 효율 저하를 함께 계산한다.

- ❌ 어떤 환경이든 같은 CP를 쓰는 것
- ❌ CP가 짧아도 대충 되겠지 하고 넘기는 것
- ❌ 다중경로를 무시한 채 변조 효율만 보는 것
---

## 5. 실무 적용 및 판단

CP/GI는 비 오는 날 문 앞에 깔아 두는 발판 같다. 물이 집 안으로 들어오기 전에 밖에서 한 번 멈춰 준다.
---

## 6. 기대효과 및 결론

CP (Cyclic Prefix) / GI (Guard Interval) - ISI 방지을 적용하면 채널 분할과 슬롯 할당에 대한 통제력이 높아지고, 운영 일관성과 성능 예측 가능성을 확보할 수 있다. 반면 설정 복잡도, 표준 호환성, 장비 비용, 운영 숙련도라는 전제가 뒤따르므로 무조건적인 도입이 정답은 아니다. 결론적으로 이 주제는 다중화와 다중접속 제어를 이해하는 기준점이며, 최근에는 자동화·가상화·지능형 제어와 결합해 더 세밀한 최적화 방향으로 진화하고 있다.

## 7. 발전 흐름도

```text
송신 심볼 끝부분 복사 → 앞에 CP 삽입 → 채널 지연 흡수 → FFT 복조 → 서브캐리어 직교성 유지
```

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| OFDM (Orthogonal Frequency Division Multiplexing) | 다중반송파 변조의 기본이다. |
| ISI (Inter-Symbol Interference) | 심볼 간 간섭을 막아야 한다. |
| CP (Cyclic Prefix) | 심볼 꼬리를 앞에 복사한다. |
| GI (Guard Interval) | 간섭을 흡수하는 보호 구간이다. |
| FFT (Fast Fourier Transform) | 복조 시 직교성을 활용한다. |
