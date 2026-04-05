+++
weight = 59
title = "59. 스토리지/볼륨"
date = "2026-04-05"
[taxonomies]
tags = ["Cloud", "Kubernetes", "K8s", "Storage", "Volume", "CSI"]
categories = ["13_cloud_architecture"]
+++

# 스토리지/볼륨

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 쿠버네티스 볼륨은 파드生命周期에 묶인 임시 스토리지이고, 영구 볼륨(PV)은 파드과는 독립적으로 존재하며 PersistentVolumeClaim(PVC)을 통해 파드에 마운트되는 영구 스토리지이다.
> 2. **가치**: 이 계층 구조는 컨테이너의 휘발성 문제를 해결하여 데이터베이스, 메시지 큐 등 상태 저장형 애플리케이션의 정상 동작을担保하며, CSI(Container Storage Interface)를 통해 다양한 스토리지 백엔드를統一적으로(통일적으로)接続できる。
> 3. **융합**: 쿠버네티스 스토리지 모델은 클라우드 네이티브 데이터 관리의 기반이 되며, StatefulSet과 연계하여 순서 있는 배치와 고유한 식별자를 통한 영속성保证를 실현한다.

---

### Ⅰ. 개요 및 필요성 (Context & Necessity)

컨테이너의 가장 큰 특징 중 하나는 **불변성(Immutability)**이다. 컨테이너 이미지는 읽기 전용이며, 컨테이너 내부에서 발생한 모든 변경(파일 생성, 데이터 쓰기 등)은容器销毁時に一緒に破棄される(컨테이너 파괴 시 함께 파기된다). 이는 stateless 앱에서는 문제가 되지 않지만, 데이터베이스, 메시지 큐, 로그 수집기처럼persistent storage가 필요한 애플리케이션에서는 치명적인 문제가 된다. 쿠버네티스 볼륨은 이 문제를 해결하기 위해 컨테이너에 외부 스토리지를 마운트하는 메커니즘을 제공한다.

쿠버네티스 스토리지 모델은 단순히 디스크를 마운트하는 것을 넘어, 다양한 백엔드(AWS EBS, Azure Disk, GCP PD, NFS, Ceph, GlusterFS 등)를同一(동일)한 인터페이스로抽象化한다. 이를 통해 애플리케이션은 underlying storage 구현에 구애받지 않고 데이터를 영속적으로保存할 수 있다. 또한 개발자는 로컬 파일 시스템과 동일한API로 스토리지에 접근할 수 있어 애플리케이션 포팅이 용이하다.

```text
[쿠버네티스 스토리지 모델: 4가지 주요 볼륨 유형]
┌──────────────────────────────────────────────────────────────────────────┐
│ 1. emptyDir: 파드 내부 임시 스토리지                                      │
│    - 파드와生命周期 동거, 파드 삭제 시 데이터 손실                         │
│    - 사이드카 컨테이너 간 공유 스토리지로 활용                            │
│                                                                       │
│ 2. hostPath: 노드 로컬 스토리지                                           │
│    - 특정 노드의 파일 시스템을 파드에 마운트                              │
│    - 노드 종속으로 스케줄링 고려 필요, StatefulSet과 자주 사용            │
│                                                                       │
│ 3. PersistentVolume (PV): 클러스터 레벨 영구 스토리지                     │
│    - 파드生命周期와 독립적으로 존재                                      │
│    - 관리자가事前プロビジョ닝하거나 StorageClass로 동적 프로비저닝        │
│                                                                       │
│ 4. projected: 시크릿/ConfigMap/ downwardAPI 등을 파드에 마운트           │
│    - 여러 소스를同一 디렉터리에マッピング投影                        │
└──────────────────────────────────────────────────────────────────────────┘
```

스토리지의 مهم성은 MSA와 데이터중심(데이터 중심) 아키텍처에서 더욱 부각된다. Kafka, PostgreSQL, Elasticsearch와 같은 상태 저장형 애플리케이션은故障가 발생해도 데이터가 손실되어서는 안 되며,副本(복제본)을 통해 고가용성을担保해야 한다. 쿠버네티스 스토리지 모델은 이러한 요구를 충족하기 위해 PV/PVC 추상화와 StatefulSet의 조합을 제공한다.

