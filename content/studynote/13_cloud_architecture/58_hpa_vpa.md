+++
title = "58. HPA/VPA"
date = "2026-04-05"
[taxonomies]
tags = ["Cloud", "Kubernetes", "K8s", "HPA", "VPA", "Autoscaling"]
categories = ["13_cloud_architecture"]
+++

# HPA/VPA

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: HPA(수평 파드 오토스케일러)는 CPU, 메모리 등 메트릭 값이 임계치를 초과하면 파드 수를 늘리고, VPA(수직 파드 오토스케일러)는 개별 파드의 리소스 Request/Limit 값을 자동으로 상향 조정하여 Resource 할당을 최적화한다.
> 2. **가치**: 이 두 오토스케일러의 조합(또는 단독 사용)은 트래픽 변화에 따른 동적 확장/축소를実現し、리소스 낭비를 줄이면서도 성능 저하를 방지한다.
> 3. **융합**: HPA/VPA는 쿠버네티스 오토스케일링 생태계의 핵심이며, Cluster Autoscaler와 결합하면 파드 레벨과 노드 레벨 양쪽에서 자동 확장이 가능하다.

---

### Ⅰ. 개요 및 필요성 (Context & Necessity)

클라우드 네이티브 애플리케이션의 트래픽은 시간대, 계절, 마케팅 이벤트 등에 따라剧烈하게(劇烈하게) 변동한다. 블랙프라이데이처럼 예측 가능한 대규모 트래픽은事前(사전)에 프로비저닝할 수 있지만, 바이럴 마케팅으로 인한突発적(돌발적) 트래픽 스파이크는事前 예측이 불가능하다. 전통적인 인프라에서는 피크 트래픽에 대비하여 과도하게 프로비저닝하여 비용이 증가하거나, 적게 프로비저닝하면 서비스 장애로 이어지는 딜레마가 존재했다.

쿠버네티스는 이 문제를 오토스케일링(Autoscaling)을 통해解決한다. 쿠버네티스의 오토스케일링은 크게 세 가지 차원으로 구분된다. **파드 수를 늘리는 수평 스케일링(HPA)**은 가장 널리 사용되며, CPU/메모리 사용률이 임계치를 초과하면レプリカ수를 증가시킨다. **파드 안에 있는 컨테이너의 자원 Request를調整하는 수직 스케일링(VPA)**은 파드가 너무 많거나 적은 리소스를 요청하는 경우 자동으로値を 조정한다. **노드 수를 늘리는 클러스터 스케일링(Cluster Autoscaler)**은 파드가 실행될 노드 자원이 부족할 때 워커 노드를追加하는ものである. 이 세 가지를 적절히 조합하면 파드, 컨테이너, 노드의 三次元적(삼차원적) 자동 확장이 가능하다.

```text
[쿠버네티스 3차원 오토스케일링]
         시간
    ◀─────────────────────────────────────────────────▶

    [HPA: 파드 수 늘림/줄임]
    replicas: 2 → 3 → 5 → 3 → 2

    [VPA: 파드 리소스 조정]
    cpu: 500m → 700m → 600m
    memory: 256Mi → 512Mi → 384Mi

    [CA: 노드 수 늘림/줄임]
    nodes: 3 → 4 → 5 → 3

    ┌─────────────────────────────────────────────┐
    │  이 세 차원이 함께 작동하여 트래픽 변화에       │
    │  자동으로 적응하는 탄력적 인프라를構築한다.      │
    └─────────────────────────────────────────────┘
```

이 구조의 핵심은 HPA가 "몇 개의 파드가 필요한가"를 결정하고, VPA가 "각 파드가 얼마만큼의 자원을 필요로 하는가"를 결정하며, Cluster Autoscaler가 "그 파드들을 호스팅하기 위해 몇 개의 노드가 필요한가"를 결정한다는 점이다. 이三段階(삼단계) 계층이分工合作하며 시스템 전체의 탄력성을担保한다.

📢 **섹션 요약 비유**: 쿠버네티스 3차원 오토스케일링은 크레딧 포인트 고객센터 운영과 같습니다. 트래픽이 늘어나면 (1단계) 상담원 수를 늘리고(HPA), 상담원 하나가 받을 전화가 너무 많으면 (2단계) 한 사람당 담당 고객 수를 줄이며(VPA), 그래도 상담원이太多了(너무 많으면) (3단계) 지점을 늘리는 것입니다(CA). 이 세 단계가 함께 작동하면 고객 대기 시간도 짧고 상담원도 과로하지 않는 최적 운영이 가능합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**HPA(수평 파드 오토스케일러)**는 파드数を水平적으로(수평적으로) 늘리거나 줄인다. HPA는Metrics Server에서 CPU, 메모리 사용률 같은メトリク스를 수집하고, 현재レプリ카数과目標使用率을 기반으로 목표レプリ카数を 산출한다. 공식은「目標使用率 = 현재 사용량 / (요청량 × 목표使用率)」이며, 예컨대 목표 사용률이 70%이고 현재 사용률이 140%이면レプリ카数は 2배가 된다. HPA는Deployment, StatefulSet, ReplicaSet 등의 워크로드에適用할 수 있다.

