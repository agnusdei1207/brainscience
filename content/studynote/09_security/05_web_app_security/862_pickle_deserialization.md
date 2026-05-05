+++
weight = 862
title = "862. pickle Deserialization (Python Pickle Insecure Deserialization)"
date = "2026-04-21"
[extra]
categories = "studynote-security"
+++
## 0. 핵심 인사이트

> **핵심**: Python `pickle` 모듈의 역직렬화는 `__reduce__` 메서드를 통해 임의 Python 코드를 실행할 수 있어, 신뢰할 수 없는 데이터를 `pickle.loads()`로 처리하는 것은 즉각적인 RCE 위험이다.
> 2. **가치**: ML (Machine Learning) 모델 파일(.pkl, .pt)이 pickle 형식으로 저장되는 경우가 많아, AI/ML 파이프라인이 새로운 역직렬화 공격 표면으로 부상하고 있다.
> 3. **판단 포인트**: pickle을 외부 입력 처리에 절대 사용하지 않는 것이 유일한 완전 방어이며, ML 모델도 Safetensors, ONNX 같은 안전한 포맷으로 저장해야 한다.

> 📝 모범 답안

---

## 1. 개요 및 필요성

Python의 `pickle` 모듈은 Python 객체를 직렬화·역직렬화하는 표준 라이브러리다. 그러나 Python 공식 문서에 명시적으로 "신뢰할 수 없는 데이터는 절대 역직렬화하지 마세요"라고 경고할 만큼 위험하다.

pickle이 위험한 이유는 역직렬화 시 `__reduce__` 메서드가 자동으로 호출되며, 이 메서드가 `os.system()`, `subprocess.Popen()` 등 임의 명령을 실행할 수 있기 때문이다. Java의 가젯 체인처럼 중간 단계 없이 직접 코드를 삽입할 수 있어 오히려 더 단순하고 강력하다.

```text
┌──────────────────────────────────────────────────────────────┐
│            Python pickle RCE 페이로드                        │
├──────────────────────────────────────────────────────────────┤
│  import pickle, os                                           │
│                                                              │
│  class Exploit(object):                                      │
│      def __reduce__(self):                                   │
│          return (os.system, ('id && whoami',))               │
│                                                              │
│  payload = pickle.dumps(Exploit())                           │
│  # payload를 서버에 전송                                     │
│                                                              │
│  서버측: pickle.loads(payload)                               │
│  → os.system('id && whoami') 실행 → RCE!                     │
└──────────────────────────────────────────────────────────────┘
```

최근 주목받는 위협은 ML 모델 공유 플랫폼(Hugging Face, MLflow)에서 악성 pickle 모델 파일이 업로드되어, 사용자가 모델을 로드하는 순간 RCE가 발생하는 공급망 공격이다.

📢 **섹션 요약 비유**: Python pickle은 마법사의 주문서처럼, 펼치는 순간(로드) 안에 적힌 모든 마법이 자동으로 실행된다. 모르는 주문서는 절대 펼치면 안 된다.

---

## 2. 구성요소

### pickle 프로토콜 취약점 메커니즘

| 단계 | 설명 | 위험 요소 |
|:---|:---|:---|
| 직렬화 | pickle.dumps(obj) | 공격자가 __reduce__ 조작 |
| 전송/저장 | 파일·네트워크·쿠키 | 검증 없이 신뢰 |
| 역직렬화 | pickle.loads(data) | __reduce__ 자동 실행 |
| 코드 실행 | os.system() 등 호출 | RCE 발생 |

```text
┌──────────────────────────────────────────────────────────────┐
│            ML 모델 파일 공급망 공격 흐름                      │
├──────────────────────────────────────────────────────────────┤
│  공격자                                                      │
│  1. 악성 __reduce__ 포함한 모델 객체 생성                     │
│  2. pickle.dumps()로 직렬화 → model.pkl 파일 생성            │
│  3. Hugging Face / MLflow에 모델 업로드                       │
│                                                              │
│  피해자                                                      │
│  4. model = torch.load('model.pkl')  ← pickle.load() 내부 호출│
│  5. 로드 즉시 악성 코드 실행 → 개발자 머신 RCE               │
│                                                              │
│  영향: 개발자 인증서, SSH 키, API 토큰 탈취                   │
└──────────────────────────────────────────────────────────────┘
```

