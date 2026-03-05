+++
title = "680. SSL/TLS (Secure Sockets Layer / Transport Layer Security)"
description = "SSL/TLS 보안 프로토콜의 핸드셰이크, 암호화 스위트, 인증서 체계, 최신 보안 기법을 심도 있게 분석합니다."
date = "2026-03-05"
[taxonomies]
tags = ["SSL", "TLS", "HTTPS", "Certificate", "PKI", "Encryption", "Handshake", "X.509"]
categories = ["studynotes-3_network"]
+++

# 680. SSL/TLS (Secure Sockets Layer / Transport Layer Security)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: TLS는 전송 계층 위에서 동작하는 보안 프로토콜로, 핸드셰이크를 통한 인증서 기반 상호 인증, 키 교환, 암호화 통신을 통해 기밀성(Confidentiality), 무결성(Integrity), 인증(Authentication)을 보장합니다.
> 2. **가치**: TLS 1.3은 1-RTT 핸드셰이크로 연결 설정 지연을 50% 단축하고, 0-RTT로 재연결 시 즉시 데이터 전송이 가능하며, PFS(Perfect Forward Secrecy)로 장기간 키 노출에도 과거 세션 보호가 가능합니다.
> 3. **융합**: QUIC 프로토콜 내에 TLS 1.3이 내장되어 HTTP/3의 보안 기반을 제공하며, mTLS(Mutual TLS)는 Zero Trust 아키텍처와 서비스 메시의 핵심 인증 메커니즘이 됩니다.

---

## Ⅰ. 개요 (Context & Background)

SSL/TLS는 인터넷 통신의 보안을 위한 사실상 표준(de facto standard) 프로토콜입니다. Netscape가 1995년 SSL 2.0을 발표한 이후, IETF가 TLS 1.0(1999), TLS 1.2(2008), TLS 1.3(2018)으로 발전시켰습니다. 현재 모든 HTTPS 통신, 이메일 보안(SMTPS, IMAPS), VPN 등에서 사용됩니다.

**💡 비유**: TLS를 **'외교관 여권 시스템'**에 비유할 수 있습니다.
- **인증서(Certificate)**는 **여권**입니다. 신뢰할 수 있는 기관(정부/CA)이 발급하고, 소유자의 신원을 증명합니다.
- **CA(Certificate Authority)**는 **여권 발급 기관**입니다. VeriSign, DigiCert, Let's Encrypt 등이 있습니다.
- **핸드셰이크**는 **입국 심사**입니다. 여권을 확인하고, 암호화된 통신 채널을 설정합니다.
- **세션 키**는 **외교 암호**입니다. 두 나라만 아는 비밀 코드로 대화를 나눕니다.

**등장 배경 및 발전 과정**:
1. **암호화되지 않은 HTTP의 위험 (1990년대 초)**: 신용카드 번호, 비밀번호가 평문으로 전송되어 도청 위험이 컸습니다.
2. **SSL 탄생 (1995년)**: Netscape가 e-Commerce를 위해 SSL 2.0을 개발했습니다. 곧 보안 취약점이 발견되어 SSL 3.0으로 개선했습니다.
3. **TLS로의 전환 (1999년)**: IETF가 SSL 3.0을 표준화하여 TLS 1.0(RFC 2246)을 발표했습니다.
4. **TLS 1.2와 현대 암호 (2008년)**: SHA-256, AES-GCM, ECDHE 등 현대적 암호 알고리즘을 지원했습니다.
5. **TLS 1.3 혁신 (2018년)**: 레거시 알고리즘 제거, 1-RTT 핸드셰이크, 0-RTT 재개, 필수 PFS 등 획기적 개선이 이루어졌습니다.

---

## Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

### TLS 프로토콜 스택 구조

| 계층 | 프로토콜 | 역할 |
|------|----------|------|
| **응용 계층** | HTTP, SMTP, IMAP | 애플리케이션 데이터 |
| **TLS Handshake** | TLS 1.2/1.3 | 인증, 키 교환, 암호 스위트 협상 |
| **TLS Record** | TLS 1.2/1.3 | 데이터 분할, 암호화, MAC, 전송 |
| **전송 계층** | TCP | 신뢰성 있는 바이트 스트림 |

