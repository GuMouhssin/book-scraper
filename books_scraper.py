#libraries:
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import json
import csv

#VARs;
base_url = "https://books.toscrape.com/"
headers = {
    "User-Agent":"Mozilla/5.0"
}

#config:
Delay = 1
Max_retries = 3

#functions:

def fetch(url):
    last_error = None
    for i in range(Max_retries):
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException as e:
            last_error = e
            print(f"{i+1} retry for: {url}")
            time.sleep(2)

    print(f"ERROR: {last_error} -- URL: {url}")
    return None

def get_books_links(url):
    print("--------Collecting books Links--------")
    i = 1
    page = url
    links = []
    while page:
        resp = fetch(page)
        if not resp:
            continue
        print(f"Collecting links from page-{i}")
        soup = BeautifulSoup(resp.text, "html.parser")
        books = soup.find_all("article", class_ = "product_pod")
        for book in books:
            rel_url = book.h3.a["href"]
            full_url = urljoin(page, rel_url)
            links.append(full_url)
        next_button = soup.find("li", class_ = "next")
        if next_button:
            page = urljoin(page ,next_button.a["href"])
        else:
            page = None
        i += 1
    return links

def parse_product_page(url):
    resp = fetch(url)
    if not resp:
        print(f"Parsing failled: {url}")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    book = soup.find("div", class_="col-sm-6 product_main")

    if not book:
        print(f"Parsing failled: {url}")
        return None

    # Title
    title_tag = book.find("h1")
    title = title_tag.text if title_tag else "N/A"

    # Price
    price_tag = book.find("p", class_="price_color")
    price = price_tag.text if price_tag else "N/A"

    # Rating
    rating_tag = book.find("p", class_="star-rating")
    rating = rating_tag["class"][1] if rating_tag and len(rating_tag["class"]) > 1 else "N/A"

    # Availability
    avail_tag = book.find("p", class_="instock availability")
    availability = avail_tag.text.strip() if avail_tag else "N/A"

    # Description
    desc_tag = soup.find("div", id="product_description")
    para_tag = desc_tag.find_next_sibling("p") if desc_tag else None
    description = para_tag.text if para_tag else "N/A"

    # Category
    bread = soup.find("ul", class_="breadcrumb")
    category = "N/A"
    if bread:
        LIs = bread.find_all("li")
        if len(LIs) > 2:
            category = LIs[2].text.strip()

    return {
        "title": title.strip(),
        "price": price.replace("Â", "").strip(),
        "rating": rating.strip(),
        "availability": availability.strip(),
        "description": description,
        "category": category.strip(),
        "url": url.strip()
    }

def scrape_all_books(start_url):
    links = get_books_links(start_url)
    print(f"Collected {len(links)} links.")
    data = []
    print("-------Starting scraping-------")
    for i, link in enumerate(links, start=1):
        print(f"Scraping {i}/{len(links)}")

        book = parse_product_page(link)

        if book:
            data.append(book)

        time.sleep(Delay) 
    return data

def scrape_by_category(start_url, category):
    links = get_books_links(start_url)
    print(f"Collected {len(links)} links.")
    data = []
    print("-------Starting scraping-------")
    for i, link in enumerate(links, start=1):
        print(f"Scraping {i}/{len(links)}")

        book = parse_product_page(link)

        if book and book["category"].lower() == category.lower():
            data.append(book)

        time.sleep(Delay) 
    return data



def save_json(data, filename = "books"):
    if not data or len(data) == 0:
        print("ERROR: there is no data to save")
        return
    with open(filename + ".json", "w", encoding = "utf-8") as f:
        json.dump(data, f, indent = 2)

def save_csv(data, filename = "books"):
    if not data or len(data) == 0:
        print("ERROR: there is no data to save")
        return
    with open(filename + ".csv", "w", newline = "", encoding = "utf-8") as f:
        keys = data[0].keys()
        writer = csv.DictWriter(f, fieldnames = keys)
        writer.writeheader()
        writer.writerows(data)

def search_books(data):
    keyword = input("Enter keyword: ").lower()

    results = [
        book for book in data
        if keyword in book["title"].lower()
    ]
    i = 1
    for book in results:
        print(f"{i}-{book['title']} - {book['price']}")
        i += 1

    print(f"\nFound {len(results)} result(s)")

if __name__ == "__main__":
    start_url = "https://books.toscrape.com/catalogue/page-1.html"
    books = []

    while True:
        print("\n=== BOOK SCRAPER MENU ===")
        print("1. Scrape books")
        print("2. Save to JSON")
        print("3. Save to CSV")
        print("4. Search books")
        print("5. Scraping by categories")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            books = scrape_all_books(start_url)
            print(f"Scraped {len(books)} books.")

        elif choice == "2":
            if books:
                filename = input("Enter JSON filename: ").strip() or "books"
                save_json(books, filename)
                print("Saved to JSON.")
            else:
                print("No data available. Scrape first.")

        elif choice == "3":
            if books:
                filename = input("Enter CSV filename: ").strip() or "books"
                save_csv(books, filename)
                print("Saved to CSV.")
            else:
                print("No data available. Scrape first.")

        elif choice == "4":
            if books:
                search_books(books)
            else:
                print("No data available. Scrape first.")

        elif choice == "5":
            category = input("Enter a category: ")
            books = scrape_by_category(start_url,  category)
            print(f"Scraped {len(books)} books of {category} category.")

        elif choice == "6":
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Try again.")

    
