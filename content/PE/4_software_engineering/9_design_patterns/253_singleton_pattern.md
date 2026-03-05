+++
title = "253. 싱글톤 패턴 (Singleton Pattern)"
description = "클래스 인스턴스의 유일성을 보장하는 생성 패턴, 전역 접근점과 리소스 관리의 양날의 검"
date = "2026-03-04"
[taxonomies]
tags = ["singleton", "design-pattern", "creational", "global-state", "thread-safety"]
categories = ["studynotes-4_software_engineering"]
+++

# 253. 싱글톤 패턴 (Singleton Pattern)

## 핵심 인사이트 (3줄 요약)
> 1. **본질**: 싱글톤 패턴은 클래스의 인스턴스가 **오직 하나만 생성되도록 보장**하며, 그 유일한 인스턴스에 대한 **전역 접근점(Global Access Point)**을 제공하는 생성(Creational) 디자인 패턴으로, 설정 관리자, 로거, 데이터베이스 연결 풀 등 시스템 전역 리소스 관리에 활용됩니다.
> 2. **가치**: 불필요한 메모리 할당을 방지하고 **일관된 상태 유지**를 가능하게 하지만, 과도한 사용은 **숨겨진 의존성, 테스트 어려움, 병렬 처리 문제**를 야기하므로 **신중하게 제한적 사용**이 필요합니다.
> 3. **융합**: 멀티스레드 환경에서의 **Thread-Safe 구현( Double-Checked Locking, Bill Pugh Solution)**, 의존성 주입(DI) 프레임워크에서의 **Scoped Singleton**, 마이크로서비스의 **Stateless 설계**와의 상충 관계를 이해하는 것이 현대적 싱글톤 활용의 핵심입니다.

---

### I. 개요 (Context & Background) - [최소 500자]

#### 1. 개념 정의

싱글톤 패턴(Singleton Pattern)은 GoF(Gang of Four)가 정의한 23가지 디자인 패턴 중 **생성 패턴(Creational Pattern)**에 속합니다. 핵심 의도는 다음과 같습니다:

1. **유일성 보장**: 클래스의 인스턴스가 정확히 하나만 존재하도록 보장
2. **전역 접근**: 해당 인스턴스에 대한 전역 접근점 제공
3. **제어된 인스턴스화**: 인스턴스 생성을 클래스 자체가 통제

**구조적 특징**:
- **Private 생성자**: 외부에서 `new` 키워드로 인스턴스 생성 불가
- **Static 인스턴스**: 클래스 내부에 유일한 인스턴스를 static으로 보관
- **Public Static 메서드**: `getInstance()` 등을 통해 인스턴스 접근

#### 2. 비유: 대통령과 국가

싱글톤 패턴은 **"한 나라에 대통령은 오직 한 명"**인 것과 유사합니다. 대한민국 대통령은 동시에 두 명이 될 수 없습니다. 대통령이라는 직위(Position)는 유일하며, 모든 국민은 그 대통령에게 접근할 수 있는 공식 채널(접근점)이 있습니다.

누구나 "대통령을 한 명 더 뽑자"고 할 수 없습니다. 헌법(Private 생성자)이 이를 막고 있습니다. 대통령 선거는 정해진 절차(getInstance())를 통해서만 이루어집니다.

그러나 대통령이 **모든 일을 직접 처리**하면 병목이 발생합니다. 모든 국무회의, 외교, 국정 수행을 한 명이 다 하면 안 되듯, 싱글톤 객체도 **과도한 책임을 지면 안 됩니다.**

#### 3. 등장 배경 및 발전 과정

**1) 1994년 GoF 디자인 패턴에서 정식 수록**

GoF의 "Design Patterns: Elements of Reusable Object-Oriented Software"에서 23개 패턴 중 하나로 공식화되었습니다.

**2) 1990~2000년대: 전역 상태 관리의 표준**

- 로깅 시스템 (Log4j, java.util.logging)
- 설정 관리자 (Configuration Manager)
- 데이터베이스 연결 풀 (Connection Pool)
- 스레드 풀 (Thread Pool)

위와 같은 시스템 리소스 관리에 표준적으로 사용되었습니다.

**3) 2010년대: 안티패턴 논쟁**

싱글톤의 과도한 사용이 **숨겨진 의존성, 테스트 어려움, SRP 위반**을 초래한다는 비판이 제기되었습니다. Robert C. Martin(Uncle Bob) 등은 "싱글톤은 상태가 있는 전역 변수와 다를 바 없다"며 신중한 사용을 권고했습니다.

