import os
import glob
import re

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Strip leading/trailing whitespaces
    content = content.strip()
    
    # 2. Find the first occurrence of +++ or ---
    # We want to find the real front matter content
    # Look for title = "..." or title: "..."
    
    # Let's try to extract anything between the first and second delimiters
    # but be careful about nested ones.
    
    # Actually, a better way:
    # Remove any combination of --- and +++ at the very start
    while content.startswith('---') or content.startswith('+++'):
        content = re.sub(r'^(\+\+\+|---)\s*', '', content)
    
    # Now the content should start with the actual fields.
    # Find where the front matter ends (the first +++ or ---)
    end_match = re.search(r'\n(\+\+\+|---)', content)
    if end_match:
        fm = content[:end_match.start()].strip()
        body = content[end_match.end():].strip()
        
        # Clean up fm: remove any internal +++ or --- lines
        fm_lines = [line.strip() for line in fm.split('\n') if line.strip() not in ['---', '+++', '```', '```markdown']]
        
        # Standardize fm lines to TOML (key = value)
        new_fm_lines = []
        for line in fm_lines:
            if not line: continue
            if ':' in line and '=' not in line and not line.startswith('['):
                line = re.sub(r'^([a-zA-Z0-9_]+)\s*:\s*(.*)$', r'\1 = \2', line)
            new_fm_lines.append(line)
            
        new_content = '+++\n' + '\n'.join(new_fm_lines) + '\n+++\n\n' + body
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    if '_index.md' in filepath: continue
    fix_file(filepath)
