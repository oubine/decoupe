import re
import json
import nltk
from pprint import pprint
from nltk.corpus import treebank
DEUX_MOTS=re.compile(r'[a-zA-Z]+[\-\'][a-zA-Z]+')
PUNCT_or_NUMBER=re.compile(r'^[.,;:\-!_?()«» 0-9]+|[.,\-;:«»!_() ?0-9]+$')
VIDE=re.compile(r'^[ \r\n\s]+|[ \r\n\s]+$')
with open('stockage.json', 'r') as f:
    book=json.load(f)

tokens = []

for part, value in book.items():
    if isinstance(value,list):
        for chapter in value:
            tokens+=nltk.word_tokenize(chapter['title'])
            if 'poems' in chapter:
                for poem in chapter['poems']:
                    tokens+=nltk.word_tokenize(poem['title'])+nltk.word_tokenize(poem['content'])
            else:
                tokens+=nltk.word_tokenize(chapter['poem'])
    else:
       tokens+=nltk.word_tokenize(value)

tokens1= []

for word in tokens:
    word=re.sub(VIDE, ' ', word)
    if bool((PUNCT_or_NUMBER.search(word))):
        word=re.sub(PUNCT_or_NUMBER, '', word )
        if word == '':
            word=None
    elif bool(DEUX_MOTS.search(word)):
        word=re.sub(DEUX_MOTS, ' ', word )
        tokens+=nltk.word_tokenize(word)
        continue
    if word:
        tokens1.append(word)

print(tokens1)


with open('stockage1.json','w') as fd:
    json.dump(tokens1, fd, indent=2, ensure_ascii=False )


