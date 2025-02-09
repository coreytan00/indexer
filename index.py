import json
from bs4 import BeautifulSoup
import re
from collections import deque
import sys
from nltk.stem import PorterStemmer
import os
from pathlib import Path
from math import log

def compute_tfidf():
	#count number of times doc id appears in dictionary
	pass

def intersect(file, *ws):#
	"""boolean search easy!"""
	count = 0
	port_stem = PorterStemmer()
	str(count)
	w1 = port_stem.stem(w1)
	w2 = port_stem.stem(w2)
	with open(file, "r") as f:
		res = json.load(f)
		total_docs = len(res[w1][1])


	return res


		
class IIMatrix:
	def __init__(self):
		self.threshold = 100
		self.doc_id = 0 #which is counted
		'''
		{term:{docid:[[position,header|strong|title],[2,0]], docid:[[3,0],[4,0]]}, term:...}
		tf - #of terms in document/# of words in document
			dict(doc_id:#of words in doc)
			at writing to txt file, we compute value
		idf - log(# of total documents/# of docs with term)
			at the end, we compute
		numOfAppear = len()
		term;docid:numOfAppear,tf,positions (split by hyphen or something), header|strong|title;docid
		'''
		self.ii = dict()
		self.file_name = 1
		self.unique_words = 0
		self.total_num_words = dict()
		self.port_stem = PorterStemmer()
		self.index_dir = "./Index/"
		self.big_index = os.path.join(self.index_dir, "BigIndex")


	def create_matrix(self, path):
		'''q = deque()
		q.append(path)
		while len(q) != 0:
			curr_dir = q.popleft()
			for obj in curr_dir.iterdir():
				print("Checking " + str(obj))
				if obj.is_dir():
					q.append(obj)
				else:
					if sys.getsizeof(self.ii) > 1000000: #10 MB #0
						self.write_text()
					try:
						with open(obj) as json_file:
							
							data = json.load(json_file)
							content = data['content']
							soup = BeautifulSoup(content, 'lxml')
							self.doc_id += 1
							self.parse(soup)

					except PermissionError:
						continue
						#print("PermissionError")
					except ValueError:
						continue
						#print("ValueError")
					except Exception as e:
						continue
		self.write_text()
		self.write_total_num_words()'''
		self.merge_index()

	'''
	Change from write_json to write_text
	1. Loop through sorted(self.ii)
	2. Create txt file called index + self.file_name
	3. Increment self.file_name
	4. Open file, write into file line by line
	5. For each entry
	6. term ; docid : numOfAppear,tf,positions (split by hyphen or something), header|strong|title;docid
	'''
	def write_text(self):
		file = "index" + str(self.file_name)
		self.file_name += 1
		with open(file, 'w') as f:
			for term,docs in sorted(self.ii.items()):
				string = '{};'.format(term)
				for docID,pos in sorted(docs.items()):
					p = pos[0]
					p = ",".join(str(a) for a in p)
					string += '{}:{}:{};'.format(str(docID), p, str(pos[1]))
				string.rstrip(';')
				string += '\n'
				try:
					f.write(string)
				except:
					continue
		self.unique_words += len(self.ii)
		self.ii.clear()

	def write_total_num_words(self):
		with open('TotalNumWords','w') as big:
			for key,value in self.total_num_words.items():
				big.write(str(key)+':'+str(value)+'\n')


	def merge_index(self):
		'''Dump all files together
		Apply readlines and sorted function
		Rewrite into file'''
		with open("index1", "r+") as big:
			#print(os.getcwd())
			for i in range(57):
				fn = "index{}".format(i+1)
				print(fn)
				if fn != "index1":
					try:
						with open(fn, 'r') as small:
							line = small.read()
							big.write(line)
					except:
						continue
			big.seek(0)
			s = big.readlines()
			s = sorted(s)
		with open('index1', 'w') as big:
			tracker = set()
			overwrite = []
			for i in range(len(s)):
				first = s[i].split(';')
				temp = first[0] + ';' + first[1]
				if first[0] not in tracker:
					for j in range(i+1,len(s)):
						second = s[j].split(';')
						if first[0] == second[0]:
							temp += ';' + second[1]
						else:
							break
					tracker.add(first[0])
					temp += ';\n'
					overwrite.append(temp)                 
			big.writelines(overwrite)
			


	def parse(self, soup):
		text = soup.get_text()
		lst = text.lower().split()
		self.total_num_words[self.doc_id] = len(lst)

		#Add .3 for header
		#Add .4 for bolds/strong
		#Add .5 for title
		header_lst = soup.find_all(re.compile(r"^h[1-6]$"))
		strong_lst = soup.find_all(re.compile(r"^strong$"))
		title_lst = soup.find_all(re.compile(r"^title$"))
		
		header_lst = (" ".join(str(w)[4:len(w)-6].lower() for w in header_lst)).split()
		strong_lst = (" ".join(str(w)[9:len(w)-11].lower() for w in strong_lst)).split()
		title_lst =  (" ".join(str(w)[7:len(w)-9].lower() for w in title_lst)).split()
		
		self.check_parse(lst, header_lst, strong_lst, title_lst)
	
	def check_parse(self, lst, header_lst, strong_lst, title_lst):
		for x in range(len(lst)):
			word = str(lst[x])
			#print("WORD:", word)
			if word.isalnum():
				word = self.port_stem.stem(word)
				if word in self.ii:
					if self.doc_id not in self.ii[word]:
						self.ii[word][self.doc_id] = [[x],0]
					else:
						self.ii[word][self.doc_id][0].append(x)
				else:
					self.ii.update({word:{self.doc_id:[[x],0]}})
				try:
					t = header_lst.index(word)
					header_lst.pop(t)
					self.ii[word][self.doc_id][1] += .3
				except:
					continue
				try:
					t = strong_lst.index(word)
					strong_lst.pop(t)
					self.ii[word][self.doc_id][1] += .4
				except:
					continue
				try:
					t = title_lst.index(word)
					title_lst.pop(t)
					self.ii[word][self.doc_id][1] += .5
				except:
					continue

	def get_big_index_path(self):
		return self.json_big_index

	def get_number_of_docs(self):
		return self.doc_id

	def number_of_unique_words(self):
		return self.unique_words

	def print_data_structure(self):
		print(self.ii)