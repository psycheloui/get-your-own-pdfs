#!/usr/bin/env python3
import requests
import sys
import os
import re

# ================= CONFIG =================
EZPROXY_PREFIX = "https://login.ezproxy.neu.edu/login?url="  # Northeastern EZproxy
OUTDIR = "pdfs"  # folder to save PDFs
# ==========================================

def extract_doi_from_line(line):
    """Return DOI from line if present, else None."""
    match = re.search(r'https?://doi\.org/[\w./_-]+', line)
    return match.group(0).replace("https://doi.org/", "") if match else None

def get_doi_from_crossref(reference):
    """Query Crossref for a DOI given a reference string."""
    url = "https://api.crossref.org/works"
    params = {"query.bibliographic": reference, "rows": 1}
    headers = {"User-Agent": "APA-DOI-Script/1.0 (mailto:your_email@neu.edu)"}
    try:
        r = requests.get(url, params=params, headers=headers, timeout=20)
        r.raise_for_status()
        data = r.json()
        items = data.get("message", {}).get("items", [])
        if items:
            return items[0].get("DOI")
    except Exception as e:
        print(f"Error looking up DOI: {e}")
    return None

def download_pdf(doi, filename):
    """Download PDF via Northeastern EZproxy."""
    filepath = os.path.join(OUTDIR, filename)
    if os.path.exists(filepath):
        print(f"Skipped: {filename} already exists")
        return True  # Skip download

    doi_url = f"{EZPROXY_PREFIX}https://doi.org/{doi}"
    headers = {
        "User-Agent": "APA-DOI-Script/1.0 (mailto:p.loui@northeastern.edu)",
        "Accept": "application/pdf"
    }
    try:
        r = requests.get(doi_url, headers=headers, timeout=60, allow_redirects=True)
        content_type = r.headers.get("content-type", "")
        if r.status_code == 200 and "pdf" in content_type.lower():
            os.makedirs(OUTDIR, exist_ok=True)
            with open(filepath, "wb") as f:
                f.write(r.content)
            print(f"Saved PDF: {filepath}")
            return True
        else:
            print(f"No direct PDF found at {doi_url} (status={r.status_code}, content-type={content_type})")
    except Exception as e:
        print(f"Error downloading PDF for DOI {doi}: {e}")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python get_dois.py input.txt output.txt")
        sys.exit(1)

    infile, outfile = sys.argv[1], sys.argv[2]

    with open(infile, "r") as f:
        references = [line.strip() for line in f if line.strip()]

    with open(outfile, "w") as out:
        for idx, ref in enumerate(references, start=1):
            doi = extract_doi_from_line(ref)
            if not doi:
                doi = get_doi_from_crossref(ref)

            if doi:
                ref_with_doi = f"{ref} DOI: https://doi.org/{doi}"
                print(ref_with_doi)
                out.write(ref_with_doi + "\n")

                # Sequential filename
                filename = f"{idx:03d}.pdf"
                download_pdf(doi, filename)
            else:
                ref_with_doi = f"{ref} DOI: NOT FOUND"
                print(ref_with_doi)
                out.write(ref_with_doi + "\n")
