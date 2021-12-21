from workbook import WorkBook
from scraper import *


def main():
    term = input('Enter search term : ').split()
    # term = ['Apple', 'ice']

    work_book = WorkBook(encoding='utf-8')

    # Google Scholar
    work_book.add_sheet('Google Scholar Source', ['Title', 'URL'])
    results, sci_dir = scrape_scholar(term)

    for index, term in enumerate(results):
        work_book.sheet['Google Scholar Source'].write_line(index+1, term)

    # ----------------------------------------

    # Science Direct
    work_book.add_sheet('Science Direct', ['First Name', 'Last Name',
                                   'Qualification', 'URL'])

    #for res in sci_dir:
    #    print(res)

    line = 1
    for res in sci_dir:
        people = scrape_sci_dir(res[1])
        for person in people:
            print(person)
            work_book.sheet['Science Direct'].write_line(line, person)
            line += 1

    # ----------------------------------------

    # ACM
    results = scrape_ACM_source(term)
    work_book.add_sheet('ACM', ['First Name', 'Last Name',
                                           'Qualification', 'URL'])

    line = 1
    for url in results:
        title, people = scrape_ACM_page(url[0])
        # print(title)
        for person in people:
            # print(person)
            work_book.sheet['ACM'].write_line(line, person)
            line += 1

    work_book.save('Results.xls')

    # TODO: IEEE and Carnegie Mellon Scraping

    '''
    people = scrape_sci_dir('https://www.sciencedirect.com/science/'
                            'article/abs/pii/S0308814619319661')
    print('out')
    for x in people:
        print(x)
    '''


def main_process(term):
    term = term.split()
    # term = ['Apple', 'ice']

    results, sci_dir = scrape_scholar(term)

    data = []
    for res in sci_dir:
        people = scrape_sci_dir(res[1])
        for person in people:
            data.append(person)

    return data


def main_():
    #term = input('Enter search term : ').split()
    term = ['machine', 'learning']
    results = scrape_ACM_source(term)
    for url in results:
        title, people = scrape_ACM_page(url[0])
        print(title)
        for person in people:
            print(person)


if __name__ == '__main__':
    main()
