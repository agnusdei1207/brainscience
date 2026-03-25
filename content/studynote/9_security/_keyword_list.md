+++
title = "09. 정보보안 키워드 목록"
date = "2026-03-25"
[extra]
categories = "studynote-security"
+++

# 정보보안 (Information Security) 키워드 목록

정보통신기술사·컴퓨터응용시스템기술사 대비 보안 전 영역 기술사 수준 핵심 키워드
> ⚡ 기술사 보안 문제는 단순 지식이 아닌 **위협 모델링 → 아키텍처 설계 → 법적·제도적 대응**까지 통합 서술을 요구함

---

## 1. 정보보안 개론 / 원칙 — 67개

1. 정보보안 3요소 — CIA (기밀성·무결성·가용성)
2. 기밀성 (Confidentiality) — 암호화, 접근 제어, DRM, 분류
3. 무결성 (Integrity) — 해시, 전자서명, MAC, HMAC, 체크섬
4. 가용성 (Availability) — HA 설계, RAID, 부하 분산, DDoS 방어, SLA
5. 인증성 (Authenticity) — 신원 확인, PKI, 디지털 서명, 메시지 인증
6. 부인방지 (Non-repudiation) — 전자서명, 타임스탬프, 로그, 감사 추적
7. 책임추적성 (Accountability) — 감사 로그, 감사 기록, 사용자 행동 추적
8. 개인정보보호 3요소 — 기밀성·무결성·접근성 (ISO 27701)
9. 정보보안 6요소 — CIA + 인증성 + 부인방지 + 책임추적성
10. 최소 권한 원칙 (Principle of Least Privilege) — 필요 알 권리
11. 직무 분리 원칙 (Separation of Duties) — 4눈 원칙, 분산 통제
12. 다단계 인증 원칙 (Defense in Depth) — 심층 방어
13. 알 필요성 원칙 (Need-to-Know) — 정보 접근 제한
14. 단순 보안 원칙 (Simplicity) — 불필요한 복잡성 제거
15. 공개 설계 원칙 (Open Design) — 키 은닉，而非 算法 은닉
16. 실패 안전 원칙 (Fail-Safe) — 기본값 거부, 오류 시 안전 상태
17. 완전한 중재 원칙 (Complete Mediation) — 모든 접근 경로 검사
18. 경제적 설계 원칙 (Economy of Mechanism) — 최소 구현
19. 완전한 통제 원칙 (Open Platform for Security) — 분리 보호
20.Least Common Mechanism — 메커니즘 공유 최소화
21. 심리적 사용성 원칙 (Psychological Acceptability) — 보안이 사용성을 해치면 안 됨
22. 정보보안 정책 — 최고 경영진 승인, 문서화된 규칙
23. 정보보안 표준 — 정책實施 위한 구체적 기준
24. 정보보안 지침 — 표준 적용 방법론
25. 정보보안 절차 — 구체적 작업 지침
26. 위험 관리 프로세스 — 식별/분석/평가/대응/모니터링/보고
27. 위험 식별 (Risk Identification) — 자산·위협·취약점 목록화
28. 정량적 위험 분석 — ALE = ARO × SLE, MTBF, MTTF, MTTR
29. 정성적 위험 분석 — High/Medium/Low 매트릭스
30. SLE (Single Loss Expectancy) — 단일 사고 예상 손실
31. ARO (Annual Rate of Occurrence) — 연간 발생 확률
32. ALE (Annual Loss Expectancy) — 연간 예상 손실
33. 위험 대응 전략 4가지 — 회피/전가/완화/수용
34. 위험 회피 (Risk Avoidance) — 위험 원천 제거
35. 위험 전가 (Risk Transfer) — 보험, 외주, 계약 조항
36. 위험 완화 (Risk Mitigation) — 통제措施 도입으로 위험 감소
37. 위험 수용 (Risk Acceptance) —管理层 승인 하에
38. 잔여 위험 (Residual Risk) — 통제 후 남은 위험
39. 검출 위험 (Detected Risk) vs 미검출 위험 (Undetected Risk)
40. inherited Risk — 상속된 위험
41.보안 아키텍처 — Zachman Framework (6×6 매트릭스)
42. SABSA (Sherwood Applied Business Security Architecture) — 수평×수직 매트릭스
43. OSA (Open Security Architecture) — 보안 아키텍처 패턴 카탈로그
44. TOGAF (The Open Group Architecture Framework) — 아키텍처 개발 方法论
45. NIST CSF 2.0 — Identify/Protect/Detect/Respond/Recover + Govern
46. 제로 트러스트 (Zero Trust) — "Never Trust, Always Verify", NIST SP 800-207
47. ZTA (Zero Trust Architecture) — NIST 4단계 구현 로드맵
48. SDP (Software Defined Perimeter) —的软件 정의 경계
49. 마이크로 세그멘테이션 — 워크로드별 격리, 측면 이동 차단
50. East-West 트래픽 통제 — 내부 세그멘테이션
51. North-South 트래픽 통제 — 경계 방어
52. 보안 통제 3가지 유형 — 관리적/기술적/물리적
53. 예방 통제 (Preventive Controls) — 사전 차단
54. 탐지 통제 (Detective Controls) — 이상 징후 발견
55. 교정 통제 (Corrective Controls) — 사고 후 복구
56. 억제 통제 (Deterrent Controls) — 위협 행동 억제
57. 상실 통제 (Compensating Controls) — 기존 통제 우회 조치
58. 내재적 보안 (Security by Design) — 설계 단계 보안 고려
59. 사후 보안 (Bolt-on Security) — 완성 후 보안 추가
60. Privacy by Design 7基本原则 — 사전 보호, 기본값私密性 등
61. Secure by Default — 기본적으로 안전한 기본값
62. Secure Coding — 안전한 소프트웨어 개발
63. Threat Modeling — STRIDE, DREAD, MITRE ATT&CK 맵핑
64. DREAD 모델 — Damage/Reproducibility/Exploitability/Affected Users discoverability
65. STRIDE 모델 — Spoofing/Tampering/Repudiation/Information Disclosure/DoS/Elevation
66. PASTA (Process for Attack Simulation and Threat Analysis) — 7단계 위협 모델링
67. Attack Surface Analysis — 공격 표면 관리

---

## 2. 암호학 기초 — 42개

1. 암호학 (Cryptography) — 기밀성·무결성·인증·부인방지 제공
2. 고전 암호 — 치환 암호, 전치 암호
3.凯撒 암호 (Caesar Cipher) — 알파벳 3자리 이동
4. 단일 치환 암호 — 하나의 알파벳을 하나의 문자로 치환
5. 다중 치환 암호 (Vigenère Cipher) — 키워드 기반 복수 치환
6. Enigma — 독일 제2차 세계대전 기계식 암호
7.一次性密码本 (One-Time Pad) — 정보 이론적으로 완벽한 안전성
8. 현대 암호학 기본 가정 — computationally infeasible
9. 대칭키 암호 (Symmetric Encryption) — 동일한 키로 암호화/복호화
10. 비대칭키 암호 (Asymmetric Encryption) — 공개키/비밀키 쌍
11. 하이브리드 암호 — 대칭+비대칭 결합 (키 교환+데이터 암호화)
12. 블록 암호 (Block Cipher) — 고정 크기 블록 단위 암호화
13. 스트림 암호 (Stream Cipher) — 비트/바이트 단위 실시간 암호화
14. RC4 — 스트림 암호, 취약점 발견으로 사용 중단 (WEP)
15. Salsa20/ChaCha20 — ARX 기반 스트림 암호, TLS 1.3
16. AES (Advanced Encryption Standard) — 128/192/256비트 키
17. AES SPN 구조 — SubBytes/ShiftRows/MixColumns/AddRoundKey
18. AES 키 스케줄 — 라운드 키 생성
19. DES (Data Encryption Standard) — 56비트 키, 취약
20. 3DES (Triple DES) — 168비트 (112비트 실효 강도)
21. 블록 암호 모드 — ECB/CBC/CFB/OFB/CTR
22. CBC (Cipher Block Chaining) — 초기화 벡터(IV) 필요, 체인 의존성
23. CTR (Counter) — 난수 대신 카운터, 병렬 처리 가능
24. GCM (Galois/Counter Mode) — AEAD, 인증 암호화
25. AEAD (Authenticated Encryption with Associated Data) — 암호화+인증 동시
26. CCA (Chosen Ciphertext Attack) — 암호문 공격 분류
27. CPA (Chosen Plaintext Attack) — 평문 공격 분류
28. IND-CPA (Indistinguishability under CPA) — 암호학적 안전성 정의
29. IND-CCA2 — 강인한 암호학적 안전성
30. 해시 함수 — 단방향성, 충돌 저항성, Preimage 저항성
31. MD5 — 128비트 해시, 충돌 공격 실용화 (1996)
32. SHA-1 — 160비트, SHA-1 충돌 발견 (2017, SHAttered)
33. SHA-2 — SHA-224/256/384/512, 현재 표준
34. SHA-3 (Keccak) — sponge construction, NIST 2015
35. BLAKE2/BLAKE3 — 채택성능 해시, AES 대체
36. HMAC (Hash-based Message Authentication Code) — 키掺入 해시
37. NMAC (Nested MAC)
38. CMAC (Cipher-based MAC) — 블록 암호 기반
39. GMAC (Galois MAC) — GCM의 인증 부분
40.rainbow table — 사전 계산 해시 테이블, 역산 공격
41. salt — 해시 충돌 방지를 위한 난수 추가
42. 키 스트레칭 — PBKDF2, bcrypt, scrypt (메모리 하드)

