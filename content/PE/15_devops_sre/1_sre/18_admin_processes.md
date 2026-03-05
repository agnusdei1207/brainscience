+++
title = "관리 프로세스 (Admin Processes)"
description = "12-Factor App의 12번째 원칙으로 일회성 관리 작업을 애플리케이션과 동일한 환경에서 실행하여 환경 일관성을 보장하는 DevOps 실천법"
date = 2024-05-15
[taxonomies]
tags = ["12-Factor-App", "Admin-Processes", "DevOps", "Database-Migration", "One-off"]
+++

# 관리 프로세스 (Admin Processes)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 데이터베이스 마이그레이션, 배치 작업, 스크립트 실행 등 일회성 관리 작업(One-off Admin Tasks)을 별도의 셸 스크립트가 아닌, 애플리케이션과 완전히 동일한 코드베이스·환경·의존성에서 실행하여 '환경 불일치'로 인한 장애를 원천 차단하는 12-Factor App의 12번째 원칙입니다.
> 2. **가치**: "내 로컬에서는 되는데 서버에서는 안 돼요"라는 환경 차이 문제를 완전히 제거하고, 관리 작업도 버전 관리(Git)와 CI/CD 파이프라인의 통제를 받게 하여 감사 추적(Audit Trail)과 재현성(Reproducibility)을 100% 보장합니다.
> 3. **융합**: Kubernetes Job/CronJob, Airflow DAG, AWS Lambda 등의 현대적 오케스트레이션 플랫폼과 결합하여 일회성 작업을 선언적(Declarative) 코드로 관리하는 GitOps 관행의 기반이 됩니다.

---

## Ⅰ. 개요 (Context & Background)

### 1. 명확한 정의 (Definition)
**관리 프로세스(Admin Processes)**는 12-Factor App의 열두 번째이자 마지막 원칙으로, 프로덕션 환경에서 실행되는 **일회성(One-off) 관리/유지보수 작업**(예: 데이터베이스 마이그레이션 실행, 데이터 백업/복원, 캐시 플러시, 사용자 데이터 일괄 수정, 리포트 생성)이 장기 실행되는 애플리케이션 프로세스와 **동일한 코드베이스, 동일한 의존성, 동일한 설정 환경**에서 실행되어야 한다는 원칙입니다. 이를 통해 관리 작업에 별도의 '운영 전용 스크립트'나 '서버 직접 접속(SSH)'을 사용하는 대신, 애플리케이션 코드의 일부로 버전 관리하고 CI/CD 파이프라인을 통해 실행합니다.

### 💡 2. 구체적인 일상생활 비유
자동차 정비소를 상상해 보세요. 정기적인 운행(애플리케이션 프로세스)과 엔진 오일 교체(관리 프로세스)는 서로 다른 작업이지만, 둘 다 **동일한 자동차 부품과 도구**를 사용합니다. 오일 교체할 때 다른 나라에서 수입한 부품을 사용하면 맞지 않을 수 있습니다. 마찬가지로, 관리 작업은 애플리케이션과 같은 코드, 같은 라이브러리, 같은 설정을 사용해야 어떤 환경에서든 일관되게 동작합니다.

### 3. 등장 배경 및 발전 과정
1. **기존 기술의 치명적 한계점 (환경 드리프트와 스크립트 관리 부재)**:
   전통적 IT 환경에서는 운영자가 프로덕션 서버에 SSH로 접속하여 `python migrate_v1_to_v2.py`와 같은 로컬 스크립트를 직접 실행했습니다. 이 스크립트는 Git에 커밋되지 않았고, 서버에만 존재했습니다. 운영자가 휴가를 가거나 퇴사하면 그 스크립트는 사라지고, 다른 사람은 어떻게 데이터를 수정했는지 알 수 없었습니다. 또한 로컬에서 테스트한 스크립트가 프로덕션 서버의 다른 라이브러리 버전 때문에 실행되지 않는 일이 빈번했습니다.

2. **혁신적 패러다임 변화의 시작**:
   12-Factor App은 "모든 실행 코드는 동일한 코드베이스에서 나와야 한다"고 선언했습니다. `rake db:migrate`(Rails), `python manage.py migrate`(Django), `npx prisma migrate deploy`(Node.js)와 같은 프레임워크 내장 마이그레이션 명령어는 애플리케이션 코드와 함께 버전 관리되며, 어떤 환경에서든 동일한 방식으로 실행됩니다. 이는 '불변 인프라(Immutable Infrastructure)' 사상과도 일치합니다.

