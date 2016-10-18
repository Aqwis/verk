import pickle
import sys
import csv

from bs4 import BeautifulSoup
from more_itertools import unique_everseen

from util import parse_arguments

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
	for filename in filenames:
		f = open(filename)
		html = f.read()

		soup = BeautifulSoup(html, 'html.parser')
		contents_list = soup.find_all("section", class_='article')

		if len(contents_list) > 1:
		    raise Exception()

		try:
			contents = contents_list[0]
		except:
			if arguments.verbose:
				print("FAILURE!")
			continue
		try:
		    contents.find(class_='factboxcontainer').decompose()
		except:
		    pass
		lines = list([s.replace('\n', ' ') for s in contents.stripped_strings])
		text = " ".join(lines)

		file_contents.append(text)

		if arguments.verbose:
			print("Success!")

	file_contents = [' '.join(f.split()) for f in file_contents]
	words_by_file = [f.split(' ') for f in file_contents]

	return words_by_file

def read_words_from_pickle(filename):
	with open(filename, 'rb') as f:
		words_by_file = pickle.load(f)
		return words_by_file