# get-your-own-pdfs
given your list of publications, find DOI links and then try to download their PDFs

references.txt = initial list of references
get_dois.py gets the initial list of dois, saves it with the references into references_with_dois.txt
extract_dois.sh extracts just the list of dois, saves it as doi_links.txt
clean_doi_links.sh removes any duplicates, saves it as doi_links_unique.txt
doi_pdf_download.py for each doi, downloads a pdf into pdfs/

