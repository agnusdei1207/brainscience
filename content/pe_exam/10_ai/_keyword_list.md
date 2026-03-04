+++
title = "10. 인공지능 키워드 목록 (완전판)"
date = 2026-03-03
[extra]
categories = "pe_exam-ai"
+++

# 인공지능 (AI) 키워드 목록 — 완전판

정보통신기술사·컴퓨터응용시스템기술사 대비 AI 전 영역 기술사 수준 핵심 키워드
> ⚡ 기술사 AI 문제: 단순 개념이 아닌 **설계 판단·도입 전략·아키텍처 결정·위험 분석·거버넌스**까지 통합 서술 요구

---

## 1. AI / 머신러닝 기초 이론 — 40개

1. 인공지능 (AI) 정의 — 약인공지능(Narrow AI) / 강인공지능(AGI) / 초인공지능(ASI)
2. 튜링 테스트 (Turing Test) — AI 지능 판단 기준
3. 기계학습 (Machine Learning) — 데이터 기반 패턴 학습, 명시적 프로그래밍 대체
4. 지도학습 (Supervised Learning) — 분류(Classification) / 회귀(Regression)
5. 비지도학습 (Unsupervised Learning) — 군집화 / 차원축소 / 생성 모델
6. 준지도학습 (Semi-supervised Learning) — 소량 레이블 + 대량 비레이블
7. 자기지도학습 (Self-supervised Learning) — 자체 레이블 생성, BERT/MAE/SimCLR
8. 강화학습 (Reinforcement Learning) — 에이전트/환경/보상(Reward)/정책(Policy)/가치함수
9. POMDP (Partially Observable MDP) — 부분 관측 환경
10. 전이학습 (Transfer Learning) — 사전훈련 → 파인튜닝, 도메인 적응
11. 메타학습 (Meta-Learning) — MAML, Prototypical, Reptile
12. 연합학습 (Federated Learning) — 데이터 분산, 프라이버시 보존
13. 능동학습 (Active Learning) — 불확실한 샘플 선택, Committee Query
14. 온라인학습 (Online Learning) — 스트리밍 데이터, SGD 기반
15. 지속 학습 (Continual Learning) — 파국적 망각(Catastrophic Forgetting), EWC
16. 멀티태스크 학습 (Multi-task Learning) — 공유 표현, 태스크 간 정규화
17. 경사하강법 — SGD / Momentum / Adam / AdamW / LAMB / Lion / Adadelta
18. 학습률 스케줄러 — Cosine Annealing / Linear Warmup / OneCycleLR
19. 역전파 (Backpropagation) — 연쇄 법칙, 계산 그래프, 자동 미분 (AutoDiff)
20. 손실 함수 — MSE / MAE / Cross-Entropy / Focal Loss / CTC / KL Divergence
21. 편향-분산 트레이드오프 (Bias-Variance Tradeoff)
22. 과적합 / 과소적합 — Overfitting, Underfitting 진단 및 처방
23. 정규화 — L1(Lasso) / L2(Ridge) / Elastic Net / Dropout / BatchNorm / LayerNorm
24. 교차검증 — k-Fold / Stratified k-Fold / LOOCV / Time-Series CV
25. 하이퍼파라미터 최적화 (HPO) — Grid / Random / Bayesian / Optuna / Ray Tune
26. 앙상블 — Bagging(Random Forest) / Boosting(XGBoost/LightGBM/CatBoost) / Stacking
27. 결정 트리 (Decision Tree) — CART, ID3, C4.5, 불순도(Gini/Entropy)
28. SVM (Support Vector Machine) — 마진 최대화, 커널 트릭 (RBF/Poly/Sigmoid)
29. k-NN (k-Nearest Neighbor) — 비파라미터, 거리 기반 분류
30. 나이브 베이즈 (Naive Bayes) — 조건 독립 가정, 텍스트 분류
31. 군집화 — K-Means / DBSCAN / 계층적 군집 / Gaussian Mixture Model
32. 차원 축소 — PCA / t-SNE / UMAP / ICA / Autoencoder
33. 이상 탐지 (Anomaly Detection) — Isolation Forest / One-Class SVM / VAE
34. 데이터 증강 (Data Augmentation) — 이미지/텍스트/시계열/음성
35. 불균형 데이터 — SMOTE / ADASYN / 클래스 가중치 / Focal Loss
36. 특성 공학 (Feature Engineering) — 선택(Filter/Wrapper/Embedded) / 추출
37. AutoML — H2O.ai / Google AutoML / Auto-sklearn / FLAML / TPOT
38. NAS (Neural Architecture Search) — DARTS, EfficientNet 설계 자동화
39. 기계 망각 (Machine Unlearning) — GDPR 삭제권, 선택적 데이터 제거
40. 합성 데이터 (Synthetic Data) — GAN/VAE/Diffusion 기반 프라이버시 대체

