import scrapydo
scrapydo.setup()

from tornado import web, ioloop
import json

from ACM.ACM.spiders.ACM_scraper import AcmScraperSpider as ACMScraper
from pymongo import MongoClient


class ResultPageRequestHandler(web.RequestHandler):
    page_pointers = {'ACM': [{'page': 0, 'article': 0, 'person': 0, 'Done': False}]}
    client, db, collection = None, None, None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = MongoClient(
            'mongodb+srv://python:pythonpass@datacluster.8ohor.mongodb.net/RDP_DB?retryWrites=true&w=majority')
        self.db = self.client.get_database('RDP_DB')
        self.collection = self.db.irins

    def dynamic_scraper(self, query_name, page):
        new = False
        if page == 0:  # Erase pointers if new query
            self.page_pointers['ACM'] = self.page_pointers['ACM'][:1]
            ACMScraper.pointer = self.page_pointers['ACM'][-1].copy()
            page = 1
            new = True

        if page == len(self.page_pointers['ACM']):  # Add pointer for next page
            ACMScraper.pointer = self.page_pointers['ACM'][-1].copy()
            new = True
        else:
            ACMScraper.pointer = self.page_pointers['ACM'][page - 1].copy()

        search_terms = query_name.split()
        ACMScraper.search_term = search_terms
        scraper_results = scrapydo.run_spider(ACMScraper)

        # results = {"query_name": query_name, "page": page, "filters": filters, "records": scraper_results}

        if new:
            self.page_pointers['ACM'].append(ACMScraper.pointer.copy())
            self.page_pointers['ACM'][-1]['Done'] = False

        return scraper_results

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
        sort = data['sort']
        order = data['order']
        pageTotal = data['pageTotal']
        # data = {"Data": f"{self.query_name} + {self.page} + {self.filters}"}

        query_name = query_name.lower()
        results = []
        result_fields = {'name':1, 'qual':1, 'cite':1, 'hindex':1, 'orcid':1, 'link':1,'_id':1}
        order = -1 if order == "Descending" else 1
        page = 1 if page == 0 else page

        if 'ACM' in filters:
            results = self.dynamic_scraper(query_name, page)
        else:
            search_terms = query_name.split()
            query = {'exp': {'$all': search_terms}}
            if filters:
                query['qual'] = {'$in': filters}

            initial, final = (page-1)*pageTotal, page*pageTotal
            if sort == "Sort by H-Index":
                results = exact = self.collection.find(query, result_fields).sort('hindex', order).skip(initial).limit(final)
            elif sort == "Sort by Citations":
                results = exact = self.collection.find(query, result_fields).sort('cite', order).skip(initial).limit(final)
            elif sort == "Sort by Name":
                results = exact = self.collection.find(query, result_fields).sort('name', order).skip(initial).limit(final)

        results = list(results)

        for result in results:
            result['key'] = str(result["_id"])
            result.pop('_id', None)

        final_data = {"query_name": query_name, "page": page,
                      "filters": filters, "records": results}

        # print(self.page_pointers, page)
        self.write(json.dumps(final_data))


def main():
    app = web.Application([
        (r'/results', ResultPageRequestHandler),
        (r'/refresh_db', None)
    ])

    app.listen(8000)
    print('Server has started listening...')
    # server.start(0)  # forks one process per cpu
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
