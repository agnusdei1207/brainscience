+++
weight = 50
title = "50. TPM & 하드웨어 보안"
date = "2026-05-17"
[extra]
categories = "gisulsa-computer-architecture"
+++

# 🎯 TPM & 하드웨어 신뢰 루트

> **별점**: ★★★★★ | 기본 필수

## 1. TPM (Trusted Platform Module)

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

## 2. Secure Boot & UEFI

```
[Secure Boot]
부팅 소프트웨어의 디지털 서명 검증
검증 실패 시 부팅 차단

[Secure Boot 체인]
UEFI 펌웨어(Secure Boot On)
  → 부트로더 서명 검증 (Microsoft 서명)
  → 커널 서명 검증
  → 모듈 서명 검증 (Linux DKMS)

[Windows Secure Boot DB]
db: 신뢰할 수 있는 인증서 목록
dbx: 차단 목록 (취약한 부트로더 해시)
KEK: 데이터베이스 업데이트 키
PK: 플랫폼 마스터 키
```

## 3. 신뢰 체인 (Chain of Trust)

```
RTM (Root of Trust for Measurement):
  측정의 시작점 (TPM = CRTM)

[전체 부팅 신뢰 체인]
CRTM (TPM) → BIOS/UEFI → MBR/부트로더
→ OS 커널 → OS 모듈
각 단계가 다음 단계를 검증

= Remote Attestation:
클라우드 VM이 TPM으로 부팅 무결성 증명
Confidential Computing의 기반
```

## 4. 답안 포인트

**3단락**: ① TPM 기능(PCR/Sealing/Attestation) → ② Secure Boot UEFI 체인 → ③ 신뢰 체인 & Confidential Computing 연계

## 5. 관련 개념

`Secure Boot(51번)` → TPM이 기반 | `TEE(52번)` → TPM + TEE = 하드웨어 보안 스택 | `Confidential Computing(53번)` → TPM 기반 원격 증명
