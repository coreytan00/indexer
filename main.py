from index import IIMatrix
from pathlib import Path

PATH="C:\\Users\\polar\\GitRepos\\indexer\\developer\\DEV"
TEST="C:\\Users\\polar\\GitRepos\\indexer\\developer\\DEV\\aiclub_ics_uci_edu"

def main():
	path_obj = Path(PATH)
	t = Path(TEST)
	iim = IIMatrix()
	iim.create_matrix(t)

if __name__=="__main__":
	main()