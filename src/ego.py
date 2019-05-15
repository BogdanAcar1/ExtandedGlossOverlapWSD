import difflib as dl
from nltk.corpus import wordnet as wn
from nltk.corpus import senseval as se
from process import *
from nltk import word_tokenize
from nltk.tag import StanfordPOSTagger
import sense_mapping as sm
from process import tagger_to_wn_pos


postagger = StanfordPOSTagger("stanford-postagger-2018-10-16/models/english-bidirectional-distsim.tagger",
"stanford-postagger-2018-10-16/stanford-postagger-3.9.2.jar" )

HYPE = "hypernymy" #Y is a hypernym of X if every X is a (kind of) Y (canine is a hypernym of dog)
HYPO = "hyponymy"  #Y is a hyponym of X if every Y is a (kind of) X (dog is a hyponym of canine)
HOLO = "holonymy"  #Y is a holonym of X if X is a part of Y (building is a holonym of window)
MERO = "meronymy"  #Y is a meronym of X if Y is a part of X (window is a meronym of building)
GLOSS = "gloss"    #xA's gloss is A's definition
EXAMPLE = "example"

def symmetric_closure(relations):
	closure = []
	for (r1, r2) in relations:
		if (r1, r2) not in closure:
			closure.append((r1, r2))
		if (r2, r1) not in closure:
			closure.append((r2, r1))
	return closure

relpairs = [(GLOSS, GLOSS), (HYPE, HYPE), (HYPO, HYPO), (HYPE, GLOSS), (GLOSS, HYPE)]
#relpairs = symmetric_closure([(HYPO, MERO), (HYPO, HYPO), (GLOSS, MERO), (GLOSS, GLOSS), (EXAMPLE, MERO)])

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
	elif relation == EXAMPLE:
		#print(synset.examples())
		return process_text(" ".join(synset.examples()))

	return process_text(" ".join([s.definition() for s in synsets]))

def relatedness(s1, s2, relpairs):
	return sum([score(get_extended_gloss(s1, r1), get_extended_gloss(s2, r2)) for (r1, r2) in relpairs])

def get_context_window(target, tagged_context, n = 2, tagged = True):
	word_context = [word for (word, pos) in tagged_context]
	begin = max(0, word_context.index(target) - n)
	end = min(len(word_context), word_context.index(target) + n + 1)
	return tagged_context[begin : end]

def run_ego(target, tagged_context, use_test_synsets = False):
	scores = []
	target_pos = [pos for (word, pos) in tagged_context if word == target][0]
	synsets = wn.synsets(target, pos = tagger_to_wn_pos(target_pos))
	if use_test_synsets:
		synsets = [s for s in synsets if sm.map_synset_to_sense(target, s) != None]
	for target_sense in synsets:
		sk = 0
		for word, pos in tagged_context:
			if word != target:
				for word_sense in wn.synsets(word, pos = tagger_to_wn_pos(pos)):
					sk += relatedness(target_sense, word_sense, relpairs)
		scores.append(sk)
	if len(scores) > 0:
		return synsets[scores.index(max(scores))]
	return None

def get_sense(target, tagged_context):
	tagged_context = process_tagged_tokens(tagged_context)
	sense_synset = run_ego(target, get_context_window(target, tagged_context), use_test_synsets = True)
	return sense_synset

def get_sense_from_text(target, text_context):
	text_context = process_text(text_context)
	tagged_context = postagger.tag(text_context)
	print(tagged_context)
	sense = run_ego(target, tagged_context)
	return sense.definition()

def test_hard_line_serve(only_senses = None):
	targets = ["line"]#, "hard", "serve"]
	for target in targets:
		with open(f"{target}.log", "w") as log:
			all, ok = 0, 0
			for (i, it) in enumerate(se.instances(f"{target}.pos")):
				try:
					s = get_sense(target, it.context)
					p_sense = sm.map_synset_to_sense(target, s)
					a_sense = it.senses[0]
					print(f"{i}. predicted: {p_sense}, actual: {a_sense}\n")
					log.write(f"{i}. predicted: {p_sense}, actual: {a_sense}\n")
					if p_sense == a_sense:
						ok += 1
					all += 1
					if i % 100 == 0:
						print(str(ok / all) + "\n")
						log.write(str(ok / all) + "\n")
				except Exception as e:
					print(e)
					print(str(ok / all) + "\n")
					log.write(str(e))
			log.write(str(ok / all) + "\n")

if __name__ == '__main__':
	test_hard_line_serve()
