import os
from newsapi import NewsApiClient
from dotenv import load_dotenv
load_dotenv()

newsapi = NewsApiClient(api_key=os.environ['api_key'])

"""
KEYWORD(S) FORMAT -> 'KEYWORD, KEYWORD'
CATEGORY OPTIONS  -> BUSINESS, ENTERTAINMENT, GENERAL, HEALTH, SCIENCE, SPORTS, TECHNOLOGY
PAGE_SIZE (INT)   -> NUMBER OF SOURCES PER PAGE
"""


def get_top(category):
    top_headlines = newsapi.get_top_headlines(
        category=category,
        page_size=100,
        page=1)
    return top_headlines



def get_headline_info(articles, category):
    categories = []
    authors = []
    titles = []
    descriptions = []
    sources = []
    publish_dates = []
    urls = []
    urls_to_image = []

    for article in articles['articles']:
        categories.append(category)
        authors.append(article['author'])
        titles.append(article['title'])
        descriptions.append(article['description'])
        sources.append(article['source']['name'])
        publish_dates.append(article['publishedAt'])
        urls.append(article['url'])
        urls_to_image.append(article['urlToImage'])

    article_tuple = zip(categories, authors, titles, descriptions, sources, publish_dates, urls, urls_to_image)

    return article_tuple



def request_headlines(category):
    top_headlines = get_top(category)
    article_tuple = get_headline_info(top_headlines, category)
    
    return article_tuple