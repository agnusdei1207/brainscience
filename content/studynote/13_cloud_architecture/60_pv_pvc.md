+++
weight = 60
title = "60. PV/PVC"
date = "2026-04-05"
[taxonomies]
tags = ["Cloud", "Kubernetes", "K8s", "PV", "PVC", "PersistentVolume"]
categories = ["13_cloud_architecture"]
+++

# PV/PVC

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: PersistentVolume(PV)은 클러스터 전체에서 관리되는 영구 스토리지의 물리적 또는 논리적 표현이며, PersistentVolumeClaim(PVC)은 네임스페이스 레벨에서 PV를 요청하는 개발자의 요구 명세이다.
> 2. **가치**: 이 추상화 계층은 스토리지의 프로비저닝 방법(내부/외부, AWS/GCP/Azure)과 사용 방법을 분리하여, 개발자가 백엔드 스토리지 세부 사항을 몰라도 스토리지를 사용할 수 있게 한다.
> 3. **융합**: PV/PVC는 StatefulSet과 함께 사용되어 데이터베이스, 메시지 큐 등 상태 저장형 워크로드에 필수적인 영속성(Persistence)과 순서 있는 배치를 제공한다.

---

### Ⅰ. 개요 및 필요성 (Context & Necessity)

쿠버네티스 환경에서 컨테이너는 기본적으로 Stateless하게 설계된다. 컨테이너 내부에서 생성된 모든 데이터는 컨테이너가 삭제될 때 함께 사라진다. 그러나 현실의 애플리케이션은データを保存해야 할 필요가 항상 존재한다. 데이터베이스는 영구적으로 데이터를 저장해야 하고, 메시지 큐는 처리되지 않은 메시지를 장애 상황에서도 유지해야 하며, 로그 수집기는 수집된 로그를 다른 시스템으로 전송하기 전까지 유지해야 한다. 이러한需求的背景下(배경)에서 PersistentVolume(PV)과 PersistentVolumeClaim(PVC)이 탄생했다.

PV/PVC 이전에는 개발자가 직접 스토리지 백엔드의 세부 정보(AWS EBS 볼륨 ID, NFS 서버 주소, Ceph 클러스터 자격 증명 등)를 애플리케이션 설정에 기재해야 했다. 이는 개발 환경과 운영 환경 간의 설정 불일치를 유발하고, 스토리지 백엔드를 변경할 때 애플리케이션 코드 수정을 필요로 했다. PV/PVC는 스토리지의 **"제공자(Provider)"**와 **"소비자(Consumer)"**를 분리하는 추상화 계층을提供하여, 관리자는ストレージインフラ(스토리지 인프라)를管理하고,開発者は只需指定する(지정하기만 하면) 하면 된다.

