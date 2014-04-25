import oauth2 as oauth
import json
import tweepy
import sys
import re
import math
import random


CONSUMER_KEY      = None
CONSUMER_SECRET   = None

ACCESS_KEY        = None
ACCESS_SECRET     = None

def api_search(query):
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
    client = oauth.Client(consumer, access_token)
    timeline_endpoint = "https://api.twitter.com/1.1/search/tweets.json?q=i" + query + "&rpp=100"
    response, data = client.request(timeline_endpoint)
    tweets = json.loads(data)
    print len(tweets['statuses'])
   
def tweepy_search(query):
    if CONSUMER_KEY == None or CONSUMER_SECRET == None :
        print "No consumer key or secret"
        sys.exit(-1)
        return
    if ACCESS_KEY == None or ACCESS_SECRET == None:
        print "No access key or secret"
        sys.exit(-1)
        return
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    count  = 0
    currTweets = ''
    for tweet in tweepy.Cursor(api.search,
                                q=query,
                               count=100,
                               result_type="recent",
                               exclude="retweets",
                               include_entities=True,
                               lang="en").items():
        count = count+1
        currTweets = currTweets + ' ' + tweet.text.lower()
        if(count%50 == 0):
            return  currTweets

def collect_tweets(queries):
    tweetDict = {}
    tweetFile = open('tweetData', 'w')
    tweetDict = {}
    for query in queries:
        print 'Collecting', query
        tweetDict[query] = tweepy_search(query)
    #json.dump(tweetDict,tweetFile)
    return tweetDict

def calcTfIDFTokens(tweetData, totalTokens):
   print 'Num of tokens', len(totalTokens)
   N = len(totalTokens)
   newtweetData = {}
   for query, queryDict in tweetData.items():
       for token in queryDict:
           queryDict[token] = (1 + math.log10(queryDict[token])) * math.log10((N*1.0)/len(totalTokens[token]))
       newtweetData[query] = queryDict
   return newtweetData


def process_tweets(tweetData):
    totalTokens = {}
    for query, queryData in tweetData.items():
        print 'Processing', query
        queryDict = {}
        queryData = re.sub(r'^https?:\/\/.*[\r\n]*', '', queryData, flags=re.MULTILINE)
        queryTokens = re.findall(r"[\w]+", queryData, re.UNICODE)
        for token in queryTokens:
            try:
                queryDict[token] = queryDict[token]+1
            except:
                queryDict[token] = 1
            try:
                totalTokens[token].add(query)
            except:
                totalTokens[token] = set()
                totalTokens[token].add(query)
        tweetData[query] = queryDict
    tweetData = calcTfIDFTokens(tweetData, totalTokens)
    return tweetData, totalTokens

def getClosestCentroideuclidean(data, clusters):
    nearestCentroid = clusters[0]
    minDistance = 1.7976931348623157e+308
    for cluster in clusters:
        totalTokens = set(cluster.keys())
        totalTokens = totalTokens.union(set(data.keys()))
        currDistance = 0.0
        for token in totalTokens:
            if(token in data and token in cluster):
                diff = data[token] - cluster[token]
            elif(token in data):
                diff = data[token]
            else:
                diff = cluster[token]
            currDistance = currDistance + diff * diff
        if(currDistance < minDistance):
            minDistance = currDistance
            nearestCentroid = cluster
    return clusters.index(nearestCentroid)

def getClosestCentroid(data, clusters):
    nearestCentroid = clusters[0]
    maxsimilarity = 0.0
    for cluster in clusters:
        clusternormal = 0.0
        datanormal = 0.0
        for token in set(cluster.keys()):
            clusternormal = clusternormal + cluster[token] * cluster[token]
        for token in set(data.keys()):
            datanormal = datanormal + data[token] * data[token]
        clusternormal = math.sqrt(clusternormal)
        datanormal = math.sqrt(datanormal)
        totalTokens = set(cluster.keys())
        totalTokens = totalTokens.intersection(set(data.keys()))
        currsimilarity = 0.0
        for token in totalTokens:
            currsimilarity = currsimilarity + cluster[token] * data[token]
        currsimilarity = currsimilarity/(clusternormal * datanormal)
        if currsimilarity > maxsimilarity:
            maxsimilarity = currsimilarity
            nearestCentroid = cluster
    return clusters.index(nearestCentroid)


