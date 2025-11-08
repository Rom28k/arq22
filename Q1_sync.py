import csv
import re
from time import time
from urllib.request import urlopen, Request
import statistics

times = []

def analyze_html(html: str):
    """
    Return a dict of basic stats for a raw HTML string.
    """
    stats = {}
    stats['char_count'] = len(html)
    stats['byte_size']  = len(html.encode('utf-8'))
    stats['line_count'] = html.count('\n') + 1
    stats['word_count'] = len(html.split())
    stats['tag_count']  = html.count('<')
    stats['link_count'] = len(re.findall(r'<a\s', html, flags=re.IGNORECASE))
    stats['img_count']  = len(re.findall(r'<img\s', html, flags=re.IGNORECASE))
    stats['h1_count']   = len(re.findall(r'<h1\b', html, flags=re.IGNORECASE))
    stats['h2_count']   = len(re.findall(r'<h2\b', html, flags=re.IGNORECASE))
    stats['p_count']    = len(re.findall(r'<p\b', html, flags=re.IGNORECASE))
    return stats

def fetch_url(url: str):
    """
    Fetches the URL synchronously, records elapsed time, and returns stats.
    """
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req) as resp:
        html_bytes = resp.read()
    html = html_bytes.decode('utf-8', errors='replace')
    return analyze_html(html)

def load_csv(file_path: str):
    """
    Loads a single-column CSV (with header) of URLs.
    """
    urls = []
    #Completar función
    return urls

def main():
    urls = load_csv('links.csv')
    results = []
    for url in urls:
        try:
            stats = fetch_url(url)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            stats = None
        results.append(stats)

if __name__ == '__main__':
    main()
