+++
weight = 248
title = "248. DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol) - Cisco 전용"
date = "2026-05-05"
[extra]
categories = "studynote-network"
+++

## 0. 핵심 인사이트

> **핵심**: DTP와 VTP는 수십~수백 대의 스위치가 엮인 거대한 기업망에서, 관리자가 일일이 트렁크 포트를 뚫고 VLAN을 생성하는 **"수작업 노가다"를 없애기 위해 시스코(Cisco)가 독자 개발한 자동화 프로토콜**이다.
> **비유**: DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol) - Cisco 전용은(는) LAN/WAN 구조와 2계층 장비 안에서 데이터와 제어 규칙을 질서 있게 맞춰 주는 교통 체계와 같다.

> 📝 모범 답안

## 1. 개요 및 필요성

- **개념**:
  - **DTP (Dynamic Trunking Protocol)**: 스위치 포트가 상대방 장비를 감지해 Access로 동작할지 Trunk로 동작할지 자동으로 결정하는 시스코 전용 프로토콜.
  - **VTP (VLAN Trunking Protocol)**: 한 스위치에서 생성/삭제/수정된 VLAN 데이터베이스(vlan.dat)를 트렁크 링크를 통해 네트워크 내 다른 스위치들과 자동 동기화하는 시스코 전용 프로토콜.
- **필요성**: 만약 스위치가 50대 있는 대학교 네트워크에 '컴퓨터공학과(VLAN 30)'를 새로 추가한다고 가정해 보자. VTP가 없다면 관리자는 스위치 50대에 일일이 원격 접속해 `vlan 30` 명령어를 50번 쳐야 한다. 또한 스위치들을 연결하는 수십 개의 포트를 일일이 `switchport mode trunk`로 세팅해야 한다. 이 극악의 비효율성을 버튼 하나(자동화)로 끝내기 위해 발명되었다.

---

시스코 스위치 포트는 기본적으로 `Dynamic Desirable` 또는 `Dynamic Auto` 모드로 설정되어 있어 쉴 새 없이 DTP 협상 패킷을 내보낸다.
- **Dynamic Desirable (적극적)**: "나랑 트렁크 맺자!"라고 먼저 들이대는 모드. 상대방이 Auto이거나 Desirable이면 트렁크가 맺어진다.
- **Dynamic Auto (수동적)**: 가만히 있다가 상대가 트렁크 맺자고(Desirable) 오면 "그래~" 하고 트렁크로 변하는 모드. (Auto끼리 만나면 둘 다 가만히 있으므로 Access 포트가 됨)

**⚠️ DTP 보안 취약점**: 해커가 노트북에 칼리리눅스(Kali)를 깔고 랜선을 빈 스위치 포트에 꽂은 뒤 "나랑 트렁크 맺자!"(DTP Desirable 패킷 발송)라고 쏘면, 멍청한 스위치 포트가 노트북과 트렁크를 맺어버린다. 해커는 트렁크 라인을 타고 흐르는 회사의 모든 VLAN 데이터를 다 엿볼 수 있게 된다. 따라서 실무에서는 반드시 **DTP 기능을 강제로 끄고 수동 설정(Static Trunk)**을 권장한다 (`switchport nonegotiate`).

## 2. 구성요소

VTP 영역(Domain)으로 묶인 스위치들은 3가지 모드 중 하나를 갖는다.
1. **Server 모드**: 대장. VLAN을 직접 만들고 지울 수 있으며, 부하들에게 전파한다.
2. **Client 모드**: 부하. VLAN을 스스로 만들지 못하고, 서버가 하라는 대로 자신의 메뉴판을 똑같이 덮어쓴다.
3. **Transparent 모드**: 방관자. VTP 메시지가 들어오면 남에게 전달(Bypass)은 해주지만, 자기 자신은 동기화하지 않고 독자적인 VLAN을 갖는다.

```text
 ┌─────────────────────────────────────────────────────────────┐
 │                VTP 리비전 번호 폭탄(Bomb) 사고                │
 ├─────────────────────────────────────────────────────────────┤
 │                                                             │
 │   [ Main Switch (Server) ] ──── 트렁크 ──── [ Switch B (Client) ] │
 │    VLAN 10, 20, 30 존재                       (정상 동기화 중)  │
 │    Revision Number: 15                                      │
 │                                                             │
 │   ⚠️ 사고 발생 시나리오:                                        │
 │   다른 테스트망에서 막 쓰다가 'Revision Number가 50'까지 올라가 버린 │
 │   고물 스위치(Server 모드)를 실수로 회사 메인망에 꽂음!              │
 │                                                             │
 │   [ 고물 스위치 ] "야! 내 리비전이 50이야! 내 걸로 다 덮어써!"       │
 │   [ Main Switch ] "헉 50이 최신이네! 내 거 15짜리 다 지우고 덮어쓸게!"│
 │                                                             │
 │   ▶ 결과: 회사의 전사 VLAN(10, 20, 30)이 순식간에 다 삭제되고      │
 │          인터넷 전면 마비 (네트워크 셧다운).                        │
 └─────────────────────────────────────────────────────────────┘
```

