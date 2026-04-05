+++
weight = 93
title = "93. 추천 시스템 (Recommendation System)"
description = "추천 시스템의 개념, 협업 필터링, 콘텐츠 기반 필터링, 딥러닝 기반 추천, 실전 적용 사례"
date = "2026-04-05"
[taxonomies]
tags = ["추천시스템", "Recommendation", "협업필터링", "콘텐츠기반", "딥러닝", "매트릭스분해", "개인화"]
categories = ["studynote-bigdata"]
+++

# 추천 시스템 (Recommendation System)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 추천 시스템은 사용자의 과거 행동, 선호도,商品의 특성을 분석하여 사용자가 관심을 가질 것으로 예측되는 商品을 제안하는 시스템이다.
> 2. **가치**: Amazon, Netflix, YouTube, Spotify 등 주요 플랫폼의 핵심 사업 인프라로, 매출과 사용자 만족도를 크게 좌우하는 핵심 요소이다.
> 3. **융합**: 협업 필터링(Collaborative Filtering), 콘텐츠 기반 필터링(Content-Based Filtering), 하이브리드 방식, 그리고 최근에는 딥러닝과 inúmer러닝을 활용한 고급 추천 알고리즘이 활용되고 있다.

---

### Ⅰ. 개요 및 필요성 (Context & Necessity)

추천 시스템(Recommendation System)은"信息 超负荷(Information Overload)"문제에 대한解决方案으로 등장했다. 인터넷에서利用 가능한 정보의 양이爆炸的に增加함에 따라, 사용자가 自己에게 적합한 정보를 찾는 것이 점점 어려워졌다.

대표적인 사례를 살펴보면, Netflix는 영화/드라마 추천을 통해 사용자당 약 75%의 시청時間が추천 콘텐츠에서 왔다고 보고했으며, Amazon은 매출의 약 35%가 추천 시스템을 통해 발생한다고 밝혔다. Spotify, YouTube, TikTok 등도 마찬가지로 추천 시스템이 핵심 사업 축이다.

```text
[추천 시스템의 문제 정의]

古典적 접근법:
  - 사용자가 능동적으로 검색
  - 원하는 결과를 얻기까지 多段階의 필터링 필요

추천 시스템 접근법:
  - 시스템이 사용자의 취향을 분석하여 능동적으로 제안
  - 사용자는"받아들이는" 역할
  - 발견의 새로운 가능성 확대

[추천 시스템의 세 가지 주요 접근법]

1. 협업 필터링 (Collaborative Filtering)
   "비슷한 사용자들이 좋아하는 것을 추천"
   - 사용자 A와 B가 비슷한 시청 패턴 → A가 본 영화를 B에게 추천

2. 콘텐츠 기반 필터링 (Content-Based Filtering)
   "내가 좋아했던 것과 비슷한 것을 추천"
   - 사용자가 아메리카노를 좋아함 → 다른 커피 음료를 추천

3. 하이브리드 (Hybrid)
   - 위 두 방법을 결합
   - 더 robust한 추천 가능
```

> 📢 **섹션 요약 비유**: 추천 시스템은犹如知的な书店員と類似している. 이 직원은顧客의 과거 구매내역(협업 필터링)과 현재 관심사(콘텐츠 기반)를 파악하여,顧客가 아직 모르는하지만 아마 좋아할 새로운 도서를 입때推荐한다. 이 과정에서 쌓인 경험(데이터)을 바탕으로 추천의 정확성을 계속 향상시킨다.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 2.1 협업 필터링 (Collaborative Filtering)

협업 필터링은"비슷한 취향의 사용자들은 비슷한 아이템을 선호한다"는 가정에 기반한다.

