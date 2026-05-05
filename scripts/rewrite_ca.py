#!/usr/bin/env python3
"""
Batch rewrite all Subject 01 (Computer Architecture) files to PE_GUIDELINE standard.
Uses parallel processing for maximum throughput.
"""

import os
import re
import sys
import json
import subprocess
import concurrent.futures
from pathlib import Path
from datetime import date

BASE = Path("/home/ubuntu/workspace/brainscience/content/studynote/01_computer_architecture")
TODAY = date.today().isoformat()

# --- Keyword metadata extracted from _keyword_list.md ---
# Section mapping: keyword number -> directory
SECTION_MAP = {
    (1, 72): "01_basic_electronics_logic",
    (73, 122): "02_data_representation_arithmetic",
    (123, 156): "03_architecture_basics_performance",
    (157, 203): "04_instruction_set_architecture",
    (204, 244): "05_control_unit_pipelining",
    (245, 281): "06_memory_hierarchy_cache",
    (282, 308): "07_virtual_memory_os_integration",
    (309, 343): "08_io_storage_systems",
    (344, 367): "09_system_bus_interconnects",
    (368, 392): "10_parallel_processing_architecture",
    (393, 416): "11_multicore_synchronization",
    (417, 448): "12_accelerators_ai_hardware",
    (449, 474): "13_reliability_power_management",
    (475, 499): "14_hardware_security_trends",
    (500, 802): "15_advanced_topics",
}

def get_section(num):
    for (lo, hi), sec in SECTION_MAP.items():
        if lo <= num <= hi:
            return sec
    return "15_advanced_topics"

def extract_frontmatter(filepath):
    """Extract weight and title from existing file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        weight_match = re.search(r'weight\s*=\s*(\d+)', content)
        title_match = re.search(r'title\s*=\s*"([^"]+)"', content)
        
        weight = int(weight_match.group(1)) if weight_match else None
        title = title_match.group(1) if title_match else None
        
        return weight, title, content
    except:
        return None, None, None

def check_quality(content):
    """Check if file already meets PE_GUIDELINE standard."""
    if not content:
        return False
    
    required = [
        "## 0. 핵심 인사이트",
        "📝 모범 답안",
        "## 1. 개요 및 필요성",
        "## 2. 구성요소",
        "## 3. 구조 및 원리",
        "## 4. 비교 및 연결",
        "## 5. 실무 적용 및 판단",
        "## 6. 기대효과 및 결론",
        "## 7. 관련 개념 맵 및 발전 흐름도",
    ]
    
    banned = [
        "어린이를 위한",
        "📢 섹션 요약 비유",
        "## 4. 비교 및 트레이드오프",
        "## 5. 실무 적용 및 최적화 기법",
    ]
    
    has_all_required = all(r in content for r in required)
    has_no_banned = not any(b in content for b in banned)
    is_long_enough = len(content) > 5000  # PE_EXAMPLE gold standard is ~12K
    
    return has_all_required and has_no_banned and is_long_enough

def collect_files():
    """Collect all .md files that need rewriting."""
    files_to_process = []
    
    for dirpath, dirnames, filenames in os.walk(BASE):
        for fname in filenames:
            if fname.endswith('.md') and fname != '_index.md' and fname != '_keyword_list.md':
                filepath = os.path.join(dirpath, fname)
                weight, title, content = extract_frontmatter(filepath)
                
                if weight is None or title is None:
                    print(f"SKIP (no metadata): {filepath}")
                    continue
                
                if check_quality(content):
                    # Already meets standard
                    continue
                
                files_to_process.append({
                    "path": filepath,
                    "weight": weight,
                    "title": title,
                    "filename": fname,
                })
    
    return sorted(files_to_process, key=lambda x: x["weight"])

def main():
    files = collect_files()
    print(f"Total files needing rewrite: {len(files)}")
    
    # Output the list for batch processing
    with open("/tmp/ca_rewrite_list.json", "w", encoding="utf-8") as f:
        json.dump(files, f, ensure_ascii=False, indent=2)
    
    print(f"File list saved to /tmp/ca_rewrite_list.json")
    
    # Print summary
    sections = {}
    for f in files:
        sec = get_section(f["weight"])
        sections[sec] = sections.get(sec, 0) + 1
    
    print("\n=== Files to rewrite per section ===")
    for sec in sorted(sections.keys()):
        print(f"  {sec}: {sections[sec]} files")

if __name__ == "__main__":
    main()
