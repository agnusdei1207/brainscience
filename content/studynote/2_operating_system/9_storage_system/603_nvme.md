+++
title = "603. NVMe"
weight = 603
+++

# 603. NVMe (Non-Volatile Memory Express)
weight = 603
+++

# 603. NVMe (Non-Volatile Memory Express)
weight = 603
+++

# 603. NVMe (Non-Volatile Memory Express)
weight = 603
+++

# 603. NVMe (Non-Volatile Memory Express)
weight = 603
+++

# 603. NVMe (Non-Volatile Memory Express)

Non-Volatile Memory Express)**는 **PCI Express를 통해 SSD에 고속으로 접근하는 인터페이스**입니다.
### 💡 비유: 고속도로
NVMe는 **고속도로**와 같습니다. 12차선으로 초고속 이동합니다.
### NVMe 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                NVMe 구조                                             │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【NVMe 표준】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  표준              인터페이스        대역폭        속도            │ │   │
│  │  ────              ──────────    ────          ────            │ │   │
│  │  NVMe 1.0          PCIe 3.0 x4     4 lanes     1 GB/s        │ │   │
│  │  NVMe 1.1b         PCIe 3.0 x4     4 lanes     2 GB/s        │ │   │
│  │  NVMe 1.2          PCIe 3.0 x4     4 lanes     4 GB/s        │ │   │
│  │  NVMe 1.3          PCIe 3.0 x4     4 lanes     4 GB/s        │ │   │
│  │  NVMe 2.0          PCIe 4.0 x4     4 lanes     8 GB/s        │ │   │
│  │  NVMe 3.0          PCIe 4.0 x4     4 lanes     16 GB/s       │ │   │
│  │  NVMe 4.0          PCIe 4.0 x4     4 lanes     32 GB/s       │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【NVMe 아키텍처】                                                    │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  ┌──────────┐      ┌──────────┐      ┌──────────┐       │ │   │
│  │  │ App     │      │  Submission  │    │ Completion   │     │ │   │
│  │  │  큐     │      │  SQ           │    │ CQ            │     │ │   │
│  │  └──────────┘      └──────────┘      └──────────┘       │ │   │
│  │                                                             │ │   │
│  │  Submission Queue:                                              │ │   │
│  │  • 앱 -> SQ (Submission Queue)                                     │ │   │
│  │  • 최대 64,000개 엔트리 (NVMe 1.0/1.1)                             │ │   │
│  │  • 32개 엔트리 (NVMe 1.1b) / 16개 (NVMe 1.0/1.1b)                     │ │   │
│  │                                                             │ │   │
│  │  Completion Queue:                                                │ │   │
│  │  • CQ (Completion Queue)                                            │ │   │
│  │  • SQ 완료 후 CQ로 이동                            │ │   │
│  │                                                             │ │   │
│  │  Doorbell Register:                                                │ │   │
│  │  • MSI-X: 메시지 알림 (Doorbell)                               │ │   │
│  │  • 관리자 인터럽트 발생                               │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【NVMe vs SATA vs SAS】                                            │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  항목            SATA              SAS              NVMe            │ │   │
│  │  ────            ────              ────              ────            │ │   │
│  │  인터페이스       SATA              SAS              PCIe           │ │   │
│  │  속도            600 MB/s          640 MB/s         7.8 GB/s        │ │   │
│  │  프로토콜         ATA              SCSI             NVMe           │ │   │
│  │  지연 시간        높음              중간              매우 낮음          │ │   │
│  │  CPU 오버헤드     높음              높음              매우 낮음          │ │   │
│  │  병렬성           낮음              높음              매우 높음          │ │   │
│  │  핫 스왑          지원              지원              지원             │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅲ. 실무 적용
### 구현 예시
```
┌─────────────────────────────────────────────────────────────────────┐
│                실무 적용                                            │ |
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【NVMe 장치 확인】                                                    │
│  ──────────────────                                                │
│  // lsblk                                                            │
│  $ lsblk                                                             │
│  NAME        MAJ:MIN:RM   SIZE RO TYPE  MOUNTPOINT                  │
│  nvme0n1     259:0    disk                nvme                        │
│  nvme0n1p1   259:1    part                 nvme                        │
│  nvme0n1p2   259:2    part                 │
│                                                                     │
│  // nvme-cli                                                          │
│  $ sudo nvme list                                                    │
│  Node             SN               Model                 Namespace  Usage    │
│  ----------------- ----------------- --------------------  ------------       │
│  nvme0n1           SAMSUNG           SSD 970 EVO Plus        /dev/nvme0n1   1.69 TB      │
│                                                                     │
│  // SMART 정보                                                       │
│  $ sudo nvme smart-log /dev/nvme0n1                              │
│  Smart Log for NVME device:                                    │
│  critical_warning                  : 0                              │
│  temperature                        : 45 Celsius                      │
│  available_spare                    : 68                              │
│  percentage_used                    : 1%                              │
│  data_units_read                    : 32,044,131,328              │
│                                                                     │
│  // 컨트롤러 정보                                                       │
│  $ sudo nvme id-ctrl /dev/nvme0n1 --human-readable                      │
│  $ sudo nvme get-feature /dev/nvme0n1 -f 0 (Get all features)      │
│                                                                     │
│  【NVMe 성능 테스트】                                                 │
│  ──────────────────                                                │
│  // hdparm (일부 지원)                                              │
│  $ sudo hdparm -I /dev/nvme0n1                                         │
│                                                                     │
│  // fio (유연한 I/O)                                             │
│  $ sudo fio --name=randread --ioengine=libaio --filename=/dev/nvme0n1│
│                                                                     │
│  // io_uring (고성능)                                             │
│  $ sudo apt install liburing2                                          │
│  // 또는 fio-uring-built-in (최신 커널)                              │
│                                                                     │
│  // nvme-benchmarks (성능 벤치마크)                                │
│  $ sudo apt install nvme-cli                                          │
│  $ sudo nvme write /dev/nvme0n1 --start=0 --size=1G                 │
│  $ sudo nvme read /dev/nvme0n1 --start=0 --size=1G                   │
│                                                                     │
│  【NVMe 포맷팩 설정】                                               │
│  ──────────────────                                                │
│  // I/O 스케줄러 확인                                                │
│  $ cat /sys/block/nvme0n1/queue/scheduler                           │
│  [none] mq-deadline                                             │
│                                                                     │
│  // I/O 스케줄러 변경 (일부 시스템)                                   │
│  $ echo none | sudo tee /sys/block/nvme0n1/queue/scheduler         │
│                                                                     │
│  // 큐 깸이 확인                                                       │
│  $ cat /sys/block/nvme0n1/queue/nr_requests                        │
│  $ cat /sys/block/nvme0n1/queue/queue_depth                        │
│                                                                     │
│  【NVMe TRIM 설정】                                                 │
│  ──────────────────                                                │
│  // 현재 TRIM 설정 확인                                              │
│  $ lsblk -D /dev/nvme0n1                                             │
│  DISCSEQ   TRIM-SEQ                                                │
│                                                                     │
│  // fstrim으로 TRIM 실행                                               │
│  $ sudo fstrim -v /dev/nvme0n1                                 │
│  $ sudo fstrim -a /dev/nvme0n1                                 │
│  // 또는 blkdiscard (지원 시)                                        │
│  $ sudo blkdiscard /dev/nvme0n1                                     │
│                                                                     │
│  // wiper 설정 (지원 시)                                             │
│  $ sudo nvme get-feature /dev/nvme0n1 -f 0x04 | grep -i write_enable│
│  $ sudo nvme get-feature /dev/nvme0n1 -f 0x0d | grep -i write_zeroes│
│                                                                     │
│  【NVMe 보안】                                                      │
│  ──────────────────                                                │
│  // crypto 지원 확인                                                   │
│  $ sudo nvme get-feature /dev/nvme0n1 -f 0x0 | grep -i crypto                 │
│                                                                     │
│  // PSK (Power State)                                                 │
│  $ sudo nvme get-feature /dev/nvme0n1 -f 0x0 | grep -i telemetry                    │
│  $ sudo nvme get-feature /dev/nvme0n1 -f 0x0 | grep -i host_mem_buffer      │
│                                                                     │
│  // TCG (Trusted Computing Group) - TPM 2.0                            │
│  $ sudo nvme get-feature /dev/nvme0n1 -f 0x0 | grep -i tcg                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: PCIe Express를 통해 SSD에 고속으로 접근
• 속도: 1 GB/s (NVMe 1.0) ~ 32 GB/s (NVMe 4.0)
• 큐: Submission Queue, Completion Queue
• 명령어: 읽기용 (SQ), 쓰기용 (CQ)
• 레지스터: Doorbell, MSI-X 인터럽트
• 장점: 낮은 지연 시간, 높은 IOPS, 높은 병렬성
• TRIM: fstrim, blkdiscard
• SMART: smartctl, nvme smart-log
• 확인: lsblk, nvme list, nvme id-ctrl
• 성능: hdparm, fio, io_uring
• 포맷팅: /sys/block/nvme*/queue/
• 서버: 고성능 스토리지, 데이터베이스
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [SATA](./602_sata.md) → SATA 인터페이스
- [HDD](./604_hdd.md) → 기존 하드 디스크
- [SSD](./605_ssd.md) → NVMe의 저장 매치



### 👶 어린이를 위한 3줄 비유 설명
**개념**: NVMe는 "고속도로" 같아요!

**원리**: 12차선 고속도로로 데이터를 이동해요!

**효과**: SSD의 성능을 극대화해요!