---

## 3. 암호학 심화 / PKI — 52개

1. RSA — 소인수분해 문제 기반, 1977년 Rivest/Shamir/Adleman
2. RSA 키 생성 — 두 소수의 곱, 오일러 파이 함수
3. RSA-OAEP — 최적 asymmetric encryption padding, CCA2 안전성
4. RSA-PSS — 확률적 서명 방식, safe 서명
5. modulo 연산 — RSA 핵심인 나머지 연산
6. Carmichael 수 — RSA 안전성 분석 관련
7. GCD (최대공약수) — RSA 키 생성에서 사용
8. 확장 유클리드 알고리즘 — 모듈로 역수 계산
9. CRT (Chinese Remainder Theorem) — RSA 복호화 최적화
10. ECC (Elliptic Curve Cryptography) — 타원곡선 이산 로그 문제
11. 타원곡선 — y² = x³ + ax + b 꼴의 곡선
12. ECDLP (Elliptic Curve Discrete Log Problem) — ECC 안전성 기반
13.secp256k1 — Bitcoin에서 사용되는 곡선
14. P-256 (secp256r1) — NIST 권장 곡선
15. P-384 / P-521 — NIST 고강도 곡선
16. ECDSA (Elliptic Curve DSA) — ECC 기반 디지털 서명
17. EdDSA / Ed25519 — Edwards 곡선, 결정론적 서명
18. X25519 — ECDH를 Edwards 곡선에서 구현
19. DH (Diffie-Hellman) — 이산 로그 기반 키 교환
20. DHE (Ephemeral DH) — 임시 DH, 전방 비밀성(PFS) 제공
21. ECDH — ECC 기반 효율적 키 교환
22. ECDHE — Ephemeral ECDH, TLS 1.3 기본
23. 키교환 프로토콜 — 중간자 공격 방지를 위한 상호 인증
24. Hybrid Encryption — KEM/DEM 분리 구조 (ISO 18033-2)
25. KEM (Key Encapsulation Mechanism) — 키 포장
26. DEM (Data Encapsulation Mechanism) — 데이터 암호화
27. HKDF (HMAC-based Key Derivation Function) — RFC 5869
28. TLS 1.3 핸드셰이크 — 1-RTT, 0-RTT, PSK
29. AEAD 요구 — TLS 1.3은 AEAD 암호만 허용
30. 전방 비밀성 (PFS) — 과거 세션 키 유출해도 과거 통신 보호
31. 세션 키 — 임시 세션용短期密钥
32. 마스터 시크릿 — Pre-Master Secret에서 파생
33. PSK (Pre-Shared Key) — 사전 공유 키
34. Diffie-Hellman Gruppen — RFC 3526 소수 그룹
35. 키 파생 함수 — TLS 1.3의 HKDF-Extract/Expand
36. NIST PQC 표준화 — 2016년 시작, 2024년 4개 알고리즘 선정
37. CRYSTALS-Kyber — 격자 기반 KEM, NIST PQC 표준
38. CRYSTALS-Dilithium — 격자 기반 디지털 서명, NIST PQC
39. FALCON — 격자 기반 서명, 짧은 서명
40. SPHINCS+ — 해시 기반 서명, 양자 내성
41. BIKE / HQC / Classic McEliece — 코드 기반 PQC
42. 양자 컴퓨팅 위협 — Shor 알고리즘 (RSA/ECC 깨뜨림), Grover (AES 128→64)
43. "Harvest Now, Decrypt Later" — 양자 위협 대응 전략
44..crypto agility — 알고리즘 교체 능력, PQC 이전 준비
45. 키 관리 생명주기 — 생성/분배/저장/사용/순환/폐기
46. 키 폐기 — 안전한 삭제, 키 재료 완전 소멸
47. 키 순환 — 정기적 키 교체, 유출 시 복구력
48. HSM (Hardware Security Module) — 물리적 키 보호
49. TPM (Trusted Platform Module) — 플랫폼 키 저장, 원격 증명
50. PKI (Public Key Infrastructure) — 공개키 인증서 체계
51. CA (Certification Authority) — 인증서 발급/관리
52. RA (Registration Authority) — 인증 요청 검증/승인

---

## 4. PKI 심화 / 인증 프로토콜 — 48개

1. CRL (Certificate Revocation List) — 폐지 인증서 목록
2. OCSP (Online Certificate Status Protocol) — 실시간 인증서 상태 질의
3. OCSP 스테이플링 — 서버가 OCSP 응답 사전 가져옴
4. CT (Certificate Transparency) — 인증서 발급 공개 로그
5. CT 로그 서버 — Google/Rustproof 등 다수 운영
6. SCT (Signed Certificate Timestamp) — CT 증명
7. CAA (Certification Authority Authorization) — 허용된 CA DNS 레코드
8. PKCS#10 — 인증서 서명 요청 (CSR) 형식
9. PKCS#7 / CMS — 인증서 envelope 형식
10. PKCS#12 — 인증서+개인키 보관 형식 (.pfx)
11. DER / PEM 인코딩 — 인증서 인코딩 형식
12. X.509 v3 인증서 — Subject/Issuer/SAN/Key Usage/NSC
13. SAN (Subject Alternative Name) — 다중 도메인 인증서
14. 와일드카드 인증서 — *.example.com
15. EV (Extended Validation) 인증서 — 엄격한 검증, 녹색 주소창
16. DV (Domain Validation) 인증서 — 도메인 검증만
17. OV (Organization Validation) — 조직 검증
18. Self-signed 인증서 — 자체 발급 인증서, 내부용
19. 인증서 체인 검증 — Root CA → Intermediate CA → End Entity
20. 브릿지 CA (Bridge CA) — 교차 인증
21. 인증서 핀닝 —已知 인증서 목록 하드코딩
22. HPKP (HTTP Public Key Pinning) — deprecated, 동적 핀닝 권장
23. Certificate Patrol / Security/Telemetry — Firefox 브라우저 핀닝
24. 동적 핀닝 — CT 로그 기반pins
25. Stapling of OCSP Response — TLS 핸드셰이크 최적화
26. mTLS (Mutual TLS) — 서버+클라이언트 상호 인증
27. Code Signing — 소프트웨어 원산지 인증
28. Authenticode — Microsoft 코드 서명
29. Apple Developer ID — macOS/iOS 앱 서명
30. 서명 타임스탬프 —TSA (Time Stamping Authority)
30.TSA (Time Stamping Authority) — RFC 3161, 부인방지
31. CRL Distribution Point — CRL 발급 위치
32. Authority Information Access — OCSP 응답자 위치
33. CRL Scope — 전체/crlNumber 용도
34. delta CRL —增量 CRL, 효율성 향상
35. LDH (Limited Distribution Hypothesis) — 인증서 배포 모델
36. Key Usage 확장 — digitalSignature/keyEncipherment/codeSigning
37. Extended Key Usage — serverAuth/clientAuth/codeSigning/emailProtection
38. nameConstraints — CA가 발급 가능한 이름 공간 제한
39. Basic Constraints — CA 여부, 경로 길이 제한
40. 정책 매핑 — 상위 CA 정책과 하위 CA 정책 매핑
41. SPC (Signed Public Key Challenge) — 코드 서명 blob
42.Authenticode Timestamp Protocol — RFC 3161 호환
43. Kernel Mode Signing — Windows 커널 드라이버 필수
44. UEFI Secure Boot — 부팅 과정 코드 서명 검증
45. DKIM (DomainKeys Identified Mail) — 이메일 발신자 인증
46. SPF (Sender Policy Framework) — 허용된 발신 서버 목록 (DNS TXT)
47. DMARC (Domain-based Message Auth Reporting) — SPF+DKIM 정책
48. DANE (DNS-Based Auth of Named Entities) — TLSA 레코드, 인증서 고정

---

## 5. 네트워크 보안 — 55개

