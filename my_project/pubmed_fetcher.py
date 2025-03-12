import requests
import csv
import argparse
from Bio import Entrez

# Set PubMed API email (change this to your email)
Entrez.email = "your_email@example.com"

def fetch_pubmed_papers(query: str, max_results: int = 10):
    """
    Fetch papers from PubMed API using the specified query.
    """
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        handle.close()
        
        paper_ids = record["IdList"]
        if not paper_ids:
            print("No matching papers found.")
            return []

        # Fetch paper details
        handle = Entrez.efetch(db="pubmed", id=paper_ids, rettype="xml")
        papers_data = Entrez.read(handle)
        handle.close()

        papers = []
        for article in papers_data["PubmedArticle"]:
            medline = article["MedlineCitation"]["Article"]
            pubmed_id = article["MedlineCitation"]["PMID"]
            title = medline["ArticleTitle"]
            pub_date = medline["ArticleDate"][0]["Year"] if "ArticleDate" in medline else "N/A"
            
            authors = medline.get("AuthorList", [])
            non_academic_authors = []
            company_affiliations = []
            corresponding_email = "N/A"

            for author in authors:
                if "AffiliationInfo" in author:
                    affiliation = author["AffiliationInfo"][0]["Affiliation"]
                    if any(keyword in affiliation.lower() for keyword in ["pharma", "biotech", "laboratory", "company"]):
                        non_academic_authors.append(author.get("LastName", "Unknown"))
                        company_affiliations.append(affiliation)
                    if "@" in affiliation:
                        corresponding_email = affiliation.split()[-1]

            papers.append({
                "PubmedID": pubmed_id,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": ", ".join(non_academic_authors),
                "Company Affiliation(s)": ", ".join(company_affiliations),
                "Corresponding Author Email": corresponding_email
            })

        return papers

    except Exception as e:
        print(f"Error fetching PubMed data: {e}")
        return []


def save_to_csv(papers, filename="results.csv"):
    """
    Save fetched papers to a CSV file.
    """
    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=[
                "PubmedID", "Title", "Publication Date", 
                "Non-academic Author(s)", "Company Affiliation(s)", 
                "Corresponding Author Email"
            ])
            writer.writeheader()
            writer.writerows(papers)
        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")
