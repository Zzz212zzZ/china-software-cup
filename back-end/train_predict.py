import math
import os
import datetime
import pickle
import paddle
import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler
import paddle.nn.functional as F
from util import *
import matplotlib.pyplot as plt

# 随机种子，保证实验能复现
import random
seed = 142
paddle.seed(seed)
np.random.seed(seed)
random.seed(seed)

import warnings
warnings.filterwarnings('ignore')

# 模型参数

epoch_num = 100  # 模型训练的轮数
batch_size = 256  # 每个训练批次使用的样本数量
patience = 10  # 如果连续patience个轮次性能没有提升，就会停止训练。
learning_rate = 0.0002  # 学习率


# turbine_id, use_cols, train_start, train_end, val_start, val_end
class args():
    """

    """
    def __init__(self, epoch_num=10, batch_size=512, learning_rate=0.0002, pri_use_cols=[0,1], sec_use_cols=[2,3,4], embedding_size=256, GRU_layers=3, agg_method='sum', turbine_id = 11, train_start=0, train_end=20000, val_start=20000, val_end=22000):
        self.epoch_num = epoch_num
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.pri_use_cols = pri_use_cols
        self.sec_use_cols = sec_use_cols
        self.turbine_id = turbine_id
        self.train_start = train_start
        self.train_end = train_end
        self.val_start = val_start
        self.val_end = val_end
        self.embedding_size = embedding_size
        self.GRU_layers = GRU_layers
        self.agg_method = agg_method

def data_preprocess(df):
    # ===========读取数据===========
    df = df.sort_values(by='DATATIME', ascending=True)
    # ===========去除重复值===========
    df = df.drop_duplicates(subset='DATATIME', keep='first')
    # 用yd15补全ROUND(A.POWER,0)
    df['ROUND(A.POWER,0)'][df['ROUND(A.POWER,0)'].isnull()] = df['YD15'][df['ROUND(A.POWER,0)'].isnull()]
    # ===========重采样（可选） + 线性插值===========
    df = df.set_index('DATATIME')
    # TODO 尝试一些其他缺失值处理方式，比如，用同时刻附近风机的值求均值填补缺失值
    df = df.interpolate(method='linear', limit_direction='both').reset_index()
    print('After Resampling:', df.shape)
    return df
class pre_model(paddle.nn.Layer):
    def __init__(self, pri_use_cols, sec_use_cols, embedding_size, GRU_layers, agg_method):
        super(pre_model, self).__init__()
        self.relu = paddle.nn.ReLU()
        self.agg_method = agg_method
        self.pri_use_cols = pri_use_cols
        self.sec_use_cols = sec_use_cols
        self.mlp1 = paddle.nn.Sequential(
            paddle.nn.Linear(in_features=len(pri_use_cols), out_features=512),
            paddle.nn.ReLU(),
            paddle.nn.Linear(in_features=512, out_features=embedding_size),
        )
        self.mlp2 = paddle.nn.Sequential(
            paddle.nn.Linear(in_features=len(sec_use_cols), out_features=512),
            paddle.nn.ReLU(),
            paddle.nn.Linear(in_features=512, out_features=embedding_size),
        )

        self.gru1 = paddle.nn.GRU(1, 1, GRU_layers)
        self.gru2 = paddle.nn.GRU(1, 1, GRU_layers)


        self.mlp_sum = paddle.nn.Sequential(
            paddle.nn.Linear(in_features=embedding_size, out_features=128),
            paddle.nn.ReLU(),
            paddle.nn.Linear(in_features=128, out_features=64),
            paddle.nn.ReLU(),
            paddle.nn.Linear(in_features=64, out_features=1)
        )
        self.mlp_concat = paddle.nn.Sequential(
            paddle.nn.Linear(in_features=2*embedding_size, out_features=128),
            paddle.nn.ReLU(),
            paddle.nn.Linear(in_features=128, out_features=64),
            paddle.nn.ReLU(),
            paddle.nn.Linear(in_features=64, out_features=1)
        )
        self.att = paddle.nn.Sequential(
            paddle.nn.Linear(in_features=5, out_features=128),
            paddle.nn.ReLU(),
            paddle.nn.Linear(in_features=128, out_features=2)
        )
    def forward(self, x):
        # x形状大小为[batch_size, feature_size]
        pri = []
        for i in range(len(self.pri_use_cols)):
            pri.append(x[:,self.pri_use_cols[i]:self.pri_use_cols[i]+1])
        sec = []
        for i in range(len(self.sec_use_cols)):
            sec.append(x[:,self.sec_use_cols[i]:self.sec_use_cols[i]+1])

        pri = paddle.concat(pri, -1)
        sec = paddle.concat(sec, -1)

        emb1 = self.mlp1(pri)
        emb2 = self.mlp2(sec)

        emb1_ = paddle.reshape(emb1,[emb1.shape[0],emb1.shape[1],1])
        emb2_ = paddle.reshape(emb2,[emb2.shape[0],emb2.shape[1],1])

        output1, _ = self.gru1(emb1_)
        output2, _ = self.gru2(emb2_)

        output1 = paddle.reshape(output1,[output1.shape[0], -1])
        output2 = paddle.reshape(output2,[output2.shape[0], -1])

        if self.agg_method == 'sum':
            output = self.mlp_sum(output1 + output2)
        elif self.agg_method == 'attention_sum':
            att = self.att(x)
            att_weight = paddle.nn.functional.softmax(att)
            output = paddle.multiply(output1, paddle.reshape(att_weight[:, 0], [att.shape[0], 1])) + paddle.multiply(output2,
                                                                                                           paddle.reshape(
                                                                                                               att_weight[:,
                                                                                                               1], [att.shape[0], 1]))
            output = self.mlp_sum(output)
        elif self.agg_method == 'concat':
            output = [output1, output2]
            output = self.mlp_concat(paddle.concat(output, 1))
        else:
            print('没有这个方法')

        return output

