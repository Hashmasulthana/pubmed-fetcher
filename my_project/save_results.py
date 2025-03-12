import csv
from typing import List, Dict

def save_to_csv(papers: List[Dict], filename: str):
    """Save the results to a CSV file."""
    if not papers:
        print("No data to save.")
        return

    try:
        # Ensure all dictionaries have the same keys
        fieldnames = set().union(*(paper.keys() for paper in papers))

        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(papers)

        print(f"✅ Results successfully saved to {filename}")

    except Exception as e:
        print(f"❌ Error saving file: {e}")
