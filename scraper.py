"""
Module for Scrapers and associated helper functions.

Available scrapers:
-------------------
scrape_scholar          : Google Scholar    :   Get all title and URL and titles and URL for Science Direct pages.

scrape_sci_dir_source   : Science Direct    :   Get URLs from Science Direct search results.

scrape_sci_dir_page     : Science Direct    :   Get first name, last name, qualifications and SCOPUS query link for each author.

scrape_ACM_source       : ACM               :   Get URLs from ACM search results.

scrape_ACM_page         : ACM               :   Get first name, last name, qualifications and ACM profile link for each author.

TODO: Yet to implement: IEEE, Carnegie Mellon, Dimensions, IITs, NITs, IIITs

"""

# For scrapers
import requests
from bs4 import BeautifulSoup
# import lxml

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selenium_exec


# For helper functions
import re
from urllib.parse import quote
import json


def sanitize(text):
    """ Convert UTF-8 text to URL friendly string. """

    data = '+'.join(quote(x) for x in text.split())
    return data


def get_uni_SCOPUS_field(qualification, ref):
    """ Check through all qualifications and return with university term
    for the SCOPUS query. """

    for term in ref:
        text = qualification[term]
        data = text.split(',')
        for segment in data:
            if segment.find('University') > 0:
                return segment


def get_author_ref(author):
    """ Get references of author to link to appropriate university. """

    res = []
    for auth in author.find_all("span", {"class": "author-ref"}):
        val = auth.get_text(strip=True)
        if val.isalpha():
            res.append(val)
    return res


def get_qualifications_string(qualification, ref):
    """ Return string with all qualifications. """

    out = ''
    for term in ref:
        out = out + qualification[term] + '; '
    return out[:-2]


def scrape_scholar(term):
    """ Scrape through Google Scholar. Return all results and results
    to the Science Direct Website. """

    # Create URL to scrape
    term = '+'.join(x for x in term)
    # print(term)
    url = f'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5' \
          f'&q={term}&btnG=&oq=app'

    # print(url)

    # Impersonate user.
    headers_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}

    # Get data via request
    req = requests.get(url, headers=headers_)
    soup = BeautifulSoup(req.content, 'lxml')

    # Get records page div
    records_page = soup.find("div", {"id": "gs_res_ccl_mid"})
    records = records_page.find_all("div", {"class": "gs_r gs_or gs_scl"})

    results = []
    sci_dir = []

    # Scrape every result in the div and get required data.
    for record_wrapper in records:
        record = record_wrapper.find("div", {"class": "gs_ri"})

        title_heading = record.find("h3", {"class": "gs_rt"})
        title_data = title_heading.find("a")
        title = title_data.get_text(strip=True)
        record_url = title_data['href']

        # Place data in appropriate lists.
        results.append([title, record_url])
        if record_url.split('.')[1] == 'sciencedirect':
            sci_dir.append([title, record_url])

    return results, sci_dir


