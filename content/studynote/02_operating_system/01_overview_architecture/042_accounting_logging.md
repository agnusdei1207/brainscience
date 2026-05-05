+++
title = "042. 회계 및 로깅 (Accounting and Logging)"
weight = 42
date = "2026-04-05"
[extra]
categories = "studynote-operating-system"
+++

## 0. 핵심 인사이트

> **핵심**: 회계 및 로깅 (Accounting and Logging)은(는) 운영체제가 자원을 추상화하고 통제하는 과정에서 성능, 보호, 응답성을 동시에 조율하기 위해 필요한 핵심 개념이다.
> **비유**: 회계 및 로깅 (Accounting and Logging)은(는) 복잡한 교통을 한 번에 통제해 전체 흐름을 맞추는 신호 체계와 같다.

---

📝 모범 답안

## 1. 개요 및 필요성

```
프로세스 회계 (Process Accounting):

커널이 각 프로세스 종료 시 기록하는 정보:
  - CPU 사용 시간 (사용자 모드 + 커널 모드)
  - 경과 시간 (Wall clock time)
  - 메모리 최대 사용량 (RSS/VSZ)
  - I/O 바이트 수 (읽기/쓰기)
  - 컨텍스트 스위치 횟수
  - 종료 상태 (exit code)

Linux 프로세스 회계:
  패키지: acct (BSD) / sysstat
  활성화: accton /var/log/pacct
  조회:  lastcomm (최근 명령 기록)
         sa (통계 요약)

/proc 파일시스템:
  /proc/[PID]/stat   : 프로세스 상태/자원
  /proc/[PID]/status : 사람이 읽을 수 있는 형태
  /proc/[PID]/io     : I/O 통계

활용:
  클라우드 과금: 컨테이너 CPU/메모리 사용량 측정
  용량 계획: 시간대별 자원 소비 패턴 분석
  SLA 보고: 서비스별 자원 사용 보고서
```

> 📢 **섹션 요약 비유**: 프로세스 회계는 회사 경비 시스템 — 직원(프로세스)이 무엇을 얼마나 썼는지 자동 기록, 나중에 부서별 청구서 발행.

---

## 2. 구성요소

```
Linux 로깅 아키텍처:

커널 → [dmesg 링 버퍼] → 부팅 로그
     ↓
커널/사용자 공간 → syslog() 시스템 콜 → rsyslog/syslog-ng
     ↓
서비스 (systemd) → [journald] → /var/log/journal

/var/log 주요 파일:
  /var/log/messages : 일반 시스템 메시지 (RHEL)
  /var/log/syslog   : 일반 로그 (Ubuntu/Debian)
  /var/log/auth.log : 인증 이벤트 (sudo, ssh)
  /var/log/kern.log : 커널 메시지
  /var/log/dmesg    : 부팅 시 커널 링 버퍼
  /var/log/secure   : 보안 이벤트 (RHEL)

syslog 우선순위 (Severity Level, RFC 5424):
  0: Emergency (emerg) — 시스템 불안정
  1: Alert        — 즉시 조치 필요
  2: Critical     — 크리티컬 상태
  3: Error        — 오류 조건
  4: Warning      — 경고
  5: Notice       — 중요 정상 상태
  6: Info         — 정보성
  7: Debug        — 디버그 상세 정보

Facility (시설):
  kern(0), user(1), mail(2), daemon(3)
  auth(4), syslog(5), ... local0-7(16-23)
```

> 📢 **섹션 요약 비유**: syslog 우선순위는 병원 응급도 분류(트리아지) — Emergency(즉시 처치), Error(긴급), Warning(주의관찰), Info(일반 정보).

---

## 3. 구조 및 원리

**핵심 조건**: 운영체제의 해당 메커니즘은 현재 상태 정보, 자원 제약, 정책 기준이 함께 정합성을 가질 때 안정적으로 동작한다.

동작 순서:
1. **요청 또는 이벤트 발생**: 사용자 요청, 인터럽트, 시스템 호출 등으로 커널이 해당 기능을 처리할 필요가 생긴다.
2. **현재 상태 확인**: 커널은 큐, 제어 블록, 메타데이터, 자원 가용량을 확인해 실행 가능 여부와 우선순위를 판단한다.
3. **정책 적용 및 자원 배정**: 해당 주제의 핵심 정책에 따라 상태 전이, 자원 할당, 보호 검사를 수행한다.
4. **결과 반영 및 후속 처리**: 처리 결과를 시스템 상태에 기록하고 다음 인터럽트·스케줄링·복구 단계로 연결한다.

```
전통 vs 구조화 로그:

전통 텍스트 로그:
  "2025-04-05 10:30:45 ERROR Connection refused to DB"
  단점: 파싱 어려움, 비정형, 검색 비효율

구조화 로그 (JSON):
  {
    "timestamp": "2025-04-05T10:30:45Z",
    "level": "ERROR",
    "message": "Connection refused",
    "service": "api-server",
    "target": "db-primary",
    "user_id": "u-12345",
    "trace_id": "abc123"
  }
  장점: 자동 파싱, 필드 검색, 집계 용이

로그 수집 파이프라인:

[앱/서버]
  → Filebeat / Fluentd (수집)
  → Logstash / Fluentd (변환/필터)
  → Elasticsearch (저장/인덱싱)
  → Kibana (시각화/검색)

클라우드 네이티브:
  AWS CloudWatch Logs
  GCP Cloud Logging
  Azure Monitor Logs

OpenTelemetry:
  Logs + Traces + Metrics 통합 수집
  벤더 중립 표준 (CNCF 프로젝트)
```

