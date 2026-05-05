+++
weight = 25
title = "25. SDS (Software Defined Storage) — 소프트웨어 정의 스토리지"
date = "2026-04-29"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: SDS (Software Defined Storage, 소프트웨어 정의 스토리지)는 스토리지 하드웨어(HDD, SSD, NVMe)와 제어 소프트웨어를 분리(Disaggregation)하여, 이기종 하드웨어를 추상화하고 단일 API로 제어하는 스토리지 아키텍처다.
> **비유**: 복잡한 시스템을 작은 운영 규칙으로 정리해 안정적으로 굴러가게 만드는 교통 관제 체계와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

전통적 스토리지는 하드웨어+소프트웨어가 단일 어플라이언스로 통합되어, 벤더 종속, 고비용, 수직적 확장(Scale-up) 한계를 가졌다.

```text
┌───────────────────────────────────────────────────────────┐
│         SDS 핵심 아키텍처                                   │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  [앱 계층]    K8s PVC / NFS / S3 API / Block API          │
│       │                                                   │
│  [SDS 계층]   Ceph / GlusterFS / vSAN / Longhorn          │
│       │       (데이터 배치, 복제, 복구, 티어링)             │
│       │                                                   │
│  [물리 계층]   x86 서버 + HDD / SSD / NVMe                 │
│               (이기종 하드웨어 추상화)                      │
└───────────────────────────────────────────────────────────┘
```

SDS의 3가지 스토리지 서비스:
- **블록 스토리지(Block)**: 데이터베이스, VM 디스크
- **파일 스토리지(File)**: NFS/SMB, 공유 파일시스템
- **오브젝트 스토리지(Object)**: S3 호환, 대규모 비정형 데이터

---

## 2. 구성요소

### Ceph — 오픈소스 SDS 레퍼런스 아키텍처

```text
┌────────────────────────────────────────────────────────────┐
│                  Ceph 아키텍처                               │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  [클라이언트]                                               │
│  librados / S3 API / RBD / CephFS                         │
│       │                                                    │
│  [RADOS (Reliable Autonomic Distributed Object Store)]    │
│  MON (모니터) - 클러스터 상태 관리                          │
│  OSD (Object Storage Daemon) - 실제 데이터 저장·복제        │
│  MGR (Manager) - 메트릭, 대시보드                           │
│  MDS (Metadata Server) - CephFS 파일 메타데이터             │
│       │                                                    │
│  [CRUSH 알고리즘] - 데이터 배치 결정 (중앙 조회 없이)        │
└────────────────────────────────────────────────────────────┘
```

### K8s CSI 기반 동적 프로비저닝

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ceph-rbd
provisioner: rbd.csi.ceph.com
parameters:
  pool: kubernetes
reclaimPolicy: Delete
volumeBindingMode: Immediate
# PVC 생성 시 자동으로 Ceph에서 볼륨 할당
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
spec:
  storageClassName: ceph-rbd
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 100Gi
```

---

## 3. 구조 및 원리

**핵심 조건**: 자원 추상화, 격리 수준, 자동 프로비저닝, 보안 경계, 비용 통제가 함께 설계되어야 안정적인 서비스 가치가 나온다.

동작 순서:
1. 요구사항과 책임 경계를 먼저 정의한다.
2. 추상화 계층에서 컴퓨팅·스토리지·네트워크 자원을 논리적으로 분리하고 격리 수준을 결정한다.
3. 제어 평면이 정책에 맞는 자원을 프로비저닝하고 서비스 모델에 따라 사용자에게 노출한다.
4. 운영 중에는 확장, 가용성, 백업, 보안 정책을 지속적으로 적용해 상태를 안정화한다.
5. 마지막으로 비용·성능·벤더 종속성을 함께 평가해 구조를 최적화한다.

| 항목 | 전통 SAN/NAS | SDS (Ceph/vSAN) |
|:---|:---|:---|
| **확장 방식** | Scale-up (고가 어플라이언스 교체) | Scale-out (노드 추가) |
| **벤더 종속** | 높음 (EMC, NetApp 전용) | 낮음 (x86 범용 하드웨어) |
| **비용** | 높음 (라이선스+HW) | 낮음 (OSS + COTS) |
| **API** | 벤더별 상이 | S3, CSI 표준 API |

---

## 4. 비교 및 연결

### 실무 시나리오: 공공 클라우드 SDS 구축 (Ceph + OpenStack)
1. 상용 스토리지 어플라이언스(EMC) 교체 → x86 서버 30대 + Ceph 구축.
2. 비용: 어플라이언스 3억 → x86+Ceph 8,000만원 (73% 절감).
3. 성능: IOPS 30% 향상 (NVMe OSD 노드 활용).
4. 가용성: 3-way 복제 + Ceph 자동 복구 → 노드 장애 시 5분 내 자동 재균형.

### 안티패턴
- 단순 비용 절감만 보고 SDS를 도입했으나 운영 전문성 부족으로 장애 대응 실패. SDS는 소프트웨어 복잡성(CRUSH 알고리즘 이해, OSD 튜닝, 모니터 정족수 관리)이 높아, 전문 교육 없이 도입하면 전통 어플라이언스보다 운영 비용이 더 높아진다.

---

## 5. 실무 적용 및 판단

| 기대효과 | 내용 |
|:---|:---|
| **비용 절감** | 상용 어플라이언스 대비 60~75% 절감 |
| **유연한 확장** | 노드 추가로 페타바이트 선형 확장 |
| **표준 API** | S3, CSI로 클라우드 네이티브 통합 |

SDS는 Hyperconverged Infrastructure (HCI, 하이퍼컨버지드 인프라)로 발전하여 컴퓨팅·스토리지·네트워킹을 단일 소프트웨어 스택으로 통합(예: Nutanix, VMware vSAN)하고 있다. 컨테이너 스토리지(Longhorn, Rook-Ceph)는 K8s 네이티브 SDS의 표준으로 자리잡았다.

---

## 6. 기대효과 및 결론

SDS (Software Defined Storage) — 소프트웨어 정의 스토리지를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 SDS (Software Defined Storage) — 소프트웨어 정의 스토리지의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
[전통 SAN/NAS — 전용 어플라이언스, 벤더 종속]
    │
    ▼
[SDS (Ceph/GlusterFS) — 상용 HW + 소프트웨어 분리]
    │
    ▼
[K8s CSI 통합 — 컨테이너 네이티브 동적 프로비저닝]
    │
    ▼
[HCI (Nutanix/vSAN) — 컴퓨팅+스토리지+네트워크 통합]
    │
    ▼
[AI 기반 스토리지 자동화 — 데이터 티어링, 이상 탐지]
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| **SDDC** | SDS는 SDDC의 스토리지 레이어 |
| **Ceph** | 오픈소스 SDS 사실상 표준 |
| **K8s CSI** | 컨테이너 환경 SDS 연동 표준 |
| **HCI** | 컴퓨팅+스토리지+네트워크 통합 SDS |
| **S3 API** | SDS 오브젝트 스토리지 표준 인터페이스 |

---