### TLS 핸드셰이크 상세 (TLS 1.3)

| 단계 | 메시지 | 방향 | 내용 |
|------|--------|------|------|
| 1 | ClientHello | C→S | 지원 암호 스위트, 키 공유(ECDHE), SNI |
| 2 | ServerHello | S→C | 선택 암호 스위트, 키 공유, 인증서 |
| 3 | Certificate | S→C | 서버 인증서 체인 |
| 4 | CertificateVerify | S→C | 인증서 서명 증명 |
| 5 | Finished | S→C | 핸드셰이크 완료 (암호화됨) |
| 6 | Finished | C→S | 핸드셰이크 완료 (암호화됨) |
| - | **Application Data** | 양방향 | 암호화된 데이터 통신 |

### Cipher Suite 구조 분석

```
TLS_AES_256_GCM_SHA384
│    │     │   │
│    │     │   └── PRF/해시 함수 (SHA-384)
│    │     └────── AEAD 암호화 모드 (GCM)
│     └──────────── 대칭키 암호 (AES-256)
└────────────────── 프로토콜 (TLS)
```

| Cipher Suite 요소 | TLS 1.2 | TLS 1.3 |
|------------------|---------|---------|
| **키 교환** | RSA, DHE, ECDHE | ECDHE, DHE만 (PFS 필수) |
| **인증** | RSA, ECDSA | RSA, ECDSA |
| **대칭 암호** | AES, 3DES, RC4 | AES, ChaCha20 |
| **AEAD 모드** | GCM, CBC+HMAC | GCM, CCM, Poly1305 |
| **해시** | SHA-1, SHA-256, SHA-384 | SHA-256, SHA-384 |

### 정교한 구조 다이어그램: TLS 1.3 핸드셰이크

```ascii
================================================================================
[ TLS 1.3 Full Handshake (1-RTT) ]
================================================================================

Client                                                Server

    +------------------+                               +------------------+
    | ClientHello      |                               |                  |
    | - TLS 1.3        |                               |                  |
    | - Cipher Suites  |                               |                  |
    | - Key Share      |  -------- (1-RTT) -------->   |                  |
    |   (ECDHE PubKey) |                               |                  |
    | - SNI            |                               |                  |
    +------------------+                               +------------------+
                                                       | ServerHello      |
                                                       | - Selected Cipher|
                                                       | - Key Share      |
                                                       +------------------+
                                                       | EncryptedExtensions
                                                       +------------------+
                                                       | Certificate      |
                                                       +------------------+
                                                       | CertificateVerify|
                                                       +------------------+
                                                       | Finished         |
                               <-------- (1-RTT) ----- +------------------+
    +------------------+
    | Finished         |                               | [암호화된 통신 시작]
    +------------------+                               |
    ------------------> |                               |
                       |                               |
    [암호화된 통신 시작] |                               |
    +------------------+                               +------------------+
    | Application Data | <====== Encrypted Data =====> | Application Data |
    +------------------+                               +------------------+

================================================================================
[ TLS 1.3 0-RTT (Session Resumption) ]
================================================================================

Client                                                Server

    +------------------+
    | ClientHello      |
    | + Key Share      |
    | + Pre-Shared Key |
    | + Early Data     |  -------- 0-RTT --------->    | Application Data |
    |                  |                               | (즉시 처리)       |
    | Application Data |                               +------------------+
    | (암호화됨)        |                               | ServerHello      |
    +------------------+                               | + Key Share      |
                                                       | + Finished       |
                               <-------- 1-RTT ------- +------------------+
    +------------------+
    | Finished         |
    +------------------+
    [정식 암호화 통신]

================================================================================
[ X.509 Certificate Chain ]
================================================================================

          [ Root CA ] (자체 서명)
              |
              | 서명
              v
        [ Intermediate CA ]
              |
              | 서명
              v
    +---------------------+
    |   Server Certificate |
    |---------------------|
    | Version: v3          |
    | Serial Number        |
    | Issuer: Intermediate |
    | Subject: example.com |
    | Validity: Not Before |
    |           Not After  |
    | Public Key: RSA-2048 |
    | Signature: SHA256RSA |
    | Extensions:          |
    |   - SAN (DNS names)  |
    |   - Key Usage        |
    |   - Extended Key Use |
    +---------------------+

검증 경로:
  Server Cert → Intermediate CA → Root CA (Trust Store에 저장)
```

