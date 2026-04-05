import json
import os
import shutil

with open('audit_results_9_security.json', 'r') as f:
    results = json.load(f)

# Assuming audit_results_9_security.json contains a list, wait, we used `jq '.[]'` to output.
# The `jq` output was just the object.
# Let me re-read the json properly.
