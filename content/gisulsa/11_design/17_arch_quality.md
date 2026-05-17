+++
weight = 17
title = "17. 클라우드 감리 실무"
date = "2026-05-17"
[extra]
categories = "gisulsa-design"
+++

# 🎯 SW 아키텍처 평가 실무 & 설계 원칙

> **별점**: ★★★★☆ | 기본 필수

## 1. 아키텍처 품질 속성

```
[ISO 25010 기반 아키텍처 품질]
성능 (Performance):
  처리량, 응답시간, 자원 효율
  측정: TPS, P95 응답시간

가용성 (Availability):
  99.9%, 99.99%, 99.999% (파이브나인)
  패턴: Active-Active, 헬스체크, 자동복구

변경성 (Modifiability):
  변경 비용 최소화
  패턴: 모듈화, 인터페이스 분리

보안성 (Security):
  기밀성, 무결성, 가용성
  패턴: 심층 방어, 최소 권한

테스트 용이성 (Testability):
  단위/통합/시스템 테스트 용이
  패턴: 의존성 주입, 인터페이스 추상화
```

## 2. 아키텍처 트레이드오프

```
[주요 트레이드오프]
성능 vs 보안: 암호화 → 지연 증가
가용성 vs 일관성: CAP 정리
성능 vs 비용: 캐시/CDN → 비용 증가
변경성 vs 성능: 추상화 → 간접 비용

[ATAM 트레이드오프 예시]
MSA 선택:
  + 독립 배포, 확장성 (가용성↑)
  - 분산 복잡도, 네트워크 지연 (성능↓)
  - 운영 복잡도 (유지보수성↓)
```

## 3. 아키텍처 패턴 & 설계 원칙 종합

```
[설계 원칙]
DRY (Don't Repeat Yourself): 중복 금지
KISS (Keep It Simple, Stupid): 단순하게
YAGNI (You Aren't Gonna Need It): 필요할 때 만들어라
SoC (Separation of Concerns): 관심사 분리

[패턴 선택 가이드]
고성능 읽기: CQRS + 캐시 레이어
분산 일관성: 사가 + 보상 트랜잭션
느슨한 결합: 이벤트 드리블(EDA)
레거시 통합: Strangler Fig, ACL
```

## 4. 답안 포인트

**3단락**: ① 아키텍처 품질 속성 정의 → ② 트레이드오프 분석(성능 vs 보안 vs 비용) → ③ SOLID + DRY/KISS/YAGNI 설계 원칙 통합

## 5. 관련 개념

`ATAM(07번)` → 트레이드오프 분석 방법 | `SOLID(04_sw 08번)` → OOP 설계 원칙 | `MSA` → 아키텍처 패턴의 현대적 적용
