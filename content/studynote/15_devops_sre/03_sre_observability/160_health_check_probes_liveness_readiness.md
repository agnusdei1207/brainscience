+++
weight = 160
title = "160. 헬스 체크/프로브 (Health Check/Probes)"
date = "2026-04-21"
[extra]
categories = "studynote-devops-sre"
+++
## 0. 핵심 인사이트

> **핵심**: 쿠버네티스 프로브는 Liveness (생사 확인), Readiness (트래픽 수신 준비), Startup (기동 완료 확인) 세 종류로, 각 프로브가 실패하면 컨테이너 재시작 또는 트래픽 라우팅 제외 등 다른 치유 동작이 수행된다.
> 2. **가치**: 올바른 헬스 체크 설계는 애플리케이션이 실제로 요청을 처리할 준비가 됐는지를 쿠버네티스가 정확히 판단하게 하여 트래픽을 준비 안 된 파드로 보내는 것을 방지한다.
> 3. **판단 포인트**: Liveness와 Readiness를 혼용하는 것이 가장 흔한 실수다. Liveness는 재시작이 필요한 상태(교착 상태, 무한 루프)만, Readiness는 트래픽을 받을 준비가 안 된 상태(DB 연결 대기, 캐시 워밍)에 사용해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

컨테이너 환경에서 프로세스가 실행 중이라도 반드시 요청을 처리할 준비가 된 것은 아니다. JVM 기반 애플리케이션은 기동에 수십 초가 걸리고, 의존 서비스(DB, 캐시)에 연결하는 데 시간이 필요하다. 애플리케이션이 기동 중에 트래픽이 들어오면 오류가 발생한다.

Kubernetes는 세 가지 프로브로 컨테이너 상태를 판단한다. Liveness Probe는 컨테이너가 정상 실행 중인지 확인하고, 실패 시 컨테이너를 재시작한다. Readiness Probe는 컨테이너가 트래픽을 받을 준비가 됐는지 확인하고, 실패 시 서비스 엔드포인트에서 제거한다. Startup Probe는 초기 기동 시간이 긴 애플리케이션에서 Liveness Probe가 너무 빨리 컨테이너를 재시작하지 않도록 보호한다.

외부 의존성 장애가 발생했을 때 Liveness Probe가 실패로 판단하면 컨테이너가 계속 재시작되는 재시작 폭풍 (Restart Storm)이 발생한다. Liveness는 외부 의존성 포함 불가, Readiness는 외부 의존성 포함 가능이 원칙이다.

📢 **섹션 요약 비유**: Liveness Probe는 "심장이 뛰고 있는가?"이고, Readiness Probe는 "일할 준비가 됐는가?"이고, Startup Probe는 "아직 출근하는 중이다, 기다려라"이다.

---

## 2. 구성요소

### 2.1 세 가지 프로브의 역할과 실패 처리

```
┌──────────────────────────────────────────────────────────────────────┐
│              Kubernetes 3종 프로브 동작 비교                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Container 기동 시작                                                 │
│       │                                                              │
│  Startup Probe (기동 완료 대기)                                      │
│  ├── 성공: Liveness + Readiness Probe 활성화                        │
│  └── 시간 초과: 컨테이너 재시작 (기동 실패)                         │
│                                                                      │
│  Liveness Probe (지속 실행 중)                                       │
│  ├── 성공: 정상 운영                                                 │
│  └── 실패 (연속 N회): 컨테이너 재시작                               │
│       (교착 상태, 메모리 누수로 응답 불가 상황 치유)                 │
│                                                                      │
│  Readiness Probe (지속 실행 중)                                      │
│  ├── 성공: 서비스 엔드포인트 포함 (트래픽 수신)                    │
│  └── 실패: 서비스 엔드포인트 제거 (트래픽 차단)                    │
│       (DB 연결 재시도 중, 캐시 워밍 중, 점진적 배포 완료 전)        │
└──────────────────────────────────────────────────────────────────────┘
```

### 2.2 헬스 체크 엔드포인트 설계 원칙

| 엔드포인트 | 포함 항목 | 제외 항목 |
|:---|:---|:---|
| `/health/live` (Liveness) | 프로세스 상태, 교착 상태 감지 | DB 연결, 외부 API |
| `/health/ready` (Readiness) | DB 연결 상태, 캐시 연결 | 외부 결제 API (옵셔널 의존성) |
| `/health` (일반) | 전체 시스템 요약 | — |

### 2.3 프로브 설정 파라미터

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 30  # 기동 후 30초 대기
  periodSeconds: 10         # 10초마다 확인
  failureThreshold: 3       # 3회 연속 실패 시 재시작
  timeoutSeconds: 5         # 응답 대기 5초

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5          # 5초마다 확인 (더 빠르게)
  failureThreshold: 2       # 2회 실패 시 트래픽 제거

startupProbe:
  httpGet:
    path: /health/live
    port: 8080
  failureThreshold: 30      # 최대 30 × 10s = 300초 기다림
  periodSeconds: 10
