#!/usr/bin/env python3

import string
import pickle
import sys
import csv

import networkx as nx
#import matplotlib.pyplot as mpl

from collections import defaultdict
from bs4 import BeautifulSoup
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

					if w+1 >= len(words):
						break
					nextWord = strip_word(words[w+i])

			full_name = " ".join(full_name)
			names[full_name].append(w)
		already_added_indexes = already_added_indexes[-10:]

	return names

def create_graph(words):
	nodes = set()
	edges = set()
	edge_weights = defaultdict(lambda: 0)
	for i in words:
		for j in words:
			if i == j:
				continue
			for loc_i in words[i]:
				for loc_j in words[j]:
					if abs(loc_i - loc_j) < 30:
						edge_set = frozenset([str(i), str(j)])
						edges.add(edge_set)
						edge_weights[edge_set] = edge_weights[edge_set] + 1
						nodes.add(i)
						nodes.add(j)
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
			if not row[0].isalpha():
				continue

			words.append(row[0])
	return words

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

	text = ' '.join(file_contents)
	text = ' '.join(text.split())
	words = text.split(' ')

	with open('data.pickle', 'wb') as f:
		pickle.dump(words, f, pickle.HIGHEST_PROTOCOL)

	return words

def read_words_from_pickle():
	with open('data.pickle', 'rb') as f:
		words = pickle.load(f)
		return words

def plot_graph(edge_weights):
	G = nx.Graph()
	for edge in edge_weights:
		left = list(edge)[0]
		right = list(edge)[1]
		weight = edge_weights[edge]

		G.add_edge(left, right, weight=weight)
	
	G = nx.convert_node_labels_to_integers(G)
	nx.draw(G, 'graph.png', format='png', prog='neato')

def main():
	words = []
	if sys.argv[1] == "pickle":
		words = read_words_from_pickle();
	elif sys.argv[1] == "html":
		words = read_words_from_files()
	else:
		raise Exception("First argument must be \"html\" or \"pickle\".")

	names = extract_names(words)
	(nodes, edges, edge_weights) = create_graph(names)
	plot_graph(edge_weights)

	edge_list = [(edge, edge_weights[edge]) for edge in edge_weights]
	edge_list = sorted(edge_list, key=lambda x: x[1])

	print(edge_list)

if __name__ == "__main__":
	main()