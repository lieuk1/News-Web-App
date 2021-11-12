from flask import request, session
import math
from config import RESULTS_PER_PAGE  # config.py
from database import db, Article  # database.py
from news import get_top, get_everything, get_headline_info  # news.py


# INSERT ARTICLES INTO DATABASE
def insert_headlines(user_choice, article_tuple):
    for title, description, source, date, url in article_tuple:
        if user_choice == 'top':
            # Remove source from end of title
            hyphen_index = title.rfind(' - ')
            title = title[:hyphen_index]

        # Remove info from end of date
        time_index = date.rfind('T')
        date = date[:time_index]

        article = Article(title, description, source, date, url)
        db.session.add(article)

    db.session.commit()


# REQUEST ARTICLES FROM NEWS API
def request_headlines():
    # Clear all data in database for new search
    Article.query.delete()
    db.session.commit()

    if request.form['submit'] == 'Search Trending':
        session['user_choice'] = 'top'

        session['keyword'] = request.form['keyword']
        # session['country'] = request.form['country']
        session['category'] = request.form['category']

        # Get article data from News API
        # top_headlines = get_top(session['keyword'], session['country'], session['category'])
        top_headlines = get_top(session['keyword'], session['category'])
        article_tuple = get_headline_info(top_headlines)
        session['total_results'] = top_headlines['totalResults']

        insert_headlines(session['user_choice'], article_tuple)

    if request.form['submit'] == 'Search Everything':
        session['user_choice'] = 'all'

        session['keyword'] = request.form['keyword']
        # session['language'] = request.form['language']
        session['sortby'] = request.form['sortby']

        # Get article data from News API
        all_articles = get_everything(session['keyword'], session['sortby'])
        article_tuple = get_headline_info(all_articles)
        session['total_results'] = all_articles['totalResults']

        insert_headlines(session['user_choice'], article_tuple)

    if session['keyword'] == '':
        session['keyword'] = 'none'
    if session['total_results'] > 100:  # News API allows 100 max results for developers
        session['total_results'] = 100

    # Calculate last page number
    session['last_page'] = math.ceil(session['total_results'] / RESULTS_PER_PAGE)
