#!/bin/bash

INPUT="doi_links.txt"
OUTPUT="doi_links_unique.txt"

# Remove all duplicates, preserving order
awk '!seen[$0]++' "$INPUT" > "$OUTPUT"

echo "Done! Unique DOI links saved to $OUTPUT"
