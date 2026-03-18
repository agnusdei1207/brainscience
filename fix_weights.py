import os
import glob
import re

directory = "content/studynote/1_computer_architecture"
count = 0

for filepath in glob.glob(f"{directory}/**/*.md", recursive=True):
    if "_index.md" in filepath or "_keyword_list.md" in filepath:
        continue
        
    filename = os.path.basename(filepath)
    match = re.match(r"^(\d+)_", filename)
    if match:
        weight = match.group(1)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        if "weight =" not in content and content.startswith("+++"):
            new_content = content.replace("+++", f"+++\nweight = {weight}", 1)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            count += 1

print(f"Updated {count} files.")
