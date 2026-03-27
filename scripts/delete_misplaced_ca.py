import json
import subprocess
from pathlib import Path

data = subprocess.check_output(["python3", "scripts/audit_studynote.py", "1_computer_architecture", "--json"])
parsed = json.loads(data)[0]

misplaced = parsed.get("misplaced_files", [])
for m in misplaced:
    path = Path(m["path"])
    if path.exists():
        print(f"Deleting misplaced file: {path}")
        path.unlink()

print("Deleted misplaced files.")
