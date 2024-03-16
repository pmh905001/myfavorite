import json

from flask import Flask, request, make_response, render_template

from toutiao.essearcher import ESSearcher

app = Flask(__name__, template_folder='../views')


@app.route('/search', methods=['GET'])
def search():
    keywords = request.args.get('keywords')
    page = int(request.args.get('page', '1'))
    result = ESSearcher().query(keywords, page).raw['hits']['hits']
    result = [x['_source'] for x in result]
    # return json.dumps(result, ensure_ascii=False), 200, {'Content-Type': 'application/json'}
    resp = make_response(json.dumps(result, ensure_ascii=False))
    resp.status = '200'
    resp.headers['Access-Control-Allow-Origin'] = "*"
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/myfavs', methods=['GET'])
def myfavs():
    return render_template('myfavs.html')
    # return "Hello"


if __name__ == '__main__':
    app.jinja_env.variable_start_string = '[['
    app.jinja_env.variable_end_string = ']]'
    app.run(debug=True)
