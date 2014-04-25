import json
import sys
import subprocess
import unicodedata
import shutil
import os

list_of_repos = []

def get_curr_infile():
    rootdir = os.getcwd()
    for root, subFolders, files in os.walk(rootdir):
        for filename in files:
            if(any(filename.endswith(x) for x in ('.txt', '.py', '.swp'))):
                continue
            return filename;

def git(*args):
    return subprocess.check_call(['git'] + list(args))

def process_repo(repo):
    global list_of_repos
    count = 0
    curr_repo = {}
    clone_url = repo['clone_url']
    fullName = repo['full_name'].split('/')
    curr_repo['description'] = repo['description']
    curr_repo['name'] = repo['full_name']
    curr_repo['url'] = repo['clone_url']
    html_url = repo['html_url']
    print repo['size'], html_url
    if(repo['size'] > 10000):
        list_of_repos.append(curr_repo)
        print 'Not cloning'
        return
    git("clone", clone_url)
    reponame = unicodedata.normalize('NFKD', fullName[1]).encode('ascii','ignore')
    try:
        readfile = open(reponame +'/'+'README.md')
        curr_repo['readme'] = readfile.read()
        list_of_repos.append(curr_repo)
    except:
        print 'No read me'
        list_of_repos.append(curr_repo)
        pass
    shutil.rmtree(reponame)
    
def process_file(infilename, trainfilename):
    global list_of_repos
    count = 0
    infile = open(infilename, 'r')
    trainfile = open(trainfilename, 'w')
    try:
        for line in infile:
            listOfrepo = json.loads(line)
    except:
        print 'json load fail'
        #repoObj = json.loads(line)
        return
    for repo in listOfrepo:
        print 'Processing ', count
        count = count+1
        process_repo(each)
    json.dump(list_of_repos, trainfile)

def main():
    global list_of_repos
    infilename = get_curr_infile()
    trainfilename = infilename + '.txt'
    print infilename, trainfilename 
    list_of_repos = []
    process_file(infilename, trainfilename)

if(__name__=='__main__'):
    sys.exit(main())
