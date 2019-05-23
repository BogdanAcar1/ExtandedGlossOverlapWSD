from nltk.corpus import senseval as se
from nltk.corpus import wordnet as wn
from process import *



def get_test_corpus(target, tagged = False, process = True, start = 0, n = 5000):
    """
    Returns a list of pairs containing a tokenized context of the target word
    and its sense in that specific context. The list is taken form the line-hard-serve
    corpus
    """
    s = []
    if target not in ["line", "hard", "serve", "interest"]:
        raise Exception(f"Target '{target}' not in hard-line-serve corpus.")
    if tagged == True:
        corpus = [(ins.context, ins.senses[0]) for ins in se.instances(f"{target}.pos")]
    else:
        corpus = []
        for ins in se.instances(f"{target}.pos"):
            print(ins)
            context = [w[0] for w in ins.context]
            if process == True:
                context = process_tokens(context)
            corpus.append((context, ins.senses[0]))
            if len(corpus) - start == n:
               break
    return corpus[start :]

def test1():
    words = ["line", "hard", "serve"]
    senses = {}
    word = "serve"
    for ins in se.instances(f"{word}.pos"):
        print(' '.join(w[0] for w in ins.context))
        for sense in ins.senses:
            if sense not in senses:
                senses[sense] = 1
            else:
                senses[sense] += 1
    print(senses)

def test2():
    for sense in line_sense_mapping.keys():
        print(sense)
        for id in line_sense_mapping[sense]:
            print(wn._synset_from_pos_and_offset('n', id))
        print("=" * 100)

def test3():
    for id in line_sense_mapping.values():
        try:
            print(wn._synset_from_pos_and_offset('n', id))
        except:
            print("error")

def test4():
    word = "line"
    for ss in wn.synsets(word, pos = wn.NOUN):
        for ls in line_sense_mapping.keys():
            for id in line_sense_mapping[ls]:
                if str(id).find(str(ss._offset)) > -1:
                    print(ss._offset, ls, line_sense_mapping[ls])

if __name__ == '__main__':
    for s in wn.synsets("serve"):
        print(s, s._offset)
