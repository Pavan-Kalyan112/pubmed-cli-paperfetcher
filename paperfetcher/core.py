from typing import List, Dict
from Bio import Entrez, Medline
import time
from io import StringIO
from paperfetcher.utils import is_non_academic, extract_email, clean_text

Entrez.email = "your_email@example.com"  # Replace with your actual email


def search_pubmed(query: str, max_results: int = 20) -> List[str]:
    """Search PubMed and return a list of PubMed IDs."""
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    return record.get("IdList", [])


def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict]:
    """Fetch detailed MEDLINE data for a list of PubMed IDs and parse it."""
    all_papers = []
    for i in range(0, len(pubmed_ids), 10):  # process in batches of 10
        batch = pubmed_ids[i:i + 10]
        handle = Entrez.efetch(db="pubmed", id=batch, rettype="medline", retmode="text")
        data = handle.read()
        parsed = parse_medline(data)
        all_papers.extend(parsed)
        time.sleep(1)  # to respect PubMed rate limits
    return all_papers


def parse_medline(medline_text: str) -> List[Dict]:
    """Parse MEDLINE text into structured paper dictionaries."""
    papers = []
    handle = StringIO(medline_text)
    records = Medline.parse(handle)

    for record in records:
        pubmed_id = record.get("PMID", "N/A")
        title = clean_text(record.get("TI", "No Title"))
        pub_date = record.get("DP", "Unknown")
        abstract = clean_text(record.get("AB", ""))
        authors = record.get("AU", [])

        # Normalize affiliation data
        raw_affiliations = record.get("AD", [])
        affiliations = [raw_affiliations] if isinstance(raw_affiliations, str) else raw_affiliations

        non_academic_authors = []
        company_affiliations = []

        for affil in affiliations:
            if is_non_academic(affil):
                company_affiliations.append(affil)
                non_academic_authors.extend(authors)

        # Step 1: Prefer the EM field if available
        email = record.get("EM")

        # Step 2: Fallback to regex from affiliations, IR, and abstract
        if not email:
            fallback_fields = []
            if affiliations:
                fallback_fields.extend(affiliations)
            if "IR" in record:
                fallback_fields.extend(record["IR"])
            if "AB" in record:
                fallback_fields.append(record["AB"])
            email = extract_email(fallback_fields)

        papers.append({
            "PubmedID": pubmed_id,
            "Title": title,
            "Publication Date": pub_date,
            "Abstract": abstract,
            "Non-academic Authors": list(set(non_academic_authors)),
            "Company Affiliations": list(set(company_affiliations)),
            "Corresponding Author Email": email or "N/A"
        })

    return papers


def filter_non_academic(papers: List[Dict]) -> List[Dict]:
    """Filter papers that have at least one company affiliation."""
    return [paper for paper in papers if any(is_non_academic(aff) for aff in paper.get("Company Affiliations", []))]
