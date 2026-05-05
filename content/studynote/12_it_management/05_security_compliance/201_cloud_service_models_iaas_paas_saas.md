+++
weight = 201
title = "201. 클라우드 서비스 모델 (IaaS, PaaS, SaaS, BaaS, FaaS) 엔터프라이즈 도입 전략"
date = "2026-04-21"
[extra]
categories = "studynote-it-management"
+++

## 0. 핵심 인사이트

> **핵심**: 클라우드 서비스 모델 (IaaS, PaaS, SaaS, BaaS, FaaS) 엔터프라이즈 도입 전략의 본질은 클라우드 서비스 모델 (IaaS, PaaS, SaaS, BaaS, FaaS) 엔터프라이즈 도입 전략의 목적·구성·운영 기준을 명확히 설명하는 주제를 비즈니스 가치, 통제, 실행 관점에서 일관되게 연결하는 데 있다.
> **비유**: 복잡한 시스템을 안전하게 연결하는 교통망 설계도와 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

클라우드 컴퓨팅(Cloud Computing)은 인터넷을 통해 컴퓨팅 자원(서버·스토리지·네트워크·소프트웨어)을 필요할 때 필요한 만큼 사용하는 IT 인프라 패러다임이다. NIST (National Institute of Standards and Technology, 미국 국립표준기술연구소)는 클라우드 서비스를 제공 방식에 따라 IaaS (Infrastructure as a Service), PaaS (Platform as a Service), SaaS (Software as a Service) 세 가지 기본 모델로 정의하였으며, 이후 BaaS (Backend as a Service), FaaS (Function as a Service) 등 특화 모델이 추가되었다.

클라우드 도입의 핵심 가치는 단순한 비용 절감을 넘어선다. 탄력적 확장성(Elasticity), 글로벌 즉시 배포(Rapid Deployment), 관리 부담 감소(Reduced Operational Overhead), 혁신 주기 단축이 실질적인 비즈니스 가치다. 그러나 모델 선택이 잘못되면 보안 취약, 통제 불가, 예상치 못한 비용 폭증으로 이어지므로, 정확한 모델 이해는 클라우드 전략의 출발점이다.

---

## 2. 구성요소

```text
┌─────────────────────────────────────────────────────────────────────┐
│           클라우드 서비스 모델별 책임 범위 (■=고객, □=공급자)       │
├──────────────────────┬──────────┬──────────┬──────────┬────────────┤
│       계층           │ On-Prem  │  IaaS    │  PaaS    │   SaaS     │
├──────────────────────┼──────────┼──────────┼──────────┼────────────┤
│ 애플리케이션         │    ■     │    ■     │    ■     │     □      │
│ 데이터               │    ■     │    ■     │    ■     │   ■(일부)  │
│ 런타임/미들웨어      │    ■     │    ■     │    □     │     □      │
│ OS                   │    ■     │    ■     │    □     │     □      │
│ 가상화               │    ■     │    □     │    □     │     □      │
│ 서버/스토리지/네트워크│   ■     │    □     │    □     │     □      │
│ 물리 인프라          │    ■     │    □     │    □     │     □      │
└──────────────────────┴──────────┴──────────┴──────────┴────────────┘
■ 고객 책임  □ 클라우드 공급자 책임
```

| 모델 | 정의 | 제공 범위 | 대표 서비스 | 주 사용자 |
|:---|:---|:---|:---|:---|
| IaaS | 가상화된 컴퓨팅 자원 제공 | VM·스토리지·네트워크 | AWS EC2, Azure VM, GCP CE | 시스템 관리자, DevOps |
| PaaS | 애플리케이션 개발 플랫폼 제공 | OS+런타임+미들웨어 | Heroku, AWS Elastic Beanstalk, GCP App Engine | 애플리케이션 개발자 |
| SaaS | 완성된 소프트웨어 제공 | 전체 스택 | Office 365, Salesforce, Google Workspace | 최종 사용자 |
| BaaS | 모바일/웹 앱 백엔드 기능 제공 | 인증·DB·알림 등 API | Firebase, AWS Amplify | 프론트엔드 개발자 |
| FaaS | 개별 함수 단위 실행 환경 제공 | 실행 환경(서버리스) | AWS Lambda, Azure Functions, GCP Cloud Functions | 이벤트 드리븐 개발자 |

---

## 3. 구조 및 원리

| 구분 | IaaS | PaaS | SaaS | FaaS |
|:---|:---|:---|:---|:---|
| 초기 비용 | 중간 | 낮음 | 매우 낮음 | 거의 없음 |
| 운영 부담 | 높음 | 중간 | 매우 낮음 | 없음(공급자 관리) |
| 커스터마이징 | 매우 높음 | 중간 | 낮음 | 함수 단위 |
| 벤더 락인 위험 | 낮음 | 중간 | 높음 | 중간~높음 |
| 확장성 | 수동/자동 | 자동 | 자동 | 즉시 자동 |
| 보안 통제 범위 | 넓음 | 중간 | 좁음 | 매우 좁음 |

기업은 단일 모델을 선택하기보다 워크로드 특성에 따라 혼합(Hybrid) 방식을 채택한다. 핵심 비즈니스 시스템(ERP, 금융 코어)은 IaaS 또는 On-Premise로 유지하고, 협업 도구(이메일, 화상회의)는 SaaS로 전환하며, 신규 디지털 서비스는 PaaS/FaaS로 개발하는 3계층 전략이 일반적이다.

