from collections import defaultdict

from .input import import_first_names
from .util import parse_arguments
from .extract_names import extract_names

arguments = parse_arguments()

def extract_names_from_articles(articles):
	first_names = import_first_names(arguments.names)
	names_by_article = []
	for f in articles:
		names_by_article.append(extract_names(f, first_names))
	return remove_unique_names(names_by_article) # Remove names that only occur in one article

def remove_unique_names(names_by_article):
	occurrences = defaultdict(lambda: 0)

	for f in names_by_article:
		for name in f:
			occurrences[name] += 1

	names_by_article = [[name for name in article_names if occurrences[name] >= 2] for article_names in names_by_article]
	return names_by_article