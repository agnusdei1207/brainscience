+++
weight = 7
title = "07. 네트워크 가상화 (NFV/SDN 심화)"
date = "2026-05-17"
[extra]
categories = "gisulsa-network"
+++

# 🎯 SDN & NFV 심화 & 네트워크 슬라이싱

> **별점**: ★★★★★ | ★135회 기출

## 1. SDN 심화

```
[OpenFlow 프로토콜]
컨트롤러 ↔ 스위치 표준 프로토콜
플로우 테이블: 매칭 필드 + 액션 + 카운터

[플로우 테이블 처리]
패킷 도착 → 플로우 테이블 매칭
  매칭 O: 액션 수행 (Forward/Drop/Modify)
  매칭 X: 컨트롤러에 문의 (Packet-In)
  → 컨트롤러가 새 플로우 규칙 설치

[SDN 컨트롤러]
OpenDaylight, ONOS, Ryu
P4: 데이터 플레인 프로그래밍 언어
  → 패킷 처리 로직을 소프트웨어로 정의
```

## 2. 네트워크 슬라이싱

```
정의: 하나의 물리 네트워크 위에 가상의 독립적인
     논리 네트워크를 여러 개 생성

[5G 네트워크 슬라이싱]
eMBB 슬라이스: 고속 모바일 브로드밴드
URLLC 슬라이스: 초저지연 (자율주행, 산업)
mMTC 슬라이스: 대규모 IoT 연결

격리 보장:
  각 슬라이스 간 성능·보안 격리
  SLA별 차별화된 서비스

[기술 기반]
SDN + NFV + MEC + 5G 코어(AMF/SMF/UPF)
```

## 3. ETSI NFV 아키텍처

```
[NFV 주요 구성]
VNF (Virtual Network Function): 가상화된 네트워크 기능
  예) 가상 방화벽, 가상 로드밸런서, 가상 라우터

NFVI (NFV Infrastructure):
  컴퓨팅 + 스토리지 + 네트워크 하드웨어

MANO (Management & Orchestration):
  NFV 오케스트레이터 (NFVO) → VNF 라이프사이클 관리
  VNF 매니저 (VNFM) → VNF 인스턴스 관리
  VIM → NFVI 자원 관리 (OpenStack)

서비스 체이닝 (SFC):
  트래픽 → VNF1(방화벽) → VNF2(IDS) → VNF3(LB)
  = 가상 함수 연결
```

## 4. 답안 포인트

**3단락**: ① SDN 심화(OpenFlow/P4) → ② 네트워크 슬라이싱 & 5G 연계 → ③ ETSI NFV MANO 오케스트레이션

## 5. 관련 개념

`5G(★133회)` → 네트워크 슬라이싱의 기반 | `ETSI ZSM(★135회)` → NFV 자율 관리 | `클라우드(13번)` → NFV + 클라우드 통합