---

## 2. 딥러닝 심화 아키텍처 — 45개

### 기본 구조 및 원리
1. 퍼셉트론 (Perceptron) — 단층/다층, Rosenblatt 1957
2. MLP (Multi-Layer Perceptron) — Feedforward, 완전연결층
3. 활성화 함수 — Sigmoid / Tanh / ReLU / Leaky ReLU / GELU / Swish / SiLU / Mish
4. 소멸하는 그래디언트 (Vanishing Gradient) — BatchNorm · ResNet · LSTM으로 해결
5. 폭발하는 그래디언트 (Exploding Gradient) — Gradient Clipping, 가중치 초기화
6. 가중치 초기화 — Xavier (Glorot) / He (Kaiming) / Orthogonal
7. 배치 정규화 (Batch Normalization) — 내부 공변량 이동 해결
8. 레이어 정규화 (Layer Normalization) — Transformer 기본, 배치 독립
9. 그룹 정규화 (Group Normalization) — 소배치에 유리
10. Residual Connection / Skip Connection — ResNet, 깊은 망 학습 가능
11. Dense Connection — DenseNet, 모든 이전 층 연결
12. Dropout / DropBlock / DropPath / Spatial Dropout

### CNN 계열
13. CNN 구조 — 합성곱/풀링/완전연결, 파라미터 공유, 지역 수용 필드
14. CNN 발전사 — LeNet → AlexNet → VGG → GoogLeNet → ResNet → EfficientNet → ConvNeXt v2
15. Depthwise Separable Convolution — MobileNet, 경량화
16. Dilated Convolution (Atrous) — 해상도 유지 receptive field 확대
17. Deformable Convolution — 변형 가능한 수용 필드
18. 객체 탐지 패러다임 — 1-stage (YOLO/SSD) vs 2-stage (RCNN 계열)
19. YOLO v5/v8/v9/v10 — 실시간 객체 탐지, anchor-free
20. Faster R-CNN → DETR → DAB-DETR → Co-DETR
21. 이미지 분할 — U-Net / DeepLab v3+ / Mask R-CNN / SAM (Segment Anything)
22. SAM 2 — 비디오 세그멘테이션, 프롬프터블
23. Vision Transformer (ViT) — 이미지 패치 → 토큰화, Self-Attention

### RNN 계열
24. RNN (Recurrent Neural Network) — 순서 의존성, 은닉 상태 전달
25. LSTM (Long Short-Term Memory) — Input/Forget/Output 게이트, 장기 의존성
26. GRU (Gated Recurrent Unit) — Reset/Update 게이트, 경량 LSTM
27. Bidirectional RNN/LSTM — 양방향, 문맥 파악 강화

### Transformer 심화
28. Self-Attention 수식 — Attention(Q,K,V) = softmax(QK^T/√d_k)V
29. Multi-Head Attention — 다수 Head 병렬, 다양한 부분 공간 학습
30. Cross-Attention — Encoder-Decoder 간 어텐션
31. Causal Attention (Masked) — 자기회귀 모델에서 미래 토큰 차단
32. Flash Attention / Flash Attention 2 / 3 — IO-Aware 구현, 메모리·속도 최적화
33. RoPE (Rotary Position Embedding) — LLaMA 계열 위치 인코딩
34. ALiBi (Attention with Linear Biases) — 외삽 가능 위치 인코딩
35. Mamba (State Space Model, SSM) — 선형 복잡도, 장문 처리
36. Mamba 2 / Jamba — SSM + Attention 혼합
37. Mixture of Experts (MoE) — Sparse MoE, 라우터, GPT-4/DeepSeek-V3

### 생성 모델
38. GAN (Generative Adversarial Network) — 생성자/판별자, Mode Collapse
39. Progressive GAN / StyleGAN2/3 — 고품질 이미지 생성
40. VAE (Variational Autoencoder) — 잠재 공간, ELBO, Reparameterization
41. Diffusion Model (DDPM/DDIM) — 노이즈 제거 과정, Score Matching
42. Latent Diffusion (LDM) — 잠재 공간 확산, Stable Diffusion 기반
43. Flow Matching — Rectified Flow, Consistent Flow

### 특수 구조
44. GNN (Graph Neural Network) — GCN / GraphSAGE / GAT / GIN / DiffPool
45. Capsule Network — 동적 라우팅, 자세 불변성
46. Neural ODE — 연속 깊이, 불규칙 시계열
47. JEPA (Joint-Embedding Predictive Architecture) — Yann LeCun 세계 모델 비전

