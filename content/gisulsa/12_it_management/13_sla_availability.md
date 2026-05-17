+++
weight = 13
title = "13. SLA & 가용성 관리"
date = "2026-05-17"
[extra]
categories = "gisulsa-it-mgmt"
+++

# 🎯 SLA & 가용성 관리

> **별점**: ★★★★★ | 기본 필수

## 1. 가용성 목표

```
[9의 개수로 표현]
99% (two-nines):   87.6시간/년 다운 (낮음)
99.9% (three-nines): 8.76시간/년 (일반 서비스)
99.95%:           4.38시간/년 (엔터프라이즈)
99.99% (four-nines): 52.6분/년 (금융, 중요 서비스)
99.999% (five-nines): 5.26분/년 (통신, 의료)
99.9999%:         31.5초/년 (미션 크리티컬)

비용 vs 가용성 트레이드오프:
9 하나 더 추가 ≈ 비용 10배 증가
```

## 2. 가용성 설계 패턴

```
[Active-Active vs Active-Passive]
Active-Active:
  두 사이트 동시 트래픽 처리
  가용성 최고, 비용 2배
  
Active-Passive:
  하나가 Primary, 다른 하나 Standby
  장애 시 Passive 활성화 (수초~수분 소요)

[서버 레벨 HA]
로드밸런서: 트래픽 분산, 헬스체크
오토스케일링: 장애 인스턴스 자동 교체
데이터: Master-Slave 복제, Multi-AZ

[장애 도메인]
AZ (Availability Zone): 독립 데이터센터
Region: 지역 (여러 AZ)
Multi-Region: 지역 재난 대비
```

## 3. SLA 관리

```
[SLA 핵심 지표]
가용성: 요청 시 서비스 제공 비율
응답시간: P50, P95, P99 지연시간
처리량: TPS, RPS
오류율: 5xx 오류 비율

[SLA 위반 대응]
크레딧 정책: 위반 시 요금 감액
에스컬레이션: 위반 임박 시 긴급 대응
사후 분석: RCA (Root Cause Analysis)
```

## 4. 답안 포인트

**3단락**: ① 9의 개수 가용성 목표 & 비용 트레이드오프 → ② 가용성 설계(AA/AP, 로드밸런서, 오토스케일링) → ③ SLA 지표 & 위반 대응

## 5. 관련 개념

`SRE(06번)` → 에러 버짓 = 1-SLO | `BCP/DRS(09번)` → 재해 시 가용성 보장 | `K8s(13_cloud)` → K8s 오토스케일링으로 가용성 확보
