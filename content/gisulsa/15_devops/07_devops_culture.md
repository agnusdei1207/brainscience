+++
weight = 7
title = "07. DevOps 문화 & 지표"
date = "2026-05-17"
[extra]
categories = "gisulsa-devops"
+++

# 🎯 DevOps 문화 & DORA 지표

> **별점**: ★★★★★ | 기본 필수

## 1. DevOps 핵심 원칙

```
정의: 개발(Dev)과 운영(Ops)의 통합으로 빠르고
     안정적인 소프트웨어 전달

[CALMS 프레임워크]
C (Culture): 협업 문화, 비난 없는 문화(Blameless)
A (Automation): 자동화 (CI/CD, IaC, 테스트)
L (Lean): 낭비 제거, 지속적 개선
M (Measurement): 데이터 기반 의사결정
S (Sharing): 지식 공유, 도구 공유

[3가지 Way]
1st Way: 왼쪽(개발) → 오른쪽(운영) 흐름 가속
2nd Way: 피드백 루프 (오른쪽 → 왼쪽)
3rd Way: 실험 문화, 반복 학습 = 지속적 개선
```

## 2. DORA 지표 (DevOps 성과 측정)

```
[4가지 핵심 지표]
배포 빈도 (Deployment Frequency):
  얼마나 자주 배포하나?
  Elite: 하루 여러 번 / Low: 월 1회 미만

변경 리드 타임 (Lead Time for Changes):
  코드 커밋 → 프로덕션 배포까지 시간
  Elite: 1시간 미만 / Low: 6개월 초과

변경 실패율 (Change Failure Rate):
  배포 후 장애/롤백 비율
  Elite: 0~15% / Low: 46~60%

서비스 복구 시간 (Time to Restore):
  장애 발생 → 복구까지 시간
  Elite: 1시간 미만 / Low: 1주일 초과

→ 고성과 팀: 배포 빈도 ↑, 리드타임 ↓,
  실패율 ↓, 복구시간 ↓ = 동시 달성 가능
```

## 3. 가치 흐름 매핑 (Value Stream Mapping)

```
정의: 고객 가치 전달 과정의 모든 단계를 시각화하여
     낭비를 식별하고 개선

[측정 지표]
리드 타임: 요구사항 → 전달
사이클 타임: 실제 작업 시간
대기 시간: 다음 단계 이동 전 대기

[DevOps 가치 흐름]
아이디어 → 코딩 → 빌드 → 테스트 → 릴리즈 → 배포
→ 운영 → 모니터링 → 피드백 → 아이디어

병목 식별: 대기 시간이 긴 단계
  → 자동화로 제거 (CI/CD)
```

## 4. 답안 포인트

**3단락**: ① DevOps CALMS 원칙 & 3가지 Way → ② DORA 4지표 & Elite vs Low 수준 → ③ 가치 흐름 매핑 & 병목 제거

## 5. 관련 개념

`CI/CD(01번)` → 배포 빈도·리드타임 향상 수단 | `SRE(12_it)` → DORA 복구 시간 = SRE MTTR | `플랫폼 엔지니어링(05번)` → DORA 개선 플랫폼