### 심층 동작 원리: ECDHE 키 교환

**Elliptic Curve Diffie-Hellman Ephemeral (ECDHE)**:

```
1. Client가 타원 곡선 상의 점 G에서 임의의 비밀값 a 선택
2. ClientHello에 공개값 A = a*G 포함하여 전송

3. Server가 타원 곡선 상의 점 G에서 임의의 비밀값 b 선택
4. ServerHello에 공개값 B = b*G 포함하여 전송

5. 양측이 공유 비밀키 계산:
   Client: S = a*B = a*(b*G) = (a*b)*G
   Server: S = b*A = b*(a*G) = (a*b)*G

6. S에서 HKDF를 통해 세션 키 유도:
   - Client Write Key, Server Write Key
   - Client IV, Server IV
```

### 핵심 코드: TLS 연결 분석 (Python)

```python
import ssl
import socket
from dataclasses import dataclass
from typing import List, Optional, Dict
import datetime

@dataclass
class CertificateInfo:
    """인증서 정보 데이터 클래스"""
    subject: Dict[str, str]
    issuer: Dict[str, str]
    version: int
    serial_number: int
    not_before: datetime.datetime
    not_after: datetime.datetime
    signature_algorithm: str
    public_key_type: str
    public_key_size: int
    san: List[str]  # Subject Alternative Names
    is_valid: bool
    days_until_expiry: int


class TLSAnalyzer:
    """
    TLS 연결 분석기
    인증서 정보, 암호 스위트, 프로토콜 버전 분석
    """

    def __init__(self, hostname: str, port: int = 443):
        self.hostname = hostname
        self.port = port
        self.context: Optional[ssl.SSLContext] = None
        self.socket: Optional[ssl.SSLSocket] = None

    def connect(self) -> bool:
        """TLS 연결 수립"""
        try:
            # SSL 컨텍스트 생성 (TLS 1.2+ 강제)
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            self.context.minimum_version = ssl.TLSVersion.TLSv1_2
            self.context.check_hostname = True
            self.context.verify_mode = ssl.CERT_REQUIRED

            # 시스템 기본 CA 사용
            self.context.load_default_certs()

            # 소켓 생성 및 TLS 핸드셰이크
            raw_socket = socket.create_connection(
                (self.hostname, self.port),
                timeout=10
            )

            self.socket = self.context.wrap_socket(
                raw_socket,
                server_hostname=self.hostname
            )

            return True

        except ssl.SSLCertVerificationError as e:
            print(f"[TLS] 인증서 검증 실패: {e}")
            return False
        except Exception as e:
            print(f"[TLS] 연결 실패: {e}")
            return False

    def get_protocol_info(self) -> Dict[str, str]:
        """프로토콜 및 암호 스위트 정보"""
        if not self.socket:
            return {}

        return {
            'protocol_version': self.socket.version(),
            'cipher_suite': self.socket.cipher()[0],
            'cipher_bits': self.socket.cipher()[1],
            'cipher_protocol': self.socket.cipher()[2]
        }

    def get_certificate_info(self) -> Optional[CertificateInfo]:
        """인증서 상세 정보 추출"""
        if not self.socket:
            return None

        try:
            # PEM 형식 인증서 가져오기
            cert_der = self.socket.getpeercert(binary_form=True)
            cert_dict = self.socket.getpeercert()

            # Subject 파싱
            subject = {}
            for rdn in cert_dict.get('subject', ()):
                for attr_type, attr_value in rdn:
                    subject[attr_type] = attr_value

            # Issuer 파싱
            issuer = {}
            for rdn in cert_dict.get('issuer', ()):
                for attr_type, attr_value in rdn:
                    issuer[attr_type] = attr_value

            # SAN (Subject Alternative Names) 추출
            san = []
            for ext_type, ext_data in cert_dict.get('subjectAltName', ()):
                if ext_type == 'DNS':
                    san.append(ext_data)

            # 유효 기간 계산
            not_before = datetime.datetime.strptime(
                cert_dict['notBefore'],
                '%b %d %H:%M:%S %Y %Z'
            )
            not_after = datetime.datetime.strptime(
                cert_dict['notAfter'],
                '%b %d %H:%M:%S %Y %Z'
            )

            now = datetime.datetime.utcnow()
            is_valid = not_before <= now <= not_after
            days_until_expiry = (not_after - now).days

            return CertificateInfo(
                subject=subject,
                issuer=issuer,
                version=cert_dict.get('version', 0),
                serial_number=cert_dict.get('serialNumber', 0),
                not_before=not_before,
                not_after=not_after,
                signature_algorithm=cert_dict.get('signatureAlgorithm', 'Unknown'),
                public_key_type=self._get_pubkey_type(),
                public_key_size=self.socket.cipher()[1],
                san=san,
                is_valid=is_valid,
                days_until_expiry=days_until_expiry
            )

        except Exception as e:
            print(f"[TLS] 인증서 정보 추출 실패: {e}")
            return None

    def _get_pubkey_type(self) -> str:
        """공개키 타입 추정"""
        cipher = self.socket.cipher()[0]
        if 'RSA' in cipher or 'TLS_RSA' in cipher:
            return 'RSA'
        elif 'ECDSA' in cipher or 'ECDHE_ECDSA' in cipher:
            return 'ECDSA'
        elif 'ECDHE' in cipher:
            return 'ECDH'
        return 'Unknown'

    def check_security_features(self) -> Dict[str, bool]:
        """보안 기능 점검"""
        if not self.socket:
            return {}

        cipher = self.socket.cipher()[0]
        version = self.socket.version()

        return {
            'tls_1_3': version == 'TLSv1.3',
            'tls_1_2_plus': version in ['TLSv1.2', 'TLSv1.3'],
            'forward_secrecy': 'ECDHE' in cipher or 'DHE' in cipher,
            'aead_cipher': 'GCM' in cipher or 'CCM' in cipher or 'POLY1305' in cipher,
            'strong_key_exchange': 'ECDHE' in cipher,
            'no_weak_hash': 'SHA1' not in cipher and 'MD5' not in cipher
        }

    def close(self):
        """연결 종료"""
        if self.socket:
            self.socket.close()


class TLSSecurityAssessment:
    """
    TLS 보안 평가 도구
    PCI DSS, NIST 기준에 따른 평가
    """

    @staticmethod
    def assess_hostname(hostname: str) -> Dict:
        """호스트 TLS 보안 평가"""
        analyzer = TLSAnalyzer(hostname)
        results = {
            'hostname': hostname,
            'connected': False,
            'protocol': {},
            'certificate': None,
            'security_features': {},
            'grade': 'F',
            'issues': []
        }

        if not analyzer.connect():
            results['issues'].append('TLS 연결 실패')
            return results

        results['connected'] = True
        results['protocol'] = analyzer.get_protocol_info()
        results['certificate'] = analyzer.get_certificate_info()
        results['security_features'] = analyzer.check_security_features()

        # 보안 등급 산정
        grade, issues = TLSSecurityAssessment._calculate_grade(results)
        results['grade'] = grade
        results['issues'] = issues

        analyzer.close()
        return results

    @staticmethod
    def _calculate_grade(results: Dict) -> tuple:
        """보안 등급 계산 (A+ ~ F)"""
        score = 100
        issues = []

        sec = results.get('security_features', {})

        # TLS 1.3 지원 (+10)
        if sec.get('tls_1_3'):
            score += 10
        elif not sec.get('tls_1_2_plus'):
            score -= 30
            issues.append('TLS 1.2 미만 지원')

        # Forward Secrecy (-20 if not)
        if not sec.get('forward_secrecy'):
            score -= 20
            issues.append('Forward Secrecy 미지원')

        # AEAD 암호 (-15 if not)
        if not sec.get('aead_cipher'):
            score -= 15
            issues.append('AEAD 암호 미사용')

        # 인증서 만료 임박
        cert = results.get('certificate')
        if cert:
            if cert.days_until_expiry < 30:
                score -= 20
                issues.append(f'인증서 {cert.days_until_expiry}일 후 만료')
            elif cert.days_until_expiry < 90:
                score -= 10
                issues.append(f'인증서 {cert.days_until_expiry}일 후 만료')

        # 등급 결정
        if score >= 90:
            grade = 'A+'
        elif score >= 80:
            grade = 'A'
        elif score >= 70:
            grade = 'B'
        elif score >= 60:
            grade = 'C'
        elif score >= 50:
            grade = 'D'
        else:
            grade = 'F'

        return grade, issues


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("[ TLS Security Assessment ]")
    print("=" * 60)

    test_sites = [
        "www.google.com",
        "github.com",
        "www.naver.com"
    ]

    for hostname in test_sites:
        print(f"\n[ {hostname} ]")
        print("-" * 40)

        results = TLSSecurityAssessment.assess_hostname(hostname)

        print(f"  연결 상태: {'성공' if results['connected'] else '실패'}")
        print(f"  보안 등급: {results['grade']}")

        if results['protocol']:
            print(f"  프로토콜: {results['protocol']['protocol_version']}")
            print(f"  암호 스위트: {results['protocol']['cipher_suite']}")

        cert = results['certificate']
        if cert:
            print(f"  인증서 발급자: {cert.issuer.get('organizationName', 'N/A')}")
            print(f"  유효 기간: ~{cert.not_after.strftime('%Y-%m-%d')}")
            print(f"  만료까지: {cert.days_until_expiry}일")
            print(f"  SAN 개수: {len(cert.san)}")

        if results['security_features']:
            print("  보안 기능:")
            for feature, enabled in results['security_features'].items():
                status = "✓" if enabled else "✗"
                print(f"    {status} {feature}")

        if results['issues']:
            print("  이슈:")
            for issue in results['issues']:
                print(f"    ! {issue}")
```

