import json

import re
from pprint import pprint
ROMAN_NUMBER=re.compile(r'^[\r\n\sIVX]+$')
NOT_ROMAN_NUMBER=re.compile(r'[^\r\n\sIVX]')
DEDICACE=re.compile(r'^\s*A\s+(?!UNE)|[A-Z]\.')

def is_next_line_title(lines, line, i):
    while is_useless(lines[i+1]):
        i+=1
    return is_title(lines[i+1])

def is_exception(line):
    return 'STATUE ALLÉGORIQUE DANS LE GOUT DE LA RENAISSANCE' in line or 'STATUAIRE' in line or 'LES TÉNÈBRE' in line or 'LE PARFUM' in line or 'LE CADRE' in line or 'LE PORTRAIT' in line


def is_useless(line):
    return not line.strip() or bool(DEDICACE.search(line)) or bool(ROMAN_NUMBER.search(line)) or is_exception(line)

def is_title(line):
    return line.isupper() and not bool(ROMAN_NUMBER.search(line)) and not bool(DEDICACE.search(line)) and not is_exception(line)

with open ('fleurs.txt', 'r') as f:
    lines=f.readlines()

book={
    'chapters':[]
}
state='PREFACE'
current_chapter = None
current_poem = None

preface=''
for i,line in enumerate(lines):
    line=line.strip()
    if state=='PREFACE':
        if 'AU LECTEUR' in line:
            book['preface']=preface
            state='BOOK'
        else:
            preface+=line+'\n'
    elif state=='BOOK':
        if 'End of the Project Gutenberg EBook of'in line:
            break
        if is_title(line):
            if is_next_line_title(lines, line, i):
                if current_chapter is not None:
                    book['chapters'].append(current_chapter)
                current_chapter = {'title' : line, 'poems' : [ ]}
            else:
                if current_poem is not None:
                    current_chapter['poems'].append(current_poem)
                current_poem = {'title' : line, 'content' : ''}
        else:
            if is_useless(line):
                continue
            if current_poem is not None:
                current_poem['content'] += line + '\n'

current_chapter['poems'].append(current_poem)
book['chapters'].append(current_chapter)


with open('stockage.json','w') as fd:
    json.dump(book, fd, indent=2, ensure_ascii=False )


