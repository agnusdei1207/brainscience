+++
weight = 11
title = "11. DX & AX 엔터프라이즈"
date = "2026-05-17"
[extra]
categories = "gisulsa-enterprise"
+++

# 🎯 클라우드 전환 전략 (6R)

> **별점**: ★★★★★ | ★135회 기출

## 1. 클라우드 전환 6R 전략

```
기존 온프레미스 애플리케이션을 클라우드로 이전하는 전략

[6R (Gartner)]
Retire:     폐기 (불필요 시스템 제거)
Retain:     유지 (현재 온프레미스 최적)
Rehost:     리호스팅 (Lift & Shift) - 코드 변경 없이 IaaS로
Replatform: 리플랫폼 (일부 최적화) - DB → 관리형 DB
Refactor:   리팩터 (코드 재설계) - 클라우드 네이티브로
Rearchitect:재아키텍처 - MSA/서버리스로 완전 재설계

[선택 기준]
Rehost: 빠른 이전, 레거시 의존성 높음
Replatform: 적정 비용, 중간 최적화
Refactor: 장기 ROI, 클라우드 혜택 극대화
```

## 2. 마이그레이션 단계

```
[클라우드 마이그레이션 프로세스]
1. 발견 (Discovery): 현행 인프라 현황 파악
2. 계획 (Plan): 6R 전략 결정, 우선순위
3. 이전 (Migrate): 파일럿 → 점진적 이전
4. 최적화 (Optimize): 비용·성능 최적화 (FinOps)
5. 운영 (Operate): 클라우드 네이티브 운영

도구:
- AWS Migration Hub, Azure Migrate
- 비용 분석: AWS TCO Calculator
- 의존성 파악: Application Discovery Service
```

## 3. 답안 포인트

**3단락**: ① 클라우드 전환 필요성 & 6R 전략 정의 → ② 각 전략 특성·비용·위험 비교 → ③ 마이그레이션 단계 & FinOps

## 4. 관련 개념

`멀티클라우드(★135회)` → 전환 후 운영 전략 | `BCP/DRS(★133회)` → 클라우드 DR | `레거시 현대화` → 6R로 레거시 탈피
