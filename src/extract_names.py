import regex as re
import sys

from collections import defaultdict

def extract_predefined_names(words):
	# Alternative but currently unused function that extracts names from
	# a list of words according to a predefined list of (full) names.
	names = defaultdict(list)
	text = ' '.join(words)
	arguments = parse_arguments()

	predefined_names = import_predefined_names(arguments.names)

	for name in predefined_names:
		if name in text:
			names[name].append(1)

	return names

def remove_spaces(string):
    return re.sub(r"[ ]+", "", string)

def sentence_tokenizer(text):
	sentences = text.split('.')
	new_sentences = [sentences[0],]
	# Handle the case where one sentence gets split because of the period
	# in names such as "Richard M. Nixon".
	for i in range(1, len(sentences)):
		if len(sentences[i-1]) >= 2 and sentences[i-1][-1].isupper() and sentences[i-1][-2] == " ":
			new_sentences[-1] = new_sentences[-1] + " " + sentences[i]
		else:
			new_sentences.append(sentences[i])
	return new_sentences

def tokenizer(text):
	sentences = sentence_tokenizer(text)
	tokens_by_sentence = {}
	for s, sentence in enumerate(sentences):
		tokens = re.split("([ \p{P}])", sentence)
		tokens = [remove_spaces(t) for t in tokens]
		tokens = [tok for tok in tokens if len(tok) > 0]
		tokens_by_sentence[s] = tokens
	return (sentences, tokens_by_sentence)

def find_first_names_in_sentence(sentence_tokens, first_names):
	found_first_names = []
	for t, token in enumerate(sentence_tokens):
		if not token[0].isupper():
			continue
		if token in first_names:
			found_first_names.append((token, t,))
	return found_first_names

def find_full_names(first_names_by_sentence, tokens_by_sentence, first_names):
	full_names = []
	for s, _ in enumerate(tokens_by_sentence):
		names_in_sentence = first_names_by_sentence[s]
		tokens = tokens_by_sentence[s]

		# We go back and ahead from the found first name and record every capitalized word we find
		# until we find a non-capitalized word. We then join these words together to (hopefully)
		# end up with a full name.
		for token, t in names_in_sentence:
			capitalized_words_before = []
			capitalized_words_after = []
			if t != 0:
				for b in range(t-1, -1, -1):
					previous_word = tokens[b]
					# Names that occur between the first name must be found in the list
					# of first names as well. We also avoid including words in ONLY CAPITAL LETTERS.
					if previous_word[0].isupper() and previous_word in first_names and not previous_word.isupper():
						capitalized_words_before.insert(0, previous_word)
					else:
						break
			if t != len(tokens)-1:
				for a in range(t+1, len(tokens)):
					next_word = tokens[a]
					if next_word[0].isupper() and not next_word.isupper():
						capitalized_words_after.append(next_word)
					else:
						break
			full_names.append(capitalized_words_before + [token] + capitalized_words_after)
	return full_names

def extract_names(text, first_names):
	(sentences, tokens_by_sentence) = tokenizer(text)

	first_names_by_sentence = defaultdict(list)
	for s, sentence in enumerate(sentences):
		first_names_by_sentence[s] = find_first_names_in_sentence(tokens_by_sentence[s], first_names)

	full_names = find_full_names(first_names_by_sentence, tokens_by_sentence, first_names)
	return set([" ".join(name) for name in full_names if len(name) > 1])

if __name__ == "__main__":
	firstname_file = sys.argv[1]
	textfile = sys.argv[2]

	text = ""
	with open(textfile, 'r') as f:
		text = f.read().replace('\n', '')

	first_names = import_first_names(firstname_file)
	full_names = extract_names(text, first_names)
	print(full_names)