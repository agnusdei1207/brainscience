+++
title = "54. ConfigMap/Secret"
date = "2026-04-05"
[taxonomies]
tags = ["Cloud", "Kubernetes", "K8s", "ConfigMap", "Secret", "Configuration"]
categories = ["13_cloud_architecture"]
+++

# ConfigMap/Secret

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: ConfigMap은 환경 변수나 설정 파일 형태로 구성을 저장하는 비민감 정보용 쿠버네티스 오브젝트이며, Secret은 패스워드, API 키, 인증서 등 민감한 정보를 암호화하여 저장하는 오브젝트이다.
> 2. **가치**: 이 분리된 설계를 통해 애플리케이션 코드를 변경하지 않고도 환경별(dev, staging, prod) 구성을 다르게 적용할 수 있으며, 민감 정보는 런타임에 파드에 안전하게 주입된다.
> 3. **융합**: ConfigMap/Secret은 12-Factor App의 "외부화된 설정(Externalized Configuration)" 원칙을 쿠버네티스 환경에서実装하는 핵심 메커니즘이다.

---

### Ⅰ. 개요 및 필요성 (Context & Necessity)

현대 애플리케이션은 개발(DEV), 스테이징(STG), 운영(PROD) 환경마다 서로 다른 설정을 필요로 한다. 데이터베이스 연결 문자열, 외부 API 엔드포인트, 로깅 레벨, 피처 플래그(Feature Flag) 등이 환경에 따라 다르다. 이러한 설정을 애플리케이션 코드에 하드코딩하면, 코드를 修改하지 않고 환경만 바꿀 수 없어 DevOps의 핵심 원칙인 "설정과 코드의 분리"에 위배된다. 더 큰 문제는 패스워드, API 키, 인증서 등 민감 정보가 코드에 포함되면 Git 저장소를 통해 외부에 노출되는 "정보 유출" 보안 사고로 이어질 수 있다는 점이다.

쿠버네티스는 이 문제를 ConfigMap과 Secret이라는 두 가지专门的(전용) 오브젝트를 제공하여 해결한다. ConfigMap은 데이터베이스 URL, 포트 번호, 일반 설정 등 비민감 정보를 저장하는 데 사용되며, Secret은 패스워드, OAuth 토큰, SSH 키, TLS 인증서 등 민감한 정보를 저장하도록 설계되었다. 둘 다 파드에 환경 변수, 명령줄 인자, 볼륨 마운트 등의 방법으로 주입될 수 있어 애플리케이션 코드 수정 없이 런타임에 설정을 변경할 수 있다.

```text
[설정 분리 원칙: 코드 vs 구성]
이 흐름도는 하드코딩 방식과 ConfigMap/Secret 사용 방식을 비교한다.

[하드코딩 방식 (나쁜 예)]
┌─────────────────────────────────────────────┐
│  애플리케이션 코드                            │
│  const dbPassword = "my_secret_password";    │ ← 코드 내부에 민감 정보 포함
│  const apiUrl = "http://prod-api.example.com";│ ← 환경별 다른 URL 하드코딩
└─────────────────────────────────────────────┘
문제: 코드 변경 없이 환경 전환 불가, Git 유출 위험

[ConfigMap/Secret 방식 (좋은 예)]
┌─────────────────────────────────────────────┐
│  ConfigMap (DEV)      │  ConfigMap (PROD)   │
│  apiUrl: dev-api...   │  apiUrl: prod-api..│
│  logLevel: DEBUG      │  logLevel: INFO    │
│────────────────────────┼─────────────────────│
│  Secret (공통)        │                    │
│  dbPassword: *****    │                    │
└─────────────────────────────────────────────┘
              │ 환경별 선택적 적용
              ▼
┌─────────────────────────────────────────────┐
│  애플리케이션 코드                            │
│  const dbPassword = process.env.DB_PASSWORD; │ ← 설정 참조만, 값은 런타임 주입
│  const apiUrl = process.env.API_URL;         │
└─────────────────────────────────────────────┘
```

