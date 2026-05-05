+++
weight = 194
title = "194. 블루-그린 배포 (Blue-Green Deployment)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: 현재 운영 환경(Blue)과 완전히 동일한 규모의 신버전 환경(Green)을 사전 구성해두고, 트래픽을 한 번에 전환하는 '즉시 스위칭' 배포 패턴이다.
> **비유**: 블루-그린 배포는 공연 무대를 교체하는 것과 같다. 한 무대(Blue)에서 공연 중인 동안 백스테이지에서 새 무대 세트(Green)를 완전히 준비하고, 막간에 한 번에 전환한다. 문제 생기면 다시 블루 무대로 돌아가면 된다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

블루-그린 배포는 1990년대 Daniel Terhorst-North와 Jez Humble이 『Continuous Delivery』에서 정립한 패턴이다. 이름의 유래는 두 환경을 Blue(구버전)와 Green(신버전)으로 색으로 구분하는 데서 왔다.

핵심 아이디어는 단순하다: 언제든지 즉시 이전 버전으로 돌아갈 수 있는 **완전한 환경을 항상 유지**하는 것이다. 신버전(Green)이 완전히 준비되고 테스트가 완료된 이후에야 로드밸런서가 트래픽을 Green으로 전환한다. 문제가 발생하면 로드밸런서를 다시 Blue로 돌리면 된다.

이 방식이 특히 강력한 상황은 **DB 스키마 변경이 동반되는 배포**다. 신버전용 DB를 별도로 마이그레이션하고 Green 환경에서 완전히 검증한 뒤 전환하면, 구버전 코드와 신버전 DB가 섞이는 상황을 원천적으로 방지할 수 있다.

---

## 2. 구성요소

### 블루-그린 배포 구조

```
  ┌─────────────────────────────────────────────────────────────┐
  │                     Load Balancer / DNS                      │
  └──────────────────────────┬──────────────────────────────────┘
                             │
           ┌─────────────────┼─────────────────┐
           ▼                                   ▼
  ┌─────────────────┐                ┌─────────────────┐
  │  Blue 환경 (v1) │  ←── 현재 운영 │  Green 환경(v2) │ ←── 준비 중
  │  [App v1 x4]    │                │  [App v2 x4]    │
  │  [DB: Schema A] │                │  [DB: Schema B] │
  └─────────────────┘                └─────────────────┘
           │
           ▼
  [트래픽 전환 후]
  LB → Green 100% / Blue 대기 (즉시 롤백 대기)
```

### 배포 절차

| 단계 | 행동 |
|:---:|:---|
| 1 | Green 환경 프로비저닝 (Blue와 동일 인프라) |
| 2 | Green에 신버전 코드·DB 마이그레이션 적용 |
| 3 | Green 환경에서 스모크 테스트·통합 테스트 수행 |
| 4 | 로드밸런서 / DNS 레코드를 Green으로 전환 |
| 5 | 모니터링 (수 분~수 시간 안정화 관찰) |
| 6 | 안정화 확인 → Blue 환경 자원 해제 (또는 다음 배포까지 유지) |

### K8s에서의 구현

```yaml
# Blue Service (현재 운영)
apiVersion: v1
kind: Service
metadata:
  name: my-app
spec:
  selector:
    app: my-app
    version: blue    # ← 이 셀렉터를 green으로 변경하면 전환 완료
  ports:
  - port: 80
    targetPort: 8080
# Blue Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-blue
spec:
  replicas: 4
  selector:
    matchLabels:
      app: my-app
      version: blue
  template:
    metadata:
      labels:
        app: my-app
        version: blue
    spec:
      containers:
      - name: my-app
        image: my-app:v1
# Green Deployment (신버전 준비)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app-green
spec:
  replicas: 4
  selector:
    matchLabels:
      app: my-app
      version: green
  template:
    metadata:
      labels:
        app: my-app
        version: green
    spec:
      containers:
      - name: my-app
        image: my-app:v2
```

---

## 3. 구조 및 원리

**핵심 조건**: 변경 자동화와 운영 안정성은 별개가 아니라 하나의 루프이며, 빌드·검증·배포·관측·피드백이 끊기지 않아야 지속 개선이 가능하다.

