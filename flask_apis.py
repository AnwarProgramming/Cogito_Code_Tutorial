from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/hello', methods=['GET'])
def hello_world():
    data = {
        'message':'Hello, World!'
    }

    return jsonify(data) , 200

# methods
# GET - client can retrive data via this route/url
# POST - client can Send/create data via this route/url
# PUT - client can  update data via this route/url
# DELETE - client can delete data via this route/url

# Status code 
# 100-199 information
# 200- 299 success
# 300 - 399 redirection
# 400-499 client error
# 500-599 server error
@app.route('/api/hello/error', methods=['GET'])
def hello_world_error():
    data = {
        'message':'Error while loading'
    }

    return jsonify(data) , 404

@app.route('/api/addition/<int:a>/<int:b>', methods=['GET'])
def addition_with_url_request(a,b):
    result = a + b
    data = {
        'value': result,
        'message':f"Addition of two numbers {a} and {b} is {result}"
    }
    return jsonify(data) , 200

@app.route('/api/addition', methods=['GET'])
def addition():
    request_data = request.get_json()
    # print(request_data)
    # print(type(request_data))
    result_data = {
        'value' : request_data['a'] + request_data['b'],
        'message': f'Addition of two numbers  {request_data['a']} and {request_data['b']} is {request_data['a']+request_data['b']}'
    }
    return jsonify(result_data),200
# request is an object that contains all the data sent by the client to the serve.
# in Flask:request is a Flask object that represents the incoming HTTP request from the client.


if __name__=='__main__':
    app.run(debug=True)