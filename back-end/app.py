import pandas as pd
from flask import Flask,request,jsonify, g,Blueprint
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource
import json
import shutil
import os

from BinProcessor import BinProcessor
from DatabaseConnector import DatabaseConnector,User,Model
from DataSource import DataSource
from DateEncoder import DateEncoder
from train_predict import train,args,predict_valid
from Predictor import Predictor
import sys
from external import db
from jwt_token import encode,decode
from jwt.exceptions import InvalidTokenError

app = Flask(__name__)
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db.init_app(app)

CORS(app, supports_credentials=True)
api = Api(app)
with app.app_context():
    dbcon=DatabaseConnector()

data_src=DataSource(dbcon)
predictor=Predictor()


@app.before_request
def before_request():
    #手动验证一下是否为注册或登录
    if request.path.split('/')[1]=='login_api':
        return None

    # 获取请求头中的 Authorization 字段
    auth_header = request.headers.get('Authorization', None)
    if request.method=='GET' or request.method=='POST':
        # print(auth_header)

        # 如果 Authorization 字段不存在，或者格式错误，返回错误
        if not auth_header or 'Bearer' not in auth_header:
            return jsonify({'message': 'Invalid token'}), 401

        # 从 Authorization 字段中获取 token
        token = auth_header.split(' ')[1]

        try:
            # 解析 token，并将结果存储在全局对象 g 中
            g.user = decode(token)
        except InvalidTokenError:
            # 如果 token 解析失败，返回错误
            return jsonify({'message': 'Invalid token'}), 401

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
    # print(f'{missingValueOption}+{aValueOption}+{bValueOption}')
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

@app.route('/save_model',methods=['POST'])
def save_model():
    data = json.loads(request.data)
    # print(data)
    copy_path=f'model/{data["analyst"]}/temp/{data["number"]}'
    if not os.path.exists(copy_path):
        return json.dumps({'error':'没有模型'}, ensure_ascii=False)

    common_files=['args.pkl','scaler_x.pkl','scaler_y.pkl']
    models={
        "上传神经网络模型":'model_nn.pdparams',
        "上传随机森林模型":'model_random.pkl'
    }
    model_path={
        "上传神经网络模型": f'model/{data["analyst"]}/{data["number"]}/model_nn/{data["nn_score"]}',
        "上传随机森林模型": f'model/{data["analyst"]}/{data["number"]}/model_random/{data["rf_score"]}'
    }
    models_type = {
        "上传神经网络模型": '神经网络',
        "上传随机森林模型": '随机森林'
    }
    models_score={
        "上传神经网络模型": data["nn_score"],
        "上传随机森林模型": data["rf_score"]
    }

    for m in data['models']:
        if os.path.exists(model_path[m]):
            shutil.rmtree(model_path[m])
        os.makedirs(model_path[m])

        for f in common_files:
            shutil.copy(copy_path + '/' + f, model_path[m])
        shutil.copy(copy_path + '/' + models[m], model_path[m])
        with app.app_context():
            model=Model(analyst_id=g.user.id,
                        dataset=data['dataset'],
                        model_type=models_type[m],
                        score=models_score[m],
                        comment=data['comment'])
            db.session.add(model)
            db.session.commit()

    #操作数据库
    return json.dumps({'result':'上传成功'}, ensure_ascii=False)

@app.route('/receive_predict_data', methods=['POST'])
def receive_predict_data():
    if request.files is None:
        return json.dumps({'error': '传输失败'}, ensure_ascii=False)
    try:
        csv_data = pd.read_csv(request.files['file'])
    except:
        return json.dumps({'error': '无法读取文件'}, ensure_ascii=False)
    # 判断是否存在关键行
    cols = ['DATATIME', 'WINDDIRECTION', 'WINDSPEED', 'TEMPERATURE', 'HUMIDITY', 'PRESSURE']
    col_exists=True
    for c in cols:
        col_exists=col_exists and (c in csv_data.columns)
    if not col_exists:
        return json.dumps({'error': '文件格式有误'}, ensure_ascii=False)

    predictor.data=csv_data
    return json.dumps({'result': '传输完成'}, ensure_ascii=False)

