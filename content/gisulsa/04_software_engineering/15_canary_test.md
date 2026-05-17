+++
weight = 15
title = "15. 카나리 테스트 (Canary Testing)"
date = "2026-05-17"
[extra]
categories = "gisulsa-sw-engineering"
+++

# 카나리 테스트 & 배포 전략 (Blue-Green, Rolling, Canary)

> 별점: ★★★★★ | ★132회 기출

---

## 답안.

### Ⅰ. 개요

전체 트래픽 → 100% 구버전(v1)
Step 1: 5% 트래픽 → 신버전(v2)
         95% 트래픽 → v1

### Ⅱ. 핵심 구성요소

```
[카나리 배포 흐름]
전체 트래픽 → 100% 구버전(v1)

Step 1: 5% 트래픽 → 신버전(v2)
         95% 트래픽 → v1
         ↓ KPI 모니터링 (오류율, 지연, 전환율)

Step 2: 문제 없으면 → 30% → v2
         오류 발생 → 즉시 0%로 롤백

Step 3: 50% → 100% 점진적 증가

도구: Kubernetes + Argo Rollouts, Istio
     AWS: CodeDeploy, App Mesh
     특징: 실제 사용자 트래픽으로 테스트
```
```
[Blue-Green 배포]
Blue (현재 운영): v1 ──→ DNS/LB 연결
Green (새 버전): v2 ──→ 테스트 완료 후

LB 전환: Blue → Green (즉시 전환, 다운타임 0)
문제 시: Green → Blue 즉시 롤백
단점: 자원 2배, DB 스키마 변경 복잡
```


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
