import pickle
import sys
import csv
import importlib

from more_itertools import unique_everseen

from .util import parse_arguments

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

def read_words_from_files(filenames):
	file_contents = []
	arguments = parse_arguments()
	for i, filename in enumerate(filenames):
		f = open(filename)

		text = f.read()
		parser_filename = arguments.parser
		parse = importlib.import_module("src.parsers." + parser_filename).parse

		try:
			text = parse(text, verbose=arguments.verbose)
			file_contents.append(text)
		except Exception as e:
			if arguments.verbose:
				print("File " + str(i) + ": FAILURE!")
			continue

	file_contents = [' '.join(f.split()) for f in file_contents]
	words_by_file = [f.split(' ') for f in file_contents]

	return words_by_file

def read_words_from_pickle(filename):
	with open(filename, 'rb') as f:
		words_by_file = pickle.load(f)
		return words_by_file