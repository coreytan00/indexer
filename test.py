import json
from nltk.stem import PorterStemmer
import os
from collections import deque
from pathlib import Path

def intersect(file, *ws):
    def compute_tfidf(w1, w2):
        w1docs = sorted(res[w1][1].keys())
        w2docs = sorted(res[w2][1].keys()) # redundant. optimize later
        print("Retrieved Postings")
        c1, c2 = 0, 0
        doc_lst = []
        print("Checking Begins Now")
        while True:
            try:
                ptr1 = int(w1docs[c1])
                ptr2 = int(w2docs[c2])
                if ptr1 < ptr2:
                    c1 +=1
                elif ptr1 > ptr2:
                    c2 +=1
                else: #both found in same doc
                    doc_lst.append(ptr1) #add one -- doesn't matter
                    c1 +=1
                    c2 +=1
            except IndexError:
                print("Index Error occurred")
                break
        return doc_lst

    port_stem = PorterStemmer()
    ws = [port_stem.stem(word) for word in ws]
    print("Words have been stemmed")
    with open(file, "r") as f:
        res = json.load(f)
        print("File loaded")
        res_lst = []
        if len(ws) > 1:
            for i in range(len(ws)-1):
                print("Checking " + ws[i] + " and " + ws[i+1])
                res_lst.append(compute_tfidf(ws[i], ws[i+1]))
            return set.intersection(*[set(lst) for lst in res_lst])
        else:
            res_lst.append(compute_tfidf(ws[0],ws[0]))
            return [set(lst) for lst in res_lst]

def counter(numbers):
    q = deque()
    q.append(Path.cwd())
    doc_id = 0
    URLS = dict()
    while len(URLS) != len(numbers):
        curr_dir = q.popleft()
        for obj in curr_dir.iterdir():
            if obj.is_dir():
                q.append(obj)
            else:
                if obj.name != "jsonBigIndex":
                    try:
                        with open(obj) as json_file:
                            data = json.load(json_file)
                            doc_id += 1
                            if doc_id % 900 == 0:
                                print("Made it to: " + str(doc_id))
                            if doc_id in numbers:
                                URLS[doc_id] = data['url']
                    except:
                        continue
            if len(URLS) == len(numbers):
                break
    return URLS
'''
print(intersect("jsonBigIndex", 'cristina', 'lopes'))
print(intersect("jsonBigIndex", 'machine', 'learning'))
print(intersect("jsonBigIndex", "ACM"))
print(intersect("jsonBigIndex", 'master', 'of', 'software', 'engineering'))

print(counter([16927,19264,21574,29345,24237]))
print(counter([1, 11, 22, 33, 47]))
print(counter([20, 30, 33, 8233, 8234]))
print(counter([16479, 16507, 16985, 16986, 16988]))'''

#print(counter([49968,19345,19419,16467,12547,25756,33529]))
'''
print('Enter query: cristina lopes')
print('Results')
print('-> http://sdcl.ics.uci.edu/author/andre/page/2/')
print('-> http://sdcl.ics.uci.edu/category/news/page/2/')
print('-> http://sdcl.ics.uci.edu/page/3/')
print('-> https://www.cs.uci.edu/events-page/computer-science-seminar-series/')
print('-> https://www.ics.uci.edu/community/news/notes/notes_2011.php')
input('Enter query: ')'''

def told(f):
    with open(f, 'r+') as a:
        print(a.readline())

told('f.txt')
        
