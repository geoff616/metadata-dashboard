# -*- coding: utf-8 -*-
"""
Created on Sun Jun 07 11:59:17 2015

@author: agitzes
"""

#Take data from elastic search.  Based on index and type send data to appropriate data 
#manipulation function

for data in big_dict.keys():
    events = big_dict[data]


#Global Meta Data
#Transform all categorical data to binary columns

    if data.split('_')[0] == 'metadata':
        df =DataFrame(events)
        df = transform2Binary(df)
        
        
#Intervention
#Transform Data to start and end dates of each intervention Type|Label|Start|End
#build a during time series that is 0 before intervention and 1 during for each intervention
#build an after time series that  is 0 during intervention and 1 after intervention
        if data.split('_')[0] == 'intervention':
        df = DataFrame(events)
        df = intervention2state(df,data.split('_')[1] )
        df2=state2binaries      

#Business Event data
#Aggregate to day level Day|#of visitors|$Spent|Time on Slope
    if data.split('_')[0] == 'segment':
        df = DataFrame(events)
        df=aggregate(df)

#Place output into dict of Dfs
    to_index[data] = df 

#For each intervention, separately join intervention ts to metadata, run regression model, see lift caused by binary 1's
liftdict={}
for i in to_index:
    if i is binary intervention ts
    join to metadata
    model.fit(joinedmetadata, outcome variable)
    liftdict[i]=model.score(), model.significance
    
#Output sorted lift and significance of lift for during and after time periods for each intervention to highlight what best interventions were
sorting algo on liftdict




