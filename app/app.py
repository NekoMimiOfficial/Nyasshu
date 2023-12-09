from logging import debug
import requests
import sqlite3
import pickle
import re
from NekoMimi import utils as nm
from flask import Flask, request, render_template

DB = "cacheDB.db"
DEBUG_DIR = "debug/"
INDEX_TEMPLATE = "index.html"
BASE_TEMPLATE = "base.html"
SSL_FAIL_TEMPLATE = "fail.html"
URI_ERROR_TEMPLATE = "uri_e.html"

conn = sqlite3.connect(DB, check_same_thread=False)
cursor = conn.cursor()
app = Flask(__name__)

#db init
cursor.execute('CREATE TABLE IF NOT EXISTS request_data (id INTEGER PRIMARY KEY AUTOINCREMENT, data BLOB, site TEXT)')
conn.commit()
#end init

def store_b(data, site):
    cursor.execute('INSERT INTO request_data (data, site) VALUES (?, ?)', (data, site))
    conn.commit()

def get_b():
    cursor.execute('SELECT * FROM request_data')
    rows = cursor.fetchall()
    request_list = rows
    return request_list

class objectStore:
    def __init__(self, url) -> None:
        self.url = url
        self.res = None
        self.text = render_template(SSL_FAIL_TEMPLATE)

    def cache(self):
        req = requests.get(self.url)
        self.res = req
        s = self.url
        d = pickle.dumps(req)
        store_b(d, s)
        return req


def worker(url):
    if not url.startswith('http'):
        class uriError:
            content = render_template(URI_ERROR_TEMPLATE)
        res = uriError()
        return res.content
    print("getting status...")
    status = nm.isUp(url)
    print(status)
    db = get_b()
    for entry in db:
        if url in entry[2]:
            data = entry[1]
            response = pickle.loads(data)
            return response.text
    
    factory = objectStore(url)
    if status > 199 and status < 300:
        res_c = factory.cache()
        return res_c.text
    return factory.text

@app.route("/")
def _index():
    return render_template(INDEX_TEMPLATE)

@app.route("/cache", methods=['GET'])
def _cache():
    get_site = request.args.get('site')
    print(site)
    content = worker(get_site)
    b_data = nm.isUp(get_site)
    if b_data == 0:
        b_data = "Down"
    nm.write(content, f"{DEBUG_DIR}last_site.html")
    return render_template(BASE_TEMPLATE, **{'content':content, 'bar':b_data})

if __name__ == "__main__":
    site = "https://core.telegram.org/bots/api"
    app.run(port=8888, debug=True)
    # db = get_b()
    # for entry in db:
    #     if site in entry[2]:
    #         wd = entry[1]
    #         res = pickle.loads(wd)
    #         cont = res.text
    #         urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(/[^\s]*)?',  cont)
    #         print(urls)
