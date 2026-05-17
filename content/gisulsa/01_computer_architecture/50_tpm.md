+++
weight = 50
title = "50. TPM & 하드웨어 보안"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# TPM & 하드웨어 신뢰 루트

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

정의: 암호화 키, 인증서, 해시 값을 안전하게 저장하는
     보안 전용 하드웨어 칩 (ISO/IEC 11889)
키 생성·저장: 개인키가 TPM 밖으로 나가지 않음

### Ⅱ. 핵심 구성요소

```
정의: 암호화 키, 인증서, 해시 값을 안전하게 저장하는
     보안 전용 하드웨어 칩 (ISO/IEC 11889)

[TPM 핵심 기능]
키 생성·저장: 개인키가 TPM 밖으로 나가지 않음
PCR (Platform Configuration Register):
  시스템 부팅 과정의 해시값 누적 저장
  각 부팅 컴포넌트 → SHA-256 → PCR 확장
Sealing: 특정 PCR 값일 때만 데이터 복호화
Attestation: TPM이 서명으로 플랫폼 무결성 증명

[TPM 버전]
TPM 1.2: SHA-1, RSA-2048
TPM 2.0: SHA-256, ECC, AES (현재 표준)
  Windows 11: TPM 2.0 필수 요건

[적용]
BitLocker: 디스크 암호화 키를 TPM에 저장
원격 증명: TPM이 서버에 부팅 무결성 증명
Device Identity: 디바이스 고유 인증서
```
```
[Secure Boot]
부팅 소프트웨어의 디지털 서명 검증
검증 실패 시 부팅 차단

[Secure Boot 체인]
UEFI 펌웨어(Secure Boot On)
  → 부트로더 서명 검증 (Microsoft 서명)


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
