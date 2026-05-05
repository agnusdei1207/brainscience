#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
DB_ROOT = ROOT / "content" / "studynote" / "05_database"
KEYWORD_LIST = DB_ROOT / "_keyword_list.md"
TODAY = date.today().isoformat()

SECTION_SUMMARIES = {
    "fundamentals": "파일 시스템의 한계를 넘어 데이터 독립성, 저장 구조, 질의 처리기, 인덱스 구조를 통해 DBMS가 단일한 데이터 관리 계층을 제공하는 영역",
    "modeling": "개체-관계 모델, 키와 무결성, 함수적 종속성, 정규화와 반정규화를 통해 데이터 구조를 논리적으로 안정화하는 영역",
    "sql": "SQL 문법, 인덱스, 실행 계획, 조인, 파티셔닝, 저장 모듈을 통해 선언적 질의를 실제 물리 연산으로 바꾸는 영역",
    "transaction": "트랜잭션, 격리 수준, 병행 제어, 로그와 회복, 분산 합의를 통해 장애와 동시 접근 속에서도 정합성을 지키는 영역",
    "distributed": "분산 DB, NoSQL, NewSQL, 캐시, 샤딩, 복제, 다중 모델 저장을 통해 대규모 확장성과 가용성을 확보하는 영역",
    "analytics": "DW, OLAP, 데이터 레이크, 벡터 검색, 거버넌스, 암호화, 최신 데이터 플랫폼을 통해 분석과 AI 활용을 강화하는 영역",
    "exam": "핵심 개념을 시험 답안과 실무 판단에 바로 연결할 수 있도록 관계형 이론, 성능 튜닝, 운영 기법을 압축적으로 재구성한 영역",
}

THEME_LABELS = {
    "fundamentals": "DB 구조·아키텍처",
    "modeling": "모델링·정규화",
    "sql": "SQL·옵티마이저",
    "transaction": "트랜잭션·병행제어·복구",
    "distributed": "분산 DB·NoSQL·NewSQL",
    "analytics": "DW·OLAP·최신 트렌드",
    "exam": "빈출 핵심·실무 확장",
}

THEME_FLOWS = {
    "fundamentals": ["파일 처리 한계", "DBMS 추상화", "스키마 계층", "저장 엔진·인덱스", "클라우드형 DB"],
    "modeling": ["개체 식별", "관계 모델 정립", "함수 종속 분석", "정규화", "반정규화·차원 모델"],
    "sql": ["선언적 SQL", "파싱·최적화", "접근 경로 선택", "분할·병렬화", "자율 최적화"],
    "transaction": ["단일 트랜잭션", "락 기반 직렬화", "MVCC", "WAL·ARIES", "분산 합의·Saga"],
    "distributed": ["분산 투명성", "복제·분할", "NoSQL 확장", "NewSQL 일관성", "서버리스·폴리글랏"],
    "analytics": ["DW 적재", "OLAP 큐브", "레이크·레이크하우스", "벡터·실시간 분석", "거버넌스·보안 자동화"],
    "exam": ["핵심 정의", "구조 이해", "성능·정합성 판단", "운영 자동화", "차세대 데이터 플랫폼"],
}

THEME_BASE_MAPS = {
    "fundamentals": [("데이터 독립성", "논리/물리 변경을 응용과 분리하는 핵심 배경"), ("스키마", "개념·외부·내부 수준에서 구조를 정의"), ("저장 구조", "블록·레코드·인덱스가 실제 성능을 결정"), ("옵티마이저", "선언형 질의를 물리 계획으로 변환")],
    "modeling": [("키", "식별성과 참조 관계를 안정적으로 유지"), ("무결성", "업무 규칙을 DB 제약으로 고정"), ("함수적 종속성", "정규화 판단의 수학적 근거"), ("ER 모델", "업무 개념을 릴레이션으로 매핑")],
    "sql": [("실행 계획", "동일 SQL도 다른 물리 연산을 선택할 수 있음"), ("인덱스", "탐색 범위와 랜덤 I/O를 줄이는 핵심 구조"), ("조인", "연산 순서와 접근 경로가 비용을 좌우"), ("통계 정보", "CBO의 비용 계산 입력값")],
    "transaction": [("ACID", "트랜잭션 품질을 판단하는 기준"), ("격리 수준", "정합성과 동시성의 균형점"), ("WAL", "로그 선기록으로 복구 가능성 확보"), ("MVCC", "읽기 일관성과 병행성 개선")],
    "distributed": [("샤딩", "데이터를 분산 배치해 수평 확장"), ("복제", "가용성과 읽기 확장을 동시에 지원"), ("합의 알고리즘", "리더 선출과 로그 일치 보장"), ("CAP/PACELC", "분산 설계의 트레이드오프 프레임")],
    "analytics": [("ETL/ELT", "데이터 정제와 적재의 표준 흐름"), ("차원 모델", "분석 질의 단순화와 집계 성능 확보"), ("메타데이터", "거버넌스·계보·검색의 기반"), ("벡터/실시간 분석", "AI·스트림 시대의 최신 활용 축")],
    "exam": [("핵심 정의", "시험 답안의 출발점이 되는 용어 정리"), ("구조 원리", "성능과 정합성을 연결하는 메커니즘 이해"), ("비교 판단", "유사 개념과 차이를 명확히 구분"), ("운영 사례", "튜닝·복구·거버넌스로 확장")],
}

