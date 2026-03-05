+++
title = "84. 칸반 (Kanban)"
date = "2026-03-05"
[extra]
categories = "studynotes-se"
+++

# 칸반 (Kanban)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 칸반(Kanban)은 데이비드 앤더슨이 2000년대 초 도요타의 JIT(Just-In-Time) 생산 시스템에서 영감을 받아 개발한 소프트웨어 개발 방법론으로, WIP(Work In Progress) 제한, 시각화, 흐름 관리를 통해 작업의 리드 타임을 단축하고 병목을 해소하는 진화적(Evolutionary) 프로세스 개선 프레임워크다.
> 2. **가치**: 칸반 적용 시 평균 리드 타임을 50-70% 단축하고, 처리량(Throughput)을 20-40% 향상시키며, 예측 가능성을 30% 이상 개선하여 고객 만족도와 팀 효율성을 동시에 극대화한다.
> 3. **융합**: 칸반은 스크럼, DevOps, SRE와 결합하여 지속적 배포 파이프라인을 최적화하고, 누적 흐름도(CFD)와 리드 타임 분산 분석을 통해 데이터 기반 프로세스 개선을 실현한다.

---

## Ⅰ. 개요 (Context & Background)

### 개념 정의
칸반(Kanban)은 일본어로 "간판(看板)"을 의미하며, **작업의 시각화**, **WIP(Work In Progress) 제한**, **흐름(Flow) 관리**를 핵심 원칙으로 하는 애자일 방법론이다. 스크럼과 달리 **이터레이션이 없고**, **역할이 정의되지 않으며**, **기존 프로세스를 존중**하면서 점진적으로 개선하는 **진화적(Evolutionary)** 접근 방식을 취한다.

### 💡 비유
칸반은 **"고속도로 톨게이트"**에 비유할 수 있다. 차량(작업)이 진입하면 톨게이트(WIP 제한)가 동시에 처리할 수 있는 대수를 제한한다. 차량이 막히면(병목) 새로운 차량의 진입을 제한하여 전체 흐름을 유지한다. 전광판(칸반 보드)으로 현재 상황을 한눈에 볼 수 있고, 통행 시간(리드 타임)을 측정하여 효율성을 개선한다.

### 등장 배경 및 발전 과정

**1. 기존 방법론의 치명적 한계점**
- 이터레이션 기반 방법론(스크럼)의 경직성
- 긴급 작업과 계획된 작업의 충돌
- 팀 간 작업 의존성으로 인한 대기 시간
- 프로세스 일괄 변경에 대한 조직 저항

**2. 혁신적 패러다임 변화**
- 1940-50년대 도요타의 JIT 생산 시스템 개발 (오노 타이이치)
- 2004년 데이비드 앤더슨의 Microsoft 프로젝트에서 최초 적용
- 2010년 "Kanban: Successful Evolutionary Change for Your Technology Business" 출판
- 2010년대 DevOps, SRE와 결합하여 지속적 배포 최적화

**3. 비즈니스적 요구사항**
- 지속적 서비스 제공 환경(운영, 유지보수)에 적합한 방법론
- 긴급 요청에 대한 유연한 대응
- 예측 가능한 서비스 수준(SLA) 달성

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### 구성 요소 상세 분석

| 구성 요소 | 상세 역할 | 내부 동작 메커니즘 | 관련 기술/도구 | 비유 |
|-----------|-----------|---------------------|----------------|------|
| **칸반 보드** | 작업 시각화 | 열(Column), 행(Swimlane), 카드 | Jira, Trello, Azure Boards | 교통 표지판 |
| **WIP 제한** | 동시 작업량 제어 | 열별 최대 카드 수 | WIP Limits 설정 | 톨게이트 대수 |
| **리드 타임** | 총 소요 시간 | 요청~완료 시간 | Cycle Time Plugin | 통행 시간 |
| **사이클 타임** | 실제 작업 시간 | 작업 시작~완료 | Analytics Tools | 운행 시간 |
| **처리량** | 단위별 완료량 | 주/월 완료 카드 수 | Throughput Report | 교통량 |
| **CFD** | 흐름 시각화 | 누적 영역 차트 | Cumulative Flow Diagram | 교통 흐름도 |

