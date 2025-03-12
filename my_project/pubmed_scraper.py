import requests
import csv
from bs4 import BeautifulSoup

def fetch_papers(query):
    base_url = "https://pubmed.ncbi.nlm.nih.gov/"
    search_url = f"{base_url}?term={query}"

    response = requests.get(search_url)
    if response.status_code != 200:
        print("Failed to fetch data")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("div", class_="docsum-content")  # Updated selector

    results = []

    for article in articles:
        # Extract PubMed ID correctly
        id_tag = article.find_previous("a", class_="docsum-title")
        pubmed_id = id_tag["href"].split("/")[-1] if id_tag else "N/A"

        # Extract Title
        title = id_tag.text.strip() if id_tag else "N/A"

        # Extract Publication Date
        date_tag = article.find("span", class_="docsum-journal-citation")
        publication_date = date_tag.text.strip().split(".")[-1].strip() if date_tag else "N/A"

        # Fetch details from the article page
        affiliation_url = f"{base_url}{pubmed_id}/"
        aff_response = requests.get(affiliation_url)
        aff_soup = BeautifulSoup(aff_response.text, "html.parser")

        affiliations = []
        emails = []

        for aff in aff_soup.find_all("li", class_="affiliation"):  # Updated selector
            aff_text = aff.text.strip()
            affiliations.append(aff_text)
            if "@" in aff_text:
                emails.append(aff_text)

        # Extract non-academic authors and company affiliations
        non_academic_authors = [aff for aff in affiliations if "university" not in aff.lower()]
        company_affiliations = [aff for aff in affiliations if "pharma" in aff.lower() or "biotech" in aff.lower()]

        # Extract corresponding author email
        corresponding_email = emails[0] if emails else "N/A"

        results.append({
            "PubmedID": pubmed_id,
            "Title": title,
            "Publication Date": publication_date,
            "Non-academic Author(s)": ", ".join(non_academic_authors) if non_academic_authors else "N/A",
            "Company Affiliation(s)": ", ".join(company_affiliations) if company_affiliations else "N/A",
            "Corresponding Author Email": corresponding_email
        })

    return results

def save_to_csv(data, filename="pubmed_results.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "Machine Learning"
    results = fetch_papers(query)
    save_to_csv(results)
    print(f"Results saved to pubmed_results.csv")
