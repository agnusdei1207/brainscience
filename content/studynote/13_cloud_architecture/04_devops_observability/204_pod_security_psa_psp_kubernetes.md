+++
weight = 204
title = "204. 컨테이너 보안 / Pod 시큐리티 (PSA/PSP)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: Kubernetes PSA(Pod Security Admission)는 Pod를 Privileged·Baseline·Restricted 세 보안 프로파일로 분류하여, 루트 실행·호스트 네트워크 접근 같은 위험 구성을 클러스터 레벨에서 강제로 차단하는 입장 통제 메커니즘이다.
> **비유**: PSA는 건물 출입문 보안과 같다. 방문자(Pod)가 들어오기 전에 "이 사람이 마스터키(root)를 가졌는지", "보안 구역(host network)에 접근하려는지"를 체크하여, 위험한 사람은 애초에 입장 자체를 막는다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

컨테이너 환경의 보안 위협은 전통 VM 환경과 다르다. 컨테이너는 호스트 커널을 공유하므로, 특권(Privileged) 컨테이너가 탈출하면 전체 노드, 나아가 클러스터 전체를 장악할 수 있다. 이것이 "컨테이너 킬 체인(Container Kill Chain)"의 핵심 시나리오다.

실제 공격 사례: 2019년 runc 취약점(CVE-2019-5736)은 Privileged 컨테이너에서 호스트 파일 시스템의 `/proc/self/exe`를 통해 호스트 runc 바이너리를 덮어쓸 수 있는 취약점이었다. 루트가 아닌 컨테이너에서는 이 공격이 불가능했다.

Kubernetes는 이를 방어하기 위해 PodSecurityPolicy(PSP)를 도입했지만, 복잡한 설정과 RBAC 통합 문제로 운영이 어려웠다. 1.21에서 deprecated, 1.25에서 완전 제거되고 PSA(Pod Security Admission)로 대체됐다.

---

## 2. 구성요소

### PSA 세 가지 보안 프로파일

| 프로파일 | 허용 수준 | 적합 상황 |
|:---|:---|:---|
| **Privileged** | 제한 없음 (모든 권한 허용) | 시스템 데몬, 인프라 에이전트 (최소 사용) |
| **Baseline** | 알려진 권한 상승 차단 | 일반 앱 워크로드, 최소한의 보안 |
| **Restricted** | 최소 권한 강제 | 보안 중요 워크로드, 권장 기본값 |

### Restricted 프로파일 주요 규칙

```
Restricted 프로파일이 금지하는 것:
  ❌ runAsRoot (UID=0으로 실행)
  ❌ allowPrivilegeEscalation: true
  ❌ hostNetwork: true
  ❌ hostPID: true / hostIPC: true
  ❌ privileged: true
  ❌ securityContext.capabilities 추가
  ✅ runAsNonRoot: true (필수)
  ✅ seccompProfile: RuntimeDefault (필수)
  ✅ readOnlyRootFilesystem: true (권장)
```

### K8s PSA 네임스페이스 레이블 설정

```yaml
# 네임스페이스에 PSA 프로파일 적용
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    # enforce: 정책 위반 시 Pod 생성 거부
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: v1.28
    # audit: 위반 로그만 기록 (생성은 허용)
    pod-security.kubernetes.io/audit: restricted
    # warn: 위반 경고 메시지 (생성은 허용)
    pod-security.kubernetes.io/warn: restricted
```

### Restricted 준수 Pod 예시

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-app
spec:
  securityContext:
    runAsNonRoot: true           # 루트 실행 금지
    runAsUser: 1000              # 일반 사용자로 실행
    runAsGroup: 3000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault       # 기본 seccomp 프로파일 적용
  containers:
  - name: app
    image: myapp:v1
    securityContext:
      allowPrivilegeEscalation: false   # 권한 상승 금지
      readOnlyRootFilesystem: true      # 루트 파일시스템 읽기 전용
      capabilities:
        drop:
        - ALL                           # 모든 Linux 캐퍼빌리티 제거
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

### PSP vs PSA 비교

| 항목 | PSP (구, 제거됨) | PSA (신, 현재) |
|:---|:---|:---|
| K8s 버전 | ~1.24 (1.25에서 제거) | 1.22 도입, 1.25 GA |
| 설정 방식 | RBAC와 복잡한 통합 | 네임스페이스 레이블 단순 설정 |
| 유연성 | 세밀한 커스터마이징 | 3개 표준 프로파일 |
| 운영 복잡도 | 높음 | 낮음 |
| 외부 도구 | OPA Gatekeeper, Kyverno로 보완 가능 | 동일 |

