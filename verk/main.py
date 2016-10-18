#!/usr/bin/env python3

import sys
import os.path

from util import parse_arguments, files_in_directory, edge_weights_to_list, create_graph
from input import read_words_from_files, read_words_from_pickle
from output import export_to_csv, save_words_to_pickle
from processing import extract_names

def main():
	arguments = parse_arguments()
	words_by_file = []
	pickle_path = os.path.join(arguments.folder, 'cache.pickle')

	if arguments.clean:
		print('Reading words from files in folder ' + arguments.folder + '...')
		words_by_file = read_words_from_files(files_in_directory(arguments.folder))
		save_words_to_pickle(words_by_file, pickle_path)
		print('Saved words to pickle ' + pickle_path)
	else:
		if os.path.isfile(pickle_path):
			words_by_file = read_words_from_pickle(pickle_path)
		else:
			words_by_file = read_words_from_files(files_in_directory(arguments.folder))

	names = extract_names(words_by_file)
	(nodes, edges, edge_weights) = create_graph(names)

	export_to_csv(edge_weights, os.path.join(arguments.folder, 'graph.csv')) # Export graph to CSV
	#print(edge_weights_to_list(edge_weights))

if __name__ == "__main__":
	main()