📢 **섹션 요약 비유**: 쿠버네티스 스토리지는 항구 화물 운송 시스템과 같습니다. 컨테이너(컨테이너)는 화물선(파드)이 떠나면 화물도 같이 사라지는使い捨て箱(일회용 상자)와 같습니다. 그래서 중요한 화물(데이터)은 반드시船내(컨테이너)에固定(고정)되지 않는 항구 창고(PV)에 보관을 하며, 화물을 찾고 싶을 때마다 창고 열쇠(PVC)를 사용하여 접근합니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

쿠버네티스 볼륨은 크게 **임시 볼륨(Ephemeral Volume)**과 **영구 볼륨(Persistent Volume)**으로 구분된다. **임시 볼륨**의 대표格は`emptyDir`이며, 파드가 노드에 스케줄링될 때 创建되고 파드가 삭제되면 함께销毁される(파기된다). emptyDir의 용도는 다양하며, 사이드카 패턴에서 메인 컨테이너와helper 컨테이너 간의 데이터 공유(예: 로그 수집기), 또는 일시적인 캐시 저장소 등으로 활용된다.

**영구 볼륨(PV)**는 파드의生命周期과 무관하게 존재하는 스토리지 리소스이다. PV는 클러스터 전체에서 공유되며, 특정 네임스페이스에 종속되지 않는다. PV는 관리자가 수동으로 생성하는 **Static Provisioning**과, 사용자가 PVC를 요청하면 시스템이 자동으로 PV를 생성하는 **Dynamic Provisioning** 두 가지 방식이 있다. Dynamic Provisioning은 **StorageClass**를 통해実現되며, 사용 가능한 StorageClass가 있으면 사용자의 PVC 요청에 따라 적절한 스토리지 볼륨이 자동으로 생성된다.

```yaml
# PersistentVolumeClaim 예시
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce   # 단일 노드에 읽기/쓰기 (RWO)
    # - ReadOnlyMany   # 다수 노드에 읽기 전용 (ROX)
    # - ReadWriteMany  # 다수 노드에 읽기/쓰기 (RWX)
  resources:
    requests:
      storage: 10Gi    # 10Gi 스토리지 요청
  storageClassName: "gp3"   # AWS EBS gp3 스토리지 클래스
  selector:
    matchLabels:
      environment: production
```

PV와 PVC의Binding(바인딩)는 선택적Label/Selector를 통해 제어될 수 있다. 특정 환경(environment=production)용 PV와 일반 환경용 PV를 분리하여, 사용자의 PVC가 적절한 PV에 바인딩되도록 할 수 있다. 또한 `accessModes`는 스토리지의 사용 방식을指定한다. `ReadWriteOnce(RWO)`는 단일 노드에서만 읽기/쓰기가 가능하여 대부분의 블록 스토리지(AWS EBS, Azure Disk)에서 사용되고, `ReadWriteMany(RWX)`는 여러 노드에서 동시 읽기/쓰기가 가능하여 NFS, CephFS 같은 파일 스토리지에서 사용된다.

```text
[Static vs Dynamic Provisioning]
┌─────────────────────────────────────────────────────────────────────────┐
│ Static Provisioning (관리자 사전 프로비저닝)                              │
│ ─────────────────────────────────────────────────────────────────────── │
│ 1. 관리자가 PV 3개 생성 (storage: 10Gi, 20Gi, 30Gi)                     │
│ 2. 사용자: PVC 요청 (storage: 15Gi)                                      │
│ 3. 시스템: 적합한 PV(20Gi) 선택 → Binding                               │
│                                                                       │
│ Dynamic Provisioning (StorageClass 기반 자동 생성)                      │
│ ─────────────────────────────────────────────────────────────────────── │
│ 1. 관리자: StorageClass "fast-ssd" 생성 (AWS EBS gp3 프로비저너)         │
│ 2. 사용자: PVC 요청 (storageClassName: "fast-ssd", storage: 50Gi)      │
│ 3. 시스템: "fast-ssd" 프로비저너가 AWS EBS 50Gi 자동 생성 → PV 자동 Binding │
└─────────────────────────────────────────────────────────────────────────┘
```

스토리지의 수명 주기는 PVC가 삭제될 때 결정된다. PVC의 `persistentVolumeReclaimPolicy`는 `Retain`(유지), `Delete`(삭제), `Recycle`(재사용) 중 하나를指定할 수 있다. `Retain`은 PVC가 삭제되어도 PV와 데이터가 유지되어 다른 사용자가 볼 수 있고, `Delete`는 PV와 실제 스토리지 볼륨이 함께 삭제되며, `Recycle`은 데이터 삭제 후 PV를 재사용 가능한 상태로 만든다. Production 환경에서는通常(통상) `Retain` 정책이 권장되며, `Delete`는 실수에 의한 데이터 손실을유발할 수 있다.

