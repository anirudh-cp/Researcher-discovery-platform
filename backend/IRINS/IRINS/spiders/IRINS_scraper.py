import scrapy
import json
import nltk


class IrinsScraperSpider(scrapy.Spider):
    name = 'IRINS_scraper'
    allowed_domains = ['irins.org']
    start_url = None

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'FEED_URI': 'irins.json',
        'FEED_FORMAT': 'json',
        'ITEM_PIPELINES': {
            'IRINS.IRINS.pipelines.IrinsPipeline': 300,
        }
    }

    last_page_index = 20

    def start_requests(self):
        for page in range(1, self.last_page_index + 1):
            next_url = 'https://irins.org/irins/a/searchc/search'
            form_data = {
                'field': 'all',
                'title': '',
                'opt': 'free',
                'limits': '100',
                'cPageNo': f'{page}'
            }

            # form_data = {'field': 'all', 'title': '', 'opt': 'free', 'limits': '10', 'cPageNo': '2'}
            yield scrapy.http.FormRequest(next_url, formdata=form_data, callback=self.parse_page)


    def parse_page(self, response):
        response_html = scrapy.Selector(text=str(response.body)[2:-1])
        urls = response_html.xpath('//div[@class="col-sm-3 product-description"]'
                                   '/div/div/center/'
                                   'a[@class="btn-u btn-u-dark-blue"]'
                                   '/@href').extract()

        yield from response.follow_all(urls, self.parse_person)

    def parse_person(self, response):
        name = response.xpath('//div[@class="profile-blog br1"]/ul/li/h1/strong/text()').extract_first()
        name = " ".join(name.split())
        qual = response.xpath('//div[@class="profile-blog br1"]/ul/li[3]/text()').extract_first().rstrip()
        qual = " ".join(qual.split())

        expertise = response.xpath('//div[@id="expertise-view"]/div/h5/text()').extract_first()
        expertise = [word for (word, pos) in nltk.pos_tag(nltk.word_tokenize(expertise)) if pos[0] == 'N']

        citations = response.xpath('//div[@class="Cell-citation br1"]/div[2]/span/text()').extract_first()
        hindex = response.xpath('//div[@class="Cell-citation br1"]/span/text()').extract_first()

        orcid = response.xpath('//div[@id="identity-view"]/ul/li/div/span[2]/small/a/text()').extract_first()

        yield {'name': name, 'qual': qual, 'exp':expertise, 'cite': citations,
               'hindex': hindex, 'orcid': orcid, 'link': response.url}
