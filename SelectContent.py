_author_ = 'arichland'

import requests
import Credentials
import pymysql.cursors


class Content:
    def __init__(self):
        self.user = Credentials.sql_user
        self.password = Credentials.sql_password
        self.host = Credentials.sql_host
        self.db = Credentials.sql_database

    def select_news_content(self):
        con = pymysql.connect(user=self.user, password=self.password, host=self.host, database=self.db)
        content = []
        with con.cursor() as cur:
            available = 'SELECT sum(case when  status = "Available" then 1 else 0 end) as Available FROM tbl_Posts'
            cur.execute(available)
            rows_available = cur.fetchall()

            for row in rows_available:
                print(f'{row[0]}')
                available_count = row[0]

            if available_count == 0:
                # No more available posts, run update qry to rest all posts
                reset = 'Update tbl_Posts Set Status = "Available";'
                cur.execute(reset)

                # After updating posts, run select qry to find next post
                selectqry = 'Select Min(ID) as ID , LastPostUTC, Status, Title, URL, Descr FROM tbl_Posts where status = "Available"; '
                cur.execute(selectqry)
                rows = cur.fetchall()

                # Assign record fields to variables
                for row in rows:
                    recordID = row[0]

                # Run qry to update MySQL
                updateqry = "Update tbl_Posts set LastPostUTC = Now(), Status = 'Unavailable' where ID = %d" % (recordID)
                cur.execute(updateqry)

                selectqry2 = 'Select ID , LastPostUTC as Timestamp, Status, Title, URL, Descr FROM tbl_Posts where ID = %d' % (recordID)
                cur.execute(selectqry2)
                rows2 = cur.fetchall()

                for row in rows2:
                    c = [row[3], row[4], row[5]]
                    content.append(c)

            else:
                selectqry = 'Select Min(ID) as ID , LastPostUTC, Status, Title, URL, Descr FROM tbl_Posts where status = "Available" '
                cur.execute(selectqry)
                rows = cur.fetchall()

                for row in rows:
                    recordID = row[0]

                    # Run qry to update MySQL
                    updateqry = "Update tbl_Posts set LastPostUTC = Now(), Status = 'Unavailable' where ID = %d" % (recordID)
                    cur.execute(updateqry)
                    selectqry2 = 'Select ID , LastPostUTC as Timestamp, Status, Title, URL, Descr FROM tbl_Posts where ID = %d' % (recordID)
                    cur.execute(selectqry2)
                    rows2 = cur.fetchall()

                    for row in rows2:
                        #print(f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]}')
                        c = [row[3], row[4], row[5]]
                        content.append(c)
                    con.commit()
        cur.close()
        con.close()
        print(content)
        return content

def main():
    go = Content()
    return go.select_news_content()