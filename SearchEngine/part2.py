import os
import re
import sys
import string
import time
import math
import operator

my_dictwd = {}
my_dictidf = {}
normalized_docs = {}
words_to_doc = {}
my_files = set()


start_time = time.time()
replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))

def walk_and_build(rootdir):
    count = 0
    for root, subFolders, files in os.walk(rootdir):
        for filename in files:
            if(filename.endswith('.txt')):
                filePath = os.path.join(root, filename)
            else:
                continue
            count = count+1
            if(count%5000 == 0):
                print count, ' files', time.time() - start_time, ' Seconds '
            fp = open(filePath, 'r')
            content = fp.read().lower()
            words = re.findall(r"\w+", content)
            for word in words:
                if(word == '\n' or word == ' '):
                    continue
                if(word not in my_dictwd):
                    my_dictwd[word] = {}
                    my_dictwd[word][filename] = 1
                else: 
                    if(filename not in my_dictwd[word]):
                        my_dictwd[word][filename] = 1
                    else:
                        my_dictwd[word][filename] = my_dictwd[word][filename]+1
            sum_of_squares = 0
            my_files.add(filename)
            words_to_doc[filename] = set(words)
    print time.time() - start_time, ' Dict Built', count
    return count


#Calc IDF
def calculate_idf(N):
    print 'num of words', len(my_dictwd)
    for word in my_dictwd:
        my_dictidf[word] = math.log10((N*1.0)/len(my_dictwd[word]))
        for doc in my_dictwd[word]:
            my_dictwd[word][doc] = my_dictidf[word] * (1+ math.log10(my_dictwd[word][doc] * 1.0))
    my_dictidf.clear()
    print time.time() - start_time, 'IDF Done '

def calculate_modulus():
    for doc in my_files:
        sumofsq = 0.0
        for word in words_to_doc[doc]:
            sumofsq = sumofsq + (my_dictwd[word][doc] * my_dictwd[word][doc])
        normalized_docs[doc] = math.sqrt(sumofsq)
        words_to_doc[doc].clear()
    print time.time() - start_time, 'Modulus Done '

def run_query():
    cont = 0
    while(1):
        print 'Enter a query or exit'
        dict_of_scores = {}
        my_query = {}
        sum_of_squares = 0
        line = sys.stdin.readline()
        start_time = time.time()
        line = line.lower()
        if(line == '\n'):
            continue
        words = line.split()
        if(words[0] == 'exit'):
            print 'Thankyou'
            sys.exit(0)
        for word in words:
            if(word not in my_query):
                my_query[word] = 1
            else:
                my_query[word] = my_query[word]+1
        if(len(words)==0):
            continue
        set_of_matched_docs = set()
        results = {} 
        words = my_query.keys()
        sum_of_squares = 0.0
        for word in words:
            try:
                set_of_matched_docs = set_of_matched_docs.union(set(my_dictwd[word].keys()))
                sum_of_squares = sum_of_squares + my_query[word] * my_query[word]
            except:
                print 'No Match'              
                cont = 1
                break
        if(cont == 1):
            cont = 0
            continue
        num = len(words)
        count = 0
        normalized_query = math.sqrt(sum_of_squares)

        for doc in set_of_matched_docs:
            results[doc] = 0
            for word in words:
                try:
                    results[doc] = results[doc] + \
                                   my_dictwd[word][doc] *\
                                   (1.0/normalized_docs[doc]) * (1.0/normalized_query) \
                                   * my_query[word]
                except:
                    pass
        print '\nResults Matched :', len(results)
        print '\n Time taken :',time.time()-start_time
        sorted_results = sorted(results.iteritems(), key=operator.itemgetter(1), reverse = True)    
        hello = 0
        for doc, value in sorted_results:
            hello = hello+1
            print doc, value
            if(hello > 50):
                break


def main(argv):
    if(len(argv)<2):
        print 'Usage: python part2.py <dirname>'
        sys.exit(0)
    print 'You wll see a timestamp every 5k files processing(around 70-90s)'
    num_of_files = walk_and_build(sys.argv[1])
    print num_of_files
    calculate_idf(num_of_files)
    calculate_modulus()
    run_query()

if(__name__ == '__main__'):
    sys.exit(main(sys.argv))