동작 순서:
1. 변경 사항을 버전 관리 시스템에서 감지한다.
2. 빌드·테스트·보안 검증으로 변경의 품질을 빠르게 확인한다.
3. 승인된 산출물을 선언형 배포나 자동화 파이프라인으로 운영 환경에 반영한다.
4. 메트릭·로그·트레이스를 통해 실제 동작 결과를 관측한다.
5. 피드백을 다음 개선 주기에 연결해 반복적으로 신뢰성을 높인다.

### 블루-그린 vs 롤링 비교

| 항목 | Blue-Green | Rolling Update |
|:---|:---:|:---:|
| 구/신 버전 혼재 | ❌ (순간 전환) | ✅ (배포 중) |
| 자원 비용 | 2배 (동시 운영) | ~1.25배 |
| 롤백 속도 | 1~2초 | 수 분 |
| DB 스키마 변경 | ✅ 안전 | ⚠️ 위험 |
| 구현 복잡도 | 중간 | 낮음 (K8s 기본) |

### Warm Standby vs Blue-Green

| 항목 | Blue-Green | Warm Standby (DR) |
|:---|:---|:---|
| 목적 | 배포 전략 | 재해 복구 |
| Green/Standby 버전 | 신버전 (다른 코드) | 동일 버전 (복제) |
| 전환 계기 | 배포 완료 | 장애 발생 |

---

## 4. 비교 및 연결

**비용 최적화 전략**:
1. 클라우드 환경에서는 Green 환경을 배포 직전에 자동 프로비저닝하고, 안정화 후 Blue를 즉시 삭제하여 비용 절감
2. Terraform/Pulumi로 환경을 코드화하면 Green 환경 생성에 5분 미만 소요
3. 데이터베이스는 공유 DB + 스키마 버전 관리를 통해 DB 복제 비용 절약 가능

**상태 있는 서비스(Stateful) 주의**:
- 세션 데이터를 서버 로컬에 저장하는 서비스는 전환 시 세션 유실
- 해결책: Redis 같은 외부 세션 저장소 사용 (Stateless 아키텍처 선행 필요)

**기술사 판단 포인트**:
- 금융, 의료 등 규제 산업에서는 배포 전 완전한 검증이 필수 → Blue-Green 최적
- DNS TTL 고려: DNS 기반 전환 시 TTL만큼 구버전 응답이 섞일 수 있음 (IP 직접 전환 또는 짧은 TTL 설정)
- Blue 환경 유지 기간: 안정화 확인 전까지 최소 1~24시간 유지 권장

---

## 5. 실무 적용 및 판단

| 기대효과 | 설명 |
|:---|:---|
| 즉시 롤백 | LB 전환 1~2초로 이전 버전 복구 |
| 완전한 버전 분리 | 구/신 버전 혼재 없어 API 호환 문제 없음 |
| 프리-프로덕션 검증 | Green에서 실서비스 환경과 동일한 테스트 가능 |
| 규제 감사 용이 | 배포 이력과 롤백 증적이 명확 |

**한계**: 자원 비용 2배는 실제로는 단기간(수 시간~1일)에 불과하며, 클라우드 환경에서는 그 비용이 크지 않다. 진정한 한계는 Stateful 서비스에서 DB 데이터 동기화 복잡성과, 실시간 세션이 Blue에서 Green으로 이어지지 않는 문제다.

---

## 6. 기대효과 및 결론

블루-그린 배포 (Blue-Green Deployment)를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 블루-그린 배포 (Blue-Green Deployment)의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
Blue (현재 운영) ↔ Green (대기 환경)
    │
    ▼
배포: Green에 신버전 → 검증 → 라우터 전환
    │
    ▼
롤백: 라우터를 Blue로 되돌림 (즉시)
    │
    ▼
비용 절감: 클라우드 Auto-Provision Green 환경
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Load Balancer | 트래픽 전환의 물리적 스위치 역할 |
| DB 마이그레이션 | Blue-Green의 가장 강력한 적용 시나리오 |
| Stateless 아키텍처 | Blue-Green 세션 유실 문제의 근본적 해결책 |
| Terraform / IaC | Green 환경 자동 프로비저닝으로 비용 최적화 |
| DNS TTL | 전환 지연의 원인, 짧게 설정하여 최소화 필요 |
| Canary 배포 | Blue-Green 이후 더 세밀한 리스크 분산 전략 |

---
