+++
weight = 269
title = "269. PVC (Permanent Virtual Circuit) / SVC (Switched Virtual Circuit)"
date = "2026-05-05"
[extra]
categories = "studynote-network"
+++

## 0. 핵심 인사이트

> **핵심**: 패킷 교환망(X.25, 프레임 릴레이, ATM 등)에서 출발지와 목적지 간의 논리적인 길(가상 회선, Virtual Circuit)을 **어떻게 맺고 유지하느냐에 따라 PVC와 SVC 두 가지 방식으로 나뉜다**.
> **비유**: PVC (Permanent Virtual Circuit) / SVC (Switched Virtual Circuit)은(는) LAN/WAN 구조와 2계층 장비 안에서 데이터와 제어 규칙을 질서 있게 맞춰 주는 교통 체계와 같다.

> 📝 모범 답안

## 1. 개요 및 필요성

- **개념**: X.25나 프레임 릴레이 망 내부에서 라우터 간에 논리적 통로(Virtual Circuit)를 확립하는 두 가지 상반된 메커니즘.
  - **PVC (Permanent Virtual Circuit)**: 영구 가상 회선
  - **SVC (Switched Virtual Circuit)**: 교환 가상 회선
- **필요성**: 기업 망은 지사마다 특성이 다르다. 서울 본사와 부산 지사는 1초도 쉬지 않고 회사 인트라넷 데이터를 주고받아야 하니 '전용선' 같은 무조건적인 연결(PVC)이 필요하다. 반면, 한 달에 한 번 결산 자료만 올리는 외딴섬 출장소는 굳이 길을 24시간 열어두며 요금을 낼 필요 없이, 필요할 때만 잠시 길을 뚫어서 쓰고 버리는(SVC) 편이 경제적이다.

---

데이터 패킷 기반망이지만, 동작 방식은 아날로그 전화망(PSTN)의 회선 교환 방식을 그대로 모방했다.

1. **호 설정 (Call Setup)**: 라우터가 목적지 IP 주소를 기반으로 통신사 망에게 "가상 회선 좀 뚫어줘"라고 요청한다. 망 내부 스위치들이 길을 찾고 논리적 터널을 뚫는 데 꽤 오랜 지연 시간(Setup Delay)이 걸린다.
2. **데이터 전송 (Data Transfer)**: 길이 뚫리면 그 길(가상 회선 번호)을 타고 패킷들이 쏜살같이 연달아 날아간다.
3. **호 해제 (Call Teardown)**: 통신이 10분 정도 없거나 볼일이 끝나면 "수고했어, 길 없애자"라며 터널을 파기하고 자원(대역폭)을 반환한다.

## 2. 구성요소

- 통신사(ISP)의 네트워크 엔지니어가 망 관제 센터에서 스위치 설정을 통해 **수동으로 가상 회선을 하드코딩**해 버린다.
- 라우터를 켜자마자 호 설정(Setup) 절차 없이 즉시 데이터 전송이 가능하다.
- 길이 영원히(Permanent) 뚫려 있으므로 초기 연결 지연 시간이 제로(0)에 가깝다.
- 실무의 99% 기업들은 언제 끊길지 모르는 SVC의 불안정성을 싫어하여 **압도적으로 PVC 방식을 선호**했고, 프레임 릴레이 요금제도 PVC 위주로 팔렸다.

```text
 ┌─────────────────────────────────────────────────────────────┐
 │                    PVC vs SVC 통신 타임라인 비교                │
 ├─────────────────────────────────────────────────────────────┤
 │                                                             │
 │   [ SVC (교환 가상 회선) ]                                     │
 │   시간 0초: "A지사로 길 뚫어줘!" (Setup 요청)                   │
 │   시간 3초: 길이 뚫림 (지연 발생)                               │
 │   시간 4초: 데이터 전송 시작 ────▶                               │
 │   시간 10초: 전송 완료. "길 파기해!" (Teardown)                 │
 │                                                             │
 │   [ PVC (영구 가상 회선) ]                                     │
 │   통신사 직원이 어제 이미 길을 고정해 둠.                           │
 │   시간 0초: 라우터 전원 켜자마자 바로 데이터 전송 시작 ────▶         │
 │   시간 6초: 전송 완료 (하지만 길은 영원히 뚫려 있음)                 │
 │                                                             │
 └─────────────────────────────────────────────────────────────┘
```

## 3. 구조 및 원리