| 배포 모델 | 설명 | 적합 서비스 모델 |
|:---|:---|:---|
| 퍼블릭 클라우드 (Public Cloud) | 공유 인프라, CSP 완전 관리 | SaaS, PaaS, FaaS |
| 프라이빗 클라우드 (Private Cloud) | 전용 인프라, 고통제 | IaaS |
| 하이브리드 클라우드 (Hybrid Cloud) | 온프레미스 + 퍼블릭 혼합 | IaaS + SaaS 혼합 |
| 멀티 클라우드 (Multi-Cloud) | 복수 CSP 사용 | 모든 모델 혼합 |

---

## 4. 비교 및 연결

| 선택 기준 | 권장 모델 |
|:---|:---|
| 빠른 출시(Time-to-Market) 최우선 | SaaS 또는 PaaS |
| 높은 커스터마이징 요구 | IaaS |
| 비용 최적화, 이벤트 드리븐 워크로드 | FaaS |
| 모바일 앱 백엔드 빠른 구축 | BaaS |
| 규제 산업(금융·의료)의 데이터 통제 | IaaS + Private Cloud |

SaaS 도입 시 데이터 주권(Data Sovereignty) 이슈가 발생할 수 있다. EU GDPR (General Data Protection Regulation, 유럽 일반 데이터 보호 규정), 국내 개인정보보호법은 데이터의 물리적 저장 위치와 제3자 처리 방식에 대한 규제를 포함하므로, SaaS 계약 시 데이터 처리 위치(Data Residency)와 클라우드 공급자의 보안 인증(ISO 27001, SOC 2 Type II)을 반드시 확인해야 한다.

클라우드 비용 관리(FinOps, Financial Operations)를 위해 IaaS에서는 예약 인스턴스(Reserved Instance)·스팟 인스턴스(Spot Instance) 활용, PaaS에서는 자동 스케일링 정책 최적화, FaaS에서는 함수 실행 시간·메모리 튜닝을 통해 비용을 절감한다.

---

## 5. 실무 적용 및 판단

클라우드 서비스 모델의 올바른 선택과 책임 공유 모델의 이해는 디지털 전환의 성패를 좌우한다. IaaS부터 FaaS까지 각 모델의 관리 범위, 비용 구조, 보안 책임을 명확히 구분함으로써 조직은 워크로드에 최적화된 아키텍처를 설계하고, 불필요한 기술 부채와 비용 낭비를 방지할 수 있다.

기술사 시험에서는 단순 모델 나열을 넘어서 ① 책임 공유 모델의 계층별 경계, ② FaaS·BaaS 등 신규 모델의 등장 배경과 서버리스와의 관계, ③ 규제 환경에서의 SaaS 도입 위험과 대응 전략을 체계적으로 서술해야 고득점을 받을 수 있다.

---

## 6. 기대효과 및 결론

클라우드 서비스 모델 (IaaS, PaaS, SaaS, BaaS, FaaS) 엔터프라이즈 도입 전략를 올바르게 적용하면 의사결정의 일관성, 운영의 재현성, 통제의 추적성이 동시에 향상된다. 즉 “누가 무엇을 왜 했는가”가 남기 때문에 조직이 커질수록 효과가 커진다.

다만 클라우드 서비스 모델 (IaaS, PaaS, SaaS, BaaS, FaaS) 엔터프라이즈 도입 전략는 문서만 잘 만들어도 성공하는 영역이 아니다. 정의와 실행이 분리되면 형식주의가 되고, 자동화만 앞서면 통제 목적이 사라진다. 따라서 표준화와 민첩성, 통제와 생산성 사이의 균형이 항상 필요하다.

향후에는 정책 코드화(Policy as Code), 실시간 관측성(Observability), AI 기반 이상 탐지와 의사결정 지원이 결합되면서 관리 체계가 더 자동화되고 증거 중심으로 진화할 가능성이 크다. 결론적으로 핵심은 도구가 아니라 기준선이며, 기준선이 명확할 때만 자동화와 확장이 의미를 가진다.

---

## 7. 발전 흐름도

```text
사일로형 구조
    ↓
표준 인터페이스 정립
    ↓
클라우드 서비스 모델 (IaaS, PaaS, SaaS, BaaS, FaaS) 엔터프라이즈 도입 전략 정착
    ↓
자동화·관측성 결합
    ↓
지능형 최적화
```

---

## 8. 관련 개념 맵

| 개념 | 설명 | 연관 키워드 |
|:---|:---|:---|
| IaaS | Infrastructure as a Service, 인프라 임대 | EC2, VM, 네트워크 가상화 |
| PaaS | Platform as a Service, 개발 플랫폼 제공 | Heroku, App Engine, 미들웨어 |
| SaaS | Software as a Service, 완성 소프트웨어 제공 | Office 365, Salesforce |
| BaaS | Backend as a Service, 백엔드 API 제공 | Firebase, Amplify |
| FaaS | Function as a Service, 함수 단위 실행 | Lambda, 서버리스 |
| 책임 공유 모델 | Shared Responsibility Model, 보안 책임 경계 구분 | 고객 vs. 공급자 |
| Data Sovereignty | 데이터 주권, 물리적 저장 위치 규제 | GDPR, 개인정보보호법 |
| FinOps | 클라우드 비용 최적화 운영 방식 | 예약 인스턴스, 스팟 |
| Vendor Lock-in | 특정 공급자 의존성 심화 위험 | 멀티 클라우드, 오픈소스 |
