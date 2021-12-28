_author_ = 'arichland'

import urllib.request
import json
import Credentials
import pprint
pp = pprint.PrettyPrinter(indent=1)
class News:
    def __init__(self):
        self.user = Credentials.sql_user
        self.password = Credentials.sql_password
        self.host = Credentials.sql_host
        self.db = Credentials.sql_database
        self.key = Credentials.api_key

    def get_news(self):
        data = []
        api_dict = {
            1: {'url': 'https://newsapi.org/v2/top-headlines?language=en&category=business&apiKey=%s',
                'tag': ' #business'},
            2: {'url': "https://newsapi.org/v2/top-headlines?language=en&category=health&apiKey=%s",
                'tag': ' #health'},
            3: {'url': 'https://newsapi.org/v2/top-headlines?language=en&category=technology&apiKey=%s',
                'tag': ' #technology'},
            4: {'url': 'https://newsapi.org/v2/top-headlines?language=en&category=science&apiKey=%s',
                'tag': ' #science'}}

        for key, value in api_dict.items():
            tag = value['tag']
            api_url = value['url'] %(self.key)
            response = urllib.request.urlopen(api_url).read()
            response = json.loads(response)
            news = response["articles"]

            for i in news:
                source = i['source']['name']
                url = i['url']
                descr = i['description']
                title = i['title']
                data.append([title, descr, url, tag, source])
        return data

def callAPI():
    go = News()
    return go.get_news()

if __name__ == "__main__":
    callAPI()
