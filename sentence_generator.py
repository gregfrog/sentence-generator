import argparse
import random
import operator
import os
import shlex
import pandas as pd 

lastpcn = 3000000

csv = pd.read_csv("usstates.csv")
states = sorted(csv["stusps"])

def randomstate():
	rndst  = random.sample(states,1)[0]
	return rndst

def digit():
	digitList = [str(x) for x in list(range(10))]
	return random.choice(digitList)

def pcnsequence():
	global lastpcn
	lastpcn = lastpcn + 1
	return str(lastpcn)


def parse_grammar(file_path):
	"""
	Generate a grammar from a file describing the production rules.
	Note that the symbols are inferred from the production rules.

	For more information on the format of the file, please reffer to
	the README.md or the the sample grammars provided in this repository.

	:param file_path: Path to the file containing the description of the grammar.
	:returns: the grammar object and the starting symbol.
	"""
	with open(file_path) as f:
		content = f.read().splitlines()

	if len(content) <= 1:
		raise Exception('Grammar should have at least one production rule and a starting symbol')

	# strip comments
	content = [textLine for textLine in content if len(textLine) > 0 and textLine[0] != "#"]

	# First line should be the starting symbol
	start_symbol = content[0]

	grammar = {}
	for line in content[1:]:
		# Each line should be in the format:
		# X -> A B ... C
#		symbols = line.split()
		symbols = shlex.split(line)
		if len(symbols) <= 2 or symbols[1] != '->':
			raise Exception(f'Each production line should be in the format: X -> A B ... C, read "{line}"')

		symbols = [globals()[s[:-2]] if s[-2:] == "()" else s for s in symbols]
		symbols = [s[1:-1] if isinstance(s,str) and len(s) > 0 and s[0] == "'" and s[-1] == "'" else s for s in symbols]
		if symbols[0] not in grammar:
			grammar[symbols[0]] = []

		grammar[symbols[0]].append(symbols[2:])

	if start_symbol not in grammar:
		raise Exception('Grammar should have at leats one production rule with the start_symbol.')

	return grammar, start_symbol


def find_terminals(grammar):
	"""
	For a given grammar, return a set of the terminal symbols.

	:param grammar: The grammar (set of productions rules).
	:return: set of terminal symbols.
	"""
	terminals = set()
	for key, val in grammar.items():
		for word_list in val:
			for word in word_list:
				if word not in grammar:
					terminals.add(word)
	return terminals

def analyze_stats(sentences):
	"""
	For a given set of sentences, print how many times each symbol appears,
	printing statistics sorted by occurrance.

	:param sentences: List of sentences.
	"""
	counts = {}
	for sentence in sentences:
		for element in sentence.split():
			if element not in counts:
				counts[element] = 1
			else:
				counts[element] += 1

	# print stats
	sorted_counts = sorted(counts.items(), key = operator.itemgetter(1))
	for key, val in sorted_counts:
		print("%5d %s" % (val, key))

def generate_random_sentence(grammar, start_symbol, print_sentence = True):
	"""
	For a given grammar (set of production rules) and a starting symbol,
	randomly generate a sentence using the production rules.

	:param sentences: The grammar (set of productions rules).
	:param start_symbol: The starting symbol.
	:param print_sentence: Wether to print the generated sentence. Defaults to true.
	:returns: A randomly generated sentence.
	"""
	# Starting symbol must be a part of the grammar
	assert start_symbol in grammar
	
	sentence = [start_symbol]
	idx = 0
	while idx < len(sentence):
		if sentence[idx] in terminals:
			idx += 1
		else:
			choices = grammar[sentence[idx]]
			choice = random.choice(choices)
			sentence = sentence[:idx] + choice + sentence[idx+1:]
	sentence = "".join(
		[word if isinstance(word, str) else word() for word  in sentence])
	if print_sentence:
		print(sentence)
	return sentence

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Grammar utils')
	parser.add_argument('--grammar', type=str, default='simple_grammar.txt',
					  help='Path to grammar file.')
	parser.add_argument('--print_terminal_symbols', type=bool, const=True, nargs='?',
					  help='Print the terminal symbols of the grammar.')
	parser.add_argument('--numbered_output', type=bool, const=True, nargs='?',
					  help='Print the terminal symbols of the grammar.')
	parser.add_argument('--num_sentences', type=int, default=1,
					  help='The number of random sentences to generate.')
	

	args = parser.parse_args()

	grammar, start_symbol = parse_grammar(args.grammar)

	terminals = find_terminals(grammar)
	
	if args.print_terminal_symbols == True:
		stringTerminals = [ str(x) for x in list(terminals)]
		for terminal in sorted(stringTerminals):
			if terminal == '':
				terminal = "''"
			print(terminal)
		print('-----------------')
		print('There are', len(terminals), 'terminals')

	sentences = []
	for i in range(args.num_sentences):
		sentences.append(generate_random_sentence(grammar, start_symbol, False))

	for i in range(len(sentences)):
		if args.numbered_output == True:
			print("%d. %s" % (i, sentences[i]))
		else:
			print("%s" % (sentences[i]))
			