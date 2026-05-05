+++
weight = 284
title = "284. OpenVPN — 오픈소스 SSL/TLS VPN"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: OpenVPN은 OpenSSL 라이브러리를 기반으로 TLS 세션 위에 자체 VPN 프로토콜을 구현한 오픈소스 솔루션으로, 플랫폼 독립성과 높은 설정 유연성이 핵심 강점이다.
> 2. **가치**: TCP 443 또는 UDP 1194 모두 사용 가능하고, 심층 패킷 검사(DPI: Deep Packet Inspection) 우회를 위해 obfsproxy 등 난독화 플러그인을 결합할 수 있어 엄격한 방화벽 환경에서도 동작한다.
> 3. **판단 포인트**: TUN(Layer 3 IP 터널)과 TAP(Layer 2 이더넷 터널) 인터페이스를 선택할 수 있어, 단순 IP 라우팅에는 TUN을, 브리징·비IP 프로토콜 지원에는 TAP을 사용하는 설계 판단이 중요하다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

OpenVPN은 James Yonan이 2001년 오픈소스로 개발한 VPN 솔루션이다. GPLv2 라이선스로 공개되어 전 세계에서 널리 사용되며, 커뮤니티 에디션과 상용 Access Server 에디션이 존재한다. 핵심 기술 스택은 OpenSSL로, TLS 1.2/1.3 기반의 강력한 암호화와 PKI (Public Key Infrastructure) 인증을 지원한다.

IPsec 기반 VPN은 OS 커널 수준의 구현이 필요하고 플랫폼별 차이가 커서 설정이 복잡하다. 반면 OpenVPN은 사용자 공간(userspace)에서 동작하여 커널 패치 없이 Linux, Windows, macOS, Android, iOS 모두에서 동일한 설정 파일(.ovpn)로 동작한다. 이 단일 설정 파일 방식은 배포와 관리를 크게 단순화한다.

OpenVPN의 또 다른 강점은 포트 443을 TCP 모드로 사용할 수 있다는 것이다. 이를 통해 HTTPS 트래픽으로 위장할 수 있어 엄격한 기업 방화벽이나 국가 방화벽(Great Firewall) 환경에서도 접속이 가능하다.

📢 **섹션 요약 비유**: OpenVPN은 "어떤 언어도 통역할 수 있는 만능 통역사"와 같다. 영어(Windows), 한국어(Linux), 중국어(Android) 모두 같은 매뉴얼(ovpn 파일)로 대화할 수 있고, 심지어 검열관(방화벽)도 속일 수 있다.

---

## 2. 구성요소

### TUN vs TAP 인터페이스

```
[TUN 모드 - Layer 3]                    [TAP 모드 - Layer 2]
                                         
클라이언트 (tun0: 10.8.0.2)             클라이언트 (tap0: MAC + 10.8.0.2)
     |  IP 패킷만 전달                        |  이더넷 프레임 전달
     |  ARP 브로드캐스트 불가                 |  ARP, 브로드캐스트 가능
     |                                        |
OpenVPN TLS 터널                         OpenVPN TLS 터널
     |                                        |
서버 (tun0: 10.8.0.1)                   서버 (tap0: 브리지)
     |  라우팅으로 내부망 연결                |  브리지로 LAN 확장
     |                                        |
  [내부 라우터]                           [내부 L2 스위치]
```

### 패킷 처리 흐름 (UDP 모드)

```
애플리케이션
    |
OS 네트워킹 스택
    |  IP 패킷 → tun0 인터페이스 진입
    v
OpenVPN 프로세스 (userspace)
    |  1. LZO/LZ4 압축 (선택)
    |  2. AES-256-GCM 암호화 (TLS 세션 키 사용)
    |  3. HMAC/GCM 태그 추가
    v
UDP 또는 TCP 소켓 전송
    |  UDP 1194 또는 TCP 443
    v
인터넷 → 원격 OpenVPN 서버
```

### 핵심 설정 파라미터

| 파라미터 | 권장값 | 설명 |
|:---|:---|:---|
| proto | udp (성능) / tcp (방화벽 우회) | 전송 프로토콜 |
| port | 1194 (기본) / 443 (우회) | 사용 포트 |
| dev | tun (L3) / tap (L2) | 가상 인터페이스 유형 |
| cipher | AES-256-GCM | 암호화 알고리즘 |
| tls-version-min | 1.2 (최소) | TLS 최소 버전 |
| tls-crypt | 키 파일 | HMAC 사전 인증 (DoS 방지) |
| auth | SHA256 | HMAC 알고리즘 |
| compress | lz4-v2 | 압축 (선택) |
| --tls-auth | ta.key | TLS HMAC 방화벽 |

📢 **섹션 요약 비유**: TUN/TAP 선택은 "도로 건설 방식 선택"이다. TUN은 고속도로(IP 패킷만 통과), TAP은 도시 내 도로(자전거, 오토바이, 차 모두 통과). 목적지가 멀면 고속도로, 동네 구석구석이 필요하면 도시 도로.

---

## 3. 구조 및 동작 원리

