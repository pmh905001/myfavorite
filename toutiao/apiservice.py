import json

from flask import Flask, request, make_response

from toutiao.essearcher import ESSearcher

app = Flask(__name__)


@app.route('/search', methods=['GET'])
def search():
    # keywords = request.args.get('keywords')
    # result = ESSearcher().query(keywords).raw
    # return json.dumps(result, ensure_ascii=False), 200, {'Content-Type': 'application/json'}
    result = [{'id': 1, 'title': 'title 1', 'url': 'https://toutiao.com/1'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 3, 'title': 'title 3', 'url': 'https://toutiao.com/3'},
              {'id': 4, 'title': 'title 4', 'url': 'https://toutiao.com/4'},
              {'id': 5, 'title': 'title 5', 'url': 'https://toutiao.com/5'},
              {'id': 6, 'title': 'title 6', 'url': 'https://toutiao.com/6'},
              {'id': 7, 'title': 'title 7', 'url': 'https://toutiao.com/7'},
              {'id': 8, 'title': 'title 8', 'url': 'https://toutiao.com/8'},
              {'id': 9, 'title': 'title 9', 'url': 'https://toutiao.com/9'},
              {'id': 10, 'title': 'title 10', 'url': 'https://toutiao.com/10'},
              ]
    # return json.dumps(result), 200, {'Content-Type': 'application/json'}

    resp = make_response(result)
    resp.status = '200'
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp


if __name__ == '__main__':
    app.run(debug=True)
