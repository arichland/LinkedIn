_author_ = 'arichland'
import pymysql
import Credentials

class CreateSQLTable:
    # Creates tables for SQL database
    def __init__(self):
        self.user = Credentials.sql_user
        self.password = Credentials.sql_password
        self.host = Credentials.sql_host
        self.db = Credentials.sql_database

    def tbl_posts(self):
        con = pymysql.connect(user=self.user, password=self.password, host=self.host, database=self.db)
        with con.cursor() as cur:
            query = """CREATE TABLE IF NOT EXISTS tbl_Posts(
                id INT AUTO_INCREMENT PRIMARY KEY,
                LastPostUTC DATETIME,
                ImportDate DATETIME,
                Title TEXT,
                Descr TEXT,
                URL TEXT,
                Status TEXT,
                Source VARCHAR(45),
                Category VARCHAR(45)
                )
                ENGINE=INNODB;"""
            cur.execute(query)
            con.commit()
        cur.close()
        con.close()

    def post_view(self):
        con = pymysql.connect(user=self.user, password=self.password, host=self.host, database=self.db)
        with con.cursor() as cur:
            query = """CREATE OR REPLACE VIEW linkedin.sql_posts AS
            SELECT
                sq1.id,
                sq1.PostEST,
                sq1.Status,
                sq1.Source,
                sq1.Title,
                sq1.Description                
            FROM (SELECT
                id,
                DATE_FORMAT(CONVERT_TZ(LastPostUTC, 'UTC', 'US/Eastern'), '%Y/%m/%d %H:%i') as PostEST,
                Status,
                Source,
                Title,
                Descr AS Description
            FROM tbl_Posts) AS sq1
            ORDER BY PostEST DESC;"""
            cur.execute(query)
            con.commit()
        cur.close()
        con.close()

def main():
    go = CreateSQLTable()
    go.tbl_posts()
    go.post_view()

if __name__ == "__main__":
    main()
