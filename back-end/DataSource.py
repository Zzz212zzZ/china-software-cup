import pandas as pd

from DatabaseConnector import DatabaseConnector
from BinProcessor import BinProcessor

class DataSource(object):
    def __init__(self,dbcon:DatabaseConnector):
        self.dbcon=dbcon
        self.bin=None
        self.data=None
        self.processedData=None
        self.synchronization=True
        self.table_name=None

    def update(self, table_name):
        if not (self.table_name==table_name and self.synchronization):
            # print('updated')
            self.data=self.dbcon.read_db(table_name)
            self.table_name=table_name
            self.synchronization=True

    def get_basic_info(self,table_name):
        """
        获取该表的基本信息，返回字典，其中Data dimension：数据维度，Records number ：数据记录数，NULL values：YD15缺失值条数，Record days：记录天数，最后一天：最后一天的日期

        :param table_name:表名
        :return:返回包含基本信息的字典
        """
        dict={}
        df=self.dbcon.read_db(table_name)
        dict['数据维度']=df.shape[1]
        dict['数据记录数']=df.shape[0]
        dict['YD15缺失数']=df['YD15'].isna().sum().item()
        dict['记录天数']=(df['DATATIME'].max()-df['DATATIME'].min()).days
        #还要返回最后一天的日期
        dict['最后一天']=df['DATATIME'].max().strftime('%Y/%m/%d')
        return dict

    def get_data(self,table_name,columns=None) ->pd.DataFrame:
        """
        获取表信息
        :param table_name: 表名
        :param columns: 列名，如果为None则返回所有列
        :return: 表
        """
        self.update(table_name)
        if columns is None:
            return self.data
        return self.data[columns]

    def get_dimension_data(self, table_name, dimension):
        """
        获取指定表的指定维度的数据

        :param table_name: 表名
        :param dimension: 数据维度
        :return: 包含指定维度数据的字典
        """
        # 从表中读取数据
        self.update(table_name)

        # 检查维度是否存在
        if dimension not in self.data.columns:
            raise ValueError(f"Dimension {dimension} does not exist in table {table_name}.")

        # 获取指定维度的数据
        data = self.data[dimension].fillna(value=0).tolist()
        # 将Timestamp对象转换为字符串
        if isinstance(data[0], pd.Timestamp):
            data = [d.strftime("%Y-%m-%d %H:%M:%S") for d in data]

        # 返回数据
        return {dimension: data}

    def set_bin(self,table_name,r,step,deadValue):
        self.update(table_name)
        self.bin=BinProcessor(self.data)
        self.bin.bin(r,step,deadValue)

    def set_processed_data(self,missingValueOption,aValueOption,bValueOption):
        data=self.bin.getProcessedData(missingValueOption,aValueOption,bValueOption)
        self.processedData=self.data.loc[data.index]
        self.processedData[['ROUND(A.WS,1)','YD15']]=data