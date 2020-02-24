import json
from bs4 import BeautifulSoup
import re
from collections import defaultdict, deque
import sys
from nltk.stem import PorterStemmer
		
class IIMatrix:
	def __init__(self):
		self.threshold = 100
		self.doc_id = 0 #which is counted
		self.ii = dict() #{term:[num of docs, {docid:[tf, [positions], {"header":freq, "strong":freq, "title":freq}],...}], term:[....],...}
		self.file_name = 1
		self.unique_docs = 0
		self.port_stem = PorterStemmer()


	def create_matrix(self, path):
		q = deque()
		q.append(path)
		while len(q) != 0:
			q.popleft()
			for obj in path.iterdir():
				if obj.is_dir():
					q.append(obj)
				else:
					if sys.getsizeof(self.ii) > 90000:
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

	def write_json(self):
		file = "jsonindex" + str(self.file_name)
		print("Just wrote " + file)
		self.file_name += 1
		with open(file, 'w') as f:
			json.dump(self.ii, f)
		self.unique_docs += len(self.ii)
		self.ii.clear()

	'''
	Need path of the files as another parameter
	Perhaps we should write them all in a folder, easy to find?
	Open one file
	Keep opening the others until we go through it all
	Delete the files that are finished
	'''
	def merge_json(self):
		pass
		'''
		{term:[num of docs, {docid:[tf, [positions], {"header":freq, "strong":freq, "title":freq}],...}], term:[....],...}
		for term in second:
			if term in first:
				#don't need to access excessive amount of times
				temp1 = first[term]
				temp2 = second[term]
				temp1[0] += second[term][0] add num freq
				temp1[1].update(f[1])
				first[term] = temp1
				delete the other term
			else:
				first[term] = second[term]
		'''

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
				

	def get_number_of_docs(self):
		return self.doc_id

	def number_of_unique_words(self):
		return self.unique_docs

	def print_data_structure(self):
		print(self.ii)