from flask import Flask,request
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource
import json

from DatabaseConnector import DatabaseConnector
from DataSource import DataSource

app = Flask(__name__)
CORS(app)
api = Api(app)
dbcon=DatabaseConnector(app)
data_src=DataSource(dbcon)


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
    return json.dumps(data_src.get_basic_info(table_name), ensure_ascii=False)

@app.route('/correlation', methods=['GET'])
def correlation():
    """
    输入风机编号number,y轴y，x轴x
    :return: 对应数据
    """
    table_name=request.args['number']
    y=request.args['y']
    x=request.args['x']
    return data_src.get_data(table_name,[y,x]).dropna().to_json()



if __name__ == '__main__':
    app.run()