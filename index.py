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

#{term:[num of docs, {docid:[#ofwords,tf, [positions], {"header":freq, "strong":freq, "title":freq}],...}], term:[....],...}
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
		self.create_big_index()
		q = deque()
		q.append(path)
		while len(q) != 0:
			curr_dir = q.popleft()
			for obj in curr_dir.iterdir():
				print("Checking " + str(obj))
				if obj.is_dir():
					q.append(obj)
				else:
					
					if sys.getsizeof(self.ii) > 10000000: #10 MB
						self.write_text()

					
					try:
						with open(obj) as json_file:
							
							data = json.load(json_file)
							content = data['content']
							soup = BeautifulSoup(content, 'lxml')
							self.doc_id += 1
							self.parse(soup)

					except PermissionError:
						print("PermissionError")
		self.write_text()
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
				string = term + ';'
				for docID,pos in sorted(docs.items()):
					p = str(pos)
					string += docID + ':' + p[1:len(p)-1] + ';'
			string.rstrip(';')
			string += '\n'
			f.write(string)
		self.unique_words += len(self.ii)
		self.ii.clear()
	
	def create_big_index(self):
		if not os.path.isdir(self.index_dir):
			os.mkdir(self.index_dir)
		f = open('BigIndex','w')
		f.close()
		return self.big_index


	def merge_index(self):
		#open the json file here
		print(os.getcwd())
		os.chdir(self.index_dir)
		with open("BigIndex", "r+") as big:
			path = Path(os.getcwd())
			print(path)
			for j in path.iterdir():
				if j.name != "BigIndex":
					try:
						for line in open(j):
							big.write(line)
							

							line = line.rstrip('\n').split(';')
							#total num of documents is len(line)-1
							term = line[0]




							if term in res:
								temp1 = res[term]
								temp2 = data[term]
								temp1[0] += temp2[0] #add num freq
								temp1[1].update(temp2[1])
							else:
								res[term] = data[term]
					with open ('jsonBigIndex', 'w') as f:
						json.dump(res, f)
					os.remove(j)
				except PermissionError:
					continue

	def parse(self, soup):
		text = soup.get_text()
		lst = text.lower().split()
		self.total_num_words[self.doc_id] = len(lst)

		header_lst = soup.find_all(re.compile(r"^h[1-6]$"))
		strong_lst = soup.find_all(re.compile(r"^strong$"))
		title_lst = soup.find_all(re.compile(r"^title$"))
		
		for x in range(len(lst)):
			word = lst[x]
			if word.isalnum():
				word = self.port_stem.stem(word)
				"""
				create dictionary of doc ids with values of word counts
				update at the very end.
				{term:{docid:[[1,2],[2,0]], docid:[[3,0],[4,0]]}, term:...}
				"""
				if word in self.ii:
					if self.doc_id not in self.ii[word]:
						self.ii[word][self.doc_id] = [x]
					else:
						self.ii[word][self.doc_id].append(x)
				else: #not inside
					self.ii.update({word:{self.doc_id:[x]}})

	def get_big_index_path(self):
		return self.json_big_index

	def get_number_of_docs(self):
		return self.doc_id

	def number_of_unique_words(self):
		return self.unique_words

	def print_data_structure(self):
		print(self.ii)