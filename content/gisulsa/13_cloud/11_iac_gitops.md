+++
weight = 11
title = "11. IaC & GitOps"
date = "2026-05-17"
[extra]
categories = "gisulsa-cloud"
+++

# IaC (인프라 코드) & GitOps

> 별점: ★★★★★ | ☆ 2026 예측

---

## 답안.

### Ⅰ. 개요

정의: 인프라 프로비저닝을 코드로 선언하고
버전 관리: Git으로 변경 이력 추적
자동화: CI/CD와 통합하여 자동 프로비저닝

### Ⅱ. 핵심 구성요소

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
```
정의: Git을 단일 소스(SSoT)로 사용하여


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
