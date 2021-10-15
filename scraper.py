import requests
# import lxml
from bs4 import BeautifulSoup

import re
from urllib.parse import quote


def sanitize(text):
    data = '+'.join(quote(x) for x in text.split())
    return data


def get_uni(qualification, ref):
    for term in ref:
        text = qualification[term]
        data = text.split(',')
        for segment in data:
            if segment.find('University') > 0:
                return segment


def get_ref(author):
    res = []
    for auth in author.find_all("span", {"class": "author-ref"}):
        val = auth.get_text(strip=True)
        if val.isalpha():
            res.append(val)
    return res


def get_qualifications(qualification, ref):
    out = ''
    for term in ref:
        out = out + qualification[term] + '; '
    return out[:-2]


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


# noinspection PyPep8
def scrape_sci_dir(url):
    headers_ = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'}

    req = requests.get(url, headers=headers_)
    soup = BeautifulSoup(req.content, 'lxml')

    script = soup.find('script', {"type": "application/json"})
    script = str(script)

    # noinspection SpellCheckingInspection,PyPep8,PyPep8,PyPep8
    pattern = r"(?:\{\"#name\":\"label\",\"_\":\"\w\"\},)*\{\"#name\":\"textfn\",(?:\"\$\":\{\"id\":\"[\w\d]*\"\},)*\"_\":\"(?:[A-zÀ-ÖØ-öø-įĴ-őŔ-žǍ-ǰǴ-ǵǸ-țȞ-ȟȤ-ȳɃɆ-ɏḀ-ẞƀ-ƓƗ-ƚƝ-ơƤ-ƥƫ-ưƲ-ƶẠ-ỿ]*\s*\.*\d*,*-*&*\(*\)*)*\"\}"
    data_full = re.findall(pattern, script, re.M)
    data_full = set(data_full)

    qualification = {}
    for term in data_full:
        data = term.split('},{')

        if len(data) > 1:
            qualification[data[0].split(':')[-1].replace('"', '')] = \
                data[1].split(':')[-1].replace('"', '').replace('}', '')
        else:
            # noinspection PyPep8
            qualification['0'] = data[0].split(':')[-1].\
                replace('"', '').replace('}', '')

    # print(qualification)

    author_group = soup.find("div", {"class": "AuthorGroups text-xs"})

    author_details = author_group.find_all("a", {"class": "author size-m "
                                                          "workspace-trigger"})
    results = []

    for author in author_details:
        given_name = author.find("span", {"class": "text given-name"}).\
            get_text(strip=True)
        surname = author.find("span", {"class": "text surname"}).\
            get_text(strip=True)

        if len(qualification) > 1:
            ref = get_ref(author)
        else:
            ref = '0'

        surname_ = sanitize(surname)
        given_name_ = sanitize(given_name)
        uni = get_uni(qualification, ref)

        # noinspection PyPep8
        if uni is not None:
            uni_ = sanitize(uni)
            # noinspection SpellCheckingInspection,SpellCheckingInspection,SpellCheckingInspection,PyPep8,PyPep8,PyPep8,PyPep8
            url = f'https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al&affilName={uni_}&sid=3356f44acd1842874e123cc86b8004b0&sot=al&sdt=al&sl=88&s=AUTHLASTNAME%28{surname_}%29+AND+AUTHFIRST%28{given_name_}%29+AND+AFFIL%28{uni_}%29&st1={surname_}&st2={given_name_}'
        else:
            # noinspection SpellCheckingInspection,PyPep8
            url = f'https://www.scopus.com/results/authorNamesList.uri?sort=count-f&src=al&sid=77ff2eb1a3f81dea6930fea81b3366ee&sot=al&sdt=al&sl=43&s=AUTHLASTNAME%28{surname_}%29+AND+AUTHFIRST%28{given_name_}%29&st1={surname_}&st2={given_name_}'

        results.append([given_name, surname,
                        get_qualifications(qualification, ref), url])

    return results