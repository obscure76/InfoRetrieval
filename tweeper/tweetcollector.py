import oauth2 as oauth
import json
import tweepy
import sys


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
        return
    if ACCESS_KEY == None or ACCESS_SECRET == None:
        print "No access key or secret"
        return
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    #results = api.search(q="Football", rpp = 100)
    #print len(results)
    count  = 0
    #api_search(query)
    for tweet in tweepy.Cursor(api.search,
                                q=query,
                                rpp=100,
                                result_type="recent",
                                include_entities=True,
                                exclude="retweets",
                                lang="en").items():
        count = count+1
        print count, ' )  ', tweet.created_at, tweet.text
        if(count%50 == 0):
            return
def main():
    while(1):
        print 'Enter the search query or exit '
        line = sys.stdin.readline()
        if(line == '\n'):
            continue
        if(line.split()[0] == 'exit'):
            sys.exit(0)
        print line
        tweepy_search(line)

if __name__ == "__main__":
    sys.exit(main())
