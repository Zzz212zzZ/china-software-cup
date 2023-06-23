from flask import Flask,request
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource

app = Flask(__name__)
CORS(app)
api = Api(app)



@app.route('/hello', methods=['GET'])
def hello():
    return {'message': 'Hello, World!'}


@app.route('/basic_info', methods=['GET'])
def basic_info():
    """
    输入风机编号number,返回风机的基本信息(1-9的编号为01-09)

    :return: json格式的字典，其中Data dimension：数据维度，Records number ：数据记录数，NULL values：YD15缺失值条数，Record days：记录天数
    """
    table_name=request.args['number']
    return json.dumps(dbcon.get_basic_info(table_name), ensure_ascii=False)



if __name__ == '__main__':
    app.run()