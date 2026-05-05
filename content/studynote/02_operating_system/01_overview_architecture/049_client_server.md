+++
title = "049. 클라이언트-서버 — Client-Server Architecture"
weight = 49
date = "2026-04-05"
[extra]
categories = "studynote-operating-system"
+++

## 0. 핵심 인사이트

> **핵심**: 클라이언트-서버 — Client-Server Architecture은(는) 운영체제가 자원을 추상화하고 통제하는 과정에서 성능, 보호, 응답성을 동시에 조율하기 위해 필요한 핵심 개념이다.
> **비유**: 클라이언트-서버 — Client-Server Architecture은(는) 복잡한 교통을 한 번에 통제해 전체 흐름을 맞추는 신호 체계와 같다.

---

📝 모범 답안

## 1. 개요 및 필요성

```
클라이언트-서버 모델:

클라이언트 (Client):
  서비스 요청자
  능동적: 연결 시작
  예: 브라우저, 모바일 앱, CLI

서버 (Server):
  서비스 제공자
  수동적: 연결 대기
  예: 웹 서버, DB 서버, 파일 서버

기본 통신 흐름:

클라이언트 → [요청: Request] → 서버
클라이언트 ← [응답: Response] ← 서버

소켓 기반 통신:
  서버:
  1. socket() → 소켓 생성
  2. bind(IP, Port) → 주소 바인딩
  3. listen() → 연결 대기
  4. accept() → 연결 수락 (블로킹)
  5. recv()/send() → 데이터 교환
  6. close() → 연결 종료

  클라이언트:
  1. socket() → 소켓 생성
  2. connect(서버IP, 서버Port) → 연결 시도
  3. send()/recv() → 데이터 교환
  4. close() → 종료

아키텍처 유형:
  2-Tier: 클라이언트 ↔ DB 서버 (직접)
  3-Tier: 클라이언트 ↔ 앱 서버 ↔ DB 서버
  N-Tier: 마이크로서비스 (각 서비스가 클라+서버)
```

> 📢 **섹션 요약 비유**: 클라이언트-서버 = 손님과 식당 — 손님(클라이언트)이 주문(요청), 식당(서버)이 요리해서 전달(응답). 식당은 항상 열려 있고(listen), 손님이 와야 시작!

---

## 2. 구성요소

```
서버 연결 처리 모델:

1. 단일 프로세스 (Single Process):
  연결 하나씩 순차 처리

  while True:
      conn = accept()
      handle(conn)  # 완료될 때까지 대기

  문제: 동시 접속 불가 (처음부터 비실용)

2. 멀티프로세스 (Multi-Process):
  요청마다 fork()로 자식 프로세스 생성

  while True:
      conn = accept()
      pid = fork()
      if pid == 0:   # 자식 프로세스
          handle(conn)
          exit()

  Apache 전통 방식 (prefork MPM)

  단점:
  fork() 비용: ~수ms, 메모리 복사(CoW)
  프로세스당 메모리: ~50MB
  동시 1000연결: 50GB 메모리!

3. 멀티스레드 (Multi-Thread):
  요청마다 스레드 생성 (또는 스레드 풀)

  while True:
      conn = accept()
      thread = Thread(target=handle, args=(conn,))
      thread.start()

  Apache worker MPM

  스레드 특성:
  프로세스보다 생성 빠름 (~수십us)
  메모리 공유 (stack만 분리, 약 8MB)

  단점:
  C10K(10,000 동시 연결) 시 스레드 10,000개
  컨텍스트 스위칭 오버헤드 급증

4. 이벤트 루프 (Event Loop / Non-Blocking I/O):
  단일 스레드가 모든 연결 이벤트 처리

  epoll (Linux):
  while True:
      events = epoll.wait()  # 준비된 이벤트 대기
      for event in events:
          if event.type == READ:
              handle_read(event.fd)
          elif event.type == WRITE:
              handle_write(event.fd)

  Nginx, Node.js 방식

  장점:
  C10K 이상 처리 (C100K+)
  메모리 효율 (스레드 수 제한)

  단점:
  CPU 집약 작업에 부적합
  콜백 지옥 (비동기 복잡성)
```

> 📢 **섹션 요약 비유**: 서버 처리 방식 = 식당 서빙 방식 — 멀티프로세스(손님마다 요리사 1명), 멀티스레드(웨이터 여러 명), 이벤트 루프(웨이터 1명이 알림(이벤트) 받으며 효율적으로 처리). Nginx = 1명 슈퍼 웨이터!

---

## 3. 구조 및 원리

