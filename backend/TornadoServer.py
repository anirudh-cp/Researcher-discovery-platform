import tornado.platform.twisted
# tornado.platform.twisted.install()

import scrapydo
scrapydo.setup()

from tornado import web, ioloop
import json
from copy import deepcopy

from ACM.ACM.spiders.ACM_scraper import AcmScraperSpider as ACMScraper

from scrapy.crawler import CrawlerRunner


class ResultPageRequestHandler(web.RequestHandler):
    page_pointers = {'ACM': [{'page': 0, 'article': 0, 'person': 0, 'Done': False}]}

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "content-type")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, PATCH, PUT')
    
    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    # def get(self):
    #    self.write(json.dumps({'results': 'Hello'}))

    def post(self):
        data = json.loads(self.request.body)
        query_name = data['query_name']
        page = data['page']
        filters = data['filters']
        # data = {"Data": f"{self.query_name} + {self.page} + {self.filters}"}
        
        # print(self.page_pointers, page)

        new = False

        if page == -1:
            # print('Erase')
            self.page_pointers['ACM'] = self.page_pointers['ACM'][:1]
            # print(self.page_pointers)
            ACMScraper.pointer = self.page_pointers['ACM'][-1].copy()
            page = 1
            new = True
        
        # print(self.page_pointers, page, new)

        if page == len(self.page_pointers['ACM']):
            ACMScraper.pointer = self.page_pointers['ACM'][-1].copy()
            new = True
        else:
            ACMScraper.pointer = self.page_pointers['ACM'][page - 1].copy()

        search_terms = query_name.split()
        ACMScraper.search_term = search_terms
        scraper_results = scrapydo.run_spider(ACMScraper)

        results = {"query_name": query_name, "page": page,
                   "filters": filters, "records": scraper_results}
        
        if new:
            # print('Here')
            self.page_pointers['ACM'].append(ACMScraper.pointer.copy())
            self.page_pointers['ACM'][-1]['Done'] = False
            new = False

        # print(self.page_pointers, page)
        self.write(json.dumps(results))


def main():
    app = web.Application([
        (r'/results', ResultPageRequestHandler)
    ])

    app.listen(8000)
    # server.start(0)  # forks one process per cpu
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
