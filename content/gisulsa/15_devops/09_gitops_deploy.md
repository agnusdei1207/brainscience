+++
weight = 9
title = "09. GitOps & 배포 전략"
date = "2026-05-17"
[extra]
categories = "gisulsa-devops"
+++

# 고급 배포 전략 & GitOps

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

Blue: 현재 운영, Green: 새 버전 대기
트래픽 전환: 100% 즉시 전환 (로드밸런서)
단점: 자원 2배 (두 환경 동시 운영)

### Ⅱ. 핵심 구성요소

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
```
[Pull-based GitOps]
ArgoCD/Flux가 Git 감시 → K8s 자동 동기화

vs Push-based CI/CD:
  Push: Jenkins가 kubectl apply 실행


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