3. **현재 시장/산업의 비즈니스적 요구사항**:
   SOX(Sarbanes-Oxley), SOC 2, GDPR 등의 규정 준수 요구사항은 "누가, 언제, 어떤 데이터를 수정했는가"에 대한 완전한 감사 로그(Audit Log)를 요구합니다. SSH로 서버에 접속하여 수동으로 실행한 스크립트는 추적할 수 없습니다. 반면 CI/CD 파이프라인에서 실행된 `kubectl exec` 또는 Kubernetes Job은 자동으로 로그가 남고 승인 프로세스를 거치므로 규정 준수에 용이합니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 1. 핵심 구성 요소 (표)

| 요소명 (Component) | 상세 역할 | 내부 동작 메커니즘 | 관련 도구/기술 | 실행 방식 |
| :--- | :--- | :--- | :--- | :--- |
| **Admin Command** | 애플리케이션 코드 내 일회성 작업 진입점 | CLI 파서(Argparse, Cobra), 환경 변수 로드, DB 연결 초기화 | Django manage.py, Rails rake | 로컬/CI/K8s Job |
| **Database Migration** | DB 스키마 변경(DDL) 및 데이터 이관 | 마이그레이션 파일 버전 관리, 트랜잭션 내 실행, 롤백 스크립트 | Flyway, Liquibase, Prisma | CI/CD 파이프라인 |
| **Batch Processing** | 대량 데이터 처리, 리포트 생성 | 청크(Chunk) 단위 처리, 진행률 추적, 실패 시 재시도 | Spring Batch, Airflow | K8s CronJob |
| **Data Seed Script** | 초기 데이터(마스터 데이터) 로드 | idempotent(멱등성) 보장, 중복 실행 시 에러 없음 | Django fixtures, Rails seeds | 배포 파이프라인 |
| **Cleanup Job** | 만료된 데이터 삭제, 로그 정리 | TTL 기반 필터링, 배치 삭제(DELETE LIMIT) | Custom Script | K8s CronJob |
| **Kubernetes Job** | 일회성 작업 오케스트레이션 | Pod 생성 → 작업 실행 → 완료 시 Pod 유지(로그 확인) | kubectl, Argo Workflows | K8s Cluster |

### 2. 정교한 구조 다이어그램: 관리 프로세스 실행 아키텍처