**4) 현대: 의존성 주입(DI)과의 결합**

Spring, Guice 등 DI 프레임워크에서 **"싱글톤 스코프"** 개념으로 재정의되어, 싱글톤 패턴의 장점은 유지하면서 단점을 완화하는 방식으로 진화했습니다.

---

### II. 아키텍처 및 핵심 원리 (Deep Dive) - [최소 1,000자]

#### 1. 싱글톤 패턴의 구성 요소

| 구성 요소 | 역할 | 구현 특징 | 비고 |
|:---|:---|:---|:---|
| **Private 생성자** | 외부 인스턴스화 방지 | `private ClassName() {}` | 상속 불가 |
| **Static 인스턴스** | 유일한 인스턴스 저장 | `private static ClassName instance` | Lazy/Eager 초기화 |
| **Public getInstance()** | 전역 접근점 제공 | `public static ClassName getInstance()` | Thread-Safe 고려 |
| **Clone 방지** | 복제 통제 | `clone()` 오버라이드 | Serializable 주의 |

#### 2. 정교한 ASCII 다이어그램: 싱글톤 패턴 구조와 동작

```
================================================================================
|                    SINGLETON PATTERN - STRUCTURE & BEHAVIOR                   |
================================================================================

    [ Client Code ]                      [ Singleton Class ]
    +------------------+                 +------------------------+
    | Singleton s1 =   | ------------>   | - instance: Singleton  | <-- static
    |   Singleton.     |    first call   | - data: String         |
    |   getInstance()  |    creates new  +------------------------+
    +------------------+                 | - Singleton()          | <-- private
                                       > | + getInstance()        | <-- static
    [ Client Code ]   |                 | + doSomething()        |
    +------------------+                 +------------------------+
    | Singleton s2 =   | ------------>              |
    |   Singleton.     |    returns same            |
    |   getInstance()  |    instance                v
    +------------------+                 +------------------------+
                                        |      RUNTIME HEAP       |
    [ Memory Layout ]                   +------------------------+
    +---------------------------------> | [Singleton Instance]    |
    |                                                          |
    |  s1 ───┐                              data: "config"     |
    |        │                              ...                 |
    |  s2 ───┘                                                  |
    +-----------------------------------------------------------+

    [ Thread-Safety Challenge ]

    Thread A                     Thread B
        |                            |
        v                            v
    if (instance == null)       if (instance == null)  <-- Race Condition!
        |                            |
        v                            v
    instance = new Singleton()  instance = new Singleton()  <-- Two instances!

    [ Solutions ]
    =============
    1. Eager Initialization: instance 생성을 클래스 로딩 시점으로
    2. Synchronized Method: getInstance() 동기화
    3. Double-Checked Locking: 동기화 범위 최소화
    4. Bill Pugh Solution: 내부 정적 클래스 활용
    5. Enum Singleton: JVM 보장 활용

================================================================================
```

#### 3. 심층 동작 원리: 5가지 구현 방식 비교

**방식 1: Eager Initialization (이른 초기화)**
```java
// 장점: 구현 간단, Thread-Safe
// 단점: 사용하지 않아도 인스턴스 생성 (메모리 낭비)
public class EagerSingleton {
    // 클래스 로딩 시점에 인스턴스 생성
    private static final EagerSingleton instance = new EagerSingleton();

    private EagerSingleton() {}

    public static EagerSingleton getInstance() {
        return instance;
    }
}
```

**방식 2: Lazy Initialization (늦은 초기화) - Not Thread-Safe**
```java
// 장점: 필요할 때 생성 (메모리 효율)
// 단점: 멀티스레드 환경에서 안전하지 않음
public class LazySingleton {
    private static LazySingleton instance;

    private LazySingleton() {}

    public static LazySingleton getInstance() {
        if (instance == null) {
            instance = new LazySingleton();  // Race Condition!
        }
        return instance;
    }
}
```

**방식 3: Thread-Safe Lazy Initialization (동기화)**
```java
// 장점: Thread-Safe
// 단점: 매번 동기화 오버헤드 (성능 저하)
public class ThreadSafeSingleton {
    private static ThreadSafeSingleton instance;

    private ThreadSafeSingleton() {}

    public static synchronized ThreadSafeSingleton getInstance() {
        if (instance == null) {
            instance = new ThreadSafeSingleton();
        }
        return instance;
    }
}
```

