+++
title = "다크 론칭 (Dark Launching)"
description = "신규 기능을 사용자 인터페이스에 노출하지 않고 백그라운드에서 프로덕션 트래픽으로 성능과 안정성을 사전 검증하는 고급 배포 기법"
date = 2024-05-15
[taxonomies]
tags = ["Dark-Launching", "Deployment", "Testing", "Production", "Canary", "DevOps"]
+++

# 다크 론칭 (Dark Launching)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 새로운 기능을 사용자에게 UI로 공개하지 않은 상태에서, 프로덕션 환경의 실제 트래픽(또는 트래픽 미러링)을 백엔드 신규 코드로 흘려보내 성능, 에러율, 응답 시간을 실전처럼 검증하는 '숨겨진 시범 운영' 기법입니다.
> 2. **가치**: 사용자 경험에 영향을 주지 않으면서 프로덕션 규모의 부하와 실제 데이터로 신규 기능을 테스트할 수 있어, 정식 공개(Launch) 후 발생할 수 있는 장애를 90% 이상 사전 차단합니다.
> 3. **융합**: 피처 플래그(Feature Flag), 트래픽 섀도잉(Traffic Shadowing), 서비스 메시(Istio)와 결합하여 MSA 환경에서 완벽하게 통제된 실험 환경을 구축하는 핵심 전략입니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**다크 론칭(Dark Launching)**은 소프트웨어 개발에서 신규 기능이나 서비스를 최종 사용자에게 공식적으로 발표(Official Launch)하기 전에, 사용자 인터페이스(UI)에 노출하지 않은 채(다크/Dark) 백그라운드에서 실제 프로덕션 환경에 배포하고, 실제 트래픽(또는 복제된 트래픽)으로 기능을 검증하는 배포 전략입니다. 사용자는 신규 기능의 존재를 알지 못하지만, 백엔드에서는 신규 코드가 실행되어 실제 DB 조회, 외부 API 호출, 계산 로직 등이 수행됩니다. 결과는 사용자에게 반환되지 않고 폐기(Discard)되거나 별도 로깅 시스템에만 기록됩니다. 페이스북이 2011년 "Messenger" 기능을 출시 전 이 방식으로 수개월간 테스트한 것으로 유명합니다.

### 💡 2. 구체적인 일상생활 비유
새로운 요리를 메뉴에 올리기 전에, **비공개 주방 테스트**를 한다고 상상해 보세요. 손님들은 여전히 기존 메뉴만 주문하지만, 주방에서는 손님이 주문한 스테이크 요리와 똑같은 재료로 새로운 소스를 만들어 맛을 보고, 조리 시간을 측정하고, 재료 소진량을 확인합니다. 손님에게는 기존 요리가 그대로 나가지만, 주방은 새 요리가 실전에서 얼마나 잘 작동할지 미리 알 수 있습니다. 문제가 발견되면 메뉴에 올리기 전에 레시피를 수정합니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (스테이징 환경의 비현실성)**:
   전통적인 테스트는 스테이징(Staging) 환경에서 수행되었습니다. 그러나 스테이징은 프로덕션과 다음과 같은 차이가 있습니다: ① 트래픽 양이 1/1000 수준 ② 데이터가 샘플/가짜 데이터 ③ 하드웨어 스펙이 다름. 이로 인해 "스테이징에서는 문제없었는데 프로덕션에서 터졌다"는 상황이 빈번했습니다.

2. **혁신적 패러다임 변화의 시작**:
   페이스북, 구글, 아마존 같은 메가 스케일 기업들은 "프로덕션만이 진짜 프로덕션과 같다"는 깨달음으로, 신규 기능을 사용자 몰래 프로덕션에서 먼저 실행해 보는 '다크 론칭' 문화를 정착시켰습니다. 이는 "실패를 조기에, 안전하게 경험하라(Fail Fast, Fail Safely)"는 DevOps 철학의 구현입니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   블랙 프라이데이, 명절 이벤트 등 대규모 트래픽이 예상되는 시즌에 새로운 추천 알고리즘을 도입해야 할 때, 스테이징 테스트만으로는 부족합니다. 다크 론칭은 실제 사용자 행동 패턴으로 알고리즘을 검증하여 이벤트 당일 장애를 예방합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Component) | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/도구 | 비유 |