1. 네트워크 보안 3대 영역 — 경계/세그멘테이션/무결성
2. 방화벽 — 네트워크 경계 접근 제어
3. 패킷 필터링 방화벽 — 3-4층 헤더 기반 필터
4. 상태 검사 방화벽 (Stateful Inspection) — 연결 상태 추적
5. 애플리케이션 게이트웨이 (Proxy) — 7층 프로토콜 검사
6. NGFW (Next-Generation Firewall) — DPI, 사용자识别, 앱識別
7. 방화벽 토폴로지 — 스크린 서브넷, 이중 DMZ
8. bastion host — 경계 호스트, 공개 서비스 전용
9. DMZ (Demilitarized Zone) — 비 Military Zone, 공개 구간
10. 내부 방화벽 (Internal Firewall) — 내부 세그멘테이션
11. East-West 트래픽 — 수평 방향 통신, 내부 위협 통제
12. North-South 트래픽 — 경계 통과 통신
13. 네트워크 세그멘테이션 — VLAN, VRF, 논리적 격리
14. VLAN (Virtual LAN) — 브로드캐스트 도메인 분리
15. VRF (Virtual Routing and Forwarding) — 경로 격리
16. NAC (Network Access Control) — IEEE 802.1X, 포트 기반 접근 제어
17. EAP (Extensible Authentication Protocol) — 802.1X 인증 프로토콜
18. EAP-MD5 — 취약, 권장되지 않음
19. PEAP (Protected EAP) — TLS隧道保护 EAP
20. EAP-TLS — 인증서 기반 상호 인증
21. MAC Address Filtering — 허가된 MAC만 허용
22. IDS (Intrusion Detection System) — 오용 탐지/이상 탐지
23. IDS 배치 — in-band (IDS) vs out-of-band (tap/mirror)
24. IPS (Intrusion Prevention System) — 인라인 배치, 자동 차단
25. Signature-based detection —已知 공격 패턴 매칭
26. Anomaly-based detection —정상 프로파일과 비교
27. HIDS/HIPS — 호스트 기반 IDS/IPS
28. NIDS/NIPS — 네트워크 기반 IDS/IPS
29. Snort — 오픈소스 NIDS
30. Suricata — 멀티스레드 NIDS
31. Zeek (formerly Bro) — 네트워크 트래픽 분석
32. WAF (Web Application Firewall) — HTTP/HTTPS 보호
33. OWASP Core Rule Set — WAF 규칙 세트
34. Virtual Patching — 실제 패치 전 WAF로 취약점 우회
35. ModSecurity — 오픈소스 WAF 엔진
36. API Gateway — API 접근 제어,_RATE limiting, 인증
37. API Gateway 기능 — 인증/인가/캐싱/로깅/변환
38. DDoS 공격 — 고의적 서비스 중단 공격
39. DDoS 3유형 — 볼류메트릭/프로토콜/애플리케이션 계층
40. DDoS 방어 기법 — Rate Limiting, Anycast, Scrubbing Center
41. BGP Blackhole — DDoS 트래픽 경로黑洞
42. DNS Amplification — DNS 쿼리 증폭 공격
43. NTP Amplification — NTP 모노리스트 상태 쿼리 증폭
44. memcached Amplification — UDP 포트 11211 활용
45. SYN Flood — TCP 半開 연결 점유
46. UDP Flood — 비효율적 프로토콜滥用
47. HTTP Flood — application layer DDoS
48. Slowloris — HTTP 헤더 미완성 전송으로 연결 점유
49. IP Spoofing — 출발지 IP 위조, BCP38 필수
50. uRPF (Unicast Reverse Path Forwarding) — Spoofing 방지
51. ARP Spoofing — MAC 주소 위조, 스위칭 환경에서도 가능
52. Gratuitous ARP — 정상 ARP 응답 위조, MiTM 사전 준비
53. DHCP Spoofing — DHCP 서버 역할 사칭
54. DNS Spoofing — DNS 응답 캐시 오염
55. DNS Cache Poisoning — Kaminsky 공격, 검증 없는 응답

---

## 6. 네트워크 보안 심화 — 50개

1. MITM (Man-in-the-Middle) 공격 — 통신 경로 가로채기
2. SSL Stripping — HTTPS→HTTP 강제 다운그레이드
3. HSTS (HTTP Strict Transport Security) — HTTPS 강제 사용
4. HTTP Public Key Pinning — deprecated (2018)
5. Cookie Hijacking — 세션 쿠키 탈취
6. 세션 하이재킹 — TCP 시퀀스 넘버 예측
7. 패킷 스니핑 — 프로미스큐어스 모드 네트워크 인터페이스
8. 세션 고정 공격 (Session Fixation) — 공격자 세션 ID 강제 설정
9.Replay Attack — 통신 도청 후 재전송
10. IPsec — 네트워크層 투명한 보안
11. IPsec 두 가지 프로토콜 — AH (인증만)/ESP (암호화+인증)
12. IPsec 모드 — Transport 모드/Tunnel 모드
13. IKE (Internet Key Exchange) — 키 교환 프로토콜
14. IKEv1 Phase 1/2 — Main Mode/Aggressive Mode
15. IKEv2 — MOBIKE 지원, NAT-T 자동 처리
16. NAT-T (NAT Traversal) — IPsec VPN NAT 통과
17. L2TP/IPsec — L2TP 터널 + IPsec 암호화
18. SSL VPN — 브라우저 기반/클라이언트 설치형
19. OpenVPN — 오픈소스 SSL VPN
20. WireGuard — modern VPN, Linux 커널에 통합
21. ZeroTier — 분산 VPN, P2P 터널
22. Tailscale — WireGuard 기반 관리형 VPN
23. SASE (Secure Access Service Edge) — 네트워크+보안 통합
24. SSE (Security Service Edge) — SASE의 보안 요소
25. SD-WAN (Software-Defined WAN) — WAN 가상화
26. SD-WAN 보안 — 암호화된 터널, 중앙 집중식 정책
27. VPN concentrator — 다수 VPN 연결 집약 장치
28. TLS/SSL 취약점 역사 — POODLE/BEAST/CRIME/ROGUE
29. POODLE (Padding Oracle On Downgraded Legacy Encryption)
30. BEAST (Browser Exploit Against SSL/TLS)
31. CRIME — TLS 압축 사이드 채널 공격
32. HEARTBLEED — OpenSSL 하트비트 확장 메모리 유출
33. DROWN — SSLv2滥用による RSA 解読
34. Logjam — DH_EXPORT 키 강제 사용, 512비트 그룹
35. FREAK — RSA_EXPORT 키 강제 사용
36. Sweet32 — 64비트 블록 암호 Birthday 공격
37. TLS 1.3 — 이전 버전과의 호환성 제거, 빠른 핸드셰이크
38. TLS 1.3 vs 1.2 차이 — 1-RTT 핸드셰이크, 0-RTT, PFS 의무
39. TLS 密码套件 — TLS_AES_256_GCM_SHA384 등
40. cipher suite命名规则 — TLS_kex_AUTH
41. Perfect Forward Secrecy — 각 세션独立的密钥
42. SSH (Secure Shell) — 안전한 원격 접속
43. SSH 키 기반 인증 — 공개키/개인키 쌍
44. SSH Agent Forwarding — 로컬 에이전트를远程에 전달
45. SFTP — SSH 기반 파일 전송
46. SCP — SSH 기반 파일 복사
47. SSH Tunnel/Proxy — SOCKS 프록시
48. Known Hosts — 서버 공개키 최초 수락/저장
49. SSH 옵션 강화 — PasswordAuthentication no, PubkeyAuthentication yes
50. LDAP — 디렉터리 서비스 접근 프로토콜
51. LDAPS (LDAP over SSL) — 포트 636, LDAP 암호화
52. LDAP 인젝션 — 특수 문자注入으로 인증 우회
53. ARP 캐시poisoning —静态 ARP 설정으로 MiTM
54. VLAN Hopping — Switch Spoofing/Double Tagging
55. Bridge Protocol Data Unit (BPDU) — 스위치 프로토콜

---

## 7. 시스템 보안 / 엔드포인트 — 55개

1. 엔드포인트 보안 — 단말기에 대한 보안措施
2. EPP (Endpoint Protection Platform) — 통합 엔드포인트 보호
3. AV (Anti-Virus) — 시그니처 기반 악성코드 탐지
4. 행위 기반 탐지 — 시그니처 없이 의심 행동 감지
5. EDR (Endpoint Detection and Response) — 실시간 모니터링+응답
6. XDR (Extended Detection and Response) — 멀티 플랫폼 상관 분석
7. MDR (Managed Detection and Response) — 관리형 탐지/응답
8. 엔드포인트 보호 조합 — AV+EDR+NDR+UEBA
9. TTP (Tactics, Techniques, Procedures) — 공격자 행동 패턴
10. 버퍼 오버플로우 (Buffer Overflow) — 메모리 경계 초과
11. 스택 버퍼 오버플로우 — 함수 복귀 주소 덮어쓰기
12. 힙 버퍼 오버플로우 — 힙 메모리 오염
13. 정수 오버플로우 (Integer Overflow) — 정수 범위 초과
14. Format String Bug — %x, %s 등 포맷 지시어 악용
15. NX bit (No-Execute) — 실행 가능 메모리 영역 분리
16. DEP (Data Execution Prevention) — NX를 OS 수준에서 구현
17. ASLR (Address Space Layout Randomization) — 주소 공간 난수화
18. PIE (Position Independent Executable) — EXE도 ASLR
19. Stack Canary — 스택 프레임 손상 탐지 쿠키
20. SSP (Stack Smashing Protector) — GCC의 스택 보호
21. RELRO (Relocation Read-Only) — GOT 쓰기 보호
22. Full RELRO — GOT 전체 읽기 전용
23. FORTIFY_SOURCE — _chk 함수로 버퍼 연산 대체
24. ROP (Return-Oriented Programming) — 가젯 체인, 셸코드 없이 코드 실행
25. 가젯 (Gadget) — Ret 명령으로 끝나는 코드 조각
26. JOP (Jump-Oriented Programming) — 함수 포인터Hijacking
27. COP (Call-Oriented Programming) — 호출 기반 가젯 체인
28. Return-to-libc — libc 함수 직접 호출
29. Heap Spray — 힙 메모리에 셸코드 대량 배치
30. Heap Feng Shui — 힙 레이아웃 조작
31. Use-After-Free — 해제된 메모리 재사용
32. Double Free — 이중 해제로 힙 손상
33. Race Condition — TOCTOU (Time-of-Check-Time-of-Use)
34. Deadlock / Livelock — 자원 점유로 인한 교착/기아
35. Time-of-Check to Time-of-Use — 파일 접근 races
36. 권한 상승 — Local Privilege Escalation (LPE)
37. 커널 privilege escalation — Dirty COW, EternalBlue
38. Zero-Day — 패치되지 않은 취약점 利用
39. 루트킷 (Rootkit) — 시스템에潜伏하는 악성 코드 모음
40. 커널 루트킷 — OS 커널 레벨 설치
41. 사용자모드 루트킷 — 애플리케이션 레벨
42. 부트킷 (Bootkit) — 부팅 과정infecting
43. MBR Bootkit — Master Boot Record 감염
44. UEFI Bootkit — UEFI 펌웨어 수준 감염
45. Secure Boot 우회 — 서명 검증 무력화
46. Firmware Rootkit — BIOS/펌웨어 숨겨진 백도어
47. 키로거 (Keylogger) — 키입력 기록
48. 백도어 (Backdoor) — 정상 인증 우회
49. 논리炸弾 (Logic Bomb) — 특정 조건 충족 시 발동
50. 트로이목마 (Trojan Horse) — 겉보기에 정상인 악성코드
51. 랜섬웨어 (Ransomware) — 파일 암호화 후 몸값
52.CryptoLocker / WannaCry / Ryuk — 주요 랜섬웨어 변종
53. Wiper — 데이터 파괴 목적인 malware
54. 지능형 지속 위협 (APT) — 국가 수준 위협 행위자
55. Fileless Malware — 메모리 내에서만 실행, 파일 없는 공격

