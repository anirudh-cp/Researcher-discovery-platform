import requests
import lxml
from bs4 import BeautifulSoup

import xlwt as wb

import re
from urllib.parse import quote


def scrape_scholar(term):
    term = '+'.join(x for x in term)
    print(term)
    url = f'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5' \
          f'&q={term}&btnG=&oq=app'
    print(url)

    headers_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}

    req = requests.get(url, headers=headers_)
    soup = BeautifulSoup(req.content, 'lxml')

    records_page = soup.find("div", {"id": "gs_res_ccl_mid"})
    records = records_page.find_all("div", {"class": "gs_r gs_or gs_scl"})

    results = []
    sci_dir = []

    for record_wrapper in records:
        record = record_wrapper.find("div", {"class": "gs_ri"})

        title_heading = record.find("h3", {"class": "gs_rt"})
        title_data = title_heading.find("a")
        title = title_data.get_text(strip=True)
        record_url = title_data['href']

        results.append([title, record_url])
        if record_url.split('.')[1] == 'sciencedirect':
            sci_dir.append([title, record_url])

    return results, sci_dir


def sanitize(text):
    data = '+'.join(quote(x) for x in text.split())
    return data


def get_uni(text):
    data = text.split(',')
    for term in data:
        if term.find('University') > 0:
            return term


def scrape_sci_dir(url):
    headers_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}

    req = requests.get(url, headers=headers_)
    soup = BeautifulSoup(req.content, 'lxml')

    script = soup.find('script', {"type":"application/json"})
    script = str(script)
    pattern = r"\{\"#name\":\"label\",\"_\":\"\w\"\},\{\"#name\":\"textfn\",\"_\":\"[\w*\s*,*]*\"\}"
    data_full = re.findall(pattern, script, re.M)

    qualification = {}
    for term in data_full:
        data = term.split('},{')
        qualification[data[0].split(':')[-1].replace('"','')] = \
            data[1].split(':')[-1].replace('"','').replace('}', '')

    #print(qualification)

    author_group = soup.find("div", {"class": "AuthorGroups text-xs"})

    author_details = author_group.find_all("a", {"class": "author size-m "
                                                          "workspace-trigger"})
    results = []

    for author in author_details:
        given_name = author.find("span", {"class": "text given-name"}).\
            get_text(strip=True)
        surname = author.find("span", {"class": "text surname"}).\
            get_text(strip=True)
        ref = author.find("span", {"class": "author-ref"}).get_text(strip=True)

        surname_ = sanitize(surname)
        given_name_ = sanitize(given_name)
        uni = get_uni(qualification[ref])
        uni_ = sanitize(uni)

        url = f'https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al&affilName={uni_}&sid=3356f44acd1842874e123cc86b8004b0&sot=al&sdt=al&sl=88&s=AUTHLASTNAME%28{surname_}%29+AND+AUTHFIRST%28{given_name_}%29+AND+AFFIL%28{uni_}%29&st1={surname_}&st2={given_name_}'

        results.append([given_name, surname, qualification[ref], url])

    return results


def main():
    '''
    term = input('Enter search term : ').split()
    # term = ['Apple', 'ice']

    work_book = wb.Workbook(encoding='utf-8')
    table = work_book.add_sheet('Results')
    table.write(0, 0, 'Title')
    table.write(0, 1, 'URL')
    line = 1

    results, sci_dir = scrape_scholar(term)

    for x in results:
        table.write(line, 0, x[0])
        table.write(line, 1, x[1])
        line += 1

    table = work_book.add_sheet('People')
    table.write(0, 0, 'First Name')
    table.write(0, 1, 'Last Name')
    table.write(0, 2, 'Search Link')
    line = 1

    for res in sci_dir:
        people = scrape_sci_dir(res[1])
        for person in people:
            table.write(line, 0, person[0])
            table.write(line, 1, person[1])
            table.write(line, 2, person[2])
            line += 1

    work_book.save('Results.xls')
    '''

    people = scrape_sci_dir('https://www.sciencedirect.com/science/article/pii/S0260877420303605')

    for a in people:
        print(a)


if __name__ == '__main__':
    main()
