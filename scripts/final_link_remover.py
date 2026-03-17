import os
import glob
import re

def remove_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    # Simple non-greedy match for markdown links
    pattern = r'\[(.*?)\]\((.*?)\)'
    while re.search(pattern, new_content):
        new_content = re.sub(pattern, r'\1', new_content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

for filepath in glob.glob('content/**/*.md', recursive=True):
    remove_links(filepath)
