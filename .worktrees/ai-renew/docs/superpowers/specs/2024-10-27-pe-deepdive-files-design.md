# Design Spec: 9 New Deep-Dive Markdown Files for PE Studynotes

## 1. Overview
As an expert Professional Engineer (PE), implement 9 new deep-dive markdown files for missing keywords in three domains: Algorithm/Stats, Security, and AI.

## 2. Target Files & Keywords

### Domain 8: Algorithm / Stats (`content/studynote/8_algorithm_stats/3_graph_search/`)
1. **62_hamiltonian_path.md**: Hamiltonian Path (해밀턴 경로) - NP-complete problem.
2. **63_tsp.md**: Traveling Salesman Problem (외판원 문제) - NP-hard optimization.
3. **64_lcs.md**: Longest Common Subsequence (최장 공통 부분수열) - DP approach.

### Domain 9: Security (`content/studynote/9_security/1_intro_principles/`)
4. **006_non_repudiation.md**: Non-repudiation (부인방지) - Digital signatures and evidence.
5. **007_accountability.md**: Accountability (책임추적성) - Audit logs and tracking.
6. **008_privacy_3_elements.md**: Privacy 3 Elements (개인정보보호 3요소) - Confidentiality, Integrity, Accessibility.

### Domain 10: AI (`content/studynote/10_ai/3_transformer_llm/`)
7. **128_encoder_decoder_attention.md**: Encoder-Decoder Attention (인코더-디코더 어텐션) - Cross attention.
8. **129_feed_forward_network_transformer.md**: Feed-Forward Network (피드 포워드 신경망) - Position-wise FFNN.
9. **130_foundation_model.md**: Foundation Model (파운데이션 모델) - Pre-trained large-scale models.

## 3. Mandatory Structure
Each file MUST include:
- `+++` Frontmatter: `weight`, `title`, `date`, `[extra] categories`.
- `## 핵심 인사이트 (3줄 요약)`
- `### Ⅰ. 개요 (Context & Background)`
- `### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)` with a BILINGUAL ASCII diagram.
- `### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)` with a Markdown table.
- `### Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)`
- `### Ⅴ. 기대효과 및 결론 (Future & Standard)`
- `### 📌 관련 개념 맵 (Knowledge Graph)`
- `### 👶 어린이를 위한 3줄 비유 설명`

## 4. Quality Standards
- Technical terms in Korean (with English in parentheses).
- Professional Engineer (PE) tone: analytical, strategic, and architecture-focused.
- Valid Markdown and Frontmatter.
