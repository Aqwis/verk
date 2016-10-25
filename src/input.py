import pickle
import sys
import csv
import importlib

from more_itertools import unique_everseen

from .util import parse_arguments

def import_first_names(filename):
	with open(filename, 'r') as f:
		return [a.replace('\n', '').replace('\ufeff', '') for a in f.readlines()]

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
	# Not currently used
	names = []
	with open(filename) as f:
		reader = csv.reader(f)
		for row in reader:
			if not row[0][0].isalpha():
				continue

			names.append(row[0])
	names = list(unique_everseen(names))
	return names

def read_files(filenames):
	articles = []
	arguments = parse_arguments()
	for i, filename in enumerate(filenames):
		f = open(filename)

		text = f.read()
		parser_filename = arguments.parser
		parse = importlib.import_module("src.parsers." + parser_filename).parse

		try:
			text = parse(text, verbose=arguments.verbose)
			articles.append(text)
		except Exception as e:
			if arguments.verbose:
				print("File " + str(i) + ": FAILURE!")
			continue

	return articles

def unpickle_articles(filename):
	with open(filename, 'rb') as f:
		return pickle.load(f)