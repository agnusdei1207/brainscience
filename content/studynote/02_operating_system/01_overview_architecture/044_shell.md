+++
title = "044. 셸 — Shell"
weight = 44
date = "2026-04-05"
[extra]
categories = "studynote-operating-system"
+++

## 0. 핵심 인사이트

> **핵심**: 셸 — Shell은(는) 운영체제가 자원을 추상화하고 통제하는 과정에서 성능, 보호, 응답성을 동시에 조율하기 위해 필요한 핵심 개념이다.
> **비유**: 셸 — Shell은(는) 복잡한 교통을 한 번에 통제해 전체 흐름을 맞추는 신호 체계와 같다.

---

📝 모범 답안

## 1. 개요 및 필요성

```
셸 (Shell):

운영체제 구조:
  사용자
    │
    ↓ (명령 입력)
  [셸 (Shell)]  ← 인터프리터, 스크립트 실행
    │
    ↓ (시스템 콜)
  [커널 (Kernel)]
    │
    ↓ (하드웨어 제어)
  [하드웨어]

셸의 역할:
  1. 명령 해석 (Command Interpretation)
  2. 명령 실행 (fork/exec 시스템 콜)
  3. 환경 변수 관리 (PATH, HOME 등)
  4. 파이프 & 리다이렉션
  5. 작업 제어 (Job Control): fg, bg, &
  6. 셸 스크립팅

명령 실행 과정:
  사용자: ls -la /tmp

  1. 셸이 입력을 파싱: 명령=ls, 인수=-la, /tmp
  2. fork(): 자식 프로세스 생성
  3. exec(): 자식에서 /bin/ls 실행
  4. wait(): 부모(셸)가 자식 종료 대기
  5. 셸 프롬프트 재표시

셸 종류:
  sh  (Bourne Shell, 1979) — POSIX 원형
  csh (C Shell, 1978) — C 문법 유사
  ksh (Korn Shell, 1983) — sh 확장
  bash (Bourne Again SHell, 1989) — Linux 표준
  zsh (Z Shell, 1990) — 강력한 자동완성
  fish (2005) — 사용자 친화, 비POSIX
```

> 📢 **섹션 요약 비유**: 셸은 번역관 — 사람의 한국어(명령)를 커널의 언어(시스템 콜)로 번역해주는 통역사. 커널은 셸이 없으면 사람과 직접 대화하기 어려워요.

---

## 2. 구성요소

```
Bash 셸 스크립팅:

기본 구조:
  #!/bin/bash          # 쉬뱅 (Shebang) — 인터프리터 지정

  NAME="World"
  echo "Hello, $NAME"

  export MY_VAR="value"

조건문:
  if [ $? -eq 0 ]; then
      echo "성공"
  elif [ $COUNT -gt 10 ]; then
      echo "10 초과"
  else
      echo "실패"
  fi

  if [ -f "/etc/passwd" ]; then echo "파일 존재"; fi
  if [ -d "/tmp" ]; then echo "디렉토리 존재"; fi

반복문:
  for i in {1..5}; do
      echo "처리 중: $i"
  done

  COUNT=0
  while [ $COUNT -lt 10 ]; do
      COUNT=$((COUNT + 1))
  done

  for FILE in /tmp/*.log; do
      echo "로그: $FILE"
  done

함수:
  greet() {
      local NAME=$1    # 지역 변수
      echo "Hello, $NAME"
      return 0
  }
  greet "Alice"

파이프 & 리다이렉션:
  ls -la | grep ".log" | wc -l

  echo "로그" >> output.log   # 추가
  cat < input.txt             # 입력 리다이렉션
  find / 2>/dev/null          # 에러 버림
```

> 📢 **섹션 요약 비유**: 셸 스크립팅은 요리 레시피 — 변수는 재료 이름, 조건은 "소금이 있으면", 반복은 "재료마다 씻고", 함수는 재사용 가능한 레시피 단위.

---

## 3. 구조 및 원리

**핵심 조건**: 운영체제의 해당 메커니즘은 현재 상태 정보, 자원 제약, 정책 기준이 함께 정합성을 가질 때 안정적으로 동작한다.

동작 순서:
1. **요청 또는 이벤트 발생**: 사용자 요청, 인터럽트, 시스템 호출 등으로 커널이 해당 기능을 처리할 필요가 생긴다.
2. **현재 상태 확인**: 커널은 큐, 제어 블록, 메타데이터, 자원 가용량을 확인해 실행 가능 여부와 우선순위를 판단한다.
3. **정책 적용 및 자원 배정**: 해당 주제의 핵심 정책에 따라 상태 전이, 자원 할당, 보호 검사를 수행한다.
4. **결과 반영 및 후속 처리**: 처리 결과를 시스템 상태에 기록하고 다음 인터럽트·스케줄링·복구 단계로 연결한다.

