import requests
from bs4 import BeautifulSoup

def get_urls(url):
    """Diese Funktion liest von einer gegebenen URL die Anchor-Tags mit einem href aus
    und gibt die entsprechendend Keywords dazu zurück"""
    r  = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    website_urls = []
    for link in soup('a', href=True):
        href = link['href']
        keywords = link.get_text().split()
        website_urls.append((href, keywords))

    return website_urls, len(website_urls)

def print_urls(urls_with_keywords):
    for url, keywords in urls_with_keywords:
        print(f"URL: {url}")
        print(f"Keywords: {', '.join(keywords)}")
        print("-" * 40)


if __name__ == '__main__':
    urls, count = get_urls('https://th-brandenburg.de')
    print_urls(urls)
    print(f"Total URLs found: {count}")