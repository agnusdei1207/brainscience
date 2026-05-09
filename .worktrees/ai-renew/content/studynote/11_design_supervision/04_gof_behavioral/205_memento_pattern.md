+++
weight = 205
title = "205. 메멘토 패턴 (Memento Pattern)"
date = "2026-04-21"
[extra]
categories = "studynote-design-supervision"
+++

## 핵심 인사이트 (3줄 요약)

> 1. **본질**: Memento (메멘토) 패턴은 객체의 캡슐화(Encapsulation)를 훼손하지 않으면서, 특정 시점의 내부 상태(스냅샷)를 외부에 저장하고 필요 시 복원(Undo/Redo)할 수 있게 한다.
> 2. **가치**: Originator (원본 객체)만이 Memento의 내용을 읽고 쓸 수 있으므로, 상태 노출 없이 Undo 스택을 구현할 수 있다.
> 3. **판단 포인트**: 텍스트 에디터 Undo, 게임 세이브·로드, 트랜잭션 롤백처럼 "시간을 되돌리는" 기능이 필요할 때 적용한다.

---

## Ⅰ. 개요 및 필요성

### 1-1. Undo 기능 구현의 딜레마

Undo (실행 취소) 기능을 구현하려면 이전 상태를 저장해야 한다. 하지만 저장 객체(Caretaker)가 Originator의 내부 필드에 직접 접근하면 **캡슐화가 깨진다**.

```
  ❌ 나쁜 방법: 캡슐화 파괴
  Caretaker caretaker = ...;
  caretaker.savedState = editor.text;  // private 필드 직접 접근
  caretaker.savedCursor = editor.cursor; // 내부 구현 노출

  ✅ Memento 패턴: 캡슐화 보존
  Memento m = editor.save();         // Originator가 직접 스냅샷 생성
  caretaker.push(m);                 // Caretaker는 불투명한 Memento만 보관
  editor.restore(m);                 // 복원도 Originator가 직접
```

### 1-2. 3요소: Originator, Memento, Caretaker

| 역할 | 책임 | 비유 |
|:---|:---|:---|
| **Originator** | 상태를 가진 원본 객체, Memento 생성·복원 | 사진 찍히는 대상 |
| **Memento** | 특정 시점의 상태 스냅샷 (불투명 객체) | 인화된 사진 |
| **Caretaker** | Memento를 보관하지만 내용을 읽지 않음 | 사진 앨범 |

📢 **섹션 요약 비유**: 게임 세이브 기능 — 캐릭터(Originator)가 자기 상태를 세이브 파일(Memento)로 저장하고, 세이브 슬롯(Caretaker)이 보관하고, 로드(restore)하면 그 시점으로 복원된다.

---

## Ⅱ. 아키텍처 및 핵심 원리

### 2-1. 구조 (UML 요약)

```
  Originator                     Caretaker
  ──────────────                 ──────────────────
  - state                        - history: Stack<Memento>
  + save(): Memento              + push(m: Memento)
  + restore(m: Memento)          + pop(): Memento
        │                               │
        └───── creates ────────►  Memento
                                  ──────────────────
                                  - state (private)
                                  + getState() [Originator only]
```

### 2-2. 텍스트 에디터 Undo 스택 예시

```
  [ 작업 흐름 ]

  (1) 초기 상태: "Hello"
       │ save() → Memento("Hello")
       │ history: [M1("Hello")]

  (2) 입력: "Hello World"
       │ save() → Memento("Hello World")
       │ history: [M1("Hello"), M2("Hello World")]

  (3) 입력: "Hello World!!!"
       │ save() → Memento("Hello World!!!")
       │ history: [M1, M2, M3("Hello World!!!")]

  (4) Ctrl+Z (Undo)
       │ history.pop() → M3
       │ restore(M2) → 텍스트 = "Hello World"

  (5) Ctrl+Z (Undo)
       │ restore(M1) → 텍스트 = "Hello"
```

### 2-3. Command 패턴과 조합: Undo 스택