**핵심 조건**: 운영체제의 해당 메커니즘은 현재 상태 정보, 자원 제약, 정책 기준이 함께 정합성을 가질 때 안정적으로 동작한다.

동작 순서:
1. **요청 또는 이벤트 발생**: 사용자 요청, 인터럽트, 시스템 호출 등으로 커널이 해당 기능을 처리할 필요가 생긴다.
2. **현재 상태 확인**: 커널은 큐, 제어 블록, 메타데이터, 자원 가용량을 확인해 실행 가능 여부와 우선순위를 판단한다.
3. **정책 적용 및 자원 배정**: 해당 주제의 핵심 정책에 따라 상태 전이, 자원 할당, 보호 검사를 수행한다.
4. **결과 반영 및 후속 처리**: 처리 결과를 시스템 상태에 기록하고 다음 인터럽트·스케줄링·복구 단계로 연결한다.

```
C10K 문제 (1999, Dan Kegel):
  단일 서버에서 동시 10,000 연결 처리 도전

  당시 Apache (멀티프로세스) 한계:
  프로세스 10,000개 × 50MB = 500GB 메모리 필요
  컨텍스트 스위칭: 10,000번/초 → CPU 병목

해결책:

epoll (Linux 2.6):
  select(): O(N) - 전체 FD 스캔
  poll(): O(N) - 유사
  epoll(): O(1) - 이벤트 기반 준비 통보

  epoll 메커니즘:
  - epoll_create(): 이벤트 큐 생성
  - epoll_ctl(): FD 등록/수정/삭제
  - epoll_wait(): 준비된 이벤트 블로킹 대기

  10,000 연결 중 100개 활성 → 100개만 처리

Nginx 아키텍처:
  마스터 프로세스 1개
  워커 프로세스 = CPU 코어 수 (예: 16개)
  각 워커: 이벤트 루프로 수천 연결 처리

  구성:
  worker_processes auto;  # CPU 코어 수
  events {
      worker_connections 1024;
      use epoll;
  }

  이론적 최대: 16 × 1024 = 16,384 동시 연결

Node.js libuv:
  V8 엔진 + libuv(이벤트 루프 라이브러리)
  epoll(Linux), kqueue(macOS), IOCP(Windows) 통합

  비동기 I/O:
  fs.readFile('data.json', (err, data) => {
      // I/O 완료 후 콜백 (블로킹 없음)
  });
```

> 📢 **섹션 요약 비유**: C10K = 동시 손님 1만 명 — 멀티프로세스 식당은 요리사 1만 명 고용(불가). Nginx/epoll은 "요청 완료" 알림 시스템으로 효율화. 알림 받은 것만 처리!

---

## 4. 비교 및 연결

```
C10K 문제 (1999, Dan Kegel):
  단일 서버에서 동시 10,000 연결 처리 도전

  당시 Apache (멀티프로세스) 한계:
  프로세스 10,000개 × 50MB = 500GB 메모리 필요
  컨텍스트 스위칭: 10,000번/초 → CPU 병목

해결책:

epoll (Linux 2.6):
  select(): O(N) - 전체 FD 스캔
  poll(): O(N) - 유사
  epoll(): O(1) - 이벤트 기반 준비 통보

  epoll 메커니즘:
  - epoll_create(): 이벤트 큐 생성
  - epoll_ctl(): FD 등록/수정/삭제
  - epoll_wait(): 준비된 이벤트 블로킹 대기

  10,000 연결 중 100개 활성 → 100개만 처리

Nginx 아키텍처:
  마스터 프로세스 1개
  워커 프로세스 = CPU 코어 수 (예: 16개)
  각 워커: 이벤트 루프로 수천 연결 처리

  구성:
  worker_processes auto;  # CPU 코어 수
  events {
      worker_connections 1024;
      use epoll;
  }

  이론적 최대: 16 × 1024 = 16,384 동시 연결

Node.js libuv:
  V8 엔진 + libuv(이벤트 루프 라이브러리)
  epoll(Linux), kqueue(macOS), IOCP(Windows) 통합

  비동기 I/O:
  fs.readFile('data.json', (err, data) => {
      // I/O 완료 후 콜백 (블로킹 없음)
  });
```

> 📢 **섹션 요약 비유**: C10K = 동시 손님 1만 명 — 멀티프로세스 식당은 요리사 1만 명 고용(불가). Nginx/epoll은 "요청 완료" 알림 시스템으로 효율화. 알림 받은 것만 처리!

---

## 5. 실무 적용 및 판단

