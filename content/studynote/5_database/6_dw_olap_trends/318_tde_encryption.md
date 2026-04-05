+++
title = "318. TDE / 암호화"
weight = 4318
+++

> **💡 핵심 인사이트**
> TDE(Transparent Data Encryption, 투명한 데이터 암호화)는 **"애플리케이션의 SQL 코드나 쿼리를 수정하지 않고, DBMS가磁盘에 데이터를 저장하는 순간 자동으로 암호화하고, 읽어올 때 자동으로 복호화하는 투명한 암호화 레이어"**입니다.
> 개발자나 DBA가意識하지 않는 채 기존 인터페이스(SQL)를 그대로 사용하면서, **存储 시점(At Rest)의 데이터가 암호화되어物理적으로 보호**됩니다. 키 관리는 DBMS 외부(Hardware Security Module, KMIP 등)에서 수행하여, DBMS가 해킹되어도 키 없이 평문을얻을 수 없는 구조입니다.

---

## Ⅰ. 데이터 암호화의 필요성:硬盘放任시 보안 문제

**어떤 경우에 평문 데이터가 노출되는가:**

```
[평문 데이터 노출 시나리오]

  1. 디스크 도난/분실
     - 서버 하드웨어 통째로 도난
     - ("우리의 RAID 배열이小偷에 의해 반출")

  2. 백업 파일 탈취
     - S3 버킷의 DB 백업 파일이_public으로 설정
     - ("백업 파일을 압축 풀었더니 customers 테이블이 텍스트로...")

  3. 관리자 권한 남용
     - DBA가 Curiosity에驱动되어 고객 정보 열람
     - (접근 통제로는 防げない 내부 위협)

  4. OS/Hypervisor 层漏洞
     - VMotion 중 메모리 덤프 취득
     - (VM의 메모리 이미지에 평문 데이터가 있을 수 있음)

  5. 로그/코어 덤프
     - 장애 시 생성되는 덤프 파일에 平文이 섞여 있음
```

**TDE는 위 모든 시나리오에서 "硬盘단위로 보호"합니다.**

---

## Ⅱ. TDE의 작동 원리: 키의 구조

TDE는 **2단계 키 구조(DEK + MEK)**를 사용합니다:

```
[TDE 암호화 아키텍처]

  ┌──────────────────────────────────────────────────────┐
  │                  Application Layer                    │
  │              (SQL 입력/결과, 변경 없음)               │
  └──────────────────────────┬───────────────────────────┘
                             │ 평문 SQL
  ┌──────────────────────────▼───────────────────────────┐
  │                    DBMS Engine                        │
  │   ┌─────────────────────────────────────────────┐   │
  │   │           Encryption/Decryption Layer         │   │
  │   │                                             │   │
  │   │  Insert → TDE가 데이터 파일에 저장 전 암호화  │   │
  │   │  Select → TDE가 디스크에서 읽은 직후 복호화   │   │
  │   │  (애플리케이션视角: "그냥 보통 SQL")           │   │
  │   └─────────────────────────────────────────────┘   │
  └──────────────────────────┬───────────────────────────┘
                             │ 암호문 (Encrypted Data)
  ┌──────────────────────────▼───────────────────────────┐
  │               Disk / Storage Layer                   │
  │  ┌─────────────────────────────────────────────┐    │
  │  │         Encrypted Data File (.mdf/.ibd)     │    │
  │  │  ← 디스크에서 이 파일을 읽으면?               │    │
  │  │    "가장 男의 소설 42화"처럼 無意味한 데이터  │    │
  │  └─────────────────────────────────────────────┘    │
  └──────────────────────────────────────────────────────┘
                             │
  ┌──────────────────────────▼───────────────────────────┐
  │            External Key Management (외부)             │
  │   ┌─────────────────────────────────────────────┐   │
  │   │  MEK (Master Key): KMIP 서버/Hardware HSM   │   │
  │   │  DEK (Data Encryption Key): DBMS 내부 저장   │   │
  │   │  ← MEK 없으면 DEK를 解読不能                 │   │
  │   └─────────────────────────────────────────────┘   │
  └──────────────────────────────────────────────────────┘
```

**키 역할 분담:**
- **DEK (Data Encryption Key)**: DBMS 내 존재, 실제 데이터 암/복호화에 사용
- **MEK (Master Encryption Key)**: HSM(하드웨어 보안 모듈)이나 KMIP 서버에 저장, DEK 자체를 암호화
- **방어 심화**: DBMS가 털려도 MEK가 없으면 DEK를 복호화할 수 없음

---

## Ⅲ. TDE의 실제 구현: Oracle, SQL Server, PostgreSQL

### Oracle TDE

