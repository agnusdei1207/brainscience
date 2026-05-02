+++
title = "475. STRIDE 모델 (STRIDE Model)"
date = 2026-04-21
weight = 475
description = "보안 위협을 Spoofing부터 Elevation of Privilege까지 6가지로 분류하는 모델"
taxonomy = ""
tags = ["Software Engineering", "Security", "STRIDE", "Threat Modeling", "Model"]
+++

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)는 위협을 6개 범주로 나누는 분류법이다.
> 2. **가치**: 놓치기 쉬운 공격 유형을 체계적으로 빠짐없이 점검하게 해준다.
> 3. **판단 포인트**: 자산보다 "어떤 공격 종류가 가능한가"를 먼저 묻는다.

---

## Ⅰ. 개요 및 필요성

STRIDE는 설계 단계에서 보안 위협을 분류하기 위한 대표적인 방법이다. 이름을 외우는 것보다, 각 글자가 어떤 공격 유형을 뜻하는지 이해하는 것이 중요하다.

이 모델은 위협 모델링 (Threat Modeling)에서 빠르게 점검 목록을 만들 때 유용하다.

- **📢 섹션 요약 비유**: 장난감 상자를 볼 때 "부서짐, 분실, 훔침"처럼 문제 종류를 먼저 나누는 것이다.

---

## Ⅱ. 아키텍처 및 핵심 원리

STRIDE는 아래처럼 6가지 질문으로 생각한다.

```text
자격 위조? -> Spoofing
변조?      -> Tampering
부인?      -> Repudiation
유출?      -> Information Disclosure
서비스 거부? -> Denial of Service
권한 상승? -> Elevation of Privilege
```

| 항목 | 의미 |
|:---|:---|
| Spoofing | 신원 위조 |
| Tampering | 데이터/흐름 변조 |
| Repudiation | 행위 부인 |
| Information Disclosure | 정보 노출 |
| Denial of Service | 서비스 방해 |
| Elevation of Privilege | 권한 상승 |

- **📢 섹션 요약 비유**: 감기 증상을 볼 때 열, 기침, 통증을 따로 구분하는 것과 같다.

---

## Ⅲ. 비교 및 연결

STRIDE는 체크리스트가 아니라 분류 틀이다. 그래서 동일한 시스템도 관점에 따라 여러 STRIDE 항목에 걸릴 수 있다.

| 구분 | STRIDE | 단순 취약점 목록 |
|:---|:---|:---|
| 목적 | 위협 분류 | 항목 나열 |
| 강점 | 누락 방지 | 빠른 기록 |
| 한계 | 우선순위는 별도 필요 | 구조적 분석 부족 |

위협 모델링, 공격 표면 분석, 보안 리뷰와 함께 쓰면 효과가 크다.

- **📢 섹션 요약 비유**: 책을 장르별로 나누면 찾기 쉽지만, 어떤 책이 좋은지는 또 따로 골라야 하는 것과 같다.

---

## Ⅳ. 실무 적용 및 기술사 판단

실무에서는 인증, 입력 검증, 로그, 권한 분리, API 설계에서 STRIDE를 적용한다.

적용 순서는 다음과 같다.
1. 데이터 흐름을 그린다.
2. 흐름의 각 지점에 STRIDE 항목을 대입한다.
3. 대응책을 요구사항에 반영한다.

- **📢 섹션 요약 비유**: 가게를 둘러보며 "도난, 위조, 파손"이 어디서 생길지 미리 적어두는 것이다.

---

## Ⅴ. 기대효과 및 결론

STRIDE는 보안 사고를 감으로 보지 않고 구조적으로 본다. 그래서 설계 검토의 품질을 높인다.

결론적으로 STRIDE는 "보안 위협 분류 프레임워크"다.

- **📢 섹션 요약 비유**: 문제를 종류별로 정리해야 약도 제대로 챙길 수 있다.

### 📌 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Threat Modeling | 상위 적용 맥락 |
| DREAD 모델 | 위험도 산정 보완 |
| OWASP Top 10 | 대표 취약점 분류 |

### 👶 어린이를 위한 3줄 비유 설명

1. STRIDE는 나쁜 일이 어떤 종류인지 나눠 보는 거예요.
2. 훔치기, 고치기, 숨기기 같은 걸 찾죠.
3. 그래서 빠뜨리지 않고 대비할 수 있어요.