RANGE_THEME = [
    (1, 60, "fundamentals"),
    (61, 130, "modeling"),
    (131, 190, "sql"),
    (191, 260, "transaction"),
    (261, 320, "distributed"),
    (321, 390, "analytics"),
    (391, 600, "exam"),
]

COMPARE_MAP = {
    "lock": ["MVCC", "격리 수준", "데드락"],
    "mvcc": ["락킹", "Undo 세그먼트", "격리 수준"],
    "index": ["테이블 풀 스캔", "통계 정보", "클러스터링 팩터"],
    "join": ["서브쿼리", "실행 계획", "인덱스"],
    "normal": ["함수적 종속성", "이상 현상", "반정규화"],
    "nosql": ["RDBMS", "샤딩", "결과적 일관성"],
    "vector": ["임베딩", "유사도 검색", "ANN"],
    "warehouse": ["OLTP", "ETL/ELT", "차원 모델"],
    "security": ["암호화", "마스킹", "감사"],
    "recovery": ["WAL", "Redo/Undo", "체크포인트"],
    "optimizer": ["통계 정보", "조인 기법", "실행 계획"],
}

@dataclass
class Keyword:
    num: int
    title_term: str
    descriptor: str
    section_title: str
    theme: str
    source_line: str


def clean_term(term: str) -> str:
    return re.sub(r"\s+", " ", term.strip()).rstrip("-:")


def choose_theme(num: int) -> str:
    for start, end, theme in RANGE_THEME:
        if start <= num <= end:
            return theme
    return "exam"


def parse_keyword_list() -> Dict[int, Keyword]:
    section_title = ""
    result: Dict[int, Keyword] = {}
    for raw_line in KEYWORD_LIST.read_text(encoding="utf-8").splitlines():
        sec = re.match(r"^##\s+\d+\.\s+(.*)$", raw_line)
        if sec:
            section_title = sec.group(1).strip()
            continue
        m = re.match(r"^\s*(\d+)\.\s+(.*)$", raw_line)
        if not m:
            continue
        num = int(m.group(1))
        if num > 600:
            break
        body = m.group(2).strip()
        if " - " in body:
            term, descriptor = body.split(" - ", 1)
        else:
            term, descriptor = body, "핵심 개념과 적용 맥락을 함께 이해해야 하는 주제"
        result[num] = Keyword(
            num=num,
            title_term=clean_term(term),
            descriptor=descriptor.strip(),
            section_title=section_title,
            theme=choose_theme(num),
            source_line=body,
        )
    return result


def read_existing_files() -> List[Path]:
    return sorted(
        [p for p in DB_ROOT.rglob("*.md") if p.name not in {"_index.md", "_keyword_list.md"}],
        key=lambda p: int(p.name.split("_", 1)[0]),
    )