**방식 4: Double-Checked Locking (DCL)**
```java
// 장점: Thread-Safe + 성능 최적화
// 단점: volatile 필요, 복잡한 구현
public class DCLSingleton {
    // volatile: 메모리 가시성 보장
    private static volatile DCLSingleton instance;

    private DCLSingleton() {}

    public static DCLSingleton getInstance() {
        if (instance == null) {                    // First check (no lock)
            synchronized (DCLSingleton.class) {
                if (instance == null) {            // Second check (with lock)
                    instance = new DCLSingleton();
                }
            }
        }
        return instance;
    }
}
```

**방식 5: Bill Pugh Solution (권장)**
```java
// 장점: Thread-Safe, Lazy Loading, 성능 최적
// 단점: 없음 (가장 권장되는 방식)
public class BillPughSingleton {

    private BillPughSingleton() {}

    // 내부 정적 클래스는 getInstance() 호출 시에만 로딩됨
    private static class SingletonHelper {
        private static final BillPughSingleton INSTANCE =
            new BillPughSingleton();
    }

    public static BillPughSingleton getInstance() {
        return SingletonHelper.INSTANCE;
    }
}
```

**방식 6: Enum Singleton (Effective Java 권장)**
```java
// 장점: 직렬화 안전, 리플렉션 방어, Thread-Safe
// 단점: Lazy Loading 불가, Enum 제약
public enum EnumSingleton {
    INSTANCE;

    private String config;

    public void setConfig(String config) {
        this.config = config;
    }

    public String getConfig() {
        return config;
    }
}

// 사용
EnumSingleton.INSTANCE.setConfig("value");
```

#### 4. 핵심 코드: 싱글톤 레지스트리 (다중 싱글톤 관리)

```python
"""
싱글톤 레지스트리 패턴
여러 싱글톤을 이름으로 관리하는 확장된 싱글톤 패턴
"""

from threading import Lock
from typing import Dict, Type, TypeVar, Optional
from dataclasses import dataclass
import logging

T = TypeVar('T')

@dataclass
class SingletonInfo:
    """싱글톤 정보"""
    instance: object
    class_type: Type
    created_at: str

class SingletonRegistry:
    """
    싱글톤 레지스트리
    여러 클래스의 싱글톤 인스턴스를 중앙에서 관리
    """

    _instances: Dict[str, SingletonInfo] = {}
    _lock = Lock()

    @classmethod
    def get_instance(cls, class_type: Type[T], name: Optional[str] = None) -> T:
        """
        싱글톤 인스턴스 획득
        없으면 생성, 있으면 기존 인스턴스 반환
        """
        key = name or class_type.__name__

        # Double-Checked Locking
        if key not in cls._instances:
            with cls._lock:
                if key not in cls._instances:
                    instance = class_type()
                    cls._instances[key] = SingletonInfo(
                        instance=instance,
                        class_type=class_type,
                        created_at=str(datetime.now())
                    )
                    logging.info(f"Singleton created: {key}")

        return cls._instances[key].instance

    @classmethod
    def register_instance(cls, name: str, instance: object):
        """외부에서 생성한 인스턴스 등록"""
        with cls._lock:
            if name in cls._instances:
                raise ValueError(f"Singleton already exists: {name}")
            cls._instances[name] = SingletonInfo(
                instance=instance,
                class_type=type(instance),
                created_at=str(datetime.now())
            )

    @classmethod
    def get_all_singletons(cls) -> Dict[str, SingletonInfo]:
        """모든 싱글톤 목록 조회"""
        return cls._instances.copy()

    @classmethod
    def reset(cls, name: Optional[str] = None):
        """
        싱글톤 리셋 (테스트용)
        """
        with cls._lock:
            if name:
                if name in cls._instances:
                    del cls._instances[name]
                    logging.info(f"Singleton reset: {name}")
            else:
                cls._instances.clear()
                logging.info("All singletons reset")

# 사용 예시 싱글톤 클래스들
class DatabaseConnection:
    """데이터베이스 연결 싱글톤"""
    def __init__(self):
        self.connection_string = "jdbc:postgresql://localhost:5432/mydb"
        self.is_connected = False

    def connect(self):
        self.is_connected = True
        return "Connected to database"

    def execute(self, query: str):
        if not self.is_connected:
            raise RuntimeError("Not connected")
        return f"Executed: {query}"

class ConfigurationManager:
    """설정 관리자 싱글톤"""
    def __init__(self):
        self._config: Dict[str, str] = {
            "app.name": "MyApp",
            "app.version": "1.0.0",
            "log.level": "INFO"
        }

    def get(self, key: str, default: str = None) -> Optional[str]:
        return self._config.get(key, default)

    def set(self, key: str, value: str):
        self._config[key] = value

class Logger:
    """로거 싱글톤"""
    def __init__(self):
        self.log_level = "INFO"
        self._logs: list = []

    def log(self, level: str, message: str):
        if self._should_log(level):
            entry = f"[{level}] {message}"
            self._logs.append(entry)
            print(entry)

    def _should_log(self, level: str) -> bool:
        levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
        return levels.get(level, 0) >= levels.get(self.log_level, 0)

    def get_logs(self) -> list:
        return self._logs.copy()

# 데코레이터 방식 싱글톤
def singleton(cls):
    """싱글톤 데코레이터"""
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class CacheManager:
    """캐시 관리자 (데코레이터 방식)"""
    def __init__(self):
        self._cache: Dict[str, object] = {}

    def get(self, key: str) -> Optional[object]:
        return self._cache.get(key)

    def set(self, key: str, value: object):
        self._cache[key] = value

    def clear(self):
        self._cache.clear()

# 사용 예시
if __name__ == "__main__":
    from datetime import datetime

    # 레지스트리 방식
    db1 = SingletonRegistry.get_instance(DatabaseConnection)
    db2 = SingletonRegistry.get_instance(DatabaseConnection)
    print(f"Same instance? {db1 is db2}")  # True

    # 설정 관리자
    config = SingletonRegistry.get_instance(ConfigurationManager)
    print(config.get("app.name"))

    # 모든 싱글톤 조회
    print("\nRegistered Singletons:")
    for name, info in SingletonRegistry.get_all_singletons().items():
        print(f"  {name}: {info.class_type.__name__}")

    # 데코레이터 방식
    cache1 = CacheManager()
    cache2 = CacheManager()
    print(f"\nDecorator Singleton same? {cache1 is cache2}")
```

