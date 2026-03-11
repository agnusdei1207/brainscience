#!/usr/bin/env python3
import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
STUDYNOTE_ROOT = REPO_ROOT / "content" / "studynote"

HEADING_RE = re.compile(r"^##\s+(\d+)\.\s+(.+)$")
KEYWORD_RE = re.compile(r"^(\d+)\.\s+(.+)$")
FILE_NUM_RE = re.compile(r"^(\d+)")

REQUIRED_MARKERS = [
    "## 핵심 인사이트",
    "## Ⅰ.",
    "## Ⅱ.",
    "## Ⅲ.",
    "## Ⅳ.",
    "## Ⅴ.",
    "### 📌 관련 개념 맵",
    "### 👶 어린이를 위한 3줄 비유 설명",
]


@dataclass
class SectionRange:
    index: int
    title: str
    start: int
    end: int
    folder: Path | None


def parse_keyword_list(subject_dir: Path) -> tuple[list[SectionRange], list[int]]:
    keyword_path = subject_dir / "_keyword_list.md"
    lines = keyword_path.read_text(encoding="utf-8").splitlines()

    sections: list[dict] = []
    current: dict | None = None
    numbers: list[int] = []

    for line in lines:
        heading = HEADING_RE.match(line.strip())
        if heading:
            if current:
                sections.append(current)
            current = {
                "index": int(heading.group(1)),
                "title": heading.group(2).strip(),
                "numbers": [],
            }
            continue

        item = KEYWORD_RE.match(line.strip())
        if item:
            num = int(item.group(1))
            numbers.append(num)
            if current:
                current["numbers"].append(num)

    if current:
        sections.append(current)

    section_dirs = sorted(
        [p for p in subject_dir.iterdir() if p.is_dir() and not p.name.startswith(".")],
        key=lambda p: int(p.name.split("_", 1)[0]) if p.name.split("_", 1)[0].isdigit() else 10**9,
    )
    section_dir_map = {
        int(p.name.split("_", 1)[0]): p
        for p in section_dirs
        if p.name.split("_", 1)[0].isdigit()
    }

    ranges: list[SectionRange] = []
    for section in sections:
        section_numbers = section["numbers"]
        if not section_numbers:
            continue
        ranges.append(
            SectionRange(
                index=section["index"],
                title=section["title"],
                start=section_numbers[0],
                end=section_numbers[-1],
                folder=section_dir_map.get(section["index"]),
            )
        )

    return ranges, numbers


def expected_folder(number: int, section_ranges: list[SectionRange]) -> Path | None:
    for section in section_ranges:
        if section.start <= number <= section.end:
            return section.folder
    return None


def audit_subject(subject_dir: Path) -> dict:
    section_ranges, keyword_numbers = parse_keyword_list(subject_dir)
    expected_numbers = set(keyword_numbers)

    actual_files = []
    for path in sorted(subject_dir.rglob("*.md")):
        if path.name in {"_index.md", "_keyword_list.md"}:
            continue
        if "_index.md" in path.parts:
            continue
        match = FILE_NUM_RE.match(path.name)
        if not match:
            continue
        actual_files.append((int(match.group(1)), path))

    actual_numbers = [num for num, _ in actual_files]
    actual_counter = Counter(actual_numbers)

    missing = sorted(expected_numbers - set(actual_numbers))
    unexpected = sorted(set(actual_numbers) - expected_numbers)
    duplicates = {
        str(num): [str(path.relative_to(REPO_ROOT)) for actual_num, path in actual_files if actual_num == num]
        for num, count in actual_counter.items()
        if count > 1
    }

    misplaced = []
    structure_issues = []

    for num, path in actual_files:
        target_dir = expected_folder(num, section_ranges)
        if target_dir and path.parent != target_dir:
            misplaced.append(
                {
                    "number": num,
                    "path": str(path.relative_to(REPO_ROOT)),
                    "expected_dir": str(target_dir.relative_to(REPO_ROOT)),
                }
            )

        text = path.read_text(encoding="utf-8")
        missing_markers = [marker for marker in REQUIRED_MARKERS if marker not in text]
        analogy_count = text.count("📢 섹션 요약 비유")
        if missing_markers or analogy_count < 5:
            structure_issues.append(
                {
                    "number": num,
                    "path": str(path.relative_to(REPO_ROOT)),
                    "missing_markers": missing_markers,
                    "section_analogy_count": analogy_count,
                }
            )

    folder_order = []
    valid_dirs = sorted(
        [p for p in subject_dir.iterdir() if p.is_dir() and p.name.split("_", 1)[0].isdigit()],
        key=lambda p: int(p.name.split("_", 1)[0]),
    )
    for idx, directory in enumerate(valid_dirs, start=1):
        num = int(directory.name.split("_", 1)[0])
        if num != idx:
            folder_order.append(
                {
                    "path": str(directory.relative_to(REPO_ROOT)),
                    "expected_prefix": idx,
                    "actual_prefix": num,
                }
            )

    return {
        "subject": subject_dir.name,
        "keyword_count": len(keyword_numbers),
        "document_count": len(actual_files),
        "missing_numbers": missing,
        "unexpected_numbers": unexpected,
        "duplicate_numbers": duplicates,
        "misplaced_files": misplaced,
        "structure_issues": structure_issues,
        "folder_order_issues": folder_order,
        "section_ranges": [
            {
                "index": section.index,
                "title": section.title,
                "start": section.start,
                "end": section.end,
                "folder": str(section.folder.relative_to(REPO_ROOT)) if section.folder else None,
            }
            for section in section_ranges
        ],
    }


def render_text_report(results: list[dict]) -> str:
    lines = []
    for result in results:
        lines.append(f"[{result['subject']}] keywords={result['keyword_count']} docs={result['document_count']}")
        lines.append(f"  missing: {len(result['missing_numbers'])}")
        if result["missing_numbers"]:
            preview = ", ".join(map(str, result["missing_numbers"][:20]))
            suffix = " ..." if len(result["missing_numbers"]) > 20 else ""
            lines.append(f"    {preview}{suffix}")
        lines.append(f"  duplicates: {len(result['duplicate_numbers'])}")
        lines.append(f"  misplaced: {len(result['misplaced_files'])}")
        lines.append(f"  structure issues: {len(result['structure_issues'])}")
        lines.append(f"  folder order issues: {len(result['folder_order_issues'])}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit studynote structure and guideline compliance.")
    parser.add_argument("subjects", nargs="*", help="Subject directory names such as 1_computer_architecture")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = parser.parse_args()

    subject_dirs = (
        [STUDYNOTE_ROOT / subject for subject in args.subjects]
        if args.subjects
        else sorted([p for p in STUDYNOTE_ROOT.iterdir() if p.is_dir() and p.name[0].isdigit()])
    )

    results = [audit_subject(subject_dir) for subject_dir in subject_dirs]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(render_text_report(results), end="")


if __name__ == "__main__":
    main()
