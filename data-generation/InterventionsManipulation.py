# -*- coding: utf-8 -*-
"""
Created on Sun Jun 07 09:26:12 2015

@author: agitzes
"""
import pandas

def intervention2state(df):
    StartEnd={}    
    for i in df.columns:
        for k in range(0,len(df.drop_duplicates(subset=i)[i])):
            StartEnd[i,k]={"Start":df.drop_duplicates(subset=i,take_last=False).index[k],
            "End": df.drop_duplicates(subset=i,take_last=True).index[k]}
    df2=pandas.DataFrame(columns=["Type","Label","Start","End"])
    n=0
    for i in StartEnd:
        d={"Type":i[0], "Label":i[1],"Start":StartEnd[i]["Start"], "End":StartEnd[i]["End"]}
        ind=[n]
        df3=pandas.DataFrame(data=d, index=ind)
        df2=df2.append(df3, ignore_index=True)
    return df2