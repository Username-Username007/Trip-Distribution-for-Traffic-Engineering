import numpy as np
import pandas as pd
import os

df = pd.read_excel(os.path.dirname((__file__))+"\\OD.xlsx",
     index_col=0, header = 0)   #读入原始OD矩阵
err = 0.03      # 指定误差
o_ratio = 2     # 先瞎初始化
d_ratio = 2     # 先瞎初始化, 进行迭代
n_iter = 0
while(  np.any(   np.logical_or(np.abs(o_ratio-1)>err , np.abs(d_ratio-1)>err)     )    ):
    #↑ 判断是否达到误差要求

    dfa = np.array(df).copy()
    o_ratio = np.array(df['new sum']/df['sum'])[:-2]
    d_ratio = np.array(df.loc['new sum']/df.loc['sum'])[:-2]

    Li = np.zeros((df.shape[0]-2, ))    
    Lj = np.zeros((df.shape[0]-2, ))
    for i in range(Li.shape[0]):
        Li[i] = df['sum'].iloc[i]/np.sum(dfa[i, 0:-2]*d_ratio)  #  计算Li
        Lj[i] = df.loc['sum'].iloc[i]/np.sum(dfa[0:-2, i]*o_ratio)  #计算Lj
    print(np.round(Li, 3), np.round(Lj, 3))   #输出Li, Lj
    Q = np.zeros((Li.size, Li.size))
    for i in range(Li.size):
        for j in range(Li.size):
            Q[i, j] = dfa[i, j]*o_ratio[i]*d_ratio[j]*(Li[i]+Lj[j])/2   #计算新的OD
            df.iat[i, j] = Q[i, j]  
        df.iat[i, j+1] = np.sum(Q[i, :])    #保存total O

    df.iloc[i+1, :-2] = df.iloc[:-2, :-2].sum() #保存total D
    o_ratio = np.array(df['new sum']/df['sum'])[:-2]    #再次计算增长系数
    d_ratio = np.array(df.loc['new sum']/df.loc['sum'])[:-2]    #增长系数
    print(np.round(Q, 3))
    print(f"{np.abs(np.abs(o_ratio-1)).max()*100:.2f}%")    #输出最大的增长系数与1的差
    print(f"{np.abs(np.abs(d_ratio-1)).max()*100:.2f}%")
    n_iter+=1
    print(f"Time of iteration: {n_iter}")


print("Final Result:")
print(df)
