+++
weight = 11
title = "11. IaC & GitOps"
date = "2026-05-17"
[extra]
categories = "gisulsa-cloud"
+++

# 🎯 IaC (인프라 코드) & GitOps

> **별점**: ★★★★★ | ☆ 2026 예측

## 1. IaC (Infrastructure as Code)

```
정의: 인프라 프로비저닝을 코드로 선언하고
     버전 관리·자동화하는 방식

[이점]
재현성: 동일 환경 반복 생성 가능
버전 관리: Git으로 변경 이력 추적
자동화: CI/CD와 통합하여 자동 프로비저닝
협업: 코드 리뷰로 인프라 변경 검토

[IaC 도구]
Terraform (HashiCorp):
  선언적, 멀티클라우드, HCL 언어
  state 파일로 현재 인프라 추적
  Plan → Apply 2단계

Pulumi:
  Python/JavaScript 등 범용 언어 사용
  Terraform보다 표현력 높음

AWS CloudFormation:
  AWS 전용, YAML/JSON
  스택 기반 관리

Ansible:
  절차적, 서버 구성(Configuration) 특화
  YAML Playbook, 에이전트리스
```

## 2. GitOps

```
정의: Git을 단일 소스(SSoT)로 사용하여
     인프라/앱 배포를 선언적으로 관리하는 운영 모델

[GitOps 원칙]
1. 선언적: 원하는 상태를 코드로 선언
2. 버전 관리: Git에 모든 변경 기록
3. 자동 적용: Git 변경 → 인프라 자동 반영
4. 감사 가능: 모든 변경은 PR/MR 추적

[GitOps 도구]
ArgoCD: K8s용 GitOps 컨트롤러
  Git → K8s 클러스터 자동 동기화
Flux: CNCF GitOps 표준
  K8s 내장, 멀티테넌시

[적용 흐름]
PR 생성 → 코드 리뷰 → 머지
  → ArgoCD가 변경 감지 → K8s 자동 배포
  → 드리프트 탐지: 실제≠선언 시 자동 복원
```

## 3. 답안 포인트

**3단락**: ① IaC 정의 & Terraform 특성 → ② GitOps 4원칙 & ArgoCD 동작 → ③ DevOps CI/CD 파이프라인에서 IaC+GitOps

## 4. 관련 개념

`멀티클라우드(10번)` → Terraform 멀티클라우드 프로비저닝 | `K8s(07번)` → ArgoCD GitOps 대상 | `DevSecOps(15_devops)` → IaC 보안 스캐닝