class TSDataset(paddle.io.Dataset):
    def __init__(self, data, args,
                 ts_col='DATATIME',
                 labels=['YD15'],
                 data_type='train',):
        super(TSDataset, self).__init__()
        self.ts_col = ts_col  # 时间戳列
        self.use_cols = ['WINDDIRECTION', 'WINDSPEED', 'TEMPERATURE', 'HUMIDITY', 'PRESSURE']
        self.labels = labels  # 待预测的标签列
        self.data_type = data_type  # 需要加载的数据类型
        self.turbine_id = args.turbine_id
        self.train_start, self.train_end, self.val_start, self.val_end = args.train_start, args.train_end, args.val_start, args.val_end
        self.scale = True  # 是否需要标准化
        assert data_type in ['train', 'val']  # 确保data_type输入符合要求
        type_map = {'train': 0, 'val': 1}
        self.set_type = type_map[self.data_type]
        self.transform(data)

    def transform(self, df):
        # 获取unix时间戳、输入特征和预测标签
        x_values, y_values = df[self.use_cols].values, df[self.labels].values
        # 划分数据集
        border1s = [self.train_start, self.val_start]
        border2s = [self.train_end, self.val_end]
        # 获取data_type下的左右数据截取边界
        border1 = border1s[self.set_type]
        border2 = border2s[self.set_type]
        # 标准化
        self.scaler1 = StandardScaler()
        self.scaler2 = StandardScaler()
        if self.scale:
            # 使用训练集得到scaler对象
            self.scaler1.fit(x_values)
            self.scaler2.fit(y_values)
            x_values = self.scaler1.transform(x_values)
            y_values = self.scaler2.transform(y_values)
            # 保存scaler
            pickle.dump(self.scaler1, open('model/scaler{}_x.pkl'.format(self.turbine_id), 'wb'))
            pickle.dump(self.scaler2, open('model/scaler{}_y.pkl'.format(self.turbine_id), 'wb'))
        else:
            pass
        # array to paddle tensor
        self.data_x = paddle.to_tensor(x_values[border1:border2], dtype='float32')
        self.data_y = paddle.to_tensor(y_values[border1:border2], dtype='float32')
    def __getitem__(self, index):
        """
        实现__getitem__方法，定义指定index时如何获取数据，并返回单条数据（训练数据）
        """
        # 由于赛题要求利用当日05:00之前的数据，预测次日00:00至23:45实际功率
        # 所以x和label要间隔19*4个点
        # TODO 可以增加对未来可见数据的获取
        seq_x = self.data_x[index]
        seq_y = self.data_y[index]
        return seq_x, seq_y
    def __len__(self):
        """
        实现__len__方法，返回数据集总数目
        """
        return len(self.data_x)

class MSELoss(paddle.nn.Layer):
    """
    设置损失函数, 多任务模型，两个任务MSE的均值做loss输出
    """
    def __init__(self):
        super(MSELoss, self).__init__()
    def forward(self, inputs, labels):
        mse_loss = paddle.nn.loss.MSELoss()
        mse = mse_loss(inputs, labels)
        return mse