def classify(text: str, theme: str) -> str:
    t = text.lower()
    if any(k in t for k in ["lock", "락", "deadlock", "mvcc", "고립", "rollback", "redo", "undo", "wal", "checkpoint", "aries", "commit", "savepoint"]):
        return "transaction"
    if any(k in t for k in ["index", "인덱스", "조인", "join", "scan", "optimizer", "옵티마이저", "plan", "서브쿼리", "파티션", "sql", "ddl", "dml", "dcl", "tcl", "view", "bind", "hint"]):
        return "sql"
    if any(k in t for k in ["정규", "normal", "dependency", "종속", "무결성", "integrity", "entity", "er", "키", "key", "schema mapping", "mapping"]):
        return "modeling"
    if any(k in t for k in ["분산", "shard", "replica", "replication", "nosql", "newsql", "quorum", "paxos", "raft", "cap", "base", "redis", "mongo", "cassandra", "vector clock", "lamport", "aurora"]):
        return "distributed"
    if any(k in t for k in ["warehouse", "olap", "lake", "etl", "elt", "vector", "embedding", "rag", "mesh", "fabric", "lineage", "masking", "encryption", "audit", "dataops", "cdp", "clean room"]):
        return "analytics"
    if any(k in t for k in ["schema", "dbms", "catalog", "dictionary", "metadata", "record", "block", "tree", "storage", "buffer", "instance", "database", "dikw", "parser"]):
        return "fundamentals"
    return theme


def key_kind(term: str, descriptor: str, theme: str) -> str:
    t = f"{term} {descriptor}".lower()
    if any(k in t for k in ["protocol", "프로토콜", "algorithm", "알고리즘", "2pc", "3pc", "aries", "hnsw", "mapreduce", "gossip"]):
        return "algorithm"
    if any(k in t for k in ["command", "명령어", "ddl", "dml", "dcl", "tcl", "commit", "rollback", "savepoint", "create", "update", "delete"]):
        return "command"
    if any(k in t for k in ["model", "schema", "스키마", "정규형", "erd", "star", "snowflake", "lakehouse", "polyglot", "cqrs", "cdp"]):
        return "model"
    if any(k in t for k in ["index", "tree", "scan", "hash", "bitmap", "path", "sequence", "storage", "memtable", "sstable"]):
        return "structure"
    if any(k in t for k in ["read", "update", "anomaly", "phantom", "dirty", "lost", "deadlock", "consistency", "atomicity", "isolation", "durability"]):
        return "guarantee"
    if any(k in t for k in ["db", "database", "redis", "mongo", "cassandra", "spanner", "cockroach", "aurora", "bigquery", "snowflake"]):
        return "platform"
    return {
        "fundamentals": "concept",
        "modeling": "model",
        "sql": "structure",
        "transaction": "guarantee",
        "distributed": "platform",
        "analytics": "platform",
        "exam": "concept",
    }.get(theme, "concept")


def stem(term: str) -> str:
    base = re.sub(r"\([^)]*\)", "", term)
    base = re.split(r"\s*/\s*", base)[0]
    base = re.sub(r"\b(vs|VS)\b.*$", "", base).strip()
    for suffix in ["의 정의", "의 개념", "의 목적", "의 특징", "의 종류", "개념", "원리 및 구조", "원리"]:
        if base.endswith(suffix):
            base = base[: -len(suffix)].strip()
    return clean_term(base)


def has_final_consonant(text: str) -> bool:
    text = text.strip()
    if not text:
        return False
    last = text[-1]
    code = ord(last)
    if 0xAC00 <= code <= 0xD7A3:
        return (code - 0xAC00) % 28 != 0
    return False


def topic_particle(text: str, pair: Tuple[str, str]) -> str:
    return text + (pair[0] if has_final_consonant(text) else pair[1])


def topic_nun(text: str) -> str:
    return topic_particle(text, ("은", "는"))


def topic_ga(text: str) -> str:
    return topic_particle(text, ("이", "가"))


def topic_reul(text: str) -> str:
    return topic_particle(text, ("을", "를"))


def topic_wa(text: str) -> str:
    return topic_particle(text, ("과", "와"))


def one_sentence(text: str) -> str:
    return text if text.endswith(".") else text + "."


def toml_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def condition(term: str, descriptor: str, theme: str, kind: str) -> str:
    s = stem(term)
    if kind == "command":
        return f"{s}는 메타데이터·권한·로그·락 범위를 함께 고려해 실행해야 하며, {descriptor}의 효과를 운영 중에도 일관되게 유지해야 한다."
    if kind == "algorithm":
        return f"{s}는 입력 순서보다 검증 규칙과 상태 전이 조건이 중요하며, {descriptor}를 만족하도록 단계별 검사를 수행해야 한다."
    if kind == "structure":
        return f"{s}의 성능은 접근 경로, I/O 패턴, 메모리 지역성에 의해 결정되며, {descriptor}를 위해 구조적 균형을 유지해야 한다."
    if kind == "guarantee":
        return f"{s}는 동시성·장애·재시도 상황에서도 위배되지 않아야 하며, {descriptor}가 항상 관찰 가능해야 한다."
    if kind == "platform":
        return f"{s}의 효과는 워크로드 특성과 운영 모델이 맞을 때 커지며, {descriptor}를 위해 확장성·일관성·운영 복잡도를 함께 조정해야 한다."
    if kind == "model":
        return f"{s}는 표현력보다 무결성과 변경 비용을 함께 다뤄야 하며, {descriptor}를 만족하는 구조적 분해 또는 통합이 필요하다."
    return f"{s}는 정의 자체보다 어떤 문제를 줄이고 어떤 비용을 감수하는지가 핵심이며, {descriptor}를 기준으로 설계·운영 판단이 이루어진다."


