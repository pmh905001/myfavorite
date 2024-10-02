import json

from flask import Flask, request, make_response, render_template

from essearcher import ESSearcher
from flask_cors import CORS, cross_origin


app = Flask(__name__, template_folder='../views')


@app.route('/search', methods=['GET'])
# @cross_origin()
def search():
    keywords = request.args.get('keywords')
    page = int(request.args.get('page', '1'))
    result = ESSearcher().query(keywords, page).raw['hits']['hits']
    
    # result = [x['_source'] for x in result]
    records=[]
    for x in result:
        source =x['_source']
        source["_id"]=x["_id"]
        records.append(source)
        
    # return json.dumps(result, ensure_ascii=False), 200, {'Content-Type': 'application/json'}
    resp = make_response(json.dumps(records, ensure_ascii=False))
    resp.status = '200'
    resp.headers['Access-Control-Allow-Origin'] = "*"
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/remove', methods=['DELETE'])
@cross_origin()
def delete():
    id = request.args.get('_id')
    print(f'--------------------------{id}')
    ESSearcher().delete(id)
    # resp = make_response(json.dumps({}, ensure_ascii=False))
    # resp.status = '200'
    # resp.headers['Access-Control-Allow-Origin'] = "*"
    # resp.headers['Content-Type'] = 'application/json'
    # return resp
    return ""
    
    
    

@app.route('/myfavs', methods=['GET'])
def myfavs():
    return render_template('myfavs.html')
    # return "Hello"


def run_app():
    app.jinja_env.variable_start_string = '[['
    app.jinja_env.variable_end_string = ']]'
    app.run(debug=True)


if __name__ == '__main__':
    run_app()
