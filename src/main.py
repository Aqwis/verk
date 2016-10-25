#!/usr/bin/env python3

import sys
import os.path

from .util import parse_arguments, files_in_directory, edge_weights_to_list, create_graph
from .input import read_files, unpickle_articles
from .output import export_to_csv, pickle_articles
from .processing import extract_names_from_articles

def main():
	arguments = parse_arguments()
	words_by_file = []
	pickle_path = os.path.join(arguments.folder, 'cache.pickle')

	articles = []

	if arguments.clean:
		print('Reading files in folder ' + arguments.folder + '...')
		articles = read_files(files_in_directory(arguments.folder))
		pickle_articles(articles, pickle_path)
		print('Saved words to pickle ' + pickle_path)
	else:
		if os.path.isfile(pickle_path):
			articles = unpickle_articles(pickle_path)
		else:
			articles = read_files(files_in_directory(arguments.folder))

	names = extract_names_from_articles(articles)
	(nodes, edges, edge_weights) = create_graph(names)

	export_to_csv(edge_weights, os.path.join(arguments.folder, 'graph.csv')) # Export graph to CSV
	#print(edge_weights_to_list(edge_weights))

if __name__ == "__main__":
	main()