##############################################################################
#################### Author: Midhun Chinta ###################################
#################### UIN   : 722005998     ###################################
#################### Leaning to rank       ###################################
##############################################################################

from sklearn.cross_validation import KFold
import sys
import operator
import itertools
from scipy.sparse import *
from sklearn import svm
from sklearn import cross_validation

trfend = '/train.txt'
tefend = '/test.txt'
resultf = open('result', 'w')
num_of_features = 46
clf = svm.LinearSVC(C=30.0)
ind = 0
xtrlist = []
ytrlist = []
xtelist = []
ytelist = []

def get_valid_pairs(list_of_rel):
    subsets = set(itertools.combinations(range(len(list_of_rel)),2))
    rsubsets = set()
    for subset in subsets:
        ele = list(subset)
        if(not(list_of_rel[ele[0]] == list_of_rel[ele[1]])):
            rsubsets.add(subset)
    return rsubsets

#for every unique query process the list of all its docs
def processtrdocs(list_of_docs, list_of_rel):
    global xtrlist
    global ytrlist
    pairs = get_valid_pairs(list_of_rel)
    numofpairs = len(pairs)
    for pair in pairs:
        #create two entries in pairmat
        ele = list(pair)
        if(list_of_rel[ele[0]]>list_of_rel[ele[1]]):
            value = 1
        else:
            value = -1
        temp = list_of_docs[ele[0]]
        currvector = [0.0]*len(temp)
        currrev = [0.0]*len(temp)
        for each in range(len(temp)):
            currvector[each] = temp[each] - list_of_docs[ele[1]][each]
            currrev[each] = list_of_docs[ele[1]][each] - temp[each] 
        xtrlist.append(currvector)
        xtrlist.append(currrev)
        ytrlist.append(value)
        ytrlist.append(-1*value)

def processtedocs(list_of_docs, list_of_rel):
    global xtelist
    global ytelist
    pairs = get_valid_pairs(list_of_rel)
    numofpairs = len(pairs)
    for pair in pairs:
        #create two entries in pairmat
        ele = list(pair)
        if(list_of_rel[ele[0]]>list_of_rel[ele[1]]):
            value = 1
        else:
            value = -1
        temp = list_of_docs[ele[0]]
        currvector = [0.0]*len(temp)
        currrev = [0.0]*len(temp)
        for each in range(len(temp)):
            currvector[each] = temp[each] - list_of_docs[ele[1]][each]
            currrev[each] = list_of_docs[ele[1]][each] - temp[each] 
        xtelist.append(currvector)
        xtelist.append(currrev)
        ytelist.append(value)
        ytelist.append(-1*value)

#for each of training data set, train the data query wise 
def train(dirname):
    global xtrlist
    global ytrlist
    print 'Training', dirname
    trfname = dirname+trfend
    trfile = open(trfname, 'r')
    set_of_queries = set()
    curr_list_of_docs = []
    curr_list_of_rel = []
    for line in trfile:
        currdoc = [0.0] * num_of_features
        words = line.split()
        if(words[1] not in set_of_queries):
            #New query!! Process the list of docs of prev query if present
            set_of_queries.add(words[1])
            if(len(curr_list_of_docs)):
                processtrdocs(curr_list_of_docs, curr_list_of_rel)
                curr_list_of_docs = []
                curr_list_of_rel = []
        index = 0
        for word in words:
            if(index<2):
                index = index+1
                continue
            attr = word.split(':')
            currdoc[int(attr[0])-1] = float(attr[1])
        curr_list_of_docs.append(currdoc)
        curr_list_of_rel.append(int(words[0]))
    #all lines in trainind data set parsed: Now its time to learn
    scores = cross_validation.cross_val_score(clf, xtrlist, ytrlist, cv=5)
    clf.fit(xtrlist, ytrlist)
    coeff = clf.coef_
    abscoeff = {}
    revmap = {}
    index = 0
    for each in coeff[0]:
        abscoeff[each] = abs(each)
        revmap[each] = index+1
        index = index+1
    #print coeff
    sorted_results = sorted(abscoeff.iteritems(), key=operator.itemgetter(1), reverse = True)
    index = 0
    str1 = ''
    for val1, val2 in sorted_results:
        str1 = str1+str(revmap[val1])+':'+str(val1)+'\n'
        index = index+1
        if(index>10):
            break
    print 'Top 10 features for ', dirname
    print str1
    xtrlist = []
    ytrlist = []

def test(dirname):
    global xtelist
    global ytelist
    print 'Testing ', dirname
    tefname = dirname+tefend
    tefile = open(tefname, 'r')
    set_of_queries = set()
    curr_list_of_docs = []
    curr_list_of_rel = []
    for line in tefile:
        currdoc = [0.0] * num_of_features
        words = line.split()
        if(words[1] not in set_of_queries):
            #New query!! Process the list of docs of prev query if present
            set_of_queries.add(words[1])
            if(len(curr_list_of_docs)):
                processtedocs(curr_list_of_docs, curr_list_of_rel)
                curr_list_of_docs = []
                curr_list_of_rel = []
        index = 0
        for word in words:
            if(index<2):
                index = index+1
                continue
            attr = word.split(':')
            currdoc[int(attr[0])-1] = float(attr[1])
        curr_list_of_docs.append(currdoc)
        curr_list_of_rel.append(int(words[0]))
    predict = clf.predict(xtelist)
    corr = 0
    for each in range(len(predict)):
        if(predict[each] == ytelist[each]):
            corr = corr+1
    print 'Accuracy %.2f \n' % ((1.0*corr)/(len(predict)))
    xtelist = []
    ytelist = []

#Process all the folders[train n test]
def processall(argve):
    print 'Using Linear SVC:'
    for index in range(len(argve)-1):
        train(argve[index+1])
        test(argve[index+1])
        clf = svm.LinearSVC(C=30.0)
    print '\n\n\nUsing SVC(kernel = Linear)'
    for index in range(len(argve)-1):
        clf = svm.SVC(C=30.0, kernel = 'linear')
        train(argve[index+1])
        test(argve[index+1])
    return

def main(argv):
    if(len(sys.argv)<4):
        print 'usage learn.py <dir1> <dir2> <dir3>'
    processall(sys.argv)
    return 0

if(__name__ == '__main__'):
    sys.exit(main(sys.argv))
