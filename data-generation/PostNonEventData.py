# -*- coding: utf-8 -*-
"""
Created on Sat Jun 06 17:11:53 2015

@author: agitzes
"""

from datetime import datetime
from elasticsearch import Elasticsearch
from iron_mq import IronMQ
import pandas
import string
import json

datadir='~/metadata-dashboard/data-generation/'


#connection to es cluster
es = Elasticsearch(['http://58d3ea40c46e8b15000.qbox.io:80'])

#initiate ironmq connection
ironmq = IronMQ(host="mq-aws-us-east-1.iron.io",
            project_id="557330ae33f0350006000040",
            token="JZsM3ArjIhEfiKlG52Bt99b7Hh4",
            protocol="https", port=443,
            api_version=1,
            config_file=None)

#specify the queue where seqment is writing 
eventqueue = ironmq.queue("event-stream")



Trends=pandas.read_csv(datadir+"GlobalmetadataTrends.csv",index_col=0)
interventions=pandas.read_csv(datadir+"intervention.csv",index_col=0)
weather=pandas.read_csv(datadir+"Globalmetadataweather.csv",index_col=0)
CompPrice=pandas.read_csv(datadir+"Globalmetadataweather.csv",index_col=0)



for i in range (0,len(interventions)):



    Promotions = {
    "Index" : "intervention",
    "Date" : string.split(str(interventions.index[i])," ")[0],
    "Type" : "promotion",
    "Properties": {"Value" : interventions.Promotion.iloc[i]}

    }
    
    Campaigns = {
    "Index" : "intervention",
    "Date" : string.split(str(interventions.index[i])," ")[0],
    "Type" : "campaign",
    "Properties": {"Value" : interventions.Campaign.iloc[i]}
    
    }
    
    Catastrophe = {
    "Index" : "intervention",
    "Date" : string.split(str(interventions.index[i])," ")[0],
    "Type" : "campaign",
    "Properties": {"Value" : interventions.Catastrophe.iloc[i]}
    }
    
    eventqueue.post(json.dumps(Promotions, default=str))
    eventqueue.post(json.dumps(Campaigns,default=str))
    eventqueue.post(json.dumps(Catastrophe,default=str))


for i in range(0,len(weather)):
    Properties={}
    for k in weather.columns:
        Properties[k] = weather[k].iloc[i]
    Measure = {
    "Index" : "metadata",
    "Date" : string.split(str(weather.index[i])," ")[0],
    "Type" : "weather",
    "Properties": Properties}
    
    eventqueue.post(json.dumps(Measure, default=str))
    
for i in range(0,len(Trends)):
    Properties={}
    for k in Trends.columns:
        Properties[k] = Trends[k].iloc[i]
    Measure = {
    "Index" : "metadata",
    "Date" : string.split(str(Trends.index[i])," ")[0],
    "Type" : "trends",
    "Properties": Properties}
    
    eventqueue.post(json.dumps(Measure, default=str))
    
for i in range (0, len (CompPrice)):
    Measure = {
    "Index" : "metadata",
    "Date" : string.split(str(CompPrice.index[i])," ")[0],
    "Type" : "comp-price",
    "Properties": {"Value":CompPrice.iloc[i]}}

    eventqueue.post(json.dumps(Measure,default=str))

 
       
        
        
    
    