---

## 8. 시스템 보안 심화 — 40개

1. 커널 취약점 — 시스템 콜 인터페이스 악용
2.Spectre/Meltdown — CPU 취약점 (推测執行 악용)
3. Spectre v1/v2 — Bounds Check Bypass/Branch Target Injection
4. Meltdown — Rogue Data Cache Load
5. MDS (Microarchitectural Data Sampling) — CPU 내부 데이터 샘플링
6. ZombieLoad / RIDL — Load值的리스크
7. SWAPGS — GPU 취약점 악용
8. CPU 취약점缓解 — 마이크로코드 업데이트, OS 패치
9. 펌웨어 보안 — UEFI Secure Boot
10. Measured Boot — TPM利用, boot 측정값 기록
11. Static PCR — 부팅 과정 무결성 측정
12. Dynamic PCR — late launch으로 동적 측정
13. Intel TXT (Trusted Execution Technology) — late launch
14. SGX (Software Guard Extensions) — enclave 메모리 보호
15. enclave — SGX의加密 메모리 영역
16. AMD SEV (Secure Encrypted Virtualization) — VM 암호화
17. SEV-ES — VM 레지스터 state 암호화
18. Memory Encryption Engine — 하드웨어 메모리 암호화
19. TPM 2.0 — 키 저장, 플랫폼 증명
20. TPM 기능 — PCR, EK, NV Index, Attestation
21. remote attestation — 원격 플랫폼 증명
22. BitLocker — Windows FDE, TPM+N PIN/USB 사용
23. FileVault — macOS FDE
24. LUKS — Linux Unified Key Setup, 디스크 암호화
25. VeraCrypt — 오픈소스 암호화 도구
26. 全드라이브 암호화 (FDE) — OS 레벨 암호화
27. 필드 레벨 암호화 — DB 컬럼/필드별 암호화
28. TDE (Transparent Data Encryption) — DB 엔진 레벨 암호화
29. 백업 암호화 — 백업 데이터도 암호화 필수
30. Secure Erase — SSD trim + 암호화 키 삭제
31. 패치 관리 — CVSS 점수 기반 우선순위
32. CVSS (Common Vulnerability Scoring System) — 0~10점
33. CVSS 구성 — Base/Transient/Temporal/Global 벡터
34. CVE (Common Vulnerabilities and Exposures) — 취약점 등록 번호
35. CWE (Common Weakness Enumeration) — 취약점 유형 분류
36. CPE (Common Platform Enumeration) — 플랫폼 명칭
37. OVAL (Open Vulnerability and Assessment Language) — 취약점 검사 언어
38.弱口令检测 — 기본パスワード/사전攻撃
39. 시스템 강화 — Hardening, 불필요 서비스 제거
40. CIS Benchmarks — Center for Internet Security 강화 가이드

---

## 9. 웹 / 애플리케이션 보안 — 60개

1. OWASP Top 10 — 가장 위험한 웹 보안 취약점
2. A01. 취약한 접근 제어 — IDOR, 권한 없는 기능 접근
3. IDOR (Insecure Direct Object Reference) — 객체 참조Manipulation
4. 경로 순회 (Path Traversal) — ../../etc/passwd
5. 보편적 자원 순회 (Directory Traversal) — 경로 역추적
6. Local File Inclusion (LFI) —本地 파일 포함
7. Remote File Inclusion (RFI) — 원격 파일 포함
8. 접근 제어 회피 — 메소드 제한 우회, CORS Misconfiguration
9. A02. 암호화 실패 — 안전하지 않은 암호화 사용
10. 하드코딩 자격증명 — 소스코드 내 평문 비밀번호
11. 약한 TLS 버전 — TLS 1.0/1.1 사용
12. Certificate Pinning 우회 — Frida, Objection
13. A03. 인젝션 — 입력값 검증 부재로 인한 코드 실행
14. SQL 인젝션 — 데이터베이스 쿼리Manipulation
15. Error-based SQL Injection — 오류 메시지 통한 정보 탈취
16. Blind SQL Injection — 논리적 참/거짓 반응으로 정보 추출
17. Time-based Blind SQL Injection — SLEEP() 함수로 반응 지연
18. ORM Injection — 객체-관계 매핑 프레임워크 공격
19. NoSQL Injection — MongoDB 등 문서DB 공격
20. OS Command Injection — 서버 명령어 실행
21. LDAP Injection — LDAP 쿼리 조작
22. XPath Injection — XML 데이터 질의 조작
23. Expression Language Injection — Spring/Struts EL 공격
24. Template Injection (SSTI) — 서버 사이드 템플릿 엔진 공격
25. A04. 안전하지 않은 설계 — threat modeling 부재
26. 위협 모델링 부재 — 설계 단계 보안 평가 미실시
27. 안전하지 않은 기본값 — 기본 계정/비밀번호
28. 초과 기능 — 불필요한 기능 활성화
29. A05. 보안 설정 오류 — 잘못된 구성으로 인한 노출
30. 기본 계정 —厂商 제공 기본 비밀번호
31. 불필요 서비스 — 사용 안 하는 서비스 running
32. 오류 메시지 정보 유출 — 내부 경로/스택 트레이스
33. Missing Security Headers — 보안 헤더 미설정
34. Debug Mode — 개발용 모드 생산 환경 노출
35. CORS Misconfiguration — Access-Control-Allow-Origin: *
36. A06. 취약한 컴포넌트 — 알려진 취약점 포함 라이브러리
37. Log4Shell (CVE-2021-44228) — Log4j RCE
38. 서드파티 라이브러리 취약점 — npm/PyPI/RubyGems 의존성
39. A07. 인증 실패 — 부적절한 인증 메커니즘
40. 크리덴셜 스터핑 — 유출 계정 재사용
41. 브루트포스 — 무차별 대입 공격
42. 패스워드 스프레이 — 다양한 비밀번호 소량 시도
43. 크리덴셜 풀링 — 자격증명 목록 활용
44. 세션 ID 노출 — URL, 로그, Referer 헤더
45. 세션 고정 — 세션 ID 고정 공격
46. A08. 무결성 실패 — 소프트웨어 무결성 검증 부재
47. CI/CD 보안 — 파이프라인 침해, 의존성 오염
48. 의존성 오염 (Dependency Confusion) — 비공개 패키지 덮어쓰기
49. 잘못된 서명 검증 — 코드 서명 검증 우회
50. A09. 로깅/모니터링 실패 — 증거 미보존
51. Blindness — 공격 탐지 못 함
52. Logging Without Alert — 로그만 기록, 알림 없음
53. A10. SSRF — 서버 사이드 요청 위조
54. SSRF 메타데이터 — 169.254.169.254 등 cloud metadata
55. XSS (Cross-Site Scripting) —客户端 스크립트 삽입
56. 반사형 XSS — URL 파라미터 반영
57. 저장형 XSS — DB에 저장, 모든 사용자에게 발동
58. DOM-based XSS —客户端 JavaScript 변조
59. XSS 페이로드 — <script>alert(1)</script>, img onerror
60. CSP (Content Security Policy) — XSS 완화 헤더

---

## 10. 웹 보안 심화 / API 보안 — 50개

