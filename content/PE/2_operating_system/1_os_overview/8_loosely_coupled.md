+++
title = "약결합 시스템 (Loosely Coupled System) / 분산 시스템"
description = "네트워크로 연결된 독립 노드들로 구성된 약결합 분산 시스템의 아키텍처와 원리를 심층 분석합니다."
date = "2026-03-04"
[taxonomies]
tags = ["약결합", "분산시스템", "메시지전달", "클러스터", "클라우드"]
categories = ["studynotes-2_operating_system"]
+++

# 약결합 시스템 (Loosely Coupled System) / 분산 시스템

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 네트워크로 연결된 독립적인 컴퓨터 노드들이 메시지 전달(Message Passing)을 통해 협업하는 분산 컴퓨팅 아키텍처. 각 노드는 자신만의 CPU, 메모리, 운영체제를 가지며, 물리적으로 분산되어 있으면서 논리적으로 단일 시스템처럼 동작하는 투명성(Transparency)을 제공한다.
> 2. **가치**: 거의 무제한적인 확장성(수만~수백만 노드), 고가용성(부분 장애 시에도 서비스 지속), 지역적 분산(물리적 재해 대응), 이기종 시스템 통합(다양한 하드웨어/OS 혼용)을 실현. 클라우드 컴퓨팅, 인터넷, IoT의 기반 아키텍처.
> 3. **융합**: 마이크로서비스 아키텍처, 컨테이너 오케스트레이션(Kubernetes), 서버리스 컴퓨팅, 엣지 컴퓨팅 등 현대 클라우드 네이티브 기술의 근간. CAP 정리, 분산 합의(Raft, Paxos), 이벤트ual 일관성 등 분산 시스템 이론의 실제 적용.

---

### Ⅰ. 개요 (Context & Background)

#### 개념
약결합 시스템(Loosely Coupled System)은 **네트워크로 연결된 독립적인 컴퓨터 노드들이 메시지 전달 방식으로 통신하며, 각 노드가 자신만의 메모리와 운영체제를 가지고 독립적으로 작동하면서도, 사용자에게는 단일 시스템처럼 보이는 분산 컴퓨팅 아키텍처**를 의미한다. "약결합(Loosely Coupled)"이라는 명칭은 노드 간의 연결이 네트워크를 통해 이루어지며, 통신 지연이 상대적으로 크고(마이크로초~초), 각 노드가 상당한 독립성을 가진다는 점을 강조한다.

약결합 시스템의 핵심 특성:
1. **독립적 메모리(Private Memory)**: 각 노드가 자신만의 메모리 보유
2. **분산 주소 공간(Distributed Address Space)**: 노드마다 별도의 주소 공간
3. **메시지 전달 통신(Message Passing)**: 네트워크를 통한 데이터 교환
4. **다중 OS 인스턴스(Multiple OS Instances)**: 각 노드마다 독립적인 OS
5. **높은 장애 격리(High Fault Isolation)**: 한 노드 장애가 다른 노드에 직접 영향 없음

**약결합 시스템 = 분산 시스템 = 클러스터 시스템**: 본질적으로 동일한 개념.

#### 💡 비유
약결합 시스템을 **'이메일로 소통하는 글로벌 팀'**에 비유할 수 있다. 팀원들(노드)이 전 세계 여러 곳에 있고, 각자 자신의 책상(메모리)과 일정(OS)을 가진다. 서로 이메일(메시지)로만 소통하므로 즉시 답장을 받지 못할 수도 있지만, 한 팀원이 아파도(장애) 다른 팀원들은 계속 일할 수 있다. 또한 팀원을 언제든지 추가(확장)하거나 교체(복구)할 수 있다.

#### 등장 배경 및 발전 과정

**1. 문제 인식: 강결합 시스템의 한계**
- 강결합(SMP) 시스템은 32~64 CPU 수준에서 확장성 한계 도달.
- 단일 시스템 장애가 전체 서비스 중단으로 이어짐.
- 물리적 한 공간에 제약, 지역적 재해에 취약.

**2. 분산 시스템의 등장**
- 1970~80년대, ARPANET, Ethernet 기술 발전.
- 1980년대, Sun NFS, Andrew File System 등 분산 파일 시스템 등장.
- **핵심 혁신**: RPC(Remote Procedure Call), 분산 동기화, 분산 파일 시스템.

