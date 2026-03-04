+++
title = "01. 컴퓨터 구조 키워드 목록 (완전판)"
date = 2026-03-04
[extra]
categories = "pe_exam-computer-arch"
+++

# 컴퓨터 구조 키워드 목록 — 완전판

정보통신기술사·컴퓨터응용시스템기술사 대비 컴퓨터 구조 전 영역 기술사 수준 핵심 키워드

---

## 1. 컴퓨터 구조 기초 / 역사 — 14개

1. 폰 노이만 구조 (Von Neumann Architecture) — 프로그램 내장 방식, 폰 노이만 병목
2. 하버드 구조 (Harvard Architecture) — 명령어/데이터 버스 분리, DSP/MCU
3. 수정 하버드 구조 (Modified Harvard) — 캐시 분리 + 주기억 통합, ARM Cortex-A
4. 컴퓨터 세대 — 진공관→트랜지스터→IC→VLSI→AI 시대
5. ENIAC / UNIVAC — 역사적 맥락, 최초 전자식/상업용 컴퓨터
6. CISC (Complex Instruction Set Computer) — x86, 복잡 명령어, 마이크로코드
7. RISC (Reduced Instruction Set Computer) — ARM/MIPS/RISC-V, 단순·고속
8. VLIW (Very Long Instruction Word) — ILP 명시적 표현, 컴파일러 의존
9. EPIC (Explicitly Parallel Instruction Computing) — Itanium, IA-64
10. SoC (System on Chip) — CPU+GPU+NPU+IO 통합, 모바일/임베디드
11. MCU (Micro Controller Unit) — AVR/STM32/RP2040, 마이크로초 제어
12. MPU (Micro Processing Unit) — x86/ARM, 범용 OS 실행
13. 임베디드 시스템 (Embedded System) — 특수 목적, 실시간성
14. 엣지 컴퓨팅 하드웨어 — Jetson Orin / RK3588 / i.MX 8

---

## 2. 디지털 논리 / 부울 대수 — 20개

