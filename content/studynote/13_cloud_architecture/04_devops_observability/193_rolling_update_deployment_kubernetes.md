+++
weight = 193
title = "193. 롤링 배포 (Rolling Update Deployment)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: 구버전 인스턴스를 하나씩 끄고 신버전을 하나씩 켜면서 트래픽을 점진적으로 이전하는 가장 보편적인 무중단 배포 방식이다.
> **비유**: 롤링 업데이트는 마치 고속도로의 차선 개보수 공사와 같다. 전체 차선을 한꺼번에 막지 않고 한 차선씩 막아 작업하면서 나머지 차선으로 차량이 계속 통행하도록 한다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

롤링 업데이트(Rolling Update)는 Kubernetes Deployment의 기본 배포 전략으로, 전체 서비스를 중단하지 않고 인스턴스를 순차적으로 교체한다. 롤링이라는 이름은 파도처럼 점진적으로 변경이 흘러가는 모습에서 유래했다.

가장 큰 장점은 **추가 인프라 비용이 거의 없다**는 점이다. 10개의 Pod을 운영하는 서비스라면, 동시에 최대 `maxSurge`개의 신버전 Pod만 추가 생성되므로 자원 효율이 높다. 또한 K8s Deployment가 기본으로 지원하므로 별도 구성 없이 사용 가능하다.

단점은 배포 중 **구버전(v1)과 신버전(v2)이 동시에 트래픽을 처리**한다는 것이다. API 응답 형식이 버전 간 호환되지 않는다면 클라이언트가 버전에 따라 다른 응답을 받아 예기치 못한 오류가 발생한다. DB 스키마가 변경된 경우라면 구버전 코드가 새 스키마를 처리하지 못하거나, 신버전 코드가 구 스키마 데이터를 잘못 해석할 수 있다.

---

## 2. 구성요소

### K8s 롤링 업데이트 핵심 파라미터

| 파라미터 | 설명 | 기본값 |
|:---|:---|:---:|
| `maxSurge` | 원하는 Pod 수 초과 생성 허용 최대치 (절대값 또는 %) | 25% |
| `maxUnavailable` | 업데이트 중 서비스 불가 Pod 최대 허용 수 | 25% |
| `minReadySeconds` | 새 Pod가 준비 완료로 간주되기 전 최소 대기 시간(초) | 0 |
| `progressDeadlineSeconds` | 배포 진행 타임아웃 (초과 시 실패 처리) | 600 |

### 배포 단계 흐름

```
초기 상태 (v1 x4):
  [v1] [v1] [v1] [v1]    총 4개 Pod

maxSurge=1, maxUnavailable=1 설정 시:

단계 1: v2 1개 생성 → [v1][v1][v1][v1][v2]  (5개)
단계 2: v1 1개 종료 → [v1][v1][v1][v2]      (4개)
단계 3: v2 1개 생성 → [v1][v1][v1][v2][v2]  (5개)
단계 4: v1 1개 종료 → [v1][v1][v2][v2]      (4개)
  ... 반복 ...
완료: [v2] [v2] [v2] [v2]    총 4개 Pod
```

### K8s Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1          # 최대 5개까지 허용 (4+1)
      maxUnavailable: 0    # 서비스 불가 Pod 0개 (고가용성 우선)
  template:
    spec:
      containers:
      - name: my-app
        image: my-app:v2
        readinessProbe:    # 준비 완료 확인 후 트래픽 수신
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
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

### maxSurge/maxUnavailable 조합 전략

| 설정 | 특징 | 사용 시나리오 |
|:---|:---|:---|
| maxSurge=1, maxUnavailable=0 | 최대 가용성, 느린 배포 | 프로덕션 핵심 서비스 |
| maxSurge=0, maxUnavailable=1 | 자원 절약, 중간 속도 | 자원 제약 환경 |
| maxSurge=25%, maxUnavailable=25% | 기본값, 균형 | 일반 서비스 |
| maxSurge=100%, maxUnavailable=0 | 빠른 배포 (자원 2배) | 빠른 릴리즈 필요 |

### 롤백 방법

```bash
# 직전 버전으로 즉시 롤백
kubectl rollout undo deployment/my-app

# 특정 리비전으로 롤백
kubectl rollout undo deployment/my-app --to-revision=3

# 배포 상태 확인
kubectl rollout status deployment/my-app
kubectl rollout history deployment/my-app
```

---

## 4. 비교 및 연결

**구/신 버전 공존 문제 해결 방법**:
1. **API 버전 호환성 유지**: 신버전 코드가 구버전 API 형식도 처리할 수 있도록 하위 호환 설계
2. **DB 마이그레이션 선행**: expand-contract 패턴으로 스키마를 먼저 추가(호환)하고 배포 후 구버전 컬럼 제거
3. **readinessProbe 설정**: 헬스체크 실패 Pod에는 트래픽을 보내지 않아 오류 전파 방지

**배포 속도 최적화**:
- `minReadySeconds` 줄이기 (단, 충분한 워밍업 필요)
- `maxSurge` 값 높이기 (자원 여유 있을 때)
- Pod Disruption Budget(PDB)과 함께 설정하여 최소 가용 Pod 수 보장

**기술사 판단 포인트**:
- 롤링 업데이트 중 에러율이 급등하면 즉시 `kubectl rollout pause`로 일시 중지 후 원인 파악
- readinessProbe가 없으면 준비되지 않은 Pod에 트래픽이 유입되어 502/503 에러 발생
- Deployment revision 이력을 통해 롤백 지점 관리가 핵심이다

---

## 5. 실무 적용 및 판단

| 기대효과 | 설명 |
|:---|:---|
| 무중단 배포 | 서비스 중단 없이 업데이트 진행 |
| 자원 효율 | 추가 인프라 비용 최소화 |
| K8s 표준 통합 | 별도 도구 없이 Deployment로 관리 |
| 점진적 검증 | 일부 Pod의 동작을 확인하며 전체 교체 |

롤링 업데이트는 구버전 호환성이 보장된 대부분의 서비스 배포에서 최선의 선택이다. 특히 K8s 환경에서는 `readinessProbe`, `maxSurge`, `maxUnavailable` 세 가지를 제대로 설정하는 것만으로도 안정적인 무중단 배포가 가능하다.

---

## 6. 기대효과 및 결론

롤링 배포 (Rolling Update Deployment)를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 롤링 배포 (Rolling Update Deployment)의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
K8s Deployment: maxSurge · maxUnavailable 설정
    │
    ▼
Rolling Update: 기존 Pod 종료 → 신규 Pod 생성 (순차)
    ├─► Readiness Probe: 트래픽 수신 준비 확인
    └─► Graceful Shutdown: 기존 연결 완료 대기
    │
    ▼
롤백: kubectl rollout undo → 이전 ReplicaSet 복원
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| K8s Deployment | 롤링 업데이트의 기본 구현체 |
| readinessProbe | 트래픽 수신 전 준비 완료 여부 확인 핵심 설정 |
| Pod Disruption Budget | 최소 가용 Pod 수 보장으로 롤링 중 SLA 유지 |
| expand-contract 패턴 | DB 스키마 변경 시 롤링 배포와 호환 가능한 마이그레이션 |
| kubectl rollout | 배포 상태 확인·일시 중지·롤백 명령어 |
| Blue-Green / Canary | 롤링 업데이트로 해결이 어려운 상황을 커버하는 대안 전략 |

---