이 구조의 핵심 이점은 설정 변경 시 애플리케이션을 다시 빌드/배포할 필요가 없다는 점이다. ConfigMap의 내용을 更新하면 해당 ConfigMap을 사용하는 모든 파드가 새로운 설정을 읽게 된다(환경变量的 경우 파드 재시작 필요). 이는 12-Factor App의 "II. 의존성(Dependencies)"과 "III. 설정(Configuration)" 원칙을 직접적으로 충족한다.

📢 **섹션 요약 비유**: ConfigMap/Secret은 요리사와 조리대에 비유할 수 있습니다. 요리사(애플리케이션)는 만드는 방법(코드)을 외우고 있으며, 조리대 위의 레시피 카드는 개발/운영 환경에 따라 다르게 배치됩니다(DEV는 조리법을 상세히, PROD는 결과 위주로). 민감한 양념통(시크릿)은 자물쇠(암호화)가 있는 수납장에 보관되어 있습니다.

### Ⅱ. 아키텍처 및 핵심 원리 (Deep Dive)

**ConfigMap**은 키-값 쌍뿐만 아니라 다양한 형태로 데이터를 저장할 수 있다. 가장 기본적인 형태는 `kubectl create configmap` 명령으로 생성하는 단순 키-값(simple key-value)이다. 또한 `from-literal`フラグ를 사용하여命令行에서直接値を与えたり、`from-file`でファイルを与えたり、`--from-env-file`で環境設定ファイル(.env)を与えることができる. 複雑な設定したい場合は YAML/JSON 포맷으로 multi-level構造를作成할 수도 있다. ConfigMapの容量上限は1MBで、それ以上の大きな設定ファイルには別のアプローチ(EventualにはObject Storageなど)が必要である.

ConfigMap을 파드에 전달하는 방법은主に3가지 있다. **환경 변수(Environment Variable)**로 주입하면 `process.env.KEY` 형태로 코드에서 읽을 수 있다. **명령줄 인자(Command Line Argument)**로 주입하면 `$VAR_NAME` 형태로ocker-entrypointスクリプトで参照できる. **볼륨 마운트(Volume Mount)**로 주입하면 설정 文件을 파드의 filesystem에 마운트하여 `vi /etc/config/db.conf` 형태로 읽을 수 있다.

**Secret**은 기본적으로 Base64 인코딩만 되어 저장되며, 암호화되지 않는다. 따라서 etcd에서 Secret 내용이 평문으로 저장될 수 있어, Production 환경에서는 etcd 암호화(Encryption at Rest)를 활성화하는 것이 필수이다. Secret 종류로는 **Opaque**(일반적인 키-값), **kubernetes.io/tls**(TLS 인증서), **kubernetes.io/dockerconfigjson**(레지스트리 인증 정보), **kubernetes.io/ssh-auth**(SSH 키) 등이 있다. 시크릿을 파드에 전달하는 방식도 ConfigMap과 동일하게 환경変数、명령줄、볼륨 마운트 세 가지이다.

```text
[ConfigMap/Secret 주입 방식 비교]
┌──────────────────────────────────────────────────────────────────┐
│ 1. 환경 변수로 주입                                               │
│ ──────────────────────────────────────────────────────────────── │
│ env:                                                                │
│   - name: API_URL           # ConfigMap 키                        │
│     valueFrom:                                                      │
│       configMapKeyRef:                                              │
│         name: my-config                                              │
│         key: api_url                                                 │
│   - name: DB_PASSWORD      # Secret 키                            │
│     valueFrom:                                                      │
│       secretKeyRef:                                                  │
│         name: my-secret                                              │
│         key: password                                                 │
├──────────────────────────────────────────────────────────────────┤
│ 2. 볼륨 마운트로 주입                                              │
│ ──────────────────────────────────────────────────────────────── │
│ volumeMounts:                                                       │
│   - name: config-volume       # 설정 파일 마운트                    │
│     mountPath: /etc/config                                            │
│   - name: secret-volume       # 민감 파일 마운트                    │
│     mountPath: /etc/secrets                    │
│     readOnly: true                                                      │
└──────────────────────────────────────────────────────────────────┘
```

