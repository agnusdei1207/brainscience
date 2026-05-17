+++
weight = 9
title = "09. Wi-Fi 7 (802.11be)"
date = "2026-05-17"
[extra]
categories = "gisulsa-ict"
+++

# 🎯 Wi-Fi 7 (IEEE 802.11be)

> **별점**: ★★★★★ | ★134회 기출

## 1. 정의

Wi-Fi 7(IEEE 802.11be, EHT: Extremely High Throughput): 최대 **46Gbps 이론 속도**와 **멀티링크 동작(MLO)**를 핵심으로 하는 차세대 Wi-Fi 표준 (2024년 상용화).

## 2. Wi-Fi 세대 비교

| 세대 | 표준 | 최대 속도 | 주파수 | 핵심 기술 |
|------|------|---------|--------|---------|
| Wi-Fi 5 | 802.11ac | 3.5Gbps | 5GHz | MU-MIMO |
| Wi-Fi 6/6E | 802.11ax | 9.6Gbps | 2.4/5/6GHz | OFDMA, TWT |
| **Wi-Fi 7** | **802.11be** | **46Gbps** | **2.4/5/6GHz** | **MLO, 320MHz, 4K-QAM** |

## 3. Wi-Fi 7 핵심 기술

```
[MLO (Multi-Link Operation) — 핵심!]
여러 주파수 대역을 동시에 사용
예) 5GHz + 6GHz 동시 → 대역폭+안정성 동시 향상
→ 지연 감소 + 처리량 증가

[320MHz 채널 대역폭]
Wi-Fi 6: 160MHz → Wi-Fi 7: 320MHz (2배)
주로 6GHz 대역 활용 (비혼잡)

[4K-QAM (4096-QAM)]
Wi-Fi 6: 1024-QAM (10비트/심볼)
Wi-Fi 7: 4096-QAM (12비트/심볼) → 20% 처리량 향상
SNR이 높은 근거리에서 효과적

[멀티 RU (Multi-RU)]
OFDMA에서 여러 자원단위 동시 할당 → 효율 향상

활용:
- XR (AR/VR): 저지연 + 고대역폭
- 산업 Wi-Fi: 실시간 제어, 이음5G 보완
- 게이밍: <1ms 지연
```

## 4. 답안 포인트

**3단락**: ① Wi-Fi 7 정의 & 이전 세대와 차이 → ② MLO/320MHz/4K-QAM 핵심 기술 → ③ 기업/산업 적용 & 이음5G와의 관계

## 5. 관련 개념

`5G 특화망(★133회)` → 실내 Wi-Fi 7 + 실외 이음5G 상호보완 | `XR` → Wi-Fi 7 기반 저지연 필요 | `샤논정리(★135회)` → 320MHz 대역폭의 용량 계산
