from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet as wn

stop_words = set(stopwords.words('english'))

def tagger_to_wn_pos(pos):
	if pos.find('VB') > -1:
		return wn.VERB
	if pos.find('NN') > -1:
		return wn.NOUN
	if pos.find('JJ') > -1:
		return wn.ADJ
	if pos.find('RB'):
		return wn.ADV
	return None

def lemmatize(word, pos = None):
	if pos is None:
		return WordNetLemmatizer().lemmatize(word)
	return WordNetLemmatizer().lemmatize(word, pos)

def normalize(word):
	return lemmatize(word.lower())

def word_filter(word):
	return word not in stop_words and word.isalpha()

def process_text(gloss):
	words = gloss.split() # find better way to tokenize
	words = [normalize(word.translate(str.maketrans('', '', string.punctuation))) for word in words]
	words = [word for word in filter(word_filter, words)]
	return words

def process_tokens(words):
	words = [word for word in filter(word_filter, words)]
	words = [normalize(word) for word in words]
	return words

def process_tagged_tokens(tagged_tokens):
	tagged_tokens = [t for t in tagged_tokens if type(t) is tuple]
	tagged_tokens = [(word, pos) for (word, pos) in tagged_tokens if word_filter(word)]
	tagged_tokens = [(lemmatize(word, tagger_to_wn_pos(pos)), pos) for (word, pos) in tagged_tokens]
	return tagged_tokens

if __name__ == '__main__':
	print(lemmatize("harder", wn.ADJ))
	print(lemmatize("hard", wn.ADJ))
