+++
title = "23. 형상 기록/보고 (Configuration Status Accounting)"
description = "형상 항목의 변경 이력, 상태, 기준선 정보를 기록하고 보고하는 SCM 활동"
date = "2026-03-05"
[taxonomies]
tags = ["형상기록", "CSA", "StatusAccounting", "변경이력", "SCM"]
categories = ["studynotes-4_software_engineering"]
+++

# 형상 기록/보고 (Configuration Status Accounting)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 형상 기록/보고(CSA)는 형상 항목(CI)의 **식별 정보, 변경 상태, 기준선 현황, 감사 결과**를 체계적으로 기록하고 필요 시 보고서를 생성하여 가시성과 추적성을 확보하는 SCM 활동입니다.
> 2. **가치**: CSA는 **변경 이력 100% 추적, 형상 현황 실시간 파악, 감사 증거 제공**을 가능하게 하며, 프로젝트 의사결정과 형상 감사의 핵심 정보원입니다.
> 3. **융합**: 전통적 보고서에서 **Git 커밋 로그, CI/CD 대시보드, 자동화된 체인지로그, SBOM 생성**으로 진화하였으며, DevOps 가시성(Observability)의 기반이 됩니다.

---

## Ⅰ. 개요 (Context & Background) - [최소 500자 이상]

### 1. 명확한 개념 및 정의

**형상 기록/보고(Configuration Status Accounting, CSA)**는 형상 관리(SCM)의 4대 핵심 활동 중 세 번째로, 형상 식별, 형상 통제, 형상 감사 과정에서 발생하는 **모든 정보를 기록하고 유지관리**하는 활동입니다.

**IEEE Std 828-2012 정의**:
> "Configuration status accounting is the process of recording and reporting the information needed to manage a configuration effectively, including the identification of configuration items, the status of proposed changes, and the implementation status of approved changes."

**CSA의 핵심 정보 유형**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CSA 기록 정보 유형                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 형상 항목 식별 정보                                          │
│     ├── CI ID, 명칭, 버전                                       │
│     ├── 소유자, 위치                                            │
│     ├── 관련 기준선                                             │
│     └── 부모/자식 CI 관계                                       │
│                                                                 │
│  2. 변경 상태 정보                                               │
│     ├── 변경 요청(CR) ID, 상태                                  │
│     ├── 승인 일시, 승인자                                       │
│     ├── 구현 현황                                               │
│     └── 검증 결과                                               │
│                                                                 │
│  3. 기준선 정보                                                  │
│     ├── 기준선 ID, 유형                                         │
│     ├── 포함된 CI 목록                                          │
│     ├── 설정 일시                                               │
│     └── 승인자                                                  │
│                                                                 │
│  4. 감사 정보                                                    │
│     ├── 감사 유형, 일시                                         │
│     ├── 감사 결과                                               │
│     ├── 시정 조치 현황                                          │
│     └── 완료 일시                                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 💡 일상생활 비유: 병원 진료 기록부

```
[CSA = 병원 전자 건강 기록(EHR)]

병원에서 환자의 모든 진료 기록을 관리합니다:

┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  📋 기록 정보                                               │
│                                                             │
│  1. 환자 식별: 이름, 주민번호, 차트번호                      │
│  2. 진료 이력: 언제, 누가, 무슨 진료를 했는가                │
│  3. 처방 기록: 어떤 약을 언제 처방했는가                     │
│  4. 검사 결과: 혈액검사, X-ray 결과                          │
│  5. 수술 기록: 수술 일시, 집도의, 경과                       │
│                                                             │
│  이 기록이 있어야:                                          │
│  - 담당 의사가 환자 상태 파악                                │
│  - 다른 병원에서도 기록 공유                                 │
│  - 의료 분쟁 시 증거 제시                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘

소프트웨어도 마찬가지:
- 어떤 CI가, 언제, 누가, 왜 변경했는지 기록
- 이 정보로 형상 상태 파악, 감사 지원
```

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. CSA 데이터베이스 구조

```sql
-- 형상 항목 테이블
CREATE TABLE config_items (
    ci_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    type VARCHAR(50),  -- SOURCE, DOC, TEST, CONFIG
    current_version VARCHAR(30),
    baseline_id VARCHAR(50),
    owner VARCHAR(100),
    location VARCHAR(500),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- 변경 요청 테이블
CREATE TABLE change_requests (
    cr_id VARCHAR(50) PRIMARY KEY,
    ci_id VARCHAR(50) REFERENCES config_items(ci_id),
    requester VARCHAR(100),
    request_date TIMESTAMP,
    change_type VARCHAR(50),
    priority VARCHAR(20),
    status VARCHAR(30),
    description TEXT,
    justification TEXT
);

-- 변경 이력 테이블
CREATE TABLE change_history (
    history_id SERIAL PRIMARY KEY,
    ci_id VARCHAR(50),
    cr_id VARCHAR(50),
    old_version VARCHAR(30),
    new_version VARCHAR(30),
    changed_by VARCHAR(100),
    changed_at TIMESTAMP,
    change_description TEXT
);

-- 기준선 테이블
CREATE TABLE baselines (
    baseline_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(200),
    type VARCHAR(50),  -- REQUIREMENTS, DESIGN, CODE, PRODUCT
    created_at TIMESTAMP,
    created_by VARCHAR(100),
    status VARCHAR(30)
);

-- 기준선-CI 매핑
CREATE TABLE baseline_ci_mapping (
    baseline_id VARCHAR(50),
    ci_id VARCHAR(50),
    version VARCHAR(30),
    included_at TIMESTAMP,
    PRIMARY KEY (baseline_id, ci_id)
);
```

### 2. CSA 보고서 유형

