#!/usr/bin/env bash
# Extract all https links (like DOI links) from a references text file.

# Input file with references
INPUT_FILE="references_dois.txt"

# Output file for the links (optional)
OUTPUT_FILE="doi_links.txt"

# Grep for https links and write them out
grep -Eo 'https://doi.org/[[:alnum:]/._-]+' "$INPUT_FILE" > "$OUTPUT_FILE"

echo "Extracted links saved to $OUTPUT_FILE"
