+++
weight = 1
title = "1. 컴퓨터 구조 (Computer Architecture)"
[extra]
categories = "gisulsa-computer-architecture"
+++
# 01. 컴퓨터 구조 (Computer Architecture)

> **섹션 목표**: CPU 성능 향상 원리와 병목 제어를 구조적으로 설명하는 훈련에 초점을 둔다.

## 학습 전략

- **30초 훈련**: 정의 1문장, 비교축 1개, 적용사례 1개를 말로 바로 꺼내는 연습을 한다.
- **5분 훈련**: 개요-구성요소-비교-사례의 4단 구조로 압축 답안을 손으로 써본다.
- **25분 훈련**: 비교표를 먼저 그린 뒤, 장단점과 실무 판단을 연결하는 기술사형 서술을 완성한다.

## 과목 공략 포인트

- 성능 향상 기술은 항상 지연 시간, 전력, 비용의 트레이드오프로 답안을 마무리한다.
- ISA, 메모리 계층, 병렬성은 각각 독립 주제가 아니라 하나의 성능 사슬로 연결해 쓴다.
- 실무 사례는 서버 CPU, 모바일 SoC, AI 가속기처럼 워크로드별 선택 기준을 넣어야 점수가 오른다.

## 키워드 마스터 리스트

| 번호 | 파일 | 키워드 클러스터 | 훈련 포인트 |
|------|------|----------------|-------------|
| 01 | [캐시·파이프라인·해저드](/gisulsa/01_computer_architecture/01_cache_pipeline/) | 캐시 메모리 (Cache Memory), 파이프라인 (Pipeline), 해저드 (Hazard) | 지역성-중첩-해저드 제어의 3축을 한 문단 안에서 연결하는 연습 |
| 02 | [메모리 계층·가상메모리·TLB](/gisulsa/01_computer_architecture/02_memory_hierarchy/) | 메모리 계층 (Memory Hierarchy), 가상 메모리 (Virtual Memory), TLB (Translation Lookaside Buffer) | 가상주소→TLB→페이지테이블→물리주소 순서로 주소 변환을 복기하는 연습 |
| 03 | [명령어 집합·RISC·CISC](/gisulsa/01_computer_architecture/03_instruction_set/) | 명령어 집합 구조 (ISA), RISC (Reduced Instruction Set Computer), CISC (Complex Instruction Set Computer) | 명령어 길이, 디코딩 난이도, 전력 특성을 한 세트로 비교하는 연습 |
| 04 | [I/O·DMA·인터럽트](/gisulsa/01_computer_architecture/04_io_dma_interrupt/) | 입출력 (I/O), DMA (Direct Memory Access), 인터럽트 (Interrupt) | Programmed I/O→Interrupt→DMA 진화 순서를 사례와 함께 말하는 연습 |
| 05 | [병렬처리·멀티코어·NUMA](/gisulsa/01_computer_architecture/05_parallel_multicore/) | 병렬 처리 (Parallel Processing), 멀티코어 (Multicore), NUMA (Non-Uniform Memory Access) | 암달의 법칙과 NUMA locality를 연결해 병렬화 한계를 설명하는 연습 |

## 실전 사용법

1. 가장 자주 출제되는 파일부터 3일 주기로 회독한다.
2. 비교표는 소리 내어 암기하고, 목차 템플릿은 빈 종이에 재현한다.
3. 실무 사례는 자신이 경험한 프로젝트로 치환해 1분 면접 답변까지 연결한다.
