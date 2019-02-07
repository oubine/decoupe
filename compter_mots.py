import re
import json
import nltk
from pprint import pprint
from nltk.corpus import treebank
PUNCT_or_NUMBER=re.compile(r'\s*["<>!:;,.?_0-9]\s*') #pb regex ici
with open('stockage.json', 'r') as f:
    book=json.load(f)


tokens = []

for key, value in book.items():
    if 'preface' in key:
        tokens += nltk.word_tokenize(value)

print(tokens)
'''
for i,word in enumerate(tokens):
    if '.' in word or ',' in word:
        tokens.remove(tokens[i])
'''

