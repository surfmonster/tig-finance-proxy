import json
import urllib.parse
from os.path import dirname, basename, isfile, join

from urllib.parse import unquote
from flask import Flask
from flask import request

from client import client

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/proxy', methods=['GET'])
def proxy():
    query = request.args.get('q')
    jstr = unquote(query)
    qobj = json.loads(jstr)
    respo = client.proxy(client.QueryDto(**qobj))
    return respo.__dict__, 201


@app.route('/proxy/gencode', methods=['POST'])
def buidQueryCode():
    content = request.json
    jstr = json.dumps(content)
    ans = urllib.parse.quote(jstr)
    return ans, 201


@app.route('/proxy/reimport', methods=['POST'])
def reimport_all():
    content = request.json
    jstr = json.dumps(content)
    ans = urllib.parse.quote(jstr)
    return ans, 201


def get_flask_app():
    return app


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
