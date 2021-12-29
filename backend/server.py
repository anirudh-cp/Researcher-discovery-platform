from scrapy.crawler import CrawlerProcess

from ACM.ACM.spiders.ACM_scraper import AcmScraperSpider as ACMScraper
from SciDir.SciDir.spiders.SciDir_scraper import \
    ScidirScraperSpider as SciDirScraper

import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


def main():
    search_terms = input('Enter search term : ').split()
    # term = ['Apple', 'ice']

    ACMScraper.search_term = search_terms
    SciDirScraper.search_term = search_terms

    process = CrawlerProcess()

    process.crawl(ACMScraper)
    process.crawl(SciDirScraper)

    # the script will block here until the crawling is finished
    process.start()


@app.route('/results', methods=["GET"], strict_slashes=False)
def main_process():
    return {'Hello': 'World', 'ABC': 123}


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
