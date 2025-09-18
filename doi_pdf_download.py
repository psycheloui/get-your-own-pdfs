#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

# ====== CONFIG ======
DOI_FILE = "doi_links_unique.txt"        # input file with DOI URLs
OUTDIR = "pdfs"              # folder to save PDFs
DOWNLOAD_WAIT = 5            # seconds to wait for download to start
CHROME_DRIVER_PATH = "/path/to/chromedriver"  # replace with your chromedriver path
# ====================

# Ensure output folder exists
os.makedirs(OUTDIR, exist_ok=True)

# Chrome options: download PDFs automatically
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": os.path.abspath(OUTDIR),
    "plugins.always_open_pdf_externally": True
})
chrome_options.add_argument("--start-maximized")

# Initialize driver
service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Read DOIs
with open(DOI_FILE, "r") as f:
    dois = [line.strip() for line in f if line.strip()]

for idx, doi_url in enumerate(dois, start=1):
    # Sequential filename
    filename = f"{idx:03d}.pdf"
    filepath = os.path.join(OUTDIR, filename)

    if os.path.exists(filepath):
        print(f"Skipped {filename}: already exists")
        continue

    print(f"Processing {idx}/{len(dois)}: {doi_url}")
    try:
        driver.get(doi_url)
        time.sleep(DOWNLOAD_WAIT)  # wait for page to load / download to start

        # Attempt to click PDF link (works on many publishers)
        try:
            pdf_link = driver.find_element(By.PARTIAL_LINK_TEXT, "PDF")
            pdf_link.click()
            print("Clicked PDF link")
            time.sleep(DOWNLOAD_WAIT)
        except:
            print("No explicit PDF link found; download may start automatically")

        # Rename most recently downloaded file to sequential filename
        # Note: Selenium downloads files to OUTDIR automatically, but we need to rename
        # We'll pick the most recent file in OUTDIR
        files = [os.path.join(OUTDIR, f) for f in os.listdir(OUTDIR)]
        files = [f for f in files if f.lower().endswith(".pdf")]
        if files:
            latest_file = max(files, key=os.path.getctime)
            if latest_file != filepath:
                os.rename(latest_file, filepath)
                print(f"Renamed to {filename}")

    except Exception as e:
        print(f"Error processing {doi_url}: {e}")

driver.quit()
print("All done!")
