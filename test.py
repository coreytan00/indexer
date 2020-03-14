import json
from nltk.stem import PorterStemmer
import os
from collections import deque
from pathlib import Path
from math import log

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
    tk = open('TotalKeeper', 'r')
    tnw = open('TotalNumWords', 'r')
    overwrite = []

    for line in open(f):
        #Look at each posting
        first = line.rstrip('\n').rstrip(';').split(';')
        print("FIRST:", first)

        #Calculate idf
        idf = log(55393/(len(first)-1))
        
        #Look at each docID
        for j in range(1,len(first)):
            t_docs = 0 #t_docs is the total number of words in the document
            inner = first[j].split(':')
            print("OVER HERE", inner)
            docID = int(inner[0])
            print("INNER:", inner)

            #Look in the bookkeping TotalKeeper for the the pointer
            while (t_docs==0):
                tk_line = tk.readline()
                tk_line = tk_line.split(':')
                placement_position = docID//500*500
                print(tk_line)
                print(placement_position)
                print(tk_line[0], placement_position == int(tk_line[0]))
                if placement_position == int(tk_line[0]) or placement_position == 1:
                    position = int(tk_line[1])
                    #Seek in the TotalNumWords, loop until you find the correct posting for it
                    #Retrieve TotalNumWords to divide by
                    #Store it
                    for m in range(500):
                        try:
                            tnw.seek(position)
                            tnw_line = tnw.readline()
                            tnw_line = tnw_line.rstrip('\n').split(':')
                            if docID == int(tnw_line[0]):
                                t_docs = int(tnw_line[1])
                                break
                            position = tnw.tell()
                        except IndexError:
                            break
                    tk.seek(0)
                if placement_position >= 55000: #if at a docID that doesn't exist, however should not occur
                    break

            #Look at each Positional Argument (need for tf)
            for k in range(1, len(inner)-1):
                ner = inner[k].split(',')
                print("NER:", ner)
                tf_numerator = len(ner)+float(inner[len(inner)-1])
                print("TF_NUM SCORE:", str(tf_numerator))             

                #Calculate tf
                print("TF_DEN SCORE:", str(t_docs))
                tf_score = tf_numerator/t_docs
                print("TF SCORE:", tf_score)
        #first[0] + ';' + 
        overwrite.append(first + ';' +)


    tk.close()
    tnw.close()

def create_bookkeeper(f, name):
    overwrite = []
    pointer = 0
    with open(f, 'r') as imp:
        line = imp.readline()
        c = line[0]
        overwrite.append(str(c)+':'+str(pointer)+'\n')
        while line:
            if line[0] != c:
                c = line[0]
                overwrite.append(str(c)+':'+str(pointer)+'\n')
            pointer = imp.tell()
            line = imp.readline()
    with open(name, 'w') as to_write:
        to_write.writelines(overwrite)

def total_bookkeeper(f, name):
    overwrite = []
    pointer = 0
    with open(f, 'r') as imp:
        line = imp.readline()
        c = int(line[0])
        overwrite.append(str(c)+':'+str(pointer)+'\n')
        while line:
            line = line.split(':')
            c = int(line[0])
            if c%500==0:
                overwrite.append(str(c)+':'+str(pointer)+'\n')
            pointer = imp.tell()
            line = imp.readline()
    with open(name, 'w') as to_write:
        to_write.writelines(overwrite)
    
                
told('f.txt')
#create_bookkeeper('TotalNumWords','TotalKeeper')
#total_bookkeeper('TotalNumWords','TotalKeeper')
        