시크릿의 볼륨 마운트 방식은 특히 TLS 인증서를 사용할 때 유용하다. TLS 인증서는 파일形式(公开키/秘密鍵)이므로 볼륨으로 마운트하여 nginx Ingress나 애플리케이션에서 파일로 읽어 사용할 수 있다. 환경変数로 주입된 Secretはプロセスの環境変数として保存され、procファイルシステムなどを 통해他のプロセスから参照可能被であるというセキュリティ上の注意がある. そのため、Secretを安全に使用するための最佳時間は、Secret 볼륨 마운트方式과 tmpfs(RAM 디스크) 활용이다.

📢 **섹션 요약 비유**: ConfigMap/Secret 주입 방식은 식당에 식자재(설정)를 delivery하는 세 가지 방법과 같습니다. 환경 변수는 냉장 식품을 조리대에 직접 놓고 조리사가 집어 드는 것이고, 명령줄 인자는 냉장 식품을 운반할 때 조리법에 인쇄해서 제품盒(상자)에 동봉하는 것이며, 볼륨 마운트는 식자재를 냉장고(마운트된 볼륨)에 넣고 조리사가 냉장고 문을 열어 읽어들이는 것입니다.

### Ⅲ. 융합 비교 및 다각도 분석 (Comparison & Synergy)

ConfigMap과 Secret의 차이는 단순히 "민감 여부"를 넘어, 보안과 운영에 直接적(직접적)인 영향을 미친다. Secret은 기본적으로 Base64 인코딩일 뿐이므로 Kubernetes Dashboard나 kubectl describe로 누구든 내용을 확인할 수 있다. 따라서 Secret를 사용할 때는 RBAC(Role-Based Access Control)을 통해 Secret에 대한 접근을 최소 권한 원칙으로 제어해야 한다. cluster-admin 권한이 있는 사용자는 모든 Secret를 읽을 수 있으므로,Production 환경에서는 cluster-admin 사용을 엄격히 제한해야 한다.

ConfigMap을 활용하면 단일 애플리케이션 패키지로 여러 환경을 خدمة(서비스)할 수 있다. 동일한 도커 이미지(Docker Image)를DEV/STG/PROD에 배포하되, 각각 다른 ConfigMap을 연결하면된다. 이것은 "이미지는 불변(Immutable)이고 설정은 가변(Variable)"이라는 클라우드 네이티브 핵심 원칙을实现한다. 또한 ConfigMap을 사용하면 설정 변경 시Deployment를 再作成할 필요 없이 ConfigMap만 更新하면 된다. 이는 새로운 Deployment 롤아웃 없이 설정만 업데이트하는 "동적 재구성(Dynamic Reconfiguration)"을可能하게 한다.

| 항목 | ConfigMap | Secret |
|:---|:---|:---|
| 용도 | 포트, URL, 로깅 레벨 등 | 패스워드, API 키, 인증서 |
| 저장 방식 | Base64 (평문) | Base64 (암호화 아님) |
| etcd 암호화 | 권장 | 필수 |
| 기본 크기 제한 | 1MB | 1MB |
| RBAC 접근 제어 | configmaps | secrets (별도 권한) |
| 사용 시나리오 | 환경별 설정 주입 | 자격 증명 주입 |

ConfigMap/Secret는 쿠버네티스 외부 도구와 결합하면 더욱 강력한 설정을管理할 수 있다. **HashiCorp Vault**를 사용하면 ConfigMap/Secret을 vault로 完全 대체하여 중앙 집중식密钥管理(키 관리)를 할 수 있다. vault-controller가 vault에서 시크릿을 읽어 쿠버네티스 Secret으로 синхрониы驅ӧ(동기화)하거나, 외부 시크릿 오퍼레이터(External Secrets Operator)가 vault/ AWS Secrets Manager/Azure Key Vault 등으로부터 시크릿을 동적으로 가져와 파드에 주입할 수 있다.

```text
[외부 시크릿 관리 시스템 통합]
┌─────────────────────────────────────────────────────────────────┐
│                    HashiCorp Vault / AWS Secrets Manager         │
│                         (중앙 집중식密钥 관리)                      │
└─────────────────────────────┬───────────────────────────────────┘
                              │ 동적 주입
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  External Secrets Operator / Vault Controller                    │
│  - 외부 시크릿을 쿠버네티스 Secret으로 동기화                       │
│  - 자동 주기적 갱신 (Rotation)                                   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  쿠버네티스 Secret (마스터 볼륨 마운트, tmpfs)                     │
└─────────────────────────────┬───────────────────────────────────┘
                              │ 주입
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  파드 (애플리케이션)                                              │
└─────────────────────────────────────────────────────────────────┘
```

