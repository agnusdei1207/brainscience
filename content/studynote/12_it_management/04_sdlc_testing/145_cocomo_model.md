+++
title = "145. COCOMO (Constructive Cost Model) 비용 산정 모델"
weight = 145
date = "2026-03-04"
[extra]
categories = "studynote-it-management"
+++
## 0. 핵심 인사이트

> 30만 라인 (미사일 제어, 실시간 시스템)

> 📝 모범 답안

- 배리 뵘(Barry Boehm)이 제안한 소스 코드 라인 수(LOC) 기반의 소프트웨어 비용 산정 알고리즘임.
- 프로젝트 규모와 난이도에 따라 유기적(Organic), 준분리형(Semi-detached), 내장형(Embedded) 모델로 분류함.
- 수학적 공식을 사용하여 개발에 필요한 인월(Man-Month)과 개발 기간(Duration)을 정량적으로 산출함.

### 1. 개요 및 필요성
초기 소프트웨어 공학에서 프로젝트 비용을 예측하는 것은 매우 어려운 과제였다. 1981년 배리 뵘은 과거의 수많은 프로젝트 데이터를 분석하여 소스 코드 규모(KDSI, 1000 Delivered Source Instructions)를 변수로 하는 **COCOMO(Constructive Cost Model)** 모델을 발표하였다. 이는 SW 비용 산정의 가장 고전적이고 기초적인 모델로, 이후 기능점수(FP)와 보헴 자신의 COCOMO II 모델로 발전하는 계기가 되었다.

### 2. 구성요소
COCOMO는 프로젝트의 성격에 따라 3가지 기본 모델로 구분하며, 각 모델마다 고유의 상수 값을 적용하여 **Effort(PM, Person-Month)**를 산출한다.

```text
[ Project Size (LOC/KDSI) ]
           |
           v
[ Selection of COCOMO Model ]
| 1. Organic (유기적)        | < 5만 라인 (비즈니스 앱)
| 2. Semi-detached (준분리형) | < 30만 라인 (운영체제, 컴파일러)
| 3. Embedded (내장형)       |            |
           v
[ Effort Calculation Formula ]
|  PM = a * (KDSI)^b * EAF   | (Effort Adjustment Factor 반영)
           |
           v
[ Schedule Calculation Formula ]
|  TDEV = c * (PM)^d         | (TDEV: Total Development Time)
```

1. **Organic**: 팀이 소규모이고 요구사항이 엄격하지 않은 업무용 SW 개발. ($a=2.4, b=1.05$)
2. **Semi-detached**: 중간 규모의 복잡도를 가진 시스템 SW 개발. ($a=3.0, b=1.12$)
3. **Embedded**: 하드웨어와 강결합된 초복잡 실시간 시스템 개발. ($a=3.6, b=1.20$)
- **KDSI**: 전달된 소스 코드의 천 라인 단위.
- **EAF**: 인적 특성, 제품 특성 등 15가지 요소를 고려한 노력 보정치.

### 3. 구조 및 동작 원리

| 비교 항목 | COCOMO (Basic) | COCOMO II | 기능 점수 (Function Point) |
| :--- | :--- | :--- | :--- |
| **산정 기준** | LOC (코드 라인 수) | 단계별 모델 (Object, Early, Post) | 논리적 기능 요구사항 |
| **산정 시점** | 구현 중/후 (정확함) | 프로젝트 초기부터 가능 | 프로젝트 기획/설계 초기 |
| **언어 의존성** | 매우 높음 (언어별 LOC 차이) | 낮음 (FP 기반 코드 변환 가능) | 없음 (사용자 관점) |
| **추정 정확도** | 낮음 (초기 예측 어려움) | 높음 (현대적 요인 반영) | 높음 (비즈니스 가치 중심) |

### 4. 비교 및 트레이드오프
- **적용 시점**: 프로젝트 초기 대략적인 예산 범위를 잡을 때나, 과거 유사 프로젝트의 코드 규모 데이터를 보유하고 있을 때 적용한다.
- **기술사적 판단**: COCOMO는 **"규모의 경제"**가 아닌 **"규모의 불경제(Diseconomy of Scale)"**를 수학적으로 증명(지수 b가 1보다 큼)했다는 점에서 큰 의의가 있다. 즉, 프로젝트 규모가 커질수록 투입 노력은 지수 함수적으로 증가하므로, 대형 프로젝트일수록 의사소통 비용과 복잡도를 낮추는 아키텍처 설계가 필수적임을 시사한다.

### 5. 실무 적용 및 최적화 기법
COCOMO는 정량적인 데이터에 기반하여 주관적인 판단을 배제하고 비용을 산출할 수 있게 해주었다. 현재는 코드 자동 생성 및 라이브러리 활용 증가로 순수 LOC 기반 산정은 한계가 있으나, COCOMO II로 진화하여 재사용성 지수 등을 반영하며 여전히 유효한 이론적 토대를 제공하고 있다. 향후 AI 자동 코딩(GitHub Copilot) 시대에는 생성된 코드의 '가치'를 어떻게 보정할지에 대한 새로운 COCOMO 모델링 연구가 필요하다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **KDSI (Kilo Delivered Source Instructions)**: 천 라인 단위 소스 코드 양.
- **Brook's Law**: 지연되는 프로젝트에 인력을 추가하면 더 늦어진다 (COCOMO 지수의 배경).
- **EAF (Effort Adjustment Factor)**: 15가지 노력 조정 요인.

### 👶 어린이를 위한 3줄 비유 설명
- 레고 성을 만드는데 '블록 개수'를 세서 얼마나 걸릴지 맞추는 거예요.
- 쉬운 성은 블록이 적어도 금방 만들지만, 복잡한 성은 블록이 많아질수록 훨씬 더 오래 걸리죠.
- 미리 블록 수를 예상해서 아빠한테 "이 성은 일주일 걸려요!"라고 말해주는 똑똑한 계산기랍니다.
