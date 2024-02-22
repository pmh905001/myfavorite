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
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'},
              ]
    # return json.dumps(result), 200, {'Content-Type': 'application/json'}

    resp = make_response(result)
    resp.status = '200'
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp


if __name__ == '__main__':
    app.run(debug=True)