---

## Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

### TLS 1.2 vs TLS 1.3 비교

| 특성 | TLS 1.2 | TLS 1.3 |
|------|---------|---------|
| **핸드셰이크 RTT** | 2-RTT | 1-RTT (0-RTT 재개) |
| **지원 키 교환** | RSA, DHE, ECDHE, DH_anon | ECDHE, DHE만 (PFS 필수) |
| **지원 암호** | CBC, RC4, 3DES 등 | AEAD만 (GCM, CCM, Poly1305) |
| **PFS (Forward Secrecy)** | 선택적 | 필수 |
| **압축** | 지원 | 제거 (CRIME 공격 방지) |
| **재협상** | 지원 | 제거 (별도 핸드셰이크) |
| **0-RTT** | 미지원 | 지원 |
| **Cipher Suite 수** | 37개 | 5개 (단순화) |

### 인증서 유형 비교

| 유형 | 검증 수준 | 발급 시간 | 비용 | 용도 |
|------|----------|----------|------|------|
| **DV (Domain Validation)** | 도메인 소유만 | 분 단위 | 무료~$10 | 블로그, 개인 사이트 |
| **OV (Organization Validation)** | 조직 실체 확인 | 1~3일 | $50~$200 | 기업 웹사이트 |
| **EV (Extended Validation)** | 엄격한 실체 확인 | 1~2주 | $200~$1,000 | 금융, 쇼핑몰 |
| **Wildcard** | *.domain.com | 일반 | 2~3배 | 멀티 서브도메인 |
| **Multi-Domain (SAN)** | 여러 도메인 | 일반 | 도메인당 추가 | 통합 인증서 |

