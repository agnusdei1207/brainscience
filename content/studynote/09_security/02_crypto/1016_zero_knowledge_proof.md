+++
weight = 1016
title = "영지식 증명 (Zero Knowledge Proof, ZKP)"
date = "2024-03-25"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> | (비밀 함축값 전달)

> 📝 모범 답안

1. **프라이버시의 정수**: 자신이 어떤 비밀을 알고 있다는 사실을, 그 비밀의 구체적인 내용은 전혀 밝히지 않으면서 상대방에게 확실히 증명하는 암호학적 기법입니다.
2. **신뢰 구조의 혁신**: 'Trust'를 'Proof'로 치환하여 데이터 노출 없이 인증 및 검증이 가능한 신뢰 인프라를 구축합니다.
3. **블록체인·인증의 핵심**: ZK-Rollup, 프라이버시 코인(Zcash), DID(분산 신원인증) 등에서 확장성과 보안성을 동시에 확보하는 핵심 기술로 활용됩니다.

### 1. 개요 및 필요성
전통적인 인증 방식(ID/PW, 인증서)은 비밀번호나 개인키 자체를 검증 서버에 제시하거나 가공하여 전송하므로, 검증 서버가 해킹당할 경우 비밀이 노출될 위험이 큽니다. **영지식 증명(ZKP)**은 1985년 Shafi Goldwasser 등이 제안한 것으로, 증명자(Prover)가 검증자(Verifier)에게 "나는 비밀 $x$를 알고 있다"는 명제를 $x$에 대한 어떠한 정보도 주지 않고 확률적으로 완벽하게 증명합니다.

### 2. 구성요소
영지식 증명의 3대 조건(Completeness, Soundness, Zero-knowledge)을 만족하며, 최근에는 비대화형 방식(zk-SNARKs)이 주로 사용됩니다.

```text
[ Zero Knowledge Proof Interaction Model ]

Prover (증명자)           Verifier (검증자)
      |                         |
      | -- 1. Commitment -----      | <----- 2. Challenge --- | (무작위 난수 질문)
      | -- 3. Response -------> | (비밀 기반 답변 생성)
      |                         |
      |          [ 4. Verify ]  | (비밀 노출 없이 수식 검증)

<Bilingual Components>
- Commitment (약정): 증명자가 값을 고정함 (Prover commits to a value)
- Challenge (도전): 검증자의 무작위 질의 (Verifier's random query)
- Response (응답): 증명자의 수학적 해답 (Prover's mathematical answer)
- Witness (증거): 증명자가 가진 비밀 데이터 (The secret piece of information)
```

**핵심 알고리즘:**
1. **zk-SNARKs**: "Zero-Knowledge Succinct Non-Interactive Argument of Knowledge"의 약자로, 증명 크기가 작고 검증이 매우 빠른 비대화형 방식입니다.
2. **zk-STARKs**: 신뢰 설정(Trusted Setup)이 필요 없고 양자 내성을 갖춘 투명한 방식입니다.

### 3. 구조 및 동작 원리

| 비교 항목 | zk-SNARKs | zk-STARKs | 전통적 인증 (Traditional) |
|:---:|:---:|:---:|:---:|
| **프라이버시** | 최상 (비밀 노출 0%) | 최상 (비밀 노출 0%) | 낮음 (비밀 노출 위험) |
| **증명 크기** | 매우 작음 (Succinct) | 중간 | - |
| **신뢰 설정** | 필요 (Trusted Setup) | 불필요 (Transparent) | 불필요 |
| **양자 내성** | 낮음 | 높음 | 낮음 |
| **주요 활용** | Zcash, 이더리움 L2 | StarkNet, 확장성 중시 | 일반 웹 로그인 |

### 4. 비교 및 트레이드오프
**실무 적용 전략:**
- **분산 신원인증 (DID)**: 성인 여부를 증명할 때, 생년월일을 공개하지 않고 "나는 19세 이상이다"라는 명제만 증명하여 개인정보를 보호합니다.
- **ZK-Rollups**: 레이어 2 블록체인에서 수천 개의 트랜잭션을 하나로 묶어 증명(Validity Proof)만 레이어 1에 기록함으로써 확장성을 폭발적으로 늘립니다.
- **익명 투표 시스템**: 투표권이 있다는 사실은 증명하되, 내가 누구인지는 노출하지 않는 안전한 전자 투표를 구현합니다.

**기술사적 판단:**
"과거의 ZKP는 연산 복잡도가 너무 높아 실무 적용이 어려웠으나, 현재는 하드웨어 가속(FPGA, ASIC)과 알고리즘 최적화를 통해 임계점을 넘었습니다. 특히 데이터 주권이 강조되는 MyData 사업이나 클라우드 보안 환경에서 **'데이터를 주지 않고도 가치를 검증'**하는 ZKP는 필수 아키텍처가 될 것입니다."

### 5. 실무 적용 및 최적화 기법
영지식 증명은 "알지 못해도 믿을 수 있는" 세상을 만듭니다. 이는 향후 양자 컴퓨팅 시대의 새로운 암호화 표준으로 진화할 것이며, 개인정보 보호와 규제 준수(Compliance)라는 두 마리 토끼를 잡는 유일한 기술적 해법이 될 것입니다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위 개념**: Privacy-preserving Technology, Cryptography
- **유사 개념**: FHE (동형암호), MPC (다자간 연산)
- **하위 기술**: zk-SNARKs, zk-STARKs, Bulletproofs

### 👶 어린이를 위한 3줄 비유 설명
1. "나 이 방 비밀번호 알아!"라고 말하면서, 비밀번호를 알려주지 않고도 그 방 안에서만 가져올 수 있는 인형을 보여주는 것과 같아요.
2. 상대방은 비밀번호는 끝까지 모르지만, 내가 비밀번호를 안다는 건 확실히 믿게 되죠.
3. 이렇게 비밀은 꽁꽁 숨기면서 "나 다 알아!"라고 증명하는 똑똑한 암호 기술이랍니다!
