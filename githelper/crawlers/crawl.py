import requests
import json
import time
from time import sleep
import urllib2
import oauth2 as oauth

CONSUMER_KEY = 'e0adbda1070c1405660f'
CONSUMER_SECRET = '0b544c49c4189ac11712d77d14853fb3440922c2'

num_of_repos = [659, 547, 1339, 1740, 983, 2210, 475, 8821, 3845, 471]


list_of_classes = ['cloud+computing', 'computer+networks', 'data+mining',
                   'distributed+systems', 'facebook+application',
                    'ios+application', 'android+application', 'information+retrieval',
                    'machine+learning', 'natural+language+processing',
                    'wireless+Networks', 'High+Performance+computing', 'Image+processing',
                   'pattern+recognition', 'web+development', 'character+recognition',
                   'database+systems', 'twitter+applications', 'google+applications',
                   'computer+vision', 'signal+processing', 'linux+applications',
                   'operating+systems', 'video+applications', 'audio+applications',
                   'music+applications']


def process_query(query):
    global num_of_req
    global start_time
    out = open(query, 'w')
    list_of_repoItems = []
    pagecount = 1
    access_token = '94038d59a46c5ea1aa4f11626a83cde3e8794668'
    while True:
        num_of_req += 1
        print num_of_req
        data = {'94038d59a46c5ea1aa4f11626a83cde3e8794668':'x-oauth-basic'}

        repo_url = 'https://api.github.com/search/repositories?page='+\
                    str(pagecount)+'&per_page='+str(100)+'&q=' \
                    + query + '&ref=searchresults&sort=stars'  \
                    + '&client_id=32b67d9db6a9c7c7fd62&client_secret=4c15f439c7288a0a4de840b2c030474852fec0f2'

        r = requests.get(repo_url, params=data)
        if r.ok:
            print r
            pagecount += 1
            totaldata = json.loads(r.text or r.content)
            if len(totaldata['items']) > 0:
                print len(list_of_repoItems)
                list_of_repoItems += totaldata['items']
                print 'Total number of repos now ', len(list_of_repoItems)
            else:
                print 'Dumping', len(list_of_repoItems)
                json.dump(list_of_repoItems, out)
                return
        else:
            print r, 'sleeping', r.text
            if r.status_code == 422:
                pagecount+=1
                print 'Dumping', len(list_of_repoItems)
                json.dump(list_of_repoItems, out)
                return
            else:
                sleep(60)

count = 0
num_of_req = 0
start_time = time.time()
for each in list_of_classes:
    print 'processing', each

    process_query(each)
    count += 1
