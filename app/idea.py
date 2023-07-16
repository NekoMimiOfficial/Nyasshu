import os
import time
import pickle
import requests
from os.path import exists
from NekoMimi import utils as nm 
from flask import request, Flask
import multiprocessing as mp

app = Flask(__name__)

FILE = "dump.pkl"

class dataEnd:
    def __init__(self, url) -> None:
        self.url = url
        self.res = None
        self.text = "ph"

    def cache(self):
        if exists(FILE):
            os.remove(FILE)
        buffer = open(FILE, 'wb')
        response = requests.get(self.url)
        pickle.dump(response, buffer)
        buffer.close()
        self.res = response

    def serve(self):
        buffer = open(FILE, 'rb')
        response = pickle.load(buffer)
        self.res = response

def bg_updater(url):
    m = dataEnd(url)
    while True:
        time.sleep(10)
        status = nm.isUp(url)
        if status == 200:
            m.cache()

def backend(url, ov=False):
    state = nm.isUp(url)
    if state > 199 and state < 300:
        if exists(FILE):
            m = dataEnd(url)
            if ov:
                m.cache()
            m.serve()
            return m.res
        else:
            m = dataEnd(url)
            m.cache()
            return m.res

    else:
        if exists(FILE):
            m = dataEnd(url)
            m.serve()
            return m.res
        else:
            m = dataEnd(url)
            m.text = "Fail"
            return m

@app.route("/cache", methods=['GET'])
def _server_side():
    site = request.args.get("site")
    if site.startswith("http"):
        response = backend(site)
        return response.text
    return "Fail"

app.run(port=8888, debug=False)
# print(backend("http://127.0.0.1:8888/cache?site=lol"))
