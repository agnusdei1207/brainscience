+++
weight = 41
title = "41. 041. 클라우드 마이그레이션 6R 전략 (Cloud Migration 6R)"
date = "2026-04-05"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: 041. 클라우드 마이그레이션 6R 전략 (Cloud Migration 6R)는 클라우드 아키텍처에서 자원, 데이터, 운영 방식을 더 탄력적이고 일관되게 만들기 위한 핵심 개념이다.
> **비유**: 6R은 이사 전략 — 버리기(Retire), 냅두기(Retain), 그대로 옮기기(Rehost), 일부 업그레이드(Replatform), 새로 구입(Repurchase), 완전 리모델링(Refactor).

---

> 📝 모범 답안

## 1. 개요 및 필요성

```
Cloud Migration 6R 전략:

[Retire] 폐기
  더 이상 사용하지 않는 시스템 종료
  클라우드 이전 없이 제거
  비율: 포트폴리오의 10~20%
  
[Retain] 유지 (보류)
  현재는 클라우드 이전 불필요 또는 불가
  레거시 의존성, 규제, 라이선스 문제
  
[Rehost] 리호스트 (Lift & Shift)
  수정 없이 그대로 클라우드 VM으로 이전
  빠르고 낮은 위험
  클라우드 최적화 없음 (비용 절감 제한)
  
[Replatform] 리플랫폼 (Lift, Tinker & Shift)
  핵심 아키텍처 유지, 일부 클라우드 서비스 활용
  예: DB → RDS 이관, 앱서버 → 관리형 컨테이너
  
[Repurchase] 재구매 (Drop & Shop)
  기존 솔루션 폐기 후 SaaS 전환
  예: 온프레미스 CRM → Salesforce
  
[Refactor] 재설계 (Re-architect)
  클라우드 네이티브로 완전 재설계
  마이크로서비스, 서버리스, 컨테이너
  최고 비용·시간, 최대 클라우드 효과
```

> 📢 **섹션 요약 비유**: 6R은 이사 전략 — 버리기(Retire), 냅두기(Retain), 그대로 옮기기(Rehost), 일부 업그레이드(Replatform), 새로 구입(Repurchase), 완전 리모델링(Refactor).

---

## 2. 구성요소

```
6R 전략 상세 비교표:

전략         | 변경 수준 | 이전 속도 | 클라우드 효과 | 위험도
-------------|---------|---------|------------|-------
Retire       | 없음    | 즉시    | N/A        | 없음
Retain       | 없음    | 보류    | 낮음       | 낮음
Rehost       | 최소    | 빠름    | 중간       | 낮음
Replatform   | 부분    | 중간    | 높음       | 중간
Repurchase   | 높음    | 중간    | 높음       | 중간
Refactor     | 완전    | 느림    | 최고       | 높음

Rehost 특징:
  AWS Migration Hub, Server Migration Service
  VMware → EC2 직접 이전
  비용: 온프레미스 대비 10~20% 절감
  
Replatform 특징:
  RDS 전환 (DB 관리 부담 감소)
  ECS/EKS 도입 (컨테이너화)
  코드 변경 최소화 + 클라우드 이점 일부 획득
  
Refactor 특징:
  MSA (마이크로서비스 아키텍처)
  Lambda/Fargate (서버리스)
  12-Factor App 원칙 적용
  비용: 최대 40~60% 절감 (올바르게 설계 시)
```

> 📢 **섹션 요약 비유**: Rehost=가구 그대로 이사, Replatform=일부 새 가구로 교체, Refactor=집 전체 인테리어 리모델링 — 효과와 비용 모두 비례.

---

## 3. 구조 및 원리

**핵심 조건**: 자원 추상화, 격리 수준, 자동 프로비저닝, 보안 경계, 비용 통제가 함께 설계되어야 안정적인 서비스 가치가 나온다.

동작 순서:
1. 요구사항과 책임 경계를 먼저 정의한다.
2. 추상화 계층에서 컴퓨팅·스토리지·네트워크 자원을 논리적으로 분리하고 격리 수준을 결정한다.
3. 제어 평면이 정책에 맞는 자원을 프로비저닝하고 서비스 모델에 따라 사용자에게 노출한다.
4. 운영 중에는 확장, 가용성, 백업, 보안 정책을 지속적으로 적용해 상태를 안정화한다.
5. 마지막으로 비용·성능·벤더 종속성을 함께 평가해 구조를 최적화한다.

