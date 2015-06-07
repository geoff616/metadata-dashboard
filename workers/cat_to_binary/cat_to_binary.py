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
        if df[i].dtype not in ("int64", "float64", "datetime64"):
            for k in df[i].value_counts().index:
                Example= df[i]==k
                df[k]=0
                df[k][Example]=1
            df.drop(i,inplace=True,axis=1)
    return df

def aggregate(df):
    #TODO: write aggregation function
    return pivot_table(df, Values=["hours-spent", "price"], index="date",
                       aggfunc=sum)
big_dict = {}    
    
#connection to es cluster
es = Elasticsearch(['http://58d3ea40c46e8b15000.qbox.io:80'])

indexes = ['intervention', 'metadata', 'segment']

for ind in indexes:

    res = es.search(index=ind, body={"query": {"match_all": {}}, "size" : 100})

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
    events = big_dict[data]

    #TODO: confirm this function is doing what is expected
    if data.split('_')[0] == 'metadata':
        df = transform2Binary(DataFrame(events))
    elif data.split('_')[0] == 'segment':
        df = aggregate(DataFrame(events))
    else:
        #intervention data
        #TODO: do something exciting here
    to_index['data'] = df.to_json()
    
for data in to_index.keys():
    ti = str(time()).split('.')[0]
    es.index(index="cat-index", doc_type=data.lower(), id=ti, body=to_index[data])



