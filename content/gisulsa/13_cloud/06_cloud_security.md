+++
weight = 6
title = "06. 클라우드 보안 & CSAP"
date = "2026-05-17"
[extra]
categories = "gisulsa-cloud"
+++

# 🎯 클라우드 보안 & CSAP (클라우드 보안 인증)

> **별점**: ★★★★★ | ★135회 연계

## 1. 클라우드 보안 위협

```
[CSA 12대 클라우드 위협]
1. 데이터 유출
2. 잘못된 구성 (Misconfiguration)
3. 클라우드 API 취약점
4. 계정 탈취
5. 내부자 위협
6. 불충분한 사고 대응
7. 메타구조 장애
8. 제한적 가시성
9. 악성 클라우드 서비스
10. DoS 공격
11. 공유 기술 취약점
12. 공급망 위험

핵심: #2 잘못된 구성 = 클라우드 보안사고의 95% 원인
      (S3 버킷 공개 설정, 광범위한 IAM 권한)
```

## 2. CSAP (클라우드 보안 인증)

```
정의: 국내 공공기관이 안전한 클라우드 서비스 이용을 위해
     KISA가 CSP를 대상으로 수행하는 보안 인증

[CSAP 등급]
상: IaaS/SaaS/PaaS (중요 정보 처리)
   - 75개 보안 통제 충족
중: 비중요 정보 (약식 심사)
하: 공개 가능 정보 (최소 요건)

공공기관 의무:
중요 정보 처리 클라우드 = 상등급 CSAP 필수
```

## 3. 클라우드 보안 핵심 기술

```
CWPP (Cloud Workload Protection Platform):
  클라우드 워크로드 보호 (VM, 컨테이너, 서버리스)

CSPM (Cloud Security Posture Management):
  클라우드 보안 구성 오류 자동 탐지·수정
  핵심: 잘못된 설정(#2) 방지

CIEM (Cloud Infrastructure Entitlement Management):
  IAM 권한 최소화, 과도한 권한 탐지

CNAPP (Cloud-Native Application Protection Platform):
  CWPP + CSPM + CIEM 통합
  = 클라우드 네이티브 종합 보안

CASB (Cloud Access Security Broker):
  SaaS 접근 제어, 데이터 손실 방지
```

## 4. 답안 포인트

**3단락**: ① 클라우드 보안 주요 위협(잘못된 구성 강조) → ② CSAP 인증 등급 & 의무 적용 → ③ CWPP/CSPM/CIEM/CNAPP 현대 클라우드 보안

## 5. 관련 개념

`Zero Trust(★136회)` → 클라우드 환경 ZT 적용 | `ISMS-P(★134회)` → 클라우드 ISMS 적용 | `DevSecOps` → 클라우드 빌드 시 보안 내장
