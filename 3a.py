import requests
from bs4 import BeautifulSoup

def get_urls(url):
    r  = requests.get(url)
    #print(r.text)
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

urls, count = get_urls('https://th-brandenburg.de')
print_urls(urls)
print(f"Total URLs found: {count}")
#print(get_urls('https://th-brandenburg.de'))