import scrapy


class AcmScraperSpider(scrapy.Spider):
    name = 'ACM_scraper'
    allowed_domains = ['dl.acm.org']

    # To define the search term used for the results page
    search_term = None
    # The actual term used in the URL
    term = None
    # To create the initial requests for the spider
    start_urls = []
    # Max number of records needed
    MAX_YIELD = 5
    # Count of number of records generated
    yield_count = 0
    # Internal pointer
    pointer = {'page': 0, 'article': 0, 'person': 0, 'Done': False}
    # Links to be scraped
    links = []

    def __init__(self):
        super().__init__()
        self.term = '+'.join(x for x in self.search_term)
        self.yield_count = 0
        self.start_urls.append(
            f'https://dl.acm.org/action/doSearch?AllField={self.term}&startPage={self.pointer["page"]}&ContentItemType=research-article')

    def parse(self, response, **kwargs):
        self.links = response.css(".hlFld-Title").xpath('a/@href').extract()
        url = 'https://dl.acm.org' + self.links[self.pointer['article']]
        yield response.follow(url, callback=self.parse_page)

    def parse_page(self, response):
        # title = response.css(".citation__title").extract_first()
        
        author_tile = response.css('.loa__item')
        author_tile = author_tile[(self.pointer['person']) : ]
        
        for author in author_tile:
            self.yield_count += 1
            if self.yield_count > self.MAX_YIELD:
                self.pointer['Done'] = True
                break
            self.pointer['person'] += 1

            name = author.xpath('a/@title').extract_first()
            first_name = name.split(' ', 1)[0]
            last_name = name.split(' ', 1)[1]

            link = self.allowed_domains[0] + author.css(
                '.author-info__body').xpath('a/@href').extract_first()
            link = '' if not link else link

            qualifications = author.css('.loa_author_inst').xpath(
                'p/text()').extract_first()
            qualifications = '' if not qualifications else qualifications

            # print(first_name, last_name, link, qualifications)
            #self.results.append({'First Name': first_name, 'Last Name': last_name,
            #                     'Qualifications': qualifications, 'Link': link})

            yield {'first_name': first_name, 'last_name': last_name,
                   'qual': qualifications, 'link': link, 'key': self.yield_count}

        if not self.pointer['Done']:
            self.pointer['article'] += 1
            if self.pointer['article'] != len(self.links):
                next_url = 'https://dl.acm.org' + self.links[self.pointer['article']]
                self.pointer['person'] = 0
                yield response.follow(next_url, callback=self.parse_page)
            else:
                self.pointer['person'] = 0
                self.pointer['article'] = 0
                self.pointer['page'] += 1
                next_url = f'https://dl.acm.org/action/doSearch?AllField={self.term}&startPage={self.pointer["page"]}&ContentItemType=research-article'
                yield response.follow(next_url, callback=self.parse)