1. 부울 대수 — 교환/결합/분배/드모르간 법칙
2. 기본 게이트 — AND / OR / NOT / NAND / NOR / XOR / XNOR
3. NAND/NOR — 기능적 완전성 (Functional Completeness)
4. 카르노 맵 (Karnaugh Map) — 논리식 최소화, 무관항(Don't Care)
5. Quine-McCluskey 알고리즘 — 다변수 논리 최소화
6. 반가산기 / 전가산기 — 덧셈 기본 회로
7. 멀티플렉서 (MUX) / 디멀티플렉서 (DEMUX)
8. 인코더 / 디코더 (우선순위 인코더 포함)
9. 비교기 (Comparator) — 크기 비교, 4비트 직렬/병렬
10. RS 플립플롭 / D 플립플롭 / JK 플립플롭 / T 플립플롭
11. 마스터-슬레이브 플립플롭 (Master-Slave FF) — 레이스 방지
12. 레지스터 (Register) — 플립플롭 집합, SISO/SIPO/PISO/PIPO
13. 카운터 (Counter) — 비동기식(리플)/동기식 카운터
14. 유한 상태 기계 (FSM) — Mealy / Moore 기계
15. 조합 논리 vs 순서 논리 비교
16. CMOS 회로 — 보완 MOS, 전력 소비 특성
17. 팬아웃 (Fan-out) / 팬인 (Fan-in) — 구동 능력
18. 전파 지연 (Propagation Delay) — 게이트 속도
19. 글리치 (Glitch) / 해저드 (Hazard) — 순간 오류
20. 프로그래밍 가능 논리 — PLA / PAL / GAL / CPLD / FPGA

---

## 3. CPU 구조 / 마이크로아키텍처 — 28개

1. CPU 구성 — ALU / 제어장치(CU) / 레지스터 파일
2. ALU (Arithmetic Logic Unit) — 산술/논리/시프트 연산
3. 레지스터 종류 — PC / MAR / MDR / IR / ACC / SP / PSW / GPR
4. 제어장치 — 하드와이어드 / 마이크로프로그래밍 방식
5. 명령어 사이클 — IF / ID / EX / MEM / WB
6. 마이크로 연산 (RTL 표기)
7. 인터럽트 처리 — 인식/저장/서비스/복귀, 벡터 테이블
8. DMA (Direct Memory Access) — 사이클 스틸링 / 버스트 모드
9. 슈퍼스칼라 (Superscalar) — 복수 실행 유닛, IPC > 1
10. 비순서 실행 (OoO, Out-of-Order Execution) — 토마술로 알고리즘
11. 레지스터 리네이밍 (Register Renaming) — WAW/WAR 위험 해소
12. 투기적 실행 (Speculative Execution) — 분기 예측 + 결과 선취
13. 분기 예측 (Branch Prediction) — 1-bit/2-bit 포화 카운터, TAGE
14. 분기 목표 버퍼 (BTB, Branch Target Buffer)
15. 리오더 버퍼 (ROB, Reorder Buffer) — 순서대로 완료(Commit)
16. 예약 스테이션 (Reservation Station) — 피연산자 대기, 비순서 발행
17. 멜트다운 / 스펙터 (Meltdown/Spectre) — 투기적 실행 보안 취약점
18. 인텔 골든 코브 (Golden Cove) — Alder Lake P코어 마이크로아키텍처
19. 인텔 그레이스몬트 (Gracemont) — Alder Lake E코어 에너지 효율
20. AMD Zen 4 / Zen 5 — 4nm/3nm, AVX-512, 전력 효율 혁신
21. 명령어 융합 (Macro-fusion) — 두 명령어를 하나로 처리
22. 마이크로 융합 (Micro-fusion) — 복합 명령어를 하나의 μop로
23. μop Cache (Decoded ICache / DSB) — 디코딩 반복 감소
24. 루프 스트림 디텍터 (LSD) — 소규모 루프 전용 최적화
25. 전력 관리 — DVFS (Dynamic Voltage Frequency Scaling), C-States, P-States
26. TDP (Thermal Design Power) — 설계 열 방산 기준
27. CPU 소켓 — LGA / BGA / PGA — 핀 배치 방식
28. 이종 집적 (Heterogeneous Integration) — 서로 다른 코어 유형 통합

---

## 4. x86 아키텍처 심화 — 16개

1. x86-64 (AMD64) — 64비트 확장, 범용 레지스터 16개
2. 레지스터 체계 — RAX/RBX/.../R8-R15, SSE/AVX 벡터 레지스터
3. 보호 모드 (Protected Mode) — 세그먼트+페이지 보호
4. 롱 모드 (Long Mode, 64-bit) — 4계층 페이지 테이블, 48비트 VA
5. 가상화 지원 — Intel VT-x / AMD-V (SVM)
6. AVX-512 — 512비트 SIMD, 32개 ZMM 레지스터, AI 추론 가속
7. AMX (Advanced Matrix Extensions) — Intel, 행렬 곱 가속, TileMM
8. Intel Core Ultra (Meteor Lake) — 타일 설계, NPU 내장 (AI 부스트)
9. Intel Xeon Scalable (Sapphire Rapids) — 서버, PCIe 5.0, CXL 1.1
10. AMD EPYC Genoa (4세대) — Zen 4, 128코어, PCIe 5.0, CXL
11. AMD EPYC Turin (5세대) — Zen 5, 192코어 (최대)
12. x86 가상화 명령 — VMXON/VMLAUNCH/VMRESUME/VMXOFF
13. IOMMU (Intel VT-d / AMD-Vi) — DMA 주소 변환, 격리
14. PCIe 버전 비교 — PCIe 3.0/4.0/5.0/6.0 — 대역폭 배증
15. Ring 보호 수준 — Ring 0(커널)/Ring 3(사용자), Ring 1/2(미사용)
16. UEFI vs BIOS — 보안 부팅, GPT, 64비트 부팅

---

## 5. ARM 아키텍처 심화 — 22개

1. ARM 아키텍처 역사 — ARM7 → Cortex → ARMv8 → ARMv9
2. ARMv8-A — AArch64 (64비트) + AArch32 (32비트 호환)
3. ARMv9-A — SVE2, Confidential Compute Architecture (CCA)
4. ARM Cortex-A 시리즈 — 응용 프로세서 (스마트폰/서버)
5. ARM Cortex-M 시리즈 — MCU, IoT, 초저전력
6. ARM Cortex-R 시리즈 — 실시간, 자동차/산업
7. big.LITTLE — 고성능 + 에너지 효율 코어 이종 구성
8. DynamIQ — big.LITTLE 개선, 8+1 구성, Cache Coherence
9. Apple Silicon — M1/M2/M3/M4 — ARM 커스텀 설계
10. Apple M1 아키텍처 — Firestorm(P)+Icestorm(E), 통합 메모리, 16GB/32GB
11. Apple M4 — TSMC 3nm N3E, 10코어 CPU, 10코어 GPU, 16코어 NPU
12. 통합 메모리 아키텍처 (UMA) — CPU/GPU/NPU 메모리 공유, 대역폭↑
13. Qualcomm Snapdragon (8 Gen 3 / X Elite) — Oryon CPU, Adreno GPU, Hexagon
14. Samsung Exynos 2500 — 3nm GAA, Cortex-X5
15. MediaTek Dimensity 9400 — ARM Cortex-X925
16. AWS Graviton 4 — 96코어 ARM, 클라우드 서버, 30% 성능 향상
17. Ampere Altra — 클라우드 ARM 서버, 192코어, 저전력
18. NEON/SVE (Scalable Vector Extension) — ARM SIMD
19. 포인터 인증 (PAC, Pointer Authentication) — ARM 보안 기능
20. 메모리 태깅 (MTE, Memory Tagging Extension) — UAF/버퍼오버플로우 탐지
21. TrustZone — ARM 보안 세계, TEE (신뢰 실행 환경)
22. Realm Virtualization (ARMv9 CCA) — 하이퍼바이저 독립 보안 영역

---

## 6. RISC-V 아키텍처 — 16개

1. RISC-V 정의 — 오픈소스 ISA, 캘리포니아 버클리, 2010
2. RISC-V 특징 — 모듈식, 로열티 무료, 기반 ISA + 확장 ISA
3. 기반 ISA — RV32I / RV32E / RV64I / RV128I
4. 표준 확장 — M(곱셈)/A(원자)/F(단정밀도FP)/D(배정밀도)/C(압축)/V(벡터)
5. RISC-V 벡터 확장 (V) — 가변 폭 SIMD, AI 가속
6. Privileged ISA — Machine / Supervisor / User 모드 3계층
7. RISC-V in AI — SiFive Intelligence X280, T-Head XuanTie
8. SiFive P670 — 고성능 임베디드, OoO 실행
9. 중국 T-Head XuanTie C920 — RISC-V 서버 칩
10. RISC-V 에코시스템 — RISC-V International, 90개국 4000+ 회원
11. RISC-V vs ARM 비교 — 라이선스 비용 / 생태계 성숙도 / 커스텀 가능성
12. RISC-V 보안 — PMP (Physical Memory Protection), sPMP
13. RISC-V 하이퍼바이저 확장 (H)
14. StarFive JH7110 — RISC-V SoC, Star64 보드
15. EsperessIF ESP32-P4 — RISC-V MCU, WiFi6
16. RISC-V in 우주 — NASA 위성 적용 사례

---

## 7. GPU 아키텍처 심화 — 32개

1. GPU (Graphics Processing Unit) 개요 — SIMT 실행 모델, 수천 코어
2. GPU 용도 분화 — 그래픽 렌더링 vs AI 훈련/추론 vs HPC
3. NVIDIA Ampere (A100) — 80GB HBM2e, 6912 CUDA, 312 TFLOPS FP16
4. NVIDIA Hopper (H100) — 80GB HBM3, SXM5, Transformer Engine FP8, NVLink 4.0
5. NVIDIA Hopper (H200) — 141GB HBM3e, 4.8TB/s 대역폭
6. NVIDIA Blackwell (B100/B200) — 192GB HBM3e, 5세대 NVLink, FP4 지원
7. NVIDIA GB200 NVL72 — 72개 B200, 130TB HBM, 1.4 엑사FLOPS
8. NVIDIA Ada Lovelace (RTX 40 시리즈) — 4세대 텐서 코어, DLSS 3
9. TENSOR CORE — 행렬 곱 전용 하드웨어, FP16/BF16/TF32/FP8/INT8
10. CUDA 코어 vs 텐서 코어 vs RT 코어 — 역할 비교
11. Streaming Multiprocessor (SM) — CUDA 실행 단위, Warp Scheduler
12. Warp — 32 스레드 묶음, SIMT 동기 실행
13. Warp Divergence — 분기로 인한 직렬화 성능 저하
14. CUDA 메모리 계층 — Global / Shared / L1/L2 Cache / Register
15. Shared Memory Bank Conflict — 동시 접근 충돌, 패딩으로 해결
16. 점유율 (Occupancy) — SM당 Warp 수, 레이턴시 은폐 핵심
17. AMD RDNA 3 (RX 7000) — Compute Units, Infinity Cache, 5nm
18. AMD CDNA 3 (MI300X) — 데이터센터/AI, 192GB HBM3, 5.3 TB/s
19. AMD MI300A — APU 형태, CPU+GPU+HBM3 통합 다이
20. AMD Infinity Fabric — CPU-GPU Die 간 고속 연결
21. Intel Arc (Alchemist/Battlemage) — Xe HPG 아키텍처, AV1 인코딩
22. Intel Xe2 (Battlemage) — 성능/전력 효율 개선
23. Intel Gaudi 3 — AI 훈련/추론 가속기, AWS/Azure 제공
24. Google TPU v5p — 행렬 연산 특화, HBM2e, 8960 칩 Pod
25. CUDA 프로그래밍 — Grid/Block/Thread, __ global __, __ shared __
26. cuBLAS / cuDNN / CUTLASS — NVIDIA AI 라이브러리
27. NCCL (NVIDIA Collective Communications Library) — AllReduce/AllGather
28. GPU 클럭 / TDP — 부스트 클럭, 열 조절, Power Limit
29. GPU 폼팩터 — SXM5 / PCIe / OAM (Open Accelerator Module)
30. GPGPU (General Purpose GPU) — CPU 오프로드, 병렬 컴퓨팅
31. OpenCL — 종류 무관 GPGPU 표준 (Intel/AMD/NVIDIA/ARM 지원)
32. Vulkan / Metal / DirectX 12 — 저수준 GPU API, CPU 오버헤드 최소화

---

## 8. AI 가속기 / 특수 프로세서 — 18개

1. NPU (Neural Processing Unit) — 추론 전용, 저전력, 온디바이스
2. Apple Neural Engine — 16코어, 38 TOPS (M4), Core ML 연동
3. Qualcomm Hexagon DSP+NPU — 73 TOPS (Gen 3), 온디바이스 LLM
4. Samsung Mobileint — Exynos NPU
5. Google TPU v5e/v5p — 교육(v5p)/추론(v5e) 구분
6. AWS Trainium 2 — 훈련 특화, UltraCluster
7. AWS Inferentia 2 — 추론 특화, inf2 인스턴스
8. Cerebras WSE-3 — 웨이퍼 스케일 엔진, 900K 코어, 44GB SRAM
9. Groq LPU (Language Processing Unit) — SRAM 기반, 빠른 추론, 500+ tok/s
10. Habana Gaudi 3 (Intel) — AI 훈련, PCIe/OAM
11. SambaNova SN40L — Reconfigurable Dataflow Unit
12. Graphcore IPU (Intelligence Processing Unit) — 벌크 동기 병렬
13. Tenstorrent Wormhole — RISC-V 기반 오픈 AI 칩
14. DSP (Digital Signal Processor) — 곱셈-누산(MAC), 실시간 신호처리
15. FPGA (Field Programmable Gate Array) — 재구성 가능, Microsoft Azure NPU
16. ASIC (Application-Specific IC) — BitCoin 채굴 칩, Google TPU
17. PIM (Processing In Memory) — DRAM 내부에서 연산, Samsung HBM-PIM
18. CIM (Compute In Memory) — 아날로그 연산, 에너지 효율↑

---

## 9. 메모리 시스템 심화 — 30개

1. 메모리 계층 구조 — 레지스터 → L1/L2/L3 캐시 → DRAM → NVMe → HDD
2. 지역성 원리 — 시간적(Temporal) / 공간적(Spatial) / 순서(Sequential)
3. L1 캐시 — 분리(I$+D$), 1~4 사이클, 32~64KB
4. L2 캐시 — 통합, 5~15 사이클, 256KB~1MB
5. L3 캐시 — 공유, 30~60 사이클, 수십MB (AMD 3D V-Cache: 192MB)
6. AMD 3D V-Cache — 캐시 수직 적층 (TSMC SoIC), 게임/서버 성능↑
7. 캐시 매핑 — 직접 / 완전 연관 / N-Way 집합 연관 (실제: 8~16-way)
8. 캐시 교체 정책 — LRU / pLRU / NRU / FIFO / Random
9. 캐시 쓰기 정책 — Write-Through / Write-Back + Write-Allocate
10. 캐시 일관성 — MESI / MESIF / MOESI 프로토콜
11. MESI 상태 — Modified / Exclusive / Shared / Invalid
12. False Sharing — 같은 캐시 라인, 다른 변수 수정 → 성능 저하
13. DRAM 종류 — DDR4 / DDR5 / LPDDR5 / LPDDR5X
14. DDR5 특성 — DDR4 대비 2배 대역폭, On-Die ECC, 4800~8400 MT/s
15. HBM (High Bandwidth Memory) — 수직 적층 DRAM, TSV
16. HBM2 → HBM2e → HBM3 → HBM3e — 세대별 대역폭 (HBM3e: 1.2TB/s/스택)
17. HBM 적층 — 8~16 Die 적층, TSV(Through-Silicon Via), μ bump
18. CoWoS (Chip on Wafer on Substrate) — TSMC 2.5D 패키징, B200
19. SoIC (System on Integrated Chips) — TSMC 3D 적층, AMD 3D V-Cache
20. InFO (Integrated Fan-Out) — TSMC, Apple M1 패키징
21. 메모리 인터리빙 — 채널 병렬 접근, 대역폭↑
22. ECC (Error Correcting Code) 메모리 — SECDED, 서버 필수
23. NVDIMM — 비휘발성 DIMM, 배터리 백업 DRAM
24. Optane (Intel 3D XPoint) — DRAM-NVMe 중간 계층, 단종 (2022)
25. CXL (Compute Express Link) 메모리 — CPU-가속기-메모리 공유 풀
26. CXL 1.1 / 2.0 / 3.0 — 메모리 공유 진화, 메모리 풀링
27. 가상 메모리 — 페이지 테이블, TLB, 요구 페이징
28. Huge Page (대형 페이지) — 2MB/1GB, TLB 미스↓
29. NUMA (Non-Uniform Memory Access) — 소켓별 로컬/원격 메모리
30. 행 해머 (RowHammer) — DRAM 보안 취약점, TRR/PARA 방어

---

## 10. 저장장치 / IO 인터페이스 — 20개

1. NVMe (Non-Volatile Memory Express) — PCIe 기반, 저지연 SSD 프로토콜
2. NVMe 세대 — PCIe 3.0 (3.5GB/s) → 4.0 (7GB/s) → 5.0 (14GB/s)
3. SATA SSD vs NVMe SSD — 속도 비교 (SATA: 550MB/s vs NVMe: 7GB+)
4. 3D NAND 플래시 — TLC/QLC/PLC 적층, 200+ Layer
5. Z-NAND / Z-SSD — 삼성, ZNS 표준, 초저지연 NVMe
6. ZNS (Zoned Namespace) — SSD 수명/성능, Zone 기반 관리
7. RAID 레벨 — 0(스트라이프)/1(미러)/5(분산패리티)/6(이중패리티)/10
8. NVMe-oF (NVMe over Fabrics) — FC/RDMA/TCP가 fabric 통해 원격 NVMe
9. RDMA (Remote Direct Memory Access) — CPU 우회 메모리 복사
10. iSCSI — TCP/IP 기반 원격 스토리지 블록 접근
11. PCIe 버스 — 레인(Lane) × 2.5/5/8/16/32/64 GT/s (Gen1~6)
12. PCIe 6.0 — 64 GT/s, 128GB/s (×16), PAM4 신호
13. USB4 / Thunderbolt 4 — 40Gbps, Alt Mode DP/PCIe, 최대 100W PD
14. SATA vs PCIe 폼팩터 — M.2 / U.2 / E.1 / EDSFF
15. HDD 헤드/플래터 — HAMR/MAMR 차세대 자기 기록
16. SSD 수명 — TBW (Total Bytes Written), DWPD
17. NVMe 네임스페이스 — 논리 스토리지 단위, 멀티 네임스페이스
18. 스토리지 클래스 메모리 (SCM) — DRAM과 NAND 사이 계층
19. IOPS / 순차/랜덤 읽기쓰기 — 스토리지 성능 지표
20. 파일 시스템별 특성 — EXT4 / XFS / Btrfs / ZFS / F2FS / APFS

---

## 11. 인터커넥트 / 칩렛 / 첨단 패키징 — 22개

1. 칩렛 (Chiplet) — 기능별 소형 다이 조합, 수율↑ / 비용↓
2. UCIe (Universal Chiplet Interconnect Express) — 칩렛 간 표준 인터페이스
3. AMD MCM (Multi-Chip Module) — EPYC: Zen 코어 칩렛 + I/O 다이
4. Intel Foveros — 3D 스택 패키징, CPU+GPU+IP 블록 수직 통합
5. Intel EMIB (Embedded Multi-die Interconnect Bridge) — 2.5D 고속 브리지
6. TSMC CoWoS-S/L/R — 2.5D SiP 패키징, NVIDIA H100/B200
7. Samsung H-Cube — HBM+Logic 이종 3D 통합
8. NVLink — NVIDIA GPU 간 고대역폭 직결, NVLink 5.0: 1.8TB/s
9. NVSwitch — NVLink 스위칭 허브, All-to-All 연결
10. Infinity Fabric (AMD) — Zen CPU + HBM + GPU 통합 연결
11. CCIX (Cache Coherent Interconnect for Accelerators) — ARM 이종 코히어런스
12. OpenCAPI — IBM, 고대역폭 호스트-가속기 연결
13. Gen-Z — 메모리 쪽 패브릭 (←CXL로 통합됨)
14. CXL 1.1 / 2.0 / 3.0 차이 — 1.1(가속기목적)/2.0(풀링)/3.0(P2P)
15. 실리콘 포토닉스 (Silicon Photonics) — 광 신호로 칩 간 통신, Intel IFS
16. 공동 패키징 광학 (CPO, Co-Packaged Optics) — 스위치+광트랜시버 통합
17. 인터포저 (Interposer) — 실리콘/유리/유기 기판, 칩 간 연결 중간층
18. 팬아웃 패키징 (Fan-Out) — FOWLP, TSMC InFO
19. 적층 다이 (3D-IC Stacking) — 면대면(F2F)/TSV 관통, 단거리 배선
20. TSV (Through-Silicon Via) — 수직 전기 연결, HBM/3D-IC 핵심
21. 미세범프 (Micro Bump) — 다이 적층 연결, μ-pillar
22. 웨이퍼-레벨 패키징 (WLP) — 웨이퍼 형태로 패키징

---

## 12. 반도체 공정 / 제조 — 16개

1. CMOS 공정 — NMOS+PMOS 상보적 구조, 저전력
2. 공정 노드 진화 — 16nm → 7nm → 5nm → 3nm → 2nm → 1.8nm
3. TSMC 공정 — N3 (3nm) / N3E / N2 (2nm 예정 2025)
4. Intel 공정 — Intel 4 (7nm급) / Intel 3 / Intel 20A(GAA) / Intel 18A
5. Samsung 공정 — SF3 (3nm GAA) / SF2 (2nm GAA 예정)
6. FinFET (Fin Field-Effect Transistor) — 3D 핀 채널, 7nm/5nm
7. GAA (Gate-All-Around) FET — 3nm/2nm 이하, MBCFET (Samsung)
8. 나노시트 FET (Nanosheet) — Intel / Samsung 2nm급
9. EUV (Extreme Ultraviolet) 리소그래피 — 13.5nm 파장, ASML 독점
10. High-NA EUV — 개구수 0.55, 2nm 이하 필수, ASML EXE:5000
11. 이중 패터닝 (SADP/SAQP) — EUV 전 해상도 보완 기법
12. 도핑 (Doping) — N형 (인/비소) / P형 (붕소) 반도체
13. 반도체 소재 — 실리콘(Si) / GaN / SiC / Ge / InGaAs 비교
14. GaN (질화갈륨) — 전력 반도체, 고전압/고주파, 5G PA
15. SiC (탄화규소) — 전기차 인버터, 고온 고전압
16. 반도체 공급망 — ASML(장비)/TSMC(파운드리)/SMIC(중국) 지정학

---

## 13. 병렬 처리 / 멀티코어 — 18개

1. 플린의 분류 (Flynn's Taxonomy) — SISD / SIMD / MISD / MIMD
2. 다중 코어 (Multi-Core) — 단일 다이에 복수 코어, LLC 공유
3. 하이퍼스레딩 (HT) / SMT — 물리 코어당 2+ 논리 스레드
4. SMP (Symmetric MultiProcessing) — 공유 메모리, 동등 CPU
5. NUMA — 소켓별 로컬 메모리, 원격 접근 고비용
6. cc-NUMA — 캐시 일관성 지원 NUMA, 현대 서버 표준
7. 클러스터 (Cluster) — 네트워크 연결 노드, MPI 통신
8. MPP (Massively Parallel Processing) — 수천 노드, 독립 메모리
9. GPU 클러스터 — InfiniBand + NVLink, AI 훈련
10. 하이브리드 코어 (P-Core + E-Core) — Intel Alder Lake, ARM big.LITTLE
11. 코어 간 캐시 일관성 — MOESI / MESIF 스누핑 or 디렉터리 방식
12. 스레드 수준 병렬성 (TLP, Thread-Level Parallelism)
13. 명령어 수준 병렬성 (ILP, Instruction-Level Parallelism)
14. 데이터 수준 병렬성 (DLP, Data-Level Parallelism) — SIMD
15. 암달 법칙 (Amdahl's Law) — 순차 부분이 병렬화 이익 한계
16. 구스타프슨 법칙 (Gustafson's Law) — 문제 크기 확장 시 선형 가속
17. 원자 연산 (Atomic Operations) — CAS / Fetch-and-Add, Lock-free
18. 메모리 일관성 모델 — SC / TSO / Relaxed (x86=TSO, ARM=Relaxed)

---

## 14. 수 표현 / 오류 감지 — 14개

1. 2의 보수 (Two's Complement) — 음수 표현, 덧셈 통일
2. IEEE 754 단정도 (32비트) — 부호(1)/지수(8)/가수(23), 바이어스 127
3. IEEE 754 배정도 (64비트) — 부호(1)/지수(11)/가수(52)
4. BF16 (Brain Float 16) — 기계학습용, 단정도와 같은 지수 범위
5. FP8 (E4M3/E5M2) — AI 추론 양자화, NVIDIA Hopper 지원
6. 고정 소수점 — 정수 연산, DSP/MCU
7. BCD (Binary Coded Decimal) — 십진수 코딩, Packed BCD
8. 문자 코드 — ASCII(7bit) / UTF-8 / UTF-16 / UTF-32 / Unicode
9. 패리티 비트 — 홀수/짝수 패리티, 1비트 오류 검출
10. 해밍 코드 — 오류 수정, p 위치에 검사 비트
11. CRC (Cyclic Redundancy Check) — 다항식 나눗셈, 통신 오류 검출
12. SECDED (Single Error Correct, Double Error Detect) — 서버 ECC 메모리
13. 체크섬 (Checksum) — 합산 기반 단순 오류 검출
14. 전달 오류 부호 — Turbo Code / LDPC / Polar Code — 채널 코딩

---

## 15. 양자 컴퓨팅 / 미래 아키텍처 — 14개

1. 양자 컴퓨팅 원리 — 중첩(Superposition) / 얽힘(Entanglement) / 측정(Measurement)
2. 큐비트 (Qubit) — 0과 1의 중첩 상태, 블로흐 구
3. 양자 게이트 — X/Y/Z/H/CNOT/Toffoli 게이트
4. 양자 회로 (Quantum Circuit) — 큐비트 초기화 → 게이트 → 측정
5. 큐비트 구현 기술 — 초전도/이온트랩/광자/실리콘 스핀/중성 원자
6. NISQ (Noisy Intermediate-Scale Quantum) — 오류 있는 5~1000 큐비트 시대
7. 양자 오류 수정 (QEC) — 표면 코드, 논리 큐비트 수천 물리 큐비트 필요
8. 양자 우위 (Quantum Advantage/Supremacy) — Google Sycamore 54큐비트 (2019)
9. IBM Quantum (Eagle/Osprey/Condor/Heron) — 127/433/1121 큐비트
10. Google Willow — 105 큐비트, 지수적 오류수정, RCS 문제
11. 양자 알고리즘 — Shor(소인수 분해) / Grover(탐색) / HHL(선형계)
12. 포스트-양자 암호 (PQC) — Kyber / Dilithium / SPHINCS+
13. 뉴로모픽 컴퓨팅 — 뇌 구조 모방, 스파이킹 뉴런, Intel Loihi 2
14. 광 컴퓨팅 (Optical Computing) — 광자 기반 행렬 연산, Lightmatter Passage

---

**총 키워드 수: 320개**
