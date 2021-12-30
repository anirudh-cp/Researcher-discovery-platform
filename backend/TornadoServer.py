import scrapydo

scrapydo.setup()

from tornado import web, ioloop
import json

from ACM.ACM.spiders.ACM_scraper import AcmScraperSpider as ACMScraper


class ResultPageRequestHandler(web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def post(self):
        data = json.loads(self.request.body)
        query_name = data['query_name']
        page = data['page']
        filters = data['filters']
        # data = {"Data": f"{self.query_name} + {self.page} + {self.filters}"}

        search_terms = query_name.split()
        ACMScraper.search_term = search_terms
        scraper_results = scrapydo.run_spider(ACMScraper)

        results = {"query_name": query_name, "page": page,
                   "filters": filters, "records": scraper_results}

        self.write(json.dumps(results))


if __name__ == '__main__':
    app = web.Application([
        (r'/results', ResultPageRequestHandler)
    ])

    app.listen(8000)
    ioloop.IOLoop.current().start()
