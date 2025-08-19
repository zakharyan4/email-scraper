import requests
from bs4 import BeautifulSoup
import time
import pyfiglet
from rich.console import Console

console = Console()

banner = pyfiglet.figlet_format("Email Scraper")
console.print(f"[bold cyan]{banner}[/bold cyan]")

print("Please enter the URL:")
BASE_URL = input()

OUTPUT_FILE = "emails.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def scrape_emails():
    emails = set()  
    range_start = 0
    range_end = 1445
    for user_id in range(range_start, range_end):  
        url = f"{BASE_URL}{user_id}"
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code != 200:
                print(f"Skipping {url} - Status code: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            
            for mailto_link in soup.select('a[href^="mailto:"]'):
                email = mailto_link["href"].replace("mailto:", "").strip()
                if email:
                    emails.add(email)
                    print(f"Found: {email}")

            time.sleep(1)

        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            continue

    with open(OUTPUT_FILE, "w") as f:
        for email in sorted(emails):
            f.write(email + "\n")

    print(f"Scraping complete! Emails saved to {OUTPUT_FILE}")

scrape_emails()
