_author_ = 'arichland'

import requests
import pymysql.cursors
import pydict
import pprint
import json
pp = pprint.PrettyPrinter(indent=1)


#MySQL connection fields
con = pymysql.connect(user=pydict.user,
                       password=pydict.password,
                       host=pydict.host,
                       database=pydict.database,
                       charset=pydict.charset)
def code():
    url = pydict.get_oauth_url
    client_id = pydict.client_id
    uri = pydict.redirect_url2
    state = pydict.state
    scope = pydict.scope
    response_type = "code"
    param = {"client_id": client_id,
              "redirect_uri": uri,
              "state": state,
              "scope": scope,
              "response_type": "code"}
    r = requests.get(url, params=param)
    headers = r.headers
    print("Response")
    print(r.next)
    print("\nheaders")
    pp.pprint(headers)

def token():
    url = pydict.post_oauth_url
    client_id = pydict.client_id
    uri = pydict.redirect_url2
    state = pydict.state
    scope = pydict.scope
    key = pydict.client_key
    response_type = "code"
    param = {"grant_type": "authorization_code",
             "redirect_uri": uri,
             "client_id": client_id,
             "client_secret": key,
             "state": state,
             "Content-Type": "x-www-form-urlencoded",
             "code": "code"}
    r = requests.post(url, params=param)
    headers = r.headers
    print("Response")
    print(r.text)
    print("\nheaders")
    pp.pprint(headers)
code()