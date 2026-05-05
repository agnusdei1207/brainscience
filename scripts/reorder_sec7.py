#!/usr/bin/env python3
"""Reorder section 7: 발전 흐름도 먼저, 관련 개념 맵 마지막."""
import re
import os

files = [
    '/home/ubuntu/workspace/brainscience/content/studynote/01_computer_architecture/01_basic_electronics_logic/002_current.md',
    '/home/ubuntu/workspace/brainscience/content/studynote/01_computer_architecture/01_basic_electronics_logic/003_resistance.md',
    '/home/ubuntu/workspace/brainscience/content/studynote/01_computer_architecture/01_basic_electronics_logic/004_impedance.md',
    '/home/ubuntu/workspace/brainscience/content/studynote/01_computer_architecture/01_basic_electronics_logic/005_capacitor.md',
    '/home/ubuntu/workspace/brainscience/content/studynote/01_computer_architecture/01_basic_electronics_logic/006_capacitance.md',
    '/home/ubuntu/workspace/brainscience/content/studynote/01_computer_architecture/01_basic_electronics_logic/007_inductor.md',
    '/home/ubuntu/workspace/brainscience/content/studynote/01_computer_architecture/01_basic_electronics_logic/008_conductor.md',
    '/home/ubuntu/workspace/brainscience/content/studynote/01_computer_architecture/01_basic_electronics_logic/009_semiconductor.md',
]

OLD_HEADING = '## 7. 관련 개념 맵 및 발전 흐름도'
NEW_HEADING = '## 7. 발전 흐름도 및 관련 개념 맵'

for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    idx = content.find(OLD_HEADING)
    if idx == -1:
        print(f'SKIP (already updated or not found): {os.path.basename(fp)}')
        continue

    before = content[:idx]
    section7 = content[idx:]

    # Extract table block (| ... |)
    table_match = re.search(r'(\| 개념 \| 연결 포인트 \|.*?)(?=\n```)', section7, re.DOTALL)
    # Extract code block
    code_match = re.search(r'(```\n[\s\S]+?```)', section7)

    if not table_match or not code_match:
        print(f'PATTERN NOT MATCHED: {os.path.basename(fp)}')
        continue

    table = table_match.group(1).strip()
    code = code_match.group(1).strip()

    new_section7 = f'{NEW_HEADING}\n\n{code}\n\n{table}\n'
    new_content = before + new_section7

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f'OK: {os.path.basename(fp)}')

print('Done.')