```text
=====================================================================================================
                      [ Admin Processes - Unified Environment Architecture ]
=====================================================================================================

  [ Same Codebase, Same Environment ]                    [ Execution Methods ]
             │                                                    │
             ▼                                                    │
+-----------------------------+                                  │
|    Application Codebase     |                                  │
|  ┌───────────────────────┐  |                                  │
|  │ /app                  │  |                                  │
|  │ ├─ src/               │  |   ┌─────────────────────────────┐│
|  │ │  ├─ controllers/    │  │   │ Admin Commands (CLI)        ││
|  │ │  └─ models/         │  ├──►│ - python manage.py migrate  ││
|  │ ├─ scripts/           │  │   │ - npx prisma migrate deploy ││
|  │ │  ├─ seed_data.py    │  │   │ - rails db:seed            ││
|  │ │  └─ cleanup_logs.py │  │   └─────────────────────────────┘│
|  │ ├─ migrations/        │  │                                   │
|  │ │  ├─ V001__init.sql  │  │                                   │
|  │ │  └─ V002__add_col.sql│  │                                   │
|  │ └─ package.json       │  │                                   │
|  └───────────────────────┘  │                                   │
+──────────────┬──────────────+                                   │
               │                                                  │
               ▼                                                  │
+-----------------------------+                                  │
|   Shared Dependencies       |                                  │
|  ┌───────────────────────┐  |                                  │
|  │ requirements.txt      │  |   Both App & Admin use same libs │
|  │ package-lock.json     │  │                                  │
|  └───────────────────────┘  │                                  │
+──────────────┬──────────────+                                   │
               │                                                  │
               ▼                                                  │
+-----------------------------+                                  │
|   Shared Configuration      |                                  │
|  ┌───────────────────────┐  |                                  │
|  │ Environment Variables │  |   Same DB URL, API Keys          │
|  │ DATABASE_URL=...      │  │   Same logging format            │
|  │ API_KEY=...           │  │                                  │
|  └───────────────────────┘  │                                  │
+──────────────┬──────────────+                                   │
               │                                                  │
               │ Same Runtime Environment                         │
               ▼                                                  │
=====================================================================================================
                    [ Admin Process Execution Scenarios ]
=====================================================================================================

Scenario A: Local Development
+------------------+      +------------------------+
| Developer Laptop | ───► | python manage.py       |
| (same codebase)  |      | migrate                |
+------------------+      +------------------------+

Scenario B: CI/CD Pipeline
+------------------+      +------------------------+      +------------------+
| GitHub Actions   | ───► | Docker Container       | ───► │ Database         |
| (after tests)    │      | (same image as app)    │      │ Migration        |
+------------------+      +------------------------+      +------------------+

Scenario C: Kubernetes Job
+------------------+      +------------------------+      +------------------+
| kubectl apply    | ───► │ K8s Job Pod            | ───► │ Database         |
| -f job.yaml      │      │ (same image as app)    │      │ Migration        |
+------------------+      +------------------------+      +------------------+
                          │                            │
                          │ Log: "Migration V002       │
                          │       completed in 3.2s"   │
                          └────────────────────────────┘

Scenario D: Argo Workflows (Complex Pipeline)
+------------------------+
| Argo Workflow DAG      |
| ┌──────────────────┐   |
| │ Step 1: Backup   │   |
│ └────────┬─────────┘   |
│          ▼             │
│ ┌──────────────────┐   |
| │ Step 2: Migrate  │   |
│ └────────┬─────────┘   |
│          ▼             │
│ ┌──────────────────┐   |
| │ Step 3: Verify   │   |
│ └──────────────────┘   |
+------------------------+
```

### 3. 심층 동작 원리 (동일 환경 보장 메커니즘)

**① 코드베이스 통합 (Codebase Integration)**
모든 관리 스크립트는 애플리케이션 코드와 동일한 Git 리포지토리에 위치합니다:
- `migrations/`: DB 마이그레이션 파일
- `scripts/`: 일회성 데이터 작업
- `management/commands/`: 프레임워크별 관리 명령어 (Django 스타일)

이로써 애플리케이션 v2.3.1 배포 시 실행해야 할 마이그레이션 버전이 명확히 매핑됩니다.

**② 동일 의존성 (Shared Dependencies)**
관리 프로세스는 애플리케이션과 동일한 `package.json`, `requirements.txt`, `Gemfile`을 사용합니다. Docker 이미지로 패키징될 때 동일한 베이스 이미지와 라이브러리 버전을 가집니다:
```dockerfile
# Same Dockerfile for both app and admin processes
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app

# App process
CMD ["gunicorn", "app:app"]

# Admin process (override at runtime)
# docker run myapp python manage.py migrate
```

**③ 동일 설정 (Shared Configuration)**
관리 프로세스는 애플리케이션과 동일한 환경 변수(`DATABASE_URL`, `REDIS_URL`)를 사용합니다. 개발/스테이징/프로덕션 환경에서 모두 동일한 방식으로 DB에 연결합니다.

### 4. 핵심 알고리즘 및 실무 코드 예시

**Django 관리 명령어 예시 (커스텀 관리 명령어)**

```python
# myapp/management/commands/cleanup_expired_sessions.py
from django.core.management.base import BaseCommand
from django.conf import settings
from myapp.models import UserSession
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Cleanup expired user sessions from database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Delete sessions older than this many days',
        )

    def handle(self, *args, **options):
        cutoff_date = datetime.now() - timedelta(days=options['days'])

        expired_sessions = UserSession.objects.filter(
            last_activity__lt=cutoff_date
        )

        count = expired_sessions.count()

        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING(f'Would delete {count} expired sessions')
            )
            return

        # Actual deletion in batches
        batch_size = 1000
        deleted = 0
        while True:
            batch = expired_sessions[:batch_size]
            if not batch:
                break
            batch.delete()
            deleted += len(batch)
            self.stdout.write(f'Deleted {deleted}/{count}...')

        logger.info(f'Cleanup completed: {deleted} sessions removed')
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {deleted} expired sessions')
        )
```