---

## 3. LLM (대형 언어 모델) 완전 심화 — 50개

### LLM 아키텍처
1. LLM (Large Language Model) 개념 — 대규모 Transformer 기반 언어 모델
2. 주요 LLM — GPT-4o / Claude 3.7 / Gemini 2.0 / LLaMA 3.3 / DeepSeek-V3 / Qwen2.5
3. Foundation Model / Base Model — 특화 전의 범용 사전훈련 모델
4. 스케일링 법칙 (Scaling Law) — Kaplan 2020, Chinchilla 최적 비율 (D ≈ 20N)
5. 창발적 능력 (Emergent Abilities) — 규모 임계점에서 갑작스러운 능력 출현
6. 컨텍스트 윈도우 (Context Window) — 1M+ 토큰 (Gemini), 200K (Claude), 위치인코딩 한계
7. 토크나이제이션 — BPE (GPT) / WordPiece (BERT) / SentencePiece / Unigram LM / Tiktoken
8. 어휘 크기 (Vocabulary Size) — GPT-4: 100K / LLaMA 3: 128K / 한국어 tokenizer 이슈
9. KV Cache — Key-Value 캐시, 긴 시퀀스 추론 메모리, PagedAttention (vLLM)
10. Prefill vs Decode — 사전 채우기(병렬) vs 토큰 생성(순차), 지연 특성 차이
11. Speculative Decoding — 초안 모델 + 검증 모델, 추론 가속
12. Continuous Batching — 동사 요청 배치 처리, vLLM, SGLang
13. Beam Search / Greedy Decoding / Sampling — 생성 전략
14. Temperature / Top-p / Top-k / Repetition Penalty — 생성 제어 파라미터
15. 긴 컨텍스트 처리 — RoPE 외삽, YaRN, LongRoPE, 슬라이딩 윈도우 어텐션

### LLM 훈련 파이프라인
16. 사전훈련 (Pre-training) — 인터넷 코퍼스, Common Crawl, The Pile
17. SFT (Supervised Fine-Tuning) — 지시 데이터셋 (Alpaca, ShareGPT)
18. RLHF (Reinforcement Learning from Human Feedback) — InstructGPT 방법론
19. PPO (Proximal Policy Optimization) — RLHF 핵심 RL 알고리즘
20. RLAIF (RL from AI Feedback) / Constitutional AI — Claude 접근법
21. DPO (Direct Preference Optimization) — 보상 모델 없는 RLHF 단순화
22. IPO / KTO / ORPO — DPO 계열 변형 정렬 기법
23. Reward Model (RM) — 선호도 점수 학습, Bradley-Terry 모델
24. Process Reward Model (PRM) — 단계별 추론 보상, Math 문제 특화

### PEFT / 효율 파인튜닝
25. PEFT (Parameter-Efficient Fine-Tuning) — 일부 파라미터만 업데이트
26. LoRA (Low-Rank Adaptation) — 저랭크 행렬 삽입 (r=8~64)
27. QLoRA — 4비트 NF4 양자화 + LoRA, 24GB GPU에서 65B 모델 파인튜닝
28. DoRA (Weight-Decomposed LoRA) — 크기/방향 분리
29. Adapter Tuning — Houlsby 어댑터, 병목층 삽입
30. Prefix Tuning — KV 공간에 학습 가능한 접두사
31. Prompt Tuning — 임베딩 공간 소프트 프롬프트
32. Instruction Tuning — FLAN-T5, WizardLM, Orca

### 추론 / 프롬프팅
33. 프롬프트 엔지니어링 (Prompt Engineering) — 구조화된 입력 설계
34. Zero-shot / Few-shot / Many-shot Prompting
35. Chain-of-Thought (CoT) — "Let's think step by step", Wei et al. 2022
36. Zero-shot CoT — 추론 유도 suffix
37. Self-Consistency CoT — 다수 CoT 경로 + 다수결 집계
38. Tree-of-Thought (ToT) — 트리 탐색 기반 추론
39. Graph-of-Thought (GoT) — 비선형 추론 그래프
40. ReAct (Reasoning + Acting) — 추론-행동-관찰 루프
41. Reflexion — 언어 피드백으로 에이전트 자체 개선
42. System Prompt / User Prompt / Assistant — 역할 기반 프롬프트 구조
43. Role Prompting — 역할 부여로 전문성 향상
44. Structured Output (JSON Mode) — 형식화된 응답 강제
45. Function Calling / Tool Calling — OpenAI API, Anthropic API 도구 호출
46. 스케일링 추론 (Test-Time Compute Scaling) — o1/o3/R1 접근법
47. Extended Thinking (Claude) — 사고 과정을 분리된 블록으로 출력