**3. 클러스터 컴퓨팅의 대중화**
- 1990년대, Beowulf 클러스터(리눅스 기반 저비용 클러스터) 등장.
- Google, Amazon 등 인터넷 기업이 상용 클러스터 구축.
- 고가용성(HA), 로드 밸런싱, HPC(고성능 컴퓨팅) 클러스터 보편화.

**4. 클라우드 컴퓨팅과 마이크로서비스**
- 2000년대 후반, Amazon EC2, Google App Engine 등 클라우드 서비스 등장.
- 2010년대, Docker, Kubernetes로 컨테이너 기반 분산 시스템 표준화.
- 마이크로서비스 아키텍처, 서버리스 컴퓨팅으로 진화.

---

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

#### 1. 구성 요소 (표)

| 요소명 | 상세 역할 | 내부 동작 메커니즘 | 관련 프로토콜/기술 | 비유 |
|:---|:---|:---|:---|:---|
| **노드 (Node)** | 독립적인 컴퓨팅 단위 | CPU, Memory, OS, Network Interface | Linux, Windows, Container | 글로벌 팀원 |
| **네트워크 (Network)** | 노드 간 통신 인프라 | 패킷 스위칭, 라우팅, 대역폭 관리 | TCP/IP, Ethernet, InfiniBand | 이메일 시스템 |
| **메시지 전달 (Message Passing)** | 노드 간 데이터 교환 | 직렬화, 전송, 역직렬화 | gRPC, REST, MQTT | 이메일 메시지 |
| **분산 파일 시스템 (Distributed File System)** | 데이터의 분산 저장 | 청크 분할, 복제, 일관성 관리 | HDFS, Ceph, GlusterFS | 공유 드라이브 |
| **분산 동기화 (Distributed Synchronization)** | 분산 환경에서의 순서 보장 | 분산 락, 합의 알고리즘, 벡터 시계 | ZooKeeper, etcd, Raft | 회의 일정 조율 |
| **분산 스케줄러 (Distributed Scheduler)** | 작업 분배 및 로드 밸런싱 | 작업 큐, 자원 할당, 장애 복구 | Kubernetes, Mesos, YARN | 프로젝트 매니저 |
| **서비스 디스커버리 (Service Discovery)** | 서비스 위치 파악 | 레지스트리, DNS, 헬스 체크 | Consul, Eureka, K8s Service | 연락처 |

#### 2. 정교한 구조 다이어그램

```text
+===========================================================================+
|              LOOSELY COUPLED DISTRIBUTED SYSTEM ARCHITECTURE              |
+===========================================================================+

   +-----------------------------------------------------------------------+
   |                         CLIENT LAYER                                   |
   |  +-----------+  +-----------+  +-----------+  +-----------+           |
   |  | Web       |  | Mobile    |  | Desktop   |  | IoT       |           |
   |  | Browser   |  | App       |  | Client    |  | Device    |           |
   |  +-----------+  +-----------+  +-----------+  +-----------+           |
   +-----------------------------------|-----------------------------------+
                                       | Internet/Load Balancer
   +-----------------------------------v-----------------------------------+
   |                         DISTRIBUTED SYSTEM                             |
   |                                                                       |
   |  +-----------------------+  +-----------------------+                 |
   |  |      NODE 1           |  |      NODE 2           |                 |
   |  | +-------------------+ |  | +-------------------+ |                 |
   |  | |  Application      | |  | |  Application      | |                 |
   |  | |  Service A        | |  | |  Service B        | |                 |
   |  | +-------------------+ |  | +-------------------+ |                 |
   |  | |  Local Memory     | |  | |  Local Memory     | |                 |
   |  | +-------------------+ |  | +-------------------+ |                 |
   |  | |  Local OS         | |  | |  Local OS         | |                 |
   |  | +--------+----------+ |  | +--------+----------+ |                 |
   |  +----------|------------+  +----------|------------+                 |
   |             |                          |                               |
   |             +-------------+------------+                               |
   |                           |                                            |
   |  +-----------------------+-----------------------+                     |
   |  |                    NETWORK                    |                     |
   |  |  +-------------+  +-------------+  +-------+ |                     |
   |  |  | Switch      |  | Router      |  | DNS   | |                     |
   |  |  +-------------+  +-------------+  +-------+ |                     |
   |  +----------------------------------------------+                     |
   |                           |                                            |
   |             +-------------+------------+                               |
   |             |                          |                               |
   |  +----------v------------+  +----------v------------+                 |
   |  |      NODE 3           |  |      NODE 4           |                 |
   |  | +-------------------+ |  | +-------------------+ |                 |
   |  | |  Application      | |  | |  Application      | |                 |
   |  | |  Service C        | |  | |  Service D        | |                 |
   |  | +-------------------+ |  | +-------------------+ |                 |
   |  | |  Local Memory     | |  | |  Local Memory     | |                 |
   |  | +-------------------+ |  | +-------------------+ |                 |
   |  | |  Local OS         | |  | |  Local OS         | |                 |
   |  | +-------------------+ |  | +-------------------+ |                 |
   |  +-----------------------+  +-----------------------+                 |
   |                                                                       |
   |  +-----------------------------------------------------------------+ |
   |  |                    DISTRIBUTED STORAGE                           | |
   |  |  +-------------+  +-------------+  +-------------+               | |
   |  |  | Storage     |  | Storage     |  | Storage     | (Replicated)  | |
   |  |  | Node 1      |  | Node 2      |  | Node 3      |               | |
   |  |  +-------------+  +-------------+  +-------------+               | |
   |  +-----------------------------------------------------------------+ |
   +-----------------------------------------------------------------------+

+===========================================================================+
|                    MESSAGE PASSING COMMUNICATION                          |
+===========================================================================+

   Node A (Sender)                       Node B (Receiver)
   +------------------+                  +------------------+
   | Application      |                  | Application      |
   | +-------------+  |                  | +-------------+  |
   | | Send(data)  |  |                  | | Receive()   |  |
   | +------+------+  |                  | +------+------+  |
   |        |         |                  |        ^         |
   +--------|---------+                  +--------|---------+
            |                                     |
   +--------v---------+                  +--------|---------+
   | Serialization    |                  | Deserialization  |
   | (JSON/Protobuf)  |                  | (JSON/Protobuf)  |
   +--------+---------+                  +--------+---------+
            |                                     ^
            |          Network Packet             |
            +-------------------------------------+
                   (TCP/IP, HTTP, gRPC)

   Latency: 0.1ms (LAN) ~ 100ms (WAN)
   Throughput: MB/s ~ GB/s (depends on network)
```

