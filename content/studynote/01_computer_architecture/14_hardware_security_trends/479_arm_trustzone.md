+++
weight = 479
title = "479. ARM TrustZone"
date = "2026-03-20"
[extra]
categories = "studynote-computer-architecture"
+++
## 0. 핵심 인사이트

> **핵심**: ARM TrustZone은 ARM 프로세서의 하드웨어 확장 기능으로, 시스템 전체를 Normal World(일반 구역)와 Secure World(보안 구역)로 분리하여, 보안 구역의 메모리와 주변기기에 대한 접근을 CPU 수준에서 차단하는 Mobile/Secure MCU의 사실상 표준 보안 아키텍처다.
> 2. **가치**: 삼성페이, 애플페이 등 모바일 결제, 지문/안면 인식, DRM 복호화에 필수적이며, Secure World는 일반 OS가 손상되더라도银行アプリ나 생체 정보에 접근할 수 없어, 전 세계 数十억台の 모바일 기기를 보호한다.
> 3. **융합**: TrustZone은 TEE (Trusted Execution Environment)의 대표적인 구현체로, Secure Boot, HSM 기능과 결합되어 ARM 기반 IoT, Automotive,莓エディタル트랜스フォーメ이션 보안의 핵심 기반 기술이 된다.

> 📝 모범 답안

# ARM TrustZone (트러스트존)

---

## 1. 개요 및 필요성

### 탄생 배경: 모바일 보안의 필요성

2010년 이전의 스마트폰은 별도의 보안 하드웨어 없이 일반 프로세서에서 모든 코드를 실행했다. 그러나 스마트폰이 은행 거래, 모바일 결제, 개인 건강 정보 등을 처리하게 되면서, 전용 보안 하드웨어에 대한 수요가 급증했다. ARM은 2003년 ARM1176JZ(F)-S 프로세서부터 TrustZone을 도입하여, 추가 비용 없이도 단일 프로세서에서 두 개의 격리된 실행 환경을 제공할 수 있게 했다.

TrustZone의 핵심 기여는"보안을 위해 별도의 보안 코프로세서를 설계할 필요 없이,既存のプロセッサー拡張만으로 하드웨어 격리"를 실현한 것이다. これにより 스마트폰의 비용과 전력 소비를 늘리지 않고도银行级 보안을 달성할 수 있었다.

### Threat 모델

TrustZone이対処하는威胁모델는 다음과 같다. OS 수준 공격에서는 Android/iOS 커널 취약점으로 인해 Malware가 root 권한을 획득하는 경우, Normal World 전체가 손상되지만 Secure World는 여전히 안전하다. Physical 접근 공격에서는 도난된 기기에서 NAND 메모리를 추출하여 분석하려는 경우, Secure World의 데이터는 키가 없으면 복호화할 수 없다. DMA 공격에서는 PCIe나 USB의 DMA를 통해 메모리에 직접 접근하려는 경우, TrustZone은 TZASC를 통해 이러한 접근도 차단한다.

**💡 비유**: TrustZone은 하나의 건물에"일반 출입증"과"특급 보안 카드" 두 종류를 도입한 것과 같다. 일반 사원증으로는 普通 직원 공간만 출입 가능하지만, 특급 보안 카드가 있으면 Server Room(보안 메모리)까지 출입 가능하다. 카드를 도난당해도(OS 해킹)特급 카드 없이는Server Room에 접근할 수 없다.

---

## 2. 구성요소

### NS (Non-Secure) 비트의 역할

TrustZone의 동작原理는 매우elegant하다. 프로세서의 상태 레지스터(CSR) 내에 NS 비트가 추가되어, 이 비트가 0이면 Secure World, 1이면 Normal World에서 실행되고 있음을 나타낸다. 모든 메모리 접근, 인터럽트 처리, 캐시 동작이 NS 비트에 따라 접근 권한이 결정된다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    TrustZone 상태 비트 (NS 비트) 동작                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  NS Bit = 0 (Secure World)                                         │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • Secure World 코드만 실행 가능                                 │   │
│  │ • Secure 메모리 + Normal 메모리 모두 접근 가능                  │   │
│  │ • 보안 주변기기 (지문 센서,加密加速기) 접근 가능               │   │
│  │ • Secure OS 및 Trusted Application 실행                        │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  NS Bit = 1 (Normal World)                                        │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ • Normal World 코드만 실행 가능                                │   │
│  │ • Normal 메모리만 접근 가능                                    │   │
│  │ • Secure 메모리 접근 시도 → Abort 예외 발생                   │   │
│  │ • 일반 OS (Android, iOS) 및 일반 앱 실행                     │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ────────────────────────────────────────────────────────────────   │
│                                                                     │
│  NS 비트 제어:                                                     │
│  • SMC (Secure Monitor Call) 명령어로만 NS 비트 변경 가능          │
│  • 다른任何 방법으로는 NS 비트 직접 조작 불가                         │
└─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** NS 비트의 설계는巧緻하다. Secure World는 양방향(자신과 상대방 모두)에 접근 가능하지만, Normal World는 Secure World에 대한 접근이Hardware적으로 차단된다. 이는 Secure World가"능동적으로" Normal World의 리소스를 활용하면서도, Normal World가 Secure World에"수동적으로" 접근을 시도하면即時 차단됨을 의미한다. SMC 명령어로만 World 전환이 가능하다는 점도重要하다 — 다른 어떤 방법(Software interrupt, Exception 등)으로도 Secure World로非法 진입이 불가능하다.

