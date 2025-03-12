PubMed Paper Fetcher
Table of Contents
Introduction
Features
Installation
Usage
Command-line Options
Output Format
Project Structure
Dependencies
Error Handling
Contributing
License

Introduction
PubMed Paper Fetcher is a Python command-line tool that searches for research papers in PubMed, extracts relevant details, and saves them in a CSV file. The program specifically identifies papers authored by individuals affiliated with pharmaceutical or biotech companies.


Features
✔ Fetches papers using the PubMed API based on a user-specified query.
✔ Extracts and filters papers with non-academic authors.
✔ Identifies company affiliations from author details.
✔ Extracts corresponding author emails.
✔ Saves results in a structured CSV format.
✔ Supports command-line options for flexibility.


Installation
1. Clone the Repository
cd pubmed-paper-fetcher

2. Install Dependencies
pip install poetry
poetry install

Usage
Run the program using:
poetry run get-papers-list "<your-query>"
For example, to search for biotech research papers and save results in results.csv:
poetry run get-papers-list "biotech research" -f results.csv


Command-line Options
Option	   Description
-h,        --help	Display help information.
-d,        --debug	Enable debug mode to print execution details.
-f         <filename>	Save output to a specified CSV file (default: prints to console).


Output Format
The CSV file will contain the following fields:

Field	                      Description
PubMed ID	                  Unique identifier of the research paper.
Title	                      Title of the paper.
Publication Date	          Date the paper was published.
Non-academic Author(s)	    List of authors affiliated with companies (not universities).
Company Affiliation(s)	    Names of pharmaceutical/biotech companies.
Corresponding Author Email	Email of the corresponding author.


Project Structure
pubmed-paper-fetcher/
│── pubmed_fetcher/
│   ├── __init__.py
│   ├── fetch.py        
│   ├── parser.py       
│   ├── save_csv.py    
│   ├── cli.py          
│── tests/              
│── README.md           
│── pyproject.toml      
│── LICENSE             


Dependencies
Dependency	      Purpose
requests	        Handles API requests to PubMed.
csv	              Saves data to CSV files.
argparse	        Parses command-line arguments.
re	              Extracts email addresses & company names.

Error Handling
✔ Handles invalid API responses.
✔ Skips papers without relevant authors or missing data.
✔ Prints warnings for network issues.

Contributing
Want to contribute? Fork the repo, create a branch, and submit a pull request.

License
This project is licensed under the MIT License.
