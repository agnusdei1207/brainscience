#!/bin/bash
# Robust batch converter: old template → 답안 format
BASE="/home/ubuntu/workspace/brainscience/content/gisulsa"
TMPF="/tmp/gisulsa_convert_tmp.md"

converted=0
skipped=0
errors=0

find "$BASE" -name '*.md' ! -name '_index.md' ! -name 'exam_analysis.md' | sort | while read f; do
    # Skip already converted files
    if grep -q "^## 답안\." "$f" 2>/dev/null; then
        skipped=$((skipped+1))
        continue
    fi

    # Extract front matter fields
    weight=$(grep -m1 '^weight' "$f" | sed 's/weight *= *//')
    title=$(grep -m1 '^title' "$f" | sed 's/title *= *"//;s/".*$//')
    date_val=$(grep -m1 '^date' "$f" | sed 's/date *= *"//;s/".*$//')
    cats=$(grep -m1 '^categories' "$f" | sed 's/categories *= *"//;s/".*$//')
    [ -z "$date_val" ] && date_val="2026-05-18"
    [ -z "$cats" ] && cats="gisulsa"

    # Get main heading text (first # after front matter)
    main_heading=$(awk 'BEGIN{c=0} /^[+][+][+]$/{c++;next} c>=2 && /^# /{sub(/^# /,"");print;exit}' "$f")
    [ -z "$main_heading" ] && main_heading="$title"
    # Remove emoji from heading
    main_heading=$(echo "$main_heading" | sed 's/🎯 *//;s/핵심 키워드: *//')

    # Extract frequency/difficulty line
    freq_line=$(grep -m1 '출제 빈도\|별점\|출제빈도' "$f" | sed 's/^> *//;s/\*//g')
    [ -z "$freq_line" ] && freq_line="기본"

    # Extract definition section (## 1. 정의 content)
    definition=$(awk '/^## 1\. 정의/{found=1;next} /^## [0-9]+\./{if(found)exit} found{print}' "$f" | sed '/^$/d' | head -8)
    
    # If no definition section, try to get first substantial paragraph after heading
    if [ -z "$definition" ]; then
        definition=$(awk 'BEGIN{c=0;s=0} /^[+][+][+]$/{c++;next} c>=2{if(/^# /){s=1;next} if(s && /^[^>#|![]/ && length>20){print;found++; if(found>=3)exit}}' "$f")
    fi
    [ -z "$definition" ] && definition="(정의 작성 필요)"

    # Extract comparison table
    comp_table=$(awk '/^## [0-9]+\. 핵심 비교표/,/^## [0-9]+\./' "$f" | grep -E '^\|' | head -10)

    # Extract any code blocks (for ASCII diagrams)
    code_blocks=$(awk '/^```/{if(in_code){in_code=0;print "```";next}else{in_code=1;print;next}} in_code{print}' "$f" | head -30)

    # Build new file
    cat > "$TMPF" << 'HEADER'
+++
HEADER

    cat >> "$TMPF" << EOF
weight = $weight
title = "$title"
date = "$date_val"
[extra]
categories = "$cats"
+++

# $main_heading

> $freq_line

---

## 답안.

### Ⅰ. 개요

$definition

### Ⅱ. 핵심 구성요소
EOF

    # Add code blocks if any exist (ASCII diagrams)
    if [ -n "$code_blocks" ]; then
        echo "" >> "$TMPF"
        echo "$code_blocks" >> "$TMPF"
        echo "" >> "$TMPF"
    fi

    cat >> "$TMPF" << 'BODY'

해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교
BODY

    # Add comparison table if exists
    if [ -n "$comp_table" ]; then
        echo "" >> "$TMPF"
        echo "$comp_table" >> "$TMPF"
    fi

    cat >> "$TMPF" << 'FOOTER'

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
FOOTER

    # Validate and copy
    if [ -s "$TMPF" ]; then
        cp "$TMPF" "$f"
        converted=$((converted+1))
    else
        errors=$((errors+1))
    fi
done

echo "=== CONVERSION COMPLETE ==="
echo "Converted: $converted"
echo "Skipped (already done): $skipped"
echo "Errors: $errors"
