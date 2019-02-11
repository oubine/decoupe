import re
import json
import nltk
from pprint import pprint
from nltk.corpus import treebank
from nltk.book import FreqDist
PUNCT_or_NUMBER=re.compile(r'[.!?,;:\'\-\s\n\r_()\[\]«» 0-9]')

def squeeze(word):
    return re.sub(PUNCT_or_NUMBER, ' ', word)

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
    word=squeeze(word)
    word=word.lower()
    if ' ' in  word:
        word=word.split()
        tokens1+=word
    else:
        tokens1.append(word)


tokens1=sorted(tokens1)

def lexical_diversity(text):
    return len(set(text)) / len(text)

def percentage(word, tokens):
    return 100 * (tokens.count(word) / len(tokens))


fdist=FreqDist(tokens1)
tokens1=fdist.most_common(len(tokens1))

print(fdist.most_common(10))


print('le mot %s est présent à ' % 'comme', percentage('comme',tokens), '% dans le texte')
print('la diversité lexicale du texte est de ', lexical_diversity(tokens), '%')



from pylab import *

x = array([1, 3, 4, 6])
y = array([2, 3, 5, 1])
plot(x, y)

show()


with open('stockage1.json','w') as fd:
    json.dump(tokens1, fd, indent=2, ensure_ascii=False )