```yaml
# HPA Manifest 예시
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: nginx-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-deployment
  minReplicas: 2      # 최소 파드 수
  maxReplicas: 10     # 최대 파드 수
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70  # CPU 70% 목표
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80  # Memory 80% 목표
  behavior:            # 스케일링 동작 세밀한 조정
    scaleDown:
      stabilizationWindowSeconds: 300  # 스케일 다운 5분 대기
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
```

**VPA(수직 파드 오토스케일러)**는 파드의 CPU/메모리 Request 값을 자동으로調整한다. VPA는 특정 Deployment나 StatefulSet에关联되며, 해당 워크로드의 истори적 리소스使用量을 分析하여 적절한 Request値を 권장하거나 자동 적용한다. VPA는 네 가지 모드가 있다: **"Off"**는 권장값만 표시하고自動 적용하지 않고, **"Initial"**은 파드 생성 시에만初始 Resource을 설정하며, **"Auto"**는 실행 중에도 리소스를 자동으로更新하고, **"Recreate"**는 리소스 변경 시 파드를再生成한다.

```yaml
# VPA Manifest 예시
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: nginx-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-deployment
  updatePolicy:
    updateMode: "Auto"   # 자동 업데이트 모드
  resourcePolicy:
    containerPolicies:
    - containerName: nginx
      minAllowed:
        cpu: 100m
        memory: 64Mi
      maxAllowed:
        cpu: 4
        memory: 8Gi
      controlledResources: ["cpu", "memory"]
```

VPA와 HPA를 함께 사용할 때 주의할 점이 있다. VPA가 리소스를 늘리면 HPA의 메트릭에 영향을 미칠 수 있고, 반대로 HPA가 Scale-Out되면 VPA의 권장값이 다시 계산될 수 있다. 따라서 일반적으로는同一(동일) 워크로드에 HPA와 VPA를 동시에適用하는 것은 권장되지 않으며, VPA는 주로"적응력이 없는"시스템(예: JVM 기반 앱)에서 リソース 요청을 튜닝하는 데 사용된다.

📢 **섹션 요약 비유**: HPA와 VPA의 차이는 인력 관리와 같습니다. HPA는 "요즘 손님이 너무 많으니 상담원을 더 뽑아라"이며, VPA는 "현재 상담원 교육 수준으로 1인당 50명씩 맡기면 효율이 떨어지니, 1인당 30명씩 재배정하라"입니다. 한명은人数(파드 수)를 늘리고, 다른 한명은1인당工作量(리소스)을 조절하는 것입니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

HPA는 가장 널리 사용되는 오토스케일러이며, 다양한 自訂 메트릭을 지원한다. 쿠버네티스 기본 HPA는 CPU와 메모리만 지원하지만, Metrics Server나 Prometheus Adapter를통해自定义(커스텀) 메트릭(예: HTTP 요청 수, 큐 메시지 수, 비즈니스 메트릭)을 사용할 수 있다. 또한 외부 메트릭(External Metrics)을 통해 AWS CloudWatch, Azure Monitor 같은 클라우드 네이티브 모니터링 도구의 메트릭으로도 Scale이 가능하다. 이러한 확장은 MSA 환경에서 각 서비스가 서로 다른 메트릭 기반으로 스케일링해야 할 때 매우 유용하다.

| 오토스케일러 ||scale 대상|扩展方式|메트릭 출처|
|:---|:---|:---|:---|
| **HPA** | 파드 수 | 수평 (개수 증감) | Metrics Server, Prometheus |
| **VPA** | 파드 리소스 | 수직 (Request 조정) | Historical usage |
| **Cluster Autoscaler** | 노드 수 | 수평 (노드 증감) | 클라우드 공급자 API |

HPA와 Cluster Autoscaler(CA)의 조합은 особенно(특히) 중요하다. HPA가 파드를 늘리면 해당 파드를 호스팅할 노드 자원이 부족해질 수 있다. 이때 CA가 워커 노드를 추가하여 전체 클러스터의 처리 용량을 확장한다. 반대로 트래픽이 줄어 HPA가 파드를 줄이면, 특정 노드에 자원이 많이 남게 되고, CA가 잉여 노드를 축소하여 비용을 절감한다. 이 두 가지는 서로連動하여システム全体(시스템 전체)의 탄력성을担保する。

