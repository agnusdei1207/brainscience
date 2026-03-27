import re
from pathlib import Path

for md_file in Path('content/studynote/1_computer_architecture').rglob('*.md'):
    content = md_file.read_text(encoding='utf-8')
    new_content = content
    new_content = re.sub(r'^## 📌 관련 개념 맵', '### 📌 관련 개념 맵', new_content, flags=re.MULTILINE)
    new_content = re.sub(r'^## 👶 어린이를 위한 3줄 비유 설명', '### 👶 어린이를 위한 3줄 비유 설명', new_content, flags=re.MULTILINE)
    if content != new_content:
        md_file.write_text(new_content, encoding='utf-8')
        print(f"Fixed {md_file}")
