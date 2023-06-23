from flask import Flask,request
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource
import json
import numpy as np

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
    table_name = request.args['number']
    y = request.args['y']
    x = request.args['x']
    step = 1 / float(request.args['percentage'])
    data = data_src.get_data(table_name, [x, y]).dropna()

    dict = {}
    dict['data'] = data.values.tolist()
    dict['Combine'] = data[np.floor(data.index % step) == 0].values.tolist()
    return json.dumps(dict, ensure_ascii=False)


@app.route('/dimension_data', methods=['GET'])
def dimension_data():
    """
    输入风机编号number和维度dimension，返回该风机的指定维度的数据

    :return: json格式的字典，包含指定维度的数据
    """
    table_name = request.args['number']
    dimension = request.args['dimension']
    return json.dumps(data_src.get_dimension_data(table_name, dimension), ensure_ascii=False)

@app.route('/bin_data', methods=['GET'])
def bin_data():
    table_name = request.args['number']
    r = request.args['r']

    dict = {}
    dict['bin_data'] = data_src.data_bin_process(table_name, r).values.tolist()
    return json.dumps(dict, ensure_ascii=False)


if __name__ == '__main__':
    app.run()