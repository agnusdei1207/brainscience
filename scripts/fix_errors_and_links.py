import os
import glob
import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove markdown links: [text](link) -> text
    # Non-greedy match for [] and ()
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', content)

    # 2. Fix front matter delimiters if content is TOML (has =)
    # Zola: --- is YAML, +++ is TOML.
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            if '=' in fm and ':' not in fm:
                # Delimiter mismatch: TOML content but YAML delimiter
                content = '+++' + fm + '+++' + parts[2]
            elif '[extra]' in fm:
                # Extra section is usually TOML
                content = '+++' + fm + '+++' + parts[2]

    # Save changes
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

# Target all markdown files in content/
for filepath in glob.glob('content/**/*.md', recursive=True):
    if '_index.md' in filepath: continue
    process_file(filepath)