```text
[협업 필터링: 사용자-아이템 행렬]

사용자-아이템 평점 행렬:

            │_ITEM1 │_ITEM2 │_ITEM3 │_ITEM4
────────────┼───────┼───────┼───────┼───────
  사용자_A  │   5   │   3   │  ?    │   4
  사용자_B  │   4   │   ?   │   2   │   5
  사용자_C  │   ?   │   4   │   5   │   ?
  사용자_D  │   2   │   5   │   ?   │   3

Task: 사용자_A에게 ITEM3를 추천

분석:
  - 사용자_A와 가장 비슷한 사용자 찾기
  - 사용자_B: (-, 2, 5) → ITEM3=2
  - 사용자_C: (4, 5, -) → ITEM3=5
  → 사용자_A와 C의 유사도가 높음 → ITEM3에 대해 C는 5점 부여
  → 사용자_A에게 ITEM3 추천
```

**사용자 기반 협업 필터링**: 비슷한 취향의 다른 사용자들이 높은 평가를 준 아이템을 추천

**아이템 기반 협업 필터링**: 사용자가 previously高度 평가한 아이템과 유사한 아이템을 추천

### 2.2 행렬 분해 (Matrix Factorization)

대규모 실전 시스템에서는 희소성(Sparsity) 문제가严重하다. 사용자-아이템 행렬은 대부분의 값이 unknown이다 (사용자가 모든 아이템을 평가하지 않기 때문에).

행렬 분해는 이 희소한 행렬을 두 개의 저차원 행렬로 분해한다.

```python
# 행렬 분해의 원리

# 원래 희소 행렬 R (사용자 × 아이템)
# R ≈ U × Vᵀ

# U: 사용자-잠재요인 행렬 (m × k)
# Vᵀ: 아이템-잠재요인 행렬 (k × n)
# k: 잠재 요인의 수 (축소 차원)

# 예시
# R[사용자_i, 아이템_j] ≈ Σ_k U[i,k] × V[j,k]

# 이를 통해:
# - unknown 평점도 예측 가능
# - 차원 축소로 인한 노이즈 감소
# - 잠재 요인을 통해 아이템의 의미 파악 가능 (커피, 액션, 로맨스 등)
```

```text
[행렬 분해 시각화]

R (희소 행렬)          ≈         U (사용자 요인)         ×        Vᵀ (아이템 요인)
┌────────────────┐              ┌─────────┐                ┌─────────┐
│ 5  3  ?  4    │              │ 0.8 0.3 │  (사용자_A)      │ 0.9 0.1 │ 아이템_1
│ 4  ?  2  5    │     ≈        │ 0.7 0.5 │  (사용자_B)  ×   │ 0.2 0.8 │ 아이템_2
│ ?  4  5  ?    │              │ 0.6 0.4 │  (사용자_C)      │ 0.1 0.9 │ 아이템_3
│ 2  5  ?  3    │              │ 0.3 0.7 │  (사용자_D)      │ 0.8 0.2 │ 아이템_4
└────────────────┘              └─────────┘                └─────────┘
                                 잠재 요인_1                  잠재 요인_2
                               (예: 액션/코미디)          (예: 인기/평점)
```

### 2.3 콘텐츠 기반 필터링

아이템의 특성(Content)을 기반으로 추천한다.

```text
[콘텐츠 기반 필터링]

영화 추천 예시:

사용자_A가 highly 평가한 영화들:
  - "어벤져스": 액션(높음), SF(높음), 코미디(낮음)
  - "인생은 아름다워": 드라마(높음), 로맨스(높음), 코미디(중간)

→ 사용자_A의 취향 프로파일 생성:
  액션: 높음, SF: 높음, 드라마: 중간, 로맨스: 중간

새 영화 "배트맨":
  - 액션(높음), SF(높음), 드라마(낮음)

→ 사용자_A 취향과의 유사도 계산 → 높음 → 추천
```

### 2.4 딥러닝 기반 추천

최근에는 딥러닝을 활용한 추천 시스템이 주목받고 있다.

**Neural Collaborative Filtering (NCF)**
- 행렬 분해를 신경망으로 모델링
- 사용자-아이템 상호작용을 MLP로 학습

