#!/usr/bin/env python3

import string
import pickle
import sys
import csv

import networkx as nx

from collections import defaultdict
from bs4 import BeautifulSoup
from more_itertools import unique_everseen
from collections import Counter

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

def extract_predefined_names(words):
	names = defaultdict(list)
	text = ' '.join(words)

	predefined_names = import_predefined_names('names.csv')

	for name in predefined_names:
		if name in text:
			names[name].append(1)

	return names

def extract_names(words):
	names = defaultdict(list)
	already_added_indexes = []

	first_names = import_first_names('fornavn.csv')
	forbidden_words = import_forbidden_words('forbidden_words.csv')

	for w in range(len(words)):
		word = strip_word(words[w])

		if not is_word_potential_name(word):
			continue

		if w in already_added_indexes:
			continue

		if word in first_names:
			full_name = [word]
			already_added_indexes.append(w)

			i = 1

			if w+1 < len(words):
				nextWord = strip_word(words[w+i])
				while is_word_potential_name(nextWord):
					notPartOfName = False
					for punctuation in string.punctuation:
						if punctuation in words[w+i-1]:
							notPartOfName = True
							break
					if notPartOfName:
						break

					if nextWord in forbidden_words:
						break

					full_name.append(nextWord)
					already_added_indexes.append(w+i)

					i = i + 1

					if w+i >= len(words):
						break
					nextWord = strip_word(words[w+i])

			full_name = " ".join(full_name)
			names[full_name].append(w)
		already_added_indexes = already_added_indexes[-10:]

	return names

def extract_names_from_files(words_by_file):
	names_by_file = []
	for f in words_by_file:
		names_by_file.append(extract_names(f))
	return names_by_file

def extract_predefined_names_from_files(words_by_file):
	names_by_file = []
	for f in words_by_file:
		names_by_file.append(extract_predefined_names(f))
	return names_by_file

def remove_incorrect_names(names_by_file):
	new_names_by_file = []
	for names in names_by_file:
		names_in_file = defaultdict(list)
		for name in names:
			if len(name.split()) > 1:
				names_in_file[name] = names[name]
		new_names_by_file.append(names_in_file)
	return new_names_by_file

def remove_one_article_predefined_names(names_by_file):
	occurrence = defaultdict(lambda: 0)
	predefined_names = import_predefined_names('names.csv')

	for f in names_by_file:
		for name in predefined_names:
			if name in f:
				occurrence[name] = occurrence[name] + 1

	single_occurrence_names = [name for name in occurrence if occurrence[name] < 2]

	deleted = 0

	for fi in range(len(names_by_file)):
		for name in single_occurrence_names:
			if name in names_by_file[fi]:
				deleted = deleted + 1
				del names_by_file[fi][name]
	print("deleted " + str(deleted) + " names")

	return names_by_file

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

def import_first_names(filename):
	words = []
	with open(filename) as f:
		reader = csv.reader(f, delimiter=';')
		for row in reader:
			if not row[0].isalpha():
				continue

			words.append(row[0])
	return words

def import_forbidden_words(filename):
	words = []
	with open(filename) as f:
		reader = csv.reader(f)
		for row in reader:
			if not row[0][0].isalpha():
				continue

			words.append(row[0])
	return words

def import_predefined_names(filename):
	names = []
	with open(filename) as f:
		reader = csv.reader(f)
		for row in reader:
			if not row[0][0].isalpha():
				continue

			names.append(row[0])
	names = list(unique_everseen(names))
	return names

def read_words_from_files():
	file_contents = []
	for filename in sys.argv[2:]:
		print('l')
		f = open(filename)
		html = f.read()

		soup = BeautifulSoup(html, 'html.parser')
		contents_list = soup.find_all("section", class_='article')

		if len(contents_list) > 1:
		    raise Exception()

		try:
			contents = contents_list[0]
		except:
			print("Failure!")
			continue
		try:
		    contents.find(class_='factboxcontainer').decompose()
		except:
		    pass
		lines = list([s.replace('\n', ' ') for s in contents.stripped_strings])
		text = " ".join(lines)

		file_contents.append(text)

	file_contents = [' '.join(f.split()) for f in file_contents]
	words_by_file = [f.split(' ') for f in file_contents]

	with open('data.pickle', 'wb') as f:
		pickle.dump(words_by_file, f, pickle.HIGHEST_PROTOCOL)

	return words_by_file

def read_words_from_pickle():
	with open('data.pickle', 'rb') as f:
		words_by_file = pickle.load(f)
		return words_by_file

def plot_graph(edge_weights):
	G = nx.Graph()
	for edge in edge_weights:
		left = list(edge)[0]
		right = list(edge)[1]
		weight = edge_weights[edge]

		G.add_edge(left, right, weight=weight)
	
	G = nx.convert_node_labels_to_integers(G)
	nx.draw(G, 'graph.png', format='png', prog='neato')

def export_to_csv(edge_weights):
	with open('graph.csv', 'wt') as f:
		print('Source;Target;Weight;Type', file=f)
		for edge in edge_weights:
			left = list(edge)[0]
			right = list(edge)[1]
			weight = edge_weights[edge]

			if weight > 0:
				print(left + ';' + right + ';' + str(int(weight)) + ";Undirected", file=f)

def main():
	words_by_file = []
	if sys.argv[1] == "pickle":
		words_by_file = read_words_from_pickle()
	elif sys.argv[1] == "html":
		words_by_file = read_words_from_files()
	else:
		raise Exception("First argument must be \"html\" or \"pickle\".")

	names = extract_predefined_names_from_files(words_by_file) # Find the names in each article
	names = remove_incorrect_names(names) # Remove non-names according to a set of criteria
	names = remove_one_article_predefined_names(names) # Remove names that only occur in one article
	(nodes, edges, edge_weights) = create_graph(names) # Create graph of names

	edge_list = [(edge, edge_weights[edge]) for edge in edge_weights]
	edge_list = sorted(edge_list, key=lambda x: x[1])

	export_to_csv(edge_weights) # Export graph to CSV

	print(edge_list)

if __name__ == "__main__":
	main()