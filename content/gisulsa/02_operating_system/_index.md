+++
weight = 2
title = "2. 운영체제 (Operating System)"
[extra]
categories = "gisulsa-operating-system"
+++
# 02. 운영체제 (Operating System)

> **섹션 목표**: 자원 관리 원리와 동시성 제어를 프로세스·메모리·파일 관점에서 답안화하는 훈련에 집중한다.

## 학습 전략

- **30초 훈련**: 정의 1문장, 비교축 1개, 적용사례 1개를 말로 바로 꺼내는 연습을 한다.
- **5분 훈련**: 개요-구성요소-비교-사례의 4단 구조로 압축 답안을 손으로 써본다.
- **25분 훈련**: 비교표를 먼저 그린 뒤, 장단점과 실무 판단을 연결하는 기술사형 서술을 완성한다.

## 과목 공략 포인트

- 운영체제 문제는 기능 나열보다 자원 배분 정책과 성능 지표를 함께 적어야 고득점이 가능하다.
- 프로세스, 스케줄링, 메모리, 동기화는 모두 응답시간과 안정성이라는 공통 목적 아래 연결해서 쓴다.
- 실무 사례는 장애 예방, 지연 최소화, 자원 활용률 개선의 세 축으로 정리하면 면접에도 강하다.

## 키워드 마스터 리스트

| 번호 | 파일 | 키워드 클러스터 | 훈련 포인트 |
|------|------|----------------|-------------|
| 01 | [프로세스·스레드·PCB](/gisulsa/02_operating_system/01_process_thread/) | 프로세스 (Process), 스레드 (Thread), PCB (Process Control Block) | 격리 수준, 공유 자원, 문맥 교환 비용을 한 번에 비교하는 연습 |
| 02 | [CPU 스케줄링](/gisulsa/02_operating_system/02_scheduling/) | CPU 스케줄링 (CPU Scheduling), 선점형 (Preemptive), 라운드 로빈 (Round Robin) | 평균 대기시간과 응답시간 관점에서 알고리즘을 비교하는 연습 |
| 03 | [메모리 관리·페이징·세그멘테이션](/gisulsa/02_operating_system/03_memory_management/) | 메모리 관리 (Memory Management), 페이징 (Paging), 세그멘테이션 (Segmentation) | 단편화와 보호 관점을 동시에 써서 비교하는 연습 |
| 04 | [교착상태·세마포어·뮤텍스](/gisulsa/02_operating_system/04_deadlock_sync/) | 교착상태 (Deadlock), 세마포어 (Semaphore), 뮤텍스 (Mutex) | 4가지 데드락 조건을 암기하고 예방·회피·탐지 차이를 말하는 연습 |
| 05 | [파일시스템·I/O·버퍼링](/gisulsa/02_operating_system/05_file_io/) | 파일 시스템 (File System), 입출력 버퍼링 (I/O Buffering), 저널링 (Journaling) | inode, 버퍼 캐시, 저널링을 한 흐름으로 설명하는 연습 |

## 실전 사용법

1. 가장 자주 출제되는 파일부터 3일 주기로 회독한다.
2. 비교표는 소리 내어 암기하고, 목차 템플릿은 빈 종이에 재현한다.
3. 실무 사례는 자신이 경험한 프로젝트로 치환해 1분 면접 답변까지 연결한다.
