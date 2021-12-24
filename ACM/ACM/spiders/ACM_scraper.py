import scrapy


class AcmScraperSpider(scrapy.Spider):
    name = 'ACM_scraper'
    allowed_domains = ['dl.acm.org']

    # To define the search term used for the results page
    search_term = None
    # To create the initial requests for the spider
    start_urls = []

    custom_settings = {'FEED_URI': "ACM.csv",
                       'FEED_FORMAT': 'csv'}

    def __init__(self):
        super().__init__()
        term = '+'.join(x for x in self.search_term)
        self.start_urls.append(
            f'https://dl.acm.org/action/doSearch?AllField={term}&startPage=0&ContentItemType=research-article')

    def parse(self, response, **kwargs):
        links = response.css(".hlFld-Title").xpath('a/@href').extract()
        yield from response.follow_all(links, self.parse_page)
        # for link in links:
        #     yield {'links': link}

    def parse_page(self, response):
        # title = response.css(".citation__title").extract_first()
        author_tile = response.css('.loa__item')
        for author in author_tile:
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
            yield {'First Name': first_name, 'Last Name': last_name,
                   'Qualifications': qualifications, 'Link': link}