```
  Command + Memento = 완전한 Undo/Redo 시스템

  ┌─────────────────────────────────────────────────────┐
  │  UndoManager (Caretaker)                            │
  │                                                     │
  │  undoStack: Stack<Command>                          │
  │  redoStack: Stack<Command>                          │
  │                                                     │
  │  execute(cmd):                                      │
  │    memento = originator.save()                      │
  │    cmd.setMemento(memento)                          │
  │    cmd.execute()                                    │
  │    undoStack.push(cmd)                              │
  │                                                     │
  │  undo():                                            │
  │    cmd = undoStack.pop()                            │
  │    originator.restore(cmd.getMemento())             │
  │    redoStack.push(cmd)                              │
  │                                                     │
  │  redo():                                            │
  │    cmd = redoStack.pop()                            │
  │    cmd.execute()                                    │
  │    undoStack.push(cmd)                              │
  └─────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 체스 경기 기록지(Caretaker) — 각 수(Memento)를 기록해두면, 언제든 되감아서(restore) 특정 시점으로 돌아갈 수 있다. 기록지는 수의 의미를 이해할 필요가 없다.

---

## Ⅲ. 비교 및 연결

### 3-1. Memento 구현 방식 비교

| 방식 | 설명 | 장점 | 단점 |
|:---|:---|:---|:---|
| **내부 클래스 Memento** | Originator 내부에 private 클래스 | 캡슐화 완벽 | 언어 지원 필요 |
| **Interface 기반** | Memento를 빈 인터페이스로 | 유연성 | 캡슐화 약화 가능 |
| **직렬화(Serialization)** | 객체를 byte[]로 저장 | 딥카피 자동 | 성능 비용 |
| **Shallow Copy** | 참조 복사 | 빠름 | 참조 타입 공유 주의 |
| **Deep Copy** | 완전 복사 | 안전 | 메모리·시간 비용 |

### 3-2. 관련 패턴 비교

| 패턴 | Memento와의 관계 |
|:---|:---|
| Command (커맨드) | Command에 Memento를 포함하면 Undo 가능 |
| Prototype (프로토타입) | 딥카피로 Memento 생성 가능 |
| Iterator (이터레이터) | Iterator 상태를 Memento로 저장·복원 |
| State (상태) | State와 Memento 조합으로 FSM 히스토리 관리 |

📢 **섹션 요약 비유**: Memento는 "타임캡슐" — 묻는 사람(Originator)만 내용을 알고, 묻어두는 사람(Caretaker)은 언제 묻었는지만 알면 된다.

---

## Ⅳ. 실무 적용 및 기술사 판단

### 4-1. 메모리 최적화: Incremental Memento

대용량 객체의 경우 매번 전체 상태를 저장하면 메모리 폭발:

```
  일반 Memento:
  State1(100MB) → State2(100MB) → State3(100MB)
  → Undo 3단계 = 300MB 필요

  Incremental Memento (증분 저장):
  State1(100MB) → Delta1(변경분만, ~1KB) → Delta2(~1KB)
  → Undo 3단계 = 100MB + 2KB 필요

  구현: 변경된 필드만 저장, 역순으로 적용
```

### 4-2. 데이터베이스 트랜잭션과의 유사성

```
  DB Transaction    ↔    Memento Pattern
  ────────────────────────────────────────
  BEGIN                  originator.save()
  UPDATE/INSERT          실행
  ROLLBACK               originator.restore(memento)
  COMMIT                 history.clear() (더 이상 롤백 불필요)
```

### 4-3. 기술사 서술 포인트

- **캡슐화 보존**이 Memento 패턴의 핵심 가치임을 반드시 언급
- Command + Memento = Undo/Redo 시스템 조합 설계 제시
- 메모리 비용과 **증분(Incremental) Memento** 최적화 방법 언급

📢 **섹션 요약 비유**: Memento는 "방 사진 촬영" — 청소하기 전에 사진을 찍어두면(save), 나중에 원래 배치로 복원(restore)할 수 있다. 청소부(Caretaker)는 사진만 보관하고 방 배치는 몰라도 된다.

---

## Ⅴ. 기대효과 및 결론

### 5-1. 기대 효과

| 효과 | 설명 |
|:---|:---|
| 캡슐화 보존 | Caretaker가 내부 구현 없이 상태 보관 |
| Undo/Redo 구현 | 히스토리 스택으로 시간 역행 가능 |
| 오류 복구 | 잘못된 연산 후 이전 상태로 복원 |
| 트랜잭션 지원 | DB 롤백과 동일한 원리의 메모리 내 구현 |

### 5-2. 한계 및 주의사항

- **메모리 사용**: 상태가 크거나 Undo 깊이가 깊을수록 메모리 급증 → 최대 히스토리 수 제한 필요
- **성능**: Deep Copy 비용 → 증분 저장 또는 Copy-on-Write 전략 고려
- **캡슐화**: Java에서는 내부 클래스, C++에서는 `friend` 키워드로 구현

### 5-3. 결론

Memento (메멘토) 패턴은 **캡슐화를 지키면서 역사를 기록**하는 우아한 해법이다. 텍스트 에디터의 Ctrl+Z, 게임 세이브·로드, 데이터베이스 트랜잭션 롤백 등 "시간을 되돌리는" 모든 기능의 설계 근간이다. Command 패턴과 결합하면 완전한 Undo/Redo 시스템이 완성된다.

📢 **섹션 요약 비유**: Memento는 "회사 연간 백업" — 매년 말 서버 상태를 통째로 저장해두고, 문제 생기면 언제든 그 시점으로 되돌아갈 수 있다.

---

### 📌 관련 개념 맵

| 관계 | 개념 | 설명 |
|:---|:---|:---|
| 상위 개념 | GoF Behavioral Pattern | 행동 패턴 그룹 |
| 하위 개념 | Originator / Memento / Caretaker | 패턴 3요소 |
| 연관 개념 | Command Pattern | Undo 스택을 위한 조합 |
| 연관 개념 | Prototype Pattern | Deep Copy로 Memento 생성 |
| 연관 개념 | DB Transaction Rollback | 동일 원리의 영속성 층 구현 |
| 연관 개념 | Encapsulation (캡슐화) | Memento가 보존하는 핵심 원칙 |

### 👶 어린이를 위한 3줄 비유 설명

- 그림 그리다가 망했을 때 "되돌리기" 버튼을 누르면 이전 그림으로 돌아가죠?
- 메멘토 패턴은 그 되돌리기 기능을 만드는 방법이에요.
- 그림판(Originator)이 자기 그림의 사진(Memento)을 찍어두고, 앨범(Caretaker)에 저장해두는 거예요!