📢 **섹션 요약 비유**: 외부 시크릿 관리 시스템을 사용하는 것은 식당에 식자재 조달을总部(총부)에서集中管理하는 것과 같습니다. 각 매장(파드)에서 직접 시크릿 양념을 보관하지 않고,总部에서 필요한 만큼만 delivery하고, 조리 완료 후에는返回(반환)하거나 폐기합니다. 이렇게 하면 도난 위험이 줄고 권한 관리도总部에서一元화됩니다.

### Ⅳ.实务適用 및技術的判断 (Strategy & Decision)

ConfigMap/Secret을 실各县(실제로) 사용할 때는 다음の原則을 따라야 한다. First, Secret 값은 절대로 코드에 하드코딩하지 말고, `kubectl create secret` 또는 CI/CD 파이프라인에서 동적으로 생성해야 한다. Second, Secret 볼륨은 반드시 tmpfs(RAM 기반 filesystem)을 사용하도록 하여, 노드의 disk에 기록되지 않도록 해야 한다. Third, Secret 업데이트 시 환경 변수는 파드 재시작이 필요하므로, 토|ARGUMENT나 volume 마운트 방식을 사용하여 동적 갱신을 지원해야 한다. Fourth, Secret 이름과 ConfigMap 이름은部署(배포)하려는 환경에 따라 다르게 naming하여 dev-config/prod-config 같은 naming 컨벤션을 使用하는 것이 권장된다.

또한 시크릿을 Git에 直接保存하면 안 된다. 따라서 시크릿 값은 `.gitignore`에 포함시키고, CI/CD 파이프라인이나 외부 시크릿 관리 도구(Vault, AWS Secrets Manager)를 통해 런타임에 주입하는 것이 필수이다. Sealed Secrets나 External Secrets와 같은 도구를 使用하면 Secret을 암호화된 형태로 Git에 저장하고, 런타임에 쿠버네티스 Secret으로 解読(복호화)할 수 있다.

```text
[ConfigMap/Secret 安全运营 체크리스트]
1. Secret 보안 강화
   ├─ etcd 암호화 활성화 (Encryption at Rest)
   ├─ Secret 볼륨은 tmpfs 사용 (디스크 미기록)
   ├─ RBAC으로 Secret 접근 제어 (최소 권한 원칙)
   └─ Secret 이름은 의미 없이 무작위 문자열 사용 (추측 방지)

2. Git 저장소 관리
   ├─ Secret 값은 Git에 저장禁止
   ├─ Sealed Secrets / External Secrets 활용
   └─ CI/CD 파이프라인에서 동적 생성

3. 환경별 관리
   ├─ DEV/STG/PROD 별 ConfigMap 분리
   ├─ kubens/kubectx로 네임스페이스 빠르게 전환
   └─ 공통 설정은 별도 ConfigMap으로 분리 (공유)

4. 업데이트 전략
   ├─ 환경 변수는 파드 재시작 필요 (재배치 불가피)
   ├─ 볼륨 마운트는 애플리케이션이 파일 변경 감지하면 재로딩 가능
   └─ ConfigMap 변경 시 즉시 적용 여부 확인 필요
```

ConfigMap을 업데이트하면 ConfigMap을 구독하는 모든 파드에 동시에 변경이 반영되므로, 예상치 못한 일관성 문제가 발생할 수 있다. 예컨대, ConfigMap을 참조하는 파드가 3개인데 ConfigMap만 바뀌면, 일부 파드는新設定을 읽고 일부 파드는 旧設定을 읽을 수 있다. 따라서 중요한 설정 변경은 새 ConfigMap을作成하고 Deployment의 selector를 更新하여 점진적으로 롤아웃하는 것이 안전하다.

