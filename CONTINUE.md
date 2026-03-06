# BrainScience PE 콘텐츠 작업 추적

- 2026-03-06: 폴더 구조 키워드 리스트에 맞체 전면 재구성 (16개 과목 모두 완료)

## ⚠️ 작업 원칙 (Rule)

1. **압도적 디테일**: 기술사 답안지 수준의 상세한 백서술. **코드 스니펫**: 가능하면 프로그래밍 코드 스니펫 없음
2. **배치 작업**: 10개 단위 작성 후 반드시 `git push` 및 `CONTINUE.md` 최신화.
3. **체계적 넘버링**: 키워드 리스트`(_keyword_list.md)` 순서를 엄격히 준수.
4. **문서 업데이트**: 진행현황 실시간으로 업데이트.
5. **병렬 처리**: 2-3개 키워드를 병렬로 작성 (한 번에 `git commit` 후 `git push`)

---

## 📊 진행현황 (2026-03-06)

### 1. 컴퓨터구조 (Computer Architecture) - Section 1 진행중
- ✅ 1-50: 전압~D 래치 (기초 전기전자 및 디지털 논리회로)
  - 46: 에지 트리거 (Edge Trigger)
  - 47: 레벨 트리거 (Level Trigger)
  - 48: 래치 (Latch)
  - 49: SR 래치
  - 50: D 래치
- 📝 51-64: 플립플롭, 레지스터, 카운터 (예정)
- 📝 65-80: 메모리, 인터페이스 (예정)

### 2. 운영체제 (Operating System) - Section 1 진행중
- ✅ 1-21: OS 목적~인터럽트 핸들러 (운영체제 개요 및 아키텍처)
  - 17: 하드웨어 인터럽트 (비동기적)
  - 18: 소프트웨어 인터럽트 / 트랩 (Trap) / 예외 (Exception)
  - 19: 인터럽트 벡터 (Interrupt Vector)
  - 20: 인터럽트 서비스 루틴 (ISR, Interrupt Service Routine)
  - 21: 인터럽트 핸들러 (Interrupt Handler)
- 📝 22-34: 커널, 부팅, 문맥교환 (예정)

### 3. 데이터통신/네트워크 (Network) - Section 1 진행중
- ✅ 1-4, 7-17: 통신구성요소~전송 지연 (데이터통신 기초)
  - 13: 대역폭 (Bandwidth), 대역폭-효율성 관계
  - 14: 처리량 (Throughput) / 굿풋 (Goodput)
  - 15: 지연 (Latency/Delay) - 데이터 관점
  - 16: 전파 지연 (Propagation Delay) - 거리/속도
  - 17: 전송 지연 (Transmission Delay) - 패킷길이/대역폭
- 📝 18-25: 큐잉 지연, 처리 지연, 채널용량, 잡음 (예정)

### 4. 소프트웨어공학 (Software Engineering) - Section 1 진행중
- ✅ 1-12, 13-22: SE 기초~형상 통제
  - 18: PSP (Personal Software Process) / TSP (Team Software Process)
  - 19: 소프트웨어 제품 라인 (SPL, Software Product Line)
  - 20: 형상 관리 (SCM, Software Configuration Management)
  - 21: 형상 식별 (Configuration Identification) - 형상 항목(CI) 선정
  - 22: 형상 통제 (Configuration Control) - 변경 제어 위원회(CCB)
- 📝 23-35: 형상 감사, 버전 관리, 재공학, 역공학 (예정)

### 5. 데이터베이스 (Database) - Section 1 진행중
- ✅ 1-21: DIKW~DML (데이터베이스 기초 및 아키텍처)
  - 17: 관계형 데이터 모델 (Relational Model)
  - 18: 객체지향 데이터 모델 (OODBMS) / 객체 관계형 데이터 모델 (ORDBMS)
  - 19: DBMS 언어
  - 20: DDL (Data Definition Language)
  - 21: DML (Data Manipulation Language)
- 📝 22-34: DCL, TCL, 절차적/비절차적 DML, 관리자 (예정)

### 6-16. 기타 과목 (예정)
- ICT 융합, 기업시스템, 알고리즘/통계, 보안, AI 등

---

## 📝 다음 작업 (Next Batch)

**우선순위:**
1. CA 51-55: 플립플롭 (SR, D, JK, T, 마스터-슬레이브)
2. OS 22-26: 커널의 역할, 모놀리식 커널, 마이크로 커널, 하이브리드 커널, 엑소 커널
3. NW 18-22: 큐잉 지연, 처리 지연, 나이퀴스트 채널 용량, 샤논의 채널 용량, 심볼 상호 간섭
4. SE 23-27: 형상 감사, 형상 기록/보고, 기준선, 버전 관리 시스템, 변경 관리 프로세스
5. DB 22-26: DCL, TCL, 절차적/비절차적 DML, DBA, DA

---

## 📈 통계 (Statistics)

| 과목 | 완료 | 진행중 | 전체 | 비율 |
|------|------|--------|------|------|
| CA   | 50   | -      | 1000+ | 5.0% |
| OS   | 21   | -      | 800+  | 2.6% |
| NW   | 17   | -      | 1200+ | 1.4% |
| SE   | 22   | -      | 800+  | 2.8% |
| DB   | 21   | -      | 800+  | 2.6% |
| **합계** | **131** | - | **~4800** | **2.7%** |

---

## 📁 최근 커밋

- `ed3697f` - feat: add 22 PE keywords across 5 subjects (2026-03-06)
- `abc313c` - feat: add 20 PE keywords across 5 subjects (2026-03-06)