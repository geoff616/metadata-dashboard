import requests

#alternate search function to get all data from an index, increasing size will return all docs but is a more expensive query than scan/scroll
res = es.search(index="test-index", body={"query": {"match_all": {}}, "size" : 100})

def prettyDate(date):
    #TODO: confirm how this will work

def handleIdentify(result):
    #TODO confirm how this data will be structured 
    
def handleTrack(result):
    #TODO confirm how this data will be structured     
    

def scan(s_id, hits, num_shards, res, obj):
    
    results = res
    to_return = obj
    
    while results < hits:
        print results
    
        url = 'http://58d3ea40c46e8b15000.qbox.io:80/_search/scroll?search_type=scan&scroll=1m&scroll_id=' + s_id
        scroll = loads(requests.get(url).text)

        
        if '_scroll_id' and 'hits' in scroll:
            s_id = scroll['_scroll_id']
        else:
            print 'error with ' + results + ' of ' + hits + ' results'
            return

    
        #loop over results and index into to_return      
        for result in scroll['hits']['hits']:    
            #use new_key 
            new_key = result['_index'] + result['_type']
            
            if result['_index'] == 'segment':
            
                if result['_type'] == 'identify':
                    handleIdentify(result)
                else:
                    handleTrack(result)
            
            results += 1
        
        #call scan again
        scan(s_id, hits, num_shards, results, to_return)
            
url = 'http://58d3ea40c46e8b15000.qbox.io:80/_search?search_type=scan&scroll=10m&query'

#TODO: determine if a post body will help 
r = loads(requests.post(url).text)
if '_scroll_id' and 'hits' and '_shards' in r:
    s_id = r['_scroll_id']
    hits = r['hits']['total']
    num_shards = r['_shards']['total']
else:
    print 'scroll fail'

#magic numbers 0 passed to start results at zero, and empty object to be filled as return value
all_the_data = scan(s_id, hits, num_shards, 0, {})   

for df_type in all_the_data.keys():
    print df_type
    #list_of_events = all_the_data[df_type]
    

