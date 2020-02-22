import json
from bs4 import BeautifulSoup
import re
from collections import defaultdict, deque
import sys
		
class IIMatrix:
	def __init__(self):
		self.threshold = 100
		self.doc_id = 0 #which is counted
		self.ii = dict() #{term:[num of docs, {docid:tf, docid:tf, ...}], term:[....], ...}
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
							self.parse(soup.get_text())

					except PermissionError:
						print("PermissionError")
		self.write_json()

	def write_json(self):
		file = "jsonindex" + str(self.file_name)
		self.file_name += 1
		with open(file, 'w') as f:
			json.dump(self.ii, f)
		self.ii.clear()

	def parse(self, text):
		lst = text.lower().split()
		for word in lst:
			if re.match(r"^[a-z0-9]+$", word):
				if word in self.ii:
					self.ii[word][1][self.doc_id] +=1
					self.ii[word][0] = len(self.ii[word][1])
				else: #not inside
					inner_dict = defaultdict(int)
					inner_dict[self.doc_id] = 1
					self.ii.update({word:[1, inner_dict]})
				

	def get_number_of_docs(self):
		return self.doc_id

	def number_of_unique_words(self):
		return len(self.ii)

	def print_data_structure(self):
		print(self.ii)