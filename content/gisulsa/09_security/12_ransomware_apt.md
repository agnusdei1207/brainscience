+++
weight = 12
title = "12. 랜섬웨어 & APT"
date = "2026-05-17"
[extra]
categories = "gisulsa-security"
+++

# 🎯 랜섬웨어 & APT 공격

> **별점**: ★★★★★ | 기본 필수

## 1. 랜섬웨어

```
정의: 피해자 파일을 암호화하고 복호화 키를 빌미로
     몸값(Ransom)을 요구하는 악성코드

[랜섬웨어 진화]
1세대: 단순 암호화, 개별 공격
2세대: RaaS (Ransomware as a Service)
  → 개발자가 서비스로 제공 (다크웹)
3세대: 이중 갈취 (Double Extortion)
  → 암호화 + 데이터 유출 위협
4세대: 삼중 갈취 + DDoS

[공격 흐름]
초기 침투: 피싱, 취약점, VPN 계정 탈취
내부 이동: 권한 상승, 내부 네트워크 확산
데이터 유출: 중요 데이터 외부 전송
암호화: 파일 암호화 (AES + RSA 하이브리드)
협박: 몸값 요구 (비트코인)

[유명 사례]
WannaCry (2017): SMB EternalBlue 취약점
NotPetya (2017): 공급망 공격 (우크라이나)
Colonial Pipeline (2021): 미국 파이프라인
Kaseya VSA (2021): MSP 공급망 공격
```

## 2. APT (Advanced Persistent Threat)

```
정의: 특정 조직을 장기간 지속적으로 침투하는
     정교한 사이버 위협 (국가 배후 추정)

[APT 특징]
Advanced: 고도의 기술 (제로데이 활용)
Persistent: 장기간 지속 (수년)
Threat: 정보 탈취, 사보타주 목적

[APT 그룹 명칭]
Lazarus (라자루스): 북한, 금융·암호화폐 탈취
APT41: 중국, 스파이활동+재정적 이익
APT28: 러시아(Fancy Bear), 정치적 목적

[APT 공격 단계 (MITRE ATT&CK)]
정찰 → 초기 접근 → 지속성 유지 →
권한 상승 → 방어 우회 → 자격증명 탈취
→ 내부 이동 → 데이터 유출
```

## 3. 방어 전략

```
[랜섬웨어 방어]
3-2-1 백업 + 오프라인 백업 (Immutable)
EDR: 랜섬웨어 행동 패턴 탐지
MFA: 계정 탈취 방어
최소 권한: 피해 범위 제한
네트워크 분할: 내부 이동 차단

[APT 방어]
위협 헌팅: 선제적 탐색
UEBA: 사용자/엔터티 행동 분석
Zero Trust: 내부도 신뢰하지 않음
EDR + NDR + XDR (통합 탐지)
```

## 4. 답안 포인트

**3단락**: ① 랜섬웨어 진화 & 이중/삼중 갈취 → ② APT 정의 & 공격 단계 → ③ 백업/EDR/Zero Trust 방어 전략

## 5. 관련 개념

`Zero Trust(★136회)` → APT 내부 이동 차단 | `SOC/SIEM(11번)` → APT 탐지 플랫폼 | `공급망 보안(SBOM)` → 공급망 랜섬웨어 대응
