import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse
import re

class WebCrawler:
    def __init__(self):
        self.index = defaultdict(list)
        self.visited = set()

    def crawl(self, url, base_url=None):
        if url in self.visited:
            return
        self.visited.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            self.index[url] = soup.get_text()

            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    # Always resolve to absolute URL
                    href = urljoin(base_url or url, href)
                    if href.startswith(base_url or url):
                        self.crawl(href, base_url=base_url or url)
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def search(self, keyword):
        results = []
        for url, text in self.index.items():
            # Only add URL if keyword is present as a whole word (case-insensitive)
            if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
                results.append(url)
        return results

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                print(f"- {result}")
        else:
            print("No results found.")

def main():
    crawler = WebCrawler()
    start_url = "https://example.com"
    crawler.craw(start_url)

    keyword = "test"
    results = crawler.search(keyword)
    crawler.print_results(results)

import unittest
from unittest.mock import patch, MagicMock
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse
import re

class WebCrawlerTests(unittest.TestCase):
    @patch('requests.get')
    def test_crawl_success(self, mock_get):
        sample_html = """
        <html><body>
            <h1>Welcome!</h1>
            <a href="/about">About Us</a>
            <a href="https://www.external.com">External Link</a>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        # Assert that 'about' was added to visited URLs
        self.assertIn("https://example.com/about", crawler.visited)

    @patch('requests.get')
    def test_crawl_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test Error")

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        # Assertions to check if the error was logged (you'll
        # likely need to set up logging capture in your tests)

    def test_search(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This has the keyword"
        crawler.index["page2"] = "No key word here"

        results = crawler.search("keyword")
        self.assertEqual(results, ["page1"])

    @patch('sys.stdout')
    def test_print_results(self, mock_stdout):
        crawler = WebCrawler()
        crawler.print_results(["https://test.com/result"])

        # Assert that the output was captured correctly by mock_stdout

    @patch('requests.get')
    def test_crawl_empty_url(self, mock_get):
        crawler = WebCrawler()
        crawler.crawl("")
        self.assertIn("", crawler.visited)

    @patch('requests.get')
    def test_crawl_duplicate_links(self, mock_get):
        sample_html = """
        <html><body>
            <a href="/about">About Us</a>
            <a href="/about">About Us Again</a>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response
        crawler = WebCrawler()
        crawler.crawl("https://example.com")
        # Should only visit /about once
        self.assertEqual(list(crawler.visited).count("https://example.com/about"), 1)

    @patch('requests.get')
    def test_crawl_non_html_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "{\"json\": true}"
        mock_get.return_value = mock_response
        crawler = WebCrawler()
        crawler.crawl("https://example.com/api")
        self.assertIn("https://example.com/api", crawler.index)

    @patch('requests.get')
    def test_crawl_circular_links(self, mock_get):
        sample_html = """
        <html><body>
            <a href="/loop">Loop</a>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response
        crawler = WebCrawler()
        # Simulate /loop links back to itself
        def side_effect(url, *args, **kwargs):
            if url.endswith("/loop"):
                return mock_response
            return mock_response
        mock_get.side_effect = side_effect
        crawler.crawl("https://example.com/loop")
        # Should not infinite loop
        self.assertIn("https://example.com/loop", crawler.visited)

    def test_search_empty_index(self):
        crawler = WebCrawler()
        results = crawler.search("anything")
        self.assertEqual(results, [])

    def test_search_case_insensitive(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "KEYword in caps"
        results = crawler.search("keyword")
        self.assertEqual(results, ["page1"])

    def test_search_no_match(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "no match here"
        results = crawler.search("notfound")
        self.assertEqual(results, [])

    @patch('sys.stdout')
    def test_print_results_empty(self, mock_stdout):
        crawler = WebCrawler()
        crawler.print_results([])
        output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
        self.assertIn("No results found.", output)

    @patch('sys.stdout')
    def test_print_results_multiple(self, mock_stdout):
        crawler = WebCrawler()
        crawler.print_results(["url1", "url2"])
        output = "".join(call.args[0] for call in mock_stdout.write.call_args_list)
        self.assertIn("Search results:", output)
        self.assertIn("- url1", output)
        self.assertIn("- url2", output)

    @patch('requests.get')
    def test_crawl_invalid_url(self, mock_get):
        mock_get.side_effect = requests.exceptions.InvalidURL("Invalid URL")
        crawler = WebCrawler()
        crawler.crawl("ht!tp://bad_url")
        self.assertIn("ht!tp://bad_url", crawler.visited)

if __name__ == "__main__":
    unittest.main()  # Run unit tests
    main()  # Run your main application logic 


if __name__ == "__main__":
    main()
