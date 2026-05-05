+++
weight = 818
title = "818. NVGRE (Network Virtualization using Generic Routing Encapsulation) MS 주도 캡슐화 통신 체계"
date = "2026-05-05"
[extra]
categories = "studynote-network"
+++

## 0. 핵심 인사이트

> **핵심**: 앞서 배운 VXLAN(817번)은 시스코와 VMWare라는 네트워크 공룡들이 합심해 만든 기술이었다. 마이크로소프트(MS)는 배가 아팠다. "야! 우리도 Hyper-V(가상화 엔진) 띄우고 애저(Azure) 클라우드 장사해야 하는데, 라이벌들 기술(VXLAN)을 가져다 쓰긴 족팔리잖아? 우리는 기존 인터넷 라우터들이 가장 흔하게 쓰던 사설망 껍데기(GRE 터널)를 개조해서 우리만의 1,600만 개짜리 오버레이 터널을 뚫자!" 그렇게 탄생한 비운의 2인자 기술이 NVGRE다.
> **비유**: NVGRE (Network Virtualization using Generic Routing Encapsulation) MS 주도 캡슐화 통신 체계은(는) 데이터센터·클라우드 네트워크 안에서 데이터와 제어 규칙을 질서 있게 맞춰 주는 교통 체계와 같다.

> 📝 모범 답안

## 1. 개요 및 필요성

- **개념**: 마이크로소프트, 인텔, 브로드컴이 주도하여 제정한 데이터센터 네트워크 가상화(Overlay) 기술입니다.
- VXLAN과 마찬가지로 L2(MAC) 이더넷 패킷을 캡슐화하여 L3(IP) 라우팅 망 위로 쏴 보내는 것은 100% 동일하지만, 택배 박스 포장지(프로토콜)로 UDP가 아니라 **GRE(Generic Routing Encapsulation)**라는 전통적인 터널링 프로토콜 껍데기를 사용한 점이 가장 큰 차이입니다. (MAC-in-GRE 방식)

- VXLAN은 VNI(24비트)를 썼습니다.
- NVGRE 역시 GRE 패킷 헤더의 잉여 공간을 싹싹 긁어모아 24비트짜리 **TNI (Tenant Network Identifier)**라는 꼬리표를 만들었습니다. 덕분에 VXLAN과 똑같이 **1,677만 개의 독립적인 가상 네트워크 조각(Tenant)**을 찍어낼 수 있습니다.

## 2. 구성요소

- **VXLAN (MAC-in-UDP)**: 패킷을 **UDP/IP** 껍데기로 감쌌습니다. UDP는 전 세계 라우터들이 가장 좋아하고 잘 처리(ECMP 해시 분산 등)하는 밥줄 프로토콜입니다.
- **NVGRE (MAC-in-GRE)**: 패킷을 **GRE/IP** 껍데기로 감쌌습니다. (IP 프로토콜 번호 47번).
  - **문제점 폭발**: 기존 물리 스위치(언더레이) 장비들은 UDP나 TCP 패킷이 들어오면 해시 수식을 돌려 여러 차선으로 트래픽을 분산(ECMP 병렬 라우팅, 804번)시키는 게 특기입니다.
  - 그런데 이 GRE 껍데기를 씌운 패킷이 날아오면, 구형 스위치 장비들은 "어? 이거 UDP/TCP도 아니고 포트 번호도 없네? 해시 계산 못하겠는데?"라며 뇌정지가 오고, **여러 차선으로 분산시키지 못한 채 그냥 한 가닥 도로로만 트래픽을 멍청하게 줄 세워서 보내버리는 끔찍한 병목 현상**이 터지고 맙니다.

## 3. 구조 및 원리

**핵심 조건**: NVGRE (Network Virtualization using Generic Routing Encapsulation) MS 주도 캡슐화 통신 체계은(는) 패브릭, 오버레이, 로드밸런싱 조건을 함께 만족할 때 안정적으로 동작한다.

동작 순서:

