+++
weight = 53
title = "53. Service/Pod/Deployment"
date = "2026-04-05"
[taxonomies]
tags = ["Cloud", "Kubernetes", "K8s", "Service", "Pod", "Deployment"]
categories = ["13_cloud_architecture"]
+++

# Service/Pod/Deployment

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 파드(Pod)는 쿠버네티스에서 컨테이너를 encapsulation하는 가장 작은 배포 단위이며, 디플로이먼트(Deployment)는 파드의 배포와 업데이트를管理하는 상위 오브젝트이고, 서비스(Service)는 파드의 동적 IP를 추상화하여 고정 진입점을 제공하는 네트워크 리소스이다.
> 2. **가치**: 이 세 가지 오브젝트의 조합은 컨테이너의 짧은 생명주기와 동적 IP 변화 문제를 해결하고, 무중단 배포와 로드밸런싱을 가능하게 한다.
> 3. **융합**: Deployment가 ReplicaSet을 통해 파드 수를 관리하고, Service가 ClusterIP/NodePort/LoadBalancer로 파드를 네트워크에 노출하며, 이三者가 함께 작동하여 MSA의 확장성과 가용성을 실현한다.

---

### Ⅰ. 개요 및 필요성 (Context & Necessity)

쿠버네티스 환경에서 컨테이너는 직접 배포되지 않는다. 컨테이너는 반드시 파드(Pod)라는 단위로 감싸서 배포되며, 이 파드를 관리하는Deployment와 네트워크를 제공하는 Service라는 추상화 계층이 존재한다. 왜 이렇게多層적(다층적) 추상화가 필요할까? 컨테이너는 짧은 생명주기를 가지고 있어 장애 시 자동으로 재시작되고, 스케일링 시 새 IP를 받게 된다. 만약 애플리케이션 코드가 직접 IP를 hard-coding한다면, 파드 재시작마다 코드 수정이 필요해질 것이다. 따라서 IP의 불확실성을 추상화하는 계층이 필수적으로 요구되었다.

파드는 하나 이상의 컨테이너를 share在一起的(함께 감싸는) 논리적 단위이다. 일반적으로 1파드 1컨테이너 원칙이 권장되지만, 하나의 파드 안에 사이드카(Sidecar) 패턴으로 메인 컨테이너와helper 컨테이너가 함께 존재할 수 있다. Deployment는 파드를管理하는上位(상위) 오브젝트로, 원하는 파드 수(Replicas)를指定하고 롤링 업데이트와 롤백 기능을 제공한다. Service는 파드의 동적 IP를 단일 고정 진입점으로 묶어 외부 또는 내부 트래픽을 분산시킨다.

```text
[Pod/Deployment/Service 계층 관계]
이 구조도는 세 오브젝트의 계층적 관계와 traffic 흐름을 보여준다.

         [Deployment (배포 관리)]
              │
              │ ReplicaSet (파드 수 유지)
              ▼
         ┌────────────────────────────────┐
         │  [ReplicaSet Controller]        │
         │  desired: 3 / current: 3        │
         └───────────────┬──────────────────┘
                         │ 파드 3개 생성
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  Pod 1   │   │  Pod 2   │   │  Pod 3   │
    │nginx:80  │   │nginx:80  │   │nginx:80  │
    └────┬─────┘   └────┬─────┘   └────┬─────┘
         │               │               │
         └───────────────┼───────────────┘
                         │ 파드 IP (동적)
                         ▼
                 ┌────────────────┐
                 │    Service     │
                 │  ClusterIP:80  │
                 │  (고정 진입점)  │
                 └───────┬────────┘
                         │ Selector: app=nginx
                         ▼
                 ┌────────────────┐
                 │  Endpoints     │
                 │ (파드 IP 목록)  │
                 └────────────────┘
```

이 구조의 핵심은 서로 다른抽象화(추상화) 계층이各自(각자) 책임과 역할을分工(분담)한다는 점이다. Deployment는 "파드가 몇 개 있어야 하는가"만 관심 있고, Service는 "어떤 파드에 traffic을 보내야 하는가"만 관심 있다. 이를 통해 Concern Separation(관심사 분리)이実現되고, 각 계층이 독립적으로 발전할 수 있게 된다.