📢 **섹션 요약 비유**: PV/PVC의 관계는 미술관寄存 시스템과 같습니다. PV는 미술품 보존 캐비닛(창고)이고, PVC는 미술품 인수 ticket입니다. visitor(사용자)가 ticket을 제시하면(claim) 가장 적당한 크기의 캐비닛이割り当てられ(할당), 미술품을保管합니다. ticket을 반납하면(삭제) 대부분의 경우 캐비닛은 유지(Retain)되어 다른 미술품이 사용할 수 있습니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

쿠버네티스 스토리지의 다양한 유형은 각기 다른 사용 시나리오에 맞춰져 있다. **로컬 임시 스토리지(local ephemeral)**는 노드-local SSD와 같은高速 스토리지를使用하여 성능이 중요한 임시 캐시나logs에 적합하지만, 노드故障 시 데이터가 손실될 수 있다. **네트워크 스토리지(Network Storage)**는 NFS, AWS EFS, Azure Files 등으로,複数(복수) 노드에서 동시에 접근해야 하는 경우에 적합하지만, 네트워크 지연이 존재한다. **블록 스토리지(Block Storage)**는 AWS EBS, Azure Disk, GCP PD 등으로, 단일 노드에서高性能 읽기/쓰기가 필요한 데이터베이스 등에 적합하다.

| 스토리지 유형 | 예시 | accessMode | 성능 | 적합한 용도 |
|:---|:---|:---|:---|:---|
| 블록 스토리지 | AWS EBS, Azure Disk | RWO | 높음 | DB, 원시 로그 |
| 파일 스토리지 | AWS EFS, NFS, Azure Files | RWX, ROX | 중간 | 공유 파일시스템 |
| 오브젝트 스토리지 | AWS S3, GCS | N/A (API) | 낮음 | 백업, 아카이브, 데이터 레이크 |
| 로컬 SSD | hostPath, local PV | RWO | 가장 높음 | Temporary 캐시, temporary logs |

**StatefulSet과 스토리지의 조합**은 쿠버네티스에서 상태 저장형 애플리케이션을管理하는 핵심 방식이다. StatefulSet은 파드에 순서 있는 이름(ordinal index: nginx-0, nginx-1)을부여하고, 각 파드에 개별 PV를 マッピング한다. 파드가 삭제되어도 동일한 PV에 재마운트되어 데이터가 유지되며, 스케일 업/다운 시 순서가 적용되어 데이터의 일관성이担保된다. 이 특성은 Kafka의 브로커, etcd의 멤버, PostgreSQL의 레플리카 등에서 필수적이다.

```text
[StatefulSet과 PV/PVC 관계]
┌─────────────────────────────────────────────────────────────────────────┐
│  StatefulSet: web-server (replicas: 3)                                   │
│  ┌────────────────┬────────────────┬────────────────┐                     │
│  │   web-server-0 │   web-server-1 │   web-server-2 │                     │
│  │   └─ PVC: data-web-server-0 │  └─ PVC: data-web-server-1 │  └─ PVC: data-web-server-2 │   │
│  │       └─ PV: ebs-0           │      └─ PV: ebs-1           │      └─ PV: ebs-2           │   │
│  └────────────────┴────────────────┴────────────────┘                     │
│                                                                       │
│  특징:                                                                  │
│  - 파드 이름: 순서대로 (web-server-0, -1, -2)                           │
│  - PV 바인딩: 파드 특정 (web-server-0 → ebs-0 영구)                      │
│  - 스케일 다운: ordinal 큰 순서대로 삭제 (2 → 1 → 0)                   │
│  - 스케일 업: ordinal 작은 순서대로 생성 (0 → 1 → 2)                    │
└─────────────────────────────────────────────────────────────────────────┘
```

