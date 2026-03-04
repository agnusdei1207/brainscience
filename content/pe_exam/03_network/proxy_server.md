+++
title = "프록시 서버 (Proxy Server)"
date = 2025-03-03

[extra]
categories = "pe_exam-03_network"
tags = ["프록시", "포워드프록시", "리버스프록시", "투명프록시", "캐싱", "익명성", "보안"]
+++

# 프록시 서버 (Proxy Server)

## 핵심 인사이트
> **클라이언트와 서버 사이에서 요청을 중계하는 서버**로, 포워드 프록시(Forward Proxy)와 리버스 프록시(Reverse Proxy)로 구분된다. 캐싱, 보안, 익명성, 로드 밸런싱 등 다양한 목적으로 활용되며, 최근에는 API 게이트웨이, Service Mesh의 핵심 구성요소로 진화하고 있다.

---

### I. 개요

**정의**: 프록시 서버(Proxy Server)는 **클라이언트와 서버 사이에서 요청을 중계하고 다양한 기능을 제공하는 서버**이다. 클라이언트의 요청을 대신 처리하거나, 서버의 응답을 대신 전달한다. 방향에 따라 포워드 프록시와 리버스 프록시로 구분된다.

> **직관적 비유**: 프록시 서버는 **"대리인"** 같아요. 중요한 문서를 직접 보내기 불안할 때 대리인이 대신 전달해 주고 받아오죠. 어떤 대리인은 내용을 미리 복사해둬 수도 있고(캐싱),, 어떤 대리인은 보내는 사람 신분을 숨겨줄 수도 있어요(익명성)!

**등장 배경** (3가지 이상):
1. **기존 한계 - 직접 연결의 제약**: 방화벽으로 인해 직접 연결이 차단되거나, 성능 최적화가 필요한 경우
2. **기술적 동인 - 보안 및 캐싱**: 악의 사이트 차단, 콘텐츠 캐싱으로 성능 향상 필요
3. **산업/시장 요구**: API 게이트웨이, 마이크로서비스 아키텍처 확산

**핵심 목적**: **접근 제어, 성능 최적화, 보안 강화, 익명성 보장**

---

### II. 필요성

#### 현황 및 문제점

| 문제 구분 | 구체적 내용 | 영향도 |
|----------|-----------|--------|
| **접근 제한** | 특정 사이트/서비스 접근 불가 | 서비스 이용 불가 |
| **성능 저하** | 원격 서버 응답 지연 | 사용자 경험 악화 |
| **보안 위협** | 직접 노출 시 공격 표면 증가 | 해킹 위험 |
| **추적 우려** | 모든 활동이 기록됨 | 개인정보 노출 |

#### 기술적 필요성

- **왜 지금인가**: 클라우드, 마이크로서비스 환경에서 필수
- **왜 이 기술인가**: 검증된 중계 서버 패턴
- **표준**: 없음 (다양한 구현)

#### 도입 시 기대 가치

| 가치 영역 | 기대 효과 | 비고 |
|----------|----------|------|
| 접근 제어 | 특정 리소스만 허용 | 보안 강화 |
| 성능 | 캐싱으로 응답 향상 | 대역폭 절감 |
| 익명성 | 클라이언트 신원 보호 | 프라이버시 |

---

### III. 구조와 원리

#### 구성 요소

| 구성 요소 | 역할 | 기술적 특징 | 직관적 비유 |
|----------|------|------------|------------|
| **포워드 프록시** | 내부→외부 중계 | 클라이언트 대신 요청 | 출장 대리인 |
| **리버스 프록시** | 외부→내부 중계 | 서버 앞단 배치 | 호텔 프론트 |
| **투명 프록시** | 사용자 인식 없음 | 자동 리다이렉트 | 숨은 대리인 |
| **캐싱 프록시** | 응답 저장 | TTL 기반 만료 | 복사기 |
| **익명성 프록시** | 신원 숨김 | IP 마스킹 | 가면 |