### LLM 평가
48. MMLU — 57개 분야 학문 지식 평가
49. HumanEval / MBPP / SWE-bench — 코드 생성 평가
50. MT-Bench / Chatbot Arena / LMSYS — 대화 능력 평가

---

## 4. AI 에이전트 / 오케스트레이션 심화 — 48개

### 에이전트 기초
1. AI 에이전트 (AI Agent) 정의 — 지각(Perception) / 추론(Reasoning) / 행동(Action) / 학습 사이클
2. 에이전트 유형 — 반응형 / 목표 기반 / 유틸리티 기반 / 학습 에이전트
3. 자율성 수준 — Semi-autonomous vs Fully Autonomous
4. 에이전트 루프 — Perceive → Plan → Act → Observe → Repeat
5. Tool Use / Function Calling — LLM이 외부 API·도구 호출
6. ReAct (Reasoning + Acting) 패턴 — Thought → Action → Observation
7. Plan-and-Execute — 계획 생성 후 단계별 실행
8. Reflexion — 언어 피드백 기반 자체 반성 및 개선
9. LATS (Language Agent Tree Search) — MCTS + 언어 에이전트
10. Voyager — Minecraft 자기 개선 에이전트, 기술 라이브러리

### 에이전트 메모리
11. 에이전트 메모리 유형 — 단기(In-Context) / 장기(External DB) / 에피소드 / 의미(Semantic) / 절차
12. 메모리 저장소 — 벡터 DB / 그래프 DB / SQL / Key-Value
13. 메모리 검색 — HNSW / IVF / PQ 기반 ANN 검색
14. MemGPT — 메모리 계층 관리 에이전트 자체 운영
15. Working Memory vs Long-term Memory
16. 망각 메커니즘 (Forgetting Mechanisms) — 에이전트 메모리 관리

### 다중 에이전트 시스템
17. MAS (Multi-Agent System) — 분산 에이전트 협업
18. 오케스트레이터-워커 패턴 — 중앙 조율자 + 전문 워커
19. 계층적 에이전트 (Hierarchical Agents) — Manager → Sub-Agents
20. 에이전트 역할 분담 — 연구자 / 작성자 / 비평가 / 실행자
21. 에이전트 간 통신 — 메시지 패싱, 공유 상태, 블랙보드 패턴

### 오케스트레이션 프레임워크
22. LangChain — 체인/에이전트/메모리/도구/프롬프트 템플릿 통합
23. LangGraph — 상태 그래프(StateGraph) 기반 에이전트 워크플로우, 사이클 지원
24. LangGraph State — 노드/엣지/조건부 라우팅, 체크포인팅
25. LangSmith — LLM 가관측성, 추적, 평가, 프롬프트 레지스트리
26. LlamaIndex — 데이터 연결·인덱싱·질의 엔진, RAG 파이프라인
27. CrewAI — 역할 기반 다중 에이전트, Crew/Agent/Task/Tool 구조
28. AutoGen (Microsoft) v0.4 — 비동기 이벤트 기반, 코드 실행 에이전트
29. AutoGen Studio — 로우코드 에이전트 빌더
30. Microsoft Semantic Kernel — 플러그인 기반 AI 오케스트레이션 (.NET/Python)
31. Microsoft Agent Framework — AutoGen + Semantic Kernel 통합 (2025)
32. DSPy — 선언적 LLM 파이프라인 최적화, 컴파일러 개념
33. Haystack — 검색·QA 파이프라인 프레임워크
34. Flowise / n8n / Dify — 로우코드 LLM 워크플로우 빌더

### 에이전트 표준 프로토콜
35. MCP (Model Context Protocol) — Anthropic 제안, "USB-C for AI", 에이전트↔도구 통합 표준
36. MCP 서버/클라이언트 — 도구·데이터소스를 MCP 서버로 래핑
37. A2A (Agent-to-Agent Protocol) — Google 제안, "TCP/IP for AI Agents", 에이전트 간 통신 표준
38. A2A Agent Card — 에이전트 능력 선언, 디스커버리
39. OpenAPI / AsyncAPI — 도구 정의 스키마
40. JSON Schema — 도구 파라미터 타입 정의

### 에이전트 RAG / 검색 심화
41. Naive RAG → Advanced RAG → Modular RAG — 발전 단계
42. Pre-Retrieval — 쿼리 재작성(Query Rewriting), HyDE (가상 문서 임베딩)
43. Post-Retrieval — Reranking, Contextual Compression, MapReduce
44. Agentic RAG — 에이전트가 검색 전략 결정, 반복적 개선
45. Corrective RAG (CRAG) — 검색 결과 신뢰도 평가 후 재검색
46. Self-RAG — 자기 반성을 통한 검색 필요성 판단
47. GraphRAG (Microsoft) — 지식 그래프 + RAG, 글로벌·로컬 탐색
48. Multi-hop RAG — 복수 검색 단계를 거친 복잡한 질문 처리

