from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string

stop_words = set(stopwords.words('english'))

def lemmatize(word):
	return WordNetLemmatizer().lemmatize(word)

def normalize(word):
	return lemmatize(word.translate(str.maketrans('', '', string.punctuation)).lower())

def word_filter(word):
	return word not in stop_words and word.isalpha()

def process_text(gloss):
	words = gloss.split(" ") # find better way to tokenize
	words = [normalize(word) for word in words]
	words = [word for word in filter(word_filter, words)]
	return words

def process_tokens(words):
	words = [normalize(word) for word in words]
	words = [word for word in filter(word_filter, words)]
	return words