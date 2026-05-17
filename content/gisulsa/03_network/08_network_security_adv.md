+++
weight = 8
title = "08. 네트워크 보안 심화"
date = "2026-05-17"
[extra]
categories = "gisulsa-network"
+++

# 🎯 네트워크 보안 심화 — 방화벽 & IDS/IPS

> **별점**: ★★★★★ | 기본 필수

## 1. 방화벽 세대

```
[1세대] 패킷 필터링:
  IP/포트 기반 정적 규칙
  L3/L4 수준, Stateless

[2세대] 상태 기반 (Stateful):
  TCP 연결 상태 추적
  세션 테이블 유지
  단순 패킷 필터링보다 정확

[3세대] 애플리케이션 계층:
  L7 페이로드 분석
  HTTP, DNS, SMTP 내용 검사

[4세대] NGFW (차세대 방화벽):
  + 애플리케이션 식별 (포트 무관)
  + 사용자 ID 기반 제어
  + SSL 복호화 검사
  + IDS/IPS 통합
  + 위협 인텔리전스 연계
```

## 2. IDS vs IPS

| 항목 | IDS (탐지) | IPS (방어) |
|------|-----------|-----------|
| 역할 | 침입 탐지·경보 | 탐지 + 실시간 차단 |
| 배치 | 네트워크 탭(Passive) | 인라인(Active) |
| 장애 영향 | 없음 | 장애 시 통신 차단 위험 |
| False Positive | 경보만 | 정상 트래픽 차단 위험 |

```
[탐지 방식]
시그니처 기반: 알려진 공격 패턴 매칭
  → 신속, 오탐 낮음, 미지 공격 탐지 불가

이상 기반 (Anomaly):
  정상 기준선 학습 → 이상 탐지
  → AI/ML 기반, 제로데이 탐지 가능
  → 오탐 높음
```

## 3. DDoS 방어

```
[DDoS 유형]
볼류메트릭: 대역폭 소진 (UDP Flood, ICMP Flood)
프로토콜: 연결 테이블 고갈 (SYN Flood)
L7: 애플리케이션 부하 (HTTP GET Flood)

[방어 전략]
스크러빙 센터: ISP 업스트림에서 정화
CDN: 분산으로 부하 흡수 (Cloudflare)
Anycast: 트래픽 분산
Rate Limiting: 임계값 초과 차단
BGP Blackhole: 대상 IP 블랙홀 라우팅
```

## 4. 답안 포인트

**3단락**: ① 방화벽 세대(패킷→Stateful→NGFW) → ② IDS vs IPS 탐지 방식(시그니처/이상) → ③ DDoS 유형 & 방어 전략

## 5. 관련 개념

`Zero Trust(★136회)` → NGFW + ZTNA 통합 | `SASE(클라우드)` → 클라우드 방화벽+IPS | `AI 위협탐지` → 이상 기반 ML 탐지