```
애플리케이션 포트폴리오 분석:

1. 인벤토리 수집:
   모든 앱, 서버, DB, 의존성 파악
   7R 질문: 주요 기능, 사용 빈도, 기술 부채

2. 평가 기준:
   비즈니스 가치 (높음/중간/낮음)
   기술 복잡도 (높음/중간/낮음)
   클라우드 이전 용이성

3. 분류 매트릭스:

  비즈니스 가치
  ↑ 높음  | Replatform | Refactor    |
           | 또는       |             |
  중간     | Rehost     | Replatform  |
           |            |             |
  낮음     | Retire     | Retain      |
           +------------+-------------→
                낮음         높음
                  기술 복잡도

4. 마이그레이션 파동 (Wave) 계획:
   Wave 1 (3~6개월): 간단한 Rehost 앱
   Wave 2 (6~12개월): Replatform 앱
   Wave 3 (12~24개월): Refactor 핵심 앱

5. 의존성 분석:
   앱 간 의존성 맵 → 이전 순서 결정
   사이클릭 의존성 해소 후 이전
```

> 📢 **섹션 요약 비유**: 포트폴리오 분석은 이사 짐 분류 — 자주 쓰는 것(가치 높음)은 먼저, 무거운 것(복잡한 것)은 나중에, 쓸모없는 것(폐기)은 버리기.

---

## 4. 비교 및 연결

```
6R별 주요 도구 (AWS 기준):

공통:
  AWS Migration Hub: 마이그레이션 추적
  AWS Application Discovery Service: 의존성 발견

Rehost:
  AWS Server Migration Service (SMS)
  VMware Cloud on AWS
  CloudEndure Migration

Replatform:
  AWS Database Migration Service (DMS)
  Amazon ECS/EKS (컨테이너화)
  AWS Elastic Beanstalk

Repurchase:
  AWS Marketplace SaaS 제품
  Salesforce, SAP, ServiceNow 이전

Refactor:
  AWS Lambda (서버리스)
  Amazon EKS (쿠버네티스)
  AWS Step Functions (워크플로우)
  Amazon API Gateway

비용 분석 도구:
  AWS Migration Evaluator (TCO 분석)
  AWS Cost Explorer (이전 후 비용 추적)
  
타사 클라우드:
  Azure Migrate
  Google Cloud Migrate for Compute Engine
```

> 📢 **섹션 요약 비유**: 마이그레이션 도구는 이사 전문 업체 서비스 — Rehost는 용달 트럭, Refactor는 인테리어 회사.

---

## 5. 실무 적용 및 판단

```
금융기관 B사 클라우드 전환 사례:

배경:
  온프레미스 220개 애플리케이션
  데이터센터 계약 만료 18개월
  
포트폴리오 분석 결과:

Retire (15개, 6.8%):
  사용 없는 레거시 시스템
  즉시 폐기, 비용 절감

Retain (25개, 11.4%):
  규제/컴플라이언스 제약 시스템
  온프레미스 유지 (하이브리드)

Rehost (120개, 54.5%):
  Wave 1~2에서 빠른 이전
  평균 이전 기간: 4.2주/앱
  비용 절감: 18%

Replatform (35개, 15.9%):
  DB → RDS, 앱서버 → ECS 이관
  관리 부담 40% 감소

Repurchase (10개, 4.5%):
  HR, 이메일 → SaaS 전환

Refactor (15개, 6.8%):
  핵심 거래 시스템 MSA 재설계
  Wave 3 (12~24개월)

결과 (18개월 완료):
  인프라 비용: 35% 절감
  장애 복구 시간(RTO): 4시간 → 15분
  배포 빈도: 월 2회 → 주 3회
```

> 📢 **섹션 요약 비유**: 금융기관 6R 전환은 대형 병원 이전 — ICU(핵심 거래)는 정밀 Refactor, 일반 병실(일반 앱)은 빠른 Rehost, 쓰지 않는 장비는 폐기.

---

## 6. 기대효과 및 결론

041. 클라우드 마이그레이션 6R 전략 (Cloud Migration 6R)를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 041. 클라우드 마이그레이션 6R 전략 (Cloud Migration 6R)의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```
[Gartner 5Rs 발표 (2010)]
클라우드 이전 전략 체계화
      |
      v
[AWS 6Rs 확장 (2016~)]
Retire 추가, 실무 표준화
Migration Hub, Discovery Service
      |
      v
[클라우드 퍼스트 정책 (2018~)]
기업 클라우드 전환 의무화
대규모 Rehost 파동 시작
      |
      v
[클라우드 스마트 전략 (2019~)]
무분별한 Lift & Shift 문제 인식
Refactor 필요성 강조
      |
      v
[현재: 하이브리드 멀티클라우드]
온프레미스 + 클라우드 Retain 병존
FinOps로 비용 최적화 강조
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 가상화 | 물리 자원을 논리 자원으로 분리하는 기반 개념 |
| 하이퍼바이저 | 격리와 자원 스케줄링을 수행하는 핵심 계층 |
| 오토스케일링 | 수요 변화에 따라 자원 수를 자동으로 조절 |
| VPC | 클라우드 내 네트워크 격리와 보안 경계 제공 |
| FinOps | 비용 가시성과 최적화를 통해 클라우드 효율을 관리 |

---