| :--- | :--- | :--- | :--- | :--- |
| **Feature Flag (Dark)** | UI 노출 없이 백엔드 코드만 활성화 | 플래그가 'dark' 모드면 신규 로직 실행, 결과는 폐기 | LaunchDarkly, Unleash | 주방 테스트 모드 스위치 |
| **Traffic Mirroring** | 실제 요청을 복제하여 신규 서비스로 전달 | 미러링된 트래픽은 응답을 기다리지 않음 (Fire & Forget) | Istio, Envoy, Nginx | 주방에 재료 복사본 전달 |
| **Shadow Service** | 신규 기능을 담당하는 격리된 서비스 | 기존 서비스와 병렬 실행, 결과 비교 | Kubernetes Deployment | 새 요리 테스트용 조리대 |
| **Response Discarder** | 신규 서비스 응답을 사용자에게 반환하지 않음 | 미러링 요청의 응답은 로그만 남기고 폐기 | Custom Middleware | 테스트 요리는 맛보고 버림 |
| **Comparison Engine** | 기존 vs 신규 결과 비교 분석 | 응답 시간, 에러율, 결과 일치율 자동 계산 | Prometheus, Custom | 기존 요리와 새 요리 비교 |
| **Observability Stack** | 다크 실행의 메트릭/로그 수집 | 신규 서비스 전용 대시보드, 알람 | Grafana, Datadog | 테스트 결과 기록 장부 |

### 2. 정교한 구조 다이어그램: 다크 론칭 아키텍처

```text
=====================================================================================================
                      [ Dark Launching - Traffic Shadowing Architecture ]
=====================================================================================================

  [ User Request Flow ]                                               [ Dark Launch Parallel Path ]
         │                                                                      │
         ▼                                                                      │
+------------------+                                                    │
| Client Request   |                                                    │
| GET /api/product │                                                    │
+--------┬---------+                                                    │
         │                                                              │
         ▼                                                              │
+------------------------------------------------------------------------------------------+
|                              [ Service Mesh / API Gateway ]                               |
|                                                                                           |
|  +---------------------------+                    +-------------------------------------+   |
|  │ Incoming Request          │                    │ Traffic Mirroring Engine             │   |
|  │ Route to Production Service│ ───────────────► │ Istio VirtualService / Envoy Mirror  │   |
|  └─────────────┬─────────────┘                    │ - Mirror 100% of traffic             │   |
|                │                                  │ - Async (non-blocking)               │   |
|                │                                  └────────────────┬────────────────────┘   |
|                │                                                   │                        |
|                ▼                                                   ▼                        |
+------------------------------------------------------------------------------------------+
         │                                                                     │
         │ Main Path                                                    Shadow Path
         ▼                                                                     ▼
+------------------------+                                       +------------------------+
| Production Service     |                                       | Shadow Service (New)   |
| (v1.0 Stable)          |                                       | (v2.0 Candidate)       |
| ┌──────────────────┐   |                                       | ┌──────────────────┐   |
| │ Business Logic   │   |                                       | │ New Algorithm    │   |
| │ (Old Algorithm)  │   |                                       | │ (Under Test)     │   |
| └────────┬─────────┘   |                                       | └────────┬─────────┘   |
|          │             |                                       |          │             |
|          ▼             |                                       |          ▼             |
| ┌──────────────────┐   |                                       | ┌──────────────────┐   |
| │ Response         │   |                                       | │ Response         │   |
| │ (Returned to     │   |                                       | │ (Discarded!      │   |
| │  User)           │   |                                       | │  Not sent back)  │   |
| └──────────────────┘   |                                       | └────────┬─────────┘   |
+------------------------+                                                │             |
         │                                                                │             |
         │                                                         ┌──────┴──────┐      |
         │                                                         │ Metrics &   │      |
         │                                                         │ Logs Only   │      |
         ▼                                                         └──────┬──────┘      |
+------------------------+                                                │             |
| User receives response │                                                ▼             |
| (Unaware of shadow)    │                                    +------------------------+   |
+------------------------+                                    | Comparison & Analysis  |   |
                                                              | ┌──────────────────┐   |   |
                                                              | │ Latency Compare  │   |   |
                                                              | │ Error Rate       │   |   |
                                                              | │ Result Match %   │   |   |
                                                              | └──────────────────┘   |   |
                                                              +------------------------+   |
                                                                           │              |
                                                                           ▼              |
+------------------------------------------------------------------------------------------+
|                              [ Observability Dashboard ]                                  |
|                                                                                          |
|  +-----------------------------+        +-----------------------------+                  |
|  │ Production Service Metrics  │        │ Shadow Service Metrics      │                  |
|  │ p99 Latency: 120ms          │        │ p99 Latency: 85ms ✓         │                  |
|  │ Error Rate: 0.1%            │        │ Error Rate: 0.05% ✓         │                  |
|  │ Throughput: 10k RPS         │        │ Throughput: 10k RPS (mirror)│                  |
| +-----------------------------+        +-----------------------------+                  |
|                                                                                          |
|  Decision: Shadow service shows BETTER performance. Ready for gradual traffic shift.    |
+------------------------------------------------------------------------------------------+

=====================================================================================================
```

