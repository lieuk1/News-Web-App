from flask_sqlalchemy import SQLAlchemy

# DATABASE
db = SQLAlchemy()

# ARTICLE DATABASE MODEL
class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    author = db.Column(db.String(100))
    title = db.Column(db.String(500))
    description = db.Column(db.String(500))
    source = db.Column(db.String(100))
    publish_date = db.Column(db.String(20))
    url = db.Column(db.String(500))
    url_to_image = db.Column(db.String(500))

    def __init__(self, category, author, title, description, source, publish_date, url, url_to_image):
        self.category = category
        self.author = author
        self.title = title
        self.description = description
        self.source = source
        self.publish_date = publish_date
        self.url = url
        self.url_to_image = url_to_image