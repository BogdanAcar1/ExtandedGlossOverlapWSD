from nltk.corpus import wordnet as wn
from ego import *
from process import *
from tests import tests
from nltk.corpus import senseval
import wikipedia as wp

def print_wn_sense(word):
	print(f"Wordnet defintions of {word}:")
	print("-" * 50)
	for s in wn.synsets(word):
		print(s.definition())
		print("-" * 50)

def test_sense(word):
	print_wn_sense(word)

	target = word
	for test in tests[target]:
		print(test, f"-> sense of {target}: ",  get_sense2(target, test))

def get_senseval_contexts(word, n = 10):
	contexts = []
	for instance in senseval.instances(f'{word}.pos')[:n]:
		try:
			contexts.append(([word for (word, pos) in instance.context], instance.senses))
		except:
			pass
	return contexts

if __name__ == '__main__':
	test_sense("fly")
	# target = "row"
	# print_wn_sense(target)
	# contexts = ["Cristi deleted a row in the matching table",
	# 			"The rowers row to keep the ship at constant speed"]
	# for context in contexts:
	# 	print(get_sense(target, process_text(context)))