### 과목 융합 관점 분석

1. **암호학과의 융합**:
   - **RSA/ECDSA**: 서명 알고리즘으로 인증서 무결성 보장
   - **ECDHE**: 키 교환으로 Forward Secrecy 보장
   - **AES-GCM/ChaCha20-Poly1305**: AEAD 인증 암호로 기밀성+무결성 동시 보장

2. **PKI(Public Key Infrastructure)와의 융합**:
   - **인증서 체인**: Root CA → Intermediate CA → End Entity
   - **CRL/OCSP**: 인증서 폐기 상태 확인
   - **CT (Certificate Transparency)**: 인증서 로그 공개로 위조 방지

3. **클라우드/DevOps와의 융합**:
   - **Let's Encrypt**: ACME 프로토콜로 자동화된 무료 인증서 발급
   - **mTLS (Mutual TLS)**: 서비스 메시(Istio)에서 서비스 간 상호 인증
   - **Certificate Pinning**: 모바일 앱에서 특정 인증서만 신뢰

---

## Ⅳ. 실무 적용 및 기술사적 판단 (Strategy & Decision)

### 실무 시나리오: 금융 서비스 TLS 구성

**문제 상황**: 온라인 뱅킹 서비스의 TLS 보안 정책을 수립해야 합니다. PCI DSS 4.0 준수가 필요합니다.

