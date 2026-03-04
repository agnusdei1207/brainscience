+++
title = "02. 운영체제 키워드 목록"
date = 2026-03-03
[extra]
categories = "pe_exam-os"
+++

# 운영체제 (OS) 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 운영체제 전 영역 핵심 키워드

---

## 1. OS 기초 / 구조 — 22개

1. 운영체제 (Operating System) 정의 · 역할 · 역사
2. 모놀리식 커널 (Monolithic Kernel)
3. 마이크로커널 (Microkernel) — Mach, L4
4. 하이브리드 커널 (Hybrid Kernel) — Windows NT, macOS XNU
5. 엑소커널 (Exokernel)
6. 계층 구조 OS (Layered OS)
7. 시스템 콜 (System Call) — Trap, 사용자→커널 전환
8. 커널 모드 / 사용자 모드 (Kernel/User Mode)
9. 이중 동작 모드 (Dual-mode Operation)
10. 특권 명령어 (Privileged Instruction)
11. 보호 링 (Protection Ring) — Ring 0~3
12. POSIX (Portable OS Interface)
13. ABI (Application Binary Interface)
14. 리눅스 커널 (Linux Kernel) — 모듈, init/systemd, proc
15. Windows 커널 — NT 계층 구조, HAL (Hardware Abstraction Layer)
16. 부팅 프로세스 — BIOS, UEFI, GRUB, 커널 초기화
17. 인터럽트 (Interrupt) — 하드/소프트웨어, IRQ, IDT
18. 예외 (Exception) — Fault/Trap/Abort
19. 시스템 콜 유형 — 프로세스 제어/파일/장치/정보/통신
20. API vs System Call 차이
21. 실시간 운영체제 (RTOS) — VxWorks, FreeRTOS, QNX
22. 분산 운영체제 — NFS, 투명성 (Transparency)

---

## 2. 프로세스 관리 — 28개

1. 프로세스 (Process) 정의 vs 프로그램
2. 프로세스 상태 전이 — New / Ready / Running / Waiting / Terminated
3. PCB (Process Control Block) — PID, PC, 레지스터, 메모리 정보
4. 프로세스 생성 — fork(), exec(), copy-on-write
5. 프로세스 종료 — exit(), wait(), 좀비 프로세스 (Zombie)
6. 고아 프로세스 (Orphan Process)
7. 스레드 (Thread) — 사용자 스레드 vs 커널 스레드
8. 다대일 (Many-to-One) 스레드 모델
9. 일대일 (One-to-One) 스레드 모델
10. 다대다 (Many-to-Many) 스레드 모델
11. POSIX Pthreads
12. 멀티스레딩 장단점 — 병렬성 vs 동기화 복잡도
13. 컨텍스트 스위칭 (Context Switching) — 오버헤드, PCB 저장/복원
14. 코루틴 (Coroutine) / 파이버 (Fiber) — 협력적 멀티태스킹
15. 경량 프로세스 (LWP, Lightweight Process)
16. 프로세스 계층 — 부모/자식, 프로세스 트리
17. 데몬 프로세스 (Daemon Process) — 백그라운드 서비스
18. 신호 (Signal) — SIGKILL, SIGTERM, SIGCHLD, 핸들러
19. IPC (Inter-Process Communication) 개요
20. 공유 메모리 (Shared Memory) — shmget, System V / POSIX
21. 메시지 큐 (Message Queue) — msgget, 직접/간접 통신
22. 파이프 (Pipe) — 익명(Anonymous) / 명명(Named, FIFO)
23. 소켓 (Socket) — Unix 도메인 소켓, 네트워크 소켓
24. 원격 프로시저 호출 (RPC) — IDL, 스텁
25. 프로세스 그룹 / 세션 — PGID, SID, 터미널 제어
26. 네임스페이스 (Namespace) — PID/NET/MNT/IPC/UTS/USER
27. cgroup (Control Group) — CPU/메모리/IO 자원 제한
28. eBPF (Extended Berkeley Packet Filter) — 커널 추적/보안

---

## 3. CPU 스케줄링 — 28개

