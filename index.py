import json
from bs4 import BeautifulSoup
import re
from collections import defaultdict, deque
import sys
		
class IIMatrix:
	def __init__(self):
		self.threshold = 100
		self.doc_id = 0 #which is counted
		self.ii = dict() #{term:[num of docs, {docid:[tf, [[postion, characetristic],[position, charac],[position,characterist]], docid:tf, ...}], term:[....], ...}
		self.file_name = 1


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
						write_json()

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
		self.file_name += 1
		with open(file, 'w') as f:
			json.dump(self.ii, f)
		self.ii.clear()

	def parse(self, soup):
		text = soup.get_text()
		header_lst = soup.find_all(re.compile(r"^h[1-6]$"))
		strong_lst = soup.find_all(re.compile(r"^strong$"))
		title_lst = soup.find_all(re.compile(r"^title$"))
		lst = text.lower().split()
		for x in range(len(lst)):
			word = lst[x]
			if re.match(r"^[a-z0-9]+$", word): 
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

	#def number_of_unique_words(self):
	#	return len(self.ii)

	def print_data_structure(self):
		print(self.ii)