import os
import re

base_dir = "content/studynote"
fixed_count = 0

for root, _, files in os.walk(base_dir):
    for filename in files:
        if filename.endswith(".md") and not filename.startswith("_"):
            match = re.match(r"^(\d+)_", filename)
            if not match:
                continue
            
            weight_val = int(match.group(1))
            file_path = os.path.join(root, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if not lines or lines[0].strip() != "+++":
                continue
                
            has_weight = False
            weight_line_idx = -1
            
            for i in range(1, len(lines)):
                if lines[i].strip() == "+++":
                    break
                if lines[i].startswith("weight =") or lines[i].startswith("weight="):
                    has_weight = True
                    weight_line_idx = i
            
            needs_fix = False
            if has_weight and weight_line_idx > 0:
                # check if there's any [ section before weight_line_idx
                for i in range(1, weight_line_idx):
                    if lines[i].strip().startswith("["):
                        needs_fix = True
                        break
            
            if needs_fix:
                # Remove the existing weight line
                line_to_move = lines.pop(weight_line_idx)
                # Insert it right after the first +++
                lines.insert(1, f"weight = {weight_val}\n")
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                fixed_count += 1
            elif not has_weight:
                # Insert weight right after +++ if missing
                lines.insert(1, f"weight = {weight_val}\n")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                fixed_count += 1

print(f"Fixed weight position in {fixed_count} files.")