+++
weight = 86
title = "86. Consumer Lag — Kafka 소비 지연 모니터링, Burrow / JMX"
description = "학습률과 경사하강법의 기본 원리, 다양한 확률적 경사하강법 변형, 학습률 스케줄링 기법"
date = "2026-04-05"
[taxonomies]
tags = ["학습률", "LearningRate", "경사하강법", "GradientDescent", "SGD", "Adam", "모멘텀"]
categories = ["studynote-bigdata"]
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Consumer Lag은 소비자 그룹이 최신 오프셋보다 얼마나 뒤처졌는지 보여 주는 값이다.
> 2. **가치**: Burrow와 JMX (Java Management Extensions)를 함께 쓰면 lag 감지와 원인 분석이 쉬워진다.
> 3. **판단 포인트**: 지속적인 lag은 처리 지연, 장애, 재배치(rebalance)를 의심해야 한다.

---

## Ⅰ. 개요 및 필요성
Consumer Lag은 실시간 스트리밍의 건강 상태를 보여 주는 가장 직관적인 신호다. 값이 커진다는 것은 메시지가 쌓이거나, 소비자가 느려졌거나, 파티션 할당이 흔들린다는 뜻이다.

평균 lag보다 중요한 것은 오래 지속되는 lag이며, 이는 SLA (Service Level Agreement) 위반으로 이어질 수 있다.
📢 섹션 요약 비유: 뒤처진 만큼 쌓인다고 보면 쉽다.

---

## Ⅱ. 아키텍처 및 핵심 원리
| 지표 | 의미 | 해석 |
|:---|:---|:---|
| latest offset | 브로커의 최신 위치 | 생산량의 끝 |
| committed offset | 소비자가 확정한 위치 | 처리 완료 기준 |
| lag | latest - committed | 뒤처진 메시지 수 |
| partition lag | 파티션별 lag | 편차와 핫스팟 확인 |

┌───────────┐   messages   ┌──────────────────┐   consume   ┌───────────────┐
│ Producer  │────────────▶│ Kafka partition  │───────────▶│ Consumer group │
└───────────┘             └─────────┬────────┘             └──────┬────────┘
                                    │ end offset                   │ committed offset
                                    └────────────── lag gap ───────┘
📢 섹션 요약 비유: 오프셋 차이가 핵심이다.

---

## Ⅲ. 비교 및 연결
| 비교 항목 | Burrow | JMX (Java Management Extensions) | Broker metrics | App metrics |
|:---|:---|:---|:---|:---|
| 주 역할 | lag 평가/알림 | JVM 내부 상태 노출 | 토픽/파티션 상태 | 처리 로직 상태 |
| 장점 | lag 해석이 직관적 | 세밀한 내부 관찰 | 클러스터 단위 파악 | 비즈니스와 연결 |
| 한계 | 세부 원인 파악은 약함 | 설정이 필요함 | 앱 지연 원인 부족 | lag 자체를 직접 못 봄 |

운영에서는 Burrow로 경보를, JMX로 원인 분석을, broker/app metrics로 보완하는 조합이 좋다.
📢 섹션 요약 비유: Burrow와 JMX는 역할이 다르다.

---

## Ⅳ. 실무 적용 및 기술사 판단
- [ ] lag을 순간값보다 추세로 본다.
- [ ] 특정 파티션만 느린지 확인한다.
- [ ] rebalance 중 lag과 실제 처리 지연을 구분한다.
- [ ] 소비 로직이 idempotent한지 확인한다.
- [ ] alert 기준을 트래픽 규모에 맞춘다.

- ❌ 평균 lag만 보고 문제 없다고 판단하는 것
- ❌ 고정 임계값 하나로 모든 토픽을 관리하는 것
- ❌ 느린 파티션 하나가 전체 SLA를 망칠 수 있음을 무시하는 것
📢 섹션 요약 비유: 평균보다 지속성과 파티션 편차를 본다.

---

## Ⅴ. 기대효과 및 결론
Consumer Lag은 뒤쪽에 쌓인 숙제 더미다. 더미가 줄지 않으면 읽는 속도가 쓰는 속도를 못 따라간다는 뜻이다.
📢 섹션 요약 비유: lag은 실시간 서비스의 체온계다.

---

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Consumer Lag | 소비 지연의 크기를 나타낸다. |
| Burrow | lag을 판정하고 알림을 준다. |
| JMX (Java Management Extensions) | 애플리케이션 내부 상태를 보여 준다. |
| rebalance | 파티션 재분배로 lag이 흔들릴 수 있다. |
| SLA (Service Level Agreement) | lag이 서비스 품질에 영향을 준다. |

### 📈 관련 키워드 및 발전 흐름도

```text
생산 → 소비 → commit offset 갱신 → latest와의 차이 계산 → lag 증가 시 알림/확장
```

### 👶 어린이를 위한 3줄 비유 설명

1. 읽지 않은 편지 개수와 비슷하다.
2. 편지가 쌓이면 읽는 속도가 부족하거나 잠깐 멈췄다는 뜻이다.
3. 편지 수가 줄지 않으면 빨리 손봐야 한다.
