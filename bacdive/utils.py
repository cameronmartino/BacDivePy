import string
import numpy as np
import pandas as pd

def check_allow(mystring):
    allowed = string.ascii_letters + string.digits + ' '
    return all(c in allowed for c in mystring)


def pullopt(v1_,v2_,index,cond):
    """ Cleans Continous data"""
    res = {}
    for v1,v2,ind_ in zip(v1_,v2_,index):
        if  type(v1)!=float:
            if cond in v2:
                res[ind_] = v1[v2.index(cond)]
            else:
                res[ind_] = v1[0]
            res[ind_] = res[ind_].replace('<','0-').replace(', nan','').replace('nan,','')
            res[ind_] = res[ind_].replace('>','').replace('g/L','')                
            if '-' in res[ind_]:
                range_ = res[ind_].split('-')
                if '.'==range_[0][-1]:
                    range_[0] = range_[0][:-1]
                res[ind_] = np.mean(np.arange(float(range_[0]),
                                              float(range_[1])))
            res[ind_] = str(res[ind_])
        else:
            res[ind_] = np.nan
    return pd.Series(res)