---

### III. 융합 비교 및 다각도 분석 - [비교표 2개 이상]

#### 1. 심층 기술 비교표: 싱글톤 구현 방식별 특성

| 구현 방식 | Thread-Safe | Lazy Loading | 성능 | 직렬화 안전 | 리플렉션 안전 | 복잡도 |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Eager** | O | X | 최상 | X | X | 낮음 |
| **Lazy (기본)** | X | O | 최상 | X | X | 낮음 |
| **Synchronized** | O | O | 낮음 | X | X | 낮음 |
| **DCL** | O | O | 양호 | X | X | 중간 |
| **Bill Pugh** | O | O | 최상 | X | X | 중간 |
| **Enum** | O | X | 최상 | O | O | 낮음 |

#### 2. 싱글톤 vs 의존성 주입(DI) 비교

| 비교 항목 | 싱글톤 패턴 | DI 싱글톤 스코프 |
|:---|:---|:---|
| **의존성 명시성** | 숨겨짐 (코드 내부 호출) | 명시적 (생성자 주입) |
| **테스트 용이성** | 어려움 (Mock 어려움) | 용이함 (Mock 주입 가능) |
| **생명주기 관리** | 개발자 직접 관리 | 컨테이너 관리 |
| **결합도** | 높음 | 낮음 |
| **설정 유연성** | 하드코딩 | 외부 설정 가능 |
| **적합 상황** | 단순 프로젝트 | 엔터프라이즈 프로젝트 |

#### 3. 과목 융합 관점 분석

**싱글톤 + 멀티스레딩**
```
[싱글톤의 스레드 안전성 이슈]

Thread A                          Thread B
    |                                 |
    v                                 v
[Check: instance == null]       [Check: instance == null]
    | true                           | true
    v                                 v
[Create Instance 1]             [Create Instance 2]
    |                                 |
    v                                 v
[Return Instance 1]             [Return Instance 2]

결과: 두 개의 인스턴스 존재 -> 싱글톤 위반!

[해결책: Double-Checked Locking]
- 첫 번째 체크: 락 없이 빠른 확인
- 두 번째 체크: 락 내부에서 확실한 확인
- volatile: 메모리 가시성 보장
```

**싱글톤 + 마이크로서비스**
```
[MSA에서의 싱글톤 문제]

모놀리식:
  +------------------+
  | App Server       |
  | [Singleton X]    |  <- JVM 내 유일
  +------------------+

마이크로서비스:
  +--------+  +--------+  +--------+
  | MS-A   |  | MS-B   |  | MS-C   |
  | [X1]   |  | [X2]   |  | [X3]   |  <- 각각 다른 싱글톤!
  +--------+  +--------+  +--------+

[MSA에서의 대안]
1. Stateless 설계: 싱글톤 대신 무상태 서비스
2. 분산 캐시: Redis 등 외부화
3. Service Registry: 중앙 집중식 상태 관리
```

