import requests
# import lxml
from bs4 import BeautifulSoup


def main():
    term = input('Enter search term : ').split()
    # term = ['Apple', 'ice']

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

    for x in results:
        print(x)

    print('-'*80)

    for x in sci_dir:
        print(x)


if __name__ == '__main__':
    main()
