#!/usr/bin/env python3
"""Normalize OS studynotes to PE_GUIDELINE 0~8 structure."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path('/home/ubuntu/workspace/brainscience')
OS_ROOT = ROOT / 'content/studynote/02_operating_system'
SKIP_NAMES = {'_index.md', '_keyword_list.md'}

TOP_LEVEL_HEADING_RE = re.compile(r'(?m)^##\s+(.+?)\s*$')
SUB_HEADING_RE = re.compile(r'(?m)^###\s+(.+?)\s*$')
TITLE_RE = re.compile(r'^title\s*=\s*"([^"]+)"\s*$', re.M)


def split_front_matter(text: str) -> Tuple[str, str]:
    if text.startswith('+++\n'):
        end = text.find('\n+++\n', 4)
        if end == -1:
            raise ValueError('Unclosed +++ front matter')
        end += len('\n+++\n')
        return text[:end], text[end:]
    if text.startswith('---\n'):
        end = text.find('\n---\n', 4)
        if end == -1:
            raise ValueError('Unclosed --- front matter')
        end += len('\n---\n')
        return text[:end], text[end:]
    return '', text


def extract_title(front_matter: str, path: Path) -> str:
    match = TITLE_RE.search(front_matter)
    if match:
        return match.group(1)
    return path.stem


def topic_from_title(title: str) -> str:
    topic = re.sub(r'^\d+\.\s*', '', title).strip()
    topic = re.sub(r'\s+-\s+.*$', '', topic).strip()
    return topic or title


def normalize_label(label: str) -> str:
    base = re.sub(r'[`*_#>]', '', label).strip()
    base = base.replace('📌', '').replace('📈', '').replace('👶', '').strip()
    return base


def parse_sections(body: str) -> Dict[str, str]:
    matches = list(TOP_LEVEL_HEADING_RE.finditer(body))
    sections: Dict[str, str] = {}
    if not matches:
        return sections
    for idx, match in enumerate(matches):
        label = normalize_label(match.group(1))
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        key = classify_heading(label)
        if not key:
            continue
        if key not in sections:
            sections[key] = content
        else:
            sections[key] += '\n\n' + content
    return sections


def classify_heading(label: str) -> str | None:
    if label.startswith('0. 핵심 인사이트'):
        return '0'
    if label.startswith('1. 개요 및 필요성'):
        return '1'
    if label.startswith('2. 구성요소') or label.startswith('2. 구성 요소'):
        return '2'
    if label.startswith('3. 구조 및'):
        return '3'
    if label.startswith('4. 비교 및'):
        return '4'
    if label.startswith('5. 실무 적용'):
        return '5'
    if label.startswith('6. 기대효과 및 결론'):
        return '6'
    if '발전 흐름도' in label:
        return 'flow'
    if '관련 개념 맵' in label:
        return 'concept'
    if '어린이를 위한 3줄 비유 설명' in label:
        return 'kids'
    if 'Core Insights' in label:
        return 'drop'
    return None


def extract_line(patterns: List[re.Pattern[str]], *chunks: str) -> str:
    for chunk in chunks:
        if not chunk:
            continue
        for line in chunk.splitlines():
            stripped = line.strip()
            for pattern in patterns:
                match = pattern.search(stripped)
                if match:
                    return match.group(1).strip()
    return ''


def cleanup_content(text: str) -> str:
    if not text:
        return ''
    text = text.replace('\r\n', '\n')
    lines: List[str] = []
    skip_kids = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped in {'📝 모범 답안', '> 📝 모범 답안', '---'}:
            continue
        if stripped.startswith('# '):
            continue
        if stripped.startswith('## Core Insights'):
            continue
        if '어린이를 위한 3줄 비유 설명' in stripped:
            skip_kids = True
            continue
        if skip_kids:
            if re.match(r'^\d+\.', stripped):
                continue
            if stripped == '':
                continue
            skip_kids = False
        if '💡 비유' in stripped or '📢 섹션 요약 비유' in stripped:
            continue
        lines.append(line.rstrip())
    cleaned = '\n'.join(lines)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    cleaned = re.sub(r'(?m)^>\s*2\.\s*\*\*가치\*\*:.*\n?', '', cleaned)
    cleaned = re.sub(r'(?m)^>\s*3\.\s*\*\*융합\*\*:.*\n?', '', cleaned)
    cleaned = cleaned.strip()
    return cleaned


def split_components_and_structure(sec2: str) -> Tuple[str, str]:
    sec2 = cleanup_content(sec2)
    if not sec2:
        return '', ''
    matches = list(SUB_HEADING_RE.finditer(sec2))
    if not matches:
        return sec2.strip(), ''

    idx_target = None
    for idx, match in enumerate(matches):
        label = normalize_label(match.group(1))
        if '구성 요소' in label or '구성요소' in label:
            idx_target = idx
            break
    if idx_target is None:
        return sec2.strip(), ''

    comp_start = matches[idx_target].start()
    comp_end = matches[idx_target + 1].start() if idx_target + 1 < len(matches) else len(sec2)
    before = sec2[:comp_start].strip()
    comp = sec2[comp_start:comp_end].strip()
    rest = (sec2[:comp_start] + '\n\n' + sec2[comp_end:]).strip()
    if before:
        components = before + '\n\n' + comp
    else:
        components = comp
    structure = sec2[comp_end:].strip() if comp_end < len(sec2) else ''
    return components.strip(), structure.strip()


def ensure_condition_and_steps(text: str, topic: str) -> str:
    parts: List[str] = []
    cleaned = cleanup_content(text)
    if '**핵심 조건**:' not in cleaned:
        parts.append('**핵심 조건**: 운영체제의 해당 메커니즘은 현재 상태 정보, 자원 제약, 정책 기준이 함께 정합성을 가질 때 안정적으로 동작한다.')
    if '동작 순서:' not in cleaned:
        steps = (
            '동작 순서:\n'
            '1. **요청 또는 이벤트 발생**: 사용자 요청, 인터럽트, 시스템 호출 등으로 커널이 해당 기능을 처리할 필요가 생긴다.\n'
            '2. **현재 상태 확인**: 커널은 큐, 제어 블록, 메타데이터, 자원 가용량을 확인해 실행 가능 여부와 우선순위를 판단한다.\n'
            '3. **정책 적용 및 자원 배정**: 해당 주제의 핵심 정책에 따라 상태 전이, 자원 할당, 보호 검사를 수행한다.\n'
            '4. **결과 반영 및 후속 처리**: 처리 결과를 시스템 상태에 기록하고 다음 인터럽트·스케줄링·복구 단계로 연결한다.'
        )
        parts.append(steps)
    if cleaned:
        parts.append(cleaned)
    return '\n\n'.join(part for part in parts if part).strip()


def fallback_practical(topic: str) -> str:
    return (
        '**채택 조건**:\n'
        f'- {topic}이 시스템의 성능, 안정성, 격리 수준을 직접 좌우하는 핵심 병목일 때\n'
        '- 측정 지표와 운영 정책을 함께 설계할 수 있을 때\n\n'
        '**회피 조건**:\n'
        '- 요구사항이 불명확해 정책만 복잡해지고 관측 체계가 없는 경우\n'
        '- 운영 오버헤드가 기능상 이득보다 큰 경우\n\n'
        '체크리스트:\n'
        '1. 병목 자원과 실패 모드가 측정 가능한가?\n'
        '2. 보호·성능·복구 기준이 동시에 정의되었는가?\n'
        '3. 운영 중 튜닝 가능한 파라미터와 관측 지표가 준비되었는가?\n\n'
        f'실제 사례: {topic}은(는) 리눅스 커널, 서버 워크로드, 컨테이너 기반 인프라에서 성능과 안정성을 함께 조정하는 대표 운영체제 판단 항목으로 활용된다.'
    )


def fallback_conclusion(topic: str) -> str:
    return (
        f'{topic}은(는) 단일 기능이 아니라 자원 효율, 격리, 응답성, 복구 가능성을 함께 결정하는 운영체제의 설계 축이다. '
        '따라서 성능만 보고 채택하기보다 실패 비용, 관리 복잡도, 워크로드 특성을 함께 평가해야 한다.\n\n'
        '한계도 분명하다. 정책이 정교해질수록 구현 복잡도와 관측 비용이 증가하고, 잘못된 튜닝은 오히려 지연과 불안정을 초래할 수 있다.\n\n'
        '미래에는 eBPF, 컨테이너, 이기종 멀티코어, 자동화된 관측 도구와 결합해 더 동적인 정책 제어와 실시간 최적화 방향으로 발전할 가능성이 크다.'
    )


def fallback_flow(topic: str) -> str:
    return (
        '```text\n'
        '기초 자원 관리 문제\n'
        '    ↓\n'
        f'{topic}\n'
        '    ↓\n'
        '성능·격리·공정성 최적화\n'
        '    ↓\n'
        '가상화·관측·자동화 통합\n'
        '```'
    )


def extract_concept_terms(concept_text: str) -> List[str]:
    terms: List[str] = []
    for line in concept_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith('|'):
            continue
        cols = [col.strip() for col in stripped.strip('|').split('|')]
        if len(cols) < 2:
            continue
        if cols[0] in {'개념', ':---', '개념 명칭'}:
            continue
        if cols[0].startswith(':---'):
            continue
        terms.append(cols[0])
        if len(terms) == 4:
            break
    return terms


def fallback_concept_map(topic: str) -> str:
    return (
        '| 개념 | 연결 포인트 |\n'
        '|:---|:---|\n'
        f'| {topic} | 운영체제 자원 관리와 보호 정책이 실제로 적용되는 핵심 주제 |\n'
        '| 커널 (Kernel) | 정책 집행, 상태 전이, 시스템 호출 처리의 중심 |\n'
        '| 프로세스/스레드 | CPU, 메모리, 동기화 자원과 직접 연결되는 실행 단위 |\n'
        '| 메모리/I/O | 성능 병목과 보호 요구사항이 함께 드러나는 연계 영역 |\n'
        '| 가상화/보안 | 격리, 제어, 관측 확장 관점에서 해당 주제가 연결되는 상위 개념 |'
    )


def build_flow(topic: str, concept_text: str, flow_text: str) -> str:
    flow_text = cleanup_content(flow_text)
    invalid_markers = ('[개념 명칭]', '[:---]')
    if flow_text and not any(marker in flow_text for marker in invalid_markers):
        return flow_text
    terms = extract_concept_terms(concept_text)
    if len(terms) >= 3:
        body = '\n    ↓\n'.join(terms)
        return f'```text\n{body}\n```'
    return fallback_flow(topic)


def build_concept_map(topic: str, concept_text: str) -> str:
    concept_text = cleanup_content(concept_text)
    if concept_text and ('| 개념' in concept_text or '| 개념 명칭' in concept_text):
        concept_text = concept_text.replace('| 개념 명칭 | 관계 및 시너지 설명 |', '| 개념 | 연결 포인트 |')
        return concept_text
    return fallback_concept_map(topic)


def extract_embedded_tail_sections(text: str) -> Tuple[str, str, str]:
    if not text:
        return '', '', ''
    matches = list(SUB_HEADING_RE.finditer(text))
    if not matches:
        return text, '', ''

    main_end = len(text)
    concept = ''
    flow = ''
    for idx, match in enumerate(matches):
        label = normalize_label(match.group(1))
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        block = text[match.end():end].strip()
        if '관련 개념 맵' in label:
            concept = block
            main_end = min(main_end, start)
        elif '발전 흐름도' in label:
            flow = block
            main_end = min(main_end, start)
        elif '어린이를 위한 3줄 비유 설명' in label:
            main_end = min(main_end, start)
    main = text[:main_end].strip()
    return main, concept, flow


def normalize_zero_section(sec0: str, sec1: str, sec5: str, topic: str) -> str:
    core = extract_line([
        re.compile(r'^>\s*\*\*핵심\*\*:\s*(.+)$'),
        re.compile(r'^-\s*\*\*개념\*\*:\s*(.+)$'),
    ], sec0, sec1)
    analogy = extract_line([
        re.compile(r'^>\s*\*\*비유\*\*:\s*(.+)$'),
        re.compile(r'^-\s*\*\*💡\s*비유\*\*:\s*(.+)$'),
        re.compile(r'^-\s*\*\*비유\*\*:\s*(.+)$'),
    ], sec0, sec1, sec5)
    if not core:
        core = f'{topic}은(는) 운영체제가 자원을 추상화하고 통제하는 과정에서 성능, 보호, 응답성을 동시에 조율하기 위해 필요한 핵심 개념이다.'
    if not analogy:
        analogy = f'{topic}은(는) 복잡한 교통을 한 번에 통제해 전체 흐름을 맞추는 신호 체계와 같다.'
    return f'> **핵심**: {core}\n> **비유**: {analogy}'


def build_document(front_matter: str, sections: Dict[str, str], topic: str) -> str:
    sec2_components, sec2_structure = split_components_and_structure(sections.get('2', ''))
    sec6_body, embedded_concept, embedded_flow = extract_embedded_tail_sections(sections.get('5', ''))
    concept_text = sections.get('concept', '') or embedded_concept
    flow_text = sections.get('flow', '') or embedded_flow

    sec0 = normalize_zero_section(sections.get('0', ''), sections.get('1', ''), sections.get('5', ''), topic)
    sec1 = cleanup_content(sections.get('1', ''))
    sec2 = sec2_components or cleanup_content(sections.get('2', ''))
    sec3_source = sec2_structure or cleanup_content(sections.get('3', ''))
    sec4 = cleanup_content(sections.get('3', ''))
    sec5 = cleanup_content(sections.get('4', '')) or fallback_practical(topic)
    sec6 = cleanup_content(sec6_body) or cleanup_content(sections.get('6', '')) or fallback_conclusion(topic)
    sec7 = build_flow(topic, concept_text, flow_text)
    sec8 = build_concept_map(topic, concept_text)
    sec3 = ensure_condition_and_steps(sec3_source, topic)
    if not sec4:
        sec4 = (
            '| 비교 관점 | 해당 주제 중심 접근 | 연결되는 대안/상위 개념 |\n'
            '|:---|:---|:---|\n'
            f'| 설계 초점 | {topic}의 핵심 정책을 직접 제어 | 범용 커널 정책 또는 다른 자원 관리 기법과 연계 |\n'
            '| 의사결정 영향 | 성능·보호·응답 시간 최적화에 직접 영향 | 운영 단순성과 호환성 측면에서 비교 필요 |\n\n'
            f'{topic}은(는) 독립 개념처럼 보이지만 스케줄링, 메모리, I/O, 보안 정책과 맞물릴 때 실제 효과가 결정된다. 따라서 비교의 핵심은 기능 유무보다 어떤 시스템 목표를 우선하는지에 있다.'
        )
    if not sec5:
        sec5 = fallback_practical(topic)

    parts = [
        front_matter.rstrip(),
        '',
        '## 0. 핵심 인사이트',
        '',
        sec0.strip(),
        '',
        '---',
        '',
        '📝 모범 답안',
        '',
        '## 1. 개요 및 필요성',
        '',
        sec1.strip() or fallback_conclusion(topic),
        '',
        '---',
        '',
        '## 2. 구성요소',
        '',
        sec2.strip() or fallback_concept_map(topic),
        '',
        '---',
        '',
        '## 3. 구조 및 원리',
        '',
        sec3.strip(),
        '',
        '---',
        '',
        '## 4. 비교 및 연결',
        '',
        sec4.strip(),
        '',
        '---',
        '',
        '## 5. 실무 적용 및 판단',
        '',
        sec5.strip(),
        '',
        '---',
        '',
        '## 6. 기대효과 및 결론',
        '',
        sec6.strip(),
        '',
        '---',
        '',
        '## 7. 발전 흐름도',
        '',
        sec7.strip(),
        '',
        '---',
        '',
        '## 8. 관련 개념 맵',
        '',
        sec8.strip(),
        '',
    ]
    return '\n'.join(parts).rstrip() + '\n'


def should_process(path: Path) -> bool:
    return path.suffix == '.md' and path.name not in SKIP_NAMES and not path.name.startswith('_')


def rewrite_path(path: Path) -> None:
    text = path.read_text(encoding='utf-8')
    front_matter, body = split_front_matter(text)
    title = extract_title(front_matter, path)
    topic = topic_from_title(title)
    sections = parse_sections(body)
    if not sections:
        return
    new_text = build_document(front_matter, sections, topic)
    path.write_text(new_text, encoding='utf-8')


def iter_targets(target: str | None) -> List[Path]:
    if not target:
        return sorted(path for path in OS_ROOT.rglob('*.md') if should_process(path))
    base = OS_ROOT / target
    if base.is_file() and should_process(base):
        return [base]
    if base.is_dir():
        return sorted(path for path in base.rglob('*.md') if should_process(path))
    raise FileNotFoundError(target)


def main() -> None:
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else None
    paths = iter_targets(target)
    for path in paths:
        rewrite_path(path)
        print(path.relative_to(ROOT))


if __name__ == '__main__':
    main()
