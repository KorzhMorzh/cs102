import requests
from typing import Union
from bs4 import BeautifulSoup


def extract_news(url):
    response = get_page(url)
    page = BeautifulSoup(response, 'html5lib')
    news = {
        'author': page.find('span', attrs={'itemprop': 'name'}).get_text(),
        'comments': page.find('a', attrs={'class': "share-comments"}).get_text(),
        'title': page.find('h1', attrs={'itemprop': 'headline'}).get_text(),
        'url': url
    }
    return news


def extract_next_page(url, n_page) -> Union[list, str]:
    url += '/news/page{n}'.format(
        n=n_page
    )
    response = get_page(url)
    page = BeautifulSoup(response, 'html5lib')
    links_list = []
    for link in page.find_all('a', attrs={'class': 'row collapse article-list-container'}):
        links_list.append(link.get('href'))
    return links_list


def get_page(url):
    response = requests.get(url)
    return response.text


def get_news(url, n_pages):
    news_list = []
    links_list = []
    q = 0
    for i in range(1, n_pages + 1):
        links_list.append(extract_next_page(url, i))
        print("Extracted page ", i)
    news_list = [
        extract_news(f"{url}/{news}")
        for links in links_list
        for news in links
    ]
    return news_list
