from nltk.corpus import wordnet as wn
from nltk.tag import StanfordPOSTagger
from ego import *
from process import *
from tests import tests
from nltk.corpus import senseval

postagger = StanfordPOSTagger("stanford-postagger-2018-10-16/models/english-bidirectional-distsim.tagger",
							  "stanford-postagger-2018-10-16/stanford-postagger-3.9.2.jar" )

def print_wn_sense(word):
	print(f"Wordnet defintions of {word}:")
	print("-" * 50)
	for s in wn.synsets(word):
		print(s.definition())
		print("-" * 50)

def test_sense(word):
	print_wn_sense("card")

	target = "card"
	for test in tests[target]:
		print(test, f"-> sense of {target}: ",  get_sense(target, process_gloss(test)))

def get_senseval_contexts(word, n = 10):
	contexts = []
	for instance in senseval.instances(f'{word}.pos')[:n]:			
		try:
			contexts.append(([word for (word, pos) in instance.context], instance.senses))
		except:
			pass
	return contexts

if __name__ == '__main__':
	target = "line"
	for context, senses in get_senseval_contexts(target, 10):
		print("context: ", " ".join(context))
		print("predicted sense: ", get_sense(target, context))
		print("true sense: ", senses)
		print("-" * 50)