def scrape_sci_dir_source(term):
    """ Scrape the ACM search results page and returns paper name and URL. """

    # Create URL to scrape.
    term = '+'.join(x for x in term)

    # print(term)

    url = f'https://www.sciencedirect.com/search?qs={term}&lastSelectedFacet=articleTypes&articleTypes=FLA'

    # Use Selenium here as the web page is built with JavaScript.
    # We have to wait for everything to render, hence we use this tool.
    options = webdriver.ChromeOptions()

    '''
    options.add_argument("--headless")
    options.add_argument('--window-size=1920,1080')
    options.add_argument("--allow-insecure-localhost");
    options.add_argument("--disable-gpu");
    options.add_argument("--no-sandbox");
    '''

    # options.add_argument("--headless")
    # options.add_argument("--start-minimized")

    options.add_argument("--headless")
    headers_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'}
    options.add_argument(f"--user-agent={headers_['User-Agent']}")

    driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    # driver.minimize_window()
    # driver.set_window_position(-10000, 0)
    driver.get(url)

    driver.get_screenshot_as_file("screenshot.png")

    # Wait till element is located (maximum 7 seconds)
    try:
        elem = WebDriverWait(driver, 7).until(
            EC.presence_of_element_located((By.ID, "srp-results-list"))
            # This is a dummy element
        )
    except selenium_exec.TimeoutException:
        print('Selenium Timeout Exception in Science Direct Source scraper')
        return
    finally:
        html = driver.page_source
        driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    '''
    # Impersonate user
    headers_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}

    # Get data via request
    req = requests.get(url, headers=headers_)
    soup = BeautifulSoup(req.content, 'lxml')
    '''

    # Find where all records are in the div
    records_page = soup.find("div", {"class": "ResultList col-xs-24"})

    records = records_page.find_all("li", {
        "class": "ResultItem col-xs-24 push-m"})

    results = []

    # Scrape through every record and get the URL alone.
    for record_wrapper in records:
        record = record_wrapper.find("div", {
            "class": "result-item-content"})

        title_heading = record.find("h2").get_text(strip=True)
        title_data = record.find("a")
        record_url = title_data['href']

        results.append([title_heading, 'https://www.sciencedirect.com'
                        + record_url])

    return results


# noinspection PyPep8
def scrape_sci_dir_page(url):
    """ Scrape Science Direct page for first name, last name, qualifications
    and SCOPUS query link for each author. """

    # Impersonate user
    headers_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}

    # Get data via request
    req = requests.get(url, headers=headers_)
    soup = BeautifulSoup(req.content, 'lxml')

    # This part is to map the qualifications to each author.
    # Take the data by parsing the javascript code.

    script = soup.find('script', {"type": "application/json"})
    script = script.get_text(strip=True)

    data = json.loads(script)['authors']['affiliations']

    # Map a reference character to each qualification as shown in the page.
    qualification = {}

    if len(data.keys()) == 1:
        qualification['0'] = list(data.values())[0]['$$'][0]['_']
    else:
        for term in data.values():
            qualification[term['$$'][0]['_']] = term['$$'][1]['_']


    # noinspection SpellCheckingInspection,PyPep8,PyPep8,PyPep8
    #pattern = r"(?:\{\"#name\":\"label\",\"_\":\"\w\"\},)*\{\"#name\":\"textfn\",(?:\"\$\":\{\"id\":\"[\w\d]*\"\},)*\"_\":\"(?:[A-zÀ-ÖØ-öø-įĴ-őŔ-žǍ-ǰǴ-ǵǸ-țȞ-ȟȤ-ȳɃɆ-ɏḀ-ẞƀ-ƓƗ-ƚƝ-ơƤ-ƥƫ-ưƲ-ƶẠ-ỿ]*\s*\.*\d*,*-*&*\(*\)*'*)*\"\}"
    '''
    data_full = re.findall(pattern, script[:30000], re.M)
    data_full = set(data_full)

    # Map a reference character to each qualification as shown in the page.
    qualification = {}
    for term in data_full:
        data = term.split('},{')

        if len(data) > 1:
            qualification[data[0].split(':')[-1].replace('"', '')] = \
                data[1].split(':')[-1].replace('"', '').replace('}', '')
        else:
            # noinspection PyPep8
            qualification['0'] = data[0].split(':')[-1]. \
                replace('"', '').replace('}', '')
    '''

    # Start scraping the author window.
    author_group = soup.find("div", {"class": "AuthorGroups text-xs"})

    author_details = author_group.find_all("a", {"class": "author size-m "
                                                          "workspace-trigger"})
    results = []

    # For every author get details and map qualifications. If any of the
    # qualifications have the term 'university' in them,
    # include in the SCOPUS query.
    for author in author_details:
        try:
            given_name = author.find("span", {"class": "text given-name"}).\
                get_text(strip=True)
        except AttributeError:
            given_name = ''

        try:
            surname = author.find("span", {"class": "text surname"}).\
                get_text(strip=True)
        except AttributeError:
            surname = ''

        if len(qualification) > 1:
            ref = get_author_ref(author)
        else:
            ref = '0'

        surname_ = sanitize(surname)
        given_name_ = sanitize(given_name)
        uni = get_uni_SCOPUS_field(qualification, ref)

        # noinspection PyPep8
        if uni is not None:
            uni_ = sanitize(uni)
            # noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,PyPep8,PyPep8,PyPep8,PyPep8
            url = f'https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al&affilName={uni_}&sid=3356f44acd1842874e123cc86b8004b0&sot=al&sdt=al&sl=88&s=AUTHLASTNAME%28{surname_}%29+AND+AUTHFIRST%28{given_name_}%29+AND+AFFIL%28{uni_}%29&st1={surname_}&st2={given_name_}'
        else:
            # noinspection SpellCheckingInspection,PyPep8
            url = f'https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al&sid=77ff2eb1a3f81dea6930fea81b3366ee&sot=al&sdt=al&sl=43&s=AUTHLASTNAME%28{surname_}%29+AND+AUTHFIRST%28{given_name_}%29&st1={surname_}&st2={given_name_}'

        results.append([given_name, surname,
                        get_qualifications_string(qualification, ref), url])

    return results