```text
[스토리지 제공자와 소비자의 분리]
┌─────────────────────────────────────────────────────────────────────────────┐
│                     管理者的(관리자) 영역                                         │
│  ────────────────────────────────────────────────────────────────────────── │
│  1. 스토리지 인프라 준비                                                        │
│     - AWS: EBS 볼륨, EFS 파일 시스템 프로비저닝                                │
│     - On-Premise: NFS 서버, Ceph 클러스터 구성                                │
│                                                                       │
│  2. StorageClass 생성 (Dynamic Provisioning 용)                          │
│     apiVersion: storage.k8s.io/v1                                        │
│     kind: StorageClass                                                   │
│     metadata:                                                             │
│       name: fast-storage                                                 │
│     provisioner: kubernetes.io/aws-ebs                                   │
│     parameters:                                                          │
│       type: gp3                                                           │
│     volumeBindingMode: WaitForFirstConsumer                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ "스토리지 요청"
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     開発者的(개발자) 영역                                         │
│  ────────────────────────────────────────────────────────────────────────── │
│  3. PVC 작성 (스토리지 요구만 기재)                                           │
│     apiVersion: v1                                                        │
│     kind: PersistentVolumeClaim                                           │
│     spec:                                                                 │
│       accessModes: [ReadWriteOnce]                                        │
│       resources:                                                          │
│         requests:                                                         │
│           storage: 20Gi                                                   │
│       storageClassName: fast-storage                                      │
│                                                                       │
│  4.Deployment에서 PVC 참조                                                  │
│     volumes:                                                              │
│       - name: data                                                       │
│         persistentVolumeClaim:                                            │
│           claimName: my-database-pvc                                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

이 구조의 핵심은 **관심사의 분리(Separation of Concerns)**이다. 인프라 관리자는 스토리지 백엔드를 설정하고 StorageClass를作成就知道(만들어就知道) 하면 되고, 개발자는 필요한 용량(accessModes, storage 크기)만 PVC에 기재하면 된다. 스토리지 백엔드가 변경되더라도(예: AWS EBS에서 Azure Disk로 마이그레이션) PVC 설정은 변경되지 않으며, 관리자가 해당 StorageClass만 업데이트하면 된다.

📢 **섹션 요약 비유**: PV/PVC는 항구 화물 창고システムと一样(시스템과 같다). 창고 관리자(관리자)는 크레인과 창고(스토리지 백엔드)를 관리하고, 화물 주선인(개발자)은 화물을保管하기 위해 창고에 원하는 크기의 공간(용량)을 요청할 뿐입니다. 크레인이 전동식에서 디젤식으로 바뀌어도(스토리지 백엔드 변경), 화물 주선인은 공간 요청 방식만 알면 됩니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**PersistentVolume(PV)**은 클러스터 레벨의 리소스이며, 특정 네임스페이스에 속하지 않는다. PV는 관리자가 수동으로作成하는 **Static PV**와, StorageClass를 통해 동적으로 생성되는 **Dynamic PV**로 구분된다. Static PV는 관리자가 물리적 스토리지를事前プロビジョ닝하고 그에 맞는 PV를作成하며, Dynamic PV는 사용자의 PVC 요청을Intercept하여 시스템이 자동으로 스토리지를 프로비저닝한 후 PV를作成한다.

PV의 핵심 속성은 다음과 같다. **Capacity**는 PV의 크기(예: 100Gi)를 나타낸다. **AccessModes**는 스토리지의 사용 방식을指定하며, `ReadWriteOnce(RWO)`는 단일 노드에서만 읽기/쓰기를 허용하고, `ReadOnlyMany(ROX)`는 다수 노드에서 읽기 전용으로 마운트 가능하며, `ReadWriteMany(RWX)`는 다수 노드에서 동시에 읽기/쓰기를 허용한다. **PersistentVolumeReclaimPolicy**는 PVC가 삭제된 후 PV의 데이터를 어떻게 처리할지를 결정하며, `Retain`(유지), `Delete`(스토리지와 함께 삭제), `Recycle`(데이터 삭제 후 재사용) 세 가지 옵션이 있다. **StorageClassName**은 어떤 StorageClass를 통해 프로비저닝되었는지를 나타낸다.

**PersistentVolumeClaim(PVC)**은 네임스페이스 레벨의 리소스로, 개발자가 PV를 요청하는 명세이다. PVC의 핵심 속성은 PV와 대응된다. **Selector**를 통해 특정 레이블을 가진 PV만 선택하도록指定할 수 있으며, **VolumeName**으로 특정 PV에 직접 바인딩될 수도 있다. PVC가 요청되면 쿠버네티스는 사용 가능한 PV 중 조건에 맞는 것을 찾아 바인딩한다. 바인딩되면 PVC는 해당 PV에 1:1로 매핑되며, 다른 PVC가 이미 바인딩된 PV에 重複して(중복해서) 바인딩될 수는 없다.

```yaml
# PersistentVolume 예시 (Static Provisioning)
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-database
  labels:
    type: fast
    environment: production
spec:
  capacity:
    storage: 100Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: standard
  awsElasticBlockStore:
    volumeID: "vol-0a1b2c3d4e5f6g7h8"
    fsType: ext4
```

```yaml
# PersistentVolumeClaim 예시
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: database-pvc
  namespace: production
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
  storageClassName: standard
  selector:
    matchLabels:
      environment: production
