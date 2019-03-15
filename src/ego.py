import difflib as dl
from nltk.corpus import wordnet as wn
from process import *

HYPE = "hypernymy" #Y is a hypernym of X if every X is a (kind of) Y (canine is a hypernym of dog)
HYPO = "hyponymy"  #Y is a hyponym of X if every Y is a (kind of) X (dog is a hyponym of canine)
HOLO = "holonymy"  #Y is a holonym of X if X is a part of Y (building is a holonym of window)
MERO = "meronymy"  #Y is a meronym of X if Y is a part of X (window is a meronym of building)
GLOSS = "gloss"    #xA's gloss is A's definition
EXAMPLE = "example"

relpairs = [(GLOSS, GLOSS), (HYPE, HYPE), (HYPO, HYPO), (HYPE, GLOSS), (GLOSS, HYPE)]

def find_longest_overlap(s1, s2):
	sm = dl.SequenceMatcher(None, s1, s2)
	s1_begin_offset, s2_begin_offset, length = sm.find_longest_match(0, len(s1), 0, len(s2))
	return s1_begin_offset, s2_begin_offset, length

def find_overlaps(s1, s2):
	overlaps = []
	s1_begin_offset, s2_begin_offset, length = find_longest_overlap(s1, s2)
	while length != 0:
		overlaps.append(s1[s1_begin_offset : s1_begin_offset + length])
		s1 = s1[:s1_begin_offset] + s1[s1_begin_offset + length:]
		s2 = s2[:s2_begin_offset] + s2[s2_begin_offset + length:]
		s1_begin_offset, s2_begin_offset, length = find_longest_overlap(s1, s2)
	return overlaps

def score(gloss1, gloss2):
	return sum([len(overlap) ** 2 for overlap in find_overlaps(gloss1, gloss2)])

def get_extended_gloss(synset, relation):
	if relation == HYPE:
		synsets = synset.hypernyms()
	elif relation == HYPO:
		synsets = synset.hyponyms()
	elif relation == HOLO:
		synsets = synset.member_holonyms() + synset.part_holonyms() + synset.substance_holonyms()
	elif relation == MERO:
		synsets = synset.member_meronyms() + synset.part_meronyms() + synset.substance_meronyms()
	elif relation == GLOSS:
		synsets = [synset]
	#elif relation == EXAMPLE:
	#	synsets = synset.examples()

	return process_text(" ".join([s.definition() for s in synsets]))

def symmetric_closure(relations):
	closure = []
	for (r1, r2) in relations:
		if (r1, r2) not in closure:
			closure.append((r1, r2))
		if (r2, r1) not in closure:
			closure.append((r2, r1))
	return closure

def relatedness(s1, s2, relpairs):
	return sum([score(get_extended_gloss(s1, r1), get_extended_gloss(s2, r2)) for (r1, r2) in relpairs])

def get_context(target, sentence, n = 5):
	begin = max(0, sentence.index(target) - n)
	end = min(len(sentence), sentence.index(target) + n + 1)
	return sentence[begin : end]

def get_sense_scores(target, context):
	scores = []
	for target_sense in wn.synsets(target):
		sk = 0
		for word in context:
			if word != target:
				for word_sense in wn.synsets(word):
					sk += relatedness(target_sense, word_sense, relpairs)
		scores.append(sk)
	return scores

def get_sense(target, context, token_input = True):
	synsets = wn.synsets(target)
	if token_input:
		context = process_tokens(context)
	else:
		context = process_text(context)
	print("processed context: ", context)
	sense_scores = get_sense_scores(target, context)
	return synsets[sense_scores.index(max(sense_scores))].definition()