| 항목 | OpenVPN | IPsec/IKEv2 | WireGuard |
|:---|:---|:---|:---|
| 코드 라인 수 | ~70,000 | OS 내장 (수십만) | ~4,000 |
| 동작 영역 | 사용자 공간 | 커널 공간 | 커널 공간 |
| 암호화 | TLS (OpenSSL) | IPsec/IKE | ChaCha20-Poly1305 |
| 인증 | PKI/인증서, PSK | PKI, EAP, PSK | 공개키(Curve25519) |
| 포트 | UDP 1194 / TCP 443 | UDP 500/4500 | UDP (임의) |
| 방화벽 우회 | ✅ TCP 443 가능 | △ UDP 필요 | △ UDP 고정 |
| 성능 | 낮음 (userspace) | 높음 (kernel) | 매우 높음 (kernel) |
| 설정 복잡도 | 높음 | 매우 높음 | 낮음 |
| 오픈소스 | ✅ | ✅ (구현체 다양) | ✅ |
| OS 내장 | ❌ | ✅ | 일부 (Linux 5.6+) |

📢 **섹션 요약 비유**: OpenVPN은 "맞춤 제작 양복"이다. 원하는 대로 만들 수 있지만 맞추는 데 시간이 걸리고 비용이 높다. WireGuard는 "기성복 중 최고급 라인"으로 빠르고 깔끔하지만 커스텀이 제한적이다.

---

## 4. 비교 및 트레이드오프

**PKI 기반 설정 절차:**

```
1. CA (Certificate Authority) 생성
   easyrsa init-pki && easyrsa build-ca

2. 서버 인증서 발급
   easyrsa gen-req server nopass
   easyrsa sign-req server server

3. 클라이언트 인증서 발급 (사용자별)
   easyrsa gen-req client1 nopass
   easyrsa sign-req client client1

4. DH (Diffie-Hellman) 파라미터 생성
   easyrsa gen-dh

5. TLS-Auth/TLS-Crypt 키 생성
   openvpn --genkey tls-crypt ta.key
```

**성능 최적화 포인트:**

1. **UDP 모드 사용**: TCP 위에 TCP(TCP-in-TCP)는 재전송 충돌로 성능 저하. 방화벽 우회가 필요 없으면 UDP 1194 사용.

2. **압축 비활성화**: TLS 1.3 환경에서 CRIME/BREACH 취약점 우려로 압축 기본 비활성화 권장. 이미 TLS가 암호화하므로 압축 효과도 미미.

3. **멀티스레딩**: OpenVPN은 기본 단일 스레드. 높은 처리량이 필요하면 여러 프로세스를 다른 포트로 실행하고 로드 밸런서로 분산.

4. **tls-crypt 적용**: TLS 핸드셰이크 전에 HMAC으로 패킷을 사전 인증해 인증되지 않은 TLS 핸드셰이크를 차단. DoS 공격 표면 감소.

📢 **섹션 요약 비유**: OpenVPN PKI 설정은 "여권 발급 시스템 구축"과 같다. 국가(CA)가 있고, 그 국가가 발행한 여권(인증서)만 입국(VPN 접속)을 허용한다. 여권 없이는 아무도 들어올 수 없다.

---

## 5. 실무 적용 및 최적화 기법

OpenVPN은 20년 이상 검증된 안정성, 광범위한 플랫폼 지원, 높은 설정 유연성으로 여전히 수많은 기업과 서비스에서 사용된다. 특히 엄격한 방화벽 환경에서의 TCP 443 동작과 다양한 플러그인 생태계는 대체 불가능한 사용 사례를 만든다.

다만 userspace 구현에 따른 성능 한계와 설정 복잡도는 명확한 단점이다. 신규 설계에서는 WireGuard나 IKEv2를 우선 검토하고, 플랫폼 호환성·방화벽 우회가 핵심 요구사항인 경우에만 OpenVPN을 선택하는 것이 기술사의 올바른 판단이다.

📢 **섹션 요약 비유**: OpenVPN은 "만능 스위스 아미 나이프"다. 다양한 도구(설정 옵션)가 있어서 어떤 상황에서도 쓸 수 있지만, 전문 공구(WireGuard, IPsec)보다 각 분야에서 성능이 낮을 수 있다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| OpenSSL | 기반 라이브러리 | TLS 암호화 및 인증서 처리 |
| TUN/TAP | 가상 인터페이스 | L3/L2 터널링 모드 선택 |
| PKI / easyrsa | 인증 인프라 | 인증서 발급 및 관리 |
| tls-crypt | DoS 방어 | 사전 인증으로 미인가 핸드셰이크 차단 |
| WireGuard | 현대적 대안 | 성능 중심 설계의 경량 VPN |
| obfsproxy | 난독화 플러그인 | DPI 우회를 위한 트래픽 위장 |

### 👶 어린이를 위한 3줄 비유 설명
1. OpenVPN은 마치 어떤 나라에서든 사용할 수 있는 만능 번역기처럼, 윈도우·맥·리눅스·폰 모두에서 같은 설정 파일로 작동해.
2. 방화벽이 문을 막아도, 443번 문(포트)은 대부분 HTTPS로 열려 있어서 그 문으로 몰래 들어갈 수 있어.
3. 직접 도로를 놓는 것처럼(userspace) 자유롭게 설정할 수 있지만, 정부가 미리 만들어 놓은 고속도로(kernel VPN)보다는 조금 느려.