def train(df, args):
    """
    :param df: 输入的dataframe格式数据
    :param args:  arg参数类实例
    :return: 可以不返回结果
    """
    df = data_preprocess(df)
    # 设置数据集
    train_dataset = TSDataset(df, args, data_type='train')
    val_dataset = TSDataset(df, args, data_type='val')
    print(f'LEN | train_dataset:{len(train_dataset)}, val_dataset:{len(val_dataset)}')

    # 设置数据读取器
    train_loader = paddle.io.DataLoader(train_dataset, shuffle=True, batch_size=args.batch_size, drop_last=True)
    val_loader = paddle.io.DataLoader(val_dataset, shuffle=False, batch_size=args.batch_size, drop_last=True)


    # 设置模型
    model = pre_model(args.pri_use_cols, args.sec_use_cols, args.embedding_size, args.GRU_layers, args.agg_method)

    # 设置优化器
    scheduler = paddle.optimizer.lr.ReduceOnPlateau(learning_rate=args.learning_rate, factor=0.5, patience=3, verbose=True)
    opt = paddle.optimizer.Adam(learning_rate=scheduler, parameters= model.parameters())

    # 设置损失
    mse_loss = MSELoss()

    train_loss = []
    valid_loss = []
    train_epochs_loss = []
    valid_epochs_loss = []
    early_stopping = EarlyStopping(patience=10, verbose=True,
                                   ckp_save_path=f'model/model_checkpoint_windid_{args.turbine_id}.pdparams')

    for epoch in tqdm(range(args.epoch_num)):
        # =====================train============================
        train_epoch_loss, train_epoch_mse1, train_epoch_mse2 = [], [], []
        model.train()  # 开启训练
        for batch_id, data in enumerate(train_loader()):
            x = data[0]
            y = data[1]
            # 预测
            outputs = model(x)
            # print(outputs)
            # 计算损失
            mse = mse_loss(outputs, y)
            # 反向传播
            mse.backward()
            # 梯度下降
            opt.step()
            # 清空梯度
            opt.clear_grad()
            train_epoch_loss.append(mse.numpy()[0])
            train_loss.append(mse.item())
        train_epochs_loss.append(np.average(train_epoch_loss))
        print("epoch={}/{} of train |  MSE of YD15:{} ".format(epoch, epoch_num, np.average(train_epoch_loss)))
        # =====================valid============================
        model.eval()  # 开启评估/预测
        valid_epoch_loss = []
        for batch_id, data in enumerate(val_loader()):
            x = data[0]
            y = data[1]
            output = model(x)
            mse = mse_loss(output, y)
            valid_epoch_loss.append(mse.numpy()[0])
            valid_loss.append(mse.numpy()[0])

        valid_epochs_loss.append(np.average(valid_epoch_loss))
        print('Valid: MSE of YD15:{}'.format(np.average(train_loss)))

        # ==================early stopping======================
        early_stopping(valid_epochs_loss[-1], model=model)
        if early_stopping.early_stop:
            print(f"Early stopping at Epoch {epoch - patience}")
            break
    return valid_epochs_loss

def predict(df, args):
    """
    :param df: 输入的dataframe格式数据
    :param args:  arg参数类实例
    :return: 返回tru_val（真实的验证集数据，list）, pre_val（预测的验证集数据，list）, pre_test（预测的测试集数据，list）, score（分数）
    """
    df = data_preprocess(df)
    df_pre = df[args.val_start:]
    model = pre_model(args.pri_use_cols, args.sec_use_cols, args.embedding_size, args.GRU_layers, args.agg_method)
    # 导入模型权重文件
    model.set_state_dict(paddle.load(f'model/model_checkpoint_windid_{args.turbine_id}.pdparams'))
    model.eval()  # 开启预测

    scaler_y = pickle.load(open('model/scaler{}_y.pkl'.format(args.turbine_id), 'rb'))
    scaler_x = pickle.load(open('model/scaler{}_x.pkl'.format(args.turbine_id), 'rb'))

    input = np.array(df_pre[['WINDDIRECTION', 'WINDSPEED', 'TEMPERATURE', 'HUMIDITY', 'PRESSURE']])
    input = scaler_x.transform(input)
    input = paddle.to_tensor(input, dtype='float32')

    output = model(input)
    output = scaler_y.inverse_transform(output)

    pre = [x for x in output.squeeze()]
    pre_val = pre[:(args.val_end-args.val_start)]
    pre_test = pre[(args.val_end-args.val_start):]

    tru_val = df_pre['YD15'].tolist()[:(args.val_end-args.val_start)]

    sum = 0
    for pre_i, tru_i in zip(pre_val, tru_val):
        sum += (pre_i-tru_i)**2
    avg = math.sqrt(sum/len(pre_val))/201000
    score = 1-avg

    return tru_val, pre_val, pre_test, score



if __name__ == '__main__':
    args = args()
    df = pd.read_csv('数据/12.csv',
                     parse_dates=['DATATIME'],
                     infer_datetime_format=True,
                     dayfirst=True)

    # train(df, args)
    predict(df,args)

