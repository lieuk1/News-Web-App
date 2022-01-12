# FLASK-SQLALCHEMY DATABASE CONFIG
class Config(object):
    db_name = 'articles.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_name
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'  # Log session info to a file
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    SECRET_KEY = '\xaf\x0c7*\xcb\x0e\x8f\xc7M9Q\x9b\x83\r\xbe\xec\xe4\xbe\xfc\xd1\xfd\xe4YT'
