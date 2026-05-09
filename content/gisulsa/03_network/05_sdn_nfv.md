+++
weight = 5
title = "5. SDN·NFV·OpenFlow (SDN NFV OpenFlow)"
date = "2026-05-09"
[extra]
categories = "gisulsa-network"
+++
# 🎯 핵심 키워드: SDN (Software Defined Networking), NFV (Network Functions Virtualization), OpenFlow

> **출제 빈도**: ★★★★☆ | **난이도**: ★★★★☆

## 1. 정의 (Definition)

SDN은 제어 평면(Control Plane)과 데이터 평면(Data Plane)을 분리하여 중앙 집중형으로 네트워크를 프로그래밍하는 구조다.  
NFV는 방화벽, 로드밸런서, WAN 최적화 같은 네트워크 기능을 전용 장비 대신 가상화 소프트웨어로 제공하는 개념이다.  
OpenFlow는 SDN 컨트롤러와 스위치 사이에서 플로우 규칙을 교환하는 대표 southbound 인터페이스다.

## 2. 출제 포인트 (Exam Key Points)

| 포인트 | 내용 | 채점 비중 |
|--------|------|----------|
| 정의 | SDN은 제어 평면(Control Plane)과 데이터 평면(Data Plane)을 분리하여 중앙 집중형으로 네트워크를 프로그래밍하는 구조다.와 OpenFlow는 SDN 컨트롤러와 스위치 사이에서 플로우 규칙을 교환하는 대표 southbound 인터페이스다.의 인과관계를 한 문장 구조로 묶어 서술한다. | 20% |
| 구성요소 | 제어 평면과 데이터 평면 분리, VNF와 서비스 체이닝, OpenFlow 매치-액션 모델를 구조-동작-효과 순으로 정리한다. | 30% |
| 비교/차이 | SDN vs NFV의 선택 기준과 트레이드오프를 비교표로 제시한다. | 30% |
| 적용사례 | 데이터센터 네트워크 자동화와 통신사의 가상화망 구축 관점에서 기대효과와 실패 포인트를 함께 적는다. | 20% |

## 3. 답안 목차 템플릿 (Answer Outline Template)

문제: "SDN과 NFV의 개념 및 차이, OpenFlow의 역할을 설명하시오."

```text
Ⅰ. 개요
   1. 정의
   2. 수동 네트워크 운영 한계

Ⅱ. 핵심 구성요소
   1. SDN 아키텍처
   2. NFV와 OpenFlow의 적용 방식

Ⅲ. 특징 및 장단점
   1. 자동화, 민첩성, 장비 종속성 감소
   2. 컨트롤러 장애와 성능·보안 이슈

Ⅳ. 유사 기술과의 비교
   - SDN vs NFV 비교표

Ⅴ. 적용사례 및 향후전망
   1. 데이터센터 네트워크 자동화와 통신사의 가상화망 구축
   2. Intent-based networking과 클라우드 네이티브 네트워크 진화
```

## 4. 핵심 비교표 (Key Comparison Table)

| 구분 | SDN | NFV |
| --- | --- | --- |
| 핵심 초점 | 제어의 중앙화와 프로그래밍 | 기능의 가상화와 유연한 배치 |
| 대상 | 네트워크 제어 구조 | 네트워크 서비스 기능 |
| 장점 | 정책 일관성과 자동화 | CAPEX/OPEX 절감 |
| 주의점 | 컨트롤러 의존성 | 가상화 성능과 운영 복잡도 |
| 대표 키워드 | Controller, OpenFlow | VNF, MANO |

## 5. 인출 훈련 문제 (Output Drills)

### 단답형 (30초)
1. SDN (Software Defined Networking)의 정의를 한 문장으로 쓰시오.
2. SDN·NFV·OpenFlow 답안에서 반드시 써야 할 핵심 구성요소 3가지를 나열하시오.
3. SDN와 NFV의 가장 큰 차이점을 설명하시오.
4. "제어 분리와 기능 가상화를 구분해 설명하는 연습"를 답안 키워드 3개로 압축하시오.
5. 데이터센터 네트워크 자동화와 통신사의 가상화망 구축 중 하나를 들고 기대효과 2가지를 말하시오.

### 서술형 (5분)
6. "SDN과 NFV의 개념 및 차이, OpenFlow의 역할을 설명하시오."의 핵심 구성요소와 기대효과를 5분 답안으로 정리하시오.
7. "SDN vs NFV"의 선택 기준과 실패 시 발생하는 운영 리스크를 서술하시오.

### 답안 작성 (25분)
8. "SDN과 NFV의 개념 및 차이, OpenFlow의 역할을 설명하시오." (개념, 구조, 비교, 적용사례, 향후전망 포함)

## 6. 면접 예상 질문 (Mock Interview)

Q1: "SDN과 NFV의 차이를 설명해보세요."  
Q2: "OpenFlow는 어디에서 어떤 역할을 합니까?"  
Q3: "데이터센터 자동화에는 SDN과 NFV 중 무엇을 우선 적용하시겠습니까?"
