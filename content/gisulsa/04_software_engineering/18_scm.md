+++
weight = 18
title = "18. 형상관리 (SCM)"
date = "2026-05-17"
[extra]
categories = "gisulsa-sw-engineering"
+++

# 형상관리 (SCM, Software Configuration Management)

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

형상관리(SCM): SW 개발 과정에서 **코드·문서·데이터의 버전을 통제**하고, 변경 이력을 추적하며, 여러 개발자 간 협업을 관리하는 체계.
형상 항목(CI): 코드, 문서, 빌드 스크립트, 설정 파일, 데이터베이스 스키마

### Ⅱ. 핵심 구성요소

```
[GitFlow]
main (운영) ─── develop (개발) ─── feature/xxx
                    ↓ release/1.0
                    ↓ hotfix/001 (긴급 패치)
특징: 릴리즈 명확, 복잡한 브랜치 관리

[GitHub Flow]
main ─── feature/xxx (PR → 리뷰 → 병합)
특징: 단순, CI/CD 친화, 지속 배포

[Trunk-Based Development]
main ─── 단기 feature 브랜치 (1~2일)
특징: 지속적 통합 (feature flag 활용), 고빈도 배포
```
```
[SCM 4대 활동]
1. 형상 식별 (Identification): CI 목록 정의
2. 형상 통제 (Control): 변경 요청 → 검토 → 승인
3. 형상 감사 (Audit): 형상 항목 무결성 확인
4. 형상 상태 보고 (Status Accounting): 변경 이력 기록

도구:
- 버전 관리: Git, SVN
- 이슈 추적: Jira, GitHub Issues
- CI/CD: Jenkins, GitHub Actions
- 아티팩트: Nexus, Artifactory
```


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
