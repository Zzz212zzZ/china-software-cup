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
        self.r=r
        self.step=step
        self.deadValue=deadValue

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
        data=self.data.loc[index]
        # print(len(self.y_Mean))
        # print(data['ROUND(A.WS,1)'].dropna().map(lambda x:int(x//self.step)).max())
        out_of_range=data['ROUND(A.WS,1)']>(data['ROUND(A.WS,1)'].dropna().map(lambda x:int(x//self.step)).max())
        data['YD15']=data['ROUND(A.WS,1)'].dropna().drop(data[out_of_range].index).map(lambda x:self.y_Mean[int(x//self.step)])
        return data


    def getProcessedData(self,missingValueOption,aValueOption,bValueOption):
        data=self.getNormalData()
        # data=self.fillMethod(self.MissingIndex)
        if missingValueOption=='fill': data=pd.concat([data,self.fillMethod(self.MissingIndex)])
        if aValueOption=='fill': data=pd.concat([data,self.fillMethod(self.AIndex)])
        if bValueOption=='fill': data=pd.concat([data,self.fillMethod(self.BIndex)])
        return data.dropna()



