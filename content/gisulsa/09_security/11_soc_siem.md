+++
weight = 11
title = "11. 보안 운영 & SOC"
date = "2026-05-17"
[extra]
categories = "gisulsa-security"
+++

# 🎯 보안 운영 센터 (SOC) & SIEM

> **별점**: ★★★★★ | 기본 필수

## 1. SOC (Security Operations Center)

```
정의: 보안 이벤트를 24/7 모니터링하고 대응하는 조직

[SOC 계층]
Tier 1 분석가: 경보 분류·초기 대응
Tier 2 분석가: 심화 조사, 인시던트 처리
Tier 3 분석가: 위협 헌팅, 역공학, 포렌식
관리자: SOC 전략, 프로세스, 보고

[SOC 핵심 역할]
인시던트 탐지: SIEM 경보 모니터링
인시던트 대응: 격리, 복구, 분석
위협 헌팅: 선제적 위협 탐색
취약점 관리: 스캔, 우선순위, 추적
```

## 2. SIEM (Security Information & Event Management)

```
정의: 보안 로그를 수집·통합하여 위협 탐지·대응하는 플랫폼

[SIEM 핵심 기능]
로그 수집: 방화벽, IDS, AD, 앱 로그 통합
상관분석: 여러 이벤트를 조합하여 공격 탐지
경보: 임계값 기반, 행동 기반 알림
포렌식: 과거 로그 검색·분석
대시보드: 보안 현황 가시화

[주요 SIEM 제품]
Splunk SIEM: 가장 널리 사용
Microsoft Sentinel: 클라우드 네이티브 (Azure)
IBM QRadar: 엔터프라이즈
Elastic SIEM: 오픈소스 기반

[SOAR (Security Orchestration, Automation, Response)]
SIEM + 자동화: 반복적인 대응 자동화
플레이북: 표준화된 대응 절차 자동 실행
예) 피싱 메일 탐지 → 격리 → 분석 → 리포트 자동화
```

## 3. 위협 헌팅 & 인텔리전스

```
[CTI (Cyber Threat Intelligence)]
전략적: 위협 행위자 프로파일, 트렌드
전술적: TTP (전술/기술/절차)
운영적: IoC (침해 지표): IP, 도메인, 해시

MITRE ATT&CK 프레임워크:
  공격자 TTP 분류 (14개 전술, 수백 기법)
  위협 헌팅·탐지 규칙 개발에 활용

[Kill Chain (록히드 마틴)]
정찰 → 무기화 → 전달 → 취약점 악용 →
설치 → C&C → 목표 실행
→ 각 단계에서 차단 기회
```

## 4. 답안 포인트

**3단락**: ① SOC 역할 & 계층 구조 → ② SIEM 기능 & SOAR 자동화 → ③ CTI/MITRE ATT&CK & Kill Chain

## 5. 관련 개념

`Zero Trust(★136회)` → SOC + ZT = 지속적 검증 | `ISMS-P(★134회)` → SOC 거버넌스 기반 | `AI 위협탐지` → AI기반 SIEM 이상 탐지
