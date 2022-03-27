import pandas as pd
import numpy as np
import os
def Furness(df, err = 0.01):
    df = np.array(df)
    n_nodes = df.shape[0]-1
    O_sum = df[:-1, :-1].sum(axis = 1)
    ratio = df[:-1, -1]/O_sum
    niter = 0
    while(np.abs(ratio-1).min()>err):
        df[:n_nodes, :n_nodes]*=ratio[:, None]

        D_sum = df[:-1, :-1].sum(axis = 0)
        ratio = df[-1, :-1]/D_sum
        print(f"{np.abs(ratio-1).max()*100:.2f}%")
        print(pd.DataFrame(df))
        if(np.abs(ratio-1).max()<= err):
            break
        df[:n_nodes, :n_nodes]*=ratio[None, :]
        O_sum = df[:-1, :-1].sum(axis = 1)
        ratio = df[:-1, -1]/O_sum
        print(f"{np.abs(ratio-1).max()*100:.2f}%")
        print(pd.DataFrame(df))
        #input("Continue...")
        niter+=1
        print(f"Time of iteration: {niter}")
    
    return df
try:
    path = os.path.dirname(__file__)
except NameError as e:
    print(e)
    path = R"D:\pyc\PythonTest\PythonTest\traffic_planning"


df = pd.read_excel(path+"\\gravity.xlsx", header = 0, index_col = 0)

n_nodes = df.shape[0]-1
F  = lambda x: np.exp(-0.1*x)
f_cost = F(df.iloc[:n_nodes, :n_nodes])
total_trip = df.iloc[-1, :n_nodes].sum()
total_f_cost = f_cost.sum().sum()
#print(total_trip)
df.iloc[:n_nodes, :n_nodes] = f_cost* total_trip/total_f_cost

df = pd.DataFrame(np.round(Furness(df), 3))
df.index = range(1, df.shape[0]+1)
df.columns = range(1, df.shape[1]+1)
df.rename(index={df.shape[0]:"sum"}, columns={df.shape[0]:"sum"}, inplace=True)
print(df)
