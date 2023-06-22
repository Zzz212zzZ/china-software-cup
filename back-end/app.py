from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource

app = Flask(__name__)
CORS(app)
api = Api(app)



@app.route('/hello', methods=['GET'])
def hello():
    return {'message': 'Hello, World!'}



if __name__ == '__main__':
    app.run()