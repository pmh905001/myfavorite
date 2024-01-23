import json

from flask import Flask, request

from toutiao.essearcher import ESSearcher

app = Flask(__name__)


@app.route('/search', methods=['GET'])
def search():
    keywords = request.args.get('keywords')
    result = ESSearcher().query(keywords).raw
    return json.dumps(result, ensure_ascii=False), 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(debug=True)
