#!/bin/bash
# Final comprehensive audit for gisulsa keyword files
BASE="/home/ubuntu/workspace/brainscience/content/gisulsa"

echo "=== 전수조사 최종 결과 ==="
total_idx=0
total_act=0

for d in $(ls -d ${BASE}/*/); do
    name=$(basename "$d")
    idx="${d}/_index.md"
    
    # Get referenced files from _index.md (improved regex to handle numbers in names)
    refs=$(grep -oP '\([0-9]+_[a-z0-9_]+\.md\)' "$idx" 2>/dev/null | tr -d '()' | sort -u)
    
    # Get actual files
    actual=$(find "$d" -maxdepth 1 -name '*.md' ! -name '_index.md' -printf '%f\n' | sort)
    
    ic=$(echo "$refs" | grep -c . 2>/dev/null)
    ac=$(echo "$actual" | grep -c . 2>/dev/null)
    total_idx=$((total_idx + ic))
    total_act=$((total_act + ac))
    
    # Find missing (referenced but not exists)
    miss=""
    for f in $refs; do
        if ! echo "$actual" | grep -qx "$f"; then
            miss="$miss $f"
        fi
    done
    
    # Find extra (exists but not referenced)
    extra=""
    for f in $actual; do
        if ! echo "$refs" | grep -qx "$f"; then
            extra="$extra $f"
        fi
    done
    
    if [ -z "$miss" ] && [ -z "$extra" ]; then
        printf "OK  %-35s idx=%2d act=%2d\n" "$name" "$ic" "$ac"
    else
        printf "ERR %-35s idx=%2d act=%2d\n" "$name" "$ic" "$ac"
        [ -n "$miss" ] && echo "   MISS:$miss"
        [ -n "$extra" ] && echo "   EXTRA:$extra"
    fi
done

echo ""
echo "TOTAL: index_refs=$total_idx actual_files=$total_act"
echo ""

echo "=== DUPLICATE FILENAMES ACROSS SUBJECTS ==="
dups=$(find "$BASE" -name '*.md' ! -name '_index.md' -printf '%f\n' | sort | uniq -d)
if [ -z "$dups" ]; then
    echo "No duplicates found."
else
    echo "$dups" | while read dup; do
        echo "  DUP: $dup found in:"
        find "$BASE" -name "$dup" ! -name '_index.md' -printf "    %P\n"
    done
fi
echo "Done."
