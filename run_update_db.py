import sqlite3
from sqlite3 import Error
from news import request_headlines


def create_connection(db_file):
    """ Create a db connection to an SQLite db """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        
    return conn


def insert_article(conn, article):
    """ 
    Insert a new article into the articles table 
    :param conn:
    :param article: tuple
    """
    sql = ''' INSERT INTO articles(category, author, title, description, source, publish_date, url, url_to_image)
              VALUES(?, ?, ?, ?, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, article)
    conn.commit()
    return cur.lastrowid


def clear_table(conn):
    """ Delete all rows in the articles table """
    sql = ''' DELETE FROM articles '''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    
    
def update_article(article):
    list_article = list(article)
    title = list_article[2]
    publish_date = list_article[5]
    
    # Remove src from end of title
    src_index = title.rfind(' - ')
    new_title = title[:src_index]
    
    # Remove info from end of publish_date
    time_index = publish_date.rfind('T')
    new_date = publish_date[:time_index]
    
    list_article[2] = new_title
    list_article[5] = new_date
    article = tuple(list_article)
    
    return article


def main():
    database = "articles.db"
    categories = ["general", "health", "science", "entertainment", "technology", "business", "sports"]
    
    # Create a db connection
    conn = create_connection(database)
    with conn:
        # Clear articles table
        clear_table(conn)
        
        # Retrieve new articles
        for category in categories:
            articles = request_headlines(category)
            for article in articles:
                article = update_article(article)
                article_id = insert_article(conn, article)
        

if __name__ == '__main__':
    main()