import pandas as pd

from DatabaseConnector import DatabaseConnector
from process_with_bin import process_with_bin

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
        self.update()

        # 检查维度是否存在
        if dimension not in self.data.columns:
            raise ValueError(f"Dimension {dimension} does not exist in table {table_name}.")

        # 获取指定维度的数据
        data = self.data[dimension].tolist()

        # 返回数据
        return {dimension: data}

    def data_bin_process(self,table_name,r):
        self.update(table_name)
        return process_with_bin(self.data,range_x=r)