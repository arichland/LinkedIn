_author_ = 'arichland'

_author_ = 'arichland'

import pymysql.cursors
import pydict
import urllib.request
import json
from datetime import date

today = date.today().isoformat()

con = pymysql.connect(user=pydict.user,
                       password=pydict.password,
                       host=pydict.host,
                       database=pydict.database,
                       charset=pydict.charset)

def news():
    api_dict = {1: {'url': 'https://newsapi.org/v2/top-headlines?country=us&apiKey=0357d10115194ff1aa94dabd36d62265&category=health', 'tag': ' #health'},
                2: {'url': "https://newsapi.org/v2/top-headlines?country=us&apiKey=0357d10115194ff1aa94dabd36d62265&category=business", 'tag': ' #business'},
                3: {'url': 'https://newsapi.org/v2/top-headlines?country=us&apiKey=0357d10115194ff1aa94dabd36d62265&category=technology', 'tag': ' #technology'},
                4: {'url': 'https://newsapi.org/v2/top-headlines?country=us&apiKey=0357d10115194ff1aa94dabd36d62265&category=science', 'tag': ' #science'},
                5: {'url': 'https://newsapi.org/v2/top-headlines?apiKey=0357d10115194ff1aa94dabd36d62265&sources=techcrunch', 'tag': ' @techcrunch'},
                6: {'url': 'https://newsapi.org/v2/top-headlines?apiKey=0357d10115194ff1aa94dabd36d62265&sources=the-wall-street-journal', 'tag': ' @wsj'},
                7: {'url': 'https://newsapi.org/v2/top-headlines?apiKey=0357d10115194ff1aa94dabd36d62265&sources=wired', 'tag': ' @wired'}}
    today = date.today().isoformat()
    con = pymysql.connect(user=pydict.user,
                       password=pydict.password,
                       host=pydict.host,
                       database=pydict.database,
                       charset=pydict.charset)

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
        'EventHubs'
    ]

    for key, value in api_dict.items():
        tag = value['tag']
        api_url = value['url']
        response = urllib.request.urlopen(api_url).read()
        data = json.loads(response)
        news = data["articles"]

        for i in news:
            source = i['source']['name']
            url = i['url']
            descr = i['description']
            title = i['title']
            insert_qry = "Insert into tbl_Posts(ImportDate, Status, Title, Descr, URL, Category, Source) Values(Now(), 'Available', %s, %s, %s, %s, %s);"
            try:
                with con.cursor() as cur:
                    cur.execute(insert_qry, (title, descr, url, tag, source))
            finally:
                con.commit()

    for i in delete_list:
            delete_qry = "Delete FROM rtcaws01.tbl_Posts where Source = %s;"
            try:
                with con.cursor() as cur:
                    cur.execute(delete_qry, i)
            finally:
                con.commit()

    update_qry = "Update rtcaws01.tbl_Posts Set Title = CONCAT(Title, Category) Where Category Is NOT Null;"
    try:
        with con.cursor() as cur:
                    cur.execute(update_qry)
    finally:
          con.commit()
news()