import os
import sys
import string
import time
import fileinput

#rootdir = 'nsf'
#fow = open('file_of_words.txt', 'w')
my_dictdid = {}
my_files = {}
set_of_words = set()
set_of_files = set()
count = 0

            

start_time = time.time()
replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))

num_files = 0
def walk_and_index(rootdir):
    count = 0
    start_time = time.time()
    for root, subFolders, files in os.walk(rootdir):
        for filename in files:
            if(any(filename.endswith(x) for x in ('.txt', '.idx', '.bad'))):
                filePath = os.path.join(root, filename)
            else:
                continue
            count = count+1
            if(count%5000 == 0):
                print count, ' Files in ', time.time()-start_time, ' Seconds\r'
            fp = open(filePath, 'r')
            content = fp.read().lower().translate(replace_punctuation)
            words = content.split()
            for word in words:
                try:
                    my_dictdid[word].add(filename)
                except KeyError:
                    my_dictdid[word] = set()
                    my_dictdid[word].add(filename)

#print my_dictdid


def run_query():
    cont = 0
    while(1):
        print 'Enter a query or exit'
        line = sys.stdin.readline()
        if(line == '\n'):
            continue
        line = line.lower()
        start_time = time.time()
        words = (line.split())
        if(words[0] == 'exit'):
            sys.exit(0)
        words = set(line.split())
        for word in words:
            if(word not in my_dictdid):
                print word, ' Not present'
                cont = 1
                break        
        if(cont == 1):
            cont = 0
            continue
        p1 = set(my_dictdid[word])
        for word in words:
            p1 = p1.intersection(my_dictdid[word])
        p1 = list(p1)
        if(len(p1)==0):
            print 'No Match'
            continue
        print '\nResults Matched :', len(p1)
        print '\n Time taken :',time.time()-start_time
        index = 0
        for doc in p1:
            try:
                index = index+1
                print doc
                if(index>50):
                    break
            except:
                continue

def main(argv):
    print 'You will see a timestamp every 5000 files as an indication'
    if(len(sys.argv)==0):
        print 'Usage: python part1.py <dirname>'
        sys.exit(-1)
    walk_and_index(argv[1])
    run_query()

if(__name__=='__main__'):
    sys.exit(main(sys.argv))
