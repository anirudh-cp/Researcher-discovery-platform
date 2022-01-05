import re
from nameparser import HumanName

import nltk
import scrapy


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

    last_page_index = 400
    start_page_index = 101

    def start_requests(self):
        for page in range(self.start_page_index, self.last_page_index + 1):
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
        name_data = " ".join(name.split())
        name_list = HumanName(name_data).as_dict()

        name = ''
        honorific = name_list['title']
        for item in name_list.items():
            if item[1] != '' and item[0] != 'title':
                name = name + (item[1]) + ' '

        qual = response.xpath('//div[@class="profile-blog br1"]/ul/li[3]/text()').extract_first().rstrip()
        qual = " ".join(qual.split())

        expertise = response.xpath('//div[@id="expertise-view"]/div/h5/text()').extract_first()
        expertise = [word.lower() for (word, pos) in nltk.pos_tag(nltk.word_tokenize(expertise)) if pos[0] == 'N']

        citations = response.xpath('//div[@class="Cell-citation br1"]/div[2]/span/text()').extract_first()
        hindex = response.xpath('//div[@class="Cell-citation br1"]/span/text()').extract_first()

        link = ''
        orcid = response.xpath('//div[@id="identity-view"]/ul/li/div/span[2]/small/a/text()').extract_first()
        if not re.match(r"(\d{4}-){3}(\d{4})", orcid):
            orcid = ''
            link = response.url
        else:
            link = 'https://orcid.org/' + orcid

        yield {'name': name, 'honorific': honorific, 'qual': qual,
               'exp':expertise, 'cite': citations,
               'hindex': hindex, 'orcid': orcid, 'link': link}