```

 PV와 PVC의 **바인딩 과정**은 다음 순서로 진행된다. First, 사용자가 PVC를作成就知道(생성就知道). Second, PVC Controller(또는 Volume Controller)가 사용 가능한 PV를 탐색한다. Third, 조건에 맞는 PV가 있으면 바인딩하고, 없으면 PVC를 Pending 상태로 둔다. Fourth, Dynamic Provisioning이 가능한 StorageClass이면 해당 프로비저너가 새로운 PV를 생성한 후 바인딩한다. Fifth, 파드에서 PVC를 참조하면 쿠버네티스는 PV를 파드에 마운트한다.

PV의 라이프사이클은 "Available → Bound → Released → Recycled/Retained/Deleted"로 구분된다. PVC가 삭제되면 PV는 "Released" 상태가 되며, ReclaimPolicy에 따라 "Retain"(데이터 유지, 수동 정리 필요), "Delete"(스토리지와 PV 자체 자동 삭제), "Recycle"(데이터 삭제 후 "Available" 상태로 복귀) 중 하나가 적용된다.

📢 **섹션 요약 비유**: PV의 라이프사이클은Rental(렌탈) 시스템과 같습니다. 창고(PV)가 Available(사용 가능) 상태에서 Someone(누군가)가 계약하면(바인딩) Bound(사용 중) 상태가 되고, 계약이 끝나면(해지) Released(반납) 상태가 됩니다. 이때 창고에 물건이 남아 있으면 Retain(보관) 상태로 두어 수동 정리하고, 창고 규정에 따라 물건을 비우고 새 계약자を受け入れる(받는다) 것이 Recycle, 창고 자체를拆卸(철거)하는 것이 Delete입니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

PV/PVC와 StatefulSet의 조합은 상태 저장형 애플리케이션(데이터베이스, 메시지 큐 등)을 쿠버네티스에서管理하는 핵심 패턴이다. StatefulSet은 각 파드에 순서 있는 이름(ordinal)을 부여하고, 각 파드에 개별 PV/PVC를 マッピング한다. 이로 인해 파드가 삭제 후 재시작되어도 동일한 PV에 재마운트되어 데이터가 유지된다. 또한 StatefulSet의 스케일 업/다운은 순서대로 진행되어 데이터의 일관성이担保된다.

| 비교 항목 | Deployment + Volume | StatefulSet + PVC |
|:---|:---|:---|
| 파드 식별 | 랜덤 해시 (web-5c9d7f8b5b-xvw2m) | 순서 인덱스 (web-0, web-1) |
| 스토리지 | 공유 볼륨 (여러 파드가同一 볼륨) | 개별 볼륨 (파드별 고유 PVC) |
| 스케일링 |任何 파드(any pod)가any 볼륨(any volume) | 파드-볼륨 1:1 매핑 |
| 장애 복구 | 새로운 파드가 어떤 볼륨이든 마운트 | 새로운 파드가 동일 볼륨에 재마운트 |
| 적합한 경우 | Stateless 웹 앱, 캐시 | DB, 레플리카셋, 메시지 큐 |

**StorageClass와 Dynamic Provisioning**의 조합은 PV/PVC의 강력한 활용 사례이다. 관리자가 StorageClass를 생성하면, 사용자가 PVC로 스토리지를 요청할 때마다 시스템이 자동으로 스토리지를 프로비저닝한다. 이로 인해 관리자는 스토리지 프로비저닝에 대한 수동 개입 없이도 온전히 스토리지를 사용할 수 있다. AWS, GCP, Azure 같은 주요 클라우드에서는 다양한 유형의 스토리지를 StorageClass로 제공하며, 이를테면 `standard`, `fast`, `Archive` 등의 이름으로 구분된다.

```yaml
# AWS EBS용 StorageClass 예시
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ebs
provisioner: ebs.csi.aws.com   # AWS EBS CSI Driver
parameters:
  type: gp3                      # SSD 타입
  iops: "3000"                   # IOPS 설정
  throughput: "125"              # 처리량 (MiB/s)
