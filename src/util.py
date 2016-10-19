import argparse
import os.path

from os import walk
from collections import defaultdict

def edge_weights_to_list(edge_weights):
	edge_list = [(edge, edge_weights[edge]) for edge in edge_weights]
	return sorted(edge_list, key=lambda x: x[1])

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("folder", help="folder containing source files (articles)")
	parser.add_argument("-v", "--verbose", help="display more messages during runtime", action="store_true")
	parser.add_argument("-c", "--clean", help="discard cache and reread every source file", action="store_true")
	parser.add_argument("-n", "--names", help="specify file containing predefined names", default="names.csv")
	parser.add_argument("-p", "--parser", help="specify parser used to parser source files if not plain text", default="default")
	return parser.parse_args()

def files_in_directory(directory):
	dirpath, _, files = walk(directory).__next__()
	try:
		files.remove('cache.pickle')
	except ValueError:
		pass
	try:
		files.remove('graph.csv')
	except ValueError:
		pass
	return [os.path.join(dirpath, file) for file in files]

def is_word_potential_name(word):
	if not len(word) > 1:
		return False

	if not word[0].isupper():
		return False

	if not word[0].isalpha():
		return False

	allCaps = True
	for letter in word:
		if not letter.isupper():
			allCaps = False
			break
	if allCaps:
		return False

	return True

def strip_word(word):
	return ''.join([l for l in word if l.isalpha()])

def create_graph(names_by_file):
	nodes = set()
	edges = set()
	edge_weights = defaultdict(lambda: 0)
	for names in names_by_file:
		for i in names:
			for j in names:
				if i == j:
					continue
				else:
					edge_set = frozenset([str(i), str(j)])
					edges.add(edge_set)
					edge_weights[edge_set] = edge_weights[edge_set] + 1
					nodes.add(i)
					nodes.add(j)
	edge_weights = {k: edge_weights[k]/2 for k in edge_weights}
	return (nodes, edges, edge_weights)