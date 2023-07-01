import datetime
import numpy as np
import paddle


class EarlyStopping():
    """早停
    当验证集超过patience个epoch没有出现更好的评估分数，及早终止训练
    若当前epoch表现超过历史最佳分数，保存该节点模型
    参考：https://blog.csdn.net/m0_63642362/article/details/121244655
    """
    def __init__(self, ckp_save_path, patience=7, verbose=False, delta=0):
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta
        self.ckp_save_path = ckp_save_path

    def __call__(self, val_loss, model):
        print("val_loss={}".format(val_loss))
        score = -val_loss
        # 首轮，直接更新best_score和保存节点模型
        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
        # 若当前epoch表现没超过历史最佳分数，且累积发生次数超过patience，早停
        elif score < self.best_score+self.delta:
            self.counter+=1
            print(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter>=self.patience:
                self.early_stop = True
        # 若当前epoch表现超过历史最佳分数，更新best_score，保存该节点模型
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model)
            self.counter = 0

    def save_checkpoint(self, val_loss, model):
        # 保存模型
        if self.verbose:
            print(
                f'Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}).  Saving model ...')
        paddle.save(model.state_dict(), self.ckp_save_path)
        self.val_loss_min = val_loss

# unix时间戳转换
def to_unix_time(dt):
    # timestamp to unix
    epoch = datetime.datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds())

def from_unix_time(unix_time):
    # unix to timestamp
    return datetime.datetime.utcfromtimestamp(unix_time)

