+++
title = "530. SMI (Structure of Management Information)"
weight = 530
+++
# 530. SMI (Structure of Management Information)

> **핵심 인사이트**: SNMP 통신을 할 때 MIB라는 전화번호부(트리)를 쓰는 것은 알았다. 그런데 그 전화번호부에 이름을 적을 때 "반드시 1바이트짜리 정수로 적어라", "글자는 ASCII 코드로만 적어라"처럼 데이터를 적는 **'문법과 규칙'** 이 필요한데, 이것이 바로 SMI다.

## Ⅰ. SMI (Structure of Management Information)의 개념
SNMP 프레임워크에서 **MIB(Management Information Base)를 정의하고 구축하기 위한 문법적이고 논리적인 규칙(구조)** 을 의미합니다. (RFC 1155, 2578)
네트워크 장비마다 제조사가 다르고 하드웨어가 다르더라도, SNMP 매니저와 에이전트 간에 오가는 데이터(예: 온도, 트래픽 양, 이름)의 '형식(Data Type)'과 '이름 부여 방식'을 통일하기 위해 IETF에서 만든 엄격한 문법 체계입니다.

## Ⅱ. SMI의 3가지 핵심 규칙 구성 요소

1. **객체 식별자 (Object Identifier, OID)**
   - MIB 트리 구조에서 각각의 객체(관리 정보)에 어떻게 점(Dot, `.1.3.6...`)을 찍어서 고유한 이름을 부여할 것인지 그 체계를 정의합니다.
2. **구문 / 데이터 타입 (Syntax / Data Types)**
   - 관리 객체가 어떤 형태의 값을 가질 수 있는지 제한합니다. SMI는 ASN.1 (Abstract Syntax Notation One)이라는 범용 데이터 표기법의 부분집합을 사용합니다.
   - **기본 타입**: `INTEGER` (정수), `OCTET STRING` (문자열), `OBJECT IDENTIFIER` (OID 주소)
   - **애플리케이션 타입**: 네트워크 관리에 특화된 타입들로, `IpAddress` (IP 주소), `Counter32` (계속 증가만 하는 누적 값), `Gauge32` (올라갔다 내려갔다 하는 값, 예: 온도), `TimeTicks` (장비 부팅 후 지난 시간) 등이 있습니다.
3. **객체의 부가 정보 (Encoding / Encoding Rules)**
   - 데이터를 실제 네트워크 선로로 전송할 때, 이 값들을 어떻게 0과 1의 비트열로 인코딩(BER, Basic Encoding Rules)할 것인지에 대한 규칙을 포함합니다.

## Ⅲ. SNMP 통신 시 SMI의 역할
SNMP 매니저가 라우터에게 "현재 인바운드 트래픽 양(InOctets)"을 물어봤을 때, 라우터(Agent)는 **SMI 규칙에 따라 해당 값을 `Counter32` 타입으로 포장하여 응답**합니다. 매니저 역시 SMI 규칙을 알고 있으므로, 받은 값이 무조건 증가만 하는 카운터 값임을 인지하고 이전 값과의 차이를 계산하여 트래픽 대역폭(bps) 그래프를 그려냅니다.

> 📢 **섹션 요약 비유**: 한글로 이력서를 쓸 때, "이름 칸에는 반드시 한글 3자만 적으시오(Syntax)", "생년월일 칸에는 YYYYMMDD 숫자 8자리만 적으시오(Type)"라고 정해둔 **'입력 서식 규칙'** 입니다. 이 규칙(SMI)이 있어야 전국 어디서 올라온 이력서(MIB)든 본사(SNMP 매니저)가 오류 없이 깔끔하게 전산망에 입력할 수 있습니다.
