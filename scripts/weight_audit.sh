#!/bin/bash
# Check weight mismatches — only real numeric differences
BASE="/home/ubuntu/workspace/brainscience/content/gisulsa"

echo "=== REAL WEIGHT MISMATCHES ==="
find "$BASE" -name '*.md' ! -name '_index.md' ! -name 'exam_analysis.md' | sort | while read f; do
    w=$(grep -m1 '^weight' "$f" 2>/dev/null | sed 's/weight *= *//')
    bn=$(basename "$f" .md)
    num=$(echo "$bn" | grep -oP '^\d+')
    rel=$(echo "$f" | sed "s|${BASE}/||")
    
    # Remove leading zeros for comparison
    w_num=$((10#${w:-0}))
    f_num=$((10#${num:-0}))
    
    if [ -z "$w" ]; then
        echo "NO_WEIGHT $rel"
    elif [ "$w_num" -ne "$f_num" ]; then
        echo "FIX $rel  weight=$w_num should=$f_num"
    fi
done
echo "Done."
