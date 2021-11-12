"""
KRISTELLA LIEU
9 JUNE 2021
"""

from flask import Flask, render_template, request, url_for, redirect, session
from flask_session import Session

from database import db, Article  # database.py
from dbconfig import Config  # dbconfig.py
from countries_languages import list_countries, list_languages  # countries_languages.py
from headline_helpers import request_headlines  # headline_helpers.py
from config import RESULTS_PER_PAGE  # config.py

app = Flask(__name__)
app.config.from_object(Config)
db.app = app
db.init_app(app)

Session(app)


"""
more user options
Put JS in separate file
search query info reveal on button click
remove bottom nav, sticky top nav
"""


@app.route("/test")
def home():
    countries = list_countries()
    languages = list_languages()

    session.pop('user_choice', None)

    return render_template("test.html",
                           title='Worldwide News Headlines',
                           countries=countries,
                           languages=languages)


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/headlines", methods=['GET', 'POST'], defaults={'page': 1})
@app.route("/headlines/<int:page>", methods=['GET', 'POST'])
def headlines(page):
    # Get data from News API if NOT paginating
    if request.method == 'POST':
        request_headlines()

    if session.get('user_choice') is not None:
        article_data = Article.query.paginate(page, RESULTS_PER_PAGE, False)

        if article_data.has_next:
            next_url = url_for('headlines', page=article_data.next_num)
        else:
            next_url = None
        if article_data.has_prev:
            prev_url = url_for('headlines', page=article_data.prev_num)
        else:
            prev_url = None

        if session['user_choice'] == 'top':
            return render_template("headlines.html",
                                   title='Trending and Breaking News',
                                   user_choice=session['user_choice'],
                                   article_data=article_data,
                                   next_url=next_url,
                                   prev_url=prev_url,
                                   page=page,
                                   last_page=session['last_page'],
                                   total_results=session['total_results'],
                                   keyword=session['keyword'],
                                   category=session['category'])
        elif session['user_choice'] == 'all':
            return render_template("headlines.html",
                                   title='Everything You Need',
                                   user_choice=session['user_choice'],
                                   article_data=article_data,
                                   next_url=next_url,
                                   prev_url=prev_url,
                                   page=page,
                                   last_page=session['last_page'],
                                   total_results=session['total_results'],
                                   keyword=session['keyword'],
                                   sortby=session['sortby'])

    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    db.create_all()
    app.run()
