+++
weight = 187
title = "187. 로그 및 ELK Stack (Logs, Centralized Logging)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: 로그(Logs)는 시스템과 애플리케이션에서 발생한 이벤트의 시간 순서 텍스트 기록으로, 장애 원인 분석(RCA)에 필수적인 상세 문맥을 제공하는 옵저버빌리티의 두 번째 기둥이다.
> **비유**: 로그 중앙화는 전국 지사 모든 직원의 업무 일지를 본사 데이터베이스에 자동으로 모으는 것이다. 문제가 생기면 전체 일지를 검색해 원인을 즉시 파악한다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

메트릭이 "서비스가 느리다"라고 알려준다면, 로그는 "왜 느린가"의 답을 담고 있다. `ERROR: 2026-04-21T14:32:01 - DB 연결 실패: connection timeout after 30000ms`처럼 구체적 원인과 컨텍스트를 포함한다.

분산 마이크로서비스 환경에서 로그는 50개 이상의 서비스 각각이 생성한다. 각 서버에 SSH로 접속해 `tail -f /var/log/app.log`하는 것은 불가능하다. 중앙 집중식 로깅(Centralized Logging)이 필수다.

ELK Stack은 이 문제의 표준 오픈소스 해법이다. E(Elasticsearch, 저장·검색), L(Logstash, 수집·변환), K(Kibana, 시각화)로 구성되며, 초당 수백만 건의 로그를 수집하고 밀리초 내 전문 검색(Full-Text Search)이 가능하다. 오늘날은 여기에 Beats(경량 수집기) 또는 Fluentd를 더해 "Elastic Stack"이라고도 부른다.

---

## 2. 구성요소

### ELK Stack 수집 흐름

```
[ELK Stack 중앙화 로깅 아키텍처]

마이크로서비스들
├── Service A: 로그 출력 (stdout/file)
├── Service B: 로그 출력
└── Service C: 로그 출력
         ↓
[수집 에이전트]
  Filebeat / Fluentd / Fluentbit
  (각 노드에 DaemonSet으로 배포)
         ↓
[수집·변환·파싱]
  Logstash / Kafka (버퍼)
  (필드 추출, 필터링, 강화)
         ↓
[저장·인덱싱]
  Elasticsearch 클러스터
  (샤딩, 복제, 역인덱스)
         ↓
[시각화·검색]
  Kibana 대시보드
  (로그 검색, 시각화, 알람)
```

| 컴포넌트 | 역할 | 대안 |
|:---|:---|:---|
| Elasticsearch | 로그 저장, 전문 검색, 인덱싱 | OpenSearch, Splunk |
| Logstash | 로그 수집, 파싱, 변환 | Fluentd, Vector |
| Kibana | 로그 시각화, 검색 UI | Grafana (Loki) |
| Filebeat | 경량 파일 수집기 (Beats 계열) | Fluentbit |

---

## 3. 구조 및 원리

**핵심 조건**: 변경 자동화와 운영 안정성은 별개가 아니라 하나의 루프이며, 빌드·검증·배포·관측·피드백이 끊기지 않아야 지속 개선이 가능하다.

동작 순서:
1. 변경 사항을 버전 관리 시스템에서 감지한다.
2. 빌드·테스트·보안 검증으로 변경의 품질을 빠르게 확인한다.
3. 승인된 산출물을 선언형 배포나 자동화 파이프라인으로 운영 환경에 반영한다.
4. 메트릭·로그·트레이스를 통해 실제 동작 결과를 관측한다.
5. 피드백을 다음 개선 주기에 연결해 반복적으로 신뢰성을 높인다.

### ELK vs Grafana Loki

| 항목 | ELK Stack | Grafana Loki |
|:---|:---|:---|
| 인덱싱 방식 | 전체 내용 인덱싱 (강력한 검색) | 레이블만 인덱싱 (경량) |
| 비용 | 높음 (인덱스 스토리지) | 낮음 |
| 검색 속도 | 빠름 | 상대적으로 느림 |
| Prometheus 통합 | 별도 설정 | 네이티브 통합 |
| 적합 환경 | 대규모, 복잡한 검색 | 쿠버네티스 네이티브, 비용 최적화 |

**구조화 로그 vs 비구조화 로그:**

```json
// 나쁜 예 (비구조화)
"2026-04-21 14:32:01 ERROR User 12345 checkout failed: DB error"

// 좋은 예 (구조화 JSON)
{
  "timestamp": "2026-04-21T14:32:01Z",
  "level": "ERROR",
  "service": "checkout-service",
  "user_id": "12345",
  "event": "checkout_failed",
  "reason": "db_connection_timeout",
  "trace_id": "abc123def456"
}
```

---

## 4. 비교 및 연결

**효과적인 로그 작성 원칙:**
1. **레벨 구분**: DEBUG, INFO, WARN, ERROR, FATAL 적절히 사용
2. **Correlation ID(상관 ID)**: 모든 로그에 Trace ID 포함하여 요청 추적
3. **개인정보 마스킹**: 비밀번호, 카드번호 로그 금지
4. **비즈니스 이벤트 로깅**: 주문 생성, 결제 완료 등 중요 이벤트 기록
5. **예외 전체 스택 트레이스**: 오류 시 full stack trace 포함

**Kubernetes 로그 수집:**
- DaemonSet으로 Fluentbit 배포: 모든 노드의 컨테이너 로그 자동 수집
- `kubectl logs` 단기 저장 한계 → 중앙화 필수
- 컨테이너는 stdout/stderr로만 출력 (파일 로그 금지)

**실무 알람 연동:**
- Kibana Watcher: 로그 패턴 기반 알람 (특정 에러 n분 내 m회 이상)
- ElastAlert: Python 기반 알람 도구

---

## 5. 실무 적용 및 판단

중앙화된 로깅은 분산 마이크로서비스 환경에서 장애 진단 시간을 드라마틱하게 단축한다. MTTR(Mean Time To Repair)이 "각 서버에 SSH 접속하여 로그 찾기"의 시간에서 "Kibana에서 Trace ID 검색" 30초로 줄어든다.

비용과 보존 정책이 주요 운영 과제다. 로그는 매우 빠르게 증가하므로, Hot(최근 7일, 빠른 검색) → Warm(30일, 일반 검색) → Cold(90일, 압축 보관) → Delete(삭제) 레이어별 데이터 수명 주기(ILM, Index Lifecycle Management) 정책을 반드시 설정해야 한다.

---

## 6. 기대효과 및 결론

로그 및 ELK Stack (Logs, Centralized Logging)를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 로그 및 ELK Stack (Logs, Centralized Logging)의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
각 서버별 개별 로그 파일 (분산 시 확인 불가)
    │
    ▼
중앙 집중 로깅: ELK (Elastic · Logstash · Kibana) · Loki
    ├─► 구조화 로그: JSON 형식 + Trace ID 포함
    └─► 로그 레벨: DEBUG · INFO · WARN · ERROR · FATAL
    │
    ▼
AIOps: 로그 패턴 자동 분석 · 이상 탐지
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 옵저버빌리티 | 로그는 3대 기둥 중 두 번째 |
| Trace ID | 로그-트레이스 상관관계 연결 키 |
| ELK Stack | 로그 중앙화의 표준 오픈소스 스택 |
| Fluentd / Fluentbit | 경량 로그 수집기, Logstash 대안 |
| Grafana Loki | 비용 효율적 로그 저장소, ELK 대안 |
| RCA | 장애 원인 분석 시 로그가 핵심 증거 |

---
