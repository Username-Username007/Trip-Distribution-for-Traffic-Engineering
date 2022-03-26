import pandas as pd
import numpy as np
"""
    The format of input matrix:
        If there are N nodes, it must be N+2 columns and rows
        The proceeding N columns and rows are the trip matrix.
        N+1 column and row are the sum of the trip for Origin and Destination.
        N+2 column and row are the sum of the future trip for Origin and Destination.
        (all the indices are 1-based)
"""
path = R"D:\pyc\PythonTest\PythonTest\traffic_planning\\"

df = pd.read_excel(path+"OD.xlsx", sheet_name=0, header = 0, index_col=0)
err = 0.03
o_newsum = np.array(df.iloc[:-2,-1])
d_newsum = np.array(df.iloc[-1,:-2])

Q = np.array(df.iloc[:-2, :-2])

o_sum = Q.sum(axis = 1)
d_sum = Q.sum(axis = 0)
o_ratio = o_newsum/o_sum
d_ratio = d_newsum/d_sum

n_iter = 0
while(True):

    Li = o_sum/(Q*d_ratio[None, :]).sum(axis=1)
    Lj = d_sum/(Q*o_ratio[:, None]).sum(axis=0)

    Q = Q*o_ratio[:, None]*d_ratio[None, :]*(Li[:, None]+Lj[None, :])/2
    o_sum = Q.sum(axis = 1)
    d_sum = Q.sum(axis = 0)
    o_ratio = o_newsum/o_sum
    d_ratio = d_newsum/d_sum
    n_iter+=1
    print(f"Number of iteration: {n_iter}")
    print(np.round(Q, 3))
    print(f"F_D = ", np.round(d_ratio, 3))
    print("F_O = ", np.round(o_ratio, 3))
    print("")
    if(np.abs(o_ratio-1).max() <= err and np.abs(d_ratio-1).max()<=err):
        break
print("Final result:")
print('\t', str(np.round(Q, 0).astype(int)).replace('\n', '\n\t'))
print("Total destination:")
print('\t', np.round(Q.sum(axis=0), 0).astype(int))
print("Total origin:")
print('\t', np.round(Q.sum(axis=1), 0).astype(int))