**핵심 조건**: PVC (Permanent Virtual Circuit) / SVC (Switched Virtual Circuit)은(는) Ethernet, MAC 주소, 스위칭 제약 안에서 일관된 제어 규칙을 유지할 때 효과가 난다.

동작 순서:
1. 대상 자원과 상태 정보를 수집한다.
2. 정책 또는 프로토콜 규칙에 따라 처리 기준을 결정한다.
3. 데이터 전달·주소 지정·세션 유지·오류 처리 중 필요한 제어를 수행한다.
4. 결과를 상위 계층 또는 인접 장비와 연동한다.
5. 성능 지표를 확인하여 병목과 예외 상황을 보정한다.

```text
[요구사항/트래픽 특성]
          ↓
[PVC (Permanent Virtual Circuit) / SVC (Switched Virtual Circuit)]
          ↓
[전달·제어·보호 처리]
          ↓
[성능 검증 및 최적화]
```

## 4. 비교 및 연결

| 관점 | PVC (Permanent Virtual Circuit) / SVC (Switched Virtual Circuit) | 인접 기술/대안 | 판단 포인트 |
|:---|:---|:---|:---|
| 적용 범위 | LAN/WAN 구조와 2계층 장비의 특정 문제를 직접 해결 | 상위·하위 계층 또는 대체 방식이 일부 기능을 분담 | 요구사항과 계층 경계 확인 |
| 장점 | Ethernet과 MAC 주소을 구조적으로 통제 | 범용성 또는 단순성이 강점 | 목적에 맞는 선택 필요 |
| 한계 | 스위칭·운영 복잡도 증가 가능 | 기능은 단순하지만 제어력 제한 | 비용·표준 호환성 검토 |

핵심은 단순 우열 비교가 아니라, PVC (Permanent Virtual Circuit) / SVC (Switched Virtual Circuit)이 어떤 맥락에서 더 적합한지와 인접 기술과의 역할 분담을 해석하는 데 있다.

## 5. 실무 적용 및 판단

**채택 조건**
- Ethernet과 MAC 주소을 동시에 관리해야 할 때
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

PVC (Permanent Virtual Circuit) / SVC (Switched Virtual Circuit)을 적용하면 Ethernet과 MAC 주소에 대한 통제력이 높아지고, 운영 일관성과 성능 예측 가능성을 확보할 수 있다. 반면 설정 복잡도, 표준 호환성, 장비 비용, 운영 숙련도라는 전제가 뒤따르므로 무조건적인 도입이 정답은 아니다. 결론적으로 이 주제는 LAN/WAN 구조와 2계층 장비를 이해하는 기준점이며, 최근에는 자동화·가상화·지능형 제어와 결합해 더 세밀한 최적화 방향으로 진화하고 있다.

## 7. 발전 흐름도

```text
기초 LAN/WAN 구조와 2계층 장비 이해
    ↓
PVC (Permanent Virtual Circuit) / SVC (Switched Virtual Circuit) 개념 정립
    ↓
표준화·상용화 적용
    ↓
자동화·가상화 연계
    ↓
지능형 최적화·차세대 확장
```

PVC (Permanent Virtual Circuit) / SVC (Switched Virtual Circuit)은(는) 단일 기능으로 끝나지 않고 표준화, 운영 자동화, 고속화·지능화 단계로 확장된다.

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Ethernet | PVC (Permanent Virtual Circuit) / SVC (Switched Virtual Circuit)를 이해할 때 함께 봐야 하는 LAN/WAN 구조와 2계층 장비 핵심 개념 |
| MAC 주소 | PVC (Permanent Virtual Circuit) / SVC (Switched Virtual Circuit)를 이해할 때 함께 봐야 하는 LAN/WAN 구조와 2계층 장비 핵심 개념 |
| 스위칭 | PVC (Permanent Virtual Circuit) / SVC (Switched Virtual Circuit)를 이해할 때 함께 봐야 하는 LAN/WAN 구조와 2계층 장비 핵심 개념 |
| VLAN | PVC (Permanent Virtual Circuit) / SVC (Switched Virtual Circuit)를 이해할 때 함께 봐야 하는 LAN/WAN 구조와 2계층 장비 핵심 개념 |
| 브리지/STP | PVC (Permanent Virtual Circuit) / SVC (Switched Virtual Circuit)를 이해할 때 함께 봐야 하는 LAN/WAN 구조와 2계층 장비 핵심 개념 |