📢 **섹션 요약 비유**: 이 관계는 항만 창고 시스템과 같습니다. Deployment는 창고 관리자가 "이 물건을 10개保管(보관)해라"라고 지시하는 것이고, Pod는 실제 물건이 들어있는 개별箱子(상자)이고, Service는 창고 앞 réception(리셉션)에서 "nginx 물건은 여기서 받으세요"라고 안내하는受付(접수) 데스크입니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**파드(Pod)**는 쿠버네티스에서最小的(가장 작은) 배포 단위로, 하나 이상의 컨테이너와 공유 스토리지, 네트워크 네임스페이스를 share한다.同一 Pod内の(동일 파드 내) 컨테이너들은 localhost를 통해 서로 통신 가능하며, IPC(Inter-Process Communication)도 가능하다. 각 파드는 고유한 클러스터 내부 IP(Pod IP)를 받으며, 파드가 죽으면 해당 IP는再也不使用(다시는 사용되지) 않는다. 파드의 리소스 요구량은 CPU Request와 Memory Request로指定되며, Limit을 超過(초과)하면 OOM(Out of Memory) Killed되거나 CPU 쓰로틀링이 발생한다.

**디플로이먼트(Deployment)**はDeploy하고更新を管理する上位オブジェクト이다. Deploymentを作成すると、ReplicaSetが自動的に作成され、ReplicaSetがPod数を管理する. ロール링 업데이트では、Deploymentのstrategyに応じて新旧のPodが교대로(교대로)作成/削除され、無停止更新が実現される. デフォルトのstrategyはRollingUpdateで、maxSurgeとmaxUnavailableパラメータで更新中の余剩/不可使Pod数を制御できる.

```yaml
# Deployment Manifest 예시
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # 여유 파드 1개 허용
      maxUnavailable: 0  # 불가용 파드 0개 (전체 무중단)
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.21
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

**서비스(Service)**는 파드의 동적 IP를 추상화하여 고정 네트워크 진입점을 제공하는 쿠버네티스 네트워킹 리소스이다. Serviceには主に4種類あり、ClusterIPはクラスタ内部通信専用、NodePortはワーカーノードの静的ポートを開示し、LoadBalancerは外部LBと統合され、ExternalNameは外部サービスを内部DNS名で参照可能にする. サービスにはLabel Selectorがあり、マッチするラベルのPodを自動的にEndpointsに登録し、Service IPへの通信を選択したPodに分散LBする.

📢 **섹션 요약 비유**: Deploymentは料理长が「この寿司を3人分作れ」と指示するのが面で、Podは実際に握られた1つの寿司で、Serviceはウェイターが「ご注文はreceiveできます」とお客様に出す皿のようなものです。寿司は傷やすくて作り直す必要があるけれど、皿はそのまま。だから皿(Service)가寿司(Pod)를，代表하여客人(ユーザー)에 서비싱합니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

Pod/Deployment/Service 외에도 쿠버네티스에는 다양한 워크로드 오브젝트가 있다. **StatefulSet**은DBやメッセージキューなどの状态保存アプリケーション用で、パ드에一意の識別子と永続ストレージを提供する. StatefulSetのパスは「nginx-0」「nginx-1」「nginx-2」のように顺序が保证され、各パ드는 PersistentVolumeClaimを通じて各自の永続ストレージにアクセスできる. **DaemonSet**はログ収取器(Fluentd)や監視エージェント(Node Exporter)などをクラスタの全ノードに1つずつ配置する用途に適している. 全ノードではなく特定ラベルのノードにのみ配置したい場合はnodeSelectorと組み合わせる.

| 워크로드 |用途| 파드 식별 | 스케일링 | 상태 관리 |
|:---|:---|:---|:---|:---|
| **Deployment** | 웹/WAS 등 무상태 | 랜덤/순번 | 자동/수동 | 불변 (Stateless) |
| **StatefulSet** | DB/큐 등 상태保存 | 고정 (ordinal) | 수동 권장 | 영속 스토리지 |
| **DaemonSet** | 로그/모니터링 | 노드당 1개 | 노드 추가 시 자동 | 무상태 |
| **Job** | 일회성 배치 | 랜덤 | parallelism控制 | 완료 시 종료 |
| **CronJob** | 스케줄링 배치 | 랜덤 | schedule 기반 | 반복 실행 |

서비스 타입도 시나리오에 따라 선택해야 한다. **ClusterIP**는 내부 서비스 간 통신에 적합하며, **NodePort**는 개발/데모 환경이나 간단한 외부 노출이 필요할 때 사용한다. **LoadBalancer**는 실제 프로덕션 환경에서 외부 트래픽을 받기 위해 필수이며, 클라우드 벤더의 네이티브 LB(예: AWS ALB, GCP Cloud Load Balancing)와統合된다. **Ingress**はURL/path 기반으로 다수의 서비스를 라우팅하는 L7 게이트웨이이며, 단일 공인 IP로 여러 서비스를 서비스할 수 있게 해준다.

```text
[서비스 타입 선택 가이드]
┌─────────────────┬────────────────────────────────────────────┐
│ 서비스 타입       │ 선택 시나리오                               │
├─────────────────┼────────────────────────────────────────────┤
│ ClusterIP       │ 마이크로서비스 간 내부 통신                   │
│ NodePort        │ 개발/데모, 임시 외부 노출 (포트: 30000~32767) │
│ LoadBalancer    │ 프로덕션 외부 LB 연동 (클라우드 네이티브)      │
│ ExternalName    │ 외부 서비스에 내부 DNS 이름 매핑              │
│ Ingress         │ URL/호스트 기반 다수 서비스 라우팅 (L7)       │
└─────────────────┴────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 쿠버네티스 워크로드는 요리 종류로 비유할 수 있습니다. Deployment는 일반적인 레스토랑 요리(대량 생산 가능한), StatefulSet은 인upati(인력 양산)寿司처럼 각자의-plate(접시)에 순서가 있는特別な(특별한) 요리이고, DaemonSet은厨房の（全厨房에 설치되는）환풍기처럼 모든 곳에 항상 설치되는 것입니다.

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

