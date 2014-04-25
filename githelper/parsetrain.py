import json
import sys
import os
import re
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.multiclass import OneVsOneClassifier
from sklearn import svm
from nltk.corpus import stopwords
import pickle
from sklearn import metrics

classmap = {'myandroiddd':'android+application', 'cloudd':'cloud+computing',
            'cnets':'computer+networks', 'data':'data+mining',
            'dsys':'distributed+systems', 'fb':'fb+application',
            'info':'information+retrieval', 'iosddd':'ios+application',
            'machinelearning':'machine+learning', 'nlppp':'natural+language+processing'}

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

rootdir = 'data-cache'

class Stripper:
    def __init__(self):
        pass

    def tokenize(self, data):
        return set(re.findall(r"[\w]+", data, re.UNICODE))

    def join(self, tokenset):
        totaltext = ''
        for token in tokenset:
            totaltext += (' ' + token)
        return totaltext


class Vectorizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(min_df=1)

    def vectorize(self, data):
        return self.vectorizer.transform(data)


class Classifier:
    def __init__(self):
        self.classifier = dimbu

    def train(self, X, Y):
        pass

    def test(self, X, Y):
        pass

    def classify(self, X):
        pass


def getcounts():
    global rootdir
    totalcounts = {}
    for root, subFolders, files in os.walk(rootdir):
        for filename in files:
            if filename.endswith('.ptext'):
                for line in open(os.path.join(root, filename)):
                    repolist = json.loads(line)
                totalcounts[filename] = len(repolist)
    return totalcounts


def dividedata():
    global rootdir
    global classmap
    totalcounts = getcounts()
    Xtrain = []
    Xtest = []
    Ytrain = []
    Ytest = []
    for root, subFolders, files in os.walk(rootdir):
        for filename in files:
            if filename.endswith('.ptext'):
                currcount = totalcounts[filename]
                traincount = int(0.7 * currcount)
                testcount = currcount - traincount
                for line in open(os.path.join(root, filename)):
                    repolist = json.loads(line)
                classindex = filename.replace('.ptext', '')
                count = 0
                for repo in repolist:
                    count += 1
                    if count < traincount:
                        Xtrain.append(repo['text'])
                        Ytrain.append(filename)
                    else:
                        Xtest.append(repo['text'])
                        Ytest.append(filename)
    return Xtrain, Xtest, Ytrain, Ytest


def parse_datasets():
    rootdir = 'data-cache'
    stripper = Stripper()
    stopwordset = set(stopwords.words('english'))
    for root, subFolders, files in os.walk(rootdir):
        for filename in files:
            try:
                if filename.endswith('.txt'):
                    newrepolist = []
                    print 'Processing', filename
                    filepath = os.path.join(root, filename)
                    for line in open(filepath, 'r'):
                        repolist = json.loads(line)
                    filename = filename.replace('.txt', '')
                    #Process the raw text and filter stopwords
                    for repo in repolist:
                        newrepo = {}
                        totaltext = ''
                        for key in repo.keys():
                            if key is not 'url':
                                totaltext = totaltext + repo[key]
                        newrepo['url'] = repo['url']
                        tokenset = stripper.tokenize(totaltext)
                        tokenset = tokenset.difference(stopwordset)
                        totaltext = stripper.join(tokenset)
                        newrepo['text'] = totaltext
                        newrepolist.append(newrepo)
                    pfilename  = filename + '.ptext'
                    pfile = open(os.path.join(root, pfilename), 'w')
                    json.dump(newrepolist, pfile)
            except:
                print filename
                print "unexpected error:", sys.exc_info()[0]
                raise


def myclassify(inputdata):
    #Parsing the datasets
    #parse_datasets()
    #Dividing the Datasets
    start_time = time.time()
    """
    vectorizer = TfidfVectorizer(min_df=1, max_features=1050)
    xtrain, xtest, ytrain, ytest = dividedata()
    print len(xtrain), len(xtest), type(xtrain)
    print 'Training data vectorized'
    xnptrain = vectorizer.fit_transform(xtrain)
    print 'Testing data vectorized'
    xnptest = vectorizer.transform(xtest)
    print type(xnptrain), type(xnptest), xnptrain.shape, xnptest.shape
    clfsvm = svm.LinearSVC(C=30.0)
    clfsvm.fit(xnptrain, ytrain)
    pred = clfsvm.predict(xnptest)
    score = metrics.f1_score(ytest, pred)
    print 'SVM', score
    clfnb = MultinomialNB()
    clfnb.fit(xnptrain, ytrain)
    pred = clfnb.predict(xnptest)
    score = metrics.f1_score(ytest, pred)
    print 'NB', score
    classifierfilesvm = open('classifiersvm', 'w')
    classifierfilenb = open('classifiernb', 'w')
    vectorizerfile = open('vectorizer', 'w')
    pickle.dump(vectorizer, vectorizerfile)
    pickle.dump(clfsvm, classifierfilesvm)
    pickle.dump(clfnb, classifierfilenb)
    """
    classifierfilesvm = open('classifiersvm', 'r')
    #classifierfilenb = open('classifiernb', 'r')
    vectorizerfile = open('vectorizer', 'r')
    clfsvm = pickle.load(classifierfilesvm)
    #clfnb = pickle.load(classifierfilenb)
    vectorizer = pickle.load(vectorizerfile)
    newnptest = vectorizer.transform([inputdata])
    newpred = clfsvm.predict(newnptest)
    print newpred[0].replace('.ptext', '')
    """
    newpred = clfnb.predict(newnptest)
    print 'NB', newpred[0].replace('.ptext', '')
    print 'Ended in', time.time() - start_time
    """

temp = open('temp', 'r')
myclassify(temp.read())
