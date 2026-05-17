+++
weight = 8
title = "08. 서버리스 & FaaS"
date = "2026-05-17"
[extra]
categories = "gisulsa-cloud"
+++

# 🎯 서버리스 & FaaS (Function as a Service)

> **별점**: ★★★★★ | ★134회 기출

## 1. 서버리스 정의

```
서버리스 (Serverless): 서버 프로비저닝·관리 없이
코드만 작성하면 자동으로 실행되는 클라우드 모델

이점:
- 서버 관리 불필요 (No-ops)
- 자동 스케일링 (트래픽에 따라 0→수천 인스턴스)
- 사용한 만큼만 과금 (밀리초 단위)
- 운영 부담 최소화

한계:
- 콜드 스타트: 첫 호출 시 지연 (수백ms~수초)
- 실행 시간 제한: 보통 최대 15분
- 상태 비저장: 함수 간 상태 공유 어려움
- 벤더 락인: CSP 종속성 높음
```

## 2. FaaS 서비스

```
[주요 FaaS 서비스]
AWS Lambda: 트리거 기반, 지원 언어 다양
Azure Functions: .NET 친화, 다양한 바인딩
GCP Cloud Functions: Node.js/Python, Firebase 연계
Cloudflare Workers: 엣지 컴퓨팅, V8 기반

[트리거 유형]
HTTP 요청: API Gateway + Lambda
이벤트: S3 파일 업로드 → Lambda 실행
스케줄: Cron 기반 주기 실행
메시지: SQS, SNS, Kafka 메시지
```

## 3. 서버리스 아키텍처 패턴

```
[이벤트 기반 아키텍처]
S3 업로드 → Lambda(이미지 처리) → DynamoDB 저장
API Gateway → Lambda → RDS 조회 → JSON 반환

[서버리스 Best Practices]
함수 단일 목적: SRP 원칙 적용
멱등성: 재호출 시 동일 결과
환경변수: 설정 외부화 (Lambda 환경 변수)
VPC: 내부 자원 접근 시 VPC 연결 (지연 증가)
프로비전드 동시성: 콜드 스타트 방지

[Cost 계산]
AWS Lambda: 요청 수 + 실행 시간(GB-초)
월 100만 요청 = $0.2 (무료 티어 100만)
```

## 4. 답안 포인트

**3단락**: ① 서버리스 정의 & 장점(자동스케일/종량과금) → ② 콜드 스타트·시간제한 한계 & 대응 → ③ 이벤트 기반 패턴 & 마이크로서비스 연계

## 5. 관련 개념

`MSA(★133회)` → 서버리스는 MSA 극단적 형태 | `그린SW(04_sw 31번)` → 유휴 자원 0 → 탄소 절감 | `FinOps(클라우드)` → 서버리스 비용 최적화