def getNewCentroid(clusterData):
    numOfDocs = len(clusterData) * 1.0
    newCentroid = {}
    currTotalTokens = set()
    for query, queryDict in clusterData.items():
        currTotalTokens = currTotalTokens.union(set(queryDict.keys()))
    for token in currTotalTokens:
        newCentroid[token] = 0.0
        for query in clusterData.keys():
            try:
                newCentroid[token] = newCentroid[token]+clusterData[query][token]
            except:
                continue
        newCentroid[token] = newCentroid[token]/numOfDocs
    return newCentroid

def kCluster(tweetData, k):
    clusterList = []
    count = 0
    totalDocs = tweetData.keys()
    assignedDocs = []
    #Initialize cluster Centroids with k random documents
    while(count<k):
        randomDocNum = random.randrange(0, 32)
        randomDoc = totalDocs[randomDocNum]
        if(randomDoc not in assignedDocs):
            clusterList.append(tweetData[randomDoc])
            count = count+1
            assignedDocs.append(randomDoc)
    count = 0
    same = 0
    while count < 15:
        #Assign each document to nearest Centroid
        clusterDict = {}
        for clusterNum in range(len(clusterList)):
            clusterDict[clusterNum] = {}
        for query, queryDict in tweetData.items():
            closestCentroidIndex = getClosestCentroid(queryDict, clusterList)
            clusterDict[closestCentroidIndex][query]=queryDict
        #Compute New Centroids
        newclusterList = []
        for cluster in clusterList:
            clusterData = clusterDict[clusterList.index(cluster)]
            newcluster = getNewCentroid(clusterData)
            newclusterList.append(newcluster)
            if newcluster == cluster:
                same = same + 1
        if same == k:
            break
        clusterList = newclusterList
        count = count+1
    return True, clusterDict, clusterList

def calcprecision(clusterdict, queries, k):
    maxmatch = range(k)
    for clusternum in range(k):
        startindex = 0
        stopindex = 8
        maxmatch[clusternum] = 0.0
        for curr in range(4):
            currmatch = 0
            for queryindex in range(startindex, stopindex):
                if queries[queryindex] in clusterdict[clusternum].keys():
                    currmatch = currmatch + 1
            if maxmatch[clusternum] < currmatch:
                maxmatch[clusternum] = currmatch
            startindex = startindex + 8
            stopindex = stopindex + 8
    purity = 0.0
    for clusternum in range(k):
        purity = purity + maxmatch[clusternum]
    purity = purity/len(queries)
    return purity

def calcRSS(clusterDict, clusterList):
    rss = 0.0
    for clusterIndex in range(len(clusterList)):
        currcluster = clusterList[clusterIndex]
        clusterData = clusterDict[clusterIndex]
        for query in clusterData.keys():
            for token in clusterData[query].keys():
                diff = currcluster[token] - clusterData[query][token]
                rss = rss + diff * diff
    return rss

def main(argv):
    if(len(argv)<2):
        print 'Usage: python part2.py queries'
        sys.exit(0)
    fp = open(sys.argv[1], 'r')
    line = fp.read()
    queries = line.split(',')
    tweetData = collect_tweets(queries)
    tweetData, totalTokens = process_tweets(tweetData)
    #data = open('processed', 'r')
    #tweetData = json.load(data)
    kList = [2, 4, 6, 8]
    for k in kList:
        print 'Calling kCluster Algo with k = ', k
        result, clusterDict, clusterList = kCluster(tweetData, k)
        RSS = calcRSS(clusterDict, clusterList)
        print 'RSS', RSS
        for clusterNum in range(k):
            print clusterNum, '--', clusterDict[clusterNum].keys()
        print '\n\n\n'

if __name__ == "__main__":
    sys.exit(main(sys.argv))
