#!/usr/bin/env python3

import string
import sys
import csv

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
	names = []
	already_added_indexes = []

	first_names = import_first_names('fornavn.csv')
	forbidden_words = import_forbidden_words('forbidden_words.csv')

	for w in range(len(words)):
		word = strip_word(words[w])

		if not is_word_potential_name(word):
			continue

		if word in first_names:
			full_name = [word]
			already_added_indexes.append(word)

			i = 1
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
				already_added_indexes.append(nextWord)

				i = i + 1
				nextWord = strip_word(words[w+i])

			names.append(" ".join(full_name))

	return names

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

def main():
	file_contents = []
	for filename in sys.argv[1:]:
		f = open(filename)
		html = f.read()

		soup = BeautifulSoup(html, 'html.parser')
		contents_list = soup.find_all("section", class_='article')

		if len(contents_list) > 1:
		    raise Exception()

		contents = contents_list[0]
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

	names = extract_names(words)

	print(Counter(names))

if __name__ == "__main__":
	main()