- VXLAN에 VTEP(입출구 담당 직원)이 있듯이, NVGRE 망에는 가상머신 밑단 하이퍼바이저 쪽에 터널을 포장하고 벗기는 모듈이 돌아갑니다. 마이크로소프트 윈도우 서버 시스템이나 System Center와 미친 듯이 강력하게 결합되어 최적화되어 있었습니다.

## 4. 비교 및 연결

초기 클라우드 가상화 기술의 양대 산맥으로 치열하게 싸웠지만, 앞서 말한 **'구형 라우터 장비에서의 ECMP 트래픽 분산(로드밸런싱)의 치명적 어려움'** 때문에 결국 시스코가 주도한 VXLAN 연합군에게 완벽하게 시장을 내주고 멸망에 가깝게 도태되었습니다. 현재 글로벌 클라우드 표준 캡슐화 포장지는 100% VXLAN으로 통일된 상태입니다.

## 5. 실무 적용 및 판단

**채택 조건**
- 패브릭과 오버레이을 동시에 관리해야 할 때
- 운영 자동화 또는 표준화된 제어가 필요할 때
- 장애 분석 시 원인 구분이 명확해야 할 때

**회피 조건**
- 단순 환경이라 오버헤드가 더 큰 경우
- 장비·프로토콜 호환성이 확보되지 않은 경우
- 측정 지표 없이 관행적으로만 적용하는 경우

**체크리스트**
1. 요구 성능과 허용 지연이 정의되었는가?
2. 오류·혼잡·보안 처리 경계가 명확한가?
3. 표준·벤더 구현 차이를 검증했는가?
4. 운영 관측성 및 장애 대응 절차가 준비되었는가?

## 6. 기대효과 및 결론

NVGRE (Network Virtualization using Generic Routing Encapsulation) MS 주도 캡슐화 통신 체계을 적용하면 패브릭과 오버레이에 대한 통제력이 높아지고, 운영 일관성과 성능 예측 가능성을 확보할 수 있다. 반면 설정 복잡도, 표준 호환성, 장비 비용, 운영 숙련도라는 전제가 뒤따르므로 무조건적인 도입이 정답은 아니다. 결론적으로 이 주제는 데이터센터·클라우드 네트워크를 이해하는 기준점이며, 최근에는 자동화·가상화·지능형 제어와 결합해 더 세밀한 최적화 방향으로 진화하고 있다.

## 7. 발전 흐름도

```text
기초 데이터센터·클라우드 네트워크 이해
    ↓
NVGRE (Network Virtualization using Generic Routing Encapsulation) MS 주도 캡슐화 통신 체계 개념 정립
    ↓
표준화·상용화 적용
    ↓
자동화·가상화 연계
    ↓
지능형 최적화·차세대 확장
```

NVGRE (Network Virtualization using Generic Routing Encapsulation) MS 주도 캡슐화 통신 체계은(는) 단일 기능으로 끝나지 않고 표준화, 운영 자동화, 고속화·지능화 단계로 확장된다.

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 패브릭 | NVGRE (Network Virtualization using Generic Routing Encapsulation) MS 주도 캡슐화 통신 체계를 이해할 때 함께 봐야 하는 데이터센터·클라우드 네트워크 핵심 개념 |
| 오버레이 | NVGRE (Network Virtualization using Generic Routing Encapsulation) MS 주도 캡슐화 통신 체계를 이해할 때 함께 봐야 하는 데이터센터·클라우드 네트워크 핵심 개념 |
| 로드밸런싱 | NVGRE (Network Virtualization using Generic Routing Encapsulation) MS 주도 캡슐화 통신 체계를 이해할 때 함께 봐야 하는 데이터센터·클라우드 네트워크 핵심 개념 |
| 고가용성 | NVGRE (Network Virtualization using Generic Routing Encapsulation) MS 주도 캡슐화 통신 체계를 이해할 때 함께 봐야 하는 데이터센터·클라우드 네트워크 핵심 개념 |
| 가상화 | NVGRE (Network Virtualization using Generic Routing Encapsulation) MS 주도 캡슐화 통신 체계를 이해할 때 함께 봐야 하는 데이터센터·클라우드 네트워크 핵심 개념 |
