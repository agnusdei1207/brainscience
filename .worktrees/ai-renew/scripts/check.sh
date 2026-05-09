#!/usr/bin/env bash
# ============================================================
#  check.sh — Zola 빌드 사전 검사 (Docker 기반)
#  Usage: bash scripts/check.sh
#  요건: Docker Desktop 실행 상태
# ============================================================
set -euo pipefail

ZOLA_VERSION="0.19.2"
CONTENT_DIR="content"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

ERRORS=0
log()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
fail() { echo -e "${RED}[✗] $1${NC}"; ERRORS=$((ERRORS+1)); }

cd "$REPO_ROOT"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   Zola Build Pre-Check (Docker)          ║"
echo "╚══════════════════════════════════════════╝"

# ── 1. TOML: _index.md에 date 필드 금지 ──────────────────
echo ""
echo "▶ [1/4] _index.md date 필드 검사..."
INDEX_DATE=$(grep -rl "^date = " "$CONTENT_DIR" --include="_index.md" 2>/dev/null || true)
if [ -n "$INDEX_DATE" ]; then
  fail "_index.md에 허용되지 않는 'date' 필드:"
  echo "$INDEX_DATE" | sed 's/^/      /'
else
  log "_index.md date 필드 없음"
fi

# ── 2. TOML: categories 이중 따옴표 오염 ────────────────
echo ""
echo "▶ [2/4] categories TOML 필드 검사..."
BAD_CAT=$(grep -rn '^categories = "' "$CONTENT_DIR" | grep -E '"[^"]*"[a-zA-Z0-9_]+' 2>/dev/null || true)
if [ -n "$BAD_CAT" ]; then
  fail "categories 값 오류:"
  echo "$BAD_CAT" | sed 's/^/      /'
else
  log "categories 필드 정상"
fi

# ── 2.5. front matter 구분자 단독 라인 검사 ──────────────
echo ""
echo "▶ [2.5/4] front matter 형식 검사..."
BAD_FM=$(while IFS= read -r -d '' file; do
  first_line=$(sed -n '1p' "$file" | tr -d '\r')
  fm_delim=""
  if [ "$first_line" = "+++" ]; then
    fm_delim="+++"
  elif [ "$first_line" = "---" ]; then
    fm_delim="---"
  elif [[ "$first_line" == +++* || "$first_line" == ---* ]]; then
    printf '%s (delimiter)\n' "$file"
    continue
  else
    continue
  fi
  fm_body=$(awk 'NR==1 {delim=$0; sub(/\r$/, "", delim); next} {line=$0; sub(/\r$/, "", line); if (line==delim) exit; if (NR>1) print line}' "$file")
  if [ "$fm_delim" = "+++" ]; then
    if printf '%s\n' "$fm_body" | grep -qE '^[[:space:]]*[A-Za-z_][A-Za-z0-9_]*:[[:space:]]*'; then
      printf '%s (TOML-style mismatch)\n' "$file"
    fi
  else
    if printf '%s\n' "$fm_body" | grep -qE '^[[:space:]]*[A-Za-z_][A-Za-z0-9_]* =[[:space:]]*'; then
      printf '%s (YAML-style mismatch)\n' "$file"
    fi
  fi
done < <(find "$CONTENT_DIR" -name "*.md" -type f -print0 | sort -z))
if [ -n "$BAD_FM" ]; then
  fail "front matter 형식이 섞이거나 구분자가 깨진 파일:"
  printf '%s\n' "$BAD_FM" | sed 's/^/      /'
else
  log "front matter 형식 정상"
fi

# ── 3. 경로 충돌: xxx.md ↔ xxx/_index.md ────────────────
echo ""
echo "▶ [3/4] 경로 충돌 검사..."
COLLISION=0
while IFS= read -r idx; do
  dir=$(dirname "$idx")
  base=$(basename "$dir")
  parent=$(dirname "$dir")
  dup="$parent/$base.md"
  if [ -f "$dup" ]; then
    fail "경로 충돌: $dup ↔ $idx"
    COLLISION=1
  fi
done < <(find "$CONTENT_DIR" -name "_index.md")
[ "$COLLISION" -eq 0 ] && log "경로 충돌 없음"

# ── 4. Zola 빌드 ─────────────────────────────────────────
echo ""
echo "▶ [4/4] Zola 빌드 실행..."

if command -v zola &>/dev/null; then
  if zola build 2>&1; then
    log "Zola 빌드 성공!"
    rm -rf "$REPO_ROOT/public" 2>/dev/null || true
  else
    fail "Zola 빌드 실패 — 위 오류 메시지를 확인하세요"
  fi
elif command -v docker &>/dev/null; then
  docker run --rm \
    -v "$REPO_ROOT:/site" \
    -w /site \
    "ghcr.io/getzola/zola:v${ZOLA_VERSION}" \
    build \
    2>&1

  if [ $? -eq 0 ]; then
    log "Zola 빌드 성공!"
    # Docker(root)가 만든 public/ 디렉토리를 같은 컨테이너로 삭제
    docker run --rm -v "$REPO_ROOT:/site" -w /site \
      "ghcr.io/getzola/zola:v${ZOLA_VERSION}" \
      /bin/sh -c "rm -rf /site/public" 2>/dev/null || true
  else
    fail "Zola 빌드 실패 — 위 오류 메시지를 확인하세요"
  fi
else
  fail "Zola 또는 Docker가 없어 빌드를 실행할 수 없습니다"
fi

# ── 결과 ─────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════╗"
if [ "$ERRORS" -eq 0 ]; then
  echo -e "║  ${GREEN}모든 검사 통과 ✓  →  git push 안전${NC}     ║"
  echo "╚══════════════════════════════════════════╝"
else
  echo -e "║  ${RED}오류 ${ERRORS}개 발견  →  수정 후 재실행${NC}     ║"
  echo "╚══════════════════════════════════════════╝"
  exit 1
fi
echo ""