#### 3. 심층 동작 원리 (분산 시스템 RPC 호출 6단계)

**① 클라이언트 스텁 호출**
- 클라이언트 애플리케이션이 원격 프로시저 호출(예: `userService.getUser(123)`).
- 클라이언트 스텁(Stub/Proxy)이 호출을 가로챔.

**② 인자 직렬화 (Marshalling)**
- 스텁이 함수 인자(매개변수)를 네트워크 전송 가능한 바이트 스트림으로 변환.
- JSON, Protocol Buffers, Avro 등의 직렬화 포맷 사용.

**③ 네트워크 전송**
- 직렬화된 메시지가 네트워크 프로토콜(TCP/IP, HTTP/2)을 통해 서버로 전송.
- 지연 시간: LAN(0.1~1ms), WAN(10~200ms).

**④ 서버 스텁 수신 및 역직렬화**
- 서버 스텁이 메시지를 수신하고 역직렬화(Unmarshalling).
- 원래 함수 호출 형태로 복원.

**⑤ 실제 함수 실행**
- 서버에서 실제 함수(비즈니스 로직) 실행.
- 필요시 데이터베이스, 다른 서비스 호출.

**⑥ 응답 반환**
- 결과를 직렬화하여 클라이언트에 반환.
- 클라이언트 스텁이 역직렬화 후 애플리케이션에 결과 전달.

#### 4. 핵심 알고리즘 & 실무 코드 예시

**[분산 락(Distributed Lock) 구현 - Redis 기반]**