---

## 5. 벡터 검색 / 임베딩 — 20개

1. 벡터 임베딩 (Vector Embedding) — 의미 공간, 고차원 밀집 벡터
2. 텍스트 임베딩 모델 — text-embedding-3 (OpenAI) / E5 / BGE / GTE / Nomic Embed
3. 코드 임베딩 — CodeBERT, UniXcoder
4. 멀티모달 임베딩 — CLIP, ImageBind, SigLIP
5. 희소 임베딩 (Sparse Embedding) — BM25, SPLADE, TF-IDF
6. 하이브리드 검색 (Hybrid Search) — 밀집(Dense) + 희소(Sparse), RRF 재현율 향상
7. ANN (Approximate Nearest Neighbor) 탐색 — 정확한 kNN의 근사
8. HNSW (Hierarchical Navigable Small World) — 계층 그래프 기반 ANN
9. IVF (Inverted File Index) — 클러스터링 기반 검색
10. PQ (Product Quantization) — 벡터 압축, 메모리 효율
11. SCaNN (Scalable Nearest Neighbors) — Google ANN
12. DiskANN / Vamana — 디스크 기반 대규모 ANN
13. Vector DB — Pinecone / Weaviate / Milvus / Chroma / Qdrant / Redis Vectors
14. pgvector — PostgreSQL 벡터 확장, SQL + 벡터 혼합 쿼리
15. 청킹 전략 — 고정 크기 / 재귀 / 의미 기반 / 레이아웃 기반 (문서 구조)
16. Reranker — BGE-Reranker / Cohere Rerank / BAAI Cross-Encoder
17. ColBERT — 후기 상호작용 레이트 검색, 토큰 수준 점수
18. Sentence Transformers — 의미 유사도 학습, bi-encoder
19. 지식 그래프 + 임베딩 — TransE, TransR, RotatE
20. 멀티벡터 표현 — 문서를 복수 벡터로, 상세 표현 향상

---

## 6. MLOps / LLMOps 완전판 — 36개

### ML 파이프라인
1. MLOps 개념 — ML 수명주기 자동화 (데이터→훈련→평가→배포→모니터링)
2. ML 파이프라인 도구 — Kubeflow / Airflow / Metaflow / Prefect / ZenML
3. Feature Store — Feast / Tecton / Hopsworks — 특성 재사용, 온/오프라인 일관성
4. 데이터 버전 관리 — DVC / Delta Lake / LakeFS / git-lfs
5. 실험 추적 — MLflow / Weights & Biases / Neptune / ClearML / Comet ML
6. 모델 레지스트리 — MLflow Registry / AWS SageMaker Registry / Vertex AI
7. 모델 서빙 아키텍처 — 온라인 vs 배치 vs 스트리밍 서빙
8. 모델 서빙 도구 — TorchServe / TF Serving / BentoML / Seldon / KServe
9. LLM 추론 서버 — vLLM / SGLang / TGI (HuggingFace) / Ollama / LMStudio
10. Triton Inference Server — NVIDIA, 다중 프레임워크 지원
11. 배포 전략 — 블루/그린 / 카나리 / 섀도우 / A/B 테스트
12. CT (Continuous Training) — 자동 재훈련 트리거, 데이터 드리프트 감지

### 모니터링 / 드리프트
13. 데이터 드리프트 (Data Drift) — 입력 분포 변화, KS 검정, PSI
14. 개념 드리프트 (Concept Drift) — 레이블-입력 관계 변화, 모델 성능 저하
15. 모델 모니터링 도구 — Evidently AI / Arize AI / WhyLabs / Fiddler AI
16. 예측 모니터링 — 정확도, 레이턴시, 에러율, 공정성 지표
17. ML 가관측성 — 로그·메트릭·추적·프로파일링 통합

### LLM 특화 운영
18. LLMOps 개요 — LLM 수명주기 (사전훈련→파인튜닝→배포→모니터링)
19. 프롬프트 버전 관리 — LangSmith / PromptLayer / Humanloop
20. LLM 평가 자동화 — G-Eval / MT-Bench / RAGAS / DeepEval
21. RAGAS — RAG 파이프라인 평가 (Faithfulness/Context Precision/Recall)
22. LLM 가드레일 — NeMo Guardrails / LlamaGuard / Guardrails AI
23. 할루시네이션 탐지 — 사실 검증, SelfCheckGPT, FACTSCORE
24. 프롬프트 캐싱 (Prompt Caching) — Claude/GPT API 비용 절감
25. 배치 API (Batch API) — 비실시간 LLM 처리 비용 절감
26. 토큰 최적화 — 입력 압축, 대화 요약, Context Distillation

