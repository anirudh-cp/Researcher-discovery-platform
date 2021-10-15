from workbook import WorkBook
from scraper import *


def main():
    term = input('Enter search term : ').split()
    # term = ['Apple', 'ice']

    work_book = WorkBook(encoding='utf-8')
    work_book.add_sheet('Results', ['Title', 'URL'])

    results, sci_dir = scrape_scholar(term)

    for index, term in enumerate(results):
        work_book.sheet['Results'].write_line(index+1, term)

    work_book.add_sheet('People', ['First Name', 'Last Name',
                                   'Qualification', 'URL'])

    for res in sci_dir:
        print(res)

    line = 1
    for res in sci_dir:
        people = scrape_sci_dir(res[1])
        for person in people:
            print(person)
            work_book.sheet['People'].write_line(line, person)
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


'''
if __name__ == '__main__':
    main()
'''
