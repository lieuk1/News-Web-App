"""
KRISTELLA LIEU
9 JUNE 2021
"""

from flask import Flask, render_template, request, jsonify, url_for, redirect, session
from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Optional

from database import db, Article  # database.py
from dbconfig import Config  # dbconfig.py
from countries_languages import list_countries, list_languages  # countries_languages.py
from config import RESULTS_PER_PAGE  # config.py

app = Flask(__name__)
app.config.from_object(Config)
db.app = app
db.init_app(app)
db.create_all()

Session(app)


"""
more user options
Put JS in separate file
search query info reveal on button click
remove bottom nav, sticky top nav
"""

class TrendingForm(FlaskForm):
    keyword = StringField('keyword', validators=[Optional()],
        description={'placeholder': 'Enter keyword (optional)', 'class': 'inputs keyword'})
    category = SelectField('category', validators=[DataRequired()],
        choices=['general', 'business', 'entertainment', 'health', 'science', 'sports', 'technology'],
        description={'class': 'inputs select'})


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    categories = ["general", "health", "science", "entertainment", "technology", "business", "sports"]
    c_h = {}
    for i, c in enumerate(categories):
        c_h.update({c: i})
        
    articles = {}
    
    page = request.args.get('page', 1, type=int)
    text = request.args.get('jsdata')
    
    for c in categories:
        article_section = Article.query.filter_by(category=c).paginate(page, 12, False)
        articles.update({c: article_section})

    return render_template('home.html',
        title='News',
        page=page,
        lenCat=len(categories),
        categories=c_h,
        articles=articles,
        text=text
        )
    

# TODO: ensure that route is only accessible through ajax request
@app.route("/articles", methods=['GET', 'POST'])
def articles():
    page = int(request.args.get('page'))    # Current page number
    category = request.args.get('category') # Current category tab
    
    # Retrieve articles from db
    articles = Article.query.filter_by(category=category).paginate(page, 12, False)
    print(articles.pages)

    return render_template('articles.html',
        page=page,
        c=category,
        articles=articles,
        pages=articles.pages
    )


@app.route('/headlines', methods=['GET', 'POST'])
@app.route('/headlines/<int:page>', methods=['GET', 'POST'])
def headlines(page):
    # Get data from News API if NOT paginating
    # if request.method == 'POST':
        # request_headlines()

    # if session.get('user_choice') is not None:
    # page = request.args.get('page', page, type=int)
    article_data = Article.query.filter_by(category="health").paginate(page, RESULTS_PER_PAGE, False)
    total_results = len(Article.query.all())

    # if session['user_choice'] == 'top':
    return render_template('headlines.html',
                            title='Trending and Breaking News',
                            # user_choice=session['user_choice'],
                            article_data=article_data,
                            page=page,
                            total_results=total_results
                            # keyword=session['keyword'],
                            # category=session['category']
                            )
        # elif session['user_choice'] == 'all':
        #     return render_template('headlines.html',
        #                            title='Everything You Need',
        #                            user_choice=session['user_choice'],
        #                            article_data=article_data,
        #                            page=page,
        #                            total_results=total_results,
        #                            keyword=session['keyword'],
        #                            sortby=session['sortby'])
    # else:
        # return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
