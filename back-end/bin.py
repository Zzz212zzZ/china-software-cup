import numpy as np

def bin_data(x, y, step):
    """
    x：风速
    y：YD15
    step：代表bin算法的单位长度，如果取1，代表风速被划分为以1单位为间隔的多个时间段
    """
    Start_X = np.min(x)

    N_Number = int((np.max(x) - Start_X) / step)+1
    AA = x
    BB = y
    x_Mean = [0 for _ in range(N_Number)]
    y_Mean = [0 for _ in range(N_Number)]
    y_std = [0 for _ in range(N_Number)]

    # 分段查找均值和标准差
    for i in range(N_Number):
        ID_Mea = np.flatnonzero((AA > (Start_X + i * step)) & (AA <= (Start_X + (i + 1) * step)))
        if ID_Mea.size>0:
            x_Mean[i] = AA[ID_Mea].mean()
            y_Mean[i] = BB[ID_Mea].mean()
            y_std[i] = BB[ID_Mea].std()
        else:
            x_Mean[i] = np.nan
            y_Mean[i] = np.nan
            y_std[i] = np.nan

    # 对标准差进行处理，此处不再对均值进行处理，因为可能不能算是好处理，和实际的偏差过大了
    num = 1
    for i in range(round(N_Number / 2), N_Number - 1):
        if y_std[i + 1] > 3 * np.mean(y_std[i - num:i]):
            y_std[i + 1] = y_std[i + 1] / 3

    return x_Mean, y_Mean, y_std