```

📢 **섹션 요약 비유**: Startup Probe의 failureThreshold × periodSeconds가 최대 기동 허용 시간이다. Spring Boot가 60초 걸리면 `failureThreshold: 12, periodSeconds: 5` = 60초를 보장해야 한다.

---

## 3. 구조 및 동작 원리

### 3.1 프로브 실수 사례

| 실수 | 증상 | 해결책 |
|:---|:---|:---|
| Liveness에 DB 연결 포함 | DB 재시작 시 모든 파드 연쇄 재시작 | DB 연결을 Readiness로 이동 |
| initialDelaySeconds 너무 짧음 | 기동 중 재시작 루프 | Startup Probe 도입 또는 지연 증가 |
| Readiness 실패 임계치 너무 낮음 | 네트워크 지터로 불필요한 트래픽 제거 | failureThreshold 3~5로 설정 |
| 모든 의존성 Readiness 포함 | 옵셔널 서비스 장애로 전체 파드 제거 | 크리티컬 의존성만 포함 |

### 3.2 헬스 체크 심층화 (Deep Health Check)

Shallow 헬스 체크는 HTTP 200 응답만 확인하고, Deep 헬스 체크는 DB 쿼리 실행, 캐시 읽기/쓰기, 외부 API ping 등 실제 동작을 검증한다. Deep 체크는 더 정확하지만 타임아웃 리스크가 있다.

📢 **섹션 요약 비유**: Shallow vs Deep 헬스 체크는 "환자가 눈을 뜨고 있는가(Shallow)"와 "혈압·체온·혈당 정상인가(Deep)"의 차이다. 눈을 뜨고 있어도 혈압이 위험할 수 있다.

---

## 4. 비교 및 트레이드오프

### 4.1 마이크로서비스 헬스 체크 아키텍처

```
GET /health/ready 응답 예시:
{
  "status": "UP",
  "components": {
    "db": { "status": "UP", "responseTime": "5ms" },
    "redis": { "status": "UP", "responseTime": "1ms" },
    "payment_api": { "status": "DOWN" }  ← 옵셔널
  },
  "overall": "UP"  ← 크리티컬 컴포넌트만 판단
}
```

크리티컬 컴포넌트(DB, Redis)가 UP이면 옵셔널 컴포넌트(결제 API)가 DOWN이어도 전체를 UP으로 반환한다.

### 4.2 헬스 체크 메트릭 모니터링

| 메트릭 | 의미 |
|:---|:---|
| `kube_pod_container_status_restarts_total` | 재시작 횟수 (Liveness 실패) |
| `kube_endpoint_address_not_ready` | 준비 안 된 엔드포인트 수 |
| `probe_success` (Custom) | 헬스 체크 성공률 |

📢 **섹션 요약 비유**: kube_pod_container_status_restarts_total이 증가하는 것은 직원이 하루에 여러 번 자리를 비우는 것과 같다. 왜 자꾸 자리를 비우는지 조사가 필요하다.

---

## 5. 실무 적용 및 최적화 기법

올바른 프로브 설계가 적용되면 배포 시 준비 안 된 파드로 트래픽이 라우팅되는 문제가 제거되고, 교착 상태에 빠진 파드가 자동으로 재시작된다. 롤링 업데이트 시 새 버전이 완전히 준비된 후에만 구 버전이 종료되는 무중단 배포가 보장된다.

한계는 Deep 헬스 체크가 의존 서비스에 추가 부하를 주고, 복잡한 의존성 관계에서 Readiness 조건 설계가 어렵다는 점이다. 미래 방향은 애플리케이션 상태를 Sidecar가 자동으로 판단하여 프로브를 보완하는 서비스 메시 통합이다.

📢 **섹션 요약 비유**: 헬스 체크는 공장 조립 라인의 품질 검사와 같다. 제품(파드)이 다음 단계(트래픽 수신)로 넘어가기 전에 반드시 검사(프로브)를 통과해야 한다.

---

### 📌 관련 개념 맵
| 분류 | 관련 개념 |
|:---|:---|
| 상위 개념 | Kubernetes, SRE, 페일오버 (#159) |
| 연관 기술 | 오토스케일링 (#152), 서킷 브레이커 (#153), 관측성 (#131) |
| 비교 대상 | AWS ALB 헬스 체크, Load Balancer Health Check |

### 👶 어린이를 위한 3줄 비유 설명
1. Liveness Probe는 "학생이 살아서 교실에 있는가?"이고, Readiness Probe는 "숙제를 다 해서 수업에 참여할 준비가 됐는가?"이다.
2. Startup Probe는 "학생이 학교에 오는 중이니 조금 더 기다려라"는 알림이다.
3. Liveness가 실패하면 교실에서 나갔다 다시 들어오게 하고(재시작), Readiness가 실패하면 발표 순서에서만 빼두고(트래픽 제거) 준비되면 다시 포함한다.
