+++
title = "HTTP Flood"
date = "2025-05-15"
weight = 257
[extra]
categories = ["security", "network-security"]
+++
## 0. 핵심 인사이트

> **핵심**: (개념 본질)
> **비유**: (개념 비유)

> 📝 모범 답안

- **L7 계층 공격**: TCP 연결 성립 후, 서버 자원을 소모시키기 위해 대량의 HTTP GET/POST 요청을 전송하는 서비스 거부 공격임.
- **정상 요청 위장**: 봇넷(Botnet)을 활용하여 정상적인 브라우저 요청처럼 위장하므로 단순 패킷 필터링으로는 방어가 매우 어려움.
- **서버 자원 고갈**: 대량의 페이지 렌더링이나 DB 쿼리를 유발하여 웹 서버의 CPU, 메모리, 커넥션 풀(Connection Pool)을 고갈시킴.

### 1. 개요 및 필요성
HTTP Flood는 애플리케이션 계층(Layer 7)에서 발생하는 대표적인 DDoS 공격이다. 과거의 네트워크 대역폭 점유형 공격(Volumetric Attack)과 달리, 정상적인 서비스 흐름을 모방하면서 서버의 로직 처리 능력을 마비시키는 데 집중한다. 공격자는 최소한의 자원으로 서버에 최대의 부하를 줄 수 있어 가성비가 매우 높은 공격 기법으로 평가받는다.

### 2. 구성요소
HTTP Flood는 크게 GET Flood와 POST Flood로 나뉜다. 공격자는 봇넷을 통해 좀비 PC들이 특정 URL로 무한히 요청을 보내게 한다.

```text
[ HTTP Flood Attack Mechanism - HTTP Flood 공격 메커니즘 ]

   [ Attacker ]
        | (Command)
        v
   [ Botnet / Zombie PCs ]
        |
        | (Massive HTTP GET/POST Requests)
        | "GET /search?q=very_heavy_query HTTP/1.1"
        v
+-----------------------+
|      Web Server       |
|  (Resource Exhaust)   | <--- Connection Full / CPU High
+-----------------------+
        |
        +-- (DB Server) -- Query Overload
```

**공격 유형:**
1. **GET Flood**: 정적/동적 페이지를 반복 요청하여 웹 서버와 WAS의 처리 한계를 초과시킴.
2. **POST Flood**: 폼(Form) 데이터 제출이나 파일 업로드를 유발하여 DB 쓰기 부하 및 세션 처리를 가중시킴.
3. **Cache-Control 활용**: `no-cache`, `max-age=0` 헤더를 포함하여 프록시 서버의 캐시를 우회하고 항상 원본 서버(Origin)에 부하를 전달함.

### 3. 구조 및 동작 원리
| 비교 항목 | HTTP Flood (L7) | SYN Flood (L4) |
| :--- | :--- | :--- |
| **공격 지점** | HTTP 애플리케이션 핸들러 | TCP 프로토콜 스택 |
| **자원 소모** | CPU, Memory, DB Thread | TCP Backlog Queue |
| **탐지 난이도** | 매우 높음 (정상 트래픽과 유사) | 보통 (Half-open 연결 감시) |
| **주요 방어** | WAF, CAPTCHA, 행동 분석 | SYN Cookie, 가속 하드웨어 |

### 4. 비교 및 트레이드오프
- **임계치 설정(Throttling)**: 단일 IP당 초당 요청 수(RPS)를 제한하는 것이 기본이나, 분산 봇넷 환경에서는 한계가 있다.
- **기술사적 판단**: 단순 IP 차단을 넘어, 브라우저 지문(Fingerprinting) 확인, 자바스크립트 챌린지 주입, 또는 CDNs(Cloudflare, Akamai)의 스크러빙 센터(Scrubbing Center)를 통한 전역적 방어 전략이 필수적이다.

### 5. 실무 적용 및 최적화 기법
클라우드 네이티브 환경이 확산되면서 오토 스케일링(Auto-scaling)을 역이용하여 클라우드 비용을 폭증시키는 '경제적 서비스 거부(EDoS)' 공격으로 진화하고 있다. 따라서 가시성(Visibility) 확보와 지능형 행위 분석(AI-based Detection)을 결합한 다층 방어 체계 구축이 향후 보안 표준의 핵심이 될 것이다.

### 📌 관련 개념 맵 (Knowledge Graph)
- **상위**: 서비스 거부 공격 (DDoS), 애플리케이션 보안
- **하위**: GET Flood, POST Flood, EDoS
- **연관**: WAF, 봇넷, Slowloris, 스크러빙 센터

### 👶 어린이를 위한 3줄 비유 설명
1. 맛집 식당에 수만 명의 가짜 손님이 몰려가서 "메뉴판 보여주세요!"라고만 계속 말하는 거예요.
2. 진짜 밥을 먹으러 온 손님들은 자리가 없어서 들어가지도 못하고 기다리게 되죠.
3. 식당 주인은 누가 진짜 배고픈 손님이고 누가 방해꾼인지 구별하기가 너무 힘든 상황이랍니다.
