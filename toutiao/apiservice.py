import json
from threading import Thread

from flask import Flask, request, make_response, render_template
from flask_socketio import SocketIO

from essearcher import ESSearcher
from flask_cors import CORS, cross_origin




app = Flask(__name__, template_folder='../views')

socketio = SocketIO(app,cors_allowed_origins="*")

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
    
    # from flask_socketio import send
    # send(f'has more at-------------------------------------')
    # print("--------------------------------------------------------------send")
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
    

# @app.before_first_request
def start_background_task():
    from main_flow import start_backend_to_fetch_data
    thread = Thread(target=start_backend_to_fetch_data)
    thread.daemon = True
    thread.start()    
    

@app.route('/myfavs', methods=['GET'])
def myfavs():
    return render_template('myfavs.html')
    # return "Hello"


def run_app():
    app.jinja_env.variable_start_string = '[['
    app.jinja_env.variable_end_string = ']]'
    # app.run(debug=True)
    socketio.run(app, debug=True)


if __name__ == '__main__':
    start_background_task()
    run_app()