**⚠️ VTP 보안 취약점**: VTP는 누가 보냈든 무조건 **수정 횟수(Revision Number)가 자기보다 더 높은 놈의 말을 무조건 최신 정보로 믿고 덮어쓰는(Overwrite) 멍청한 특징**이 있다. 테스트용 장비를 잘못 꽂았다가 회사 전체 네트워크가 날아가는 사고(VTP Bomb)가 잦아, 현대 실무에서는 VTP 역시 잘 쓰지 않고 Ansible 같은 외부 자동화 툴을 사용한다.

## 3. 구조 및 원리

**핵심 조건**: DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol) - Cisco 전용은(는) Ethernet, MAC 주소, 스위칭 제약 안에서 일관된 제어 규칙을 유지할 때 효과가 난다.

동작 순서:
1. 대상 자원과 상태 정보를 수집한다.
2. 정책 또는 프로토콜 규칙에 따라 처리 기준을 결정한다.
3. 데이터 전달·주소 지정·세션 유지·오류 처리 중 필요한 제어를 수행한다.
4. 결과를 상위 계층 또는 인접 장비와 연동한다.
5. 성능 지표를 확인하여 병목과 예외 상황을 보정한다.

```text
[요구사항/트래픽 특성]
          ↓
[DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol) - Cisco 전용]
          ↓
[전달·제어·보호 처리]
          ↓
[성능 검증 및 최적화]
```

## 4. 비교 및 연결

| 관점 | DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol) - Cisco 전용 | 인접 기술/대안 | 판단 포인트 |
|:---|:---|:---|:---|
| 적용 범위 | LAN/WAN 구조와 2계층 장비의 특정 문제를 직접 해결 | 상위·하위 계층 또는 대체 방식이 일부 기능을 분담 | 요구사항과 계층 경계 확인 |
| 장점 | Ethernet과 MAC 주소을 구조적으로 통제 | 범용성 또는 단순성이 강점 | 목적에 맞는 선택 필요 |
| 한계 | 스위칭·운영 복잡도 증가 가능 | 기능은 단순하지만 제어력 제한 | 비용·표준 호환성 검토 |

핵심은 단순 우열 비교가 아니라, DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol) - Cisco 전용이 어떤 맥락에서 더 적합한지와 인접 기술과의 역할 분담을 해석하는 데 있다.

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

DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol) - Cisco 전용을 적용하면 Ethernet과 MAC 주소에 대한 통제력이 높아지고, 운영 일관성과 성능 예측 가능성을 확보할 수 있다. 반면 설정 복잡도, 표준 호환성, 장비 비용, 운영 숙련도라는 전제가 뒤따르므로 무조건적인 도입이 정답은 아니다. 결론적으로 이 주제는 LAN/WAN 구조와 2계층 장비를 이해하는 기준점이며, 최근에는 자동화·가상화·지능형 제어와 결합해 더 세밀한 최적화 방향으로 진화하고 있다.

## 7. 발전 흐름도

```text
기초 LAN/WAN 구조와 2계층 장비 이해
    ↓
DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol) - Cisco 전용 개념 정립
    ↓
표준화·상용화 적용
    ↓
자동화·가상화 연계
    ↓
지능형 최적화·차세대 확장
```

DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol) - Cisco 전용은(는) 단일 기능으로 끝나지 않고 표준화, 운영 자동화, 고속화·지능화 단계로 확장된다.

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Ethernet | DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol) - Cisco 전용를 이해할 때 함께 봐야 하는 LAN/WAN 구조와 2계층 장비 핵심 개념 |
| MAC 주소 | DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol) - Cisco 전용를 이해할 때 함께 봐야 하는 LAN/WAN 구조와 2계층 장비 핵심 개념 |
| 스위칭 | DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol) - Cisco 전용를 이해할 때 함께 봐야 하는 LAN/WAN 구조와 2계층 장비 핵심 개념 |
| VLAN | DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol) - Cisco 전용를 이해할 때 함께 봐야 하는 LAN/WAN 구조와 2계층 장비 핵심 개념 |
| 브리지/STP | DTP (Dynamic Trunking Protocol) / VTP (VLAN Trunking Protocol) - Cisco 전용를 이해할 때 함께 봐야 하는 LAN/WAN 구조와 2계층 장비 핵심 개념 |
