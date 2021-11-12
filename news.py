from newsapi import NewsApiClient
newsapi = NewsApiClient(api_key='')

"""
KEYWORD(S) FORMAT -> 'KEYWORD, KEYWORD'
CATEGORY OPTIONS  -> BUSINESS, ENTERTAINMENT, GENERAL, HEALTH, SCIENCE, SPORTS, TECHNOLOGY
PAGE_SIZE (INT)   -> NUMBER OF SOURCES PER PAGE
"""


def get_top(keyword, category):
    top_headlines = newsapi.get_top_headlines(
        q=keyword,
        category=category,
        page_size=100,
        page=1)
    return top_headlines


def get_everything(keyword, sortby):
    all_articles = newsapi.get_everything(
        q=keyword,
        sort_by=sortby,
        page_size=100,
        page=1)
    return all_articles


def get_headline_info(articles):
    titles = []
    descriptions = []
    sources = []
    dates = []
    urls = []

    for article in articles['articles']:
        titles.append(article['title'])
        descriptions.append(article['description'])
        sources.append(article['source']['name'])
        dates.append(article['publishedAt'])
        urls.append(article['url'])

    article_tuple = zip(titles, descriptions, sources, dates, urls)

    return article_tuple
