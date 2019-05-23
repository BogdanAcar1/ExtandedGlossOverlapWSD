from nltk.corpus import wordnet as wn
from ego import *
from process import *
from tests import tests
from nltk.corpus import senseval
from corpus import *
import sense_mapping as sm

def test_wsd(target, start = 1000, n = 4000):
	correct, all = 0, 0
	corpus = get_test_corpus(target, start = start, n = n)
	for context, act_sense in corpus:
		pred_synset = get_sense_tagged(target, context)
		pred_sense = sm.map_synset_to_sense(target, pred_synset)
		print(pred_sense, act_sense)
		if act_sense == pred_sense:
			correct += 1
		all += 1
		print(correct / all)
	return correct / all

if __name__ == '__main__':
	#print(test_wsd("hard", start = 0, n = 10))
	target = "line"
	for text in tests[target]:
		print(text)
		print(get_sense_from_text(target, text))
