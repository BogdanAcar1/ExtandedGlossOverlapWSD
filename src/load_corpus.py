from os import listdir
from os.path import isfile, join
import re

LINE_CORPUS_PATH = "original-line/"

def load_line_corpus():
    corpus = {}
    for file in listdir(LINE_CORPUS_PATH):
        file_path = join(LINE_CORPUS_PATH, file)
        if isfile(file_path):
            with open(file_path, "r") as sense_in:
                corpus[file[:-1]] = []
                for line in sense_in.readlines():
                    #corpus[file[:-1]].extend([line for line in sense_in.readlines()])
                    
    print(corpus["cord"])
    print("*"*100)
    print(corpus["text"])

if __name__ == '__main__':
    load_line_corpus()
