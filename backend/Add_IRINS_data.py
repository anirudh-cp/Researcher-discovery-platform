from IRINS.IRINS.spiders.IRINS_scraper import IrinsScraperSpider as IRINS_Scraper
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(IRINS_Scraper)
# the script will block here until the crawling is finished
process.start()