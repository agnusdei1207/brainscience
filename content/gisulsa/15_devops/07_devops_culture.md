+++
weight = 7
title = "07. DevOps 문화 & 지표"
date = "2026-05-17"
[extra]
categories = "gisulsa-devops"
+++

# DevOps 문화 & DORA 지표

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

정의: 개발(Dev)과 운영(Ops)의 통합으로 빠르고
C (Culture): 협업 문화, 비난 없는 문화(Blameless)
A (Automation): 자동화 (CI/CD, IaC, 테스트)

### Ⅱ. 핵심 구성요소

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


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