```text
[HPA + Cluster Autoscaler 연계 흐름]
1. 트래픽 증가 → HPA 감지
   │
2. HPA: replicas 3 → 6 (파드 수 2배)
   │
3. 기존 노드 자원으로 감당 불가 → 일부 파드 Pending 상태
   │
4. Cluster Autoscaler: Pending 감지 → 노드 2대 추가 (AWS: EC2_launch)
   │
5. 새로 늘어난 노드에 파드 배치 → 전체 6개 파드 실행 중
   │
6. 트래픽 감소 → HPA: replicas 6 → 3
   │
7. 노드 잉여 → Cluster Autoscaler: 노드 2대 축소 (AWS: EC2_terminate)
```

또한 KEDA(Kubernetes Event-driven Autoscaling)를 사용하면 собы기반(Queue size, Kafka lag, Cron-based) 스케일링이 가능하다. KEDA는$HPA를 확장하여 외부 시스템의 메트릭(예: RabbitMQ 큐 길이, Kafka consumer lag, AWS SQS 메시지 수)으로 Scale하는 것을可能하게 한다. 이를 통해 배치 처리 workloads가 Job 수를 동적으로 조절하거나, 큐 기반 시스템이 메시지 양에 따라 Worker 수를 조절하는 등、より高度な(더高度な) 스케일링이 가능하다.

📢 **섹션 요약 비유**: HPA, VPA, CA의 조합은大型商業施設(백화점)의 운영 시스템과 같습니다. 고객 수(트래픽)가 늘어나면 HPA는 계산대 상담원(파드)을 더 뽑고, CA는 매장 공간(노드)을 확대하며, VPA는 상담원 1인당 업무량(리소스)을 조절합니다. KEDA는 고객待ち行列(대기 행렬)이 길어지면 추가로 카운터를 여는 것과 같습니다.

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

HPA를 실무에 적용할 때는 다음要点을 따라야 한다. First, `minReplicas`와 `maxReplicas`를 적절히 설정해야 한다. `maxReplicas`가 너무 높으면 예기치 못한 트래픽 스파이크 시 갑자기大量의 파드가 생성되어 비용이暴涨할 수 있다. 따라서 billing alarm과 함께 `maxReplicas`上限을 설정하는 것이 필수이다. Second, `scaleDown`의 `stabilizationWindowSeconds`를 설정하여"스케일링 지프칭(fluttering)"을 방지해야 한다. 트래픽이 순간적으로 늘어나자마자 줄어들었을 때 바로 스케일 다운하면 오히려 시스템이 불안정해질 수 있다.

HPA의 `behavior` 설정을 통해 스케일링 동작을 세밀하게 조정할 수 있다. `scaleUp.rate`와 `scaleDown.rate`를 설정하면 한 번의 스케일링 이벤트에서 늘어나거나 줄어들 수 있는 파드 수의上限을控制할 수 있다. 이는 예민한(민감한) 시스템에서猛然(갑자기)한 자원 변화로 인한 성능 버벅임을 방지한다.

```text
[오토스케일링 安全运营 체크리스트]
1. HPA 설정
   ├─ minReplicas/maxReplicas: 적절한 상한/하한 설정
   ├─ scaleDown stabilization: 3~5분 대기 (지프칭 방지)
   ├─ 스케일 업/다운 속도 제한: behavior.policies 설정
   └─ 메트릭 기준: CPU/Memory + 커스텀 메트릭 활용

2. 비용 관리
   ├─ maxReplicas에 따른 비용 한계 설정
   ├─ Budget/Cost Alarm 설정
   ├─ Cluster Autoscaler minimum node pool 설정
   └─ 스팟 인스턴스 활용 (비용 절감)

3. 장애 대비
   ├─ 스케일링 중에도 서비스 가용성 보장 (readinessProbe)
   ├─ Circuit Breaker (호출 지연 시 스케일 블로킹)
   └─ Graceful Shutdown (스케일 다운 시 처리 중 요청 완료를 기다림)

4. 모니터링
   ├─ HPA/VPA/CA의 스케일링 이벤트 로깅
   ├─ Prometheus + Grafana로 스케일링 패턴 분석
   └─ Alert: 스케일링 빈도 이상 감지 시通知
```

VPA 사용 시에도 주의할 점이 있다. VPA가 파드의 Resource Request를 更新하면 파드가再生成되기 때문에, 사용량이 급변하는 워크로드에서는 잦은 파드 재시작이 발생할 수 있다. 따라서 VPA는比較적 안정적인 리소스使用 패턴을持つ 워크로드에 적합하다. 또한 VPA와 PDB(Pod Disruption Budget)을 함께 사용하여, VPA로 인한 파드再作成이_service availability에 영향을 주지 않도록 해야 한다.