1. CPU 스케줄링 기본 개념 — 선점형 vs 비선점형
2. 스케줄링 기준 — CPU 이용률, 처리량, 반환시간, 대기시간, 응답시간
3. Ready Queue / Wait Queue / Job Queue
4. 디스패처 (Dispatcher) — 디스패치 지연 (Dispatch Latency)
5. FCFS (First-Come First-Served) — 호위 효과 (Convoy Effect)
6. SJF (Shortest Job First) — 비선점, 평균 대기시간 최소
7. SRTF (Shortest Remaining Time First) — SJF 선점형
8. Round Robin (RR) — 시간 할당량 (Time Quantum), 시분할
9. RR 타임 퀀텀 — 너무 작음(오버헤드↑) vs 너무 큼(FCFS화)
10. 우선순위 스케줄링 (Priority Scheduling)
11. 기아 (Starvation) — 무한 대기, 에이징 (Aging)으로 해결
12. 다단계 큐 (MLQ, Multi-Level Queue) — Foreground/Background 큐
13. 다단계 피드백 큐 (MLFQ) — 동적 우선순위 조정
14. HRN (Highest Response Ratio Next) — (대기+실행)/실행
15. 실시간 스케줄링 — 경성 (Hard RT) / 연성 (Soft RT)
16. EDF (Earliest Deadline First) — 동적, 최적 단일 CPU
17. RMS (Rate Monotonic Scheduling) — 정적, 주기 기반
18. CFS (Completely Fair Scheduler) — 리눅스, vruntime, Red-Black Tree
19. 리눅스 스케줄러 클래스 — SCHED_NORMAL / SCHED_FIFO / SCHED_RR / SCHED_DEADLINE
20. CPU-bound vs I/O-bound 프로세스
21. 선점 (Preemption) — 타이머 인터럽트, 강제 문맥 교환
22. 비선점 (Non-preemptive) — 자발적 양보, I/O 대기
23. 멀티프로세서 스케줄링 — 대칭(SMP) vs 비대칭(AMP)
24. Load Balancing — Push/Pull 마이그레이션
25. 프로세서 친화성 (CPU Affinity) — 캐시 효율
26. NUMA 스케줄링 — 노드 로컬 접근 최적화
27. 에너지 효율 스케줄링 (DVFS) — 동적 주파수/전압 조절
28. 가상화 환경 스케줄링 — vCPU, 하이퍼바이저 스케줄러

---

## 4. 동기화 / 상호배제 — 32개