### 3. 심층 동작 원리 (트래픽 미러링과 응답 폐기 메커니즘)

**① 트래픽 미러링 (Traffic Mirroring / Shadow Traffic)**
서비스 메시(Istio) 또는 API 게이트웨이(Kong, Nginx)는 들어오는 모든 요청을 복제하여 '섀도우 서비스'로 비동기 전송합니다. 핵심 특성:
- **Non-blocking**: 미러링된 요청의 응답을 기다리지 않고 즉시 원래 요청을 처리합니다.
- **Fire & Forget**: 섀도우 서비스가 느리거나 에러를 내도 사용자 경험에 영향이 없습니다.
- **100% 또는 비율 설정**: 전체 트래픽을 미러링하거나, 10%만 샘플링할 수 있습니다.

**② 응답 폐기 (Response Discarding)**
섀도우 서비스의 응답은 사용자에게 절대 반환되지 않습니다. 미러링 엔진은 응답을 수신하자마자 폐기합니다. 대신:
- 응답 시간, 상태 코드, 응답 본문 크기를 메트릭으로 기록합니다.
- 에러 발생 시 상세 스택 트레이스를 로그로 저장합니다.

**③ 결과 비교 분석 (Result Comparison)**
기존 서비스와 섀도우 서비스의 결과를 비교합니다:
- **기능적 일치율**: 두 서비스의 응답이 논리적으로 동일한가?
- **성능 비교**: 신규 서비스가 더 빠른가, 느린가?
- **에러율 차이**: 신규 코드에서 더 많은 에러가 발생하는가?

### 4. 핵심 알고리즘 및 실무 코드 예시

**Istio VirtualService 트래픽 미러링 설정**

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: product-service
spec:
  hosts:
  - product-service
  http:
  - route:
    - destination:
        host: product-service
        subset: v1  # Production (stable)
      weight: 100
    mirror:
      host: product-service
      subset: v2  # Shadow (new feature under test)
    mirrorPercentage:
      value: 100.0  # Mirror 100% of traffic (adjust as needed)
```

**피처 플래그 기반 다크 실행 (Python 예시)**

```python
import os
from dataclasses import dataclass
import logging
import time

logger = logging.getLogger(__name__)

@dataclass
class ProductRecommendation:
    product_id: str
    score: float

class RecommendationService:
    def __init__(self):
        self.dark_launch_enabled = os.getenv('DARK_LAUNCH_V2', 'false').lower() == 'true'

    def get_recommendations(self, user_id: str) -> list[ProductRecommendation]:
        """Main entry point - always returns v1 results to user."""

        # 1. Always call stable v1 algorithm (production)
        v1_results = self._get_v1_recommendations(user_id)

        # 2. If dark launch enabled, run v2 in background (shadow execution)
        if self.dark_launch_enabled:
            self._run_dark_launch_v2(user_id, v1_results)

        return v1_results

    def _get_v1_recommendations(self, user_id: str) -> list[ProductRecommendation]:
        """Stable production algorithm - returned to user."""
        # Simulate v1 algorithm
        time.sleep(0.120)  # 120ms latency
        return [
            ProductRecommendation("prod-001", 0.95),
            ProductRecommendation("prod-002", 0.88),
        ]

    def _run_dark_launch_v2(self, user_id: str, v1_results: list):
        """
        Dark launch execution - results NOT returned to user.
        Executed asynchronously, errors are caught and logged.
        """
        try:
            start_time = time.time()

            # Call new v2 algorithm
            v2_results = self._get_v2_recommendations(user_id)

            latency_ms = (time.time() - start_time) * 1000

            # Compare v1 vs v2 results
            match_rate = self._compare_results(v1_results, v2_results)

            # Log metrics for observability (Prometheus format)
            logger.info(
                "dark_launch_v2_execution",
                extra={
                    "user_id": user_id,
                    "v2_latency_ms": latency_ms,
                    "match_rate": match_rate,
                    "v2_result_count": len(v2_results),
                }
            )

            # Check performance criteria
            if latency_ms > 200:  # Threshold: 200ms
                logger.warning(f"Dark launch v2 slow: {latency_ms}ms")

        except Exception as e:
            # Never crash the main request due to dark launch failure
            logger.error(f"Dark launch v2 error (user not affected): {e}")

    def _get_v2_recommendations(self, user_id: str) -> list[ProductRecommendation]:
        """New algorithm under test - darker, faster, better?"""
        # Simulate new ML-based algorithm
        time.sleep(0.085)  # 85ms latency (improved!)
        return [
            ProductRecommendation("prod-001", 0.97),  # Slightly different scores
            ProductRecommendation("prod-003", 0.91),  # Different product!
        ]

    def _compare_results(self, v1: list, v2: list) -> float:
        """Calculate overlap/match rate between v1 and v2."""
        v1_ids = {r.product_id for r in v1}
        v2_ids = {r.product_id for r in v2}
        intersection = len(v1_ids & v2_ids)
        union = len(v1_ids | v2_ids)
        return intersection / union if union > 0 else 0.0
