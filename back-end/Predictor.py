from train_predict import predict,predict_model
from io import BytesIO
import pandas as pd


class Predictor(object):
    def __init__(self, data=None):
        self.data = data
        self.time_list=None
        self.pre_val=None

    def predict(self, read_path, model_type):
        time_list, pre_val=predict(self.data, read_path, model_type, self.data.shape[0])
        self.time_list=time_list
        self.pre_val=pre_val
        return time_list, pre_val

    def predict_model(self, model):
        time_list, pre_val=predict_model(self.data, model, self.data.shape[0])
        self.time_list=time_list
        self.pre_val=pre_val
        return time_list, pre_val

    def to_csv(self):
        byteio=BytesIO()
        # df=pd.DataFrame({
        #     'time_list':self.time_list,
        #     'pre_val':self.pre_val
        # })
        df=pd.DataFrame((zip(self.time_list, self.pre_val)), columns = ['time_list', 'pre_val'])
        df.to_csv(byteio, index=False)
        return byteio