**Wide & Deep**
- Wide: 기억(Memorization) - 직접적인 특성 조합 학습
- Deep: 일반화(Generalization) - 저차원 임베딩을 통한 일반화

```python
# 딥러닝 추천 모델의 기본 구조 (PyTorch 예시)
class NeuMF(nn.Module):
    def __init__(self, num_users, num_items, embed_dim, hidden_dims):
        super().__init__()
        # GMF (Generalized Matrix Factorization)
        self.user_embed_gmf = nn.Embedding(num_users, embed_dim)
        self.item_embed_gmf = nn.Embedding(num_items, embed_dim)

        # MLP
        self.user_embed_mlp = nn.Embedding(num_users, embed_dim)
        self.item_embed_mlp = nn.Embedding(num_items, embed_dim)

        # MLP layers
        mlp_layers = []
        input_dim = embed_dim * 2
        for hidden_dim in hidden_dims:
            mlp_layers.append(nn.Linear(input_dim, hidden_dim))
            mlp_layers.append(nn.ReLU())
            input_dim = hidden_dim
        self.mlp = nn.Sequential(*mlp_layers)

        # Final prediction
        self.fc = nn.Linear(embed_dim + hidden_dims[-1], 1)

    def forward(self, user_id, item_id):
        # GMF part
        user_gmf = self.user_embed_gmf(user_id)
        item_gmf = self.item_embed_gmf(item_id)
        gmf_out = user_gmf * item_gmf

        # MLP part
        user_mlp = self.user_embed_mlp(user_id)
        item_mlp = self.item_embed_mlp(item_id)
        mlp_input = torch.cat([user_mlp, item_mlp], dim=-1)
        mlp_out = self.mlp(mlp_input)

        # Combine
        output = self.fc(torch.cat([gmf_out, mlp_out], dim=-1))
        return output.sigmoid()
```

> 📢 **섹션 요약 비유**: 추천 시스템의 발전은犹如料理의 개인화 과정을 닮았다. 처음에는大家가同じ menu를 먹었지만(대량 제공), 점차 개인의 취향에 맞게Recipes를 조정하게 되었다(콘텐츠 기반). 이제는 비슷한 취향의 다른사람들食譜를参考하여(협업 필터링), 신경망이 이를综合하여 개인 맞춤형 메뉴를 제안한다(딥러닝 기반). 점점 더 개인화된 추천이 가능해지고 있다.

---

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

추천 시스템의 주요 접근법을 비교해보자.

| 접근법 | 장점 | 단점 | 적합한 상황 |
|:---|:---|:---|:---|
| **협업 필터링** | 도메인 지식 불필요, 새로운 아이템 추천 가능 | Cold-start 문제, 희소성 | 기존 사용자/아이템 |
| **콘텐츠 기반** | Cold-start 문제 해결 가능, 해석 용이 | 과적합 위험, 다양성 부족 | 아이템 특성 명확할 때 |
| **하이브리드** | 각각의 단점 보완 | 구현 복잡 | 대부분의 실전 |
| **딥러닝 기반** | 복잡한 패턴 학습, End-to-End 학습 | 데이터 많이 필요, 블랙박스 | 대규모 데이터 |

```text
[Cold-Start 문제]

새로운 사용자가 시스템에 처음 방문:
  → 과거 행동 데이터 없음 → 협업 필터링 적용 불가
  → 해결: 인구통계학적 정보 활용, 초기 설문, 콘텐츠 기반 추천

새로운 아이템이 등록될 때:
  → 아무도 평가하지 않음 → 협업 필터링 불가
  → 해결: 아이템 콘텐츠 정보 활용, 전문가 평가

[다양성 vs 정확성 트레이드오프]

정확도만追求:
  → 항상"가장 잘当たる" 것만 추천
  → 사용자가 지루해짐 (필터 버블)

다양성추천:
  → 때로는"덜 정확한" 것도 추천
  → 새로운 발견의 기회 제공
  → 장기적 사용자 만족도 향상
```

