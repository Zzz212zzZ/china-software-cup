import pandas as pd
from flask import Flask,request
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource
import json
import numpy as np
from BinProcessor import BinProcessor

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
    percentage = float(request.args['percentage'])
    data = data_src.get_data(table_name, [x, y]).dropna()

    dict = {}
    dict['data_all'] = data.values.tolist()
    dict['data_mini'] = data.sample(frac=percentage).values.tolist()
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
    r = float(request.args['sigma'])
    step = float(request.args['step'])
    deadValue = float(request.args['deadCount'])

    data_src.set_bin(table_name,r,step,deadValue)

    bin:BinProcessor=data_src.bin
    dict = {}
    normal_data=bin.getNormalData().drop_duplicates()
    if normal_data.shape[0]<=10000:
        dict['bin_data'] =normal_data.values.tolist()
    else:
        dict['bin_data'] = normal_data.sample(n=10000).values.tolist()
    a_data=bin.getAData()
    dict['a_data']=a_data.drop_duplicates().values.tolist()
    b_data=bin.getBData()
    dict['b_data']=b_data.drop_duplicates().sample(frac=0.6).values.tolist()

    dict['missing_percentage']=bin.getMissingData().shape[0]
    dict['a_data_percentage']=bin.getAData().shape[0]
    dict['b_data_percentage']=bin.getBData().shape[0]
    dict['bin_data_percentage']=bin.getNormalData().shape[0]
    return json.dumps(dict, ensure_ascii=False)


if __name__ == '__main__':
    app.run()