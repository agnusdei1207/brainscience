+++
weight = 9
title = "05. PQC (양자내성암호, Post-Quantum Cryptography)"
date = "2026-05-17"
[extra]
categories = "gisulsa-security"
+++

# PQC, NIST PQC 표준화, Kyber, Dilithium, 양자 위협

> 출제 빈도: ★★★★★ | 예측: ☆2026 확실 예측 (NIST 표준화 완료 2024)

---

## 답안.

### Ⅰ. 개요

PQC(Post-Quantum Cryptography, 양자내성암호)는 양자 컴퓨터의 Shor 알고리즘으로도 풀 수 없는 수학적 문제에 기반한 암호화 기술이다.
현재 RSA/ECC 기반 공개키 암호는 충분한 양자 컴퓨터(수백만 큐비트)가 등장하면 수 시간 내 해독 가능 → PQC로의 전환이 시급하다.

### Ⅱ. 핵심 구성요소

```
I. 양자 컴퓨터와 현재 암호체계 위협
   - 쇼어 알고리즘: RSA/ECC 인수분해/이산대수 → 다항 시간 해독
   - Harvest Now, Decrypt Later: 현재 암호문 수집 후 미래 해독
   - Y2Q(양자의 날): 2030년대 예상 → 지금부터 전환 필요

II. NIST PQC 표준화 (2024 완료)
   
   | 표준          | 알고리즘         | 기반 문제          | 용도    |
   |--------------|----------------|-----------------|--------|
   | FIPS 203     | ML-KEM (Kyber) | 격자 (LWE)       | 키 교환 |
   | FIPS 204     | ML-DSA (Dilithium)| 격자 (MLWE)   | 전자서명 |
   | FIPS 205     | SLH-DSA (SPHINCS+)| 해시 기반      | 전자서명 |
   | (예정)       | FN-DSA (FALCON)| 격자 (NTRU)      | 전자서명 |

III. PQC 핵심 수학적 기반
   
   1) 격자 기반 (Lattice): LWE (Learning With Errors)
      - n차원 격자에서 가장 짧은 벡터 찾기 (NP-hard)
      - Kyber, Dilithium의 기반
   
   2) 해시 기반 (Hash-based): SPHINCS+
      - 해시 함수의 단방향성에만 의존
      - 양자 내성 가장 확실하지만 서명 크기 큼
   
   3) 코드 기반 (Code-based): McEliece
      - 오래된 방식, 키 크기 매우 큼

IV. TLS 1.3 → Post-Quantum TLS 전환
   - 현재: ECDHE (TLS 1.3) → 2030년경: ML-KEM으로 교체


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
