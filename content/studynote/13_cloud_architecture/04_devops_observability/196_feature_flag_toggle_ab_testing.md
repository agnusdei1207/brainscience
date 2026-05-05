+++
weight = 196
title = "196. 피처 플래그 / 피처 토글 (Feature Flag / Toggle)"
date = "2026-04-21"
[extra]
categories = "studynote-cloud-architecture"
+++

## 0. 핵심 인사이트

> **핵심**: 코드 재배포 없이 런타임에 특정 기능을 ON/OFF하거나 특정 사용자 그룹에게만 노출하는 소프트웨어 조건 스위치다.
> **비유**: 피처 플래그는 새 조명을 집에 설치해두고 전기 연결만 잠깐 끊어두는 것과 같다. 조명은 이미 설치됐지만 스위치만 ON/OFF하면 언제든지 켤 수 있다. 공사(배포)와 개통(출시)이 완전히 분리된다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

피처 플래그(Feature Flag), 또는 피처 토글(Feature Toggle)은 소프트웨어 개발에서 새 기능을 코드에 포함하되 런타임 조건에 따라 활성/비활성화하는 기술이다. Martin Fowler의 블로그 포스트 "Feature Toggles (aka Feature Flags)"에서 체계적으로 정리된 개념이다.

가장 중요한 개념은 **배포와 출시의 분리(Decouple Deployment from Release)**이다. 전통적으로는 "코드 배포 = 기능 출시"였지만, 피처 플래그를 사용하면 신기능 코드를 미리 프로덕션에 배포해두고 마케팅·비즈니스 일정에 맞춰 플래그를 ON으로 전환하여 출시할 수 있다.

Facebook, Google, Netflix 등은 수천 개의 피처 플래그를 동시에 운영하며, 일부 회사는 A/B 테스트·퍼스널라이제이션·점진적 출시 모두를 피처 플래그 시스템 위에서 구현한다. LaunchDarkly, Unleash, Flagsmith, AWS AppConfig 등이 대표적인 피처 플래그 관리 플랫폼이다.

---

## 2. 구성요소

### 피처 플래그 유형 분류

| 유형 | 수명 | 사용 목적 |
|:---|:---:|:---|
| Release Toggle | 단기 (수 일~수 주) | 미완성 기능 숨기기, Trunk-based 개발 |
| Experiment Toggle | 중기 (수 주~수 달) | A/B 테스트, 통계적 검증 |
| Ops Toggle | 단기~장기 | 운영 비상 스위치, 기능 긴급 비활성화 |
| Permission Toggle | 장기 | 사용자 등급별 기능 차등 제공 (Premium) |

### 피처 플래그 동작 구조

```
  ┌─────────────────────────────────────────────────────┐
  │              Feature Flag 관리 서버                   │
  │  (LaunchDarkly / Unleash / AWS AppConfig)            │
  │                                                      │
  │  플래그 정의: new_checkout_flow                       │
  │    - 기본값: OFF                                     │
  │    - 대상: user_segment = "beta_users"               │
  │    - 가중치: 10% 랜덤 사용자                          │
  └──────────────────────┬──────────────────────────────┘
                         │ SDK 폴링 or 웹훅
                         ▼
  ┌──────────────────────────────────────────────────────┐
  │                 애플리케이션 코드                       │
  │                                                      │
  │  if (featureFlag.isEnabled("new_checkout_flow",      │
  │                             currentUser)) {          │
  │      showNewCheckout();   // 신기능                  │
  │  } else {                                            │
  │      showOldCheckout();   // 기존 기능               │
  │  }                                                   │
  └──────────────────────────────────────────────────────┘
```

### LaunchDarkly SDK 예시 (Java)

```java
LDClient client = new LDClient("sdk-key");
LDContext context = LDContext.builder("user-123")
    .set("plan", "premium")
    .build();

boolean showNewUI = client.boolVariation("new-checkout-ui", context, false);

if (showNewUI) {
    renderNewCheckout();
} else {
    renderLegacyCheckout();
}
```

---

## 3. 구조 및 원리

**핵심 조건**: 변경 자동화와 운영 안정성은 별개가 아니라 하나의 루프이며, 빌드·검증·배포·관측·피드백이 끊기지 않아야 지속 개선이 가능하다.

동작 순서:
1. 변경 사항을 버전 관리 시스템에서 감지한다.
2. 빌드·테스트·보안 검증으로 변경의 품질을 빠르게 확인한다.
3. 승인된 산출물을 선언형 배포나 자동화 파이프라인으로 운영 환경에 반영한다.
4. 메트릭·로그·트레이스를 통해 실제 동작 결과를 관측한다.
5. 피드백을 다음 개선 주기에 연결해 반복적으로 신뢰성을 높인다.

### 피처 플래그 vs 카나리 배포 vs A/B 테스트

