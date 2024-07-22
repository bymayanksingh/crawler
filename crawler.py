import requests
from bs4 import BeautifulSoup
import redis
from urllib.parse import urlparse, urljoin
import hashlib

# Initialize Redis for caching and tracking crawled URLs
cache = redis.StrictRedis(host='localhost', port=6379, db=0)

# Check robots.txt compliance
def check_robots_txt(url):
    parsed_url = urlparse(url)
    robots_url = urljoin(f'{parsed_url.scheme}://{parsed_url.netloc}', '/robots.txt')
    try:
        response = requests.get(robots_url)
        if response.status_code == 200:
            if 'Disallow: /' in response.text:
                return False
        return True
    except Exception as e:
        print(f'Error fetching robots.txt: {e}')
        return False

# Resolve DNS
def resolve_dns(url):
    try:
        ip_address = requests.get(f'https://dns.google/resolve?name={urlparse(url).netloc}')
        if ip_address.status_code == 200:
            return True
    except Exception as e:
        print(f'Error resolving DNS: {e}')
        return False

# Fetch content
def fetch_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f'Error fetching content: {e}')
        return None

# Parse content
def parse_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return text, links

# Store content
def store_content(url, content):
    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
    cache.set(f'content:{url}', content)
    cache.set(f'content_hash:{url}', content_hash)

# Main crawl function
def crawl(url, depth=2):
    if depth == 0:
        return
    
    if cache.exists(f'crawled:{url}'):
        print(f'URL already crawled: {url}')
        return
    
    if not check_robots_txt(url):
        print(f'URL disallowed by robots.txt: {url}')
        return
    
    if not resolve_dns(url):
        print(f'Error resolving DNS for URL: {url}')
        return

    html_content = fetch_content(url)
    if not html_content:
        return
    
    text, links = parse_content(html_content)
    
    content_hash = hashlib.md5(html_content.encode('utf-8')).hexdigest()
    if cache.exists(f'content_hash:{content_hash}'):
        print(f'Duplicate content found for URL: {url}')
        return
    
    store_content(url, html_content)
    cache.set(f'crawled:{url}', 1)
    
    for link in links:
        if urlparse(link).netloc:
            crawl(link, depth-1)

# Initialize crawling process
start_urls = ['https://fizznessshizzness.com/',
              "https://incomeinsider.org/", "https://eddyballe.com/", "https://www.idfy.com/"]
for url in start_urls:
    crawl(url)
