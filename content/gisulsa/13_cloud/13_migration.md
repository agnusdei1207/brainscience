+++
weight = 13
title = "13. 클라우드 마이그레이션 실무"
date = "2026-05-17"
[extra]
categories = "gisulsa-cloud"
+++

# 🎯 클라우드 마이그레이션 실무 & Well-Architected

> **별점**: ★★★★★ | ★135회 기출

## 1. AWS Well-Architected Framework

```
[6대 원칙]
1. 운영 우수성 (Operational Excellence):
   운영 자동화, 소규모 반복 변경, 실패에서 학습

2. 보안 (Security):
   공유 책임, 최소 권한, 추적 가능성

3. 신뢰성 (Reliability):
   자동 복구, 수평 확장, 비상 사태 테스트

4. 성능 효율성 (Performance Efficiency):
   최신 기술, 서버리스, 다중 지역

5. 비용 최적화 (Cost Optimization):
   FinOps, Right-Sizing, 예약 인스턴스

6. 지속가능성 (Sustainability):
   탄소 최소화, 효율적 자원 사용
```

## 2. 마이그레이션 가속 도구

```
[AWS 마이그레이션 서비스]
Migration Hub: 마이그레이션 중앙 추적
Application Discovery Service: 온프레미스 인벤토리
DMS (Database Migration Service): DB 이전
SMS (Server Migration Service): VM 이전
Snowball: 대용량 데이터 물리 이전

[마이그레이션 체크리스트]
① 발견: 현행 인벤토리, 의존성 파악
② 평가: 6R 전략 결정, TCO 분석
③ 준비: 클라우드 랜딩존 구성
④ 이전: 파일럿 → 점진적 이전
⑤ 최적화: Well-Architected Review
⑥ 운영: FinOps, 지속 개선
```

## 3. 랜딩존 (Landing Zone)

```
정의: 새 클라우드 계정 시작 시 설정하는 보안·거버넌스 기반

AWS Control Tower:
  자동 랜딩존 구성
  다중 계정 거버넌스 (Organization)
  가드레일: 예방적/탐지적 통제

랜딩존 구성 요소:
  계정 구조: 개발/스테이징/운영 계정 분리
  네트워크: VPC, Transit Gateway
  보안: SCPs, CloudTrail, Config
  비용: 통합 청구, 태그 정책
```

## 4. 답안 포인트

**3단락**: ① AWS WAF 6대 원칙 → ② 마이그레이션 6단계 프로세스 → ③ 랜딩존 거버넌스 & Control Tower

## 5. 관련 개념

`6R 전략(07_enterprise 11번)` → 이전 전략 결정 | `FinOps(09번)` → 비용 최적화 원칙 | `CSAP` → 공공 클라우드 마이그레이션 인증
