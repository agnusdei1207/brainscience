+++
weight = 9
title = "09. GitOps & 배포 전략"
date = "2026-05-17"
[extra]
categories = "gisulsa-devops"
+++

# 🎯 고급 배포 전략 & GitOps

> **별점**: ★★★★★ | 기본 필수

## 1. 배포 전략 심화

```
[블루-그린 (Blue-Green)]
Blue: 현재 운영, Green: 새 버전 대기
트래픽 전환: 100% 즉시 전환 (로드밸런서)
장점: 즉각 롤백 가능
단점: 자원 2배 (두 환경 동시 운영)

[카나리 (Canary)]
새 버전에 일부 트래픽 (1%→5%→20%→100%)
점진적 위험 감소
A/B 테스트와 결합
도구: Argo Rollouts, Flagger (K8s)

[롤링 업데이트 (Rolling Update)]
파드를 순차적으로 교체 (기본 K8s 방식)
minUnavailable / maxSurge 설정
장점: 자원 효율, 단점: 롤백 시 복잡

[Feature Flag (기능 토글)]
코드 배포 ≠ 기능 활성화 분리
런타임에 기능 ON/OFF
도구: LaunchDarkly, Unleash, Flagsmith
Dark Launch: 배포 후 특정 사용자만 활성화
```

## 2. GitOps 심화

```
[Pull-based GitOps]
ArgoCD/Flux가 Git 감시 → K8s 자동 동기화

vs Push-based CI/CD:
  Push: Jenkins가 kubectl apply 실행
  Pull: ArgoCD가 차이 감지 → 자동 적용

[드리프트 감지]
실제 K8s 상태 ≠ Git 선언 → 자동 복원
누군가 kubectl로 직접 변경 → ArgoCD가 되돌림

[Multi-Tenant GitOps]
Argo CD ApplicationSet: 다수 클러스터 동시 배포
클러스터당 Git 폴더 구조 → 환경별 관리
```

## 3. Progressive Delivery

```
정의: 카나리 + 피처 플래그 + 관찰가능성 결합
     = 위험 최소화 배포

[Flagger]
K8s에서 자동 카나리 분석
Prometheus 메트릭 기반 자동 프로모션/롤백
Linkerd/Istio + Flagger = 진정한 카나리

[실제 워크플로우]
Git 머지 → ArgoCD 배포 (카나리 1%)
→ Flagger가 오류율 모니터링
→ OK → 자동으로 비율 증가
→ NG → 자동 롤백
```

## 4. 답안 포인트

**3단락**: ① 블루그린/카나리/롤링 배포 비교 → ② GitOps Pull-based & 드리프트 복원 → ③ Progressive Delivery & Flagger 자동화

## 5. 관련 개념

`CI/CD(01번)` → 배포 파이프라인 기반 | `K8s(13_cloud)` → 카나리/롤링 플랫폼 | `SRE(12_it)` → 배포 = 에러 버짓 소비
