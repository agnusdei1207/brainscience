+++
weight = 83
title = "83. Kube-proxy - 노드 내부의 네트워크 라우팅 및 서비스 로드밸런싱 통신 규칙(iptables/IPVS) 설정"
date = "2026-05-05"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: (개념 본질)
> **비유**: (개념 비유)

---

> 📝 모범 답안

## 1. 개요 및 필요성

쿠버네티스에서 Pod는 임시적이다. 죽었다가 다시 뜨면 IP가 바뀐다. 애플리케이션이 이 변화를 직접 추적하게 두면, 서비스는 주소 변경 때문에 쉽게 깨진다. Kube-proxy는 이 문제를 해결하기 위해 Service라는 안정된 진입점을 만들고, 실제로는 살아 있는 Pod들로 트래픽을 흘려 보낸다.

즉, Kube-proxy는 패킷을 직접 오래 들고 나르는 서비스가 아니라, 노드 내부에 규칙을 심어 두고 커널이 알아서 분배하게 만드는 설정자다. 서비스 이름은 고정되고, 뒤에 연결된 Pod만 바뀐다. 이것이 쿠버네티스 서비스 추상화의 핵심이다.

```text
┌──────────────────────────────────────────────────────────────┐
│ Client → Service VIP → Kube-proxy 규칙 → Live Pod IP       │
│ Pod가 바뀌어도 Service 주소는 그대로 유지                   │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. 구성요소

Kube-proxy는 보통 모든 워커 노드에 DaemonSet으로 배포된다. 그리고 Service와 Endpoints 변경을 감시해 iptables 또는 IPVS 테이블을 갱신한다. 여기서 실제 패킷 중계는 커널이 수행하고, Kube-proxy는 규칙만 만든다. 패킷은 DNAT (Destination Network Address Translation)을 거쳐 목적지 Pod로 바뀐다.

| 모드 | 처리 위치 | 탐색 방식 | 확장성 |
| :--- | :--- | :--- | :--- |
| Userspace | 사용자 공간 | 직접 프록시 | 매우 낮음 |
| iptables | 커널 netfilter | 순차 룰 탐색 | 중간 |
| IPVS (IP Virtual Server) | 커널 LVS (Linux Virtual Server) | 해시 테이블 + 알고리즘 | 높음 |

Service 타입도 함께 봐야 한다. ClusterIP는 클러스터 내부에서만 쓰는 안정된 VIP이고, NodePort는 모든 노드에 동일 포트를 열어 외부 진입을 허용한다. LoadBalancer는 클라우드 로드밸런서 뒤에서 노드나 서비스를 노출한다. 어떤 타입이든 최종 Pod 분배는 결국 Kube-proxy의 규칙을 따른다.

```text
┌────────────────────────────────────────────────────────────────┐
│ Service/Endpoints 변경 ─► Kube-proxy Watch ─► 규칙 갱신       │
├────────────────────────────────────────────────────────────────┤
│ Packet ─► iptables/IPVS ─► DNAT ─► Backend Pod               │
└────────────────────────────────────────────────────────────────┘
```

핵심은 "Kube-proxy가 느린가"보다 "규칙이 얼마나 빨리 바뀌는가"다. 규칙이 늦으면 새로운 Pod가 떠도 트래픽이 따라오지 못하고, 규칙이 과도하면 성능이 떨어진다.

---

## 3. 구조 및 원리

**핵심 조건**: 컨테이너/쿠버네티스 환경에서는 선언형 상태, 스케줄링 정책, 네트워크·스토리지 연동, 복구 자동화가 일관되게 맞물려야 운영 안정성이 확보된다.

동작 순서:
1. 사용자가 원하는 최종 상태를 선언형으로 정의한다.
2. 컨트롤 플레인이 스케줄링과 리소스 배치를 결정한다.
3. 런타임이 컨테이너를 기동하고 네트워크·스토리지를 연계한다.
4. 서비스 계층이 외부 트래픽과 내부 통신을 안정적으로 중계한다.
5. 프로브·오토스케일링·정책 엔진이 복구와 최적화를 반복한다.

Kube-proxy는 Ingress나 외부 전송 계층 로드밸런서와 역할이 다르다. 외부 로드밸런서는 클러스터로 들어오는 큰 입구를 담당하고, Ingress는 애플리케이션 계층에서 경로와 호스트를 나눈다. Kube-proxy는 그 안쪽에서 Service VIP를 실제 Pod로 쪼개는 마지막 단계다.

| 비교 항목 | 외부 전송 계층 로드밸런서 | Ingress | Kube-proxy |
| :--- | :--- | :--- | :--- |
| 위치 | 클러스터 외부 | 클러스터 경계 | 모든 워커 노드 |
| 분산 대상 | 노드 | 서비스/경로 | Pod |
| 주된 계층 | 전송 계층 | 애플리케이션 계층 | 전송 계층 |
| 역할 | 클러스터 입구 | URL/호스트 라우팅 | 서비스 VIP 라우팅 |

iptables와 IPVS도 비교해야 한다. iptables는 규칙 수가 늘수록 순차 탐색 부담이 커져 O(n)에 가깝고, IPVS는 해시 기반 탐색과 로드밸런싱 알고리즘으로 더 잘 버틴다. 그래서 서비스 수가 많거나 엔드포인트가 많을수록 IPVS가 유리하다. 최근에는 eBPF 기반 CNI가 Kube-proxy 기능 일부를 대체하기도 한다.

---

## 4. 비교 및 연결

실무에서는 서비스 수와 트래픽을 먼저 본다. 작은 클러스터면 iptables도 충분하지만, 서비스와 엔드포인트가 많아지면 선형 탐색이 병목이 된다. 그때는 IPVS로 바꾸거나, 더 나아가 eBPF 기반 dataplane으로 전환할지 검토한다.

또 하나의 핵심은 Source IP 보존이다. Kube-proxy는 다른 노드의 Pod로 넘기기 위해 SNAT (Source Network Address Translation)을 적용할 수 있는데, 그러면 백엔드 로그에 클라이언트의 실제 IP가 아니라 노드 IP가 찍힌다. 이 문제가 중요하면 `externalTrafficPolicy: Local`을 고려해야 하지만, 노드별 부하 불균형이라는 대가가 있다.

체크리스트는 다음과 같다.
1. 서비스/엔드포인트 수가 iptables 선형 탐색을 감당할 정도인가?
2. 실제 클라이언트 IP 보존이 필요한가?
3. kube-proxy daemonset이 모든 워커 노드에 정상 배포됐는가?
4. CNI (Container Network Interface)와 kube-proxy 방식이 충돌하지 않는가?

안티패턴은 명확하다. Pod IP를 앱에 하드코딩하거나, NodePort/LoadBalancer가 알아서 다 해결해 줄 것이라 착각하거나, SNAT의 존재를 모르고 감사 로그를 해석하는 것이다. 네트워크 문제는 대개 규칙이 어긋났을 뿐이다.

---

## 5. 실무 적용 및 판단

Kube-proxy는 서비스 이름을 안정적으로 유지하면서 Pod의 생명주기를 숨겨 준다. 그 결과 애플리케이션은 IP 변경을 신경 쓰지 않고도 트래픽을 처리할 수 있고, 운영자는 Service 단위로 네트워크를 관리할 수 있다.

한편 규모가 커질수록 iptables의 한계, SNAT로 인한 원본 IP 손실, 규칙 동기화 지연이 드러난다. 그래서 결론은 단순하다. Kube-proxy는 필수지만 영원한 정답은 아니며, 규모와 요구사항에 따라 IPVS나 eBPF 대체 경로를 검토해야 한다.

---

## 6. 기대효과 및 결론

Kube-proxy - 노드 내부의 네트워크 라우팅 및 서비스 로드밸런싱 통신 규칙(iptables/IPVS) 설정를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 Kube-proxy - 노드 내부의 네트워크 라우팅 및 서비스 로드밸런싱 통신 규칙(iptables/IPVS) 설정의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
Service / Endpoints
    │
    ▼
Kube-proxy Watch
    │
    ├────────► iptables
    │
    ├────────► IPVS (IP Virtual Server)
    │
    └────────► eBPF (Extended Berkeley Packet Filter)
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
| :--- | :--- |
| Service | 고정된 접근점(VIP) |
| Endpoints | 실제 살아 있는 Pod 목록 |
| iptables | 기본 규칙 삽입 방식 |
| IPVS (IP Virtual Server) | 대규모용 고성능 규칙 엔진 |
| DNAT (Destination Network Address Translation) | 목적지 주소 변환 |
| SNAT (Source Network Address Translation) | 소스 IP 변환 |
| eBPF (Extended Berkeley Packet Filter) | 차세대 대체 dataplane |
| CNI (Container Network Interface) | Pod 네트워크를 실제로 연결하는 계층 |

---
