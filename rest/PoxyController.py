import json
import urllib.parse
from os.path import dirname, basename, isfile, join
import client.Register


from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/proxy', methods=['GET'])
def proxy():
    query = request.args.get('q')
    return query, 201

@app.route('/proxy/gencode', methods=['POST'])
def buidQueryCode():
    content = request.json
    jstr = json.dumps(content)
    ans= urllib.parse.quote(jstr)
    return ans, 201


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
