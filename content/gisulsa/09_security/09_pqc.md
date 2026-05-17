+++
weight = 9
title = "05. PQC (양자내성암호, Post-Quantum Cryptography)"
date = "2026-05-17"
[extra]
categories = "gisulsa-security"
exam = "☆ 2026~2027 확실 예측"
+++

# 🎯 핵심 키워드: PQC, NIST PQC 표준화, Kyber, Dilithium, 양자 위협

> **출제 빈도**: ★★★★★ | **예측**: ☆2026 확실 예측 (NIST 표준화 완료 2024)

## 1. 정의

PQC(Post-Quantum Cryptography, 양자내성암호)는 양자 컴퓨터의 Shor 알고리즘으로도 풀 수 없는 수학적 문제에 기반한 암호화 기술이다.

현재 RSA/ECC 기반 공개키 암호는 충분한 양자 컴퓨터(수백만 큐비트)가 등장하면 수 시간 내 해독 가능 → PQC로의 전환이 시급하다.

## 2. 양자 컴퓨터 위협

| 현재 암호 | 위협 알고리즘 | 공격 복잡도 |
|----------|-------------|-----------|
| RSA-2048 | Shor | 다항 시간 |
| ECC | Shor | 다항 시간 |
| AES-256 | Grover | 2^128 → 허용 |
| SHA-256 | Grover | 2^128 → 허용 |

→ **비대칭 암호(RSA/ECC): 즉시 교체 필요** / 대칭암호(AES): 키 길이 두 배로 보완

## 3. 답안 목차 템플릿

**문제**: "양자 컴퓨터 위협에 대응하는 PQC(양자내성암호)의 개념과 NIST 표준화 현황을 설명하시오."

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
   - 하이브리드 PQC: ECDH + ML-KEM 동시 사용 (전환 기간)
   - NIST 권고: 2030년까지 PQC 전환 완료
   
   국내: KPQC (한국 PQC 공모전), NIST 기반 국내 표준화 진행

V. 컴시응 시험 관점 적용 포인트
   - 국가 중요 정보시스템 → 2030년 PQC 전환 의무화 예상
   - 인증서(X.509) → PQC 알고리즘 대체
   - 감리: PQC 적용 여부 체크리스트 포함 예상
```

## 4. 핵심 암기 포인트

- **Kyber(ML-KEM)**: NIST PQC 키 교환 표준 (격자 기반)
- **Dilithium(ML-DSA)**: NIST PQC 서명 표준 (격자 기반)
- **Harvest Now, Decrypt Later**: PQC 전환 긴급성의 핵심 논거

## 5. 관련 개념 연결

| 개념 | 연결 포인트 |
|------|------------|
| TLS 1.3 (★136회) | PQC로 키 교환 알고리즘 교체 |
| 동형암호 (★133회) | 함께 언급되는 차세대 암호 |
| 양자통신 (QKD) | PQC와 다른 접근 (HW 기반) |
| PKI / 전자서명 | PQC 전자서명으로 교체 필요 |
| 국가 보안 가이드라인 | 2030 PQC 전환 권고 |
