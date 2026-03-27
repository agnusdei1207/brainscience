import json
import subprocess

data = subprocess.check_output(["python3", "scripts/audit_studynote.py", "1_computer_architecture", "--json"])
parsed = json.loads(data)[0]

for issue in parsed["structure_issues"]:
    if 123 <= issue['number'] <= 156:
        print(f"Num: {issue['number']}, path: {issue['path']}, missing_markers: {issue['missing_markers']}, analogy_count: {issue['section_analogy_count']}")

