+++
weight = 408
title = "408. Layer 2 롤업 Optimistic vs ZK 차이 (Layer 2 Rollup)"
date = "2026-04-21"
[extra]
categories = "studynote-enterprise-systems"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Layer 2 롤업(Rollup)은 Ethereum Layer 1의 확장성 한계(~15 TPS)를 해결하기 위해 트랜잭션을 오프체인에서 일괄 처리하고, 압축된 데이터만 Layer 1에 기록하는 확장성 솔루션이다.
> 2. **가치**: Optimistic Rollup은 사기 증명(Fraud Proof) 기반으로 단순하고 EVM 호환성이 높으며, ZK Rollup은 유효성 증명(Validity Proof) 기반으로 즉시 확정성(Finality)과 높은 보안을 제공한다.
> 3. **판단 포인트**: Optimistic은 7일 출금 대기(사기 증명 기간)가 핵심 단점, ZK는 증명 생성 비용(Prover Time)이 핵심 단점으로, 사용 사례에 따른 선택이 필요하다.

## Ⅰ. 개요 및 필요성

Ethereum Layer 1은 탈중앙화와 보안을 우선하여 TPS가 약 15~30으로 제한된다. Visa는 24,000 TPS를 처리하므로 대규모 채택을 위한 확장성 해결이 필수다. Layer 2는 Layer 1 보안을 활용하면서 오프체인 처리로 TPS를 수백~수천 배 향상시킨다.

롤업(Rollup)은 현재 가장 유망한 Layer 2 솔루션으로, Ethereum 재단이 공식 지지하는 스케일링 로드맵의 핵심이다.

📢 **섹션 요약 비유**: Layer 2 롤업은 고속도로 도우미 도로 — 메인 고속도로(Layer 1)는 막혀도, 옆 도로(Layer 2)에서 먼저 처리하고 결과만 메인 도로 요금소(스마트 컨트랙트)에 보고한다.

## Ⅱ. 아키텍처 및 핵심 원리

```
Layer 1 (Ethereum)
  ┌──────────────────────────────────────────────────────┐
  │  Rollup 스마트 컨트랙트 (상태 루트 + 트랜잭션 데이터)  │
  └──────────────────────────────────────────────────────┘
           ↑ 압축 데이터 제출       ↑ 사기/유효성 증명
  
Layer 2 (Rollup 체인)
  ┌─────────────────────┐    ┌─────────────────────┐
  │  Optimistic Rollup  │    │    ZK Rollup         │
  │  - 기본 유효 가정    │    │  - ZKP로 유효성 증명  │
  │  - 7일 사기 증명 기간│    │  - 즉시 확정성        │
  │  - EVM 호환(Arbitrum)│    │  - 증명 생성 비용 높음│
  │  Arbitrum, Optimism  │    │  zkSync, StarkNet    │
  └─────────────────────┘    └─────────────────────┘
```

| 항목 | Optimistic Rollup | ZK Rollup |
|:---|:---|:---|
| 유효성 증명 방식 | 사기 증명(Fraud Proof) | 수학적 증명(ZKP) |
| 출금 대기 시간 | 7일(사기 증명 기간) | 수 분(즉시 확정) |
| EVM 호환성 | 높음(기존 코드 이전 용이) | 낮음/증가 중(zkEVM) |
| TPS | 수백~1,000 | 수천 |
| 대표 프로젝트 | Arbitrum, Optimism | zkSync Era, StarkNet |
| 가스 절감 | 10~100x | 50~100x |

📢 **섹션 요약 비유**: Optimistic은 "믿고 보내고, 문제 있으면 7일 내 신고" — ZK는 "보내기 전에 수학으로 완벽 증명"이다.

## Ⅲ. 비교 및 연결

Data Availability(DA): 롤업의 트랜잭션 데이터를 어디에 저장하느냐가 보안의 핵심. Layer 1에 저장하면 비용이 높고(On-chain DA), Celestia 같은 별도 DA 레이어를 쓰면 비용이 낮다(Off-chain DA, Validium). EIP-4844(Proto-Danksharding): Ethereum의 Blob 트랜잭션으로 롤업 데이터 비용을 10~100x 절감.

📢 **섹션 요약 비유**: Data Availability는 계약서 원본 보관 — Layer 1(금고)에 보관하면 안전하지만 비싸고, 외부 창고(DA 레이어)에 보관하면 저렴하지만 약간의 신뢰 가정이 필요하다.

## Ⅳ. 실무 적용 및 기술사 판단

**의사결정 포인트**:
- EVM 앱 빠른 이전: Arbitrum(Optimistic) — 코드 수정 최소화
- 고성능·즉시 출금: zkSync Era(ZK) — 사용자 경험 우선
- DeFi 고빈도 거래: ZK Rollup (즉시 확정, 높은 TPS)
- NFT/게임: 가스비 절감이 중요 → 두 방식 모두 적합

📢 **섹션 요약 비유**: Optimistic은 오래된 도로에 포장만 새로(EVM 호환), ZK는 완전히 새로 설계한 고속도로(최적 성능)이다.

## Ⅴ. 기대효과 및 결론

Layer 2 롤업은 Ethereum의 TPS 한계를 10~100배 이상 향상시키면서 Layer 1 보안을 유지하는 현재 최선의 확장성 솔루션이다. Optimistic은 EVM 호환성과 단순성, ZK는 성능과 즉시 확정성에서 우위이며 zkEVM 발전으로 EVM 호환 ZK Rollup이 주류가 될 전망이다.

📢 **섹션 요약 비유**: Layer 2는 블록체인의 전기차 혁명 — 같은 도로(Layer 1 보안)를 쓰면서 훨씬 효율적으로(낮은 가스, 높은 TPS) 달린다.

### 📌 관련 개념 맵

| 개념 | 관계 | 설명 |
|:---|:---|:---|
| Optimistic Rollup | 구현 방식 1 | 사기 증명 기반, 7일 대기 |
| ZK Rollup | 구현 방식 2 | 유효성 증명 기반, 즉시 확정 |
| Fraud Proof | Optimistic 핵심 | 사기 트랜잭션 이의 제기 메커니즘 |
| Validity Proof (ZKP) | ZK 핵심 | 수학적 유효성 증명 |
| EIP-4844 | 비용 절감 | Blob 트랜잭션으로 DA 비용 감소 |

### 👶 어린이를 위한 3줄 비유 설명

1. Layer 2는 지하도 — 막힌 지상 도로(Layer 1) 대신 지하로 빠르게 이동하다가 목적지 근처에서 올라와.
2. Optimistic은 신뢰 계약 — 먼저 통과시키고, 7일 안에 이의 제기가 없으면 OK.
3. ZK는 입장권 검사 — 들어오기 전에 수학 증명(입장권)을 확인해서 즉시 통과!