### 모델 최적화
27. 지식 증류 (Knowledge Distillation) — Teacher-Student, 소형화
28. 모델 가지치기 (Pruning) — 비구조적/구조적 가지치기
29. 양자화 (Quantization) — INT8 / INT4 / FP8 / GPTQ / AWQ / GGUF (llama.cpp)
30. KV Cache 최적화 — PagedAttention (vLLM), Sliding Window, Prefix Caching
31. 연속 배치 (Continuous Batching) — 동적 배치 크기, GPU 활용률 최대화
32. Tensor Parallelism — 단일 층을 여러 GPU 분산
33. 엣지 ML — TFLite / ONNX Runtime / CoreML / OpenVINO / QNN (Qualcomm)
34. 온디바이스 추론 — 스마트폰 NPU, Apple Neural Engine

### 프라이버시 / 보안
35. 차등 프라이버시 (Differential Privacy) — 학습 데이터 보호, DP-SGD
36. 동형 암호화 (Homomorphic Encryption) — 암호화된 상태로 추론

---

## 7. 멀티모달 AI — 22개

1. 멀티모달 AI 개요 — 텍스트+이미지+오디오+비디오+센서 통합
2. 멀티모달 LLM — GPT-4o / Claude 3.7 / Gemini 2.0 / LLaVA / Qwen-VL
3. CLIP (Contrastive Language-Image Pre-training) — 이미지-텍스트 대조 학습
4. SigLIP — CLIP 개선, Sigmoid Loss, 더 나은 제로샷
5. ALIGN — Google, 대규모 이미지-텍스트 정렬
6. Flamingo — DeepMind, 시각 언어 모델, Few-shot
7. Text-to-Image — DALL-E 3 / Stable Diffusion 3.5 / Midjourney v7 / Ideogram
8. Stable Diffusion 아키텍처 — Latent Diffusion, UNet, VAE, CLIP 텍스트 인코더
9. ControlNet — 조건부 이미지 생성 (스케치/포즈/뎁스 제어)
10. LoRA for Diffusion — 이미지 스타일 파인튜닝
11. Text-to-Video — Sora / Runway Gen-3 / Kling / CogVideoX / Step-Video
12. Video Understanding — VideoBERT, Video-LLaVA, Temporal Reasoning
13. Text-to-Audio — AudioLDM2, MusicGen, Stable Audio
14. Text-to-Speech (TTS) — VITS / Voicebox / XTTS / ElevenLabs / Kokoro
15. Speech-to-Text (STT) / ASR — Whisper v3 / Conformer / Wav2Vec 2.0
16. 3D 생성 — NeRF / 3D Gaussian Splatting / Zero123 / Shap-E
17. Text-to-3D — DreamFusion, Magic3D, LDM3D
18. 감정 인식 (Emotion AI) — 표정/음성/생체 신호 멀티모달
19. Document AI — LayoutLM / Donut / PaddleOCR — 문서 구조 이해
20. Image-to-Code — GPT-4V / screenshot-to-code
21. Any-to-Any 모델 — AnyGPT, UnifiedIO 2 — 모달 간 자유 변환
22. 멀티모달 임베딩 공간 — 통일된 표현 공간 학습

---

## 8. AI 인프라 / 하드웨어 심화 — 24개

### GPU / AI 칩
1. NVIDIA GPU 로드맵 — A100 → H100 → H200 → B100 → B200 → GB200 NVL72
2. CUDA 프로그래밍 모델 — Grid/Block/Thread, Warp (32 스레드), SIMT
3. CUDA 최적화 — Shared Memory, Warp Divergence, Memory Coalescing
4. TPU (Tensor Processing Unit) — Google v5e/v5p, 행렬 연산 특화
5. NPU (Neural Processing Unit) — Apple Neural Engine / Qualcomm NPU / MediaTek APU
6. AI ASIC — AWS Trainium (훈련) + Inferentia (추론) / Cerebras WSE / Groq LPU
7. Groq LPU — 초고속 추론, SRAM 기반, 500+ tok/s
8. Cerebras Wafer-Scale Engine (WSE) — 최대 단일 칩, 40GB SRAM
9. DPU (Data Processing Unit) — NVIDIA BlueField, 네트워크·스토리지 오프로드
10. FPGA AI — Intel Agilex / AMD Xilinx Alveo — 유연한 추론 가속

