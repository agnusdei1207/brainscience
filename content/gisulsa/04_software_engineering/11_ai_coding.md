+++
weight = 11
title = "11. AI 기반 코드 생성"
date = "2026-05-17"
[extra]
categories = "gisulsa-sw-engineering"
+++

# AI 기반 코드 생성 (GitHub Copilot, AI 코딩)

> 별점: ★★★★★ | ★134회, ★136회 기출

---

## 답안.

### Ⅰ. 개요

AI 코드 생성: LLM(대형언어모델)이 자연어 주석·프롬프트를 기반으로 코드를 자동 생성·완성·리뷰하는 기술. Agentic AI 시대에 SW 개발 방식 근본 변화 유발.

### Ⅱ. 핵심 구성요소

```
[도구 비교]
도구              기반 모델         주요 기능
GitHub Copilot   OpenAI Codex     IDE 내 코드 자동완성
Amazon CodeWhisperer AWS 자체       보안 취약점 스캐닝 통합
Google Gemini Code Google Gemini   멀티파일 컨텍스트
Cursor IDE       Claude/GPT-4     에이전틱 코딩
Devin AI         (AI SW 엔지니어)  자율 개발 (실험적)

[주요 기능]
- 코드 자동완성 (Next-line, Function)
- 테스트 코드 자동 생성
- 코드 리뷰 자동화 (보안·품질)
- 문서 생성 (Docstring, README)
- 버그 탐지 & 수정 제안
```
```
위험 요소:
- 저작권: 학습 데이터 라이선스 문제 (오픈소스 코드)
- 보안: AI 생성 코드에 취약점 패턴 포함 위험
- 환각: 존재하지 않는 API 호출 (hallucination)
- 과신: 검토 없이 생성 코드 사용 → 품질 저하

대응 방안:
- SAST/DAST 파이프라인 통합 자동 검증
- 코드 리뷰 필수화 (AI가 작성해도 인간이 검토)
- SBOM: AI 생성 코드의 의존성 추적
```


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
