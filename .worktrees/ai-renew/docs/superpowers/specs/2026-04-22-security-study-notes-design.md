# Spec: Security Study Notes (OAuth 2.0, OIDC, Web Security)

## 1. Goal
Create 20 high-quality study note files in `content/studynote/09_security/05_web_app_security/` for keywords #505 and #507 to #525. These files must follow `PE_GUIDELINE.md` and `PE_EXAMPLE.md` strictly.

## 2. Target Files & Key Content
### OAuth 2.0 & Tokens (Batch 1)
- **505. Refresh Token**: Focus on token rotation, expiration management, and security (XSS vs CSRF).
- **507. OAuth 2.0 4가지 Grant**: Overview of Authorization Code, Implicit (deprecated), Client Credentials, ROP. Mention PKCE as the modern standard.
- **508. Authorization Code Grant**: Detailed flow with `redirect_uri` validation and CSRF protection (state).
- **509. PKCE (Proof Key for Code Exchange)**: How it prevents code interception in public clients (Code Verifier/Challenge).
- **510. Open Redirect**: Attack vector via manipulated `redirect_uri` in OAuth flows.
- **511. Token Leakage**: Common leak points (Referer, URL, Log, Browser History).
- **512. Scope**: Principle of Least Privilege in OAuth.
- **513. Access Token vs Refresh Token**: Comparison table of lifespan, storage, and usage.

### OpenID Connect (OIDC) (Batch 2)
- **514. OIDC**: The identity layer on top of OAuth 2.0.
- **515. ID Token**: JWT structure, claims (iss, sub, aud, exp, iat).
- **516. ID Token vs Access Token**: Identity vs Authorization distinction.
- **517. Discovery Document**: `.well-known/openid-configuration` content and usage.
- **518. jwks_uri**: Public key retrieval for JWT verification.
- **519. Nonce**: Replay attack prevention in OIDC flows.

### Web Infrastructure & Smuggling (Batch 3)
- **520. Rate Limiting**: Algorithms (Token Bucket, Leaky Bucket) and DoS prevention.
- **521. WAF 규칙**: OWASP CRS (Core Rule Set) scoring and anomaly detection.
- **522. ModSecurity Core Rule Set**: Generic vs Specific rules, tuning.
- **523. HTTP Request Smuggling**: The concept of desynchronization between Front-end and Back-end.
- **524. HTTP Request Smuggling (CL.TE, TE.CL, H2.CL)**: Detailed diagrams of each type.
- **525. HTTP Response Smuggling**: Response splitting and cache poisoning.

## 3. Visual Requirements (ASCII Diagrams)
- **OAuth/OIDC Flows**: Sequential sequence diagrams.
- **Smuggling (523-525)**: Diagrams showing the difference in `Content-Length` (CL) and `Transfer-Encoding` (TE) interpretation.
  - Front-end sees one request, Back-end sees two (or vice versa).

## 4. Compliance Checklist
- [ ] Language: Korean
- [ ] Format: Section I-V + 관련 개념 맵 + 어린이 비유
- [ ] Section 요약 비유 included in every section
- [ ] References to 506 (OAuth 2.0) in 507
- [ ] Date: 2026-04-22
- [ ] Categories: "studynote-security"
- [ ] Weight: Corresponding keyword number