#### 구조 다이어그램

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    프록시 서버 유형 및 배치                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   [포워드 프록시 - Forward Proxy]                                       │
│                                                                         │
│   내부 네트워크                    프록시                    인터넷       │
│   ┌─────────────┐                ┌─────────┐             ┌─────────┐   │
│   │  클라이언트  │ ──요청──────→│ Forward │ ──요청────→│ Server  │   │
│   │  (내부 IP)  │ ←──응답──────│  Proxy  │ ←──응답────│ (외부)   │   │
│   └─────────────┘                └─────────┘             └─────────┘   │
│                                                                         │
│   용도:                                                               │
│   - 내부 사용자의 인터넷 접근 제어                                      │
│   - 웹 필터링 (악의 사이트 차단)                                        │
│   - 캐싱으로 대역폭 절감                                                │
│   - 사용자 익명성 보호                                                  │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   [리버스 프록시 - Reverse Proxy]                                       │
│                                                                         │
│   인터넷                    프록시                    내부 서버들           │
│   ┌─────────────┐                ┌─────────┐             ┌─────────┐   │
│   │  클라이언트  │ ──요청──────→│ Reverse │ ──요청────→│ Server1 │   │
│   │  (외부 IP)   │ ←──응답──────│  Proxy  │ ←──응답────│ Server2 │   │
│   └─────────────┘                └─────────┘             │ Server3 │   │
│                                                                         │
│   용도:                                                               │
│   - 외부 요청을 내부 서버로 라우팅                                       │
│   - 로드 밸런싱                                                         │
│   - SSL 종료 (TLS Termination)                                          │
│   - 캐싱 (Static/Dynamic)                                                │
│   - WAF (웹 방화벽)                                                       │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   [리버스 프록시 상세 구조]                                             │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                     Reverse Proxy (Nginx/HAProxy)                │   │
│   │                                                                 │   │
│   │  Client ──────▶ [SSL Termination] ──────▶ Backend              │   │
│   │                    ↓                                        │   │
│   │               [캐싱 레이어]                                    │   │
│   │                    ↓                                        │   │
│   │               [압축 (Gzip)]                                     │   │
│   │                    ↓                                        │   │
│   │               [라우팅]                                         │   │
│   │         /api/* → backend-api:8080                                │   │
│   │         /web/* → backend-web:80                                 │   │
│   │         /static/* → 캐시에서 직접 응답                            │   │
│   │                    ↓                                        │   │
│   │               [보안]                                           │   │
│   │         - Rate Limiting (요청 제한)                              │   │
│   │         - IP 차단                                            │   │
│   │         - WAF 규칙                                            │   │
│   │                                                                 │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                    프록시 체인 (Proxy Chain)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   클라이언트 → [프록시1] → [프록시2] → [프록시3] → 목적지                │
│                                                                         │
│   장점:                                                               │
│   - 다중 익명성 (각 프록시가 이전 IP만 앎아)                              │
│   - 우회 능력 (하나가 차단되어도 다른 경로)                              │
│                                                                         │
│   단점:                                                               │
│   - 지연 증가 (각 홉마다 추가 대기 시간)                                  │
│   - 신뢰성 저하 (하나라도 장애 시 연결 실패)                              │
│                                                                         │
│   예: TOR (The Onion Router)                                           │
│   클라이언트 → [노드1] → [노드2] → [노드3] → 웹사이트                    │
│   각 노드는 이전/다음 노드만 알 수 있음                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 동작 흐름
```
① 요청 수신 → 2 정책 확인 → 3 캐시 조회 → 4 [Hit] 응답 / [Miss] 상위 요청 → 5 응답 저장 → 6 클라이언트 응답
```

- **①**: 클라이언트로부터 요청 수신
- **②**: ACL, 필터링 규칙 확인
- **③**: 로컬 캐시에서 응답 검색
- **④**: 캐시에 있으면 즉시 응답, 없으면 상위 서버로 요청
- **⑤**: 응답을 캐시에 저장 (TTL 기반)
- **⑥**: 클라이언트에게 응답 전송

#### 핵심 알고리즘
```
[HTTP 프록시 요청 처리]

1. 클라이언트 요청 수신:
   GET http://example.com/page HTTP/1.1

2. URL 파싱:
   - 프로토콜: http
   - 호스트: example.com
   - 경로: /page

3. 캐시 키 생성:
   key = hash(method + url + vary_headers)

4. 캐시 조회:
   if cached and not expired:
       return cached_response

5. 상위 요청:
   - DNS 조회 (또는 hosts 파일)
   - TCP 연결
   - HTTP 요청 전송

6. 응답 처리:
   - Cache-Control 헤더 확인
   - TTL 계산
   - 캐시 저장
   - 클라이언트 응답

[캐시 TTL 계산]

TTL = min(expires - now, max-age, default_ttl)

우선순위:
1. Cache-Control: max-age=N
2. Expires: 날짜
3. Last-Modified: (now - last_modified) * 0.1
4. 기본값 (예: 1시간)

[로드 밸런싱 통합]

리버스 프록시 = 로드 밸런서 역할
- Round Robin, Least Connections 등
- Health Check
- 세션 유지
```

#### 코드 예시
```python
#!/usr/bin/env python3
"""
프록시 서버 구현
"""
import socket
import select
import threading
from dataclasses import dataclass
from typing import Optional, Dict, Tuple
from urllib.parse import urlparse
import time
import hashlib

# ============================================================
# 캐시 구조
# ============================================================

@dataclass
class CacheEntry:
    """캐시 항목"""
    response: bytes
    headers: Dict[str, str]
    created_at: float
    ttl: int
    size: int

    def is_expired(self) -> bool:
        return time.time() - self.created_at > self.ttl


class ProxyCache:
    """프록시 캐시"""

    def __init__(self, max_size: int = 100 * 1024 * 1024):  # 100MB
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self.current_size = 0
        self.hits = 0
        self.misses = 0

    def _make_key(self, method: str, url: str) -> str:
        """캐시 키 생성"""
        return hashlib.md5(f"{method}:{url}".encode()).hexdigest()

    def get(self, method: str, url: str) -> Optional[CacheEntry]:
        """캐시 조회"""
        key = self._make_key(method, url)
        entry = self.cache.get(key)

        if entry is None:
            self.misses += 1
            return None

        if entry.is_expired():
            self._remove(key)
            self.misses += 1
            return None

        self.hits += 1
        return entry

    def put(self, method: str, url: str, response: bytes,
            headers: Dict[str, str], ttl: int) -> None:
        """캐시 저장"""
        key = self._make_key(method, url)
        size = len(response)

        # 기존 항목 제거
        if key in self.cache:
            self._remove(key)

        # 공간 확보
        while self.current_size + size > self.max_size and self.cache:
            # LRU: 가장 오래된 항목 제거
            oldest_key = min(self.cache.keys(),
                           key=lambda k: self.cache[k].created_at)
            self._remove(oldest_key)

        entry = CacheEntry(
            response=response,
            headers=headers,
            created_at=time.time(),
            ttl=ttl,
            size=size
        )
        self.cache[key] = entry
        self.current_size += size

    def _remove(self, key: str) -> None:
        """항목 제거"""
        if key in self.cache:
            self.current_size -= self.cache[key].size
            del self.cache[key]

    def stats(self) -> Dict:
        """통계"""
        total = self.hits + self.misses
        hit_rate = self.hits / total * 100 if total > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f"{hit_rate:.1f}%",
            'size': f"{self.current_size / 1024 / 1024:.2f}MB",
            'entries': len(self.cache)
        }


# ============================================================
# 간단한 HTTP 프록시
# ============================================================

class SimpleHTTPProxy:
    """간단한 HTTP 포워드 프록시"""

    def __init__(self, host: str = '0.0.0.0', port: int = 8080,
                 enable_cache: bool = True):
        self.host = host
        self.port = port
        self.cache = ProxyCache() if enable_cache else None
        self.running = False
        self.blocked_domains = set()  # 차단 도메인

    def block_domain(self, domain: str) -> None:
        """도메인 차단"""
        self.blocked_domains.add(domain.lower())

    def is_blocked(self, host: str) -> bool:
        """차단 여부 확인"""
        host_lower = host.lower()
        return any(blocked in host_lower for blocked in self.blocked_domains)

    def start(self) -> None:
        """프록시 서버 시작"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(100)

        self.running = True
        print(f"프록시 서버 시작: {self.host}:{self.port}")

        while self.running:
            try:
                client_socket, addr = server_socket.accept()
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, addr)
                )
                thread.daemon = True
                thread.start()
            except Exception as e:
                if self.running:
                    print(f"수락 오류: {e}")

    def handle_client(self, client_socket: socket.socket,
                     addr: Tuple[str, int]) -> None:
        """클라이언트 요청 처리"""
        try:
            # 요청 수신
            request = self._recv_all(client_socket, timeout=5)
            if not request:
                return

            # 요청 파싱
            request_line = request.split(b'\r\n')[0].decode()
            method, url, version = request_line.split()

            # URL 파싱
            parsed = urlparse(url)

            # HTTP 프록시의 경우 URL이 전체 경로
            if parsed.scheme:
                host = parsed.hostname
                port = parsed.port or 80
                path = parsed.path or '/'
                if parsed.query:
                    path += f"?{parsed.query}"
            else:
                # CONNECT 메서드 (HTTPS)
                host, port = url.split(':')
                port = int(port)
                path = '/'

            # 차단 확인
            if self.is_blocked(host):
                self._send_blocked_response(client_socket)
                return

            # 캐시 조회 (GET만)
            if method == 'GET' and self.cache:
                cached = self.cache.get(method, url)
                if cached:
                    client_socket.sendall(cached.response)
                    return

            # 상위 서버로 요청 전달
            response = self._forward_request(
                host, port, method, path, request, parsed.scheme == 'https'
            )

            # 응답 전송
            client_socket.sendall(response)

            # 캐시 저장 (GET만, 캐시 가능한 응답만)
            if method == 'GET' and self.cache:
                ttl = self._get_cache_ttl(response)
                if ttl > 0:
                    self.cache.put(method, url, response, {}, ttl)

        except Exception as e:
            print(f"요청 처리 오류 ({addr}): {e}")
        finally:
            client_socket.close()

    def _forward_request(self, host: str, port: int, method: str,
                        path: str, request: bytes, is_https: bool) -> bytes:
        """상위 서버로 요청 전달"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.settimeout(10)

        try:
            server_socket.connect((host, port))

            # 요청 수정 (절대 URL → 상대 URL)
            request_lines = request.split(b'\r\n')
            request_lines[0] = f"{method} {path} HTTP/1.1".encode()
            modified_request = b'\r\n'.join(request_lines)

            server_socket.sendall(modified_request)
            return self._recv_all(server_socket, timeout=10)

        finally:
            server_socket.close()

    def _recv_all(self, sock: socket.socket, timeout: float = 5) -> bytes:
        """모든 데이터 수신"""
        sock.setblocking(False)
        data = b''
        end_time = time.time() + timeout

        while time.time() < end_time:
            try:
                ready = select.select([sock], [], [], 0.1)
                if ready[0]:
                    chunk = sock.recv(8192)
                    if not chunk:
                        break
                    data += chunk

                    # HTTP 응답 완료 확인
                    if b'\r\n\r\n' in data:
                        # Content-Length 확인
                        if b'Content-Length:' in data:
                            header_end = data.find(b'\r\n\r\n') + 4
                            headers = data[:header_end].decode(errors='ignore')
                            for line in headers.split('\r\n'):
                                if line.lower().startswith('content-length:'):
                                    content_length = int(line.split(':')[1].strip())
                                    if len(data) >= header_end + content_length:
                                        return data
                        else:
                            # Content-Length 없으면 헤더만으로 완료 간주
                            return data
            except BlockingIOError:
                continue

        return data

    def _get_cache_ttl(self, response: bytes) -> int:
        """응답의 캐시 TTL 계산"""
        # Cache-Control 확인
        if b'Cache-Control:' in response:
            cache_control = response.split(b'Cache-Control:')[1].split(b'\r\n')[0]
            if b'no-cache' in cache_control or b'no-store' in cache_control:
                return 0
            if b'max-age=' in cache_control:
                max_age = int(cache_control.split(b'max-age=')[1].split(b',')[0])
                return max_age

        # Expires 확인
        if b'Expires:' in response:
            # 실제로는 날짜 파싱 필요
            return 3600  # 기본 1시간

        return 0  # 캐시 안 함

    def _send_blocked_response(self, client_socket: socket.socket) -> None:
        """차단 응답 전송"""
        response = (
            b"HTTP/1.1 403 Forbidden\r\n"
            b"Content-Type: text/html\r\n"
            b"\r\n"
            b"<html><body><h1>Access Denied</h1></body></html>"
        )
        client_socket.sendall(response)

    def stop(self) -> None:
        """서버 중지"""
        self.running = False


# ============================================================
# 리버스 프록시
# ============================================================

class ReverseProxy:
    """리버스 프록시"""

    def __init__(self, host: str = '0.0.0.0', port: int = 80):
        self.host = host
        self.port = port
        self.backends: Dict[str, Tuple[str, int]] = {}  # path -> (ip, port)
        self.cache = ProxyCache()
        self.rate_limits: Dict[str, int] = {}  # IP -> 요청 수
        self.rate_limit_window = 60  # 초

    def add_backend(self, path_prefix: str, backend_host: str,
                   backend_port: int) -> None:
        """백엔드 서버 등록"""
        self.backends[path_prefix] = (backend_host, backend_port)

    def route(self, path: str) -> Optional[Tuple[str, int]]:
        """요청 라우팅"""
        for prefix, backend in self.backends.items():
                if path.startswith(prefix):
                    return backend
        return None

    def check_rate_limit(self, client_ip: str, limit: int = 100) -> bool:
        """요청 제한 확인"""
        key = f"{client_ip}:{int(time.time() / self.rate_limit_window)}"
        current = self.rate_limits.get(key, 0)

        if current >= limit:
            return False

        self.rate_limits[key] = current + 1
        return True

    def print_routes(self) -> None:
        """라우팅 테이블 출력"""
        print("\n[리버스 프록시 라우팅]")
        for prefix, (host, port) in self.backends.items():
            print(f"  {prefix} → {host}:{port}")


# ============================================================
# 데모
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("         프록시 서버 데모")
    print("=" * 60)

    # 캐시 테스트
    print("\n[캐시 테스트]")
    cache = ProxyCache(max_size=10*1024*1024)  # 10MB

    # 항목 추가
    for i in range(5):
        cache.put(
            "GET",
            f"http://example.com/page{i}",
            f"<html>Page {i}</html>".encode(),
            {},
            ttl=60
        )

    print(cache.stats())

    # 캐시 히트
    entry = cache.get("GET", "http://example.com/page0")
    print(f"\n캐시 히트: {entry.response.decode() if entry else 'Miss'}")

    # 리버스 프록시 라우팅 테스트
    print("\n[리버스 프록시 라우팅]")
    rp = ReverseProxy()
    rp.add_backend("/api", "10.0.0.1", 8080)
    rp.add_backend("/web", "10.0.0.2", 80)
    rp.add_backend("/static", "10.0.0.3", 80)
    rp.print_routes()

    # 라우팅 테스트
    test_paths = ["/api/users", "/web/index.html", "/static/logo.png", "/unknown"]
    for path in test_paths:
        backend = rp.route(path)
        if backend:
            print(f"  {path} → {backend[0]}:{backend[1]}")
        else:
            print(f"  {path} → 매칭 없음")
```

---

### IV. 비교 분석
#### 장단점
| 장점 | 단점 |
|------|------|
| **보안**: 간접 접근으로 공격 표면 감소 | **지연**: 추가 홉으로 응답 지연 |
| **캐싱**: 대역폭 절감, 성능 향상 | **복잡성**: 설정 관리 부담 |
| **익명성**: 클라이언트 IP 숨김 | **SPOF**: 프록시 장애 시 전체 장애 |
| **제어**: 접근 정책 적용 | **비용**: 추가 인프라 필요 |
| **유연성**: 로드 밸런싱, 라우팅 | **호환성**: 일부 프로토콜 미지원 |

#### 포워드 vs 리버스 프록시
| 비교 항목 | 포워드 프록시 | 리버스 프록시 |
|----------|--------------|--------------|
| **위치** | 내부 네트워크 | 서버 앞단 |
| **클라이언트** | 내부 사용자 | 외부 사용자 |
| **목적** | 인터넷 접근 제어 | 서버 보호, 로드밸런싱 |
| **보안** | 필터링, 익명성 | WAF, SSL 종료 |
| **캐싱** | 인터넷 응답 | 백엔드 응답 |
| **예** | Squid, 기업 프록시 | Nginx, HAProxy, Cloudflare |

---

### V. 실무 적용
#### 적용 시나리오
| 적용 분야 | 적용 방법 | 기대 효과 |
|----------|----------|----------|
| **웹 가속** | CDN 캐싱 프록시 | 응답 시간 50% 감소 |
| **API 게이트웨이** | 리버스 프록시 + 인증 | 마이크로서비스 보안 |
| **기업 보안** | 포워드 프록시 + 필터 | 악의 사이트 차단 |
| **로드 밸런싱** | 리버스 프록시 LB | 가용성 99.99% |

#### 실제 도입 사례
- **Cloudflare**: 글로벌 CDN + WAF + DDoS 방어
- **Nginx**: 리버스 프록시, 로드 밸런서, 캐시
- **Squid**: 기업 포워드 프록시, 캐싱
- **Envoy**: Service Mesh 사이드카 프록시

#### 도입 시 고려사항
| 관점 | 핵심 체크 항목 |
|------|--------------|
| **기술적** | 캐시 정책, 타임아웃, 버퍼 크기 |
| **운영적** | 로깅, 모니터링, 장애 조치 |
| **보안적** | IP 필터링, 인증, 암호화 |
| **경제적** | 대역폭 절감 vs 프록시 비용 |

#### 주의사항
- **SPOF**: 프록시 장애 시 전체 장애 → HA 구성 필수
- **캐시 일관성**: 업데이트된 콘텐츠 반영 지연 → TTL 적절 설정
- **보안**: 프록시 자체가 공격 대상 → WAF, DDoS 방어

---

### VI. 결론
#### 기대 효과
| 효과 영역 | 내용 | 정량 수치 |
|----------|------|----------|
| 성능 | 캐싱으로 응답 향상 | 대역폭 40% 절감 |
| 보안 | 간접 접근으로 공격 차단 | 공격 표면 90% 감소 |
| 제어 | 접근 정책 적용 | 미승인 접근 100% 차단 |

#### 미래 전망
1. **기술 발전**: Service Mesh 사이드카 프록시 확산
2. **시장 트렌드**: API 게이트웨이로 진화
3. **후속 기술**: eBPF 기반 프록시

> **결론**: 프록시 서버는 보안, 성능, 제어를 위한 핵심 인프라로, 포워드/리버스 선택과 캐시 정책이 핵심이다.

> **참고**: RFC 7230 (HTTP/1.1), RFC 7234 (HTTP Caching)

---

### 관련 개념
| 관련 개념 | 관계 유형 | 설명 | 링크 |
|----------|----------|------|------|
| 로드 밸런서 | 유사/확장 | 리버스 프록시가 LB 역할 | [로드 밸런싱](./load_balancing.md) |
| CDN | 확장 | 글로벌 분산 캐싱 프록시 | [CDN](../06_ict_convergence/network/cdn.md) |
| WAF | 통합 | 프록시 + 웹 방화벽 | [VPN/보안](./vpn_network_security.md) |
| NAT | 연관 | IP 주소 변환 | [IP 주소](./ip_addressing.md) |

---

## 쉬운 설명
프록시 서버는 **"대리인"** 같아요!

중요한 일을 하러 가는데, 내가 직접 가면 누군가 알아볼 수 있어요.

**대리인이 대신 가요**:
- 내용을 미리 알면 사본을 줘요 (캐싱)
- 위험한 곳은 안 가요 (필터링)
- 내가 누군지 몰라요 (익명성)

**포워드 프록시**:
- 회사에서 인터넷 할 때
- "야, 이 사이트는 위험해!" 하고 막아요
- "이 페이지는 지난번에 봤으니까 저장해둔 거 줄게!" (캐싱)

**리버스 프록시**:
- 웹사이트 앞에서 경비원 역할
- "손님, 1번 창구로 가세요!" 하고 안내해요
- "SSL 암호 여기서 풀게요!" (SSL 종료)

---

## 부록: 다각도 관점
### 관점 요약
| 관점 | 핵심 질문 | 한 줄 요약 |
|------|----------|----------|
| 이론가 | 캐시 교체 알고리즘은? | LRU가 표준 |
| 설계자 | 캐시 크기는 얼마로? | 사용 패턴 분석 후 결정 |
| 개발자 | HTTP 파싱은 어떻게? | 표준 라이브러리 활용 |
| 운영자 | 캐시 적중률 모니터링? | 80% 이상 목표 |
| 보안 전문가 | 프록시 자체 보안? | TLS, 인증, 로깅 |
| 비즈니스 | ROI는? | 대역폭 절감 vs 인프라 비용 |
| 역사가 | 프록시의 기원은? | 1990년대 웹 프록시 |

---

#### 이론가 관점
- **복잡도**: 캐시 조회 O(1), 라우팅 O(n) 또는 O(log n)
- **캐시 정책**: LRU, LFU, FIFO
- **한계**: 캐시 일관성 문제 (stale data)

---

#### 설계자 관점
| 설계 결정 | 선택한 것 | 포기한 것 | 이유 |
|----------|----------|----------|------|
| 캐시 크기 | 사용량의 10% | 더 크게 | 비용 vs 효과 |
| TTL | 1시간 | 더 김 | 신선도 vs 히트율 |
| HA | Active-Active | Active-Standby | 가용성 |

---

#### 개발자 관점
```nginx
# Nginx 리버스 프록시 설정
server {
    listen 80;

    location /api/ {
        proxy_pass http://backend-api:8080/;
        proxy_cache api_cache;
        proxy_cache_valid 200 1h;
    }

    location / {
        proxy_pass http://backend-web:80;
    }
}
```

---

#### 운영자 관점
| 장애 시나리오 | 원인 | 탐지 | 대응 |
|-------------|------|------|------|
| 캐시 오염 | 잘못된 응답 저장 | 콘텐츠 검증 | 캐시 무효화 |
| 과부하 | 요청 급증 | CPU/메모리 | 스케일 아웃 |
| 백엔드 장애 | 서버 다운 | Health Check | 우회 |

---

#### 보안 전문가 관점
| 위협 | 공격 | 대응 |
|------|------|------|
| 캐시 포이즈닝 | 악의적 응답 저장 | 캐시 검증 |
| IP 스푸핑 | 위조 IP | 신원 확인 |
| DDoS | 요청 폭주 | Rate Limiting |

---

#### 역사가 관점
```
1994 - CERN httpd 프록시 모듈
1996 - Squid 캐싱 프록시
1999 - Apache mod_proxy
2004 - Nginx 리버스 프록시
2010 - Cloudflare CDN
2016 - Envoy 서비스 메시
```
