_author_ = 'arichland'
import pydict
import pymysql

class CreateTable:
    # Creates tables for SQL database

    def __init__(self):
        self.dict = pydict.sql.get
        self.user = self.dict('user')
        self.password = self.dict('password')
        self.host = self.dict('host')
        self.db = self.dict('db_linkedin')

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

def migrate():

        con1 = pymysql.connect(user=pydict.user, password=pydict.password, host=pydict.host, database=pydict.database)
        dict2 = pydict.sql.get
        user = dict2('user')
        password = dict2('password')
        host = dict2('host')
        db = dict2('db_linkedin')

        with con1.cursor() as cur1:
            query = """
                SELECT
                LastPostUTC,
                ImportDate,
                Title,
                Descr,
                URL,
                Status,
                Source,
                Category
                FROM tbl_Posts;"""
            cur1.execute(query)
            rows = cur1.fetchall()

            for row in rows:
                print(row)
                con2 = pymysql.connect(user=user, password=password, host=host, database=db)
                with con2.cursor() as cur2:
                    query2 = """
                       INSERT INTO tbl_Posts(
                       LastPostUTC,
                       ImportDate,
                       Title,
                       Descr,
                       URL,
                       Status,
                       Source,
                       Category)
                       VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"""
                    cur2.execute(query2, (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
                    con2.commit()
                con2.close()

            con1.commit()
        cur1.close()

#ct = CreateTable()
#ct.tbl_posts()

migrate()