> 📢 **섹션 요약 비유**: 추천 시스템의Challenger은犹如생활経費の節約と類似한 트레이드오프가 있다. 정확도만追求하면 같은 식당만 추천받아質素な生活가 되고(필터 버블), 다양성을추가하면時々とんでもない 곳에 가게 될 수 있다(정확도 저하). 이 균형을 맞추는 것이 추천 시스템 운영의 핵심이다.

---

### Ⅳ. 실무 적용 및 한계 (Application & Limitation)

**주요 적용 사례:**

1. **전자상거래 (Amazon)**
   -"함께 구매한 아이템", "이 상품을 본 고객이 함께 본 상품"
   - 개인화된 首页 추천

2. **OTT/영상 (Netflix, YouTube)**
   - 시청 기록 기반 콘텐츠 추천
   -"계속 Watching", "For You" 섹션

3. **음악 스트리밍 (Spotify)**
   -playlist 자동 생성 (Discover Weekly)
   -"Fans also play" 추천

4. **소셜 미디어 (Instagram, TikTok)**
   - 탐색 탭 콘텐츠 추천
   - 팔로우 기반 추천

**한계점:**

1. **Cold-Start**: 새로운 사용자/아이템에 대한 데이터 부족

2. **희소성**: 대다수의 사용자-아이템 조합이 미평가

3. **필터 버블**: 과도하게 개인화되어 선택지가 좁아짐

4. **명시적 피드백 의존**: 사용자가 직접 평점을 매기는 것 선호하지 않음

5. ** privacidad**: 개인 취향 데이터 수집의 privacy 우려

```python
# Surprise 라이브러리를 활용한 간단한 추천 시스템
from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import cross_validate

# 데이터 로드
data = Dataset.load_builtin('ml-100k')

# 협업 필터링 모델 (사용자 기반 KNN)
algo = KNNBasic(sim_options={'name': 'cosine', 'user_based': True})

# 교차 검증
results = cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5)
print(f"Average RMSE: {results['test_rmse'].mean():.4f}")
```

> 📢 **섹션 요약 비유**: 추천 시스템은犹如건강식食谱과 같다. 영양 균형(정확도)은 중요하지만, 때로는自己想하지 않은 健康食(새로운 추천)을 통해意外的得を收获할 수 있다. 그러나 추천이 너무 MEP(个人화)되면 식 inúmer릭 monotony에 빠지고, 새로운食材를 만날 기회가 없어진다. 이처럼 추천 시스템도 다양성과 정확성의 균형이 필요하다.

---

### Ⅴ. 요약 및 전망 (Summary & Outlook)

추천 시스템은 현대 디지털 플랫폼의核心 인프라로서, 사용자 경험과 비즈니스 성과에 直接적 영향을 미친다. 협업 필터링, 콘텐츠 기반 필터링, 하이브리드 접근법에서부터 딥러닝 기반 고급 모델에 이르기까지 빠르게 발전하고 있다.

앞으로는大型言語모델(LLM)과 추천 시스템의 결합, 실생활Assistant로서의 추천,그리고个人 뿐 아니라 사회적으로 beneficial한 추천(편향 감소, 다양성 증대)등의研究方向가 유망하다.

결론적으로, 추천 시스템은"在人에게 적합한 정보를 찾는"という根本적 필요から発生했으며, 技术의 발전과 함께 그重要性만 증가하고 있다.

---

**References**
- Ricci, F., et al. (2015). Recommender Systems Handbook (2nd ed.). Springer.
- He, X., et al. (2017). Neural Collaborative Filtering. WWW.
- Cheng, H. T., et al. (2016). Wide & Deep Learning for Recommender Systems. ACM RecSys.
- Koren, Y., et al. (2009). Matrix Factorization Techniques for Recommender Systems. IEEE Computer.
