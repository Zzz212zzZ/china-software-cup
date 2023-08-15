import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import pandas as pd
from external import db

class User(db.Model):
    __tablename__ = "user"  # 表名 默认使用类名的小写
    # 定义类属性 记录字段
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    role = db.Column(db.Text)
    avatar = db.Column(db.LargeBinary)
    email = db.Column(db.Text)
    phone = db.Column(db.Text)
    description = db.Column(db.Text)

    def __repr__(self):  # 自定义 交互模式 & print() 的对象打印
        return "(%s, %s, %s, %s, %s, %s, %s)" % (self.id, self.username, self.password, self.role,self.email,self.phone,self.description)

    def to_dict(self):
        return {
            'user_id':self.id,
            'username':self.username,
            'role':self.role
        }

class Model(db.Model):
    __tablename__ = "model"  # 表名 默认使用类名的小写
    # 定义类属性 记录字段
    id = db.Column(db.Integer, primary_key=True)
    analyst_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    analyst=db.relationship('User')
    dataset_id=db.Column(db.Integer, db.ForeignKey('dataset.id'))
    dataset=db.relationship('Dataset')
    # dataset = db.Column(db.Text)
    model_type = db.Column(db.Text)
    score = db.Column(db.Text)
    comment = db.Column(db.Text)

    args=db.Column(db.LargeBinary)
    model=db.Column(db.LargeBinary)
    scaler_x=db.Column(db.LargeBinary)
    scaler_y=db.Column(db.LargeBinary)

    def __repr__(self):  # 自定义 交互模式 & print() 的对象打印
        return "(%s, %s, %s, %s, %s, %s)" % (self.id, self.analyst.username, self.dataset.dataset_name, self.model_type, self.score, self.comment)

    def to_dict(self):
        return {
            'model_id':self.id,
            'analyst':self.analyst.username,
            'dataset':self.dataset.dataset_name,
            'table_name':self.dataset.table_name,
            'model_type':self.model_type,
            'score':self.score,
            'comment':self.comment,
        }


class Dataset(db.Model):
    __tablename__ = "dataset"  # 表名 默认使用类名的小写
    # 定义类属性 记录字段
    id = db.Column(db.Integer, primary_key=True)
    dataset_name = db.Column(db.Text, unique=True)
    table_name=db.Column(db.Text, unique=True)
    location=db.Column(db.Text)
    longitude=db.Column(db.Float)
    latitude=db.Column(db.Float)


    def __repr__(self):  # 自定义 交互模式 & print() 的对象打印
        return "(%s, %s, %s)" % (self.id, self.dataset_name, self.upload_date)

    def to_dict(self):
        return {
            'dataset_id':self.id,
            'dataset_name':self.dataset_name,
            'table_name':self.table_name,
            'location':self.location,
            'longitude':self.longitude,
            'latitude':self.latitude,
        }


class DatabaseConnector(object):
    def __init__(self):
        self.engine = db.engine

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
        df = pd.read_sql(select_sql, self.engine, parse_dates=['DATATIME'])
        return df

    def drop_table(self, table_name):
        sql = f"DROP TABLE `{table_name}`"
        self.engine.connect().execute(text(sql))