`torch.load()`, `joblib.load()`, `numpy.load()` 등 많은 ML 관련 함수가 내부적으로 pickle을 사용한다.

📢 **섹션 요약 비유**: ML 모델 pickle 공격은 인터넷에서 받은 요리 레시피(모델)를 따라 하면 갑자기 집에 불이 나는 것이다. 레시피를 확인하지 않고 실행하면 위험하다.

---

## 3. 구조 및 동작 원리

| 직렬화 포맷 | 언어 | RCE 위험 | 안전 대안 |
|:---|:---|:---|:---|
| pickle | Python | 매우 높음 | JSON, Safetensors |
| Java Serialization | Java | 매우 높음 | JSON + 스키마 |
| PHP serialize() | PHP | 높음 | JSON |
| Ruby Marshal | Ruby | 높음 | JSON, MessagePack |
| .NET BinaryFormatter | .NET | 높음 | System.Text.Json |

Safetensors는 Hugging Face가 개발한 ML 모델 저장 포맷으로, pickle을 사용하지 않고 순수 텐서 데이터만 저장해 역직렬화 RCE 위험이 없다.

📢 **섹션 요약 비유**: 안전한 직렬화 포맷 선택은 요리 재료를 안전한 냉동 진공포장(Safetensors)에 보관하는 것과 같다. 개봉해도 코드가 실행되지 않는 포장재를 쓰면 된다.

---

## 4. 비교 및 트레이드오프

**방어 전략**:
1. **근본 해결**: 외부 입력에 절대 pickle 사용 금지 → JSON으로 대체
2. **ML 모델**: Safetensors, ONNX (Open Neural Network Exchange), TensorFlow SavedModel 형식 사용
3. **코드 검토**: `pickle.loads()`, `torch.load()`, `joblib.load()` 사용 위치 모두 감사
4. **제한적 사용 시**: HMAC으로 데이터 서명 후 검증 + 신뢰된 소스만 로드
5. **보안 도구**: Fickling(Trail of Bits) - pickle 파일 정적 분석 도구

Fickling 사용 예:
```bash
fickling model.pkl  # pickle 파일의 악성 코드 탐지
```

📢 **섹션 요약 비유**: pickle 방어는 식당에서 모르는 사람이 가져온 음식(외부 pickle)은 절대 서빙하지 않고, 직접 만든 안전한 재료(JSON/Safetensors)만 사용하는 것이다.

---

## 5. 실무 적용 및 최적화 기법

Python pickle 역직렬화 취약점을 제거하면 ML 파이프라인의 공급망 공격, 웹 애플리케이션 RCE, 캐시 기반 공격을 동시에 차단할 수 있다. 특히 AI/ML 시대에 모델 공유가 활발해지면서 pickle 기반 공격 표면이 빠르게 확대되고 있으므로, ML 팀도 보안 훈련이 필요하다.

📢 **섹션 요약 비유**: pickle 완전 방어는 마법 주문서 형식(pickle)을 폐기하고, 그림만 있는 레시피북(Safetensors)으로 전환하는 것이다. 그림은 보기만 하면 되고 실행되지 않는다.

---

### 📌 관련 개념 맵
| 개념 | 관계 | 설명 |
|:---|:---|:---|
| __reduce__ | 공격 진입점 | pickle 역직렬화 시 자동 호출 |
| Safetensors | 안전 대안 | ML 모델 안전 저장 포맷 |
| ONNX | 안전 대안 | 플랫폼 중립 ML 모델 포맷 |
| Fickling | 탐지 도구 | pickle 정적 분석 |
| ML 공급망 공격 | 현대 위협 | 악성 모델 파일 배포 |

### 👶 어린이를 위한 3줄 비유 설명
- Python pickle은 특별한 마법 상자인데, 열면 안에 적힌 명령이 자동으로 실행돼요.
- 나쁜 사람이 만든 마법 상자를 열면 컴퓨터가 나쁜 사람의 명령을 따라 하게 돼요.
- 마법 상자 대신 그냥 메모지(JSON/Safetensors)를 쓰면 실행되는 것 없이 안전해요!
