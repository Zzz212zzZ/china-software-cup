import bin
import pandas as pd
from process_with_bin import bin_process

class BinProcessor(object):
    def __init__(self,data:pd.DataFrame):
        self.data=data[['ROUND(A.WS,1)','YD15']]
        self.step=None
        self.MissingIndex=data[data.isna().T.any()].index
        self.AIndex=pd.Index([],dtype='int64')
        self.BIndex=pd.Index([],dtype='int64')
        self.NormalIndex=data.dropna().index
        self.r=None
        self.step=None
        self.deadValue=None
        self.y_Mean=None

    def info(self):
        print(self.MissingIndex)
        print(self.AIndex)
        print(self.BIndex)
        print(self.NormalIndex)

    def bin(self,r,step,deadValue):
        if self.r==r and self.step==step and self.deadValue==deadValue : return
        data=self.data.dropna()
        self.AIndex=data.apply(lambda x: x.groupby((x.shift() != x).cumsum()).filter(lambda x: len(x) >= deadValue)).index
        data=data.drop(self.AIndex)

        # data.drop(data[(data['ROUND(A.WS,1)']>8) & (data['YD15']<10000)].index,inplace=True)
        # data.drop(data[(data['ROUND(A.WS,1)'] < 1) & (data['YD15'] > 20000)].index, inplace=True)

        x_Mean, y_Mean, y_std=bin.bin_data(data['ROUND(A.WS,1)'].values, data['YD15'].values, step)
        self.y_Mean=y_Mean
        self.NormalIndex = bin_process(data, data['ROUND(A.WS,1)'].min(), data['ROUND(A.WS,1)'].max(), y_Mean, y_std, step,
                           'ROUND(A.WS,1)', 'YD15', r).index
        self.BIndex=data.drop(self.NormalIndex).index

    def getMissingData(self):
        """
        获取有缺失值的数据
        :return:有缺失值的数据
        """
        return self.data.loc[self.MissingIndex]

    def getAData(self):
        """
        获取A类异常点
        :return: A类异常点数据
        """
        return self.data.loc[self.AIndex]

    def getBData(self):
        """
        获取B类异常点
        :return: B类异常点数据
        """
        return self.data.loc[self.BIndex]

    def getNormalData(self):
        """
        获取正常点的数据
        :return: 正常点数据
        """
        return self.data.loc[self.NormalIndex]

    def fillMethod(self,index):
        data=self.data[index]


    def getProcessedData(self,missingValueOption,aValueOption,bValueOption):
        data=self.getNormalData()
        return data



