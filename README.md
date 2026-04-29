# Book Scraper 📚

A Python web scraper that automatically collects data from 
all 1000+ books on books.toscrape.com across 50 pages.

## What it does

- Scrapes all books across all pages automatically
- Extracts 7 fields per book: title, price, rating, 
  availability, description, category and URL
- Interactive menu to control scraping and saving
- Exports clean data to CSV or JSON
- Handles pagination, missing fields and slow connections

## Technologies

- Python 3
- Requests
- BeautifulSoup4
- CSV / JSON file handling

## How to run

1. Install dependencies:
pip install requests beautifulsoup4

2. Run the script:
python book_scraper.py

3. Use the menu:
1 - Scrape all books (takes ~20 minutes)
2 - Save to JSON
3 - Save to CSV
4 - Search books by keyword
5 - Exit

## Sample output

=== BOOK SCRAPER MENU ===
1. Scrape books
2. Save to JSON
3. Save to CSV
4. Search books
5. Exit

Collecting links from page 1...
Collecting links from page 2...
...
Scraping 1/1000
Scraping 2/1000
...
Scraped 1000 books.

## Use cases

- Collect book data for research or analysis
- Build a searchable book database
- Monitor prices across categories
- Export clean datasets for Excel or data tools