1. CSRF (Cross-Site Request Forgery) — 사용자의 의지와 무관한 요청
2. SameSite 쿠키 — CSRF 방어
3. CSRF Token — 난수 토큰 요구
4.双重 Submit Cookie — 쿠키+파라미터 대조
5. Clickjacking — 투명 iframe 덮기
6. X-Frame-Options — frame embedding 차단
7. frame-ancestors — CSP 버전의 frame-ancestors
8. CORS Preflight — OPTIONS 요청으로 사전 검증
9. CORS 요청 흐름 — Origin 헤더 → 서버 허용/거부
10. OWASP ZAP — 웹 취약점 스캐너
11. Burp Suite — 웹 프록시,渗透 테스트 도구
12. SQLMap — SQL 인젝션 자동화 도구
13. Nikto — 웹 서버 취약점 스캐너
14. httpoxy — CGI 환경변수 proxyManipulation
15. Host Header Injection — X-Forwarded-Host 검증 우회
16. Web Cache Deception — 캐시poisoning
17. Unicode Normalization — нормализация 차이 공격
18. NULL Byte Injection — %00로 확장자 우회
19. Null Byte Poisoning — 파일명 내 null 문자
20. OAS (OpenAPI Specification) — REST API 표준
21. GraphQL 인트로스펙션 — API 스키마 공개
22. GraphQL DoS — depth/alias 제한 없으면 무한 쿼리
23. REST API 보안 — Rate Limiting, JWT, HMAC
24. API Versioning — API 버전 관리와 보안
25. JWT (JSON Web Token) — stateless 인증
26. JWT 구조 — Header/Payload/Signature (JWS/JWE)
27. JWT alg: none — 취약점, alg 검증 필수
28. HS256 vs RS256 — 대칭/비대칭 서명
29. JWT 유출 — XSS로 토큰 탈취
30. Refresh Token — 액세스 토큰 재발급
31. OAuth 2.0 — 델리게이션 프로토콜
32. OAuth 2.0 4가지 Grant — Authorization Code/PKCE/Client Credentials/ROP
33. Authorization Code Grant —redirect_uri 기반
34. PKCE (Proof Key for Code Exchange) — public client 보안
35. Open Redirect — OAuth redirect_uri 우회
36. Token Leakage — URL 내 토큰 노출
37. Scope — OAuth 권한 범위
38. Access Token vs Refresh Token — 수명 차이
39. OIDC — OAuth 2.0之上的 신원 레이어
40. ID Token — OIDC의 사용자 신원 증명
41. ID Token vs Access Token — 용도 구분
42.Discovery Document — .well-known/openid-configuration
43. jwks_uri — JSON Web Key Set 엔드포인트
44.Nonce — replay attack 방지
45. Rate Limiting — 요청 수 제한으로 DoS 방지
46. WAF 규칙 — OWASP CRS 기반
47. ModSecurity Core Rule Set — generic 공격 탐지
48. HTTP Request Smuggling — front-end/back-end interpretation 차이
49. HTTP Request走私 — CL.TE, TE.CL, H2.CL
50. HTTP Response Smuggling — 응답 분할

---

## 11. 신원 관리 / 접근 제어 — 55개

1. IAM (Identity and Access Management) — 신원+접근 통합 관리
2. 신원 관리 — 사용자 lifecycle (프로비저닝/수정/비활성화/삭제)
3. Provisioning — 사용자 계정 자동 생성
4. Deprovisioning — 퇴직/이직 시 계정 즉시 삭제
5.Joiner/Mover/Leaver 프로세스 — 신원 lifecycle 관리
6. SSO (Single Sign-On) —一次登录，多アプリ access
7. SAML 2.0 — XML 기반 SSO 프로토콜
8. SAML Assertion — 신원 정보 포함 XML
9. SAML Request/Response — SP-Initiated/IdP-Initiated
10. SP (Service Provider) — 서비스 제공자
11. IdP (Identity Provider) — 신원 제공자
12. OpenID Connect — OAuth 2.0 기반 SSO
13. OIDC Discovery — 자동 설정 메타데이터
14. Claims — OIDC의 사용자 속성
15. Scope — 요청하는 정보 범위 (openid/profile/email)
16. PKCE in OIDC — Authorization Code 보호
17. OAuth 2.0 vs OIDC — 델리게이션 vs 인증
18. Federation — 조직 간 신뢰 기반 ID 공유
19. Trust Relationship — federation 파트너 간 신뢰
20. eduGAIN — 학술 기관간 federation
21. Shibboleth — SAML 기반 federation
22. LDAP — 디렉터리 서비스 프로토콜
23. Active Directory — Microsoft 디렉터리 서비스
24. Azure AD / Microsoft Entra ID — 클라우드 신원
25. Azure AD Connect — 온프레미스 AD 클라우드 연동
26. Okta — SaaS IDaaS
27. MFA (Multi-Factor Authentication) — 다중 인증
28. 지식 요인 — 비밀번호, PIN
29. 소유 요인 — 토큰, 스마트폰, 스마트카드
30. 내재 요인 — 지문, 홍채, 음성, 얼굴
31. 위치 요인 — GPS, IP 기반 위치
32. 행동 요인 — 타이핑 패턴, 마우스 움직임
33. TOTP (Time-based OTP) — 30초마다 변경
34. HOTP (HMAC-based OTP) — 카운터 기반
35. Push Notification — 모바일 푸시 알림
36. FIDO2 / WebAuthn —公开키 암호 기반 인증
37. Passkey — FIDO2 기반, 플랫폼 관리
38. Passkey 장점 — 피싱 저항, 암호 불필요
39. PAM (Privileged Access Management) — 특권 계정 관리
40.特권 계정 — 관리자,root, 서비스 계정
41. 세션 레코딩 — 특권 세션 녹화/감사
42.vault — 비밀번호 금고 (HashiCorp Vault)
43. Just-In-Time Access — 필요 시만 일시적 권한
44. RBAC (Role-Based Access Control) — 역할 기반 권한
45. RBAC 1/2/3 —.flat/hierarchical/constrained
46. 역할 계층 — 상위 역할이 하위 권한 상속
47. ABAC (Attribute-Based Access Control) — 속성 기반
48. 속성 종류 — subject/object/environment/action
49. XACML (eXtensible Access Control Markup Language) — ABAC 정책 언어
50. ReBAC (Relationship-Based Access Control) — 관계 기반
51. Zanzibar — Google의 권한 시스템
52. 최소 권한 원칙 — 필요한 최소 권한만 부여
53. 직무 분리 (SoD) —권한 분산으로 부정행위 방지
54. 어카운팅 — 접근 기록, 감사 자료
55. 접근 검토 (Access Review) — 정기적 권한 재검토

---

## 12. 신원 보안 심화 / 위협 — 40개

1. 인증 서버 — KDC, IdP, 인증 endpoints
2. Kerberos — 네트워크 인증 프로토콜 (v5)
3. KDC (Key Distribution Center) — AS+TGS 통합
4. AS (Authentication Server) — 초기 인증
5. TGS (Ticket Granting Server) — 티켓 발급
6. TGT (Ticket Granting Ticket) — 장기 티켓
7. ST (Service Ticket) — 특정 서비스용 단기 티켓
8. Kerberos 상호 인증 — client+server mutual
9. Silver Ticket — ST 위조 (서비스 계정 키 사용)
10. Golden Ticket — TGT 위조 (KRBTGT 키 사용)
11. Pass-the-Ticket — 메모리 내 티켓 재사용
12. Pass-the-Hash — NTLM 해시 재사용
13. Kerberos Bronze Attack — AS-REP Roasting
14. NTLM — Windows 네이티브 인증 프로토콜
15. NTLM Hash — MD4(UTF-16LE(password))
16. NTLM Authentication — 3-way handshake (質詢/응답)
17. LM Hash — DES 기반, 취약한 레거시
18. NTLMv2 — HMAC-MD5 기반 강화 버전
19. NetNTLM — 네트워크 상에서만 사용되는 NTLM
20. MS-CHAPv2 — PPP/EAP 내부의 NTLM 변형
21. Credential Dumping — LSASS 메모리/ SAM hive 추출
22. Mimikatz — 크리덴셜 추출 도구
23. WDigest — 평문 비밀번호 캐싱 (레지스트리 설정)
24. SSP (Security Support Provider) — 인증 공급자 DLL
25. Golden/Silver Ticket mitigation — KRBTGT 비밀번호 周월적 교체
26. Protected Users 그룹 — Kerberos 전용 인증
27. Smart Card — 인증서 기반 MFA
28. PKINIT — Kerberos에서 공개키 인증 사용
29. Remote Desktop Gateway — RDG, HTTPS 기반 원격접속
30. Azure AD条件부 액세스 — 정책 기반 접근 제어
31. 조건부 액세스 신호 — 사용자/위험/디바이스/위치
32. Identity Protection — Azure AD ID 보호
33. UEBA (User Entity Behavior Analytics) — 행동 기반 이상 탐지
34. 애드혹 identity — 임시/외부 사용자 관리
35. Federated Identity — SAML/OIDC 기반 연합
36. Identity Bridge — AD FS, Azure AD Connect Federation
37. SCIM 2.0 — 자동 사용자 프로비저닝 프로토콜
38. JIT 프로비저닝 — Just-In-Time, On-Demand 프로비저닝
39. ID Governance — 권한 인증, 합성성 검토
40. Privileged Identity Management (PIM) —Azure 특권 ID 관리

---

## 13. 보안 운영 (SecOps) — 60개

