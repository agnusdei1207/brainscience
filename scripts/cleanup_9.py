import json
import os
import shutil
from pathlib import Path

with open('audit_results_9_security.json', 'r') as f:
    results = json.load(f)[0]

misplaced = results.get('misplaced_files', [])
duplicates = results.get('duplicate_numbers', {})

expected_dirs = {}
for m in misplaced:
    expected_dirs[str(m['number'])] = m['expected_dir']

# Determine which duplicates to keep
for num_str, paths in duplicates.items():
    # check which path is in the expected_dir
    expected_dir = expected_dirs.get(num_str)
    if not expected_dir:
        # If not misplaced, assume the first one is the one we want to keep?
        # Let's find out expected_dir from keyword_list
        pass
    
    kept = False
    for path in paths:
        if expected_dir and path.startswith(expected_dir):
            kept = True
            break
            
    # if none are in expected dir, we'll keep the first one and move it later
    if not kept:
        target_to_keep = paths[0]
    else:
        target_to_keep = [p for p in paths if expected_dir and p.startswith(expected_dir)][0]
        
    for path in paths:
        if path != target_to_keep and os.path.exists(path):
            print(f"Removing duplicate: {path}")
            os.remove(path)

# Refresh misplaced after deleting duplicates
# If the remaining file is misplaced, move it
for m in misplaced:
    path = m['path']
    if os.path.exists(path):
        filename = os.path.basename(path)
        expected_dir = m['expected_dir']
        new_path = os.path.join(expected_dir, filename)
        
        if not os.path.exists(expected_dir):
            os.makedirs(expected_dir, exist_ok=True)
            
        if path != new_path:
            # check if destination already exists
            if not os.path.exists(new_path):
                print(f"Moving {path} to {new_path}")
                shutil.move(path, new_path)
            else:
                print(f"Could not move {path}, destination exists: {new_path}")
                os.remove(path)