```python
"""
Distributed Lock Implementation using Redis
약결합 시스템에서 상호 배제를 위한 분산 락 구현

핵심 특성:
1. 상호 배제: 어느 시점에든 하나의 클라이언트만 락 보유
2. 교착 상태 방지: TTL(Time-To-Live)로 자동 해제
3. 가용성: Redis Sentinel/Cluster로 고가용성 보장
"""

import redis
import uuid
import time

class DistributedLock:
    def __init__(self, redis_client, lock_name, timeout=10):
        """
        Args:
            redis_client: Redis 클라이언트 인스턴스
            lock_name: 락의 이름 (공유 자원 식별자)
            timeout: 락의 자동 만료 시간 (초)
        """
        self.redis = redis_client
        self.lock_name = f"lock:{lock_name}"
        self.timeout = timeout
        self.identifier = str(uuid.uuid4())  # 고유 식별자
        
    def acquire(self, blocking=True, timeout=None):
        """
        분산 락 획득
        
        Args:
            blocking: 블로킹 여부
            timeout: 블로킹 대기 최대 시간 (초)
        
        Returns:
            bool: 락 획득 성공 여부
        """
        start_time = time.time()
        
        while True:
            # SETNX (SET if Not eXists) + TTL을 원자적으로 수행
            acquired = self.redis.set(
                self.lock_name, 
                self.identifier, 
                nx=True,      # 키가 없을 때만 설정
                ex=self.timeout  # 만료 시간 설정
            )
            
            if acquired:
                return True
            
            if not blocking:
                return False
            
            # 타임아웃 확인
            if timeout and (time.time() - start_time) > timeout:
                return False
            
            # 잠시 대기 후 재시도 (Exponential Backoff 권장)
            time.sleep(0.1)
    
    def release(self):
        """
        분산 락 해제
        Lua 스크립트를 사용하여 원자성 보장
        """
        # Lua 스크립트: 락이 자신의 것인지 확인 후 삭제
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        
        self.redis.eval(lua_script, 1, self.lock_name, self.identifier)
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

# 사용 예시
if __name__ == "__main__":
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    
    # 분산 락 사용 (Context Manager)
    with DistributedLock(redis_client, "inventory_update", timeout=30):
        # 크리티컬 섹션: 여러 노드에서 동시에 실행되면 안 되는 코드
        print("Processing inventory update...")
        # ... 비즈니스 로직 ...
        time.sleep(2)
        print("Inventory update completed!")
    
    # 또는 수동으로 획득/해제
    lock = DistributedLock(redis_client, "user_sync")
    if lock.acquire(blocking=True, timeout=5):
        try:
            # 크리티컬 섹션
            pass
        finally:
            lock.release()
```

---

### Ⅲ. 융합 비교 및 다각도 분석

#### 1. 약결합 시스템 토폴로지 비교

| 토폴로지 | 설명 | 장점 | 단점 | 사용 사례 |
|:---|:---|:---|:---|:---|
| **클라이언트-서버** | 중앙 서버에 요청 | 단순, 중앙 관리 | 서버 병목, SPOF | 웹 서비스 |
| **P2P (Peer-to-Peer)** | 모든 노드가 동등 | 확장성, 내구성 | 복잡성, 일관성 | BitTorrent, Blockchain |
| **계층형 (Hierarchical)** | 트리 구조 | 효율적 라우팅 | 루트 병목 | DNS, LDAP |
| **망형 (Mesh)** | 모든 노드 상호 연결 | 높은 가용성 | 복잡성, 비용 | 데이터센터 |
| **하이브리드** | 여러 토폴로지 혼합 | 유연성 | 설계 복잡 | 대규모 클라우드 |

#### 2. 분산 시스템 일관성 모델 비교

| 모델 | 보장 내용 | 지연 | 가용성 | 사용 사례 |
|:---|:---|:---|:---|:---|
| **강 일관성 (Strong)** | 모든 읽기가 최신 쓰기 반환 | 높음 | 낮음 | 금융, 재고 |
| **결과적 일관성 (Eventual)** | 시간 경과 시 일관성 달성 | 낮음 | 높음 | SNS, CDN |
| **인과적 일관성 (Causal)** | 인과 관계 있는 연산 순서 보장 | 중간 | 중간 | 협업 도구 |
| **세션 일관성 (Session)** | 세션 내에서 일관성 보장 | 낮음 | 높음 | 쇼핑몰 |

#### 3. CAP 정리 트레이드오프

```
                    CAP Theorem
                    
                         Consistency
                             /\
                            /  \
                           /    \
                          /  CA  \
                         / (RDBMS)\
                        /----------\
                       /     CP     \
                      /  (HBase,    \
                     /  ZooKeeper)  \
                    /----------------\
                   /        AP        \
                  / (Cassandra, DynamoDB)
                 /______________________\
            Availability   Partition Tolerance
```

---

### Ⅳ. 실무 적용 및 기술사적 판단

#### 시나리오 1: 대규모 이커머스의 마이크로서비스 아키텍처

**문제 상황**: 블랙 프라이데이 트래픽 대응을 위해 기존 모놀리식 시스템을 분산 마이크로서비스로 전환.

**기술사적 결단**:
1. **서비스 분해**: 주문, 결제, 재고, 사용자 서비스로 분리.
2. **메시지 큐 도입**: Kafka를 사용한 비동기 이벤트 기반 통신.
3. **서비스 디스커버리**: Consul/Kubernetes Service로 동적 서비스 발견.
4. **서킷 브레이커**: Hystoxy/Resilience4j로 장애 전파 방지.
5. **분산 추적**: Jaeger/Zipkin으로 요청 추적.