실무에서 Deployment를 설정할 때는 항상 리소스 Request와 Limit을 명시적으로指定하는 것이 필수이다.指定하지 않으면 파드가 노드의大部分(대부분) 자원을 점거하여 다른 파드에 영향을 미치는 "노이즈 네이버(Noise Neighbor)" 문제가 발생할 수 있다. 또한 livenessProbe와 readinessProbe를 설정하여 쿠버네티스가 application's 건강 상태를判断하고 appropriate한 조치(살해 또는 트래픽 전송 중지)를 취하게 해야 한다.

롤링 업데이트 전략은 서비스 특성에 따라選択해야 한다. 무중단 배포가 필수적인 웹/API 서비스에서는 maxUnavailable: 0과 maxSurge: 1 설정으로新版(신버전) 파드를 먼저启动하고旧版(구버전) 파드를，慢慢하게(점진적으로)下线(삭제)하는 것이 안전하다. однако(그러나) 이렇게 하면更新中(배포 중) 자원이 2배로 필요하므로 충분한 노드 자원이 확보되어야 한다. 데이터베이스 같이 상태가 있는 워크로드는rist数据传输(데이터 이전)가 필요한 경우가 있어 StatefulSet을 사용하고, Helm 또는 ArgoCD를利用した(활용한) 블루-그린 배포를 고려해야 할 수도 있다.

```text
[Deployment 운영 시 필수 체크포인트]
1. 리소스 설정
   ├─ resources.requests: "이 정도는 보장해줘야 해"
   ├─ resources.limits: "이 이상은 못 쓰게 해줘"
   └─ QoS Class: Guaranteed/Burstable/BestEffort 결정

2. 헬스체크 설정
   ├─ livenessProbe: "이 파 데드락이면 재시작해줘"
   ├─ readinessProbe: "아직 준비 중이면 트래픽 보내지 마"
   └─ startupProbe: "초기 로딩 오래 걸리면 그때만 봐줘"

3. 배포 전략
   ├─ RollingUpdate: 점진적 교체 (무중단, 자원 2배)
   ├─ Recreate:全旧削除後新版作成 (다운타임 발생)
   └─maxSurge/maxUnavailable:更新中の余剩 파드 수 제어

4. 버전 관리
   ├─ revisionHistoryLimit: 롤백 가능한 히스토리 수
   └─ paused:一時的に(일시적으로) 배포 일시 중지
```

또한 Deployment의 replicas 수는 단일 노드의 자원 크기를 기준으로設定해야 한다. 예컨대 노드당 4개의 파드만 실행 가능한 작은 노드를 사용하면, 10개 replicas라도 3개 노드가 필요하게 되어 자원 비효율이 발생할 수 있다. 따라서 노드 사양과 desired replicas를 함께 고려하여 노드 사이즈를 선정하는 것이 비용 효율적인 클러스터 운영의 핵심이다.