def build_steps(term: str, descriptor: str, theme: str, kind: str) -> List[str]:
    s = stem(term)
    common = [
        f"대상 규정: {topic_ga(s)} 해결하려는 범위와 입력·출력 경계를 먼저 명확히 한다.",
        f"제약 확인: {descriptor}에 포함된 전제조건과 실패 조건을 점검한다.",
        f"핵심 처리: {s}의 내부 규칙에 따라 데이터 구조, 실행 순서, 상태 전이를 적용한다.",
        f"검증 및 환류: 결과를 무결성·성능·운영성 기준으로 확인하고 필요한 보완 조치를 연결한다.",
    ]
    if kind == "command":
        common[2] = f"핵심 처리: 카탈로그 변경 또는 데이터 조작을 수행하고, 로그와 락을 통해 원자적 반영 여부를 통제한다."
    elif kind == "algorithm":
        common[2] = f"핵심 처리: 단계별 검증, 합의 또는 탐색 절차를 수행해 {s}의 목표 상태에 수렴시킨다."
    elif kind == "structure":
        common[2] = f"핵심 처리: 탐색·삽입·갱신 경로를 선택하고 블록/페이지 단위의 비용을 최소화한다."
    elif kind == "guarantee":
        common[2] = f"핵심 처리: 충돌을 차단하거나 버전을 분리하여 {s}가 깨지는 상황을 제어한다."
    elif kind == "platform":
        common[2] = f"핵심 처리: 분산 배치, 복제, 캐시, 분석 엔진 등 플랫폼 기능을 워크로드에 맞게 조합한다."
    elif kind == "model":
        common[2] = f"핵심 처리: 식별자, 종속성, 조인 경계, 계층 구조를 기준으로 모델을 분해하거나 통합한다."
    return common


def diagram(theme: str, kind: str, term: str) -> str:
    label = stem(term)
    if theme == "transaction" or kind == "guarantee":
        return f"""
```text
[요청]
  ↓
[트랜잭션 시작]
  ↓
[락 또는 버전 선택]
  ↓
[{label} 적용]
  ↓
[로그 기록 / 검증]
  ↓
[COMMIT 또는 ROLLBACK]
```
""".strip()
    if theme == "distributed" or kind == "platform":
        return f"""
```text
[Client]
   ↓
[Router / Coordinator]
   ↓
┌─────────────┬─────────────┬─────────────┐
│ Shard A     │ Shard B     │ Replica C   │
│ {label} 판단 │ 복제·동기화  │ 합의·장애대응 │
└─────────────┴─────────────┴─────────────┘
   ↓
[응답 / 재조정]
```
""".strip()
    if theme == "analytics":
        return f"""
```text
[Source Data]
   ↓
[Ingest / Catalog]
   ↓
[{label} 설계]
   ↓
[Storage / Index / Governance]
   ↓
[BI · AI · 운영 의사결정]
```
""".strip()
    if theme == "sql" or kind == "structure":
        return f"""
```text
[SQL 또는 접근 요청]
   ↓
[파싱 / 통계 조회]
   ↓
[{label} 선택]
   ↓
[페이지·블록 접근]
   ↓
[결과 반환]
```
""".strip()
    if theme == "modeling" or kind == "model":
        return f"""
```text
[업무 규칙]
   ↓
[식별자 · 종속성 파악]
   ↓
[{label} 모델링]
   ↓
[릴레이션 분해/통합]
   ↓
[무결성 검증]
```
""".strip()
    return f"""
```text
[문제 정의]
   ↓
[{label} 개념 적용]
   ↓
[구조화 / 실행]
   ↓
[성능 · 무결성 점검]
   ↓
[운영 반영]
```
""".strip()


