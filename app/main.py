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
