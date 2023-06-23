import os
import sys
from flask_sqlalchemy import SQLAlchemy
import pandas as pd


class DatabaseConnector(object):
    def __init__(self, app):
        self.db_name = 'data'
        WIN = sys.platform.startswith('win')
        if WIN:  # 如果是 Windows 系统，使用三个斜线
            prefix = 'sqlite:///'
        else:  # 否则使用四个斜线
            prefix = 'sqlite:////'
        app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, self.db_name + '.db')
        with app.app_context():
            self.db = SQLAlchemy(app)
            self.engine = self.db.engine

    def df_to_database(self, data: pd.DataFrame, table_name, if_exists='fail'):
        """
        将DataFrame数据读入对应表

        :param data: DataFrame数据
        :param table_name：表名
        :param if_exists: 如果表存在，'fail'：不做任何操作，'append':将数据加入表末尾，'replace':删除之前的数据
        :return:
        """
        data.to_sql(name=table_name, con=self.engine, if_exists=if_exists, index=False)

    def read_db(self, table_name, *columns):
        """
        从表中读取对应维度的数据

        :param table_name: 表名
        :param columns: 要选取的列，如果为空默认为所有列
        :return:
        """
        select_sql = "SELECT "
        if len(columns) == 0:
            select_sql += '*'
        else:
            for c in columns:
                select_sql += '`' + c + '`,'
            select_sql = select_sql.rstrip(',')
        select_sql += " FROM `" + table_name + '`'
        df = pd.read_sql(select_sql, self.engine,parse_dates=['DATATIME'])
        return df


    def get_basic_info(self,table_name):
        """
        获取该表的基本信息，返回字典，其中Data dimension：数据维度，Records number ：数据记录数，NULL values：YD15缺失值条数，Record days：记录天数，最后一天：最后一天的日期

        :param table_name:表名
        :return:返回包含基本信息的字典
        """
        dict={}
        df=self.read_db(table_name)
        dict['数据维度']=df.shape[1]
        dict['数据记录数']=df.shape[0]
        dict['YD15缺失数']=df['YD15'].isna().sum().item()
        dict['记录天数']=(df['DATATIME'].max()-df['DATATIME'].min()).days
        #还要返回最后一天的日期
        dict['最后一天']=df['DATATIME'].max().strftime('%Y/%m/%d')
        return dict
    

    def get_dimension_data(self, table_name, dimension):
        """
        获取指定表的指定维度的数据

        :param table_name: 表名
        :param dimension: 数据维度
        :return: 包含指定维度数据的字典
        """
        # 从表中读取数据
        df = self.read_db(table_name)

        # 检查维度是否存在
        if dimension not in df.columns:
            raise ValueError(f"Dimension {dimension} does not exist in table {table_name}.")

        # 获取指定维度的数据
        data = df[dimension].tolist()

        # 返回数据
        return {dimension: data}