### 메모리 / 상호연결
11. HBM (High Bandwidth Memory) — HBM2e / HBM3 / HBM3e (B200: 192GB 8TB/s)
12. NVLink 4/5 — GPU-GPU 900GB/s, NVSwitch 통한 올투올
13. CXL (Compute Express Link) — CPU-GPU-메모리 통합 메모리 공간
14. InfiniBand NDR (400Gb/s) / XDR (800Gb/s) — 클러스터 통신
15. RoCE v2 (RDMA over Converged Ethernet) — 이더넷 기반 저지연

### 분산 학습
16. Data Parallelism — DDP (Distributed Data Parallel), AllReduce
17. Model Parallelism — Tensor/Pipeline/Expert Parallelism
18. ZeRO (Zero Redundancy Optimizer) — Stage 1/2/3, DeepSpeed
19. 3D Parallelism — Data + Tensor + Pipeline 조합, Megatron-LM
20. FSDP (Fully Sharded Data Parallel) — PyTorch, ZeRO-3 유사
21. GLOO / NCCL / MPI — 집합 통신 라이브러리

### AI 전용 최적화
22. FlashAttention 1/2/3 — IO-Aware Self-Attention, HBM-SRAM 계층 활용
23. Paged Attention (vLLM) — KV Cache 메모리 단편화 해결
24. Speculative Decoding — 드래프트 모델 + 검증, 2~4배 가속

---

## 9. AI 응용 산업 심화 — 26개

1. 컴퓨터 비전 응용 — 분류/탐지/분할/OCR/포즈/광학 흐름
2. NLP 응용 — 감성분석/NER/번역/요약/QA/대화시스템
3. 코드 AI — GitHub Copilot / Cursor / Claude Code / Devin / SWE-agent
4. 과학 AI — AlphaFold 3 / AlphaGeometry 2 / AI Scientist (자율 논문 작성)
5. 의료 AI — 영상 진단 AI-CAD / 신약 발굴 / 임상 예측 / Med-PaLM 2
6. 금융 AI — 이상거래탐지(FDS) / AML / 알고트레이딩 / 신용평가 / 로보어드바이저
7. 법률 AI — Harvey / EvenUp / 계약서 분석 / 판례 검색 / 규정 컴플라이언스
8. 교육 AI — 지능형 튜터(ITS) / 개인화 학습 / 자동 채점 / Khanmigo
9. 자율주행 AI — ADAS L1~L5 / BEV(Bird-Eye View) / Occupancy Network / DriveVLM
10. 로봇 AI — 모방 학습(IL) / RT-2 / π0 / MRG Model / 촉각 센서 융합
11. 드론 AI — 자율 비행 / 영상 분석 / 군집 비행 (Swarm)
12. 스마트 제조 AI — 예지 정비(PdM) / 시각 품질검사 / 에너지 최적화
13. 물류 AI — 수요 예측 / 경로 최적화 / AMR / 창고 자동화
14. 농업 AI (AgriAI) — 정밀 농업 / 수확량 예측 / 병해충 탐지
15. 에너지 AI — 전력 수요 예측 / 재생에너지 예측 / 그리드 최적화
16. 사이버보안 AI — 이상 탐지 / 위협 헌팅 / 취약점 분석 / LLM 보안 분석
17. 추천 시스템 — CF / CB / Two-Tower / Sequential Rec / LLM 기반 추천
18. 검색 AI — Neural IR / Dense Retrieval / Re-ranking / AI Overviews (Google)
19. 건축/도시 AI — 생성적 설계 / 에너지 시뮬레이션 / 스마트시티
20. 마케팅 AI — 초개인화 / 광고 최적화 / 고객 여정 예측
21. HR AI — 이력서 스크리닝 / 면접 AI / 적성 예측 / 조직 분석
22. 고객서비스 AI — LLM 챗봇 / 감성 분석 / 에스컬레이션 자동화
23. 미디어 AI — Text-to-Video / AI 더빙 / 영상 편집 자동화
24. 양자+AI 융합 — Quantum ML, QNN, 변분 양자 회로 (VQC)
25. 뇌과학+AI — BCI (뇌-컴퓨터 인터페이스), 계산 신경과학
26. 디지털 트윈 + AI — NVIDIA Omniverse / 실시간 물리 시뮬레이션

---

## 10. AI 거버넌스 / 윤리 / 안전 — 26개

