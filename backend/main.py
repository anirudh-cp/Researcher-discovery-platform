from scrapy.crawler import CrawlerProcess

from ACM.ACM.spiders.ACM_scraper import AcmScraperSpider as ACMScraper
from SciDir.SciDir.spiders.SciDir_scraper import ScidirScraperSpider as SciDirScraper


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


def main_process(term):
    search_term = term.split()
    return search_term


if __name__ == '__main__':
    main()
