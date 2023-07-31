import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse


def simple_web_crawler(url, max_depth=2):
    visited_urls = set()
    rp = RobotFileParser()

    def crawl(url, depth):
        if depth > max_depth:
            return

        if url in visited_urls:
            return

        visited_urls.add(url)

        try:
            # Check robots.txt before crawling the URL
            base_url = f"{url.scheme}://{url.netloc}"
            robots_txt_url = urljoin(base_url, "robots.txt")
            rp.set_url(robots_txt_url)
            rp.read()

            if not rp.can_fetch("*", url.geturl()):
                print(f"Skipping: {url.geturl()} - Blocked by robots.txt")
                return

            response = requests.get(url.geturl())
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                print(f"Crawling: {url.geturl()}")

                # Process the data from the page here (e.g., extract information)
                # For demonstration purposes, we will just print the page title
                print(f"Title: {soup.title.string}")

                # Recursively crawl links on the page
                for link in soup.find_all('a'):
                    next_url = link.get('href')
                    if next_url and next_url.startswith('http'):
                        next_url_parsed = urlparse(next_url)
                        if next_url_parsed.netloc == url.netloc:
                            crawl(next_url_parsed, depth + 1)

        except Exception as e:
            print(f"Error crawling {url.geturl()}: {e}")

    starting_url = urlparse(url)
    rp.set_url(urljoin(f"{starting_url.scheme}://{starting_url.netloc}", "robots.txt"))
    rp.read()

    if rp.can_fetch("*", url):
        crawl(starting_url, 1)
    else:
        print(f"The website {url} is disallowed by robots.txt.")


if __name__ == "__main__":
    # Provide the starting URL for the web crawler
    starting_url = "https://www.youtube.com/@CodecHorizonLabs"
    simple_web_crawler(starting_url)