**CSI(Container Storage Interface)**는 쿠버네티스에서 다양한 스토리지 백엔드를Plugin 형태로 연결하는 표준 인터페이스이다. CSI 도입 이전에는 각 스토리지 벤더가 쿠버네티스 내부 코드에Plugin을 추가해야 했지만, CSI 도입 이후에는 외부Plugin으로提供되어 벤더들이 독립적으로Plugin을 개발하고 배포할 수 있게 되었다. AWS EBS CSI Driver, Azure Disk CSI Driver, Ceph CSI Driver, NFS CSI Driver 등이 대표적인 예이며, 클라우드 환경에서는 대체로 각 CSP(Cloud Service Provider)에서 제공하는 공식 CSI Driver를 사용한다.

📢 **섹션 요약 비유**: CSI는 만물창자의万能 콘센트 어댑터와 같습니다. 각기 다른 모양의 플러그(스토리지 백엔드: EBS, Azure, NFS)를同一(동일)한 규격의 어댑터(CSI)를 통해 쿠버네티스(콘센트)에 연결하면, 어떤 스토리지도 unified 방식으로 작동합니다. 그래서 새로운 스토리지 기계를 사고 싶으면 해당 어댑터(CSI Driver)만 설치하면 됩니다.

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

스토리지를 실무에 적용할 때는 다음要点을 반드시 고려해야 한다. First, **스토리지 클래스의 선택**이 중요하다. AWS EBS는 `gp2`(범용 SSD), `gp3`(新一代 범용 SSD), `io1`(IOPS 최적화 SSD), `st1`(처리량 최적화 HDD) 등 다양한 클래스를提供하며, 각각 가격과 성능 특성이 다르다. 데이터베이스에는 `io1` 또는 `gp3`를,ログ에는 `st1`을 선택하는 것이 좋다. Second, **Snapshot과 백업**을 반드시 구성해야 한다. PV/PVC의 데이터는 스토리지层面上(层面)에서障害(장애)에취약하며, Velero 같은 도구를 사용한 Periodic 백업이 필수이다.

스토리지 성능 문제도 중요하다. 스토리지의 **IOPS(Input/Output Operations Per Second)**와 **처리량(Throughput)**은 애플리케이션 성능에 직접적 영향을 미친다. 프로비저닝된 IOPS(P_IOPS)를 지원하는 스토리지(AWS io1, io2)를使用하면 일관된 성능을担保할 수 있다. 또한 **레이턴시(지연 시간)**도 고려해야 하며, 특히 분산 시스템에서 스토리지 레이턴시가 증가하면 전체 시스템 처리량이低下될 수 있다.

```text
[Production 스토리지 安全运营 체크리스트]
1. 스토리지 클래스 선택
   ├─ DB/ transaction: io1/io2 (프로비저닝된 IOPS)
   ├─ 일반アプリ: gp3 (가성비 SSD)
   ├─ 로그/아카이브: st1 (저렴한 HDD)
   └─ 공유 파일시스템: EFS/GlusterFS (RWX)

2. 데이터 보호
   ├─ PVC 백업: Velero + Restic (주기적 스냅샷)
   ├─ 복구 테스트: Quarterly 복구演练
   ├─ Reclaim Policy: "Retain" (잘못된 삭제 방지)
   └─ 스토리지 인크립션: KMS 키 활용 (데이터 암호화)

3. 성능 관리
   ├─ IOPS/처리량 요구량 산정 (애플리케이션 특성 기반)
   ├─ 프로비저닝된 IOPS 사용 시: 필요한 IOPS 예측
   ├─ 모니터링: 스토리지 레이턴시, IOPS 사용률
   └─ 스토리지 병목 감지: Prometheus + node_exporter

4. 고가용성
   ├─ DB: 다중 AZ에 파드 배치 (내구성 확보)
   ├─ 레플리카: 동기 복제 구성 (RPO 0)
   └─ 장애 대비:定期的な(정기적인) 백업 및 복구演练
```

또한 **스토리지 모니터링**을 반드시 설정해야 한다. AWS EBS의 경우 CloudWatch를 통해 IOPS, 처리량, 디스크 대기 시간 등을 모니터링할 수 있으며, Grafana 대시보드로可视化하면異常(이상)을 빠르게 탐지할 수 있다. 특히 데이터베이스 파드가 Pending 상태로 전환되는 것은 часто(자주) 스토리지 프로비저닝 한계에 도달했기 때문이며, 이를 사전에 탐지하여 프로비저닝을 늘려야 한다.

