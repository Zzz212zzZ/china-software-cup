import pandas as pd

from DatabaseConnector import DatabaseConnector
import time

class DataSource(object):
    def __init__(self,dbcon:DatabaseConnector):
        self.dbcon=dbcon
        self.data=None
        self.synchronization=True
        self.table_name=None

    def update(self, table_name):
        if not (self.table_name==table_name and self.synchronization):
            # print('updated')
            self.data=self.dbcon.read_db(table_name)
            self.table_name=table_name
            self.synchronization=True

    def get_basic_info(self, table_name):
        """
        获取基本信息，返回字典，其中Data dimension：数据维度，Records number ：数据记录数，NULL values：YD15缺失值条数，Record days：记录天数

        :param table_name:表名
        :return:返回包含基本信息的字典
        """
        self.update(table_name)
        dict = {}
        df = self.data
        dict['Data dimension'] = df.shape[1]
        dict['Records number'] = df.shape[0]
        dict['NULL values'] = df['YD15'].isna().sum().item()
        dict['Record days'] = (df['DATATIME'].max() - df['DATATIME'].min()).days
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