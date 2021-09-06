import requests
import multiprocessing
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse


class MultiThreadScraper:
    # contents = list()

    def __init__(self, base_url):
        self.base_url = base_url
        self.root_url = '{}://{}'.format(
            urlparse(self.base_url).scheme,
            urlparse(self.base_url).netloc)
        self.pool = ThreadPoolExecutor(max_workers=5)
        self.scrapped_pages = set([])
        self.to_crawl = Queue()
        self.to_crawl.put(self.base_url)

    def parse_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            url = link['href']
            if url.startswith('/') or url.startswith(self.root_url):
                url = urljoin(self.root_url, url)
                if url not in self.scrapped_pages:
                    self.to_crawl.put(url)

    def scrape_info(self, html):
        soup = BeautifulSoup(html, "html5lib")
        text = soup.get_text(strip=True)
        # print(text)
        return

    def post_scrape_callback(self, res):
        result = res.result()
        if result and result.status_code == 200:
            self.parse_links(result.text)
            self.scrape_info(result.text)

    def scrape_page(self, url):
        try:
            res = requests.get(url, timeout=(3, 30))
            return res
        except requests.RequestException:
            return

    def run_scraper(self):
        while True:
            try:
                print("\n name of the Process:\n",
                      multiprocessing.current_process().name)
                target_url = self.to_crawl.get(timeout=60)
                if target_url not in self.scrapped_pages:
                    print("Scrapping URL: {}".format(target_url))
                    self.scrapped_pages.add(target_url)
                    job = self.pool.submit(self.scrape_page, target_url)
                    job.add_done_callback(self.post_scrape_callback)
            except Empty:
                print("CRAWLING COMPLETED")
                return
            except Exception as e:
                # print(e)
                continue


if __name__ == '__main__':
    s = MultiThreadScraper("https://github.com/")
    s.run_scraper()