1. SOC (Security Operations Center) — 보안 관제 조직
2. SOC 티어 — 티어 1(alert 분석)/2( approfondita調査)/3( threat hunting)
3. NOC (Network Operations Center) — 네트워크 모니터링
4. SIEM (Security Information and Event Management) — 로그 집적/상관 분석
5. SIEM 구성 — 수집(Curator)/저장(Repository)/분석(Analyzer)/可视化(Dashboard)
6. 로그 수집 — syslog, Windows Event Log, NetFlow, PCAP
7. Normalizzazione — 다양 로그 형식 정규화
8. 상관 분석 (Correlation) — 이벤트 간 관계 탐지
9. UEBA in SIEM — 행동 분석 기반 이상 탐지
10. Splunk — Enterprise SIEM
11. Elastic SIEM — Elasticsearch 기반
12. QRadar — IBM SIEM
13. ArcSight — HPE/Micro Focus SIEM
14. Graylog — 오픈소스 SIEM
15. Wazuh — 오픈소스 SIEM/EDR
16. SOAR (Security Orchestration, Automation, Response) — 자동화 대응
17. 플레이북 — 시나리오별 자동 대응 절차
18. 보안 자동화 — 반복 작업 자동화
19.Threat Intelligence — 위협 정보 공유
20. TI 4가지 유형 — 전략/전술/운영/기술적
21. STIX/TAXII — 위협 정보 교환 표준
22. MITRE ATT&CK — 공격자 전술/기법/절차DB
23. ATT&CK Matrix — Pre-ATT&CK/Enterprise/Mobile
24. Sub-techniques — 세분화된 공격 기법
25. Cyber Kill Chain — Lockheed Martin 7단계
26. UNC/APT 그룹 — APT 집합 명칭 (MITRE)
27. Diamond Model — 공격 분석 4要素 모델
28. Pyramid of Pain — 위협 Inteligence 가치 계층
29. OSINT (Open Source Intelligence) — 공개 출처 위협 정보
30. CVE/CVSS — 취약점 점수 체계
31. NVD (National Vulnerability Database) — NIST CVE DB
32. 인시던트 대응 (IR) — NIST 6단계
33. IR 단계 — 준비/식별/억제/근절/복구/교훈
34. IR 준비 — 대응 계획, 팀 구성, 교육
35. 식별 — 모니터링/알람→初步 분석
36. 억제 (Containment) — 단기(isolation)/장기(정상运营 복귀)
37. 근절 (Eradication) — 감염 원인 제거
38. 복구 — 시스템 정상화, 운영 재개
39. 교훈 (Lessons Learned) — 후속 조치, 보고서 작성
40. tabletop exercise —桌上演習, 시나리오 기반 연습
41. DFIR (Digital Forensics and Incident Response) — 디지털 포렌식+IR
42. 포렌식 4원칙 — 순수성/재현성/검증/객관성
43. 증거 보전 —write blocker, integrity hashing
44. Chain of Custody — 증거 이동/처리 기록
45. 메모리 포렌식 — Volatility, Rekall
46. RAM Dump — 물리 메모리 덤프
47. 페이지 파일 분석 — pagefile.sys, hiberfil.sys
48. 네트워크 포렌식 — PCAP, NetFlow, DNS 로그
49. 로그 보전 — syslog, Windows Event, Firewall 로그
50. 타임라인 분석 — 이벤트 시간순 재구성
51. MFT 분석 — Windows NTFS 메타데이터
52. 레지스트리 분석 — NTUSER.DAT, SAM, SECURITY hive
53. 스텔스 기법 — anti-forensics, 로그 삭제
54.anti-forensics — 증거 인멸/변조 기술
55.脆弱点 スキャン — Nessus, OpenVAS, Qualys
56. 침투 테스트 — 합법적 해킹 시뮬레이션
57. PTES — Penetration Testing Execution Standard
58. OWASP Testing Guide — 웹 앱 테스트 가이드
59. OSSTMM — 보안 테스트 방법론
60. 버그 바운티 — 공개 취약점 보상 프로그램

---

## 14. 보안 운영 심화 / 위협 헌팅 — 40개

1. 레드팀 — 적대적 관점, 실제 공격 시뮬레이션
2. 블루팀 — 방어 관점, 탐지/대응
3. 퍼플팀 — 레드+블루 협력
4. White Team — 시나리오 관리/심사
5. 적대적 시뮬레이션 — Red Team vs Purple Team exercises
6. 가정 침투 (Assumed Breach) — 내부 접근 가정
7. BAS (Breach and Attack Simulation) — 자동화된 공격 시뮬레이션
8. Purple Team — 공격/방어 협력, 탐지 규칙 개선
9. 위협 헌팅 (Threat Hunting) — 가설 기반 선제적 탐색
10. Huntington 가설 — "공격자는 이미 내부에 있다"
11. Hunting Loop —가설/탐색/발견/정보 공유
12. MITRE Engage — 방어적 사이버 전략 프레임워크
13. Deception Technology —蜜罐/蜜网/ canary token
14. Honey Pot — 유인 시스템
15. Honey Net — 유인 네트워크 세그먼트
16. Canary Token — 조기 탐지용 경보
17. 파일 canary — 조기 침해 탐지
18. 브라우저 canary — 세션 탈취 탐지
19. 포렌식 이미지 — DD, FTK Imager
20. MD5/SHA-256 해시 — 증거 무결성 검증
21. FTK / EnCase — 포렌식 도구
22. AXIOM — Magnet Forensics 포렌식
23. UAC绕过 — 사용자 계정 컨트롤 우回
24. LSASS 추출 — Mimikatz, procdump
25. SAM hive 추출 — reg save HKLM\SAM
26. Kerberoasting — SPN 요청 티켓 hash 추출
27. AS-REP Roasting — 사전 인증 미사용 계정 공격
28. DCSync — DC에서 크리덴셜Replication 요청
29. NTDS.dit 추출 — DC 데이터베이스 직접 추출
30. BloodHound — AD 공격 경로 분석 도구
31. CrackMapExec — 네트워크 크리덴셜 공격 도구
32. Empire / PowerShell Empire — 포스트-침투 프레임워크
33. Cobalt Strike — 상업용 침투 테스트 도구
34. Sliver — 오픈소스 C2 프레임워크
35. Caldera — MITRE 자동화 적대적 시뮬레이션
36. Red Canary — EDR,威胁検出
37. osquery —Endpoint 시각화/쿼리
38. Sysmon — Windows 시스템 모니터링
39. Zeek — 네트워크 트래픽 분석
40. YARA — 악성코드 패턴 규칙

---

## 15. 악성코드 / 공격 기법 — 60개

1. 악성코드 분류 — 바이러스/웜/트로이목마/랜섬웨어/스파이웨어/루트킷
2. 바이러스 (Virus) — 정상 파일에感染, 자기 복제
3. 웹orm — 네트워크 통해 само복제, 독립 실행
4. 네트워크 웜 — 취약점 직접 침투 (Code Red, SQL Slammer)
5. 이메일 웜 — 메일附件/링크 (ILOVEYOU)
6. 트로이목마 — 겉보기에 정상, 실질적으로 악성
7.バックドア — 정상software伪装된 후면入口
8. 드롭퍼 (Dropper) — 다단계 Downloader
9. Downloader — 원격에서 추가 악성코드 가져옴
10. 랜섬웨어 (Ransomware) — 파일 암호화 후 몸값
11. CryptoLocker — 2014년 대규모 랜섬웨어
12. WannaCry — 2017년 글로벌, EternalBlue 활용
13. NotPetya — 2017년 Ukraine 전력网攻击
14. Ryuk — 목표형 대규모 랜섬웨어
15. 이중extortion — 암호화+데이터 유출
16. RaaS (Ransomware as a Service) — 랜섬웨어 임대 서비스
17.Locker — 화면 잠금형 Ransomware
18. wipers — 데이터 파괴 목적
19. 스파이웨어 (Spyware) — 사용자 활동 감시
20. 키로거 — 키入力 기록
21. 广告软件 (Adware) — 강제 광고 표시
22.cryptominer — 시스템 자원 활용 암호화폐 채굴
23.bots — 명령 制圧力 갖춘 감염 호스트
24. botnet — 다수의 bots 집합
25. botnet 구조 — 중앙집중형 (C&C)/P2P
26. C2 (Command and Control) — 봇넷 지휘 통제
27. Cobalt Strike — 침투 테스트용 C2
28. APT (Advanced Persistent Threat) — 국가/조직적 위협
29. APT 그룹 — Lazarus(北한국), FIN7(범죄조직), APT29(러시아)
30. APT 공격 단계 — 정찰/침투/내부정찰/横向移动/유지/데이터반출
31. First Initial Access — 최초 침투 수단
32. 피싱 (Phishing) — 가장 일반적인 침투 수단
33. 스피어 피싱 (Spear Phishing) — 목표 맞춤형
34. 웨일링 (Whaling) — 임원 대상 고대상 피싱
35. BEC (Business Email Compromise) — 경영자 사칭 금융 사기
36. 스미싱 (Smishing) — SMS 기반 피싱
37. 비싱 (Vishing) — 전화 기반 피싱
38. 사전조사 (Pretexting) — 거짓 상황 구성
39. 테일게이팅 (Tailgating) — 따라 들어가기
40. 버스딩 (Busybasing) —注意力转移
41. 제로데이 — 공개되지 않은 취약점 利用
42. watering hole — 목표 집합 자주 방문 사이트 감염
43. drive-by download — 악성 사이트 접근만으로 감염
44.供应链攻击 — 소프트웨어 개발망 침해 (SolarWinds)
45. 업데이트 역추적 (Update Interception) — 자동更新 가로채기
46. 다형성 (Polymorphic) — 암호화된 코드,侦码 변경
47. 메타모픽 (Metamorphic) — 코드 자체 변환
48. armored virus —侦码 회피를 위한 보호 层
49. 파일리스 (Fileless) — 메모리만 사용, 파일 없는 공격
50. LOLBins (Living Off the Land) — 정당한 도구 활용
51. PowerShell 공격 — 메모리 내 스크립트 실행
52. WMI 공격 — WMI 이벤트消费者 활용
53. JScript/VBScript 공격 — 스크립트 기반
54. 레지스트리 런키 — 자동 실행 등록 정보
55. 예약 작업 (Scheduled Task) — 정기적 실행
56. 서비스 등록 — Windows 서비스로潜伏
57. DNS 터널링 — DNS 프로토콜 내 데이터 반출
58. ICMP 터널링 — ICMP 패킷 내 데이터 운반
59. HTTPS 역투명 relay — 내부망 통신 외부로
60. 동적 프록시 — 감염 호스트를 Proxy로 활용

