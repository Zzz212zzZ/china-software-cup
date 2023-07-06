import pandas as pd
from flask import Flask,request
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource
import json
import shutil
import os

from BinProcessor import BinProcessor
from DatabaseConnector import DatabaseConnector
from DataSource import DataSource
from DateEncoder import DateEncoder
from train_predict import train,args,predict_valid

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
    # percentage = float(request.args['percentage'])
    data = data_src.get_data(table_name, [x, y]).dropna()

    dict = {}
    dict['data_all'] = data.values.tolist()
    # dict['data_mini'] = data.sample(frac=percentage).values.tolist()
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

    dict['bin_data'] = normal_data.values.tolist()
    a_data=bin.getAData()
    dict['a_data']=a_data.drop_duplicates().values.tolist()
    b_data=bin.getBData()
    dict['b_data']=b_data.drop_duplicates().values.tolist()

    dict['not_missing_percentage'] = bin.data.shape[0]-bin.getMissingData().shape[0]
    dict['missing_percentage']=bin.getMissingData().shape[0]
    dict['a_data_percentage']=bin.getAData().shape[0]
    dict['b_data_percentage']=bin.getBData().shape[0]
    dict['bin_data_percentage']=bin.getNormalData().shape[0]
    return json.dumps(dict, ensure_ascii=False)

@app.route('/do_data_process', methods=['GET'])
def do_data_process():
    missingValueOption = request.args['missingValueOption']
    aValueOption = request.args['aValueOption']
    bValueOption = request.args['bValueOption']
    print(f'{missingValueOption}+{aValueOption}+{bValueOption}')
    data_src.set_processed_data(missingValueOption,aValueOption,bValueOption)
    return json.dumps({'result':'success'}, ensure_ascii=False)

@app.route('/unprocessed_data', methods=['GET'])
def unprocessed_data():
    table_name = request.args['number']
    if data_src.table_name!=table_name: return json.dumps({'error':'数据不存在，请先完成数据预处理'}, ensure_ascii=False)
    if data_src.processedData is None: return json.dumps({'error':'数据不存在，请先完成数据预处理'}, ensure_ascii=False)

    dict = {}
    dict['length'] = data_src.processedData.shape[0]

    data=data_src.processedData.sort_values(by='DATATIME')['YD15'].values.tolist()
    x = [i for i in range(dict['length'])]
    dict['data'] = [[i, j] for i,j in zip(x,data)]
    return json.dumps(dict, ensure_ascii=False)

@app.route('/train', methods=['POST'])
def train_data():
    data = json.loads(request.data)
    cols=['WINDDIRECTION', 'WINDSPEED', 'TEMPERATURE', 'HUMIDITY', 'PRESSURE']
    pri_use_cols=[]
    for c in data['primaryVars']:
        pri_use_cols.append(cols.index(c))
    sec_use_cols=[]
    for c in data['secondaryVars']:
        sec_use_cols.append(cols.index(c))


    arg=args(
        epoch_num=data['epoch'],
        batch_size=eval(data['batchsize']),
        learning_rate=eval(data['learning_rate']),
        pri_use_cols=pri_use_cols,
        sec_use_cols=sec_use_cols,
        embedding_size=data['embedding_size'],
        GRU_layers=data['GRU_layers'],
        agg_method=data['Aggregation_function'],
        turbine_id=data['number'],
        train_start=int(data['samples'][0]),
        train_end=int(data['samples'][1]),
        val_start=int(data['samples'][2]),
        val_end=int(data['samples'][3]),
    )
    path=f'model/{data["analyst"]}/temp/{data["number"]}'
    arg.save(path)
    train(data_src.processedData,arg,path)
    return json.dumps({'result':'success'}, ensure_ascii=False)

@app.route('/trained_data', methods=['POST'])
def trained_data():
    data = json.loads(request.data)
    print(data['samples'][2])
    print(data['samples'][3])
    path = f'model/{data["analyst"]}/temp'
    if data_src.processedData is None:
        return json.dumps({'error':'no data'}, ensure_ascii=False)
    if not os.path.exists(path+'/'+str(data['number'])):
        if os.path.exists(path):
            shutil.rmtree(path)
        return json.dumps({'error':'no modal'}, ensure_ascii=False)

    tru_val, nn_pre_val, random_pre_val, nn_score, random_score = predict_valid(data_src.processedData ,path+'/'+str(data['number']))
    nn_score = round(nn_score, 3)
    random_score = round(random_score, 3)

    dict = {}
    dict['tru_val']=tru_val
    dict['nn_pre_val']=nn_pre_val
    dict['random_pre_val']=random_pre_val
    dict['nn_score']=nn_score
    dict['random_score']=random_score
    dict['x'] = [i for i in range(len(tru_val))]

    x_train = [i for i in range(data['samples'][1])]
    x_valid = [i for i in range(data['samples'][2],data['samples'][3])]

    yd_train = data_src.processedData.sort_values(by='DATATIME')['YD15'].values.tolist()[:data['samples'][1]]
    dict['data_train'] = [[i,j] for i,j in zip(x_train,yd_train)]

    dict['data_valid'] = [[i,j] for i,j in zip(x_valid,tru_val)]
    dict['nn_pre_valid'] = [[i,j] for i,j in zip(x_valid,nn_pre_val)]
    dict['random_pre_valid'] = [[i,j] for i,j in zip(x_valid,random_pre_val)]
    return json.dumps(dict, ensure_ascii=False)

@app.route('/retrain', methods=['GET'])
def retrain():
    analyst = request.args['analyst']
    path = f'model/{analyst}/temp'
    if(os.path.exists(path)):
        shutil.rmtree(path)
    return json.dumps({'result':'成功删除'}, ensure_ascii=False)


if __name__ == '__main__':
    app.run()