```

**Grafana 대시보드 메트릭 쿼리 (Prometheus)**

```promql
# Dark launch v2 latency comparison
histogram_quantile(0.99,
  sum(rate(dark_launch_v2_latency_bucket[5m])) by (le)
) / histogram_quantile(0.99,
  sum(rate(recommendation_v1_latency_bucket[5m])) by (le)
)

# Dark launch error rate (should be near 0, but doesn't affect users)
sum(rate(dark_launch_v2_errors_total[5m])) / sum(rate(dark_launch_v2_total[5m]))

# Result match rate (functional correctness)
avg(dark_launch_match_rate)
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 배포 검증 기법 비교

| 평가 지표 | 스테이징 테스트 | 카나리 배포 | 다크 론칭 | A/B 테스트 |
| :--- | :--- | :--- | :--- | :--- |
| **프로덕션 트래픽** | 없음 (가짜) | 일부 (1%~100%) | 100% 미러링 | 일부 분할 |
| **사용자 노출** | 없음 | 있음 (일부 사용자) | 없음 (UI 숨김) | 있음 (비교군) |
| **장애 영향** | 없음 | 일부 사용자 영향 | 없음 | 일부 사용자 영향 |
| **검증 항목** | 기능 위주 | 기능+성능 | 성능+안정성 | 비즈니스 메트릭 |
| **실행 비용** | 낮음 | 중간 | 높음 (리소스 2배) | 중간 |
| **적용 시나리오** | 초기 개발 | 점진적 출시 | 백엔드 리팩터링 | UI/UX 실험 |

### 2. 과목 융합 관점 분석

**다크 론칭 + 서비스 메시 (Service Mesh)**
- Istio/Envoy의 트래픽 미러링 기능을 활용하면 애플리케이션 코드 수정 없이 인프라 레벨에서 다크 론칭을 구현할 수 있습니다. 이는 "관심사의 분리" 원칙을 따릅니다.

**다크 론칭 + MLOps**
- 새로운 머신러닝 모델을 배포할 때, 기존 모델과 새 모델에 동일한 실제 트래픽을 입력하여 예측 정확도와 지연 시간을 비교합니다. 모델 드리프트(Model Drift) 문제를 사전에 감지할 수 있습니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 대규모 알고리즘 교체 (추천 시스템 v1 → v2)**
- **문제점**: 추천 알고리즘을 완전히 새로 작성했습니다. 스테이징에서는 잘 작동하지만, 프로덕션의 수백만 사용자 데이터에서도 제대로 동작할지 확신이 없습니다.
- **기술사 판단 (전략)**: 다크 론칭으로 2주간 섀도우 실행합니다. 모든 추천 요청을 v1과 v2에 동시에 보내고, v2의 응답 시간과 결과 품질을 모니터링합니다. v2가 v1보다 빠르고 정확하면 카나리 배포로 전환합니다.

**[상황 B] 데이터베이스 마이그레이션 (MySQL → PostgreSQL)**
- **문제점**: DB를 교체해야 합니다. 쿼리 호환성과 성능을 실전 데이터로 검증해야 합니다.
- **기술사 판단 (전략)**: CDC(Change Data Capture)로 MySQL의 쓰기 트래픽을 PostgreSQL에 실시간 복제합니다. 읽기 트래픽은 다크 론칭으로 PostgreSQL에 미러링하여 쿼리 결과를 비교합니다. 일치율이 99.9% 이상이면 실제 전환을 진행합니다.