---

### IV. 실무 적용 및 기술사적 판단 - [최소 800자]

#### 1. 기술사적 판단 (실무 시나리오)

**[시나리오 1] 로깅 시스템 구축**

*   **상황**:
    - 대규모 웹 애플리케이션의 로깅 시스템 설계
    - 모든 컴포넌트에서 로그 기록 필요
    - 로그 파일 관리, 포맷팅, 레벨 관리 중앙화

*   **기술사적 판단**: **싱글톤 + Facade 패턴 적절**

*   **실행 전략**:
    ```java
    public class Logger {
        private static volatile Logger instance;
        private LogLevel level = LogLevel.INFO;
        private List<Appender> appenders;

        private Logger() {
            appenders = new ArrayList<>();
            appenders.add(new FileAppender("app.log"));
            appenders.add(new ConsoleAppender());
        }

        public static Logger getInstance() {
            if (instance == null) {
                synchronized (Logger.class) {
                    if (instance == null) {
                        instance = new Logger();
                    }
                }
            }
            return instance;
        }

        public void log(LogLevel level, String message) {
            if (this.level.ordinal() <= level.ordinal()) {
                LogEntry entry = new LogEntry(level, message);
                for (Appender appender : appenders) {
                    appender.append(entry);
                }
            }
        }
    }
    ```

*   **핵심 의사결정 포인트**:
    - 로깅은 **상태가 거의 없고**, 전역 접근이 필요하므로 싱글톤 적합
    - 테스트 시 Mock Logger 주입 가능하도록 인터페이스 분리

**[시나리오 2] 데이터베이스 연결 풀**

*   **상황**:
    - 고부하 웹 서비스의 DB 연결 관리
    - 연결 생성 비용이 높음
    - 연결 수 제한 필요

*   **기술사적 판단**: **싱글톤보다 DI 컨테이너 관리 권장**

*   **실행 전략**:
    ```java
    // Spring에서의 싱글톤 스코프 빈
    @Service
    @Scope("singleton")  // 기본값이지만 명시
    public class ConnectionPool {
        private final BlockingQueue<Connection> pool;

        public ConnectionPool(DataSourceConfig config) {
            this.pool = new LinkedBlockingQueue<>(config.getMaxPoolSize());
            initializePool(config);
        }

        public Connection getConnection() throws InterruptedException {
            return pool.take();
        }

        public void releaseConnection(Connection conn) {
            pool.offer(conn);
        }
    }
    ```

*   **핵심 의사결정 포인트**:
    - 전통적 싱글톤보다 **DI 컨테이너 관리**가 유연함
    - 테스트 시 인메모리 DB로 쉽게 교체 가능

**[시나리오 3] 설정 관리자**

*   **상황**:
    - 애플리케이션 전역 설정 로드
    - 환경별(dev, staging, prod) 설정 분리
    - 런타임에 설정 변경 불가

*   **기술사적 판단**: **Enum 싱글톤 또는 설정 클래스**

*   **실행 전략**:
    ```java
    // 불변 설정 싱글톤
    public final class AppConfig {
        private static final AppConfig INSTANCE = new AppConfig();

        private final String databaseUrl;
        private final int maxConnections;
        private final Duration timeout;

        private AppConfig() {
            Properties props = loadProperties();
            this.databaseUrl = props.getProperty("db.url");
            this.maxConnections = Integer.parseInt(props.getProperty("db.maxConnections"));
            this.timeout = Duration.parse(props.getProperty("timeout"));
        }

        public static AppConfig getInstance() {
            return INSTANCE;
        }

        // Getters only (불변)
        public String getDatabaseUrl() { return databaseUrl; }
        public int getMaxConnections() { return maxConnections; }
        public Duration getTimeout() { return timeout; }
    }
    ```

#### 2. 도입 시 고려사항 체크리스트

**적합성 판단**:
- [ ] **진정으로 유일해야 하는가?** (여러 인스턴스가 있어도 되는가?)
- [ ] **상태가 필요한가?** (상태 없으면 static 메서드로 충분)
- [ ] **전역 접근이 정말 필요한가?** (의존성 주입으로 대체 가능?)
- [ ] **테스트에서 Mock 가능한가?** (인터페이스 분리 필요?)

