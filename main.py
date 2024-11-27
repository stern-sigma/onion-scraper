import requests
from requests import HTTPError
from datetime import datetime
from bs4 import BeautifulSoup
from time import sleep

def get_article_details(url: str) -> dict:
    response = requests.get(url)
    if response.status_code >= 400:
        raise requests.HTTPError(response=response)
    parse_data = BeautifulSoup(response.text, features="html.parser")

    title = parse_data.find('h1').get_text()

    published_raw = parse_data.find('time')['datetime']
    published = datetime.fromisoformat(published_raw)

    tag_div = parse_data.find("div", class_="taxonomy-post_tag")
    if tag_div:
        tags = tag_div.find_all('a')
        tag_list = [x.text for x in tags]
    else:
        tag_list = []

    return {
        "title": title,
        "published": published,
        "tags": tag_list
    }


def get_articles_from_page(url: str) -> list[dict]:
    response = requests.get(url)
    if response.status_code >= 400:
        raise requests.HTTPError(response=response)
    parse_data = BeautifulSoup(response.text, features="html.parser")
    links_raw = parse_data.find_all('h3')
    articles = []
    for l in links_raw:
        try: 
            articles.append(get_article_details(l.find('a')['href']))
        except Exception as e:
            print('something went wrong')
            print(l)
            print(e)
            continue
    return articles


if __name__ == "__main__":
    data = get_articles_from_page(
        'https://theonion.com/')
    # data = get_article_details(
    #    ' https://theonion.com/stephen-nedoroscik-under-fire-after-video-shows-him-whi-1851616068rev1723128732701/'
    # )
    print(data)