1. AI 윤리 4원칙 — 자율성(Autonomy) / 유익(Beneficence) / 무해(Non-maleficence) / 정의(Justice)
2. 공정성 (Fairness) — 개인 공정성 vs 그룹 공정성, 불가능 정리 (Impossibility Theorem)
3. AI 편향(Bias) 유형 — 데이터 편향 / 알고리즘 편향 / 배포 편향 / 피드백 루프
4. 알고리즘 공정성 지표 — Demographic Parity / Equalized Odds / Calibration
5. 설명 가능 AI (XAI) — LIME / SHAP / Integrated Gradients / Attention Visualization
6. 반사실 설명 (Counterfactual) — "If X changed, outcome would be Y"
7. TCAV (Testing with CAV) — 개념 수준 해석
8. AI 정렬 (AI Alignment) — Corrigibility / Amplification / Debate / RLHF
9. AI 안전성 (AI Safety) — 목표 오지정, 보상 해킹, 권한 탐색 방지
10. 감독 신호 (Oversight) — HITL / HILF (Loop-From) / Scalable Oversight
11. 할루시네이션 (Hallucination) — 사실성 오류, 신뢰도 보정 (Calibration)
12. 그라운딩 문제 (Grounding Problem) — 언어 의미와 현실 연결 부재
13. EU AI Act (2024) — 위험 등급 4단계 (Unacceptable/High/Limited/Minimal)
14. AI Act 고위험 AI — 의료 진단, 신용평가, 채용, 사법, 인프라 등
15. NIST AI RMF 2.0 — Govern / Map / Measure / Manage 4개 함수
16. OECD AI 원칙 — 42개국 채택, 5가지 원칙
17. G7 AI 행동 강령 (Hiroshima AI Process)
18. AI 워터마킹 — C2PA / SynthID (Google) — 합성 콘텐츠 식별
19. 딥페이크 탐지 — Deepfake Detection Challenge (DFDC), FaceForensics++
20. 저작권과 AI — 학습 데이터 저작권 소송 (NYT v OpenAI), 생성물 귀속
21. 소버린 AI (Sovereign AI) — 국가 주도 AI 인프라 / 데이터 주권
22. AI 탄소 발자국 — GPT-3 훈련 CO₂ ≈ 500t, Green AI 접근법
23. AI TRiSM (Gartner) — AI Trust / Risk / Security Management
24. Responsible AI 체계 — Microsoft / Google / IBM 내부 원칙
25. AI 거버넌스 구조 — AI 위원회 / Chief AI Officer / AI 윤리 팀
26. 디지털 출처 (Digital Provenance) — C2PA 프레임워크, 콘텐츠 이력 관리

---

## 11. 최신 AI 동향 (2025~2026) — 24개

1. OpenAI o1/o3/o4 — Extended Thinking, System 2 추론, 수학·코드 특화
2. DeepSeek-R1/V3 — 강화학습 추론, 오픈소스, 저비용으로 GPT-4 수준
3. Gemini 2.0/2.5 — 실시간 멀티모달, 2M 컨텍스트, Deep Research
4. Claude 3.7 Sonnet — 하이브리드 추론 모드, 확장 사고
5. LLaMA 4 — Meta 최신 오픈소스, Mixture of Experts, 멀티모달
6. Reasoning Model 시대 — System 2 사고, Chain-of-Thought 내재화
7. Agentic AI 주류화 — 단순 챗봇 → 자율 업무 시스템
8. MCP (Model Context Protocol) 생태계 확장 — 수백 개 MCP 서버
9. A2A (Agent-to-Agent) Protocol — Google, 에이전트 간 통신 표준화
10. Compound AI System — 단일 모델 → 다중 모델·도구·DB 복합체
11. Vibe Coding / AI-first 개발 — Claude Code / Cursor / Windsurf
12. On-device AI / Edge LLM — Phi-4-mini / Gemma 3 2B / Qwen2.5-0.5B
13. Small Language Model (SLM) — 1~7B 파라미터, 특화 태스크
14. Long Context Utilization — "Lost in the Middle" 문제, 위치 편향
15. Multimodal Reasoning — 이미지·코드·수학 통합 추론
16. AI Native Software — AI가 코드 생성·리팩토링·테스트 주도하는 개발
17. Data Flywheel — 사용자 피드백 → 자동 개선 선순환
18. AI Superagent — 복잡한 장기 과제를 자율 수행하는 범용 에이전트
19. Physical AI — NVIDIA Cosmos / Boston Dynamics Spot AI / 체화 인지
20. World Model — 환경 예측 모델, 시뮬레이션 기반 계획
21. 모델 효율화 — Mixture of Depths / Mixture of Experts 최적화
22. AI Chip Wars — NVIDIA B200 / AMD MI325X / Intel Gaudi 3 / Google TPU v5p
23. Post-Training Scaling — 추론 시 컴퓨팅 확장 (o1 패러다임)
24. AI Regulation 2025 — EU AI Act 시행, 한국 AI 기본법, 글로벌 규제 경쟁

---

**총 키워드 수: 361개**