**구현 시 주의사항**:
- [ ] **Thread-Safe 구현** 선택 (DCL, Bill Pugh, Enum)
- [ ] **직렬화/역직렬화** 처리 (readResolve 오버라이드)
- [ ] **리플렉션 방어** (Enum 사용 또는 체크)
- [ ] **Clone 방지** (clone() 오버라이드)

#### 3. 주의사항 및 안티패턴 (Anti-patterns)

*   **싱글톤 남용 (Singleton Abuse)**:
    - 모든 서비스를 싱글톤으로 만드는 실수
    - "유틸리티 클래스"라며 싱글톤으로 만드는 경우
    - **해결**: 진정으로 유일해야 하는 리소스만 싱글톤

*   **상태 오염 (State Pollution)**:
    - 싱글톤이 가변 상태를 가짐
    - 한 요청이 변경한 상태가 다른 요청에 영향
    - **해결**: 싱글톤은 불변(Immutable)으로 설계

*   **숨겨진 의존성 (Hidden Dependencies)**:
    - 코드만 보고 의존성을 알 수 없음
    - 생성자에 없는데 내부에서 싱글톤 호출
    - **해결**: 의존성 주입(DI) 사용

*   **테스트 어려움 (Test Difficulty)**:
    - 싱글톤 상태가 테스트 간 공유됨
    - 테스트 격리(Isolation) 어려움
    - **해결**: 인터페이스 분리 + Mock 주입

---

### V. 기대효과 및 결론 - [최소 400자]

#### 1. 정량적/정성적 기대효과

| 구분 | 효과 내용 | 기대 수치 |
|:---:|:---|:---|
| **메모리 효율** | 불필요한 인스턴스 생성 방지 | 메모리 10~30% 절감 |
| **일관성** | 전역 상태의 일관된 관리 | 상태 불일치 90% 감소 |
| **접근성** | 어디서든 접근 가능 | 코드 복잡도 감소 |
| **테스트성** | (과도한 사용 시) 저하 | Mock 어려움 증가 |
| **결합도** | (과도한 사용 시) 증가 | 의존성 파악 어려움 |

#### 2. 미래 전망 및 진화 방향

1.  **의존성 주입과의 통합**:
    - 순수 싱글톤 패턴보다 DI 컨테이너 관리 싱글톤이 표준
    - Spring, Jakarta EE 등에서 싱글톤 스코프 빈

2.  **무상태(Stateless) 설계 선호**:
    - 마이크로서비스, 서버리스 환경에서는 상태 없는 설계 선호
    - 싱글톤은 진정으로 필요한 경우만 제한적 사용

3.  **함수형 프로그래밍의 영향**:
    - 불변 객체 + 순수 함수로 싱글톤 대체
    - 모나드(Monad) 패턴으로 상태 관리

#### 3. 참고 표준/가이드

*   **GoF Design Patterns (1994)**: 싱글톤 패턴 원조 정의
*   **Effective Java (Joshua Bloch)**: Enum 싱글톤 권장
*   **Clean Code (Robert C. Martin)**: 싱글톤 사용 경고

---

### 관련 개념 맵 (Knowledge Graph)

*   [팩토리 메서드 패턴](@/studynotes/4_software_engineering/9_design_patterns/_index.md) : 객체 생성 로직을 캡슐화
*   [의존성 주입(DI)](@/studynotes/4_software_engineering/5_architecture/clean_architecture.md) : 싱글톤의 현대적 대안
*   [전역 상태(Global State)](@/studynotes/4_software_engineering/5_architecture/_index.md) : 싱글톤이 관리하는 상태
*   [불변성(Immutability)](@/studynotes/4_software_engineering/14_code_quality/_index.md) : 싱글톤 설계의 핵심 원칙
*   [스레드 안전성(Thread Safety)](@/studynotes/4_software_engineering/14_code_quality/_index.md) : 멀티스레드 싱글톤 구현의 핵심

---

### 어린이를 위한 3줄 비유 설명

1. **문제**: 학급에 반장이 여러 명이면 서로 명령해서 혼란스러워요.
2. **해결(싱글톤)**: 반장은 **딱 한 명만** 뽑아요. 누가 반장인지는 반 친구들 모두가 알고 있어요. 새로 뽑을 수 없어요.
3. **효과**: 반장이 한 명이라서 명령이 통일되고, 친구들은 반장에게 바로 말하면 돼요. 하지만 반장이 너무 많은 일을 하면 바빠서 못 움직여요!