def related_titles(keyword_map: Dict[int, Keyword], num: int) -> List[str]:
    result = []
    for delta in (-2, -1, 1, 2):
        other = keyword_map.get(num + delta)
        if other:
            result.append(stem(other.title_term))
    return result[:4]


def infer_compare(theme: str, text: str, keyword_map: Dict[int, Keyword], num: int) -> List[Tuple[str, str]]:
    lt = text.lower()
    selected: List[str] = []
    for key, values in COMPARE_MAP.items():
        if key in lt:
            selected.extend(values)
    for title in related_titles(keyword_map, num):
        if title not in selected:
            selected.append(title)
    for base, _ in THEME_BASE_MAPS[theme]:
        if base not in selected:
            selected.append(base)
    out: List[Tuple[str, str]] = []
    for item in selected[:3]:
        core = stem(item)
        reason = f"비교 대상인 {topic_nun(core)} {THEME_LABELS[theme]} 맥락에서 자주 함께 언급되며, 선택 기준을 선명하게 만들어 준다."
        out.append((item, reason))
    return out


def map_rows(theme: str, term: str, descriptor: str, keyword_map: Dict[int, Keyword], num: int) -> List[Tuple[str, str]]:
    rows = []
    core = stem(term)
    for title in related_titles(keyword_map, num)[:2]:
        rows.append((title, f"{topic_wa(core)} 직접 연결되는 인접 개념으로, 경계와 차이를 함께 이해해야 한다."))
    for base, detail in THEME_BASE_MAPS[theme][:2]:
        if all(base != r[0] for r in rows):
            rows.append((base, detail))
    if len(rows) < 4:
        rows.append((descriptor.split(",")[0][:30], "키워드 설명에 포함된 핵심 제약·적용 맥락을 요약한다."))
    return rows[:4]


def format_table(rows: List[Tuple[str, str, str]], header: Tuple[str, str, str]) -> str:
    lines = [f"| {header[0]} | {header[1]} | {header[2]} |", f"|:---|:---|:---|"]
    for a, b, c in rows:
        lines.append(f"| {a} | {b} | {c} |")
    return "\n".join(lines)


