# FLASK-SQLALCHEMY DATABASE CONFIG
class Config(object):
    db_name = 'articles.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_name
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'  # Log session info to a file
    DEBUG = True