**Kubernetes Job 매니페스트 (일회성 DB 마이그레이션)**

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration-v2
  labels:
    app: myapp
    type: migration
spec:
  ttlSecondsAfterFinished: 86400  # Keep job for 24h after completion
  backoffLimit: 3                   # Retry 3 times on failure
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: migrator
        image: myapp:v2.3.1  # Same image as application!
        command: ["python", "manage.py", "migrate"]
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-url
        envFrom:
        - configMapRef:
            name: myapp-config  # Same config as application!
      imagePullSecrets:
      - name: registry-secret
```

**CI/CD 파이프라인 통합 (GitHub Actions)**

```yaml
# .github/workflows/deploy.yml
jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - name: Run DB Migration
        run: |
          kubectl apply -f k8s/migration-job.yaml
          kubectl wait --for=condition=complete job/db-migration-v2 --timeout=300s

  deploy:
    needs: migrate  # Deploy only after migration succeeds
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Application
        run: |
          kubectl apply -f k8s/deployment.yaml
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 1. 심층 기술 비교표: 관리 작업 실행 방식 비교

| 평가 지표 | SSH 직접 접속 스크립트 | 별도 관리 서버 | 앱과 동일 환경 (12-Factor) |
| :--- | :--- | :--- | :--- |
| **버전 관리** | 없음 (서버에만 존재) | 부분적 | 완전 (Git에 커밋) |
| **환경 일관성** | 낮음 (서버마다 상이) | 중간 | 높음 (동일 이미지) |
| **감사 추적** | 없음 (수동 로그) | 부분적 | 완전 (CI/CD 로그) |
| **롤백 가능성** | 어려움 | 중간 | 용이함 (이전 버전 실행) |
| **협업 용이성** | 낮음 (지식 공유 안 됨) | 중간 | 높음 (코드 리뷰 가능) |
| **보안 (SSH 노출)** | 취약 (직접 접속) | 중간 | 강건 (CI/CD 게이트) |

### 2. 과목 융합 관점 분석

**관리 프로세스 + IaC (Terraform)**
- 인프라 프로비저닝 후 초기 데이터 시드(Seeding) 작업을 Terraform의 `local-exec` provisioner 또는 별도 Job으로 실행하여, 인프라 생성과 애플리케이션 초기화를 원스톱으로 자동화합니다.

**관리 프로세스 + 옵저버빌리티**
- 관리 작업 실행 로그를 중앙 로깅 시스템으로 수집하여, "누가 언제 어떤 데이터 작업을 했는지"를 추적합니다. 실패한 마이그레이션은 자동으로 알림을 발송합니다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 1. 실무 시나리오 기반 의사결정 전략

**[상황 A] 긴급 데이터 수정 요청**
- **문제점**: 결제 시스템 버그로 인해 100명의 사용자 포인트가 잘못 계산되었습니다. 즉시 수정이 필요합니다.
- **기술사 판단 (전략)**: SSH로 서버에 접속하여 직접 SQL을 실행하는 대신, `fix_user_points.py` 스크립트를 작성하여 Git에 커밋하고, CI/CD 파이프라인에서 실행합니다. 이렇게 하면: ① 스크립트가 코드 리뷰를 거침 ② 실행 로그가 자동 보관됨 ③ 나중에 동일 문제 발생 시 재사용 가능.

**[상황 B] 대용량 데이터 마이그레이션**
- **문제점**: 1억 건의 사용자 데이터를 새로운 스키마로 이관해야 합니다. 10시간 이상 소요될 것으로 예상됩니다.
- **기술사 판단 (전략)**: 일회성 스크립트가 아닌 Spring Batch 또는 Airflow DAG로 구현하여 청크(Chunk) 단위로 처리하고, 중단 시 재개(Resume)가 가능하도록 설계합니다. Kubernetes Job으로 실행하여 리소스 제한(limits)을 설정합니다.

### 2. 도입 시 고려사항 (체크리스트)

**기술적 고려사항**
- [ ] 멱등성(Idempotency) 보장: 관리 작업을 여러 번 실행해도 결과가 동일해야 함
- [ ] 타임아웃 설정: 장기 실행 작업의 무한 대기 방지
- [ ] 리소스 제한: 배치 작업이 DB/서버 리소스를 독점하지 않도록 throttling

