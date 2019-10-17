import requests
import csv
import time
from bs4 import BeautifulSoup as bs

# Here you enter your personal header not to be blocked as bot
headers = {'accept': '*/*',
'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36' }

# URL of HH with the name of vacancy
base_url = 'https://hh.ru/search/vacancy?search_period=3&clusters=true&area=1&text=python&enable_snippets=true'

# The function parses data on pages
def hh_parser_lxml(base_url, headers):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers = headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text) 
            print(count)
            for i in range(count):
                url = f'https://hh.ru/search/vacancy?area=1&search_period=3&text=python&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass

    for url in urls:
        request = session.get(url, headers = headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs = {'data-qa': 'vacancy-serp__vacancy'})
        for div in divs:
            try:
                title = div.find('a', attrs = {'data-qa':'vacancy-serp__vacancy-title'}).text
                _href = div.find('a', attrs = {'data-qa':'vacancy-serp__vacancy-title'})['href']
                company = div.find('a', attrs = {'data-qa':'vacancy-serp__vacancy-employer'}).text
                text1 = div.find('div', attrs = {'data-qa':'vacancy-serp__vacancy_snippet_responsibility'}).text
                text2 = div.find('div', attrs = {'data-qa':'vacancy-serp__vacancy_snippet_requirement'}).text
                content = text1 + ' ' + text2
                jobs.append({
                    'title': title,
                    'company': company,
                    'content': content,
                    'href': _href
                })
            except:
                pass

        print(len(jobs))
    else:
        print('ERROR or done ' + str(request.status_code))
    return jobs

# The function writes data to a file

def files_writer(jobs):

    # You need to select filename  

    with open('parsed_dset.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Название вакансии', 'URL', 'Название компании', 'Описание'))
        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['company'], job['content']))
        
jobs = hh_parser_lxml(base_url, headers)
files_writer(jobs)
