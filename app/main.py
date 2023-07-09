import pickle
import requests
from os.path import exists
from NekoMimi import utils as nm 
from flask import request, Flask

app = Flask(__name__)

FILE = "dump.pkl"

class dataEnd:
    def __init__(self, url) -> None:
        self.url = url
        self.res = None

    def cache(self):
        buffer = open(FILE, 'wb')
        response = requests.get(self.url)
        pickle.dump(response, buffer)
        buffer.close()
        self.res = response

    def serve(self):
        buffer = open(FILE, 'rb')
        response = pickle.load(buffer)
        self.res = response

def backend(url):
    state = nm.isUp(url)
    if state > 199 and state < 300:
        if exists(FILE):
            m = dataEnd(url)
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

@app.route("/cache", methods=['GET'])
def _server_side():
    site = request.args.get("site")
    return site

app.run(port=8888, debug=False)
print(backend("http://127.0.0.1:8888/cache?site=lol"))
