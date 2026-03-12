import os
import re

def get_existing_numbers(dir_path):
    numbers = set()
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".md") and not file.startswith("_"):
                match = re.match(r"^(\d+)_", file)
                if match:
                    numbers.add(int(match.group(1)))
    return numbers

def get_expected_numbers(keyword_file):
    numbers = set()
    with open(keyword_file, 'r', encoding='utf-8') as f:
        content = f.read()
        matches = re.findall(r"^(\d+)\.\s+", content, re.MULTILINE)
        for match in matches:
            numbers.add(int(match))
    return numbers

if __name__ == "__main__":
    dir_path = "content/studynote/1_computer_architecture/"
    keyword_file = os.path.join(dir_path, "_keyword_list.md")
    
    existing = get_existing_numbers(dir_path)
    expected = get_expected_numbers(keyword_file)
    
    # 1~802 (or max expected)
    max_num = max(expected) if expected else 802
    
    missing = []
    for i in range(1, max_num + 1):
        if i in expected and i not in existing:
            missing.append(i)
            
    print(f"Total Expected: {len(expected)}")
    print(f"Total Existing: {len(existing)}")
    print(f"Total Missing: {len(missing)}")
    print(f"Missing Numbers: {missing}")
