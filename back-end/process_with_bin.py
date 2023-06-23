import bin
import pandas as pd
import numpy as np

def neg_process(series: pd.Series):
    if not np.isnan(series["YD15"]) and series["YD15"] < 0:
        series["YD15"] = 0
    if not np.isnan(series["ROUND(A.WS,1)"]) and series["ROUND(A.WS,1)"] < 0:
        series["ROUND(A.WS,1)"] = 0
    return series

def nan_process(series: pd.Series, avg: pd.Series, r: pd.Series):
    if np.isnan(series["ROUND(A.WS,1)"]) and np.isnan(series["YD15"]):
        if not np.isnan(series["ROUND(A.POWER,0)"]):
            series["YD15"] = (series["ROUND(A.POWER,0)"] - avg["ROUND(A.POWER,0)"]) / r["ROUND(A.POWER,0)"] * r["YD15"] + avg["YD15"]
        elif not np.isnan(series["WINDSPEED"]):
            series["ROUND(A.WS,1)"] = (series["WINDSPEED"] - avg["WINDSPEED"]) / r["WINDSPEED"] * r["ROUND(A.WS,1)"] + avg["ROUND(A.WS,1)"]

    return series

def bin_process(df: pd.DataFrame, x_Min, x_Max, y_Mean, y_std, step, x, y, r):
    N_Number = int((x_Max - x_Min) / step) + 1
    df_list=[]
    for i in range(N_Number):
        in_index = (df[x] > (x_Min + i * step)) & (df[x] <= (x_Min + (i + 1) * step)) & (df[y]< (y_Mean[i] + y_std[i] * r)) & (df[y] > (y_Mean[i] - y_std[i] *r))
        #print()
        # in_range = df[in_index]

        #df.drop(df[in_index].index,inplace=True)
        df_list.append(df[in_index])

    return pd.concat(df_list)


def clean_dead_value(series, num_dead_thresh):
    """
    :param series: 目标dataframe某个序列值
    :param num_dead_thresh: 判断死值的阈值
    :return: 每个计算周期内需要删除的行数列表
    """
    slide_list = [series.index[0]]
    slide_list_all = []
    for i in range(series.index[0],series.index[-1]):
        j = i + 1
        diff = series[j] - series[i]
        if diff == 0:
            slide_list.append(j)
        else:
            slide_list.clear()
            slide_list.append(j)
        # print("slide_list:",slide_list)
        if len(slide_list) >= num_dead_thresh:
            target_list = slide_list.copy()
            slide_list_all.append(target_list)
    #print("slide_list_all:",slide_list_all)
    index= []  # 将找到的满足条件的index合并
    # 因为可能有前后包含的情况，只保留最长序列
    for i in range(len(slide_list_all) - 1):
        if set(slide_list_all[i]) < set(slide_list_all[i + 1]):
            index.append(i)
    m = {i: element for i, element in enumerate(slide_list_all)}
    [m.pop(i) for i in index]
    # 将所有需要删除的行数合并
    indexs_to_delete = []
    for i in range(len(slide_list_all)):
        indexs_to_delete = list(set(indexs_to_delete).union(slide_list_all[i]))
    return indexs_to_delete


def process_with_bin(df: pd.DataFrame, stepx=0.2, range_x=2):
    for c in ['ROUND(A.WS,1)','YD15']:
        index=clean_dead_value(df[c],3)
        df.loc[index,c]=np.nan

    df=df.apply(neg_process,axis=1)
    data=df.dropna(subset=['ROUND(A.WS,1)','YD15'])

    x_Mean, y_Mean, y_std = bin.bin_data(data['ROUND(A.WS,1)'].values, data['YD15'].values, stepx)
    data = bin_process(data, data['ROUND(A.WS,1)'].min(), data['ROUND(A.WS,1)'].max(), y_Mean, y_std, stepx,
                       'ROUND(A.WS,1)', 'YD15', range_x)

    return data