volumeBindingMode: WaitForFirstConsumer  # 파드 스케줄링 후 볼륨 바인딩
allowVolumeExpansion: true       # 볼륨 용량 확장 허용
reclaimPolicy: Retain            # PVC 삭제 시 PV 유지
```

**Local PV와 노드 어피니티**의 조합은 고성능 스토리지가 필요한 경우に如何使用(어떻게 사용되는지)를 보여준다. Local PV는 노드의 로컬 디스크를 PV로 사용하며, 데이터의 지역성(지역성)으로 인해 높은 IOPS와 낮은 레이턴시를 제공한다. 그러나 노드 장애 시 데이터가 손실될 수 있으므로, 반드시レプリ카와 함께 사용해야 한다. Local PV는 `volumeBindingMode: WaitForFirstConsumer`로 설정하여 파드가 특정 노드에 스케줄링된 후 볼륨을 바인딩하며, 노드 어피니티와 함께 사용하여 파드가 PV가 있는 노드에正確に(정확하게) 배치되도록 보장한다.

📢 **섹션 요약 비유**: Local PV는 각 가정에 설치된 가정용 창고와 같습니다. 가정에 가까운 곳에 있어 화물을出し入れ(出し入れ)하기 편리하고(낮은 레이턴시), 각 가정에1대1로 연결되어 있습니다(노드 어피니티). 그러나 만약 건물이 붕괴되면(노드 장애) 창고도 함께埋没됩니다(데이터 손실). 그래서非常重要的(매우 중요한) 물건은 반드시 다른 장소にもコピー(복사)를保管해야 합니다(레플리카).

### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

Production 환경에서 PV/PVC를 사용할 때는 다음要点을 반드시 고려해야 한다. First, **ReclaimPolicy는 반드시 "Retain"으로 설정**해야 한다. "Delete" 정책은 PVC를 삭제할 때 PV와 실제 스토리지가 자동으로 삭제되어, 실수에 의한 데이터 손실을유발할 수 있다. Production에서는 데이터의安全이最優先(가장 우선)이므로 "Retain"으로 설정하고, 필요한 경우 관리자가 수동으로 정리하는 것이 安全である。

Second, **Volume Expansion** 기능을 활성화하면 스토리지 용량 부족 시 PVC만更新하여 볼륨을 확장할 수 있다. Kubernetes 1.24 이상에서는 대부분의 CSI Driver가オンライン擴張(온라인 확장)을 지원하며, 파드를 재시작하지 않고도 볼륨을 확장할 수 있다. 그러나 확장된 용량을 파일시스템에서 사용하려면 애플리케이션이 해당 변경을感知해야 하는 경우도 있다.

```text
[Production PV/PVC 安全运营 체크리스트]
1. ReclaimPolicy 관리
   ├─ Production: reclaimPolicy: "Retain" (데이터 유지)
   ├─ Development: reclaimPolicy: "Delete" (자동 정리)
   └─ Periodic 감사: Abandoned PV (Orphaned) 탐지 및 정리

2. 스토리지 용량 관리
   ├─ 볼륨 확장: allowVolumeExpansion: true 설정
   ├─ 용량 모니터링: 80% 임계치 초과 시 Alert
   ├─ 초기 용량 산정: 예상 성장률 기반 충분한 용량 확보
   └─ 비용 관리: 불필요하게 큰 볼륨 프로비저닝 방지

3. 데이터 보호
   ├─ Snapshot: CSI Snapshot 기능을活用した Periodic 백업
   ├─ 복구演练: Quarterly 복구 테스트
   ├─ 지역성(Regulatory) 준수: 데이터 위치에 따른 스토리지 선택
   └─ 암호화: KMS를 통한 데이터 암호화 (保存中 및 전송 중)

4. 액세스 제어
   ├─ RBAC: PVC 생성 권한 통제 (namespace 별)
   ├─ ResourceQuota: PVC 수 및 총 스토리지 용량 제한
   └─ StorageClass 격리: 환경별(DEV/PROD) StorageClass 분리