---

## 16. 데이터 / 개인정보 보호 — 55개

1. 개인정보 (Personal Information) — 재识别 가능 정보
2. 민감정보 — 건강/범죄기록/유전정보/ biometric
3. 개인정보보호법 (한국) — 수집/처리/提供/파기 원칙
4. 개인정보 3대 원칙 — 수집 제한/목적 명확/보유 기간
5. 개인정보 영향평가 (PIA) — 고위험 처리前 평가
6. 개인정보 파일 표준 protection 지침 — 한국 개인정보보호법 시행규칙
7. 정보보호 管理체계 (ISMS-P) — 한국 통합 인증
8. 정보통신서비스提供者 (ISP) — 한국법상 의무
9. 利用약관 — 서비스 제공을 위한 기본 계약
10. 동의 방식 — 필수 동의/선택 동의
11. GDPR (EU General Data Protection Regulation) — 2018 시행
12. GDPR 6가지 처리 근거나유 — 동의/계약/법적 의무/생명 보호/공익/정당한 이해관계
13. 정보 주체 권리 — 접근/정정/삭제/처리 제한/이동/거부
14. Right to be Forgotten — 삭제권 (GDPR 17조)
15. Data Portability — 이동권 (GDPR 20조)
16. DPIA (Data Protection Impact Assessment) — GDPR 의무
17. DPO (Data Protection Officer) — 개인정보 보호관
18. Breach Notification — 72시간 내 신고 의무
19. 개인정보 해외 이전 — 충분성 인정 국가/표준 계약 조항
20. CCPA (California Consumer Privacy Act) — 2020 시행
21. CPRA (California Privacy Rights Act) — CCPA 강화
22. PDPA (Personal Data Protection Act) — 싱가포르
23. 개인정보보호 法律体系 — 한국/미국/EU 비교
24. ISMS-P 심사 — 기술적/관리적/물리적 安全 Control 평가
25. 정보보호 주요安全管理 —
26. 개인정보 유출 사고 — 신고/통지/공표 의무
27. 과태료/벌칙 — 한국 개인정보보호법 제64조
28. 데이터 분류 — 공개/내부/기밀/극비
29. 데이터 주권 — 국가별 데이터本地화 법規
30. 데이터 이동 — Cross-border 데이터 흐름
31. 클라우드 개인정보보호 — 데이터 소재지 주의
32. 데이터匿名화 — 완전히 역추적 불가능
33. 데이터가명화 — 식별가능성 제거,pseudo-anonymization
34. k-익명성 — k-person indistinguishability
35. l-다양성 — 민감 속성 다변화
36. t-근접성 — 레코드 분포 유사성
37. 차분 개인정보보호 — differential privacy
38. 합성 데이터 — Synthetic data 생성
39. 데이터 마스킹 — 동적/정적 마스킹
40. 토큰화 (Tokenization) — 원본↔토큰 매핑
41. TTT (Tokenization-as-a-Service) — 클라우드 토큰화
42. Format Preserving Encryption — FPE, 원 데이터 형식 유지
43. DLP (Data Loss Prevention) — 데이터 반출 방지
44. DLP 구성要素 —엔진/에이전트/서버
45. DLP 정책 — 콘텐츠 검사/컨텍스트 기반
46. 네트워크 DLP — 네트워크 경계 데이터 통제
47. 엔드포인트 DLP — 단말기 내 데이터 통제
48. 클라우드 DLP — SaaS/ PaaS/IaaS 데이터 보호
49. CASB (Cloud Access Security Broker) — 클라우드 가시성/제어
50. 데이터베이스 보안 — 접근 통제/암호화/감사
51. 필드 레벨 보안 — DB 컬럼/행 수준 접근 제어
52. DB 감사 — 접속 기록, 질의 로그
53. 전송 중 암호화 — TLS, IPsec
54. 저장 중 암호화 — TDE, 디스크 암호화
55. 메모리 내 암호화 — 클라우드 HSM

---

## 17. 보안 프레임워크 / 컴플라이언스 — 55개

1. ISO/IEC 27001 — 정보보안 management 시스템 (ISMS)
2. ISMS 인증 — 3자 감사, 인증서 발급
3. PDCA (Plan-Do-Check-Act) — 관리 시스템 적용 모델
4. ISO 27001 114개 통제 — Annex A
5. ISO/IEC 27002 — 보안 통제 implementation 지침
6. ISO/IEC 27005 — 정보보안 위험 관리
7. ISO 27017 — 클라우드 서비스 보안 통제
8. ISO 27018 — 클라우드 PII 보호
9. ISO 27701 — 개인정보보호 정보安全管理
10. ISO 22301 — 사업 연속성 관리 시스템 (BCMS)
11. NIST CSF 2.0 —Identify/Protect/Detect/Respond/Recover + Govern
12. NIST CSF Tier — Risk Inform/Repeatable/Adaptive
13. NIST SP 800-53 — 연방 정보시스템 보안 통제 (800+ 통제)
14. NIST SP 800-171 — CUI 보호 (110 통제)
15. NIST SP 800-207 — 제로 트러스트 아키텍처
16. NIST SP 800-63 — 디지털 신원 지침
17. NIST SP 800-63A — Enrollment and Identity Proofing
18. NIST SP 800-63B — Authentication and Lifecycle
19. NIST SP 800-63C — Federation and Assertions
20. SOC 2 — AICPA 서비스 조직 통제 보고서
21. SOC 2 Trust Service Criteria — 보안/가용성/처리 무결성/机密性/隐私
22. SOC 2 Type I/II — 설계 적정성/운영 효과성
23. SOC 3 — 공용 버전 SOC 2
24. PCI DSS v4.0 — Payment Card Industry Data Security Standard
25. PCI DSS 12개 요구사항 — 방화벽/비밀번호/데이터 보호 등
26. PCI DSS 수준 —merchant/service provider 등급
27. PA-DSS — Payment Application Data Security Standard
28. HIPAA — 미국 의료정보 보호법
29. PHI (Protected Health Information) — HIPAA 적용 정보
30. HITECH — 미국 의료기술법, 위반 시 책임 강화
31. GLBA (Gramm-Leach-Bliley Act) — 미국 금융정보보호
32. FERPA — 미국 교육 기록 프라이버시
33. CMMC (Cybersecurity Maturity Model Certification) — 미국 방위산업
34. CMMC 5단계 — Level 1~5 점진적 인증
35. FISMA — 미국 연방 정보 보안 법
36. FedRAMP — 미국 정부 클라우드 보안 인증
37. FedRAMP Moderate/High — 영향 수준별 기준
38. ITGrc — IT 거버넌스/리스크/컴플라이언스
39. SABSA —Business-driven 보안 아키텍처
40. TOGAF — 기업 아키텍처 프레임워크
41. Zachman Framework — EA planning 매트릭스
42. CIS Controls v8 — 18개 핵심 보안 통제
43. CIS Safeguard — Implement/M测量/관리
44. COBIT 2019 — IT 거버넌스 프레임워크
45. ITIL (Information Technology Infrastructure Library) — IT 서비스 관리
46. Privacy by Design — 설계 단계 개인정보 보호
47. PbD 7基本原则 — 사전 보호/기본값私密性 등
48. CC (Common Criteria) / ISO 15408 — 제품 보안 인증
49. CC EAL — 평가 보증 수준 (EAL 1~7)
50. FIPS 140-2/3 — 암호 모듈 보안 표준
51. K-ISMS — 한국 정보보호管理체계 인증
52. 정보보호평가 — 한국互联网振興院 (KISA)
53. 전자금융감독규정 — 금융 전산 보안 기준
54. 금융감독원 (FSS) — 금융 사이버 감독
55. SBOM (Software Bill of Materials) — 소프트웨어 부품 목록

---

## 18. IoT / OT / ICS / 물리 보안 — 50개

