import sys
import cjson
import networkx as nx
import time
import numpy as np
from scipy.sparse import *
import numpy.matlib
import operator
import string

hubs = {}
auth = {}

myGraph = nx.DiGraph()
set_of_users = set()
list_of_users = {}
start_time = time.time()

def parse(filename):
    fp = open(filename)
    start_time = time.time()
    count = 0
    for line in fp:
        count = count+1
        jsonObj = cjson.decode(line)
        user = jsonObj['user']['screen_name']
        mentions_lod = jsonObj['entities']['user_mentions']
        #print user
        if user not in set_of_users:
            myGraph.add_node(user)
            set_of_users.add(user)
        for mention in mentions_lod:
            #print mention['screen_name']A
            if(mention == user):
                continue
            if mention['screen_name'] not in set_of_users:
                myGraph.add_edge(user, mention['screen_name'])
                set_of_users.add(mention['screen_name'])
            elif(myGraph.has_edge(user, mention['screen_name'])):
                pass
            else:
                myGraph.add_edge(user, mention['screen_name'])
        if(count%1000 == 0):
            pass
            #print count, 'lines ', 'users ', len(set_of_users), ' in ', time.time() - start_time 
    print 'corpus processed ', time.time()-start_time

def calculate_HandAMat(weakGraph):
    mat = open('matrix', 'w')
    print 'Weak nodes ', len(weakGraph.nodes())
    Nodes = len(weakGraph.nodes())
    GraphMat = np.matlib.zeros((Nodes, Nodes))
    HubsMat = np.matlib.zeros((Nodes,1))
    HubsMatTmp = np.matlib.zeros((Nodes,1))
    AuthMat = np.matlib.zeros((Nodes,1))
    AuthMatTmp = np.matlib.zeros((Nodes,1))
    for fuser, findex in list_of_users.items():
        HubsMat[findex,0] = 1.0/Nodes
        AuthMat[findex,0] = 1.0/Nodes
        list_of_successors = weakGraph.successors(fuser)
        for touser in list_of_successors:
            GraphMat[findex, list_of_users[touser]] = 1
    GraphCooMat = coo_matrix(GraphMat)
    itera = 0
    print 'Matrices made ', time.time()-start_time
    while(itera <500):
        itera = itera +1
        HubsMatTmp = GraphCooMat.tocsr() * AuthMat
        AuthMatTmp = HubsMat.transpose() * GraphCooMat.tocsr()
        if(abs(numpy.sum(HubsMatTmp/(HubsMatTmp.max())) - numpy.sum(HubsMat)) < .001):
            print itera
            break
        mat.write(str(abs(numpy.sum(HubsMatTmp/(HubsMatTmp.max())) - numpy.sum(HubsMat)))+'\t')
        HubsMat = HubsMatTmp/(HubsMatTmp.max())
        AuthMat = AuthMatTmp.transpose()/(AuthMatTmp.max())
    for user, index in list_of_users.items():
        hubs[user] = HubsMat[index,0]
        auth[user] = AuthMat[index,0]
    shubs = sorted(hubs.iteritems(), key=operator.itemgetter(1), reverse = True)
    sauth = sorted(auth.iteritems(), key=operator.itemgetter(1), reverse = True)
    hna = open('hna', 'w')
    hna.write('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    hna.write('\n\n      Hub Scores Sorted Top 20\n\n')
    hna.write('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n')
    index = 0
    for user, score in shubs:
        s = ("%s   %f \n" %(user, score))
        hna.write(s)
        if(index == 20):
            break
        index = index+1
    hna.write('\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    hna.write('\n\n      Auth Scores Sorted Top 20\n\n')
    hna.write('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n')
    index = 0
    for user, score in sauth:
        s = ("%s   %f \n" %(user, score))
        hna.write(s)
        if(index == 20):
            break
        index = index+1


def main(argv):
    if(len(sys.argv)<2):
        print 'usage <>.py <datafile>'
    parse(sys.argv[1])
    weakGraphs = nx.weakly_connected_component_subgraphs(myGraph)
    index = 0
    set_of_users = weakGraphs[0].nodes()
    print 'Got the Subgraph', time.time()-start_time
    for user in set_of_users:
        list_of_users[user] = index
        index = index+1
    calculate_HandAMat(weakGraphs[0])
    return 0


if(__name__ == '__main__'):
    sys.exit(main(sys.argv))

"""
jsonObj['entities']['user_mentions'] -- List of mentions
jsonOnj['user'] -- username

fields:
id
text
created_at
user
entities
"""