```sql
-- Oracle TDE 설정
ADMINISTER KEY MANAGEMENT CREATE KEYSTORE 'wallet_location'
  IDENTIFIED BY "wallet_password";

ADMINISTER KEY MANAGEMENT CREATE ENCRYPTION KEY
  keystore 'wallet_location'
  IDENTIFIED BY "wallet_password"
  WITH BACKUP USING KEY 'oracle_key';

-- 테이블 스페이스 암호화
CREATE TABLESPACE encrypted_ts
DATAFILE '/u01/oracle/data/enc.dbf'
ENCRYPTION USING 'AES256'
DEFAULT STORAGE (ENCRYPT);
```

### PostgreSQL (pg_encryption, AWS RDS 암호화)

```sql
-- PostgreSQL TDE는 extensions로 제공
-- AWS Aurora PostgreSQL의 경우:
-- DB 생성 시 KMS 키 지정 → 자동으로 DEK 관리

-- 테이블 스페이스 암호화 (pg_tde插件)
CREATE TABLESPACE encrypted_ts LOCATION '/pgdata/encrypted';
-- 설정 파일에서 KMS 키 지정
```

### SQL Server TDE

```sql
-- SQL Server TDE
USE master;
GO

CREATE DATABASE ENCRYPTION KEY
WITH ALGORITHM = AES_256
ENCRYPTION BY SERVER CERTIFICATE MyServerCert;
GO

ALTER DATABASE MyDB
SET ENCRYPTION ON;
GO

-- tempdb도 암호화 (권장)
ALTER DATABASE tempdb SET ENCRYPTION ON;
```

---

## Ⅳ. TDE의 한계와 보완 전략

**TDE가 보호하지 못하는 것:**

| 보호 범위 | 보호 불가 범위 |
|----------|---------------|
|磁盘 저장 데이터 (At Rest) | 메모리 내 데이터 (In Motion, In Use) |
| 백업 파일 | 네트워크 구간 (TLS 필요) |
| 디스크 physically 도난 | DB 접속 사용자의 잘못된 쿼리 결과 |
| | SQL 인젝션으로 인한 데이터 유출 |

```
[TDE + 其他 보안 수단의 조합]

  ┌──────────────────────────────────────────────┐
  │         방어 심도 (Defense in Depth)           │
  │                                               │
  │  Layer 1: TDE (Disk 암호화)                    │
  │           →硬盘 도난, 백업 파일 유출 방지       │
  │                                               │
  │  Layer 2: TLS/SSL (전송 암호화)                │
  │           →네트워크 도청 방지                  │
  │                                               │
  │  Layer 3: 접근 통제 (RBAC,最小권한)            │
  │           →불필요한 접근 차단                  │
  │                                               │
  │  Layer 4: 행/컬럼 레벨 보안 (RLS, CLS)         │
  │           →민감 데이터 部分만 보호             │
  │                                               │
  │  Layer 5: 데이터 마스킹 (Dynamic Masking)       │
  │           →응용 프로그램 레벨 보호             │
  │                                               │
  │  Layer 6: DB 감사 로깅 (Auditing)              │
  │           →위반 사항 탐지                     │
  └──────────────────────────────────────────────┘
```

---

## Ⅴ. 키 관리와 📢 비유

**KMIP (Key Management Interoperability Protocol):**
- 키 관리 상호운용성 프로토콜 (OASIS 표준)
- 다양한 KMS(HashiCorp Vault, AWS KMS, Azure Key Vault)와 DBMS 간 키 관리标准化
- PKCS#11, JCE 등과의 연동

** principales 키 관리 원칙:**
1. **키 분리 (Key Separation)**: 암호화에 사용하는 키와 키를 암호화하는 키를 분리
2. **키 순환 (Key Rotation)**: 정기적인 키 교체 (보통 1~2년)
3. **키 폐기 (Key Destruction)**: 키 삭제 시 데이터 영구 복구不能 (Bit Commitment 이슈)

> 📢 **섹션 요약 비유:** TDE는 **"은행 金庫의 자동 문 잠금 장치"**와 같습니다. 직원이 문을 닫으면 자동으로 잠기고, 열쇠(키)를 가진 사람만이 열 수 있습니다. 직원이 안에 있을 때는 (메모리에 데이터가 로드된 상태) 평문으로 작동하지만, 직원이 퇴근하고 금고가关闭되면 (디스크 저장 시) 자동으로 암호화됩니다. 그리고 금고의 열쇠를 금고관리회사(HSM/KMIP)가 별도 관리하기 때문에, 은행 직원이 금고를 열쇠를 가지고 있다고 해도 금고관리회사가 동의하지 않으면 열 수 없습니다. **"데이터는金庫 안에 있을 때 자동으로 보호되는"** 것이 핵심입니다.
