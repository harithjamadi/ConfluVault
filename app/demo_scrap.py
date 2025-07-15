import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import os

BASE_URL = "https://quotes.toscrape.com"
OUTPUT_DIR = "data/docs"

def fetch_quotes_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.select(".quote")
    page_md = ""

    for quote in quotes:
        text = quote.find("span", class_="text").get_text(strip=True)
        author = quote.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.select(".tags .tag")]

        quote_html = f"""
        <blockquote>{text}</blockquote>
        <p><strong>{author}</strong></p>
        <p><em>Tags: {', '.join(tags)}</em></p>
        <hr>
        """
        quote_md = md(quote_html)
        page_md += quote_md + "\n"

    return page_md

def scrape_all_pages():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    page = 1
    url = BASE_URL
    all_md = ""

    while True:
        print(f"Scraping page {page}...")
        page_md = fetch_quotes_from_page(url)
        all_md += page_md

        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        next_btn = soup.select_one("li.next > a")
        if next_btn:
            next_url = BASE_URL + next_btn["href"]
            url = next_url
            page += 1
        else:
            break

    # Save final Markdown
    with open(os.path.join(OUTPUT_DIR, "quotes.md"), "w", encoding="utf-8") as f:
        f.write(all_md)
    print(f"✓ Done. Saved markdown to: {OUTPUT_DIR}/quotes.md")

if __name__ == "__main__":
    scrape_all_pages()
