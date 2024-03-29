import json

from flask import Flask, request, make_response

from toutiao.essearcher import ESSearcher
from flask_cors import CORS, cross_origin

app = Flask(__name__)



@app.route('/search', methods=['GET'])
@cross_origin()
def search():
    # keywords = request.args.get('keywords')
    # result = ESSearcher().query(keywords).raw
    # return json.dumps(result, ensure_ascii=False), 200, {'Content-Type': 'application/json'}
    result = [{'id': 1, 'title': 'title 1', 'url': 'https://toutiao.com/1'},
              {'id': 2, 'title': 'title 2', 'url': 'https://toutiao.com/2'}]
    return result


if __name__ == '__main__':
    app.run(debug=True)
