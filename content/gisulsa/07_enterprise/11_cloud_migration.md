+++
weight = 11
title = "11. DX & AX 엔터프라이즈"
date = "2026-05-17"
[extra]
categories = "gisulsa-enterprise"
+++

# 클라우드 전환 전략 (6R)

> 별점: ★★★★★ | ★135회 기출

---

## 답안.

### Ⅰ. 개요

기존 온프레미스 애플리케이션을 클라우드로 이전하는 전략
Retire:     폐기 (불필요 시스템 제거)
Retain:     유지 (현재 온프레미스 최적)

### Ⅱ. 핵심 구성요소

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


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
