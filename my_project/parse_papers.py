import re
from typing import List, Dict

def extract_non_academic_authors(text: str) -> List[str]:
    """Extract non-academic author names from the text."""
    if not text:
        return []
    # Improved regex to support names with middle names, hyphens, and initials
    return re.findall(r"\b[A-Z][a-z]+(?:\s[A-Z]\.?|\s[A-Z][a-z]+)*\b", text)

def extract_company_affiliations(text: str) -> List[str]:
    """Extract company affiliations from the text."""
    if not text:
        return []
    # Extract full company names before the suffix
    companies = re.findall(r"\b[A-Za-z\s]+(?:Inc|Ltd|Corp|GmbH|LLC|Technologies|Solutions|Systems)\b", text)
    return list(set(companies))  # Remove duplicates

def extract_email(text: str) -> str:
    """Extract the corresponding author’s email from the text."""
    if not text:
        return "N/A"
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else "N/A"

def parse_paper_details(papers: List[Dict]) -> List[Dict]:
    """Parse paper details to extract author info, company affiliations, and emails."""
    for paper in papers:
        abstract_text = paper.get("abstract", "") or ""

        paper["Non-academic Author(s)"] = extract_non_academic_authors(abstract_text)
        paper["Company Affiliation(s)"] = extract_company_affiliations(abstract_text)
        paper["Corresponding Author Email"] = extract_email(abstract_text)

    return papers
