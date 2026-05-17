+++
weight = 10
title = "10. 내부 개발자 플랫폼"
date = "2026-05-17"
[extra]
categories = "gisulsa-devops"
+++

# 🎯 플랫폼 엔지니어링 심화 & IDP

> **별점**: ★★★★★ | ☆ 2026 예측

## 1. IDP (Internal Developer Platform)

```
정의: 개발자가 인프라·배포·모니터링을 셀프서비스로
     이용할 수 있는 내부 플랫폼

[IDP 제공 기능]
Self-Service 인프라 프로비저닝
CI/CD 파이프라인 자동 구성
환경 관리 (개발/스테이징/운영)
서비스 카탈로그: 표준 컴포넌트
모니터링/로깅 통합 대시보드
비용 가시성

[Backstage (Spotify → CNCF)]
오픈소스 IDP 프레임워크
서비스 카탈로그: 모든 서비스 목록 + 문서
Tech Docs: 코드와 함께 문서화
Software Templates: 표준 프로젝트 템플릿
Plugins: 확장 가능한 플러그인 생태계
```

## 2. 플랫폼 팀 & 인지 부하

```
[Team Topologies (매튜 스켈튼)]
스트림 정렬 팀: 비즈니스 기능 개발
플랫폼 팀: 인프라·플랫폼 내부 서비스
가능화 팀: 스트림팀 역량 향상 (컨설팅)
복잡성 해결 팀: 특수 문제 해결

[인지 부하 감소]
개발자가 K8s, Terraform, 보안 모두 알 필요 없음
플랫폼이 추상화 → 개발에 집중
"Platform as a Product"

[골든 패스 (Golden Path)]
플랫폼 팀이 권장 기술 스택 제공
개발팀: 골든 패스 따르면 빠른 시작
이탈: 지원 줄어들지만 선택 가능
```

## 3. FinOps + Platform Engineering

```
[플랫폼으로 FinOps 구현]
자원 요청 시 비용 예측 표시
환경별 예산 쿼터 설정
개발 환경 자동 종료 (오후 6시 자동 삭제)
비용 대시보드 = 팀별 클라우드 비용 가시화

[Platform Engineering KPI]
DORA 지표 개선율
개발자 만족도 (Developer NPS)
골든 패스 채택률
인프라 셀프서비스 비율
```

## 4. 답안 포인트

**3단락**: ① IDP 정의 & Backstage 구성요소 → ② 플랫폼팀 역할 & 인지 부하 감소 → ③ FinOps + 플랫폼 통합 & DORA 지표

## 5. 관련 개념

`DevOps 문화(07번)` → 플랫폼 엔지니어링 = DevOps 성숙화 | `GitOps(09번)` → ArgoCD를 IDP에 통합 | `FinOps(13_cloud)` → 플랫폼으로 FinOps 민주화