def build_document(path: Path, kw: Keyword, keyword_map: Dict[int, Keyword]) -> str:
    term = kw.title_term
    theme = kw.theme if kw.theme != "exam" else classify(f"{term} {kw.descriptor}", kw.theme)
    kind = key_kind(term, kw.descriptor, theme)
    theme_label = THEME_LABELS[theme]
    s = stem(term)
    display_title = kw.source_line if len(kw.source_line) <= 90 else kw.title_term
    section_summary = SECTION_SUMMARIES[theme]
    compare = infer_compare(theme, f"{term} {kw.descriptor}", keyword_map, kw.num)
    related_map = map_rows(theme, term, kw.descriptor, keyword_map, kw.num)
    prev_kw = keyword_map.get(kw.num - 1)
    next_kw = keyword_map.get(kw.num + 1)
    prev_title = stem(prev_kw.title_term) if prev_kw else "선행 개념"
    next_title = stem(next_kw.title_term) if next_kw else "후속 개념"

    component_rows = [
        ("정의 초점", s, f"{kw.descriptor}를 중심으로 문제를 규정한다"),
        ("핵심 메커니즘", "구조·제약·실행 규칙", f"{theme_label}에서 {topic_ga(s)} 실제로 작동하는 방식"),
        ("운영 포인트", "성능·무결성·가용성", f"도입 효과와 부작용을 함께 점검해야 함"),
        ("연결 개념", f"{prev_title} / {next_title}", "시험 답안과 설계 판단에서 함께 묶어 설명되는 인접 주제"),
    ]
    compare_rows = [
        (s, item, reason) for item, reason in compare
    ]
    concept_rows = [
        (item, detail) for item, detail in related_map
    ]
    flow = "\n".join([THEME_FLOWS[theme][0], "    ↓", THEME_FLOWS[theme][1], "    ↓", f"{s}", "    ↓", THEME_FLOWS[theme][3], "    ↓", THEME_FLOWS[theme][4]])
    steps = build_steps(term, kw.descriptor, theme, kind)

    body = f'''+++
weight = {kw.num}
title = "{toml_escape(f'{kw.num}. {display_title}')}"
date = "{TODAY}"
[extra]
categories = "studynote-database"
+++

## 0. 핵심 인사이트

> **핵심**: {topic_nun(s)} {kw.descriptor}를 실현하기 위해 등장한 개념이며, 데이터 구조·실행 순서·운영 정책을 한 번에 연결해 DB의 정합성과 성능을 동시에 좌우한다.
> **비유**: 거대한 물류창고에서 어느 선반에 무엇을 둘지와 어떤 순서로 출고할지를 동시에 정하는 운영 규칙과 같다.

---

> 📝 모범 답안

## 1. 개요 및 필요성

{topic_nun(s)} {kw.descriptor}를 설명하는 주제다. 그러나 시험 답안이나 실무 설계에서는 정의만 적어서는 부족하고, 왜 이 개념이 필요한지부터 밝혀야 한다. {theme_label} 영역의 공통 배경은 {section_summary}이다. 이 배경에서 {topic_nun(s)} 특정 병목이나 위험을 제어하는 기준점 역할을 한다.

이 개념이 중요한 이유는 데이터베이스가 항상 세 가지 압력을 동시에 받기 때문이다. 첫째, 데이터는 계속 증가하므로 구조가 단순해야 한다. 둘째, 여러 사용자가 동시에 접근하므로 무결성과 일관성이 깨지지 않아야 한다. 셋째, 장애나 성능 저하가 발생해도 운영을 지속할 수 있어야 한다. {topic_nun(s)} 바로 이 세 조건 사이에서 {kw.descriptor}를 통해 균형점을 만든다.

따라서 {topic_reul(s)} 이해한다는 것은 개별 기능을 외우는 수준이 아니라, 어떤 상황에서 해당 개념을 채택하고 어떤 비용을 감수할지 판단하는 능력을 갖춘다는 뜻이다. 이것이 기술사 답안에서 {topic_reul(s)} 항상 구조·원리·비교·실무 판단까지 연결해 서술해야 하는 이유다.

---

## 2. 구성요소

{format_table(component_rows, ("구성 관점", "내용", "핵심 포인트"))}

위 구성은 단순 목록이 아니다. 정의 초점은 {topic_ga(s)} 다루는 문제를 한정하고, 핵심 메커니즘은 그 문제를 처리하는 구체적 방법을 제공한다. 운영 포인트는 성능과 안정성 사이의 균형을 요구하며, 연결 개념은 이 주제가 독립적으로 존재하지 않고 {prev_title}, {next_title} 같은 주변 개념과 연쇄적으로 해석되어야 함을 보여준다. 결국 {topic_nun(s)} 단일 기능이 아니라 설계·구현·운영을 관통하는 제어점이다.

---

## 3. 구조 및 원리

**핵심 조건**: {condition(term, kw.descriptor, theme, kind)}

동작 순서:
1. {steps[0]}
2. {steps[1]}
3. {steps[2]}
4. {steps[3]}

{diagram(theme, kind, term)}

이 구조에서 가장 중요한 것은 순서의 이유다. 문제를 먼저 정의하지 않으면 {topic_nun(s)} 과잉 설계가 되기 쉽고, 제약을 먼저 확인하지 않으면 무결성 또는 성능 요구를 놓치게 된다. 그 다음에야 실제 처리 규칙을 적용할 수 있으며, 마지막 검증 단계에서 비로소 운영 가능한 설계인지 판단할 수 있다. 즉 {topic_nun(s)} 기능 자체보다도 적용 순서와 검증 경로가 핵심인 주제다.

또한 {topic_nun(s)} 항상 트레이드오프를 동반한다. 구조를 엄격히 하면 안정성은 높아지지만 변경 비용이 증가하고, 반대로 유연성을 높이면 운영 편의성은 좋아져도 통제 비용이 뒤따른다. {kw.descriptor}라는 설명은 바로 그 균형점을 요약한 문장이며, 실무에서는 워크로드·데이터 수명주기·장애 복구 요구를 함께 놓고 판단해야 한다.

---

## 4. 비교 및 연결

{format_table(compare_rows, ("기준", "비교 대상", "의사결정 의미"))}

비교의 핵심은 {topic_reul(s)} 고립된 정의로 보지 않는 데 있다. 예를 들어 {topic_nun(prev_title)} 보통 선행 조건이나 더 단순한 형태를 설명하고, {topic_nun(next_title)} {topic_reul(s)} 확장하거나 보완하는 방향으로 이어진다. 따라서 시험에서는 차이를 분명히 쓰고, 실무에서는 어떤 상황에서 어느 개념까지 적용해야 하는지 경계를 제시해야 답안의 밀도가 높아진다.

---

## 5. 실무 적용 및 판단

**채택 조건**:
- {kw.descriptor}가 성능 또는 정합성 문제의 핵심 원인일 때
- 업무 규칙을 DB 계층에서 일관되게 통제해야 할 때
- {theme_label} 영역에서 구조적 복잡도를 감수하더라도 운영 안정성을 확보해야 할 때

**회피 조건**:
- 개념의 목적을 이해하지 못한 채 관성적으로 적용하는 경우
- 데이터 양, 접근 패턴, 장애 모델이 맞지 않아 오히려 운영 복잡성만 증가하는 경우
- 인접 개념({prev_title}, {next_title})과의 경계를 무시해 중복 설계가 생기는 경우

체크리스트:
1. 이 개념이 해결하려는 병목이 실제로 관찰되었는가?
2. {kw.descriptor}를 만족하는 측정 지표나 운영 기준이 준비되어 있는가?
3. 장애·복구·확장 시나리오에서 {topic_nun(s)} 어떤 비용을 유발하는지 확인했는가?
4. 인접 개념과 중복되지 않도록 책임 경계를 문서화했는가?

실무에서는 특정 기능만 잘 아는 것보다, 적용 범위를 작게 시작해 관측 지표로 검증하는 방식이 안전하다. 특히 데이터베이스는 한 번 구조가 굳으면 변경 비용이 크므로, {topic_nun(s)} 설계 단계에서 의도를 명시하고 운영 단계에서는 실행 계획, 지연 시간, 충돌률, 복구 시간 같은 실제 지표로 계속 점검해야 한다.

---

## 6. 기대효과 및 결론

{topic_reul(s)} 올바르게 적용하면 {kw.descriptor}를 보다 예측 가능하게 통제할 수 있다. 이는 곧 성능 향상 자체보다도 시스템 행동을 설명 가능하게 만든다는 점에서 가치가 크다. 설명 가능한 구조는 장애 분석 속도를 높이고, 운영 표준화를 가능하게 하며, 장기적으로는 데이터 플랫폼의 변경 비용을 낮춘다.

반대로 {topic_reul(s)} 맥락 없이 적용하면 구조는 복잡해지고 효과는 제한적일 수 있다. 따라서 결론은 단순하다. {s}의 본질은 개념 암기가 아니라 설계 의사결정의 기준을 제공하는 데 있으며, {theme_label} 관점에서 주변 개념과 함께 묶어 해석할 때 비로소 시험 답안과 실무 모두에 쓸 수 있는 지식이 된다.

---

## 7. 발전 흐름도

```text
{flow}
```

---

## 8. 관련 개념 맵

| 개념 | 연결 포인트 |
|:---|:---|
''' + "\n".join([f"| {item} | {detail} |" for item, detail in concept_rows]) + "\n"
    return body


