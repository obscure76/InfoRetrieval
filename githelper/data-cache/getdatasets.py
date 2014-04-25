import json
import sys
import subprocess
import unicodedata
import shutil
import os

list_of_repos = []

def clone_datasets():
    global list_of_repos
    rootdir = os.getcwd()
    for root, subFolders, files in os.walk(rootdir):
        for filename in files:
            if(any(filename.endswith(x) for x in ('.txt', '.py', '.swp'))):
                continue
            listoffiles = ['android+application.txt',  'database+systems.txt', 'Image+processing.txt', \
                            'natural+language+processing.txt', 'web+development.txt', 'audio+applications.txt', \
                            'data+mining.txt', 'ios+application.txt', 'operating+systems.txt', 'cloud+computing.txt',\
                            'distributed+systems.txt', 'linux+applications.txt',  'signal+processing.txt', \
                            'computer+networks.txt', 'facebook+application.txt', 'machine+learning.txt', \
                            'computer+vision.txt', 'google+applications.txt',  'music+applications.txt', 'twitter+applications.txt']
            trainfilename = filename + '.txt'
            if trainfilename in listoffiles:
                continue
            print filename, trainfilename 
            list_of_repos = []
            process_file(filename, trainfilename)

def git(*args):
    return subprocess.check_call(['git'] + list(args))

def process_repo(repo):
    global list_of_repos
    count = 0
    curr_repo = {}
    try:
        clone_url = repo['clone_url']
    except:
        return
    fullName = repo['full_name'].split('/')
    try:
        curr_repo['description'] = unicodedata.normalize('NFKD', repo['description']).encode('ascii', 'ignore')
    except:
        curr_repo['description'] = ''
    try:
        curr_repo['name'] = unicodedata.normalize('NFKD', repo['full_name']).encode('ascii', 'ignore')
    except:
        return
    curr_repo['url'] = repo['clone_url']
    html_url = repo['html_url']
    print repo['size'], html_url
    if(repo['size'] > 10000):
        list_of_repos.append(curr_repo)
        print 'Not cloning'
        return
    try:
        git("clone", clone_url)
    except:
        return
    try:
        reponame = unicodedata.normalize('NFKD', fullName[1]).encode('ascii','ignore')
        readfile = open(reponame +'/'+'README.md')
        curr_repo['readme'] = readfile.read()
        try:
            testdump = open('testdump', 'w')
            json.dump(curr_repo, testdump)
        except:
            return
        list_of_repos.append(curr_repo)
    except:
        print 'No read me'
        try:
            testdump = open('testdump', 'w')
            json.dump(curr_repo, testdump)
        except:
            return
        list_of_repos.append(curr_repo)
        pass
    shutil.rmtree(reponame)
    
def process_file(infilename, trainfilename):
    global list_of_repos
    count = 0
    trainfile = open(trainfilename, 'w')
    try:
        infile = open(infilename, 'r')
        for line in infile:
            listOfrepo = json.loads(line)
    except:
        print 'json load fail'
        #repoObj = json.loads(line)
        return
    for repo in listOfrepo:
        print 'Processing ', count
        count = count+1
        if count < 998:
            process_repo(repo)
    print len(list_of_repos)
    json.dump(list_of_repos, trainfile)

def main():
    global list_of_repos
    clone_datasets()

if(__name__=='__main__'):
    sys.exit(main())