**성과**: 
- 가용성 99.5% -> 99.99% 향상
- 배포 주기 월 1회 -> 일 10회 단축
- 장애 복구 시간 2시간 -> 5분 단축

#### 시나리오 2: 글로벌 CDN 및 엣지 컴퓨팅

**문제 상황**: 전 세계 사용자의 지연 시간 최소화.

**기술사적 결단**:
1. **지역 분산**: 각 대륙별 엣지 노드 배치.
2. **결과적 일관성**: 콘텐츠는 결과적 일관성으로 복제.
3. **지능형 라우팅**: GeoDNS로 사용자를 가장 가까운 노드로 안내.

#### 주의사항 및 안티패턴

1. **분산 단일 장애점(Distributed SPOF)**: 서비스 디스커버리, 메시지 큐 등이 SPOF가 되지 않도록 클러스터링.

2. **네트워크 분할 대응 부재**: CAP 정리를 이해하고, 서비스 특성에 맞는 일관성 모델 선택.

3. **과도한 동기화**: 분산 락, 분산 트랜잭션 남용은 성능 저하. 가능한 비동기, 결과적 일관성 활용.

---

### Ⅴ. 기대효과 및 결론

#### 정량적/정성적 기대효과

| 지표 | 단일 시스템 | 약결합 클러스터 | 개선효과 |
|:---|:---|:---|:---|
| **확장성** | 제한적 (수십 CPU) | 무제한 (수만 노드) | 획기적 |
| **가용성** | 99% (SPOF) | 99.999% | +0.99%p |
| **지역 분산** | 불가능 | 가능 (글로벌) | 새로운 가치 |
| **통신 지연** | ~100ns (메모리) | ~100ms (네트워크) | - (단점) |
| **시스템 복잡도** | 낮음 | 매우 높음 | - (단점) |

#### 미래 전망

약결합 분산 시스템은 **"클라우드 네이티브"**와 **"엣지 컴퓨팅"**의 시대를 열었다. 주요 발전 방향:

1. **서버리스/Function-as-a-Service**: 인프라 관리 없이 함수 단위 실행.
2. **서비스 메시(Service Mesh)**: Istio, Linkerd로 마이크로서비스 통신 추상화.
3. **WebAssembly(WASM) on Edge**: 엣지에서 경량 샌드박스 실행.
4. **AI 기반 자동 스케일링**: 트래픽 예측 기반 선제적 스케일링.

#### 참고 표준/가이드

- **Twelve-Factor App**: 클라우드 네이티브 애플리케이션 설계 가이드
- **Google Site Reliability Engineering (SRE)**: 대규모 분산 시스템 운영 가이드
- **CAP Theorem (Eric Brewer)**: 분산 시스템 트레이드오프 이론

---

### 관련 개념 맵 (Knowledge Graph)

- [강결합 시스템](@/studynotes/2_operating_system/1_os_overview/7_tightly_coupled.md): 대조되는 아키텍처
- [클러스터 시스템](@/studynotes/2_operating_system/1_os_overview/45_cluster_system.md): 약결합의 구현 형태
- [RPC](@/studynotes/2_operating_system/2_process_thread/126_rpc.md): 원격 프로시저 호출
- [분산 파일 시스템](@/studynotes/2_operating_system/9_file_system/585_distributed_filesystem.md): HDFS, Ceph
- [메시지 전달 IPC](@/studynotes/2_operating_system/2_process_thread/119_message_passing.md): 통신 기법

---

### 어린이를 위한 3줄 비유 설명

1. 약결합 시스템은 **'이메일로 소통하는 글로벌 팀'**과 같아요. 팀원들(컴퓨터)이 전 세계 여러 나라에 있고, 각자 자신의 책상(메모리)과 일정(OS)을 가지고 있어요.

2. 서로 이메일(메시지)로만 소통하므로 **'바로 답장을 받지 못할 수도 있어요'**. 하지만 한 팀원이 아파도(장애) 다른 팀원들은 계속 일할 수 있고, 새 팀원을 언제든지 추가할 수도 있어요.

3. 이렇게 하면 **'팀을 무한히 키울 수 있고'**, 지진이나 홍수 같은 재해가 한 곳에서 나도 **'다른 곳의 팀원들이 일을 계속할 수 있어서'** 안전해요. 대신 이메일 답장을 기다려야 해서 조금 느릴 수 있답니다!