1. 임계 구역 (Critical Section) — 경쟁 조건 (Race Condition)
2. 상호배제 (Mutual Exclusion)
3. 진행 (Progress) 조건
4. 한정 대기 (Bounded Waiting) 조건
5. 피터슨 알고리즘 (Peterson's Algorithm) — 소프트웨어 해법
6. 데커 알고리즘 (Dekker's Algorithm)
7. 베이커리 알고리즘 (Bakery Algorithm) — Lamport, N개 프로세스
8. 하드웨어 동기화 — TestAndSet, CompareAndSwap, XCHG
9. CAS (Compare-And-Swap) — 원자적 연산
10. 스핀락 (Spinlock) — Busy-Waiting, 멀티프로세서 적합
11. Ticket Lock / MCS Lock
12. 세마포어 (Semaphore) — 이진(Binary) / 카운팅(Counting)
13. P(wait) / V(signal) 연산
14. 뮤텍스 (Mutex) — 소유권, 재진입 불가, vs 세마포어
15. 모니터 (Monitor) — 조건 변수 (Condition Variable), wait/signal/broadcast
16. 모니터 구조 — 공유 데이터 + 연산 + 조건 변수 큐
17. Lock-free 자료구조 — CAS/LL-SC, ABA 문제
18. 생산자-소비자 문제 (Producer-Consumer, Bounded Buffer)
19. 판독자-기록자 문제 (Readers-Writers) — 읽기 우선 vs 쓰기 우선
20. 식사하는 철학자 문제 (Dining Philosophers)
21. 수면하는 이발사 문제 (Sleeping Barber)
22. ASLR (주소 공간 레이아웃 랜덤화)
23. DEP/NX 비트 (Data Execution Prevention)
24. Stack Canary — 스택 버퍼 오버플로우 탐지
25. 재진입성 (Reentrancy) vs 스레드 안전 (Thread Safety)
26. 메모리 배리어 (Memory Barrier / Fence) — 명령어 순서 보장
27. 순서 의존성 (Happens-Before) — Java Memory Model
28. ABA 문제 (ABA Problem) — CAS의 한계
29. 잠금 계층화 (Lock Ordering) — 교착상태 예방
30. 읽기-복사-업데이트 (RCU, Read-Copy-Update) — 리눅스
31. Transactional Memory (TM) — HTM, STM
32. 세마포어 vs 뮤텍스 vs 모니터 비교표

---

## 5. 교착상태 (Deadlock) — 20개

1. 교착상태 (Deadlock) 정의 — 무한 대기, 진전 불가
2. 교착상태 4조건 (Coffman) — 상호배제 / 점유대기 / 비선점 / 순환대기
3. 자원 할당 그래프 (RAG) — 사이클 = 교착상태
4. 교착상태 예방 (Prevention) — 4조건 중 하나 부정
5. 교착상태 회피 (Avoidance) — 안전 상태 (Safe State)
6. 은행원 알고리즘 (Banker's Algorithm) — Available/Max/Allocation/Need
7. 안전 순서 (Safe Sequence)
8. 교착상태 탐지 (Detection) — Wait-For Graph
9. 교착상태 복구 (Recovery) — 프로세스 종료 / 자원 선점
10. 롤백 (Rollback) / 체크포인트 (Checkpoint)
11. 기아 (Starvation) — 특정 프로세스 무한 대기
12. 라이브락 (Livelock) — 서로 양보, 진전 없음
13. 타임아웃 기반 감지 — 분산 시스템 교착상태
14. 분산 교착상태 감지 — 에지-추추 알고리즘
15. 현대 OS 교착상태 처리 — Ostrich Algorithm, OOM Killer
16. 자원 계층화 (Resource Ordering) — 순환대기 방지
17. 선점 자원 (Preemptable Resource) vs 비선점 자원
18. 희생자 선택 (Victim Selection) — 복구 시 기준
19. 트랜잭션 교착상태 — 데이터베이스 Wait-For Graph
20. 교착상태 vs 기아 vs 라이브락 비교

---

## 6. 메모리 관리 — 38개

1. 주소 바인딩 (Address Binding) — 컴파일 / 적재 / 실행 시점
2. 논리 주소 (Logical Address) vs 물리 주소 (Physical Address)
3. MMU (Memory Management Unit)
4. 재배치 레지스터 (Relocation Register) — Base/Limit
5. 메모리 할당 전략 — First Fit / Best Fit / Worst Fit / Next Fit
6. 단편화 — 외부 (External) / 내부 (Internal) Fragmentation
7. 컴팩션 (Compaction) — 외부 단편화 해소
8. 페이징 (Paging) — 고정 크기 페이지/프레임, 내부 단편화
9. 페이지 테이블 (Page Table) — PTE, Valid/Dirty/Reference/Access 비트
10. 다단계 페이지 테이블 — 2-level / 3-level / 4-level (x86-64)
11. 역페이지 테이블 (Inverted Page Table)
12. 해시 페이지 테이블 (Hash Page Table)
13. TLB (Translation Lookaside Buffer) — 주소 변환 캐시, 히트율 99%+
14. TLB 미스 (TLB Miss) — 소프트웨어/하드웨어 처리
15. Huge Pages (대용량 페이지) — 2MB / 1GB, TLB 효율
16. 세그멘테이션 (Segmentation) — 논리 단위, 가변 길이, 외부 단편화
17. 세그먼트-페이지 혼합 (Intel x86)
18. 가상 메모리 (Virtual Memory) — 요구 페이징 (Demand Paging)
19. 페이지 부재 (Page Fault) — 처리 과정, 오버헤드
20. FIFO 페이지 교체 — Belady's Anomaly
21. LRU (Least Recently Used) 페이지 교체
22. LFU (Least Frequently Used) 페이지 교체
23. Clock 알고리즘 (NRU, Second Chance)
24. Optimal (OPT) 알고리즘 — 이론적 최적, 구현 불가
25. Working Set Model — 지역성 (Locality)
26. PFF (Page Fault Frequency) — 프레임 할당 조정
27. 스래싱 (Thrashing) — CPU 이용률 급락, 과도한 페이지 교환
28. Copy-on-Write (COW) — fork() 최적화
29. 메모리 오버커밋 (Overcommit)
30. OOM Killer — badness 점수, 희생자 선택
31. 슬랩 할당자 (Slab Allocator) — 커널 객체 캐시
32. Buddy System — 블록 분할/합병, 외부 단편화↓
33. 메모리 매핑 (mmap) — 파일 → 주소 공간, Zero-Copy
34. 공유 메모리 세그먼트 — 공유 기반 IPC
35. NUMA (Non-Uniform Memory Access) — 노드 간 접근 지연 차이
36. 메모리 보호 — Base/Limit 레지스터, 세그먼트 권한
37. 가비지 컬렉션 (GC) — Mark-and-Sweep, 세대별 GC (JVM)
38. 메모리 단편화 시뮬레이션 — 버디, 슬랩, 파편화 비교

---

## 7. 파일 시스템 — 30개

1. 파일 시스템 구조 — 부트블록/슈퍼블록/inode/데이터블록
2. inode (Index Node) — 메타데이터, 하드링크, inode 번호
3. inode 구조 — 직접/간접/2단계/3단계 블록 포인터
4. 디렉터리 구조 — 단일/이중/트리/비순환 그래프/일반 그래프
5. 디렉터리 엔트리 (dentry) — 파일명 + inode 번호
6. 파일 할당 방법 — 연속 / 연결 / 색인 (Indexed)
7. Extent Tree (ext4) — 블록 그룹, 사전 할당
8. FAT (File Allocation Table) — FAT16/FAT32, 클러스터 체인
9. NTFS — MFT, 저널, ACL, ADS
10. EXT4 — extent, 저널링, 64비트 주소
11. APFS — Apple, CoW, 암호화, 클론
12. ZFS — CoW, RAID-Z, 체크섬, 스냅샷, 풀 기반
13. XFS — 고성능, 저널, 대용량, parallel
14. Btrfs — CoW, 서브볼륨, 스냅샷, RAID
15. 저널링 파일 시스템 (Journaling FS) — Write-Ahead Log
16. 저널링 모드 — Writeback / Ordered / Data
17. Copy-on-Write FS — ZFS, Btrfs, APFS
18. 파일 링크 — 하드 링크 (Hard Link) / 심볼릭 링크 (Symlink)
19. 파일 권한 — rwx / 소유자/그룹/기타 / SetUID / SetGID / Sticky Bit
20. ACL (Access Control List) — POSIX ACL, Windows DACL
21. 접근 제어 모델 — DAC / MAC / RBAC / ABAC
22. VFS (Virtual File System) — 파일시스템 추상화 레이어
23. 마운트 (Mount) — bind mount, overlayfs, unionfs, FUSE
24. 파티션 — MBR (2TB) / GPT (9.4ZB)
25. LVM (Logical Volume Manager) — PV/VG/LV, 스냅샷, 리사이징
26. RAID — 0/1/5/6/10 (파일시스템 계층)
27. 네트워크 파일시스템 — NFS (v3/v4), CIFS/SMB, AFS
28. 분산 파일시스템 — HDFS, GFS, Ceph, GlusterFS
29. 파일시스템 검사/복구 — fsck, chkdsk, Journal Replay
30. SSD 최적화 — TRIM, Wear Leveling, FTL (Flash Translation Layer)

---

## 8. 입출력 관리 — 20개

1. I/O 서브시스템 계층 — 사용자→VFS→블록 계층→드라이버→장치
2. 장치 드라이버 — 블록(랜덤)/문자(순차), 인터럽트/Polling
3. 장치 파일 — /dev (Major/Minor 번호), udev
4. 버퍼링 (Buffering) — 단일/이중/순환 버퍼
5. 캐싱 (Caching) — Page Cache, Buffer Cache, Read-Ahead
6. 스풀링 (Spooling) — 디스크 버퍼링, 프린터 큐
7. 동기 I/O (Synchronous I/O) — Blocking
8. 비동기 I/O (Asynchronous I/O) — Async, AIO, io_uring
9. I/O 멀티플렉싱 — select / poll / epoll / kqueue
10. epoll — LT (Level-Triggered) / ET (Edge-Triggered)
11. Zero-Copy I/O — sendfile, splice, mmap + DMA
12. DMA (Direct Memory Access) — CPU 개입 최소화
13. 디스크 스케줄링 — FCFS / SSTF / SCAN / C-SCAN / C-LOOK
14. I/O 스케줄러 (Linux) — CFQ / BFQ / deadline / mq-deadline / none
15. 인터럽트 구동 I/O (Interrupt-driven I/O)
16. 풀링 (Polling) — 바쁜 대기, CPU 낭비
17. io_uring (Linux 5.1+) — 링 버퍼 기반 비동기 I/O
18. SCSI / NVMe / SATA 프로토콜
19. Direct I/O (O_DIRECT) — 캐시 우회, DB 성능
20. I/O 가상화 — SR-IOV, virtio, IOMMU

---

## 9. 가상화 / 컨테이너 — 22개

1. 가상화 (Virtualization) 개념 — 하드웨어 추상화, 자원 격리
2. 전가상화 (Full Virtualization, HVM) — 바이너리 번역
3. 반가상화 (Paravirtualization) — 커널 수정, 하이퍼콜
4. 하드웨어 지원 가상화 — AMD-V (SVM) / Intel VT-x
5. 하이퍼바이저 Type 1 — Bare-Metal, ESXi, Hyper-V, Xen
6. 하이퍼바이저 Type 2 — Hosted, VirtualBox, VMware Workstation
7. KVM (Kernel-based Virtual Machine) — 리눅스 모듈, QEMU
8. Xen — Dom0/DomU, PV/HVM
9. EPT/NPT (Extended/Nested Page Table) — 중첩 페이지 테이블
10. IOMMU / SR-IOV — I/O 가상화, PCI 장치 직접 할당
11. vCPU 스케줄링 — Credit Scheduler, vCPU 오버커밋
12. 컨테이너 (Container) — OS 수준 가상화, 공유 커널
13. Docker — 이미지/컨테이너/레지스트리, containerd
14. Namespace — PID/NET/MNT/IPC/UTS/USER/TIME/CGROUP
15. cgroup v1 / v2 — 자원 제한, 계층적 그룹
16. 컨테이너 런타임 — OCI, runc, containerd, CRI-O, Podman
17. 컨테이너 vs VM — 격리 강도, 부팅 속도, 밀도
18. Kubernetes (k8s) — Pod, Node, 오케스트레이션
19. WebAssembly (WASM) / WASI — 샌드박스, 이식성
20. Unikernel — 라이브러리 OS, MirageOS
21. 서버리스 (Serverless) — FaaS, Cold Start
22. eBPF — 커널 수준 프로그래밍, 컨테이너 보안

---

## 10. 보안 / 보호 — 18개

1. 보호 링 (Protection Ring) — Ring 0~3, CPL
2. 시스템 콜 보안 — seccomp, syscall filtering
3. ASLR (Address Space Layout Randomization)
4. DEP/NX (Data Execution Prevention)
5. Stack Canary / Stack Guard
6. RELRO (Relocation Read-Only)
7. PIE (Position-Independent Executable)
8. CFI (Control Flow Integrity)
9. ROP (Return-Oriented Programming) — 방어 기법
10. 버퍼 오버플로우 (Buffer Overflow) — 스택/힙
11. SELinux — MAC, Type Enforcement, 정책
12. AppArmor — 프로파일 기반 MAC
13. DAC vs MAC vs RBAC vs ABAC
14. Capability (Linux) — 루트 권한 분할
15. Seccomp-BPF — 시스템 콜 화이트리스트
16. TPM (Trusted Platform Module) — 하드웨어 보안
17. Secure Boot — UEFI, 코드 서명 검증
18. Confidential Computing — Intel SGX, AMD SEV, TrustZone

---

## 11. 최신 OS 동향 — 10개

1. eBPF 기반 가관측성 (Observability) — Cilium, Falco
2. io_uring — 고성능 비동기 I/O, Linux 5.1+
3. Rust 기반 OS 개발 — Redox OS, KOS
4. 마이크로VM — Firecracker, gVisor
5. WASM 런타임 — Wasmtime, Wasmer, WasmEdge
6. 유니커널 (Unikernel) 재부상
7. CXL (Compute Express Link) — 메모리 캐싱/공유
8. 에너지 효율 OS 스케줄링 — ARM big.LITTLE, DVFS
9. AI 기반 OS 최적화 — 예측 스케줄링, 자동 튜닝
10. 실시간 Linux (PREEMPT_RT) — 패치, 하드 RT 지원

---

**총 키워드 수: 208개**
