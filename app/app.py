from logging import debug
import requests
import sqlite3
import pickle
from NekoMimi import utils as nm
from flask import Flask, request, render_template

DB = "cacheDB.db"
INDEX_TEMPLATE = "index.html"
BASE_TEMPLATE = "base.html"
SSL_FAIL_TEMPLATE = "fail.html"
URI_ERROR_TEMPLATE = "uri_e.html"

conn = sqlite3.connect(DB)
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
        self.content = render_template(SSL_FAIL_TEMPLATE)

    def cache(self):
        req = requests.get(self.url)
        self.res = req
        s = self.url
        d = pickle.dumps(req)
        store_b(d, s)

    def serve(self):
        db = get_b()
        for entry in db:
            if self.url in entry:
                self.res = entry
            else:
                class error:
                    content = "no find bro"
                self.res = error()

def worker(url):
    if not url.startswith('http'):
        class uriError:
            content = render_template(URI_ERROR_TEMPLATE)
        res = uriError()
        return res.content
    status = nm.isUp(url)
    return status

@app.route("/")
def _index():
    return render_template(INDEX_TEMPLATE)

@app.route("/cache", methods=['GET'])
def _cache():
    get_site = request.args.get('site')
    content = worker(get_site)
    b_data = nm.isUp(get_site)
    return render_template(BASE_TEMPLATE, **{'content':content, 'bar':b_data})

if __name__ == "__main__":
    site = "https://core.telegram.org/bots/api"
    app.run(port=8888, debug=True)
