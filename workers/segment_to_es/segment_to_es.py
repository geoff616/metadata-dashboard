from datetime import datetime
from elasticsearch import Elasticsearch
from iron_mq import IronMQ
from json import loads


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
segment_queue = ironmq.queue("segment")

#iterate over things waiting in the queue
for i in range(segment_queue.info()['size']):
    #get next event off queue
    data = segment_queue.get()
    try:
        #get rid of cruft
        event = data['messages'][0]
        #id to delete on sucessful write
        queue_id = event['id']
        #interesting things
        body = loads(event['body'])
        
        doc = {}
        #check if this is a track event
        if 'event' in body:
            doc_type = body['event']
            doc['properties'] = body['properties']
            #TODO: confirm if date is upper/lower case
            if 'date' in body['properties']:
                doc['timestamp'] = datetime.strptime(body['properties']['date'], '%Y-%m-%d')
            else:
                doc['timestamp'] = datetime.strptime(body['properties']['Date'], '%Y-%m-%d')
        #otherwise it is identify TODO: clean this up to handle different types 
        else:
            doc_type =  'identify'
            doc['traits'] = body['traits']

        
        doc['userId'] = body['userId']
        
        
        res = es.index(index='new-segment', doc_type=doc_type, id=queue_id, body=doc)
        if res['created'] == True:
            print 'success'
            segment_queue.delete(queue_id)
    except:
        #ugh errors
        print 'error'
        print data


