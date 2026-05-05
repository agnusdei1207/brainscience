#!/bin/bash
BASE="/home/ubuntu/workspace/brainscience/content/studynote/01_computer_architecture"
for dir in "$BASE"/[0-9]*/; do
    name=$(basename "$dir")
    count=$(find "$dir" -maxdepth 1 -name '*.md' ! -name '_index.md' | wc -l)
    first=$(find "$dir" -maxdepth 1 -name '*.md' ! -name '_index.md' -printf '%f\n' | sort | head -1)
    last=$(find "$dir" -maxdepth 1 -name '*.md' ! -name '_index.md' -printf '%f\n' | sort | tail -1)
    echo "$name: $count files ($first ... $last)"
done