```
로드밸런서 (Load Balancer):
  다수의 서버에 요청 분산
  단일 장애 지점(SPOF) 제거

로드밸런싱 알고리즘:

라운드 로빈 (Round Robin):
  순서대로 서버에 배분
  1→2→3→1→2→3
  단순, 서버 성능 동일할 때 적합

가중 라운드 로빈 (Weighted RR):
  서버 성능에 따라 비율 조정
  A(4코어): 4배, B(2코어): 2배, C(2코어): 2배
  → A에 50%, B에 25%, C에 25%

최소 연결 (Least Connections):
  현재 연결 수가 가장 적은 서버에 배분
  처리 시간이 다른 요청에 효과적

IP 해시 (IP Hash):
  클라이언트 IP로 서버 고정
  세션 친화성(Session Affinity) 필요 시

헬스 체크 (Health Check):
  주기적으로 서버 상태 확인

  HTTP: GET /health → 200 OK (정상)
  TCP: 연결 시도 성공 여부

  이상 감지 시: 라우팅에서 제외 (자동)

L4 vs L7 로드밸런서:
  L4 (Transport): IP/Port 기반 (빠름, 내용 모름)
  L7 (Application): URL/헤더 기반 (느리지만 스마트)

  L7 예:
  /api/ → API 서버 클러스터
  /static/ → 파일 서버
  /admin/ → 관리 서버
```

> 📢 **섹션 요약 비유**: 로드밸런서 = 식당 안내 데스크 — 손님 오면 대기줄 짧은 테이블(최소 연결) 배정. 한 테이블 고장(헬스 체크 실패) 시 자동으로 다른 테이블 배정!

---

## 6. 기대효과 및 결론

```
월 10억 요청 처리 API 서버 아키텍처:

요구사항:
  RPS 피크: 50,000 req/s
  P99 응답시간: 50ms 이하
  가용성: 99.99% (연 52분 이하 다운)

아키텍처:

클라이언트 → CDN(CloudFront)
  → L7 로드밸런서(ALB) × 2
  → API 서버 클러스터 (20대)
  → 내부 L4 LB → DB 서버

API 서버 (Nginx + Node.js):
  Nginx:
  worker_processes 8;
  worker_connections 4096;
  upstream api_pool {
      server 127.0.0.1:3000 weight=1;
      server 127.0.0.1:3001 weight=1;
      ...
      keepalive 100;
  }

  Node.js PM2 클러스터:
  instances = CPU 코어 수
  → 각 인스턴스: 이벤트 루프로 I/O 처리

연결 풀:
  DB 연결 풀: 서버당 20연결 × 20대 = 400연결

  연결 생성 비용: ~20ms
  풀로 재사용 → ~1ms 이하

성능 결과:
  Nginx + epoll: 50,000 RPS 안정 처리
  P99: 23ms (목표 50ms 대비 여유)
  서버 1대 CPU: 45% (헤드룸 55%)

  쿠버네티스 HPA:
  CPU 70% 초과 시 자동 스케일아웃
  RPS 급증 → 20 → 40대 자동 확장
```

> 📢 **섹션 요약 비유**: 대규모 API 서버 = 패스트푸드 체인 본사 관리 — CDN(포장 완료품 배달), ALB(매장 안내), Nginx(주문 접수), Node.js(요리), DB 풀(식재료 창고). 자동 확장으로 피크도 안정!

---

## 7. 발전 흐름도

```
[클라이언트-서버 모델 (1960s)]
메인프레임 + 터미널
중앙 집중 처리
      |
      v
[인터넷 웹 서버 (1990s)]
Apache, IIS
멀티프로세스
      |
      v
[C10K 문제 제기 (1999)]
동시 연결 한계
      |
      v
[Nginx, epoll (2000s)]
이벤트 루프 대중화
C10K 해결
      |
      v
[마이크로서비스 (2010s~)]
N-Tier 분산
서비스 메시, K8s
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 클라이언트-서버 — Client-Server Architecture | 운영체제 자원 관리와 보호 정책이 실제로 적용되는 핵심 주제 |
| 커널 (Kernel) | 정책 집행, 상태 전이, 시스템 호출 처리의 중심 |
| 프로세스/스레드 | CPU, 메모리, 동기화 자원과 직접 연결되는 실행 단위 |
| 메모리/I/O | 성능 병목과 보호 요구사항이 함께 드러나는 연계 영역 |
| 가상화/보안 | 격리, 제어, 관측 확장 관점에서 해당 주제가 연결되는 상위 개념 |