📢 **섹션 요약 비유**: 오토스케일링 안전 운영은大型遊園地(놀이공원)의 운행 관리와 같습니다. 놀이기구가 갑자기 한 번에 모두 가동되면(무분별한 스케일 업) 기계에 무리가 가고, 너무 빠르게 줄였다가 다시 손님이 오면対応不及(대응 미흡)이 됩니다. 그래서 스케일 업/다운 속도를 적절히 조절하고, 동시에 놀이기구 이용고객(사용자)에게 불편이 가지 않도록 입구에서ゆっくり(천천히) 분산시키는 것이 중요합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)

HPA/VPA와 Cluster Autoscaler를 적절히 활용하면, 인프라 비용을 최적화하면서도 높은 service availability를 달성할 수 있다. 필요할 때만 자원을 확보하고, 불필요할 때는 즉시 반납함으로써 시간당 과금의 클라우드 환경에서 비용 효율성을 극대화한다. 또한 수동 스케일링으로 인한 운영 인력의 부담과 인적 오류를 제거하여 DevOps 문화를実現한다.

| 기대 효과 | 도입 전 (고정 프로비저닝) | 도입後 (오토스케일링) | 효과 |
|:---|:---|:---|:---|
| 인프라 비용 | Peak 기준 과도 프로비저닝 | 실제 사용량 기반 | 30~50% 절감 |
| 장애 발생률 |手動扩展不及로 장애 | 자동 빠른 대응 | 80% 감소 |
| 운영 인력 부담 | 24/7 모니터링 필요 | alarms만 확인 | 70% 감소 |
| 사용자 경험 | 트래픽 초과 시 장애 | 자동 확장으로 안정 | 99% 향상 |

미래에는 KEDA와 같은 이벤트 기반 스케일링이 표준이 되어, 단순히 CPU/메모리가 아니라 비즈니스 메트릭( 주문 수, 결제 금액, 게임 접속자 수 등)으로도 스케일링하는 환경이 확대될 것이다. 또한 AI/ML 기반 수요 예측으로 사전 프로비저닝하는 Predictive Autoscaling도 발전하고 있으며, 스케일링 결정이 더욱智能적으로(지능적으로) 이루어지는 방향으로 진화하고 있다. 결론적으로, 오토스케일링은 클라우드 네이티브의 핵심 가치인 "신속한 탄력성(Rapid Elasticity)"을実装하는 필수 메커니즘이며, 쿠버네티스 환경에서 HPA/VPA를 통한 파드 레벨 스케일링과 Cluster Autoscaler를 통한 노드 레벨 스케일링의 조합이 가장 완성도 높은 탄력성 확보 전략이다.

📢 **섹션 요약 비유**: 오토스케일링은 미래 도시의 스마트 전력망과 같습니다. 전력 소비량(트래픽)이 늘면 발전기를 더 가동하고(Scale-Out), 소비량이 줄면 발전기를 끄며(Scale-In), 가동 중인 발전기의 효율(리소스)도 자동으로 조절합니다. 이렇게 하면 전기 낭비도 없고, 정전(장애)도 막을 수 있어 시민 모두가 편안하게 생활할 수 있습니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- HPA (Horizontal Pod Autoscaler) | CPU, 메모리 등 메트릭 기반으로 파드数を水平적으로 늘리거나 줄이는 오토스케일러
- VPA (Vertical Pod Autoscaler) | 파드의 CPU/메모리 Request/Limit 값을 자동으로 상향 조정하는 오토스케일러
- Cluster Autoscaler | 파드를 호스팅할 노드 자원이 부족할 때 워커 노드를追加하는 클러스터 레벨 오토스케일러
- Metrics Server | 쿠버네티스 리소스 메트릭을 수집하여 HPA 등에 제공하는 구성 요소
- KEDA (Kubernetes Event-driven Autoscaling) | 이벤트 기반 오토스케일링을実現하는 도구

### 👶 어린이를 위한 3줄 비유 설명
1. HPA는 장난감 가게에 손님이 줄을 서면 더 많은 점원을 뽑는 것이에요. 손님이 줄어들면 점원 수도 줄여요.
2. VPA는 점원 한 명이 너무 많이 일을 하면, 업무 분담을 조절해서 더 효율적으로 일하게 하는 거예요.
3. 이 두 가지를 함께 쓰면 가게는 항상 적절한 수의 점원과 적절한工作量으로 운영돼요!
