# etl/news_etl.py
"""
ETL Pipeline: Extracts news articles from a live RSS feed, cleans them, and stores them for vector indexing.
"""

import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

class NewsETL:
    def __init__(self, feed_urls):
        self.feed_urls = feed_urls

    def extract(self):
        articles = []
        for url in tqdm(self.feed_urls, desc="Extracting news"):
            try:
                resp = requests.get(url)
                soup = BeautifulSoup(resp.content, 'xml')
                items = soup.find_all("item")
                for item in items:
                    articles.append({
                        "title": item.title.text,
                        "link": item.link.text,
                        "description": item.description.text
                    })
            except Exception as e:
                print(f"Error fetching from {url}: {e}")
        return articles

    def save(self, articles, path="data/news.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    feed_urls = [
        "https://feeds.bbci.co.uk/news/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
    ]
    etl = NewsETL(feed_urls)
    data = etl.extract()
    etl.save(data)