```
환경 변수 (Environment Variables):

주요 환경 변수:
  PATH: 실행 파일 검색 경로
  HOME: 홈 디렉토리 (/root, /home/user)
  USER: 현재 사용자 이름
  SHELL: 현재 셸 경로
  PS1: 프롬프트 형식 (user@host:~$)
  LANG: 언어/인코딩 (ko_KR.UTF-8)
  PWD: 현재 작업 디렉토리

PATH 동작:
  PATH=/usr/local/bin:/usr/bin:/bin

  ls 명령 실행:
  1. /usr/local/bin/ls 있나? 없음
  2. /usr/bin/ls 있나? 없음
  3. /bin/ls 있나? 있음 → 실행

셸 변수 vs 환경 변수:
  MY_VAR="local"   → 현재 셸만 (export 없음)
  export MY_VAR    → 자식 프로세스에게 상속

  확인: env | grep MY_VAR
  삭제: unset MY_VAR

특수 변수:
  $0: 스크립트 이름
  $1~$9: 위치 매개변수
  $#: 인수 개수
  $@: 모든 인수 (배열)
  $?: 이전 명령 종료 코드 (0=성공)
  $$: 현재 프로세스 PID
  $!: 마지막 백그라운드 PID

셸에서 프로세스 생성:
  fg_job: 포그라운드 (셸 대기)
  bg_job &: 백그라운드 (셸 즉시 프롬프트)

  작업 제어:
  Ctrl+Z: 일시 중지 (SIGTSTP)
  bg: 백그라운드 재개
  fg: 포그라운드로 가져오기
  jobs: 백그라운드 작업 목록
```

> 📢 **섹션 요약 비유**: 환경 변수는 작업 도시락 — PATH는 식당 위치 목록, HOME은 집 주소, 셸은 도시락을 자식(프로세스)에게 전달할 때 export로 챙겨줘요.

---

## 4. 비교 및 연결

```
환경 변수 (Environment Variables):

주요 환경 변수:
  PATH: 실행 파일 검색 경로
  HOME: 홈 디렉토리 (/root, /home/user)
  USER: 현재 사용자 이름
  SHELL: 현재 셸 경로
  PS1: 프롬프트 형식 (user@host:~$)
  LANG: 언어/인코딩 (ko_KR.UTF-8)
  PWD: 현재 작업 디렉토리

PATH 동작:
  PATH=/usr/local/bin:/usr/bin:/bin

  ls 명령 실행:
  1. /usr/local/bin/ls 있나? 없음
  2. /usr/bin/ls 있나? 없음
  3. /bin/ls 있나? 있음 → 실행

셸 변수 vs 환경 변수:
  MY_VAR="local"   → 현재 셸만 (export 없음)
  export MY_VAR    → 자식 프로세스에게 상속

  확인: env | grep MY_VAR
  삭제: unset MY_VAR

특수 변수:
  $0: 스크립트 이름
  $1~$9: 위치 매개변수
  $#: 인수 개수
  $@: 모든 인수 (배열)
  $?: 이전 명령 종료 코드 (0=성공)
  $$: 현재 프로세스 PID
  $!: 마지막 백그라운드 PID

셸에서 프로세스 생성:
  fg_job: 포그라운드 (셸 대기)
  bg_job &: 백그라운드 (셸 즉시 프롬프트)

  작업 제어:
  Ctrl+Z: 일시 중지 (SIGTSTP)
  bg: 백그라운드 재개
  fg: 포그라운드로 가져오기
  jobs: 백그라운드 작업 목록
```

> 📢 **섹션 요약 비유**: 환경 변수는 작업 도시락 — PATH는 식당 위치 목록, HOME은 집 주소, 셸은 도시락을 자식(프로세스)에게 전달할 때 export로 챙겨줘요.

---

## 5. 실무 적용 및 판단