📢 **섹션 요약 비유**: Deployment 설정은 항의 짐을 싸는 것과 같습니다. 요청(requests)은 "이 정도 공간은 제 것"이라고预报(선점)하는 것이고, 리밋(limits)은 "이 이상은 못 넣게" 밧줄을 묶는 것입니다. livenessProbe는 짐이 손상되었는지 확인하는 검사대이고, readinessProbeは「まだ準備ができていない」間は客人を入れない受付像一个です.

### Ⅴ. 기대효과 및 결론 (Future & Standard)

Pod/Deployment/Service 추상화를 제대로 활용하면, 기존 VM 기반 배포 대비 압도적 운영 효율성을達成할 수 있다. Deployment의 선언적 API와 롤링 업데이트는 수동 배포 과정을 완전히 자동화하고, Service의 추상화는 애플리케이션이 인프라 변경에 영향받지 않게 한다. 이로 인해 개발팀은 비즈니스 로직 개발에만 집중할 수 있으며, 인프라 provisioning 시간은数분으로 단축된다.

| 기대 효과 | 도입 전 (手動 배포) | 도입後 (K8s Pod/Deployment/Service) | 효과 |
|:---|:---|:---|:---|
| 배포 시간 | 2~4시간 (SSH 접속, 빌드, 배포) | 5~15분 (kubectl/argocd) | 90% 단축 |
| 장애 복구 | 수동 탐지 및 복구 | 自动 (Self-healing) | MTTR 95% 단축 |
| 스케일링 | 수동 VM 프로비저닝 | 秒단위 오토스케일링 | 확장성革命 |
| 가용성 | 99.5% (단일 인스턴스) | 99.99% (다중 replicas) | 99배 향상 |

미래에는 쿠버네티스 워크로드가 더 발전하여, ArgoCD와 같은 GitOps 도구로Deployment가 완전히 Git에 의해 관리되고, Prometheus와 Grafana에 의해 지표가リアルタイム(실시간)으로 모니터링되며, Vela나其他 도구들에 의해 더 높은 수준으로 추상화되는方向发展할 것이다. 또한 Knative 기반의 서버리스 워크로드와 standard Deployment가同一(동일) 클러스터에서 공존하여, 워크로드特性에 따라最佳(최적)의 실행 방식을選択できる 환경이 보편화될 것이다. 결론적으로, Pod/Deployment/Service는 쿠버네티스 환경에서 애플리케이션을 배포하고 운영하는 가장 기본이 되는 핵심 추상화이며, 모든 클라우드 네이티브 개발자와 SRE가 반드시 마스터해야 할基础知识이다.

📢 **섹션 요약 비유**: Pod/Deployment/Service는 항구 물류 시스템과 같습니다. 컨테이너(Pod)는 실제 화물이고, Deployment는 화물 선적 관리자가 "이 화물을 100개 운송해라"指令(지시)하며, Service는 화물 도착港(항구)에서 "이 화물은 3번 창고로"라고 안내하는 운송 허브입니다. 이 세环节(环节)이 모두自動化되면 전 세계 물류가 놀라울 정도로 빠르고 효율적으로 동작합니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- 레플리카셋 (ReplicaSet) | Deployment가管理하는 파드 수 유지 컨트롤러
- 엔드포인트 (Endpoints) | Service가 선택한 파드 IP 목록을 저장하는 쿠버네티스 오브젝트
- 인그레스 (Ingress) | URL/호스트 기반 다수 서비스로 L7 라우팅하는 게이트웨이
- 스테이트풀셋 (StatefulSet) | 파드에 순서와 영속 스토리지를 제공하는 Stateful 워크로드
- 프로브 (Probe) | 파드의 health check를 수행하는 메커니즘 (Liveness/Readiness/Startup)

### 👶 어린이를 위한 3줄 비유 설명
1. 쿠버네티스에서 "파드(Pod)"는 장난감 상자예요. 안에 작은 장난감(컨테이너)이 들어있고, 각 상자에는 고유한 번호가 있어요.
2. "디플로이먼트(Deployment)"는 장난감 점장이에요. "이 장난감을 3개 준비해!"라고 하면 알아서 3개를 만들어요.
3. "서비스(Service)"는 장난감 가게 앞 알바생이에요. 가게 안에 장난감이 자주 바뀌어도, 알바생이는 "여기 있다!"라고 기억해줘요.