### OPA Gatekeeper vs PSA

| 항목 | PSA | OPA Gatekeeper |
|:---|:---|:---|
| 목적 | Pod 보안 프로파일 적용 | 커스텀 정책 강제 |
| 정책 언어 | 내장 프로파일 | Rego 언어 |
| 적용 범위 | Pod/컨테이너 보안 | 모든 K8s 리소스 |
| 복잡도 | 낮음 | 높음 (강력함) |
| 권장 사용 | 기본 Pod 보안 | 조직 커스텀 정책 |

---

## 4. 비교 및 연결

**PSA 마이그레이션 전략 (PSP → PSA)**:
```
1단계: 감사 모드 활성화 (warn + audit)
   - 기존 워크로드가 위반하는 내용을 로그로 수집
   - 제거 없이 현황 파악

2단계: 애플리케이션 수정
   - 로그 기반으로 각 워크로드의 securityContext 수정
   - runAsNonRoot, readOnlyRootFilesystem 추가

3단계: enforce 모드 전환
   - 네임스페이스별로 단계적으로 enforce 적용
   - 예외 처리가 필요한 시스템 컴포넌트 격리

4단계: 모니터링 강화
   - 정책 위반 시도 알림 설정
```

**컨테이너 킬 체인 방어 레이어**:
```
공격 단계              방어 수단
─────────────────────────────────────────
1. 취약점 코드 실행  → SAST/DAST, 이미지 스캔
2. 컨테이너 내부 탐색 → Read-only FS, capabilities 제거
3. 권한 상승 시도    → allowPrivilegeEscalation: false
4. 호스트 접근 시도  → hostNetwork/PID 금지, seccomp
5. 클러스터 이동     → NetworkPolicy, RBAC 최소 권한
```

**기술사 판단 포인트**:
- PSA는 네임스페이스 레벨 적용이므로, 시스템 컴포넌트(kube-system)와 일반 워크로드를 별도 네임스페이스에 분리해야 한다.
- Restricted 프로파일 적용 시 기존 Helm 차트나 사이드카(Istio 등)가 위반할 수 있으므로 사전 감사가 필수다.
- OPA Gatekeeper나 Kyverno를 함께 사용하면 이미지 태그 latest 금지, 리소스 제한 강제 등 PSA 이상의 정책을 적용 가능하다.

---

## 5. 실무 적용 및 판단

| 기대효과 | 설명 |
|:---|:---|
| 컨테이너 탈출 방어 | Privileged 컨테이너 실행 원천 차단 |
| 규정 준수 자동화 | 보안 정책이 인프라에 내재화됨 |
| 공격 표면 축소 | 불필요한 Linux 캐퍼빌리티 제거 |
| 감사 용이성 | 네임스페이스 레이블로 정책 상태 즉시 확인 |

PSA는 K8s 보안의 첫 번째 방어선이다. Restricted 프로파일을 기본값으로 시작하고, 예외는 명시적으로 허용하는 "기본 거부(Default Deny)" 원칙이 제로 트러스트 보안 모델의 컨테이너 구현이다.

---

## 6. 기대효과 및 결론

컨테이너 보안 / Pod 시큐리티 (PSA/PSP)를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 컨테이너 보안 / Pod 시큐리티 (PSA/PSP)의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
PodSecurityPolicy (PSP, 폐지됨)
    │
    ▼
Pod Security Admission (PSA): 네임스페이스 레벨 보안
    ├─► Privileged: 제한 없음
    ├─► Baseline: 위험 설정 차단
    └─► Restricted: 최소 권한 강제
    │
    ▼
OPA Gatekeeper · Kyverno → 세밀한 정책 관리
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| OPA Gatekeeper | PSA 이상의 커스텀 K8s 정책 강제 도구 |
| 컨테이너 이미지 스캔 | PSA와 함께 컨테이너 킬 체인의 앞단 방어 |
| RBAC (Role-Based Access Control) | PSA와 함께 K8s 최소 권한 원칙 구현 |
| NetworkPolicy | Pod 간 통신을 제어하는 PSA 보완 정책 |
| seccomp / AppArmor | 시스템 콜 수준의 컨테이너 격리 강화 |
| Kyverno | Rego 없이 YAML로 K8s 정책을 정의하는 대안 |

---