```
고급 셸 기능:

프로세스 치환 (Process Substitution):
  diff <(ls dir1) <(ls dir2)
  → 명령 출력을 파일처럼 사용

Here Document:
  cat <<EOF
  여러 줄 텍스트
  변수 $NAME 사용 가능
  EOF

배열:
  ARR=("a" "b" "c")
  echo ${ARR[0]}        # a
  echo ${#ARR[@]}       # 3 (길이)
  for ITEM in "${ARR[@]}"; do echo $ITEM; done

문자열 조작:
  STR="hello_world.txt"
  echo ${STR^^}          # 대문자: HELLO_WORLD.TXT
  echo ${STR%.*}         # 확장자 제거: hello_world
  echo ${STR#*_}         # 앞부분 제거: world.txt
  echo ${STR/hello/Hi}   # 치환: Hi_world.txt

정규 표현식:
  [[ "hello123" =~ ^[a-z]+[0-9]+$ ]] && echo "매치"

Zsh 차이점:
  자동완성: 탭키로 경로/명령 자동완성 (bash보다 강력)
  플러그인: Oh-My-Zsh 생태계
  Globbing: **/*.txt (재귀 탐색)

fish 특징:
  문법: if command; echo OK; end
  자동 제안: 이력 기반 실시간 제안
  비POSIX: bash 스크립트와 호환 안 됨

셸 최적화:
  .bashrc vs .bash_profile:
    .bash_profile: 로그인 셸 (한 번)
    .bashrc: 인터랙티브 셸 (매번)

  alias 정의:
    alias ll="ls -la"
    alias gs="git status"
```

> 📢 **섹션 요약 비유**: 고급 셸 기능은 개인 비서 커스터마이징 — alias는 단축 명령어(습관 단어), .bashrc는 출근 시 비서에게 전달하는 설정 메모. 셸을 내 입맛에 맞게 꾸밀 수 있어요.

---

## 6. 기대효과 및 결론

```
CI/CD 배포 셸 스크립트:

deploy.sh:
  #!/bin/bash
  set -e            # 오류 시 즉시 종료
  set -u            # 미정의 변수 사용 시 오류
  set -o pipefail   # 파이프 중 오류 감지

  APP_NAME="myapp"
  DEPLOY_DIR="/opt/$APP_NAME"
  BACKUP_DIR="/opt/backup"

  log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"; }

  check_health() {
      local URL=$1
      local HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $URL)
      [ "$HTTP_CODE" = "200" ]
  }

  log "백업 시작"
  cp -r $DEPLOY_DIR $BACKUP_DIR/$(date +%Y%m%d_%H%M%S)

  log "배포 시작"
  git -C $DEPLOY_DIR pull origin main

  pip install -r requirements.txt --quiet

  systemctl restart $APP_NAME

  log "헬스체크 중..."
  RETRY=0
  while ! check_health "http://localhost:8080/health"; do
      RETRY=$((RETRY+1))
      if [ $RETRY -gt 10 ]; then
          log "헬스체크 실패 — 롤백"
          cp -r $BACKUP_DIR/latest $DEPLOY_DIR
          systemctl restart $APP_NAME
          exit 1
      fi
      sleep 3
  done

  log "배포 완료"

사용:
  chmod +x deploy.sh
  ./deploy.sh 2>&1 | tee -a /var/log/deploy.log
```

> 📢 **섹션 요약 비유**: CI/CD 셸 스크립트는 자동 이사 — 기존 짐 백업 → 새 짐 배치 → 입주 확인(헬스체크) → 문제면 자동 되돌리기. 사람 손 없이 자동으로 안전하게 배포.

---

## 7. 발전 흐름도

```
[Thompson Shell (1971)]
Unix v1 최초 셸
기본 명령 실행만
      |
      v
[Bourne Shell sh (1979)]
스크립팅 기초 (조건, 반복, 함수)
POSIX 표준의 원형
      |
      v
[Bash (1989)]
GNU 프로젝트 sh 대체
Linux 표준 셸로 자리잡음
      |
      v
[Zsh + Oh-My-Zsh (2009~)]
플러그인 생태계 형성
macOS 기본 셸 전환 (2019)
      |
      v
[현재: DevOps 자동화]
Bash + CI/CD (GitHub Actions)
Container 셸 (Alpine sh)
셸 대신 Python 스크립트 증가
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
| 셸 — Shell | 운영체제 자원 관리와 보호 정책이 실제로 적용되는 핵심 주제 |
| 커널 (Kernel) | 정책 집행, 상태 전이, 시스템 호출 처리의 중심 |
| 프로세스/스레드 | CPU, 메모리, 동기화 자원과 직접 연결되는 실행 단위 |
| 메모리/I/O | 성능 병목과 보호 요구사항이 함께 드러나는 연계 영역 |
| 가상화/보안 | 격리, 제어, 관측 확장 관점에서 해당 주제가 연결되는 상위 개념 |