> 📢 **섹션 요약 비유**: 구조화 로그 → ELK는 도서관 카탈로그 시스템 — 산더미 책(로그)을 저자·제목·장르(필드)로 분류해 1초에 원하는 책 검색.

---

## 4. 비교 및 연결

```
전통 vs 구조화 로그:

전통 텍스트 로그:
  "2025-04-05 10:30:45 ERROR Connection refused to DB"
  단점: 파싱 어려움, 비정형, 검색 비효율

구조화 로그 (JSON):
  {
    "timestamp": "2025-04-05T10:30:45Z",
    "level": "ERROR",
    "message": "Connection refused",
    "service": "api-server",
    "target": "db-primary",
    "user_id": "u-12345",
    "trace_id": "abc123"
  }
  장점: 자동 파싱, 필드 검색, 집계 용이

로그 수집 파이프라인:

[앱/서버]
  → Filebeat / Fluentd (수집)
  → Logstash / Fluentd (변환/필터)
  → Elasticsearch (저장/인덱싱)
  → Kibana (시각화/검색)

클라우드 네이티브:
  AWS CloudWatch Logs
  GCP Cloud Logging
  Azure Monitor Logs

OpenTelemetry:
  Logs + Traces + Metrics 통합 수집
  벤더 중립 표준 (CNCF 프로젝트)
```

> 📢 **섹션 요약 비유**: 구조화 로그 → ELK는 도서관 카탈로그 시스템 — 산더미 책(로그)을 저자·제목·장르(필드)로 분류해 1초에 원하는 책 검색.

---

## 5. 실무 적용 및 판단

```
보안 감사 로그 (Audit Log):

요구사항:
  변조 불가능 (Tamper-evident)
  원본 유지 (Integrity)
  접근 제어 (Access Control)
  보존 기간 (Retention)

보안 이벤트 필수 기록:
  로그인/로그아웃 성공/실패
  권한 상승 (sudo, su)
  파일 접근/수정/삭제 (중요 파일)
  네트워크 연결 시도
  사용자/그룹 생성/변경/삭제

Linux 감사 시스템 (auditd):
  /etc/audit/audit.rules : 감사 규칙
  ausearch : 감사 로그 검색
  aureport : 요약 보고서

로그 보존 규제:
  ISO 27001: 보안 이벤트 최소 1년
  GDPR (EU): 개인정보 처리 로그 최소 3년
  PCI DSS: 카드 데이터 환경 로그 1년
  금융: 거래 로그 5~10년 (국내 규제)

로그 무결성 보장:
  WORM Storage (Write Once Read Many)
  해시 체인 (각 로그에 이전 해시 포함)
  원격 로그 서버 전송 (로컬 삭제 방지)
```

> 📢 **섹션 요약 비유**: 감사 로그는 CCTV — 무슨 일이 있었는지 증거로 남기고, 삭제·조작이 어렵고, 규정된 기간 동안 보관해야 한다.

---

## 6. 기대효과 및 결론

```
금융 서비스 장애 원인 분석 사례:

증상:
  오전 9:00~9:30 API 응답 시간 3초 이상
  사용자 민원 200건 접수

로그 분석 과정:

1. 애플리케이션 로그 확인:
  Kibana 쿼리: level:ERROR AND service:api AND
              time:[09:00 TO 09:30]
  결과: DB connection timeout 에러 다수 발견

2. DB 로그 확인:
  MySQL slow query log 확인
  → 09:05~09:28 특정 쿼리 30초 이상 실행

3. OS 시스템 로그:
  /var/log/syslog 확인
  → 09:04 디스크 I/O 경보 로그 발견
  "I/O error on device sdb, logical block 12345"

4. 커널 로그 (dmesg):
  → 디스크 불량 섹터 감지 로그 발견
  → RAID 배열 재구성 시작 → I/O 지연 → 쿼리 지연

근본 원인:
  물리 디스크 불량 섹터 → RAID 재구성
  → DB I/O 지연 → 쿼리 타임아웃 → API 지연

해결:
  디스크 교체 완료 (11:00)
  재발 방지: 디스크 S.M.A.R.T 모니터링 추가
```

> 📢 **섹션 요약 비유**: 로그 분석은 의료 부검 — 애플리케이션(증상)→DB(기관)→OS(조직)→하드웨어(세포) 순서로 원인을 파고들어 근본 원인 발견.

---

## 7. 발전 흐름도

```
[syslog 표준화 (BSD Unix, 1980s)]
프로세스 회계, syslog 도입
RFC 3164 (2001) → RFC 5424 (2009)
      |
      v
[ELK Stack 등장 (Elasticsearch 2010, Kibana 2013)]
대규모 로그 중앙 집중 검색/시각화
      |
      v
[구조화 로그 표준화 (2015~)]
JSON 로그, 12-Factor App 원칙
      |
      v
[OpenTelemetry (2019~, CNCF)]
Metrics + Traces + Logs 통합 수집
벤더 중립 표준 추진
      |
      v
[현재: AI 기반 로그 분석]
LLM으로 로그 패턴 자동 분류
AIOps: 이상 탐지 자동화
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 회계 및 로깅 (Accounting and Logging) | 운영체제 자원 관리와 보호 정책이 실제로 적용되는 핵심 주제 |
| 커널 (Kernel) | 정책 집행, 상태 전이, 시스템 호출 처리의 중심 |
| 프로세스/스레드 | CPU, 메모리, 동기화 자원과 직접 연결되는 실행 단위 |
| 메모리/I/O | 성능 병목과 보호 요구사항이 함께 드러나는 연계 영역 |
| 가상화/보안 | 격리, 제어, 관측 확장 관점에서 해당 주제가 연결되는 상위 개념 |
