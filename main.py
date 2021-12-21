from workbook import WorkBook
from scraper import *


def main():
    search_terms = input('Enter search term : ').split()
    # term = ['Apple', 'ice']

    work_book = WorkBook(encoding='utf-8')

    # ----------------------------------------
    # Google Scholar and Science Direct

    # Create page for Google Scholar results
    work_book.add_sheet('Google Scholar Source', ['Title', 'URL'])
    # Scrape Google Scholar
    results, sci_dir = scrape_scholar(search_terms)

    # Add results to page
    for index, term in enumerate(results):
        work_book.sheet['Google Scholar Source'].write_line(index + 1, term)

    # Create page for Science Direct From Scholar
    work_book.add_sheet('Science Direct From Scholar', ['First Name',
                                                        'Last Name',
                                                        'Qualification',
                                                        'URL'])
    # For every paper scraped, get author details and add them in
    line = 1
    for res in sci_dir:
        people = scrape_sci_dir_page(res[1])
        for person in people:
            print(person)
            work_book.sheet['Science Direct From Scholar'].write_line(line,
                                                                      person)
            line += 1

    # ----------------------------------------
    # Science Direct

    # Scrape Science Direct search results.
    results = scrape_sci_dir_source(search_terms)

    # Create new page
    work_book.add_sheet('Science Direct', ['First Name', 'Last Name',
                                           'Qualification', 'URL'])
    # For every paper scraped, get author details and add them in
    line = 1
    for res in results:
        people = scrape_sci_dir_page(res[1])
        for person in people:
            print(person)
            work_book.sheet['Science Direct'].write_line(line, person)
            line += 1

    # ----------------------------------------
    # ACM

    # Scrape ACM search result page
    results = scrape_ACM_source(search_terms)
    # Create new sheet
    work_book.add_sheet('ACM', ['First Name', 'Last Name',
                                'Qualification', 'URL'])
    # For every paper scraped, get author details and add them in
    line = 1
    for url in results:
        title, people = scrape_ACM_page(url[0])
        # print(title)
        for person in people:
            # print(person)
            work_book.sheet['ACM'].write_line(line, person)
            line += 1

    # Save workbook
    work_book.save('Results.xls')


def main_process(term):
    term = term.split()
    # term = ['Apple', 'ice']

    results, sci_dir = scrape_scholar(term)

    data = []
    for res in sci_dir:
        people = scrape_sci_dir_page(res[1])
        for person in people:
            data.append(person)

    return data


def main_():
    # term = input('Enter search term : ').split()
    term = ['machine', 'learning']
    results = scrape_ACM_source(term)
    for url in results:
        title, people = scrape_ACM_page(url[0])
        print(title)
        for person in people:
            print(person)


if __name__ == '__main__':
    main()
