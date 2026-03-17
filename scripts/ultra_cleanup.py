import os
import glob
import re

def cleanup(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove all markdown links
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', content)

    # 2. Fix front matter
    content = content.strip()
    
    # Identify if it starts with --- or +++
    # If it starts with anything else, find the first occurrence of --- or +++
    match = re.search(r'^(\+\+\+|---)', content, re.MULTILINE)
    if match:
        start_pos = match.start()
        delim = match.group(1)
        content = content[start_pos:]
        
        # Split by the same delimiter
        parts = content.split(delim, 2)
        if len(parts) >= 3:
            fm = parts[1].strip()
            body = parts[2].strip()
            
            # Clean up the front matter lines
            lines = fm.split('\n')
            new_fm_lines = []
            for line in lines:
                line = line.strip()
                if not line: continue
                # if it looks like key: value, change to key = value
                if ':' in line and '=' not in line and not line.startswith('['):
                    line = re.sub(r'^([a-zA-Z0-9_]+)\s*:\s*(.*)$', r'\1 = \2', line)
                new_fm_lines.append(line)
            
            # Force +++ for all
            new_content = '+++\n' + '\n'.join(new_fm_lines) + '\n+++\n\n' + body
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    if '_index.md' in filepath: continue
    cleanup(filepath)
