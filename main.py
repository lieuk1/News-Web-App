"""
KRISTELLA LIEU
9 JUNE 2021
"""

from typing import Optional
from flask import Flask, render_template, request, url_for, redirect, session
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


@app.route("/", methods=['GET', 'POST'], defaults={'page': 1})
def home(page):
    trending_form = TrendingForm()
    article_data = Article.query.filter_by(category="general").paginate(page, 5, False)
    
    if trending_form.validate_on_submit():
        page = request.args.get('page', page, type=int)
        article_data = Article.query.filter_by(category="general").paginate(page, RESULTS_PER_PAGE, False)
        total_results = len(Article.query.all())
        
        return render_template('headlines.html',
            title='News',
            article_data=article_data,
            page=page,
            keyword=trending_form.keyword.data,
            category=trending_form.category.data,
            total_results=total_results)
    return render_template('home.html',
        title='News',
        trending_form=trending_form,
        article_data=article_data)


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