📢 **섹션 요약 비유**: ConfigMap/Secret 관리는 항의 짐을 싸는行李配達(수하물 배달) 시스템과 같습니다. Secret은 금고에 넣고 열쇠 없으면 열 수 없게 하고(tdifscrypt), 짐을 delivery할 때는 도난 방지 포장재를 사용하고(umount), 짐을 열 사람이 누구인지 확인 후(sign) 전달합니다. 또한 짐 내용물은 절대 영수증에 적지 않습니다( Git 저장禁止).

### Ⅴ. 기대효과 및 결론 (Future & Standard)

ConfigMap/Secret을 제대로 활용하면, 조직은 완전히 새로운 수준의DevOps 문화를 달성할 수 있다. 개발자는 자신의 PC에서Local(로컬) 설정을 사용하여開発을 진행하고, CI/CD 파이프라인에서는 STG 설정을, Production에서는 PROD 설정을 자동으로注入받아同一 이미지上で全환경을 服务할 수 있다. 이는 "어떤 환경에서 실행되든 동일한 바이너리"라는 불변 인프라(Immutable Infrastructure) 원칙의實現이다.

| 기대 효과 | 도입 전 | 도입後 | 효과 |
|:---|:---|:---|:---|
| 환경 전환 시간 | 코드 수정 + 재빌드 + 재배포 (수 시간) | ConfigMap만切换 (수 십 초) | 99% 단축 |
| 민감 정보 유출 위험 | Git 히스토리에 영구 기록 | 런타임만 존재 | 完全 차단 |
| 설정 일관성 | 각 환경마다 다른 이미지 사용 | 单一 이미지 + 환경별 설정 | 100% 일관 |
| 시크릿 로테이션 | 대규모 Downtime 필요 | 파드 재시작만으로 가능 | 운영中断 최소화 |

미래에는 외부 시크릿 관리 시스템(Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault)과의集成が標準化され、Secrets Store CSI Driver와 같은 기술로 파드가外部 시크릿을 직접 마운트하여 사용하는 방식이 보편화될 것이다. 또한 시크릿의 자동 로테이션(Automatic Rotation)이 기본 기능으로 제공되어, 시크릿이 정기적으로自動更新되고 파드가 새로운 시크릿을 동적으로 다시読み込む 환경이 확대될 것이다. 결론적으로, ConfigMap/Secret은 쿠버네티스에서 설정을 관리하는 가장 기본이 되는 메커니즘이며, 12-Factor App의 "설정 외부화" 원칙을 충실히 구현하는 핵심 요소이다.

📢 **섹션 요약 비유**: ConfigMap/Secret은 항구의 화물 수송 시스템을 항구 저장소로 빗대면, 컨테이너(애플리케이션)는 내용물이 들어있는 박스이고, ConfigMap은 박스 바깥에 붙은 라벨(색상, 크기, 보관법)이며, Secret은 특별한 열쇠 없으면 열 수 없는 금고 상자(패스워드, 인증서)입니다. 이 세 가지로 화물(애플리케이션)이 안전하고 효율적으로 전 세계로 수송됩니다.

---

### 📌 관련 개념 맵 (Knowledge Graph)
- 12-Factor App | Heroku가 제시한 클라우드 네이티브 애플리케이션 개발 12가지 원칙
- 외부화된 설정 (Externalized Configuration) | 설정을 코드 밖에서 런타임에 주입받는 원칙
- RBAC (Role-Based Access Control) | 역할 기반으로 쿠버네티스 리소스 접근을 제어하는 메커니즘
- etcd 암호화 (Encryption at Rest) | 저장된 Secret의 내용을 암호화하여 보호하는 기능
- Sealed Secrets | Secret을 암호화하여 Git에 저장할 수 있게 하는 도구

### 👶 어린이를 위한 3줄 비유 설명
1. ConfigMap은 장난감 가게 포스터와 같아요. "이 장난감은 빨간색이고, 가격이 얼마야"라는 정보를 적어둔 게시판이에요.
2. Secret은 비밀이 적힌 특별한 수납 상자예요. 열쇠가 있어야만 열 수 있어서 아무나 안 볼 수 있어요.
3. 이 두 가지를 사용하면 같은 장난감(코드)을 다른 가게(DEV, PROD)에送去(보낼) 때 게시판(설정)만 바꿔주면 돼서 매우 편리해요!
