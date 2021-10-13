import requests
import lxml
from bs4 import BeautifulSoup

import xlwt as wb


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


def scrape_sci_dir(url):
    headers_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}

    req = requests.get(url, headers=headers_)
    soup = BeautifulSoup(req.content, 'lxml')

    author_group = soup.find("div", {"class": "AuthorGroups text-xs"})

    author_details = author_group.find_all("a", {"class": "author size-m "
                                                          "workspace-trigger"})
    results = []

    for author in author_details:
        given_name = author.find("span", {"class": "text given-name"}).\
            get_text(strip=True)
        surname = author.find("span", {"class": "text surname"}).\
            get_text(strip=True)

        surname_ = '+'.join(x for x in surname.split())
        given_name_ = '+'.join(x for x in given_name.split())
        url = f'https://www.scopus.com/results/authorNamesList.uri?sort=' \
              f'count-f&src=al&sid=acfa3b8cd0930cf6959c274e5064754a&sot=' \
              f'al&sdt=al&sl=43&s=AUTHLASTNAME%28{surname_}%29+AND+AUTHFIRST' \
              f'%28{given_name_}%29&st1={surname_}' \
              f'&st2={given_name_}&orcidId=' \
              f'&selectionPageSearch=anl&reselectAuthor=false&activeFlag=' \
              f'true&showDocument=false&resultsPerPage=20&offset=1&jtp=false' \
              f'&currentPage=1&previousSelectionCount=0&tooManySelections' \
              f'=false&previousResultCount=0&authSubject=LFSC&authSubject' \
              f'=HLSC&authSubject=PHSC&authSubject=SOSC&exactAuthorSearch' \
              f'=false&showFullList=false&authorPreferredName=&origin=' \
              f'searchauthorfreelookup'
        results.append([given_name, surname, url])

    return results


def main():
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


if __name__ == '__main__':
    main()
