+++
weight = 18
title = "18. 클라우드 네트워크"
date = "2026-05-17"
[extra]
categories = "gisulsa-cloud"
+++

# 🎯 클라우드 네트워킹 (VPC & SD-WAN)

> **별점**: ★★★★☆ | 기본 필수

## 1. VPC (Virtual Private Cloud)

```
정의: 클라우드 내 논리적으로 격리된 가상 네트워크

[VPC 구성]
CIDR 블록: VPC 주소 범위 (예: 10.0.0.0/16)
서브넷:
  퍼블릭 서브넷: 인터넷 게이트웨이 연결 (웹 서버)
  프라이빗 서브넷: 인터넷 직접 접근 차단 (DB, 앱)

라우팅:
  인터넷 게이트웨이: 퍼블릭 → 인터넷
  NAT 게이트웨이: 프라이빗 → 인터넷 단방향
  VPN/Direct Connect: 온프레미스 연결

보안:
  보안 그룹 (Security Group): 인스턴스 방화벽 (Stateful)
  NACL: 서브넷 방화벽 (Stateless)

[VPC 피어링]
두 VPC 간 직접 통신 (같은 리전)
Transit Gateway: 다수 VPC 허브 연결
```

## 2. SD-WAN & SASE

```
SD-WAN (Software Defined WAN):
  소프트웨어로 WAN 연결 제어
  MPLS 대비 저비용, 인터넷 회선 활용
  중앙 집중 정책 관리

SASE (Secure Access Service Edge):
  SD-WAN + 클라우드 보안 통합
  기능: CASB, FWaaS, SWG, ZTNA
  적합: 분산 근무, 멀티클라우드

Zero Trust Network Access (ZTNA):
  VPN 대체, 위치 무관 인증·권한
  애플리케이션별 세밀한 접근 제어
```

## 3. 답안 포인트

**3단락**: ① VPC 구성(퍼블릭/프라이빗 서브넷, 보안 그룹) → ② Transit Gateway & 하이브리드 연결 → ③ SD-WAN/SASE 현대 WAN 트렌드

## 4. 관련 개념

`멀티클라우드(10번)` → Transit Gateway & VPC 피어링 | `Zero Trust(09_security)` → ZTNA = ZT 네트워크 구현 | `클라우드 보안(06번)` → VPC 보안 아키텍처