1. OT (Operational Technology) — 운영기술, 산업控制系统
2. OT vs IT — reliability/availability/real-time 차이
3. ICS (Industrial Control System) — 산업 제어 시스템
4. SCADA (Supervisory Control and Data Acquisition) — 원격 감시 제어
5. DCS (Distributed Control System) — 분산 제어 시스템
6. PLC (Programmable Logic Controller) — 현장 제어기
7. RTU (Remote Terminal Unit) — 원격 터미널 장치
8. Modbus 프로토콜 — 산업용 직렬 통신, 암호화 없음
9. DNP3 — 전력/상하수도 SCADA 프로토콜
10. PROFINET — 산업용 이더넷
11. EtherNet/IP — CIP 기반 산업용 이더넷
12. Purdue 모델 — IT/OT 네트워크 5단계分层
13. Purdue 레벨 0~5 — Field/Level 1~2 (OT)/Level 3 (DMZ)/Level 4~5 (IT)
14. IEC 62443 — 산업 사이버보안 표준
15. ISA/IEC 62443 보안 레벨 — SL 0~4 (no security→most secure)
16. SL-CF (Security Level Capability) — 시설 보안 수준
17. SL-TF (Security Level Target) — 목표 보안 수준
18. Zone/Conduit 모델 — 구역 분리+ conduits통제
19. Zone 맵핑 — 자산 분류→ security level
20. NIST IR 8259 — IoT 보안基礎
21. NIST IR 8259D — IoT 제조 商arangement
22. OWASP IoT Top 10 — 취약한 펌웨어/기본 계정/불안전한 接口
23. IoT 보안 설계 —Secure by Default, 최소 기능 원칙
24. IoT 펌웨어 보안 — 서명 검증, 안전 업데이트
25. IoT 데이터 보안 —保存中/传输中/處理中
26. Secure Boot — 부팅 과정 소프트웨어 무결성 검증
27. rantai-root-of-trust — 신뢰의 근원
28. RoT 구성要素 — CRTM, Bootloader, Bootloader certificates
29. Measured Boot — TPM利用, boot 측정값 기록
30. 펌웨어 업데이트 보안 —签名驗證, 롤백 방지
31. MQTT 보안 — TLS, 인증, ACL
32. BACnet — 건물 자동화 프로토콜
33.，车辆网络安全 — UNECE WP.29
34. ISO/SAE 21434 — 자동차 사이버보안 엔지니어링
35. TARA (Threat Analysis and Risk Assessment) — 자동차 위협 분석
36. 의료기기 보안 — FDA cybersecurity 지침
37. 의료기기 사이버보안 관리 — 디자인 단계부터
38. 스마트 그리드 보안 — AMI 보안
39. NERC CIP — 북미 전력 신뢰성 Corporation
40. 원자력 사이버보안 — IAEA 안전기준
41. 위성 통신 보안 —，抗ジャミング/스푸핑
42. 물리적 보안 3대 요소 —威慑/ Delay/ Detection
43. CCTV (閉路テレビ) — 영상 감시
44. 접근 제어 시스템 — 카드/RFID/바이오메트릭
45.Mantrap — 이중 문으로 인적 격리
46. 주변 보안 — 담장/감시/巡伺
47. 환경 통제 — 온도/습도/소화기
48. 서버실 보안 — Tier 1~4数据中心分级
49. Faraday Cage — 전자기 차폐
50. 금屬 탐지기/ X-ray — 물리적脅威 탐지

---

## 19. AI / 신기술 보안 — 50개

1. AI 보안 — AI 시스템의 安全+AI 활용 보안
2. 적대적 예제 (Adversarial Example) — 미세한 perturbation로 오분류
3. FGSM (Fast Gradient Sign Method) — 1단계 적대적扰动
4. PGD (Projected Gradient Descent) — 반복적 적대적扰动
5. Carlini-Wagner 공격 — 강력한 적대적 공격
6. 물리 세계 적대적 공격 — 도로 표지판 등 실환경 공격
7. 데이터 포이즈닝 (Data Poisoning) — 훈련 데이터 오염
8. Clean-Label Poisoning — 레이블 유지한 데이터 오염
9. Backdoor Attack — 특정 트리거 입력에 반응
10. 모델 추출 (Model Extraction) — 쿼리 기반 모델 역추출
11. Model Inversion — 훈련 데이터 재구성
12. Membership Inference — 특정 데이터 훈련 여부 추론
13.AI 모델 탈취 — API 쿼리로 모델 복제
14. 모델 무결성 공격 — 사본 배포, 악성 교체
15. 프롬프트 인젝션 — LLM 지시어 오버라이드
16. Jailbreaking — LLM 안전 필터 우회
17. 적대적 프롬프트 — 의도한 잘못된 출력 유도
18. 데이터 추출 공격 — 훈련 데이터 기억으로 정보 유출
19.AI 기반 피싱 — 개인화된 대규모 피싱 자동화
20. Deepfake — 합성 미디어, 신원 사칭
21. 딥페이크 탐지 — C2PA, 디지털 워터마킹
22. C2PA (Coalition for Content Provenance and Authenticity) — 콘텐츠 출처
23. SynthID — Google 딥마크
24. AI TRiSM — Gartner, AI 신뢰/위험/보안 관리
25. LLM 가드레일 — 출력 필터링, 안전 레이어
26. Constitutional AI — 원칙 기반 AI 행동 통제
27. AI Red Team — LLM 안전성 테스트
28.对抗性训练 — 적대적 예제 포함한 재훈련
29. differential privacy in ML — 훈련 데이터 privacy 보호
30. Federated Learning — 분산 훈련, 데이터 불이동
31. Homomorphic Encryption in ML — 암호화된 채로 추론
32. TEE 기반 ML — SGX 등에서 안전한 추론
33.Responsible AI — 공정성/설명가능성/투명성/ privacy
34. AI Incident — AI 관련 보안 사고DB
35. OWASP LLM Top 10 — LLM 보안 취약점
36. LLM01: Prompt Injection — 프롬프트 조작
37. LLM02: Insecure Output — 출력 검증 없이 신뢰
38. LLM03: Training Data Poisoning — 훈련 데이터 오염
39. LLM04: Model Denial of Service — 비용巨大的 입력 유발
40. LLM05: Supply Chain — 공급망 취약점
41. LLM06: Sensitive Information Disclosure — 훈련 데이터 유출
42. LLM07: Plugin Abuse — 플러그인 악용
43. LLM08: Autonomous Agent — 자가 실행 에이전트 위험
44. 양자 컴퓨팅 — 양자 중첩/얽힘으로 계산 혁신
45. 양자 위협 — RSA/ECC 깨뜨릴 Shor 알고리즘
46. Grover 알고리즘 — 대칭키 강도半감
47. NIST PQC 표준 — Kyber/Dilithium/Falcon/SPHINCS+
48. crypto agility — 알고리즘 교체 능력
49.区块链 보안 — 51% 공격, 이중지불, 스마트 컨트랙트
50. Reentrancy 공격 — 스마트 컨트랙트 재진입脆弱점

---

## 20. 보안 추가 키워드 / 시험 대비 — 40개

1. Evil Maid Attack — 물리적 접근 후 백도어 설치
2. Cold Boot Attack — 메모리 잔상 읽기
3. DMA 공격 — Thunderbolt/PCIe Direct Memory Access
4. Firewire 공격 — IEEE 1394 DMA 활용
5. Thunderbolt Security — DMA 방어를 위한 레벨 설정
6. USB_BAD — USB 키보드 emulation
7. Rubber Ducky — USB 키보드 emulation 도구
8. Bash Bunny — 다목적 USB 공격 도구
9. OMG Cable — 변형된 USB 케이블
10._entropy — 난수 생성 품질
11. CSPRNG (Cryptographically Secure PRNG) — 암호학적으로 안전한 난수
12. RDRAND (Intel) — 하드웨어 난수 생성
13. /dev/urandom — Linux 난수 장치
14. hardware RNG — 물리적 난수 발생기
15. entropy source — 난수 생성 원천
16. Perfect Security — 정보 이론적 안전 (One-Time Pad)
17. Semantic Security — 암호학적으로 관찰 가능한 차이 없음
18. IND-CPA / IND-CCA2 — 암호학 안전성 정의
19. AEAD — 인증된 암호화+연관 데이터
20. Key Wrapping — 키 자체를 암호화하는 KEK 활용
21. Envelope Encryption — 데이터 키로 데이터 암호화, KEK로 데이터 키 암호화
22. CloudHSM — 클라우드 관리형 HSM
23. AWS KMS — 키 관리 서비스
24. Bring Your Own Key (BYOK) — 고객 관리 키
25. Hold Your Own Key (HYOK) — 온프레미스 키 사용
26. Zero Knowledge Proof — 비밀을 밝히지 않고 지식 증명
27. Commitment Scheme — 값을 숨기면서後で 공개
28. Secure Multi-Party Computation — 복수 당사자 협력 연산
29. Homomorphic Encryption — 암호문 간 연산
30. Functional Encryption — 함수 유형별 복호화 권한
31. Searchable Encryption — 암호문 내 키워드 검색
32. 防篡改硬件 — 변조 방지芯片 (TPM/HSM)
33. Secure Enclave — ARM TrustZone, 격리된 보안 영역
34. Trusted Execution Environment — TEE, 격리 실행 환경
35. Security Chaos Engineering — 의도적 장애로 보안 검증
36. 침해 시뮬레이션 — ATT&CK 기반 Purple Team 연습
37. 사이버 보험 —.cyber insurance, 위험 전가
38. Bug Bounty — 공개 취약점 보상
39. Responsible Disclosure — 즉시 공개 대신 제조사에 먼저 보고
40. Coordinated Disclosure — 집단적 공개

---

**총 키워드 수: 800개**
