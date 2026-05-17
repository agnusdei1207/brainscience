+++
weight = 17
title = "17. 클라우드 거버넌스"
date = "2026-05-17"
[extra]
categories = "gisulsa-cloud"
+++

# 🎯 클라우드 거버넌스 & 컴플라이언스

> **별점**: ★★★★★ | 기본 필수

## 1. 클라우드 거버넌스 요소

```
[클라우드 거버넌스 5대 축]
비용 (FinOps): 비용 가시성, 최적화, 책임
보안: 공유책임, IAM, 데이터 보호
운영: 자동화, 패치, 모니터링
컴플라이언스: 규제 준수 (GDPR, 개보법)
신뢰성: SLA, 다중 AZ, BCP
```

## 2. 클라우드 정책 & 가드레일

```
[AWS Organizations & SCP]
조직(Organization): 여러 AWS 계정 통합 관리
Service Control Policy (SCP): 계정별 허용/거부 정책
  예) "모든 계정에서 특정 리전만 사용"
      "프로덕션 계정에서 삭제 금지"

[태그 정책]
필수 태그: 팀, 환경, 프로젝트, 비용센터
자동 적용: AWS Config Rules로 미태그 자원 탐지

[Config Rules]
규정 준수 자동 점검:
  "모든 S3 버킷 퍼블릭 차단 확인"
  "암호화되지 않은 EBS 탐지"
  "MFA 미적용 IAM 사용자 탐지"
→ 비준수 시 자동 수정 (Remediation)
```

## 3. 멀티계정 전략 & 랜딩존

```
[계정 분리 원칙]
환경별: Dev / Staging / Production (별도 계정)
팀별: 팀 단위 AWS 계정 분리
보안: 로그 전용, 보안 전용 계정

[AWS Control Tower]
랜딩존 자동 생성
가드레일(Guardrail):
  예방적(Preventive): SCP로 특정 행동 차단
  탐지적(Detective): Config Rules로 위반 탐지
Account Factory: 표준화된 계정 자동 생성
```

## 4. 답안 포인트

**3단락**: ① 클라우드 거버넌스 5대 축 → ② SCP/Config Rules 정책 자동화 → ③ 멀티계정 전략 & Control Tower

## 5. 관련 개념

`FinOps(09번)` → 비용 거버넌스 | `CSAP(06번)` → 보안 거버넌스 | `멀티클라우드(10번)` → 멀티클라우드 거버넌스 확장
