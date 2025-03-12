import argparse
from pubmed_fetcher import fetch_pubmed_papers, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Save output to a CSV file")
    parser.add_argument("-n", "--num", type=int, default=10, help="Number of results to fetch")
    
    args = parser.parse_args()

    # Fetch papers
    papers = fetch_pubmed_papers(args.query, args.num)
    
    if args.debug:
        print("\nDebug Mode: Displaying fetched papers...\n")
        for paper in papers:
            print(paper)

    # Save results if file option is provided
    if args.file:
        save_to_csv(papers, args.file)
    else:
        print("\nFetched Papers:")
        for paper in papers:
            print(f"{paper['PubmedID']} - {paper['Title']}")

if __name__ == "__main__":
    main()