📢 **섹션 요약 비유**: 스토리지 안전 운영은 미술관의 작품 보존 시스템과 같습니다. 작품(PV/PVC)에 손상이 가지 않도록 온도/습도 조절(모니터링)을 상시 하고, 불재앙(장애)에 대비해 보험 가입(백업)을 하며, 작품이老朽화(노후화)되면 새 작품으로 교체(스토리지 업그레이드)하는 것이 필요합니다. 특히 무价值的(가치 없는) 작품은 미리 정리(스토리지 정리)하여 공간을 확보해야 합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)

쿠버네티스 스토리지 모델을 제대로 활용하면, 상태 저장형 애플리케이션도 Kubernetes Native하게管理할 수 있어 Hybrid Cloud 또는 Multi-Cloud 환경에서도 일관된 스토리지 운영이 가능하다. CSI를 통한 표준화는 Vendor Lock-in을 방지하고, Dynamic Provisioning은 스토리지 프로비저닝 시간을 数日から(수일에서) 수 분으로 단축시킨다. 또한 StatefulSet과 PV/PVC의 조합은 복잡한 데이터 관리 작업을抽象화하여, 개발팀이 비즈니스 로직에 집중할 수 있게 한다.

| 기대 효과 | 도입 전 | 도입後 | 효과 |
|:---|:---|:---|:---|
| 스토리지 프로비저닝 시간 | 수 일 (스토리지 팀 요청) | 수 분 (Dynamic Provisioning) | 99% 단축 |
| 스토리지 운영 복잡도 | 스토리지 팀 별도 관리 | 쿠버네티스에서 통합 관리 | 70% 감소 |
| 데이터 보호 수준 | 수동 백업 | 자동 스냅샷 + Velero | 90% 향상 |
| 스토리지 이식성 | 벤더 종속 | CSI 표준으로 자유로운 이동 | 완전 해방 |

미래에는 Kubernetes의 스토리지 기능이 더욱 발전하여, Ephemeral Volume의 역할이明確化되고, Local PV의 스케줄링 지원이 개선되며, CSI-drivers의 품질と 범위가扩大될 것이다. 또한 storage abstraction_LAYER가 더욱 높아져서 사용자가 백엔드 스토리지의 종류를 몰라도 되는 Raw Block Device 지원이나, 분산 파일시스템과의更深(더 깊은)集成が期待されている。결론적으로, 쿠버네티스 스토리지/볼륨 모델은 클라우드 네이티브 환경에서 상태 저장형 애플리케이션을管理하기 위한 필수 인프라이며, PV/PVC 추상화와 CSI 표준을 통해 확장 가능하고 이식 가능한 스토리지 관리 체계를 제공한다.

📢 **섹션 요약 비유**: 쿠버네티스 스토리지는 미래 도시의 수도 및 하수 시스템과 같습니다. 모든 가정(파드)에 수도관(PV/PVC)을 통해 물(데이터)을 전달하고, 각 가정에서는 물을 받아 활용합니다. 수도관이 노후화(스토리지劣化)되면 새로운 관(새 스토리지)로 교체하고, 단지는(물이 새면) 복구하고(백업), 시스템 전체는 중앙 감시실(쿠버네티스)에서 모니터링합니다. 이렇게 하면 시민(개발자)은 물이 어디서 오는지 신경 쓰지 않고 자신의 일(비즈니스 로직)에만 집중할 수 있습니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- PersistentVolume (PV) | 파드와 독립적으로 존재하는 클러스터 레벨 스토리지 리소스
- PersistentVolumeClaim (PVC) | 사용자가 PV를 요청하는 명세 (네임스페이스 레벨)
- StorageClass | Dynamic Provisioning을 위한 스토리지 프로비저너를定義する
- CSI (Container Storage Interface) | 쿠버네티스에서 다양한 스토리지 백엔드를Plugin 형태로 연결하는 표준
- StatefulSet | 순서 있는 배포와 고유한 네트워크 식별자를 제공하는 상태 저장 워크로드용 오브젝트

### 👶 어린이를 위한 3줄 비유 설명
1. 쿠버네티스에서 컨테이너는 스티커 메모장과 같아요. 메모지를 쓰고 나면 메모지는 사라져요.
2. 그래서 중요한 그림(데이터)을 그리려면 반드시 별도의 도화지(PV/PVC)를 구해서 스티커에 붙여야 해요.
3. 이 도화지는 어떤 색상/크기(스토리지 백엔드)가 와도 상관없어요. 쿠버네티스가 알아서 잘 붙여줘요!
