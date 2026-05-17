#!/bin/bash
# Final audit script for gisulsa keyword files
BASE="/home/ubuntu/workspace/brainscience/content/gisulsa"

for d in 01_computer_architecture 02_operating_system 03_network 04_software_engineering \
         05_database 06_ict_convergence 07_enterprise 08_algorithm 09_security 10_ai \
         11_design 12_it_management 13_cloud 14_data_engineering 15_devops 16_bigdata; do
    idx="${BASE}/${d}/_index.md"
    
    # Get referenced files from _index.md
    refs=$(grep -oP '\(\d+_[a-z_]+\.md\)' "$idx" 2>/dev/null | tr -d '()' | sort -u)
    
    # Get actual files
    actual=$(find "${BASE}/${d}" -name '*.md' ! -name '_index.md' -printf '%f\n' | sort)
    
    idx_count=$(echo "$refs" | grep -c .)
    act_count=$(echo "$actual" | grep -c .)
    
    # Find missing (referenced but not exists)
    missing=""
    for f in $refs; do
        if ! echo "$actual" | grep -qx "$f"; then
            missing="$missing $f"
        fi
    done
    
    # Find extra (exists but not referenced)
    extra=""
    for f in $actual; do
        if ! echo "$refs" | grep -qx "$f"; then
            extra="$extra $f"
        fi
    done
    
    echo "=== ${d}: index_refs=${idx_count} actual_files=${act_count}"
    if [ -n "$missing" ]; then
        echo "  MISSING (in index but no file):$missing"
    fi
    if [ -n "$extra" ]; then
        echo "  EXTRA (file exists, not in index):$extra"
    fi
    if [ -z "$missing" ] && [ -z "$extra" ]; then
        echo "  ✅ PERFECT MATCH"
    fi
done

# Check for duplicate filenames across all subjects
echo ""
echo "=== DUPLICATE CHECK ==="
find "$BASE" -name '*.md' ! -name '_index.md' -printf '%f\n' | sort | uniq -d | while read dup; do
    echo "  DUP: $dup found in:"
    find "$BASE" -name "$dup" ! -name '_index.md' -printf "    %P\n"
done
echo "Done."