def scrape_ACM_source(term):
    """ Scrape the ACM search results page and returns URL. """

    # Create URL to scrape.
    term = '+'.join(x for x in term)
    # print(term)
    url = f'https://dl.acm.org/action/doSearch?AllField={term}&startPage=0&ContentItemType=research-article'

    # print(url)

    # Impersonate user
    headers_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}

    # Get data via request
    req = requests.get(url, headers=headers_)
    soup = BeautifulSoup(req.content, 'lxml')

    # Find where all records are in the div
    records_page = soup.find("div", {"class": "search-result doSearch"})
    records = records_page.find_all("li", {
        "class": "search__item issue-item-container"})

    results = []

    # Scrape through every record and get the URL alone.
    for record_wrapper in records:
        record = record_wrapper.find("div", {
            "class": "issue-item issue-item--search clearfix"})

        title_heading = record.find("span", {"class": "hlFld-Title"})
        title_data = title_heading.find("a")
        record_url = title_data['href']

        results.append(['https://dl.acm.org' + record_url])

    return results


def scrape_ACM_page(url):
    """ Scrape a ACM paper page and get first name, last name,
    qualifications, ACM profile page link. """

    # Impersonate user.
    headers_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}

    # Get data via request.
    req = requests.get(url, headers=headers_)
    soup = BeautifulSoup(req.content, 'lxml')

    # Get title of research paper.
    title = soup.find("h1", {"class": "citation__title"}).get_text(strip=True)

    # Get author details div
    results = []
    authors_wrapper = soup.find("div", {"id": "sb-1"})
    authors = authors_wrapper.find_all("li", {"class": "loa__item"})

    # For every author get the name. Then try for qualifications.
    # If the information paragraph exists, get qualification and URL.
    # If the information paragraph does not exist, get URL alone from
    # hidden box and leave qualifications blank.
    # If the information paragraph exists with no URL, get
    # qualification and set URL to empty string.

    for author in authors:
        name = author.find("a")['title']
        info = author.find("span", {"class": "loa_author_inst"}).find("p")
        try:
            # Try to get info from paragraph tag
            qualification = info.get_text(strip=True)
            url = 'https://dl.acm.org/profile/' + info['data-doi'].split('-')[
                1]
        except AttributeError:
            # If paragraph does not exist, text and url cannot be found directly
            qualification = ''
            url = 'https://dl.acm.org' + \
                  author.find("div", {"class": "author-info__body"}).find("a")[
                      'href']
        except KeyError:
            # Paragraph block does exist, text can be found, url key is missing
            qualification = info.get_text(strip=True)
            url = ''

        try:
            first_name, last_name = name.split(' ', 1)[0], name.split(' ', 1)[
                1]
        except IndexError:
            first_name, last_name = name, ''

        results.append([first_name, last_name, qualification, url])

    return title, results
