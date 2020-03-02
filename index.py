import json
from bs4 import BeautifulSoup
import re
from collections import defaultdict, deque
import sys
from nltk.stem import PorterStemmer
import os
from pathlib import Path
from math import log


	#count number of times doc id appears in dictionary
	pass

#{term:[num of docs, {docid:[#ofwords,tf, [positions], {"header":freq, "strong":freq, "title":freq}],...}], term:[....],...}
def intersect(file, *ws):#
	"""boolean search easy!"""
	"""not finished"""
	def compute_tfidf(w1, w2):
		w1docs = [d for d in res[w1][1].keys()]
		w2docs = [d for d in res[w2][1].keys()] # redundant. optimize later
		c1, c2 = 0, 0
		doc_lst = []
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
 			except IndexError:
				break
		return doc_lst

	ws = [port_stem.stem(word) for word in ws]
	port_stem = PorterStemmer()
	with open(file, "r") as f:
		res = json.load(f)
		#total_docs = len(res[w1][1])
		res_lst = []
		for i in range(len(ws)-1):
			compute_tfidf(ws[i], ws[i+1])

	return 


		
class IIMatrix:
	def __init__(self):
		self.threshold = 100
		self.doc_id = 0 #which is counted
		self.ii = dict() #{term:[num of docs, {docid:[tf, [positions], {"header":freq, "strong":freq, "title":freq}],...}], term:[....],...}
		self.file_name = 1
		self.unique_docs = 0
		self.port_stem = PorterStemmer()
		self.json_dir = "./JSON/"
		self.json_big_index = os.path.join(self.json_dir, "jsonBigIndex")


	def create_matrix(self, path):
		q = deque()
		q.append(path)
		while len(q) != 0:
			curr_dir = q.popleft()
			for obj in curr_dir.iterdir():
				print("Checking " + str(obj))
				if obj.is_dir():
					q.append(obj)
				else:
					
					if sys.getsizeof(self.ii) > 9000000:
						self.write_json()

					self.doc_id += 1
					try:
						with open(obj) as json_file:
							
							data = json.load(json_file)
							content = data['content']
							soup = BeautifulSoup(content, 'lxml')
							self.parse(soup)

					except PermissionError:
						print("PermissionError")
		self.write_json()
		self.create_big_index()

	def write_json(self):
		file = "jsonindex" + str(self.file_name)
		#print("Just wrote " + file)
		self.file_name += 1
		with open(file, 'w') as f:
			json.dump(self.ii, f)
		self.unique_docs += len(self.ii)
		self.ii.clear()
	
	def create_big_index(self):
		if not os.path.isdir(self.json_dir):
			os.mkdir(self.json_dir)
		#filepath = os.path.join(self.json_dir, fn)
		'''d = dict()
		f = open(filepath, "w")
		json.dump(d, f)
		f.close()'''
		return self.json_big_index

	'''
	Need path of the files as another parameter
	Perhaps we should write them all in a folder, easy to find?
	Open one file
	Keep opening the others until we go through it all
	Delete the files that are finished
	'''
	def merge_json(self, fp):
		#open the json file here
		print(os.getcwd())
		with open(fp, "r+") as f:
			res = json.load(f)
		
		os.chdir(self.json_dir)
		path = Path(os.getcwd())
		print(path)
		for j in path.iterdir():
			print(j.name)
			if j.name != "jsonBigIndex":
				try:
					with open(j) as json_file:
						data = json.load(json_file)
						for term in data.keys():
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
		header_lst = soup.find_all(re.compile(r"^h[1-6]$"))
		strong_lst = soup.find_all(re.compile(r"^strong$"))
		title_lst = soup.find_all(re.compile(r"^title$"))
		lst = text.lower().split()
		for x in range(len(lst)):
			word = lst[x]
			if re.match(r"^[a-z0-9]+$", word):
				word = self.port_stem.stem(word)
				if word in self.ii:
					if self.doc_id not in self.ii[word][1]:
						self.ii[word][1][self.doc_id] = [1, [x], {"header":0, "strong":0, "title":0}]
						self.ii[word][1][self.doc_id][2]["header"] = header_lst.count(word)
						self.ii[word][1][self.doc_id][2]["strong"] = strong_lst.count(word)
						self.ii[word][1][self.doc_id][2]["title"] = title_lst.count(word)
					else:
						self.ii[word][1][self.doc_id][0] +=1
						self.ii[word][1][self.doc_id][1].append(x)
					self.ii[word][0] = len(self.ii[word][1])
				else: #not inside
					inner_dict = {self.doc_id:[1, [x], {"header":0, "strong":0, "title":0}]}
					self.ii.update({word:[1, inner_dict]})

	def get_big_index_path(self):
		return self.json_big_index

	def get_number_of_docs(self):
		return self.doc_id

	def number_of_unique_words(self):
		return self.unique_docs

	def print_data_structure(self):
		print(self.ii)