**기술사의 전략적 의사결정**:

1. **TLS 버전 정책**:
   ```
   - TLS 1.3: 권장 (모든 신규 연결)
   - TLS 1.2: 허용 (레거시 클라이언트)
   - TLS 1.0/1.0: 완전 차단
   ```

2. **Cipher Suite 우선순위**:
   ```
   1. TLS_AES_256_GCM_SHA384
   2. TLS_CHACHA20_POLY1305_SHA256
   3. TLS_AES_128_GCM_SHA256
   4. ECDHE-RSA-AES256-GCM-SHA384
   5. ECDHE-RSA-AES128-GCM-SHA256
   ```

3. **인증서 요구사항**:
   - **EV 인증서** 필수 (금융 서비스)
   - **최소 RSA-2048 또는 ECDSA P-256**
   - **SHA-256 이상 서명**
   - **90일 이내 만료 알림**

4. **보안 헤더**:
   ```
   Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
   ```

### 안티패턴 (Anti-patterns)

- **안티패턴 1 - Self-Signed Certificate in Production**:
  자체 서명 인증서는 브라우저 경고를 유발하고, 중간자 공격에 취약합니다. 반드시 공인 CA 인증서를 사용해야 합니다.

- **안티패턴 2 - RSA 키 교환 사용**:
  RSA 키 교환은 Forward Secrecy를 제공하지 않습니다. 개인키가 유출되면 모든 과거 세션이 복호화됩니다. ECDHE를 사용해야 합니다.

---

## Ⅴ. 기대효과 및 결론 (Future & Standard)

### 정량적/정성적 기대효과

| 효과 영역 | HTTP | HTTPS (TLS 1.2) | HTTPS (TLS 1.3) |
|----------|------|-----------------|-----------------|
| **연결 지연** | 1 RTT | 3 RTT | 1-2 RTT |
| **데이터 보호** | 없음 | 암호화 | 암호화 |
| **중간자 공격** | 취약 | 부분 보호 | 강력 보호 |
| **성능 오버헤드** | 없음 | ~5% | ~1% (0-RTT) |

### 미래 전망 및 진화 방향

- **Post-Quantum TLS (PQTLS)**: 양자 내성 알고리즘(Kyber, Dilithium) 통합
- **Encrypted Client Hello (ECH)**: SNI 암호화로 검열 회피
- **Delegated Credentials**: 단기 유효 크리덴셜로 키 유출 영향 최소화

### 참고 표준/가이드

| 표준 | 기관 | 내용 |
|------|------|------|
| **RFC 8446** | IETF | TLS 1.3 Protocol |
| **RFC 5246** | IETF | TLS 1.2 Protocol |
| **RFC 8446 Appendix E** | IETF | TLS 1.3 Cipher Suites |
| **NIST SP 800-52 Rev 2** | NIST | TLS 가이드라인 |
| **PCI DSS 4.0** | PCI SSC | 결제 카드 보안 표준 |

---

## 관련 개념 맵 (Knowledge Graph)
- [PKI 공개키 기반 구조](./pki_certificate_authority.md) - CA, 인증서 체인
- [대칭/비대칭 암호](./symmetric_asymmetric_encryption.md) - AES, RSA, ECDSA
- [해시 함수와 MAC](./hash_function_hmac.md) - SHA-256, HMAC
- [HTTPS와 HTTP/2](../8_application/http_https.md) - 보안 웹 프로토콜
- [mTLS 서비스 메시](../7_cloud/mtls_service_mesh.md) - Istio, Envoy

---

## 어린이를 위한 3줄 비유 설명
1. **TLS**는 **비밀 편지 교환**과 같아요. 아무나 읽을 수 없도록 특별한 암호로 편지를 씁니다.
2. **인증서**는 **여권**이에요. 이 웹사이트가 진짜 은행인지, 가짜인지 확인해 줍니다.
3. **핸드셰이크**는 **암호 약속**을 정하는 과정이에요. "우리 이런 암호 쓸래?" "좋아!" 하고 서로 합의합니다!