### 2. 도입 시 고려사항 (체크리스트)

**기술적 고려사항**
- [ ] 리소스 비용: 섀도우 서비스를 위한 추가 인프라 (CPU, 메모리, DB)
- [ ] 트래픽 격리: 섀도우 트래픽이 프로덕션 DB에 쓰기 작업을 하지 않도록 주의
- [ ] 미러링 비율 조절: 100% 미러링은 과도할 수 있음, 10%~50%로 시작

**운영/보안적 고려사항**
- [ ] 민감 데이터 처리: 섀도우 서비스에서도 개인정보 보호 규정 준수
- [ ] 로그 보관: 다크 실행 로그는 별도 인덱스로 분리하여 비용 관리
- [ ] 롤백 계획: 언제든 미러링을 중단할 수 있는 스위치 확보

### 3. 주의사항 및 안티패턴 (Anti-patterns)

**안티패턴 1: 섀도우 서비스가 프로덕션 DB에 쓰기 수행**
- 다크 론칭은 읽기 전용이어야 합니다. 섀도우 서비스가 실제 DB에 데이터를 쓰면 데이터 오염이 발생합니다. 별도 테스트 DB를 사용하거나 읽기 복제본을 활용해야 합니다.

**안티패턴 2: 미러링 지연이 프로덕션에 영향**
- 서비스 메시의 미러링 버퍼가 가득 차면 프로덕션 요청 처리가 지연될 수 있습니다. 비동기 미러링과 백프레셔(backpressure) 처리가 필수입니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | 스테이징 테스트만 (AS-IS) | 다크 론칭 적용 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **프로덕션 장애율** | 15% (새 기능 배포 시) | 2% (사전 검증) | **장애율 87% 감소** |
| **성능 문제 발견** | 프로덕션 배포 후 발견 | 배포 전 발견 | **사전 탐지 100%** |
| **사용자 불만** | 장애 시 CS 접수 증가 | 없음 (사용자 영향 없음) | **사용자 영향 제로** |
| **출시 자신감** | 낮음 ("잘 되려나?") | 높음 ("실전 검증 완료") | **출시 품질 향상** |

### 2. 미래 전망 및 진화 방향
- **AI 기반 자동 비교 분석**: 머신러닝이 기존 vs 신규 서비스의 결과 차이를 자동으로 분석하고, 유의미한 차이(Regression)를 탐지하여 자동 롤백을 트리거하는 지능형 다크 론칭 시스템으로 진화할 것입니다.
- **서버리스 다크 론칭**: AWS Lambda 등 서버리스 환경에서도 트래픽 미러링을 손쉽게 구성할 수 있는 관리형 서비스가 등장할 것입니다.

### 3. 참고 표준/가이드
- **Google SRE Workbook (Chapter 14)**: 다크 론칭과 카나리 분석 모범 사례
- **Martin Fowler's Blog**: Feature Toggles and Dark Launching
- **Istio Documentation**: Traffic Mirroring (Shadowing)

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **[카나리 배포](@/studynotes/15_devops_sre/3_automation/deployment_strategies.md)**: 다크 론칭 검증 후 점진적 트래픽 전환
- **[피처 플래그](@/studynotes/15_devops_sre/1_sre/feature_toggle.md)**: 다크 론칭 활성화/비활성화 제어
- **[서비스 메시](@/studynotes/13_cloud_architecture/1_native/service_mesh.md)**: 트래픽 미러링 인프라
- **[A/B 테스팅](@/studynotes/15_devops_sre/1_sre/42_ab_testing.md)**: UI 노출 후 비즈니스 메트릭 비교
- **[옵저버빌리티](@/studynotes/15_devops_sre/2_observability/observability_fundamentals.md)**: 다크 실행 메트릭 수집 및 분석

---

## 👶 어린이를 위한 3줄 비유 설명
1. 새로운 요리를 메뉴에 올리기 전에, **보이지 않는 주방**에서 먼저 연습해요. 손님은 모르지만 주방에서는 열심히 테스트하죠!
2. 이 주방에서는 진짜 재료로 요리해보고, 시간이 얼마나 걸리는지, 맛은 어떤지 미리 확인해요. 문제가 있으면 메뉴에 올리기 전에 고치죠.
3. 덕분에 손님은 항상 맛있는 요리만 먹게 되고, 요리사도 자신 있게 새 요리를 내놓을 수 있어요!