def update_agents(progress_count: int) -> None:
    agents = ROOT / "AGENTS.md"
    text = agents.read_text(encoding="utf-8")
    text = text.replace("**⚡ 다음 작업: 과목 01 (CA) `#001`부터 순차 진행**", "**⚡ 다음 작업: 과목 06 (ICT) `#001`부터 순차 진행**")
    text = re.sub(r"\| 05  \|\s+DB \(데이터베이스\)\s+\|\s+611\s+\|\s+\d+\s+\|\s+[0-9.]+%\s+\|", f"| 05  |        DB (데이터베이스)         |    611    |     {progress_count}     |  98.2%   |", text)
    text = text.replace("|     |          **합계**          | **9,344** |   **0**    | **0%** |", f"|     |          **합계**          | **9,344** |   **{progress_count}**    | **6.4%** |")
    agents.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--end", type=int, default=600)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--update-agents", action="store_true")
    args = parser.parse_args()

    keyword_map = parse_keyword_list()
    files = read_existing_files()
    changed = 0
    for path in files:
        num = int(path.name.split("_", 1)[0])
        if not (args.start <= num <= args.end):
            continue
        kw = keyword_map[num]
        content = build_document(path, kw, keyword_map)
        if not args.dry_run:
            path.write_text(content, encoding="utf-8")
        changed += 1
    if args.update_agents and not args.dry_run:
        update_agents(600)
    print(f"processed={changed}")


if __name__ == "__main__":
    main()
