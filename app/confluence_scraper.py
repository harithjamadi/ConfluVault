import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import os

CONFLUENCE_URL = "https://your-confluence-domain.atlassian.net/wiki"
USERNAME = "your.email@example.com"
API_TOKEN = "your_api_token"  # Get from Atlassian → API tokens

HEADERS = {
    "Accept": "application/json"
}

AUTH = (USERNAME, API_TOKEN)

def get_page_ids_from_space(space_key):
    url = f"{CONFLUENCE_URL}/rest/api/content"
    params = {
        "spaceKey": space_key,
        "expand": "body.view",
        "limit": 100
    }
    response = requests.get(url, headers=HEADERS, auth=AUTH, params=params)
    results = response.json()
    return results['results']

def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # Optional: remove unwanted tags
    for tag in soup(["script", "style", "footer", "header", "nav"]):
        tag.decompose()

    return str(soup)

def convert_to_markdown(html):
    return md(html, heading_style="ATX")  # ATX = ## headings

def save_markdown(markdown_text, title, output_dir="data/docs"):
    os.makedirs(output_dir, exist_ok=True)
    safe_title = title.replace("/", "-").replace(" ", "_")
    with open(os.path.join(output_dir, f"{safe_title}.md"), "w", encoding="utf-8") as f:
        f.write(markdown_text)

def scrape_confluence_space(space_key):
    pages = get_page_ids_from_space(space_key)
    print(f"Found {len(pages)} pages in space '{space_key}'")

    for page in pages:
        title = page['title']
        html = page['body']['view']['value']
        cleaned = clean_html(html)
        md_text = convert_to_markdown(cleaned)
        save_markdown(md_text, title)

        print(f"[✓] Saved: {title}")

if __name__ == "__main__":
    # Example: 'DEVTEAMSPACE'
    scrape_confluence_space("YOUR_SPACE_KEY")
