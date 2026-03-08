+++
title = "582. fstab"
weight = 582
+++

# 582. fstab (File System Table)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 파일시스템 영구 마운트 설정 파일
> 2. **가치**: 부팅 시 자동 마운트, 일관성
> 3. **융합**: 마운트, UUID, 파일시스템과 연관

---

## Ⅰ. 개요

### 개념 정의
**fstab(File System Table)**은 **부팅 시 자동으로 마운트할 파일시스템 목록을 정의한 설정 파일**입니다.

### 💡 비유: 출석부
fstab은 **출석부**와 같습니다. 누가 들어와야 하는지 미리 적어둡니다.

### fstab 구조
```
┌─────────────────────────────────────────────────────────────────────┐
│                fstab 구조                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【fstab 파일 형식】                                                  │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  /etc/fstab                                                    │ │   │
│  │  ─────────────                                                 │ │   │
│  │  [장치] [마운트포인트] [파일시스템] [옵션] [dump] [fsck]           │ │   │
│  │                                                             │ │   │
│  │  예시:                                                         │ │   │
│  │  /dev/sda1  /          ext4   defaults        0  1             │ │   │
│  │  /dev/sda2  /home      ext4   defaults        0  2             │ │   │
│  │  /dev/sda3  none       swap   sw              0  0             │ │   │
│  │  /dev/sdb1  /data      xfs    defaults,noatime 0  0            │ │   │
│  │  UUID=xxx   /mnt/usb   ext4   noauto,user     0  0            │ │   │
│  │  tmpfs      /tmp       tmpfs  defaults        0  0             │ │   │
│  │  proc       /proc      proc   defaults        0  0             │ │   │
│  │  //server/share /mnt smb  credentials=/etc/smb.cred  0  0     │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【필드 설명】                                                        │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  필드             설명                    예시                   │ │   │
│  │  ─────            ────                    ────                   │ │   │
│  │  장치             블록 장치 경로            /dev/sda1              │ │   │
│  │                  UUID                    UUID=xxx-xxx            │ │   │
│  │                  라벨                     LABEL=mydata           │ │   │
│  │                  네트워크                  server:/share          │ │   │
│  │                                                             │ │   │
│  │  마운트포인트       연결할 디렉토리            /, /home, /mnt         │ │   │
│  │                  스왑은 none              none                   │ │   │
│  │                                                             │ │   │
│  │  파일시스템       ext4, xfs, ntfs         ext4                   │ │   │
│  │                  nfs, cifs, tmpfs                                 │ │   │
│  │                  swap, proc, sysfs                                 │ │   │
│  │                                                             │ │   │
│  │  옵션             마운트 옵션              defaults, noatime       │ │   │
│  │                                                             │ │   │
│  │  dump            dump 명령 백업 여부        0 (안 함), 1 (함)        │ │   │
│  │                                                             │ │   │
│  │  fsck            부팅 시 fsck 순서          0 (안 함), 1 (루트),     │ │   │
│  │                                         2 (기타 파일시스템)        │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅱ. 상세 분석
### 상세 분석
```
┌─────────────────────────────────────────────────────────────────────┐
│                fstab 상세                                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  【장치 식별 방법】                                                    │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  방법              장점              단점                      │ │   │
│  │  ────              ────              ────                      │ │   │
│  │  /dev/sda1        직관적             장치 순서 변경 시 문제        │ │   │
│  │  UUID=xxx         고유 식별           길다                       │ │   │
│  │  LABEL=name       읽기 쉬움           중복 가능                   │ │   │
│  │  PARTUUID=xxx     파티션 UUID         GPT만                      │ │   │
│  │                                                             │ │   │
│  │  권장: UUID 사용 (장치 순서와 무관)                                │ │   │
│  │                                                             │ │   │
│  │  // UUID 확인                                                    │ │   │
│  │  $ sudo blkid                                                    │ │   │
│  │  $ ls -la /dev/disk/by-uuid/                                     │ │   │
│  │  $ sudo tune2fs -l /dev/sda1 | grep UUID                        │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【주요 마운트 옵션】                                                  │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  옵션              설명                                          │ │   │
│  │  ────              ────                                          │ │   │
│  │  defaults          rw,suid,dev,exec,auto,nouser,async           │ │   │
│  │  rw/ro            읽기쓰기 / 읽기전용                              │ │   │
│  │  noatime          접근 시간 갱신 안 함 (성능 향상)                  │ │   │
│  │  nodiratime       디렉토리 접근 시간 갱신 안 함                      │ │   │
│  │  noexec           실행 파일 실행 금지                              │ │   │
│  │  nosuid           SUID/SGID 비트 무시                              │ │   │
│  │  nodev            장치 파일 무시                                   │ │   │
│  │  user/users       일반 사용자 마운트 허용                           │ │   │
│  │  noauto           부팅 시 자동 마운트 안 함                         │ │   │
│  │  x-systemd.automount  접근 시 자동 마운트                          │ │   │
│  │                                                             │ │   │
│  │  파일시스템별 옵션:                                                │ │   │
│  │  ext4: data=ordered, journal, writeback                         │ │   │
│  │  xfs:  allocsize, nobarrier, inode64                            │ │   │
│  │  nfs:  hard, soft, rsize, wsize, timeo                          │ │   │
│  │                                                             │ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  【특수 파일시스템】                                                   │
│  ──────────────────                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                             │ │   │
│  │  파일시스템       마운트포인트    용도                           │ │   │
│  │  ────────         ──────────    ────                           │ │   │
│  │  proc             /proc         프로세스 정보                   │ │   │
│  │  sysfs            /sys          시스템 정보                     │ │   │
│  │  devtmpfs         /dev          장치 파일                      │ │   │
│  │  tmpfs            /tmp, /run    임시 파일 (메모리)              │ │   │
│  │  securityfs       /sys/kernel/security  보안                   │ │   │
│  │  cgroup           /sys/fs/cgroup 컨테이너                      │ │   │
│  │  debugfs          /sys/kernel/debug 디버그                     │ │   │
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
│  【fstab 편집】                                                       │
│  ──────────────────                                                │
│  // fstab 편집                                                       │
│  $ sudo nano /etc/fstab                                            │
│  $ sudo vi /etc/fstab                                              │
│                                                                     │
│  // 백업                                                            │
│  $ sudo cp /etc/fstab /etc/fstab.bak                               │
│                                                                     │
│  // fstab 적용                                                       │
│  $ sudo mount -a                  // 전체 마운트                      │
│  $ sudo mount /mnt/data          // 특정 항목만                       │
│                                                                     │
│  【fstab 검증】                                                       │
│  ──────────────────                                                │
│  // 문법 검사                                                        │
│  $ sudo findmnt --verify                                           │
│  $ sudo mount -a -v                // 상세 출력                      │
│                                                                     │
│  // 오류 시 복구                                                      │
│  // 1. 읽기 전용 루트로 재부팅                                          │
│  // 2. 재마운트                                                       │
│  $ sudo mount -o remount,rw /                                      │
│  // 3. fstab 수정                                                    │
│  $ sudo nano /etc/fstab                                            │
│                                                                     │
│  【일반적인 fstab 예시】                                               │ |
│  ──────────────────                                                │
│  # <file system>  <mount point>  <type>  <options>  <dump> <pass>  │
│                                                                     │
│  # 루트 파일시스템                                                     │
│  UUID=xxx-xxx  /        ext4  defaults,noatime      0  1            │
│                                                                     │
│  # 홈 파티션                                                          │
│  UUID=yyy-yyy  /home    ext4  defaults,noatime      0  2            │
│                                                                     │
│  # 데이터 파티션                                                       │
│  UUID=zzz-zzz  /data    xfs   defaults,noatime      0  0            │
│                                                                     │
│  # 스왑                                                              │
│  UUID=swap-uuid none    swap  sw                   0  0             │
│                                                                     │
│  # 부팅 시 마운트 안 함 (수동)                                          │
│  /dev/sdb1    /mnt/usb  ext4  noauto,user          0  0             │
│                                                                     │
│  # NFS 마운트                                                         │
│  server:/share  /mnt/nfs  nfs  defaults,_netdev    0  0             │
│                                                                     │
│  # CIFS/SMB 마운트                                                    │
│  //server/share /mnt/smb  cifs  credentials=/etc/.smb  0  0        │
│                                                                     │
│  # tmpfs (메모리 파일시스템)                                            │
│  tmpfs        /tmp      tmpfs defaults,size=2G      0  0            │
│                                                                     │
│  # systemd 자동 마운트                                                │
│  /dev/sdb1    /mnt/usb  ext4  noauto,x-systemd.automount  0  0     │
│                                                                     │
│  【NFS fstab 설정】                                                   │
│  ──────────────────                                                │
│  // 기본 NFS 마운트                                                   │
│  server:/share  /mnt/nfs  nfs  defaults  0  0                      │
│                                                                     │
│  // 성능 옵션                                                          │
│  server:/share  /mnt/nfs  nfs  rw,hard,intr,rsize=8192,wsize=8192  0 0│
│                                                                     │
│  // 네트워크 필요 옵션                                                  │
│  server:/share  /mnt/nfs  nfs  _netdev  0  0                        │
│                                                                     │
│  【스왑 설정】                                                         │
│  ──────────────────                                                │
│  // 스왑 파티션                                                        │
│  UUID=swap-uuid  none  swap  sw  0  0                              │
│                                                                     │
│  // 스왑 파일                                                          │
│  /swapfile  none  swap  sw  0  0                                   │
│                                                                     │
│  // 스왑 우선순위                                                       │
│  UUID=swap1  none  swap  sw,pri=10  0  0                           │
│  UUID=swap2  none  swap  sw,pri=5   0  0                           │
│                                                                     │
│  【UUID 확인 및 사용】                                                 │ |
│  ──────────────────                                                │
│  // 모든 장치 UUID 확인                                                │
│  $ sudo blkid                                                       │
│  $ lsblk -f                                                         │
│                                                                     │
│  // 특정 장치 UUID                                                     │
│  $ sudo blkid /dev/sda1                                            │
│  $ sudo tune2fs -l /dev/sda1 | grep UUID                           │
│                                                                     │
│  // /dev/disk/by-uuid                                                │
│  $ ls -la /dev/disk/by-uuid/                                       │
│                                                                     │
│  // fstab에 UUID 형식                                                 │
│  UUID=12345678-1234-1234-1234-123456789012  /mnt  ext4  defaults  0 0│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ⅳ. 기대효과 및 결론
### 핵심 요약
```
• 개념: 파일시스템 영구 마운트 설정 파일
• 위치: /etc/fstab
• 필드: 장치, 마운트포인트, 파일시스템, 옵션, dump, fsck
• 장치 식별: /dev/sda1, UUID=, LABEL=
• 권장: UUID 사용 (장치 순서 무관)
• defaults: rw,suid,dev,exec,auto,nouser,async
• noatime: 접근 시간 갱신 안 함 (성능)
• noauto: 자동 마운트 안 함
• _netdev: 네트워크 필요
• x-systemd.automount: 접근 시 자동 마운트
• 적용: mount -a
• 검증: findmnt --verify
• 백업: cp /etc/fstab /etc/fstab.bak
```

---

### 📌 관련 개념 맵 (Knowledge Graph)

- [마운트](./580_mount.md) → fstab이 설정하는 작업
- [파일 시스템](./575_file_system.md) → 마운트 대상
- [스왑](./588_swap.md) → fstab 스왑 설정

### 👶 어린이를 위한 3줄 비유 설명
**개념**: fstab은 "출석부" 같아요!

**원리**: 누가 들어와야 하는지 미리 적어둬요!

**효과**: 컴퓨터가 켜질 때 자동으로 마운트해요!
