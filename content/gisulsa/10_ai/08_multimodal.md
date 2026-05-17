+++
weight = 8
title = "08. 멀티모달 AI & 생성AI"
date = "2026-05-17"
[extra]
categories = "gisulsa-ai"
+++

# 🎯 멀티모달 AI & 생성형 AI

> **별점**: ★★★★★ | ★135회, ★136회 기출

## 1. 멀티모달 AI

```
정의: 텍스트, 이미지, 오디오, 비디오 등 여러 모달리티를
     동시에 처리하는 AI 모델

[주요 멀티모달 모델]
GPT-4o: 텍스트+이미지+오디오 통합
  → 실시간 음성 대화, 이미지 분석

Gemini Ultra (Google):
  텍스트+이미지+비디오+오디오+코드
  
Claude 3: 텍스트+이미지 (PDF 분석)

DALL-E 3 / Imagen: 텍스트 → 이미지 생성
Stable Diffusion: 오픈소스 이미지 생성
Sora (OpenAI): 텍스트 → 비디오 생성

[기술 기반]
Vision Transformer (ViT): 이미지를 패치로 처리
CLIP: 이미지-텍스트 공동 임베딩
Flamingo: 멀티모달 Few-shot
```

## 2. 생성형 AI 기술

```
[확산 모델 (Diffusion Model)]
이미지 생성 핵심 기술
Forward: 이미지에 점진적 노이즈 추가
Reverse: 노이즈에서 이미지 복원 (학습)

[GAN vs 확산 모델]
GAN (생성적 적대 신경망):
  생성자 vs 판별자 경쟁
  불안정, 모드 붕괴 문제
  
확산 모델:
  더 안정적, 다양성 높음
  느린 추론 (수십~수백 스텝)
  → 현재 이미지 생성 표준

[VAE (변분 오토인코더)]
잠재 공간 표현 학습
이미지 압축·생성·변형
```

## 3. 실용적 생성AI 활용

```
[코드 생성]
GitHub Copilot: 코드 자동 완성
Cursor: AI 코드 에디터
Claude Code / Gemini CLI: 터미널 AI

[콘텐츠 생성]
Suno AI: 음악 생성
ElevenLabs: 음성 클로닝
HeyGen: 디지털 휴먼 비디오

[기업 적용]
RAG + 생성AI: 사내 문서 Q&A
코드 리뷰 자동화
문서 초안 작성 (법률, 의료)
```

## 4. 답안 포인트

**3단락**: ① 멀티모달 AI 정의 & 주요 모델 비교 → ② 확산 모델 원리 & GAN과 비교 → ③ 기업 실용 사례(RAG/코드생성/콘텐츠)

## 5. 관련 개념

`LLM(02번)` → 멀티모달의 언어 처리 기반 | `RAG(03번)` → 생성AI + 검색 결합 | `온디바이스AI(01_ca 40번)` → 경량 멀티모달 추론
