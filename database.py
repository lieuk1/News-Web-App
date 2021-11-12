from flask_sqlalchemy import SQLAlchemy

# DATABASE
db = SQLAlchemy()

# ARTICLE DATABASE MODEL
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    description = db.Column(db.String(500))
    source = db.Column(db.String(100))
    date = db.Column(db.String(20))
    url = db.Column(db.String(500))

    def __init__(self, title, description, source, date, url):
        self.title = title
        self.description = description
        self.source = source
        self.date = date
        self.url = url
