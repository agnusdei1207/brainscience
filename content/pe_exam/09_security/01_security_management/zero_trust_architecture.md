+++
title = "제로 트러스트 아키텍처 (Zero Trust Architecture)"
date = 2024-05-18
description = "NIST SP 800-207 기반의 제로 트러스트(ZTA) 핵심 원칙, 논리적 구성 요소, 마이크로 세그멘테이션, 그리고 Istio를 활용한 ZTA 구현 예제"
weight = 40
+++

# 제로 트러스트 아키텍처 심층 분석 (Zero Trust Architecture, ZTA)

## 1. 제로 트러스트의 탄생 배경과 정의
기존의 사이버 보안 모델은 "성(Castle)과 해자(Moat)" 모델이었습니다. 외부 네트워크는 신뢰하지 않고, 방화벽이나 VPN 내부의 사설 네트워크는 신뢰(Trust)하는 방식입니다. 그러나 클라우드 마이그레이션, 재택근무의 일상화, BYOD(Bring Your Own Device) 등으로 인해 명확한 네트워크 경계(Perimeter)가 붕괴되었습니다. 또한, 내부망이 뚫렸을 경우 횡적 이동(Lateral Movement)을 통해 치명적인 피해가 발생하는 문제가 대두되었습니다.

**제로 트러스트(Zero Trust)**는 "Never Trust, Always Verify" (결코 신뢰하지 말고, 항상 검증하라)라는 단일 철학을 바탕으로 합니다. 사용자나 기기의 네트워크 위치(내부망/외부망)에 관계없이 모든 리소스 접근 요청을 엄격하게 인증하고 지속적으로 검증하는 보안 패러다임입니다.

## 2. NIST SP 800-207 기반의 ZTA 핵심 원칙
미국 국립표준기술연구소(NIST)는 제로 트러스트를 구현하기 위한 7가지 핵심 원칙을 제시합니다.
1. 모든 데이터 소스와 컴퓨팅 서비스는 리소스로 간주한다.
2. 네트워크 위치와 상관없이 모든 통신은 안전해야 한다.
3. 개별 기업 리소스에 대한 접근은 세션 단위로 부여된다.
4. 리소스에 대한 접근 권한은 클라이언트 신원, 애플리케이션/서비스, 요청하는 자산의 관측 가능한 상태를 포함한 동적 정책에 의해 결정된다.
5. 기업은 소유하고 있는 모든 자산의 무결성과 보안 상태를 모니터링하고 측정한다.
6. 모든 리소스의 인증과 인가는 동적이며, 접근이 허용되기 전에 엄격하게 강제된다.
7. 기업은 현재의 네트워크 및 통신 상태에 대한 가능한 한 많은 정보를 수집하고, 이를 보안 상태 개선에 활용한다.

## 3. ZTA의 논리적 아키텍처 (Logical Components)

제로 트러스트의 인프라는 제어 평면(Control Plane)과 데이터 평면(Data Plane)으로 분리됩니다.

```ascii
[ 제로 트러스트 논리적 아키텍처 (NIST Model) ]

                +-------------------------------------------------+
                |                  제어 평면 (Control Plane)      |
                |                                                 |
  +-------+     |  +----------------+      +-------------------+  |
  |  CDP  | ----|->| 정책 엔진 (PE) | ---> | 정책 관리자 (PA)  |  |
  +-------+     |  | (Policy Engine)|      | (Policy Admin)    |  |
(Threat Intel,  |  +----------------+      +-------------------+  |
 IAM, SIEM...)  +-------------------------------------------------+
                                                     | (Control Channel)
                                                     v
          +-------------------------------------------------------------+
          | +---------+       데이터 평면 (Data Plane)      +---------+ |
Subject   | |         |                                     |         | |   Enterprise
(User/  ===>| PEP (정책 시행 지점) | =====================> |   PEP   |===> Resource
Device)   | | (Policy Enforcement  |    (Data Channel)      |         | |   (App/Data)
          | +---------+       Point)                        +---------+ |
          +-------------------------------------------------------------+
```

- **PE (Policy Engine)**: 부여된 접근 권한을 허용할지 결정하는 브레인. IAM, SIEM, 위협 인텔리전스(CDP) 등의 입력을 받아 동적 신뢰 스코어를 계산합니다.
- **PA (Policy Administrator)**: PE의 결정에 따라 데이터 평면의 PEP에게 세션을 설정하거나 종료하도록 지시하는 구성 요소.
- **PEP (Policy Enforcement Point)**: 사용자와 리소스 사이에서 실제 트래픽을 차단하거나 허용하는 게이트웨이 (예: 로드밸런서, 마이크로-API 게이트웨이, 방화벽).

## 4. 핵심 구현 기술: 마이크로 세그멘테이션 (Micro-segmentation)
네트워크를 거대한 하나의 존(Zone)으로 관리하지 않고, 개별 워크로드, 애플리케이션, 또는 컨테이너 단위로 네트워크를 아주 작게 분할하는 기술입니다. 공격자가 하나의 엔드포인트를 탈취하더라도 다른 마이크로 세그먼트로 이동(Lateral Movement)하는 것을 물리적/논리적으로 차단합니다.

## 5. 실무 구현 코드: Istio를 활용한 ZTA (Service Mesh)
클라우드 네이티브 환경(Kubernetes)에서는 Istio와 같은 서비스 메시(Service Mesh)를 사용하여 ZTA의 mTLS 및 마이크로 세그멘테이션을 완벽하게 구현할 수 있습니다. 각 파드(Pod)에 주입된 Envoy 프록시가 PEP 역할을 수행합니다.

```yaml
# Istio AuthorizationPolicy 예제: 특정 서비스(PEP)에 대한 접근 제어 강제
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: "require-mtls-and-jwt"
  namespace: "finance-backend"
spec:
  selector:
    matchLabels:
      app: payment-service
  action: ALLOW
  rules:
  - from:
    # 1. mTLS가 적용된 특정 서비스 어카운트만 접근 허용 (Network Identity)
    - source:
        principals: ["cluster.local/ns/frontend/sa/checkout-service-sa"]
    to:
    # 2. 특정 HTTP 메서드와 경로만 허용 (Micro-segmentation)
    - operation:
        methods: ["POST", "GET"]
        paths: ["/api/v1/payments/*"]
    when:
    # 3. JWT 토큰 내의 특정 클레임 검증 (User/App Identity & Context)
    - key: request.auth.claims[iss]
      values: ["https://auth.company.com"]
    - key: request.auth.claims[group]
      values: ["finance-admins"]
```

위 YAML 설정은 `finance-backend` 네임스페이스의 `payment-service`에 접근하기 위해, 반드시 `checkout-service-sa` 신원 증명을 통한 mTLS 암호화 통신을 해야 하며, 동시에 인가된 발급자가 발행한 JWT 토큰(finance-admins 그룹)을 제시해야만 `/api/v1/payments/*` 엔드포인트에 도달할 수 있도록 강제합니다. (다중 계층 검증)

## 6. 결론
제로 트러스트 아키텍처는 단순한 솔루션이나 제품을 도입한다고 달성되는 것이 아닙니다. ID 기반 인증 통합(SSO, MFA), 엔드포인트 보안(EDR), 소프트웨어 정의 경계(SDP), 그리고 지속적인 모니터링이 유기적으로 결합된 전체적인 전략입니다. 클라우드와 MSA의 확산에 따라 ZTA는 더 이상 선택이 아닌 필수적인 생존 전략이 되었습니다.
