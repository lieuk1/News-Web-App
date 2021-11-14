from flask import request, session
from database import db, Article  # database.py
from news import get_top, get_everything, get_headline_info  # news.py


# INSERT ARTICLES INTO DATABASE
def insert_headlines(user_choice, article_tuple):
    for author, title, description, source, publish_date, url, url_to_image in article_tuple:
        if user_choice == 'top':
            # Remove source from end of title
            hyphen_index = title.rfind(' - ')
            title = title[:hyphen_index]

        # Remove info from end of publish_date
        time_index = publish_date.rfind('T')
        publish_date = publish_date[:time_index]

        article = Article(author, title, description, source, publish_date, url, url_to_image)
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

        insert_headlines(session['user_choice'], article_tuple)

    if request.form['submit'] == 'Search Everything':
        session['user_choice'] = 'all'

        session['keyword'] = request.form['keyword']
        # session['language'] = request.form['language']
        session['sortby'] = request.form['sortby']

        # Get article data from News API
        all_articles = get_everything(session['keyword'], session['sortby'])
        article_tuple = get_headline_info(all_articles)

        insert_headlines(session['user_choice'], article_tuple)

    if session['keyword'] == '':
        session['keyword'] = 'none'