| 보고서 유형 | 내용 | 대상 | 주기 |
| :--- | :--- | :--- | :--- |
| **CI 현황 보고서** | 전체 CI 목록, 버전, 상태 | PM, 개발팀 | 주간 |
| **변경 현황 보고서** | CR 상태, 진행률 | CCB, PM | 격주 |
| **기준선 보고서** | 기준선 구성, 변경 이력 | QA, 감사 | 월간 |
| **감사 준비 보고서** | 감사 체크리스트 현황 | 감사관 | 수시 |
| **CM 활동 보고서** | SCM 활동 통계 | 경영진 | 월간 |

### 3. Git 기반 CSA 자동화 예시

```bash
#!/bin/bash
# CSA 자동 보고서 생성 스크립트

generate_ci_status_report() {
    echo "# 형상 항목 현황 보고서"
    echo "생성 일시: $(date)"
    echo ""

    echo "## 1. 소스 코드 CI"
    find . -name "*.java" -o -name "*.py" -o -name "*.js" | while read file; do
        version=$(git log -1 --format="%h" "$file" 2>/dev/null)
        modified=$(git log -1 --format="%ci" "$file" 2>/dev/null)
        author=$(git log -1 --format="%an" "$file" 2>/dev/null)
        echo "- $file | 버전: $version | 수정: $modified | 작성자: $author"
    done

    echo ""
    echo "## 2. 최근 변경 이력 (7일)"
    git log --since="7 days ago" --oneline --name-only | sort | uniq -c | sort -rn | head -20

    echo ""
    echo "## 3. 현재 기준선 태그"
    git describe --tags 2>/dev/null || echo "태그 없음"
}

generate_change_status_report() {
    echo "# 변경 현황 보고서"
    echo "생성 일시: $(date)"
    echo ""

    echo "## 브랜치별 커밋 현황"
    git for-each-ref --sort=-committerdate --format='%(refname:short) | %(committerdate:relative) | %(authorname)' refs/heads/ | head -20

    echo ""
    echo "## 미병합 브랜치"
    git branch --no-merged main

    echo ""
    echo "## 최근 머지"
    git log --merges --oneline -10
}

# 실행
case "$1" in
    ci-status) generate_ci_status_report ;;
    change-status) generate_change_status_report ;;
    *) echo "Usage: $0 {ci-status|change-status}" ;;
esac
```

---

## Ⅲ. 융합 비교 및 다각도 분석

### 1. CSA vs 일반 로그

| 구분 | CSA | 일반 로그 |
| :--- | :--- | :--- |
| **목적** | 형상 관리 의사결정 | 디버깅, 모니터링 |
| **대상** | CI, CR, 기준선 | 시스템 이벤트 |
| **구조** | 정형화된 스키마 | 자유 형식 |
| **보존** | 프로젝트 수명 | 로그 롤링 |

### 2. 현대적 CSA 도구

| 도구 | 용도 | 특징 |
| :--- | :--- | :--- |
| **Git Log** | 버전 이력 | 분산형, 브랜치 지원 |
| **GitHub Insights** | 활동 통계 | 시각화, 협업 |
| **SonarQube** | 코드 품질 이력 | 메트릭 추적 |
| **Jira** | 이슈 추적 | CR 연동 |
| **SBOM 도구** | 의존성 기록 | 보안 추적 |

---

## Ⅳ. 실무 적용 및 기술사적 판단

### 1. 기술사적 판단

**[시나리오] CSA 도구 선정**

```
요구사항:
- 100인 개발팀
- 마이크로서비스 아키텍처
- 규제 준수 (금융권)

권장 도구 조합:
1. 버전 관리: Git + GitHub Enterprise
2. 이슈 추적: Jira (CR 연동)
3. CI/CD: Jenkins + Git 로그 연동
4. 의존성: SBOM (Syft/Trivy)
5. 대시보드: Grafana + 커스텀

CSA 자동화:
- 일일 CI 현황 보고서 자동 생성
- 주간 변경 현황 보고서 이메일 발송
- 월간 CM 활동 보고서 경영진 보고
```

---

## Ⅴ. 기대효과 및 결론

### 1. 정량적 기대효과

| 구분 | 지표 | 미적용 | 적용 | 개선 |
| :--- | :--- | :--- | :--- | :--- |
| **가시성** | 형상 현황 파악 시간 | 4시간 | 5분 | -98% |
| **추적성** | 변경 이력 조회 | 불가능 | 즉시 | ∞ |
| **감사** | 증거 자료 준비 | 2주 | 1시간 | -99% |

### ※ 참고 표준

- **IEEE 828-2012**: Configuration Management
- **ISO 10007**: Configuration Management Guidelines

---

## 📌 관련 개념 맵

- [형상 관리](./19_configuration_management.md) : SCM 전체 체계
- [형상 식별](./20_configuration_identification.md) : CI 선정
- [형상 통제](./21_configuration_control.md) : 변경 승인
- [형상 감사](./22_configuration_audit.md) : 무결성 검증
- [기준선](./25_baseline.md) : 공식 버전

---

## 👶 어린이를 위한 3줄 비유 설명

1. **문제**: 일기를 쓰는데, 내가 언제 무슨 일을 했는지 까먹었어요! "저번 주에 뭐 했지?" 생각이 안 나요!

2. **해결(CSA)**: 그래서 '모든 기록 장부'를 만들었어요! 매일 무슨 일을 했는지, 언제 했는지, 왜 했는지 다 적어요. 나중에 찾을 때 편하게요!

3. **효과**: 이제 선생님이 "저번 주 숙제 기억나?" 하면 장부를 보고 바로 말할 수 있어요! 친구한테 "이거 누가 바꿨어?" 물어도 바로 알 수 있죠!
