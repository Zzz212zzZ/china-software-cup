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



    