**운영/보안적 고려사항**
- [ ] 승인 게이트(Approval Gate): 프로덕션 관리 작업 실행 전 필수 승인 프로세스
- [ ] Dry-run 모드: 실제 변경 전 영향 범위 미리 확인 기능
- [ ] 롤백 스크립트 준비: 마이그레이션 실패 시 복구 방안

### 3. 주의사항 및 안티패턴 (Anti-patterns)

**안티패턴 1: 운영 서버에 직접 SSH 접속하여 스크립트 실행**
- "급해서"라는 이유로 서버에 직접 접속하여 `python fix_bug.py`를 실행하는 것은 12-Factor 위반이자 보안 위험입니다. 모든 작업은 CI/CD 파이프라인을 거쳐야 합니다.

**안티패턴 2: 로컬 환경에서만 테스트하고 프로덕션 바로 실행**
- 관리 스크립트는 로컬 → 스테이징 → 프로덕션 순서로 단계적 검증 후 실행해야 합니다. `DATABASE_URL`만 다를 뿐 동일한 코드가 실행되어야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 1. 정량적/정성적 기대효과

| 구분 | SSH 직접 실행 (AS-IS) | 동일 환경 실행 (TO-BE) | 개선 지표 |
| :--- | :--- | :--- | :--- |
| **장애 재현률** | 30% (환경 차이로 실패) | 95%+ (동일 환경) | **실패율 70% 감소** |
| **감사 대응 시간** | 수 시간~수 일 | 즉시 (CI/CD 로그) | **대응 시간 99% 단축** |
| **협업 효율** | 낮음 (지식 공유 안 됨) | 높음 (코드 리뷰) | **협업 품질 향상** |
| **보안 사고** | 높음 (SSH 권한 남용) | 낮음 (감사 가능) | **보안 위험 감소** |

### 2. 미래 전망 및 진화 방향
- **선언적 관리 작업 (Declarative Admin)**: 명령형 스크립트("이 데이터를 삭제해라") 대신 선언형 정의("만료된 데이터는 없어야 한다")로 관리 작업을 정의하여, 시스템이 자동으로 필요한 작업을 수행하는 방향으로 진화합니다.
- **AI 기반 데이터 작업**: 데이터 클렌징, 마이그레이션 검증 등의 작업에 AI를 활용하여 자동으로 이상치를 탐지하고 수정 제안을 하는 지능형 관리 작업이 등장할 것입니다.

### 3. 참고 표준/가이드
- **12-Factor App (12factor.net/admin-processes)**: 관리 프로세스 원칙의 원천
- **SOC 2 (CC6.1)**: 변경 관리 및 감사 추적 요구사항
- **SOX Section 404**: 내부 통제 및 변경 승인 프로세스

---

## 📌 관련 개념 맵 (Knowledge Graph)
- **[12-Factor App](@/studynotes/15_devops_sre/1_sre/twelve_factor_app.md)**: 관리 프로세스를 포함한 12가지 원칙
- **[CI/CD 파이프라인](@/studynotes/15_devops_sre/3_automation/continuous_integration.md)**: 관리 작업 자동화 인프라
- **[데이터베이스 마이그레이션](@/studynotes/8_database/1_rdbms/db_migration.md)**: 대표적인 관리 프로세스 유형
- **[빌드, 릴리스, 실행](@/studynotes/15_devops_sre/1_sre/11_build_release_run.md)**: 관리 작업도 동일한 빌드/릴리스 프로세스 적용
- **[배포 전략](@/studynotes/15_devops_sre/3_automation/deployment_strategies.md)**: 마이그레이션과 배포의 순서 조율

---

## 👶 어린이를 위한 3줄 비유 설명
1. 장난감 정리할 때 **'정리 로봇'**이 있어서, 버튼만 누르면 알아서 장난감을 제자리에 놓아요.
2. 이 로봇은 우리 집에서 쓰는 로봇과 똑같은 모양이에요. 그래서 어디서든 똑같이 작동하죠!
3. 덕분에 엄마가 "누가 장난감 치웠어?" 하고 물으면 로봇 기록을 보고 바로 알 수 있어요!
