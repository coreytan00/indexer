from index import IIMatrix
from index import intersect
from pathlib import Path

#PATH="C:\\Users\\polar\\GitRepos\\indexer\\developer\\DEV"
#TEST="C:\\Users\\polar\\GitRepos\\indexer\\developer\\DEV\\aiclub_ics_uci_edu"

#For Patrick Test, since file location difference
#PATH="C:\\Users\\Patrick\\Documents\\GitHub\\indexer\\developer\\DEV"
#TEST="C:\\Users\\Patrick\\Documents\\GitHub\\indexer\\developer\\DEV"

#General Path
PATH = Path.cwd()
TEST = Path.cwd()

def main():
	print("Starting")
	path_obj = Path(PATH)
	t = Path(TEST)
	print("Path found")
	iim = IIMatrix()
	print("Matrix initialized")
	#print(path_obj)
	iim.create_matrix(path_obj)
	#print(iim.get_number_of_docs())
	#print(iim.number_of_unique_words())
	#intersect(iim.get_big_index_path(), "artifical", "machine")
	print("Done")

if __name__=="__main__":
	main()