```

또한 **ResourceQuota를 통한 스토리지 자원 제한**도 중요하다. 네임스페이스별로 PVC 수와 총 스토리지 용량을 제한하지 않으면, 한 팀이 너무 많은 PVC를 생성하여 클러스터 전체의 스토리지 자원을 소진할 수 있다. ResourceQuota를 설정하여 이러한 문제를 예방할 수 있다. 또한 정기적으로orphan PV(어떤 PVC에도 바인딩되지 않은 PV)를 감사하여 불필요한 스토리지 비용을 줄여야 한다.

📢 **섹션 요약 비유**: PV/PVC 실무를 지키는 것은 고급 레스토랑의 식재료 관리와 같습니다. 모든 식재료(PV)는 창고(스토리지 백엔드)에谁知道(알 수 있는) 곳에만 저장되고, Chef(개발자)가 필요할 때만 요청서(PVC)를 제출하여 식재료를 전달받습니다. 식재료가 experimental(실험적으로) 사용 후 방치되어 폐기되지 않으면(Orphaned PV), 냉장고 비용(스토리지 비용)이 불필요하게 발생하는 것입니다. 그래서 주기적인 냉장고 정리(스토리지 감사)가 필요합니다.

### Ⅴ. 기대효과 및 결론 (Future & Standard)

PV/PVC 추상화를 활용하면 스토리지 인프라를より簡単に(더 쉽게)管理하고, 개발 생산성을 향상시킬 수 있다. 개발자는 스토리지 백엔드의 세부 사항을 몰라도 되고, 스토리지 팀과 별도로 협의 없이 필요한 스토리지를 요청할 수 있다. 또한 StorageClass를 통한 Dynamic Provisioning은 스토리지 프로비저닝의 속도를 数日から(수일에서) 수 초로 단축시킨다.

| 기대 효과 | 도입 전 | 도입後 | 효과 |
|:---|:---|:---|:---|
| 스토리지 프로비저닝 | 수 일 (스토리지 팀 협의) | 수 십 초 (Dynamic Provisioning) | 99% 단축 |
| 스토리지 이식성 | 스토리지 종류 변경 시 앱 수정 필요 | PVC 설정 불변 | 완전 추상화 |
| 개발 생산성 | 스토리지 세부 지식 필요 | 볼륨 요청만으로 사용 가능 | 80% 향상 |
| 인프라 제어 | 스토리지 팀이 모든 것을管理 | 관리자는 StorageClass로 정책 설정 | 70% 간소화 |

미래에는 PV/PVC 모델이 더욱 성숙하여, ROX/RWX|accessMode가 더 많은 스토리지 유형에서 지원될 것이며, CSI 기반의 고급 기능(Snapshot, Clone, Encryption)가 표준화될 것이다. 또한 분산 파일시스템(CephFS, GlusterFS)과 쿠버네티스의Integration이 더욱紧密해져서, 단일 스토리지 클러스터에서 수십 개의 클러스터에データを分散して(데이터를 분산해서)提供服务하는 것이 가능해질 것이다. 결론적으로, PV/PVC는 쿠버네티스에서 스토리지를管理하는 필수적인 추상화 계층이며, StatefulSet과 함께 사용되어 상태 저장형 애플리케이션의 영속성을担保하는 핵심 요소이다.

📢 **섹션 요약 비유**: PV/PVC는 미래 도시의Universal(범용) 물供紿(공급) 시스템과 같습니다. 수도 회사(스토리지 백엔드)는 수도관(스토리지 인프라)을管理하고, 시민(개발자)은 수도꼭지(볼륨)를 통해 물을 받습니다. 수도꼭지의 크기(용량)만 요청하면 되며, 수도관이 어떤 재질(스토리지 유형)이든 물은 동일한品質(품질)로 공급됩니다. 수도관이 낡아도 시민은 수도꼭지를 바꾸지 않아도 되며, 수도 회사만관을 교체하면 됩니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- PersistentVolume (PV) | 클러스터 레벨에서管理되는 영구 스토리지 리소스
- PersistentVolumeClaim (PVC) | 네임스페이스 레벨에서 PV를 요청하는 명세
- StorageClass | 스토리지 프로비저너의 종류와 정책을定義する
- Dynamic Provisioning | 사용자의 PVC 요청에 따라 시스템이 자동으로 PV를 프로비저닝
- StatefulSet | 순서 있는 파드 배기와 개별 PV/PVC를 제공하는 상태 저장 워크로드용 오브젝트

### 👶 어린이를 위한 3줄 비유 설명
1. PV는 항구에 있는大型 창고 상자예요. 각 상자마다 크기가 다르고, 열쇠(PV)가 있어요.
2. PVC는 창고에 물건을 넣고 싶은 사람이 작성하는 신청서예요. "100리터 크기의 상자가 필요해요"라고 써서 제출하면, 관리자가 맞는 상자를 선택해 줘요.
3. 한번 신청서가 받아들여지면(바인딩), 그 상자는 신청한 사람專門(전용)으로 사용되어, 다른 사람이 동시에 사용할 수 없어요.