### 칸반의 6가지 핵심 실천 방법

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                     KANBAN SIX CORE PRACTICES (6가지 핵심 실천)                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  1. VISUALIZE (시각화)                                                   │   │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │   │
│  │  │                                                                   │  │   │
│  │  │    Backlog     Ready     In Progress    Review     Done          │  │   │
│  │  │    ┌─────┐   ┌─────┐    ┌─────┐      ┌─────┐    ┌─────┐         │  │   │
│  │  │    │     │   │ □□□ │    │ □□□ │      │ □□  │    │█████│         │  │   │
│  │  │    │ □□  │   │     │    │     │      │     │    │█████│         │  │   │
│  │  │    │     │   └─────┘    └─────┘      └─────┘    │█████│         │  │   │
│  │  │    │     │    WIP:3      WIP:2        WIP:1     │     │         │  │   │
│  │  │    └─────┘                                          └─────┘         │  │   │
│  │  │                                                                   │  │   │
│  │  │    □: 작업 카드    █: 완료된 작업                                  │  │   │
│  │  │    WIP: Work In Progress 제한                                     │  │   │
│  │  │                                                                   │  │   │
│  │  └───────────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  2. LIMIT WIP (WIP 제한)                                                │   │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │   │
│  │  │                                                                   │  │   │
│  │  │    "동시에 진행할 수 있는 작업 수를 제한하라"                       │  │   │
│  │  │                                                                   │  │   │
│  │  │    Why?                                                          │  │   │
│  │  │    • 멀티태스킹 비용 감소 (컨텍스트 스위칭)                         │  │   │
│  │  │    • 병목 가시화                                                  │  │   │
│  │  │    • 흐름 개선                                                    │  │   │
│  │  │    • "Stop Starting, Start Finishing"                            │  │   │
│  │  │                                                                   │  │   │
│  │  │    How?                                                          │  │   │
│  │  │    • 팀원 수 × 1.5 정도로 시작                                    │  │   │
│  │  │    • 데이터 기반 조정                                             │  │   │
│  │  │    • 열별로 다르게 설정                                           │  │   │
│  │  │                                                                   │  │   │
│  │  └───────────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  3. MANAGE FLOW (흐름 관리)                                             │   │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │   │
│  │  │                                                                   │  │   │
│  │  │    Lead Time            Cycle Time                               │  │   │
│  │  │    ┌──────────────────────────────────────────┐                  │  │   │
│  │  │    │                                          │                  │  │   │
│  │  │    │  Wait   Wait   Active   Wait   Active    │                  │  │   │
│  │  │    │  ○──────○──────●─────────○──────●──────→│                  │  │   │
│  │  │    │        │                │                │                  │  │   │
│  │  │    │   Request               Work    Done     │                  │  │   │
│  │  │    │   ◄─────────────────────────────────►    │                  │  │   │
│  │  │    │              Lead Time                    │                  │  │   │
│  │  │    └──────────────────────────────────────────┘                  │  │   │
│  │  │                                                                   │  │   │
│  │  │    목표: 리드 타임 최소화, 처리량 최적화                            │  │   │
│  │  │                                                                   │  │   │
│  │  └───────────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  4. MAKE POLICIES EXPLICIT (정책 명시화)                                │   │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │   │
│  │  │                                                                   │  │   │
│  │  │    Definition of Ready (DoR):                                     │  │   │
│  │  │    • 요구사항이 명확함                                            │  │   │
│  │  │    • 인수 기준이 정의됨                                           │  │   │
│  │  │    • 의존성이 해결됨                                              │  │   │
│  │  │                                                                   │  │   │
│  │  │    Definition of Done (DoD):                                      │  │   │
│  │  │    • 코드 리뷰 완료                                               │  │   │
│  │  │    • 테스트 통과                                                  │  │   │
│  │  │    • 문서화 완료                                                  │  │   │
│  │  │                                                                   │  │   │
│  │  └───────────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  5. IMPLEMENT FEEDBACK LOOPS (피드백 루프 구현)                         │   │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │   │
│  │  │                                                                   │  │   │
│  │  │    Daily Standup (일일)                                           │  │   │
│  │  │    ┌─────────────────────────────────────────────────────┐       │  │   │
│  │  │    │ "어디가 막히고 있나?" "도울 일이 있나?"              │       │  │   │
│  │  │    └─────────────────────────────────────────────────────┘       │  │   │
│  │  │                                                                   │  │   │
│  │  │    Replenishment (주간)                                           │  │   │
│  │  │    ┌─────────────────────────────────────────────────────┐       │  │   │
│  │  │    │ Ready 열 채우기, 우선순위 조정                       │       │  │   │
│  │  │    └─────────────────────────────────────────────────────┘       │  │   │
│  │  │                                                                   │  │   │
│  │  │    Service Delivery Review (격주/월간)                           │  │   │
│  │  │    ┌─────────────────────────────────────────────────────┐       │  │   │
│  │  │    │ 리드 타임, 처리량, 품질 메트릭 검토                  │       │  │   │
│  │  │    └─────────────────────────────────────────────────────┘       │  │   │
│  │  │                                                                   │  │   │
│  │  └───────────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  6. IMPROVE COLLABORATIVELY (협력적 개선)                               │   │
│  │  ┌───────────────────────────────────────────────────────────────────┐  │   │
│  │  │                                                                   │  │   │
│  │  │    실험 기반 개선:                                                │  │   │
│  │  │    ┌─────────────────────────────────────────────────────────┐   │  │   │
│  │  │    │ Hypothesis → Experiment → Measure → Adapt               │   │  │   │
│  │  │    │                                                         │   │  │   │
│  │  │    │ "WIP를 2 줄이면 리드 타임이 20% 감소할 것이다"           │   │  │   │
│  │  │    │ → 2주 실험 → 측정 → 결과에 따라 정책 수정                │   │  │   │
│  │  │    └─────────────────────────────────────────────────────────┘   │  │   │
│  │  │                                                                   │  │   │
│  │  └───────────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 누적 흐름도(CFD) 분석

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                     CUMULATIVE FLOW DIAGRAM (CFD)                              │
│                                                                                │
│   작업량                                                                       │
│     ▲                                                                         │
│     │                                          ┌───────────────── Done       │
│     │                                    ┌─────┘                             │
│     │                              ┌─────┘             Review               │
│     │                        ┌─────┘                 ──────────────────     │
│     │                  ┌─────┘           In Progress                        │
│     │            ┌─────┘             ──────────────────────────────────     │
│     │      ┌─────┘         Ready                                            │
│     │ ─────┘         ──────────────────────────────────────────────────     │
│     │ Backlog                                                                   │
│     │ ──────────────────────────────────────────────────────────────────     │
│     │                                                                         │
│     └───────────────────────────────────────────────────────────────────►    │
│                                     시간                                       │
│                                                                                │
│   분석 요소:                                                                   │
│   ┌─────────────────────────────────────────────────────────────────────┐    │
│   │                                                                     │    │
│   │   Lead Time = Done 영역의 수평 거리                                 │    │
│   │   ┌──────────────────────────────────────────────┐                 │    │
│   │   │            ◄───────────────────────────────► │                 │    │
│   │   │                    Lead Time                  │                 │    │
│   │   └──────────────────────────────────────────────┘                 │    │
│   │                                                                     │    │
│   │   WIP = In Progress 영역의 수직 거리                                │    │
│   │   ┌──────────────────────────────────────────────┐                 │    │
│   │   │              ▲                               │                 │    │
│   │   │              │ WIP                           │                 │    │
│   │   │              ▼                               │                 │    │
│   │   └──────────────────────────────────────────────┘                 │    │
│   │                                                                     │    │
│   │   Throughput = Done 영역의 기울기                                   │    │
│   │                                                                     │    │
│   │   병목 징후:                                                         │    │
│   │   • 특정 영역이 넓어짐 → WIP 증가 → 병목                            │    │
│   │   • 기울기가 평평해짐 → 처리량 감소                                  │    │
│   │                                                                     │    │
│   └─────────────────────────────────────────────────────────────────────┘    │
│                                                                                │
└───────────────────────────────────────────────────────────────────────────────┘
```

### 핵심 알고리즘: 리드 타임 예측

```python
"""
칸반 리드 타임 예측 및 분석 시스템
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import statistics
from collections import defaultdict

@dataclass
class KanbanCard:
    """칸반 카드"""
    id: str
    title: str
    entry_date: datetime           # Backlog 진입
    start_date: Optional[datetime] # 작업 시작
    done_date: Optional[datetime]  # 완료
    blocked_days: int = 0

    @property
    def lead_time(self) -> Optional[int]:
        """리드 타임 (일 단위)"""
        if self.entry_date and self.done_date:
            return (self.done_date - self.entry_date).days
        return None

    @property
    def cycle_time(self) -> Optional[int]:
        """사이클 타임 (일 단위)"""
        if self.start_date and self.done_date:
            return (self.done_date - self.start_date).days
        return None


class KanbanMetrics:
    """칸반 메트릭 계산기"""

    def __init__(self, completed_cards: List[KanbanCard]):
        self.cards = completed_cards

    def calculate_lead_time_stats(self) -> Dict:
        """리드 타임 통계"""
        lead_times = [c.lead_time for c in self.cards if c.lead_time is not None]

        if not lead_times:
            return {"error": "데이터 부족"}

        return {
            "count": len(lead_times),
            "mean": round(statistics.mean(lead_times), 1),
            "median": round(statistics.median(lead_times), 1),
            "stdev": round(statistics.stdev(lead_times), 1) if len(lead_times) > 1 else 0,
            "percentile_85": round(sorted(lead_times)[int(len(lead_times) * 0.85)], 1),
            "percentile_95": round(sorted(lead_times)[int(len(lead_times) * 0.95)], 1),
        }

    def calculate_throughput(self, period_days: int = 7) -> Dict:
        """처리량 계산"""
        now = datetime.now()
        period_start = now - timedelta(days=period_days)

        completed_in_period = [
            c for c in self.cards
            if c.done_date and c.done_date >= period_start
        ]

        return {
            "period_days": period_days,
            "completed_count": len(completed_in_period),
            "daily_average": round(len(completed_in_period) / period_days, 2),
        }

    def predict_delivery_date(self, remaining_items: int,
                               confidence: float = 0.85) -> Dict:
        """
        배포일 예측 (몬테카를로 간소화)
        """
        throughput = self.calculate_throughput(period_days=30)
        daily_rate = throughput["daily_average"]

        if daily_rate == 0:
            return {"error": "처리량 데이터 부족"}

        # 평균 기반 예측
        avg_days = remaining_items / daily_rate

        # 신뢰도 기반 보정
        lead_stats = self.calculate_lead_time_stats()
        variability = lead_stats.get("stdev", 0)

        # 신뢰도가 높을수록 더 보수적
        buffer_factor = 1 + (1 - confidence) * (variability / lead_stats.get("mean", 1))
        predicted_days = avg_days * buffer_factor

        predicted_date = datetime.now() + timedelta(days=predicted_days)

        return {
            "remaining_items": remaining_items,
            "daily_throughput": daily_rate,
            "predicted_days": round(predicted_days, 1),
            "predicted_date": predicted_date.strftime("%Y-%m-%d"),
            "confidence": f"{confidence * 100:.0f}%",
        }

    def identify_bottleneck(self) -> Dict:
        """병목 식별"""
        # 사이클 타임 vs 리드 타임 비율로 대기 시간 분석
        wait_analysis = []

        for card in self.cards:
            if card.lead_time and card.cycle_time:
                wait_time = card.lead_time - card.cycle_time
                wait_ratio = wait_time / card.lead_time if card.lead_time > 0 else 0
                wait_analysis.append({
                    "card_id": card.id,
                    "wait_time": wait_time,
                    "wait_ratio": round(wait_ratio, 2)
                })

        avg_wait_ratio = statistics.mean(
            [w["wait_ratio"] for w in wait_analysis]
        ) if wait_analysis else 0

        return {
            "avg_wait_ratio": round(avg_wait_ratio, 2),
            "interpretation": self._interpret_wait_ratio(avg_wait_ratio),
            "recommendations": self._generate_recommendations(avg_wait_ratio)
        }

    def _interpret_wait_ratio(self, ratio: float) -> str:
        """대기 비율 해석"""
        if ratio > 0.7:
            return "대기 시간이 매우 높음 - 심각한 병목"
        elif ratio > 0.5:
            return "대기 시간이 높음 - 병목 개선 필요"
        elif ratio > 0.3:
            return "대기 시간이 보통 - 지속적 모니터링"
        else:
            return "대기 시간이 낮음 - 효율적 흐름"

    def _generate_recommendations(self, ratio: float) -> List[str]:
        """개선 권장사항"""
        recommendations = []

        if ratio > 0.5:
            recommendations.append("WIP 제한을 낮추어 병목 완화")
            recommendations.append("병목 단계에 자원 추가")
            recommendations.append("작업 단위를 더 작게 분할")
        elif ratio > 0.3:
            recommendations.append("정기적 흐름 검토")
            recommendations.append("피드백 루프 강화")

        return recommendations

    def generate_cfd_data(self) -> Dict:
        """CFD 데이터 생성"""
        # 날짜별 상태 누적 계산
        daily_totals = defaultdict(lambda: {"backlog": 0, "in_progress": 0, "done": 0})

        for card in self.cards:
            if card.entry_date:
                entry = card.entry_date.date()
                daily_totals[entry]["backlog"] += 1

            if card.done_date:
                done = card.done_date.date()
                daily_totals[done]["done"] += 1

        return dict(daily_totals)


# 실무 예시
if __name__ == "__main__":
    from datetime import datetime, timedelta

    # 샘플 데이터
    base_date = datetime(2026, 1, 1)
    cards = []

    for i in range(20):
        entry = base_date + timedelta(days=i)
        start = entry + timedelta(days=2)
        done = start + timedelta(days=i % 5 + 1)

        cards.append(KanbanCard(
            id=f"CARD-{i+1:03d}",
            title=f"작업 {i+1}",
            entry_date=entry,
            start_date=start,
            done_date=done
        ))

    metrics = KanbanMetrics(cards)

    print("=== 리드 타임 통계 ===")
    for key, value in metrics.calculate_lead_time_stats().items():
        print(f"{key}: {value}")

    print("\n=== 처리량 (7일) ===")
    for key, value in metrics.calculate_throughput().items():
        print(f"{key}: {value}")

    print("\n=== 배포일 예측 (남은 10개) ===")
    prediction = metrics.predict_delivery_date(remaining_items=10)
    for key, value in prediction.items():
        print(f"{key}: {value}")

    print("\n=== 병목 분석 ===")
    bottleneck = metrics.identify_bottleneck()
    print(f"평균 대기 비율: {bottleneck['avg_wait_ratio']}")
    print(f"해석: {bottleneck['interpretation']}")
    print(f"권장사항: {bottleneck['recommendations']}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### 심층 기술 비교: 칸반 vs 스크럼

| 비교 항목 | 칸반 | 스크럼 |
|-----------|------|--------|
| **이터레이션** | 없음 (연속적 흐름) | 1-4주 스프린트 |
| **역할** | 정의되지 않음 | PO, SM, 개발팀 |
| **작업 할당** | Pull (용량 있을 때) | Sprint Planning |
| **변경 수용** | 언제든 가능 | 스프린트 내 고정 |
| **WIP 제한** | 핵심 원칙 | 스프린트 범위로 제한 |
| **측정 지표** | 리드 타임, 처리량 | 속도(Velocity) |
| **예측** | 확률적 | 확정적(스프린트) |
| **적합 환경** | 운영, 유지보수, 서비스 | 제품 개발, 프로젝트 |

### 과목 융합 관점 분석

#### 1. 운영 관리 × 소프트웨어 공학 융합
칸반은 도요타의 JIT(Just-In-Time) 생산 시스템을 소프트웨어 개발에 적용한 것이다. WIP 제한은 재고 비용(Work-in-progress inventory)을 관리하는 운영 관리 원칙의 소프트웨어 버전이다.

#### 2. 데이터 분석 × 프로세스 개선 융합
칸반은 **데이터 기반 의사결정**을 강조한다. 리드 타임 분포, 처리량 추세, CFD 분석을 통해 프로세스 개선점을 객관적으로 식별한다. 몬테카를로 시뮬레이션으로 배포일을 확률적으로 예측한다.

#### 3. DevOps × SRE 융합
칸반은 DevOps의 지속적 배포 파이프라인과 자연스럽게 통합된다. SRE의 SLI/SLO 달성을 위해 리드 타임을 최적화하고, 에러 예산(Error Budget)과 WIP를 연계하여 안정성-속도 균형을 관리한다.

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 기술사적 판단: 실무 시나리오 3가지

#### 시나리오 1: 스크럼에서 칸반으로 전환
**상황**: 운영팀이 스프린트 방식에 적응하지 못함

**기술사적 의사결정 과정**:
1. **하이브리드 접근**: 스크럼-반(Scrumban)으로 점진적 전환
2. **스프린트 폐지**: 이터레이션 없는 연속적 흐름으로
3. **WIP 제한 도입**: 팀 규모 × 1.5로 시작
4. **메트릭 변경**: Velocity → Lead Time/Throughput

#### 시나리오 2: 긴급 작업과 계획된 작업의 균형
**상황**: 운영 이슈가 개발 작업을 방해

**기술사적 의사결정 과정**:
1. **긴급 슬롯**: WIP의 20%를 긴급 작업용 예약
2. **Swimlane 분리**: 긴급/계획/기술부채 레인 구분
3. **서비스 클래스**: 긴급/표준/무기한 클래스 정의
4. **에스컬레이션 정책**: 언제 긴급으로 승격하는지 명확화

#### 시나리오 3: 병목 해소 실패
**상황**: WIP 제한을 줄였으나 오히려 대기 시간 증가

**기술사적 의사결정 과정**:
1. **근본 원인 분석**: 병목이 어디인지 CFD로 식별
2. **단계 분할**: 큰 단계를 더 작게 나누어 흐름 개선
3. **자원 재배치**: 병목 단계에 인력 집중
4. **프로세스 재설계**: 불필요한 단계 제거

### 도입 시 고려사항 체크리스트

#### 기술적 고려사항
- [ ] 칸반 보드 도구 선정 (Jira, Trello, Azure Boards)
- [ ] CFD 및 분석 대시보드 구축
- [ ] 리드 타임 자동 추적 시스템
- [ ] CI/CD 파이프라인과 칸반 연동

#### 운영/보안적 고려사항
- [ ] WIP 제한에 대한 팀 동의
- [ ] 정기적 흐름 검토 미팅
- [ ] 정책(DoR, DoD) 명시화
- [ ] 서비스 수준 기대치(SLE) 정의

### 주의사항 및 안티패턴

1. **Unlimited WIP**: WIP 제한 없이 칸반 보드만 사용
2. **Ignoring Blocked Items**: 차단된 항목 방치
3. **Push System**: Pull 대신 관리자가 작업 할당
4. **No Metrics**: 측정 없이 감각에 의존

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 지표 | 도입 전 | 도입 후 | 개선율 |
|------|---------|---------|--------|
| 평균 리드 타임 | 30일 | 12일 | **60% 단축** |
| 처리량 (주당) | 5개 | 8개 | **60% 향상** |
| 예측 정확도 | 50% | 85% | **70% 향상** |
| 병목 해소율 | 20% | 75% | **275% 향상** |
| 팀 만족도 | 65% | 85% | **31% 향상** |

### 미래 전망 및 진화 방향

1. **AI 기반 흐름 최적화**: 머신러닝으로 WIP 제한 자동 조정
2. **예측적 분석**: 실시간 리드 타임 예측
3. **하이퍼 개인화**: 팀별 맞춤형 칸반 구성
4. **Flow Framework**: 가치 스트림 중심의 엔터프라이즈 칸반

### ※ 참고 표준/가이드
- **Kanban (David J. Anderson, 2010)**: 칸반 원전
- **The Kanban Guide (Kanban University)**: 공식 가이드
- **Actionable Agile Metrics (Daniel Vacanti)**: 메트릭 가이드

---

## 📌 관련 개념 맵 (Knowledge Graph)

1. [린 소프트웨어 개발](./87_lean_software_development.md) - 칸반의 철학적 기반
2. [WIP 제한](./84_kanban.md) - 칸반의 핵심 메커니즘
3. [누적 흐름도](./86_cumulative_flow_diagram.md) - 칸반의 분석 도구
4. [스크럼](./62_scrum_framework.md) - 칸반과 비교되는 애자일 프레임워크
5. [데브옵스](./97_devops.md) - 칸반과 결합되는 운영 모델
6. [리드 타임](./85_lead_time_cycle_time.md) - 칸반의 핵심 메트릭

---

## 👶 어린이를 위한 3줄 비유 설명

**비유: 수영장 슬라이드 줄**

1. **한 번에 몇 명만 탈 수 있어요**: 슬라이드에 한 번에 너무 많이 올라가면 막혀요. 그래서 "지금은 3명까지만!"이라고 정해요.

2. **어디가 느린지 볼 수 있어요**: 누가 물에 빠져서 늦었는지, 어디가 막혔는지 한눈에 보여요. "저기서 막혔네, 도와주자!"

3. **빨리 끝내는 게 목표예요**: 많이 시작하는 것보다 빨리 끝내는 게 더 중요해요. "빨리 끝내고 다음 친구가 탈 수 있게 해요!"
