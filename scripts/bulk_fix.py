#!/usr/bin/env python3
import json
import os
import urllib.request
import urllib.error
import time
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
BASE_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://api.z.ai/api/anthropic")
MODEL = os.environ.get("ANTHROPIC_DEFAULT_HAIKU_MODEL", "glm-4.7")

PROMPT_TEMPLATE = """You are an expert technical writer and IT systems architect.
Please rewrite the following study note to strictly comply with the PE (Professional Engineer) guideline format.

[PE GUIDELINE]
{guideline}

[ORIGINAL CONTENT]
{content}

[REQUIREMENTS]
1. Do not output anything except the Markdown content. Start with `---` (front matter) and end with the `### 👶 어린이를 위한 3줄 비유 설명`.
2. Expand the content significantly to match the high-quality Professional Engineer (PE) depth.
3. Ensure every section (Ⅰ~Ⅴ) has an ASCII diagram or table, deep explanations, and ends with `📢 섹션 요약 비유:`.
4. Include abbreviations with their full names.
5. Retain the exact same front matter (title, weight, etc.) at the top.
6. The title MUST be preserved.
"""

def call_llm(content: str, guideline: str) -> str:
    if not API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    prompt = PROMPT_TEMPLATE.format(guideline=guideline, content=content)
    
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    data = {
        "model": MODEL,
        "max_tokens": 4096,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    req = urllib.request.Request(
        f"{BASE_URL}/v1/messages",
        headers=headers,
        data=json.dumps(data).encode("utf-8"),
        method="POST"
    )
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                resp_data = json.loads(response.read().decode("utf-8"))
                return resp_data['content'][0]['text']
        except Exception as e:
            print(f"API Error (attempt {attempt+1}): {e}")
            time.append(2)
            
    raise RuntimeError("Failed to get response from LLM after 3 attempts.")

def process_file(file_path: str, guideline: str) -> bool:
    try:
        path = Path(file_path)
        original_content = path.read_text(encoding="utf-8")
        
        # Don't re-process if it looks good enough already (has Ⅰ. and Ⅴ.)
        if "## Ⅰ." in original_content and "## Ⅴ." in original_content and "📢 섹션 요약 비유" in original_content:
            return True
            
        print(f"Processing: {file_path}")
        new_content = call_llm(original_content, guideline)
        
        # Strip code blocks if the LLM wrapped the whole response
        if new_content.startswith("```markdown\n"):
            new_content = new_content[12:-3]
        elif new_content.startswith("```\n"):
            new_content = new_content[4:-3]
            
        path.write_text(new_content, encoding="utf-8")
        print(f"Done: {file_path}")
        return True
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-input", required=True, help="JSON file containing the list of files to process")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of files to process")
    parser.add_argument("--workers", type=int, default=5, help="Number of concurrent workers")
    args = parser.parse_args()

    guideline = Path("PE_GUIDELINE.md").read_text(encoding="utf-8")
    
    with open(args.json_input, "r") as f:
        data = json.load(f)
        
    paths = []
    for subject_data in data:
        for issue in subject_data.get("structure_issues", []):
            if "path" in issue and "_old" not in issue["path"]:
                paths.append(issue["path"])
                
    paths = paths[:args.limit]
    
    print(f"Found {len(paths)} files to process.")
    
    success_count = 0
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(process_file, path, guideline): path for path in paths}
        for future in as_completed(futures):
            if future.result():
                success_count += 1
                
    print(f"Finished processing. Success: {success_count}/{len(paths)}")

if __name__ == "__main__":
    main()
