from train_predict import predict


class Predictor(object):
    def __init__(self, data=None):
        self.data = data

    def predict(self, read_path, model_type):
        return predict(self.data, read_path, model_type, self.data.shape[0])
