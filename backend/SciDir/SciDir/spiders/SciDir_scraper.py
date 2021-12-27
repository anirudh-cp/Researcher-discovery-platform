import scrapy

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selenium_exec

import json
from urllib.parse import quote


class ScidirScraperSpider(scrapy.Spider):
    name = 'SciDir_scraper'
    allowed_domains = ['sciencedirect.com']

    # To define the search term used for the results page
    search_term = None
    # To create the initial requests for the spider
    start_url = None

    custom_settings = {'USER_AGENT': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
                       'FEED_URI': "SciDir.csv",
                       'FEED_FORMAT': 'csv'}

    SELENIUM_TIMEOUT = 7

    def __init__(self):
        super().__init__()
        term = '+'.join(x for x in self.search_term)
        self.start_url = f'https://www.sciencedirect.com/search?qs={term}&lastSelectedFacet=articleTypes&articleTypes=FLA'

        options = webdriver.ChromeOptions()

        # options.add_argument("--headless")
        # options.add_argument("--start-minimized")

        options.add_argument("--headless")
        headers_ = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'}
        options.add_argument(f"--user-agent={headers_['User-Agent']}")

        self.driver = webdriver.Chrome('SciDir/chromedriver.exe',
                                       chrome_options=options)

    def start_requests(self):
        self.driver.get(self.start_url)

        # self.driver.get_screenshot_as_file("screenshot.png")

        # Wait till element is located (maximum 7 seconds)
        try:
            elem = WebDriverWait(self.driver, self.SELENIUM_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "srp-results-list"))
                # This is a dummy element
            )
        except selenium_exec.TimeoutException:
            print('Selenium Timeout Exception in Science Direct Source scraper')
            return
        finally:
            html_source = self.driver.page_source.encode('utf-8')
            self.driver.quit()

        selenium_response = scrapy.Selector(text=html_source)

        links = selenium_response.css(".result-item-content").xpath('h2/span/a/@href').extract()
        for link in links:
            next_page = 'https://www.sciencedirect.com' + link
            yield scrapy.Request(url=next_page, callback=self.parse_page)

        # yield scrapy.Request(url='https://www.sciencedirect.com/science/article/pii/S0936655521004337', callback=self.parse_page)

        # for link in links:
        #     yield {'links': link}

    def parse_page(self, response):
        script = response.xpath('//script[@type="application/json"]/text()').extract_first()
        data = json.loads(script)['authors']['affiliations']

        # Map a reference character to each qualification as shown in the page.
        qualification = {}

        if len(data.keys()) == 1:
            qualification['0'] = list(data.values())[0]['$$'][0]['_']
        else:
            for term in data.values():
                qualification[term['$$'][0]['_']] = term['$$'][1]['_']

        author_tile = response.css('.author-group').xpath('a')

        # print(qualification)

        for author in author_tile:
            # first_name = author.css('.given-name::text').extract_first()
            first_name = author.xpath('span/span[@class="text given-name"]/text()').extract_first()
            first_name = '' if not first_name else first_name

            # last_name = author.css('.surname::text').extract_first()
            last_name = author.xpath('span/span[@class="text surname"]/text()').extract_first()
            last_name = '' if not last_name else last_name

            if len(qualification) > 1:
                ref = self.get_author_ref(author)
                # Remove any references that do not have a qualification mapped to it
                ref = list(set(ref).intersection(set(qualification.keys())))
            else:
                ref = '0'

            first_name_sanitized = self.sanitize(first_name)
            last_name_sanitized = self.sanitize(last_name)
            uni = self.get_uni_SCOPUS_field(qualification, ref)

            qualifications = self.get_qualifications_string(qualification, ref)

            # noinspection PyPep8
            if uni is not None:
                uni_ = self.sanitize(uni)
                # noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,PyPep8,PyPep8,PyPep8,PyPep8
                link = f'https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al&affilName={uni_}&sid=3356f44acd1842874e123cc86b8004b0&sot=al&sdt=al&sl=88&s=AUTHLASTNAME%28{last_name_sanitized}%29+AND+AUTHFIRST%28{first_name_sanitized}%29+AND+AFFIL%28{uni_}%29&st1={last_name_sanitized}&st2={first_name_sanitized}'
            else:
                # noinspection SpellCheckingInspection,PyPep8
                link = f'https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al&sid=77ff2eb1a3f81dea6930fea81b3366ee&sot=al&sdt=al&sl=43&s=AUTHLASTNAME%28{last_name_sanitized}%29+AND+AUTHFIRST%28{first_name_sanitized}%29&st1={last_name_sanitized}&st2={first_name_sanitized}'

            yield {'First Name': first_name, 'Last Name': last_name,
                   'Qualifications': qualifications, 'Link': link}


    @staticmethod
    def sanitize(text):
        """ Convert UTF-8 text to URL friendly string. """

        data = '+'.join(quote(x) for x in text.split())
        return data

    @staticmethod
    def get_uni_SCOPUS_field(qualification, ref):
        """ Check through all qualifications and return with university term
        for the SCOPUS query. """

        for term in ref:
            text = qualification[term]
            data = text.split(',')
            for segment in data:
                if segment.find('University') > 0:
                    return segment

    @staticmethod
    def get_author_ref(author):
        """ Get references of author to link to appropriate university. """

        res = set()
        for val in author.xpath('span/span[@class="author-ref"]/sup/text()').extract():
            res.add(val)
        for val in author.xpath('span/span[@class="author-ref"]/text()').extract():
            res.add(val)

        return list(res)

    @staticmethod
    def get_qualifications_string(qualification, ref):
        """ Return string with all qualifications. """

        out = ''
        for term in ref:
            out = out + qualification[term] + '; '
        return out[:-2]