@app.route('/get_models', methods=['GET'])
def get_models():
    """

    :return: 从数据库获取模型数据
    """
    dataset=request.args['dataset']

    dicts=[]
    #数据库操作
    with app.app_context():
        if dataset == 'None':
            models=Model.query.all()
        else:
            models=Model.query.filter_by(dataset=dataset).all()
        for m in models:
            dicts.append(m.to_dict())

    return json.dumps(dicts, ensure_ascii=False)

@app.route('/delete_model', methods=['POST'])
def delete_model():
    """

    :return: 从数据库删除模型
    """
    data = json.loads(request.data)
    mapper={
        "神经网络":"model_nn",
        "随机森林":"model_random"
    }
    with app.app_context():
        model=Model.query.filter_by(id=data['model_id']).first()
        path=f'model/{model.analyst.username}/{data["number"]}/{mapper[model.model_type]}/{model.score}'
        if os.path.exists(path):
            shutil.rmtree(path)
        db.session.delete(model)
        db.session.commit()
    return json.dumps({"result":"删除成功"}, ensure_ascii=False)

@app.route('/predict', methods=['GET'])
def predict():
    """

    :return: 预测数据
    """
    model_types={
        '神经网络':'model_nn',
        '随机森林':'model_random'
    }
    path=f'model/{request.args["analyst"]}/{request.args["number"]}/{model_types[request.args["model_type"]]}/{request.args["score"]}'
    time_list, pre_val=predictor.predict(path,model_types[request.args["model_type"]])

    dict = {
        'time_list':time_list,
        'pre_val':pre_val
    }
    return json.dumps(dict, ensure_ascii=False)

@app.route('/get_users', methods=['GET'])
def get_users():
    """

    :return: 从数据库获取用户数据
    """
    dicts=[]
    #数据库操作
    with app.app_context():
        users=User.query.all()
        for u in users:
            dicts.append(u.to_dict())

    return json.dumps(dicts, ensure_ascii=False)

@app.route('/promote', methods=['POST'])
def promote():
    """

    :return: 将普通用户升级为模型训练师
    """
    data = json.loads(request.data)
    with app.app_context():
        User.query.filter_by(id=data['user_id']).update({'role':'analyst'})
        db.session.commit()
    return json.dumps({"result": "提升成功"}, ensure_ascii=False)

@app.route('/demote', methods=['POST'])
def demote():
    """

    :return: 将模型训练师降级为普通用户
    """
    data = json.loads(request.data)
    with app.app_context():
        User.query.filter_by(id=data['user_id']).update({'role':'client'})
        db.session.commit()
    return json.dumps({"result": "降级成功"}, ensure_ascii=False)



login_api = Blueprint('login_api', __name__)

@login_api.route('/login', methods=['POST'])
def login():
    """

    :return: 登录，并返回用户信息
    """
    data = json.loads(request.data)
    with app.app_context():
        user=User.query.filter_by(username=data['username'],password=data['password']).one_or_none()
    if user is None:
        return json.dumps({'error': '用户名或密码错误'}, ensure_ascii=False)
    dict=user.to_dict()
    dict['token']=encode(dict)
    return json.dumps(dict, ensure_ascii=False)

@login_api.route('/sign_up', methods=['POST'])
def sign_up():
    """

    :return: 登录，并返回用户信息
    """
    data = json.loads(request.data)
    with app.app_context():
        user=User(username=data['username'],password=data['password'],role='client')
        db.session.add(user)
        db.session.commit()
    return json.dumps({"result": "注册完毕，请登录"}, ensure_ascii=False)

app.register_blueprint(login_api, url_prefix='/login_api')

if __name__ == '__main__':
    app.run()