| 기준 | Feature Flag | Canary Release | A/B Test |
|:---|:---|:---|:---|
| 제어 단위 | 기능(Feature) | 서버 버전 | UI 변형 |
| 변경 방법 | 런타임 스위치 | 배포 | 런타임 스위치 |
| 통계 검증 | 선택적 | 아님 | 필수 |
| 즉시 롤백 | ✅ (플래그 OFF) | 빠름 | ✅ |
| 코드 재배포 | ❌ 불필요 | ✅ 필요 | ❌ 불필요 |

### 피처 플래그 기술 부채 관리

```
피처 플래그 생성 규칙:
  ✅ 플래그명: JIRA 티켓 ID 포함 (ex: PROJ-123-new-checkout)
  ✅ 만료일: 생성 시 설정 (ex: 2026-07-01)
  ✅ 담당자: 팀 / 개인 명시
  ✅ 용도: Release / Experiment / Ops / Permission
  
플래그 제거 시점:
  - 전체 사용자 100% 적용 후 2주 이내 코드에서 제거
  - 분기별 Stale Flag 감사 수행
```

---

## 4. 비교 및 연결

**Trunk-based Development(TBD)와의 연계**:
- 기능 브랜치 없이 모든 개발자가 main/trunk에 직접 커밋
- 미완성 기능은 피처 플래그로 숨겨서 CI/CD 파이프라인 유지
- 장기 브랜치(feature branch)의 merge conflict 문제 해결

**킬 스위치(Kill Switch) 활용**:
```
프로덕션 장애 시:
  1. 원인: 새 기능 v2 결제 로직 버그
  2. 배포 롤백 없이 즉시: feature_flag["new_payment_v2"] = OFF
  3. 결과: 1분 내 장애 격리, 구 결제 로직 즉시 복원
  4. 이후: 수정 후 다음 배포 시 플래그 재활성화
```

**기술사 판단 포인트**:
- 피처 플래그는 Ops Toggle로 "비상 차단 스위치" 역할을 하여 배포 없는 긴급 장애 대응에 핵심적이다.
- 플래그 규칙이 복잡해지면 "피처 플래그 지옥(Flag Hell)"이 발생하므로, 단순하게 유지하고 주기적으로 정리해야 한다.
- Permission Toggle은 SaaS 제품의 Freemium/Premium 기능 분리에서 비즈니스 핵심 인프라가 된다.

---

## 5. 실무 적용 및 판단

| 기대효과 | 설명 |
|:---|:---|
| 배포·출시 분리 | 기술 일정과 비즈니스 일정의 독립적 관리 |
| 즉각적 롤백 | 재배포 없이 플래그 OFF로 기능 비활성화 |
| 안전한 점진 출시 | 내부 → 베타 → 전체 단계적 기능 노출 |
| A/B 테스트 통합 | 기능 효과를 데이터로 검증 |

피처 플래그는 현대 DevOps에서 "소프트웨어 출시의 리모컨"이 되었다. 적절히 관리되면 팀의 배포 자신감과 실험 문화를 혁신적으로 높이지만, 관리 없이 방치하면 기술 부채로 시스템 신뢰성을 위협한다.

---

## 6. 기대효과 및 결론

피처 플래그 / 피처 토글 (Feature Flag / Toggle)를 올바르게 적용하면 확장성, 운영 안정성, 자동화 수준, 가시성을 함께 높일 수 있다. 다만 이 효과는 기술 자체만으로 생기지 않으며, 책임 경계·표준화·보안 통제·비용 관리가 함께 설계될 때 비로소 현실화된다.

향후에는 관리형 서비스, 정책 자동화, AI 기반 운영 최적화와 결합되면서 피처 플래그 / 피처 토글 (Feature Flag / Toggle)의 중요성이 더 커질 것이다. 따라서 핵심은 특정 도구를 도입하는 것이 아니라, 업무 특성과 조직 역량에 맞는 적용 범위와 운영 모델을 설계하는 데 있다.

---

## 7. 발전 흐름도

```text
Feature Branch + 배포 = 기능 공개 (분리 불가)
    │
    ▼
Feature Flag: 코드 배포 ≠ 기능 공개 (Decouple)
    ├─► LaunchDarkly · Unleash · ConfigCat
    └─► A/B Testing · Percentage Rollout
    │
    ▼
Trunk-Based Development + Feature Flag = CD 극대화
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| Trunk-Based Development | 피처 플래그 없이는 TBD가 미완성 기능 노출 위험 |
| Canary Release | 피처 플래그와 결합하면 더 정밀한 점진 출시 구현 |
| A/B Testing | Experiment Toggle이 A/B 테스트의 인프라 구현체 |
| LaunchDarkly / Unleash | 피처 플래그 관리 플랫폼의 대표 도구 |
| 기술 부채 | 미제거 플래그가 누적되는 피처 플래그 지옥 |
| 킬 스위치 | Ops Toggle로 장애 시 즉각 기능 비활성화 |

---