### TZASC (TrustZone Address Space Controller)

TZASC는 TrustZone의 메모리 격리를実現하는 버스 레벨 주변기기다. 물리적 메모리 주소를Secure과 Normal 구역으로 매핑하여, Normal World에서 Secure 영역 주소에 접근하려고 하면 Transaction이 Abort된다. TZASC는 Boot 시 Secure OS가 설정하며, 이후 Normal World에서 수정할 수 없다.

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    TZASC 메모리 영역 분할 예시                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  물리 메모리 공간:                                                  │
│                                                                     │
│  0x00000000 ┌─────────────────────────────────────────────────┐   │
│             │                                                 │   │
│             │  Normal World 메모리 (Android, iOS 등)             │   │
│             │  NS Bit = 1 만 접근 가능                          │   │
│             │                                                 │   │
│  0x40000000 ├─────────── Secure/NS 분할선 ─────────────────────┤   │
│             │                                                 │   │
│             │  Secure World 메모리 (TrustZone OS, TA)           │   │
│             │  NS Bit = 0 만 접근 가능 (Normal World는 접근 불가)│   │
│             │                                                 │   │
│  0x80000000 └─────────────────────────────────────────────────┘   │
│                                                                     │
│  • Normal World에서 Secure 주소 접근 시도 → Bus Error/Abort          │
│  • Secure World는 Normal 주소에 자유롭게 접근 가능                    │
│  • TZASC는 Boot 시 Secure OS가 초기화, 이후 Lock                  │
│  • MMU와 연동되어 Virtual Address도 함께 분할                      │
└─────────────────────────────────────────────────────────────────────┘
```

**[다이어그램 해설]** TZASC의 동작은 개념적으로 Simple하지만実装では非常に正確である。Normal World의 프로세서가 Secure World 메모리 주소를Virtual Address로マッピングしても、TLB lookup 후 물리 주소로 변환되는 과정에서 TZASC가 NS 비트와 주소域を 检查하여, 위반이면 Transaction을 abort한다. 이 abort는 캐시 미스, 버스 접근 등 모든 메모리 관련 동작에 적용되어真正的인 격리를実現한다.

### 인터럽트 분리: TZIC (TrustZone Interrupt Controller)

TZIC는 TrustZone 환경에서 인터럽트優先순위및 라우팅을 제어한다. 보안 주변기기(지문 센서,加密加速기)에서 발생하는 인터럽트는 항상 Secure World로만 라우팅되도록 설정되어, Normal World OS는 보안 주변기기irup이 발생했는지조차 알 수 없다. 이를 통해 Keyboard Logger 등의 Attacks를防止한다.

---

## 3. 구조 및 동작 원리

### TrustZone vs Intel SGX vs Apple Secure Enclave

세 가지 보안 기술은 각각 다른市場과 Threat 모델을 위해 설계되었다. TrustZone은 시스템 전체를 두World로 나누어, 모바일/IoT 환경에서 OS 수준의 격리가 필요한場合に最適이다. Intel SGXはプロセスイrement 단위의 격리를提供し、 PC/서버/클라우드 환경에서特定の 애플리케이션만 보호したい場合に最適이다. Secure Enclave는 Apple의专用品으로,iOS/macOS生态系에 최적화되어 있으며,AES기반의ハードウェア暗号化과 Secure Bootを統合している.

| 구분 | ARM TrustZone | Intel SGX | Apple Secure Enclave |
|:---|:---|:---|:---|
| **격리 단위** | CPU 전체 (World 레벨) | Enclave (프로세스 레벨) | 코프로세서 (Secure Enclave) |
| **메모리 격리** | TZASC (obus 기반) | EPC (메모리 암호화) | AES 엔진 (하드웨어 암호화) |
| **주 용도** | 모바일 결제, DRM, 생체 인식 | HPC, 클라우드 | Apple Pay, Face ID |
| **키 관리** | 이중화 OS 구조 | Enclave 내부 키 관리 | Secure Enclave 전용 |
| **auditor** | ARM, SocVendor | Intel SGX SDK | Apple独自 |

### 과목 융합 관점

- **보안 부팅 (Secure Boot)**: TrustZone은 Secure Boot와紧密结合되어, Boot 시 Secure World의 무결성을 검증하고, 정상적인 경우에만 Secure World를 활성화한다.
- **IoT 보안**: ARM PSA (Platform Security Architecture)는 TrustZone을 기반으로 IoT 장치의 보안 프레임워크를 제공한다.

---

## 4. 비교 및 트레이드오프

### 실무 시나리오

**시나리오 — 모바일 결제 (Samsung Pay)**

Samsung Pay에서 사용자의 카드 정보는 Secure World (TEE) 내부에 저장된다. 결제 시에는 TEE 내부에서만 카드 정보를 읽고 payment token을 생성하므로,万一 Android가 root取证されて也从 TEE 내부 데이터にアクセスすることはできません.

**시나리오 — IoT 기기의 TrustZone 활용**

IoT 센서에서 데이터를 수집할 때, 센서 데이터의authenticityを担保するために、 TrustZone 내에서만 작동하는 Trusted Subsystemがотим measuring値を署名하여 전달한다.万一 메인 OS가 손상되어도,攻击者は署名키にアクセスできない.

### 도입 체크리스트

- [ ] 보안 요구사항에 따라 Secure World의 크기와 권한이 적절히 설계되었는가?
- [ ] Secure OS (Trusty, QSEE 등)의 보안 감사(audit)가 수행되었는가?
- [ ] Secure World와 Normal World 사이のIPC 채널이 설계 시부터 분석되었는가?
- [ ] JTAG 디버그 포트가 제품 출하 시 비활성화되었는가? (否则 물리적 공격에 노출)

### 안티패턴

**안티패턴 — Secure World에 과도한 기능 집중**: 보안 설계 시 Secure World에 너무 많은 기능을 넣으면,Secure OS의 공격 표면이 증가하여万一 버그가 발견되었을 때 영향 범위가 커진다. 최소 권한 원칙에 따라, 반드시 Secure World에서 수행해야 하는 기능만 분리해야 한다.

---

## 5. 실무 적용 및 최적화 기법

### TrustZone 도입 효과

| 구분 | TrustZone 없음 | TrustZone 있음 |
|:---|:---|:---|
| **모바일 결제 보안** | Software만으로 카드 정보 관리 | Secure World 격리 |
| **生体情報 보호** | OS 손상 시 노출 | Secure World isolation |
| **DRM** | Software 解読可能 | Hardware レベル保護 |
| **IoT 인증** | MCU 전체가 단일 trust سطح | 이중화 아키텍처 |

### 미래 전망

ARMv8.3-A부터 Pointer Authentication Code (PAC)와 Branch Target Indicator (BTI)가 추가되어,Control Flow Hijacking攻撃을防止한다. 또한 ARM Confidential Computing Architecture (CCA)는 Realm Management Extension (RME)을 통해, Secure World까지도隔離된"Realm"이라는 새로운 격리 영역을 제공한다.

**📢 섹션 요약 비유**: TrustZone은 컴퓨터 안에 만든"이중 구조 금고"와 같다. 일반 금고(일반 OS)에는 普通 자료가 들어있지만,Super 금고(보안 구역)에는 소중한 열쇠와 비밀이 들어있다.万一 일반 금고가 털려도(악성코드 감염), Super 금고는 여전히 안전하다.

---

### 📌 관련 개념 맵 (Knowledge Graph)

| 개념 | 관계 |
|:---|:---|
| TEE (Trusted Execution Environment) | TrustZone은 TEE의 ARM 계열 구현체 |
| NS 비트 | Normal World와 Secure World를 구분하는 프로세서 상태 비트 |
| TZASC | TrustZone Address Space Controller — 메모리 접근 제어 |
| TZIC | TrustZone Interrupt Controller — 인터럽트 라우팅 제어 |
| SMC (Secure Monitor Call) | World 간 전환을 수행하는唯一의 명령어 |
| Secure World / Normal World | TrustZone의 이중 실행 환경 |
| ARM PSA | TrustZone 기반 IoT 보안 프레임워크 |

---

### 👶 어린이를 위한 3줄 비유 설명

1. **TrustZone은 컴퓨터 안에 두 개의 문을 만든 것**예요. 하나는 일반 열쇠(일반 OS)로 열 수 있고, 다른 하나는 특별 열쇠(보안 카드)가 있어야만 열 수 있어요.万一 일반 열쇠가 도난당해도(악성코드),特別 열쇠 없이는 특별한 방(보안 구역)에 들어갈 수 없어요.

2. 스마트폰에서 지문이나 얼굴로 결제할 때, 지문 센서는 특별한 방(보안 구역) 안에서만 작동해서,万一 스마트폰이 해킹당해도payment에 사용되는 생체 정보나 카드 정보는 노출되지 않아요.

3. TrustZone 기술은ARM이라는 회사에서 만든特別な 보안 기능으로, 全世界的으로数十억 대의 스마트폰, 태블릿, IoT 기기에서"지갑과 같은 중요한 것들"을 지키고 있어요.
