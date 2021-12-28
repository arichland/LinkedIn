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

def main():
    go = CreateSQLTable()
    go.tbl_posts()

if __name__ == "__main__":
    main()
