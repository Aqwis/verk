import string
import networkx as nx

from collections import defaultdict
from input import import_predefined_names
from util import parse_arguments

def extract_names(words_by_file):
	names = extract_predefined_names_from_files(words_by_file) # Find the names in each article
	names = remove_incorrect_names(names) # Remove non-names according to a set of criteria
	return remove_one_article_predefined_names(names) # Remove names that only occur in one article

def extract_predefined_names_from_files(words_by_file):
	names_by_file = []
	for f in words_by_file:
		names_by_file.append(extract_predefined_names(f))
	return names_by_file

def extract_predefined_names(words):
	names = defaultdict(list)
	text = ' '.join(words)

	predefined_names = import_predefined_names('names.csv')

	for name in predefined_names:
		if name in text:
			names[name].append(1)

	return names

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
	arguments = parse_arguments()
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

	if arguments.verbose:
		print("Deleted " + str(deleted) + " names")

	return names_by_file

# def extract_names_from_files(words_by_file):
# 	names_by_file = []
# 	for f in words_by_file:
# 		names_by_file.append(extract_names_from_file(f))
# 	return names_by_file

# def extract_names_from_file(words):
# 	names = defaultdict(list)
# 	already_added_indexes = []

# 	first_names = import_first_names('fornavn.csv')
# 	forbidden_words = import_forbidden_words('forbidden_words.csv')

# 	for w in range(len(words)):
# 		word = strip_word(words[w])

# 		if not is_word_potential_name(word):
# 			continue

# 		if w in already_added_indexes:
# 			continue

# 		if word in first_names:
# 			full_name = [word]
# 			already_added_indexes.append(w)

# 			i = 1

# 			if w+1 < len(words):
# 				nextWord = strip_word(words[w+i])
# 				while is_word_potential_name(nextWord):
# 					notPartOfName = False
# 					for punctuation in string.punctuation:
# 						if punctuation in words[w+i-1]:
# 							notPartOfName = True
# 							break
# 					if notPartOfName:
# 						break

# 					if nextWord in forbidden_words:
# 						break

# 					full_name.append(nextWord)
# 					already_added_indexes.append(w+i)

# 					i = i + 1

# 					if w+i >= len(words):
# 						break
# 					nextWord = strip_word(words[w+i])

# 			full_name = " ".join(full_name)
# 			names[full_name].append(w)
# 		already_added_indexes = already_added_indexes[-10:]

# 	return names