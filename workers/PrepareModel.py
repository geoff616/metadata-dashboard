# -*- coding: utf-8 -*-
"""
Created on Sun Jun 07 09:44:17 2015

@author: agitzes
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 07 07:52:27 2015

@author: agitzes
"""
## This function performs the transformation of all three datasets not just the transformation to binary as
## the name of this script suggests

from datetime import datetime
from elasticsearch import Elasticsearch
from iron_mq import IronMQ
from json import loads
from pandas import DataFrame
from time import time

def handleEvent(result):
    temp = result['_source'] 
    return temp

def handleIdentify(result):
    temp = result['_source'] 
    return temp
    
def handleTrack(result):
    temp = result['_source']
    return temp

#convert categorical data to binary
def transform2Binary(df):
    for i in df.columns:
        if df[i].dtype not in ("int64", "float64", "datetime64[ns]"):
            for k in df[i].value_counts().index:
                Example= df[i]==k
                df[k]=0
                df[k][Example]=1
            df.drop(i,inplace=True,axis=1)
    return df

#def aggregate(df):
    #TODO: write aggregation function
    #df.pivot_table('')          

def intervention2state(df, Type):
    StartEnd={}    
    for i in df.columns:
        for k in range(0,len(df.drop_duplicates(subset=i)[i])):
            StartEnd[i,k]={"Start":df.drop_duplicates(subset=i,take_last=False).index[k],
            "End": df.drop_duplicates(subset=i,take_last=True).index[k]}
    df2=pandas.DataFrame(columns=["Type","Label","Start","End"])
    n=0
    for i in StartEnd:
        d={"Type":Type, "Label":i[1],"Start":StartEnd[i]["Start"], "End":StartEnd[i]["End"]}
        ind=[n]
        df3=pandas.DataFrame(data=d, index=ind)
        df2=df2.append(df3, ignore_index=True)
    return df2        
    
def aggregate(df):
     # TODO: test that this does what it should
     df["timestamp"] = pandas.to_datetime(df["timestamp"])
     outputs = pandas.pivot_table(df, values=["hours-spent", "price"], index="timestamp",
                          aggfunc=sum)
     user_count = pandas.pivot_table(df, index="timestamp", aggfunc="count")
     outputs=outputs.join(user_count)
     return outputs


big_dict = {}    
    
#connection to es cluster
es = Elasticsearch(['http://58d3ea40c46e8b15000.qbox.io:80'])

indexes = ['intervention', 'metadata', 'segment']

for ind in indexes:

    res = es.search(index=ind, body={"query": {"match_all": {}}, "size" : 1000000})

    for doc in res['hits']['hits']:
        new_key = doc['_index'] + '_' + doc['_type']
                
        if doc['_index'] == 'segment':

            if doc['_type'] == 'identify':
                #new_doc = handleIdentify(doc)
                a = 1
            else:
                new_doc = handleTrack(doc)
        
        else:
            new_doc = handleEvent(doc)
        
        if new_key in big_dict:
            big_dict[new_key].append(new_doc)
        else:
            big_dict[new_key] = [new_doc]

     
to_index = {}        
#for each type, create a df to manipulate
for data in big_dict.keys():
    print data
    events = big_dict[data]
    print len (events)
    if data.split('_')[0] == 'metadata':
        df =DataFrame(events)
        df.timestamp=pandas.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)
        df = transform2Binary(df)
        
        
    if data.split('_')[0] == 'intervention':
        df = DataFrame(events)
        df.timestamp=pandas.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)
        df = intervention2state(df,data.split('_')[1] )
        
    if data.split('_')[0] == 'segment':
        df = DataFrame(events)
        df=aggregate(df)

     
    to_index[data] = df 
    
        
        
        
    

    