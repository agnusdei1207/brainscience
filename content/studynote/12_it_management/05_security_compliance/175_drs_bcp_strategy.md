+++
weight = 175
title = "재해 복구 시스템(DRS) 및 업무 연속성 계획(BCP) 전략"
date = "2026-03-04"
[extra]
categories = "studynote-it-management"
+++
## 0. 핵심 인사이트

> [ Detection ] ---> [ Recovery Activation ]

> 📝 모범 답안

- **비즈니스 생존의 안전망:** 대형 재난 상황에서도 핵심 업무가 중단되지 않도록 하는 전략(BCP)과 정보시스템 복구 기술(DRS)의 통합 체계이다.
- **RTO/RPO 지표 기반 설계:** 허용 가능한 중단 시간(RTO)과 데이터 유실 허용 범위(RPO)에 따라 기술적 아키텍처(센터 유형)를 결정한다.
- **거버넌스와 기술의 융합:** 단순 시스템 구축을 넘어 업무 영향 분석(BIA)과 정기적인 모의 훈련을 통해 실효성을 확보해야 한다.

### 1. 개요 및 필요성
- 기후 변화, 테러, 사이버 공격(랜섬웨어) 등 위협이 다변화됨에 따라 단순 백업을 넘어 전사적 차원의 업무 연속성(BCP, ISO 22301) 확보가 기업의 의무로 격상되고 있다.

### 2. 구성요소

```text
[ Disaster Event ] ---                                                  |
+-------------------------------------------------+---------------------+
|      (BCP: Business Continuity Plan)            |  (DRS: Recovery)    |
| - Policy & Organization                         | - Mirror Site (RTO=0)|
| - BIA (Business Impact Analysis)                | - Hot Site (RTO<4h) |
| - Crisis Communication                          | - Warm/Cold Site    |
+-------------------------------------------------+---------------------+
          |                                            |
[ Resumed Operation ] <--- (Failback) --- [ Recovery Site ]

<Bilingual ASCII Diagram: BCP와 DRS의 유기적 연계 / Synergy of BCP & DRS>
```

- **핵심 구성 요소:**
  1. **BIA(업무 영향 분석):** 재난 시 업무 중단에 따른 손실을 정량적으로 분석하여 복구 우선순위 결정
  2. **RTO(Recovery Time Objective):** 서비스가 멈춰 있을 수 있는 최대 시간
  3. **RPO(Recovery Point Objective):** 데이터 유실을 감내할 수 있는 최대 과거 시점

### 3. 구조 및 동작 원리

| 구분 | Mirror Site | Hot Site | Warm Site | Cold Site |
| :--- | :--- | :--- | :--- | :--- |
| **RTO/RPO** | Real-time (0) | Within 4h | Within Days | Within Weeks |
| **데이터 전송** | 실시간 동기화 | 주기적 비동기 | 백업 테이프 이송 | 없음 (장비부터 설치) |
| **비용** | 극히 높음 | 높음 | 중간 | 낮음 |
| **주요 용도** | 금융/공공 핵심 | 주요 서비스 | 일반 사무 | 단순 백업 아카이빙 |

### 4. 비교 및 트레이드오프
- **재해 복구 시나리오:** 네트워크 다중화, 데이터 소산 보관, 원격지 DR 센터 구축 등 다각적 방어망 설계가 필수적이다.
- **기술사적 판단:** 클라우드 환경에서는 리전(Region) 간 가용 영역(AZ) 분산과 IaC(Terraform)를 활용한 '인스턴트 DR' 구성을 통해 전통적 방식보다 저비용 고효율의 BCP 달성이 가능하다.

### 5. 실무 적용 및 최적화 기법
- 향후 DRS는 단순히 '살려내는 것'을 넘어, 사고가 나도 서비스 중단이 없는 '무중단 아키텍처(Resiliency)'로 진화해야 한다. 정기 모의 훈련(카오스 엔지니어링)을 통한 상시 검증이 핵심이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- Risk Management -> Business Continuity -> BCP (ISO 22301) -> BIA -> DRS (RTO, RPO) -> Disaster Recovery Center

### 👶 어린이를 위한 3줄 비유 설명
- **BCP**는 소풍 갈 때 비가 올 경우를 대비해 실내 장소를 미리 빌려두는 "플랜 B"예요.
- **DRS**는 학교 급식소가 불이 나도 옆 학교에서 밥을 바로 가져다주는 "마법의 부엌" 같은 장치랍니다.
- 이 두 가지가 잘 준비되어 있으면 어떤 사고가 나도 우리 친구들이 굶거나 놀이를 멈추지 않을 수 있어요!
