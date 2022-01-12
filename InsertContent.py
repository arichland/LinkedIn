_author_ = 'arichland'

import pymysql.cursors
import Credentials
import NewsAPI
import pprint
pp = pprint.PrettyPrinter(indent=1)

class InsertIntoSQL:
    #Retrieve news articles
    def __init__(self):
        self.user = Credentials.sql_user
        self.password = Credentials.sql_password
        self.host = Credentials.sql_host
        self.db = Credentials.sql_database
        self.key = Credentials.api_key
        self.news = NewsAPI.callAPI()

    def content(self):
        con = pymysql.connect(user=self.user, password=self.password, host=self.host, database=self.db)
        data = self.news
        delete_list = [
            'Kotaku',
            'Comicbook.com',
            'Nintendo Life',
            'Siliconera',
            'Gamespot',
            'TechRadar',
            'Engadget',
            'IGN',
            'BuzzFeed News',
            'EventHubs',
            "Independent"
        ]
        try:
            with con.cursor() as cur:
                qry1 = """CREATE TEMPORARY TABLE IF NOT EXISTS temp_posts SELECT * FROM tbl_Posts LIMIT 0;"""
                qry2 = "Insert into temp_posts(Title, Descr, URL, Category, Source) Values(%s, %s, %s, %s, %s);"
                qry3 = "Delete FROM temp_posts WHERE Source = %s;"
                qry4 = """Insert into tbl_Posts (
                                            ImportDate,
                                            Status,
                                            Title,
                                            Descr,
                                            URL,
                                            Category,
                                            Source)
                                        SELECT
                                            NOW() AS ImportDate,
                                            'Available' AS Status,                                            
                                            temp_posts.Title,
                                            temp_posts.Descr,
                                            temp_posts.URL,
                                            temp_posts.Category,
                                            temp_posts.Source
                                        FROM temp_posts
                                        LEFT JOIN tbl_Posts on temp_posts.URL = tbl_Posts.URL
                                        WHERE tbl_Posts.URL IS NULL;
                                        """
                qry5 = "Delete FROM tbl_Posts WHERE datediff(NOW(), ImportDate) > 30;"

                cur.execute(qry1)
                cur.executemany(qry2, data)
                for i in delete_list:
                    cur.execute(qry3, i)
                cur.execute(qry4)
                cur.execute(qry5)
        finally:
            con.commit()
            cur.close()
            con.close()

def sql_insert():
    insert = InsertIntoSQL()
    insert.content()

if __name__ == "__main__":
    sql_insert()
