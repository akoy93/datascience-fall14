import nltk
import re

IN = re.compile(r'.*\bin\b(?!\b.+ing)')
AT = re.compile(r'.*\bat\b(?!\b.+ing)')
WITH = re.compile(r'.*\bwith\b(?!\b.+ing)')
ON = re.compile(r'.*\bon\b(?!\b.+ing)')

for doc in nltk.corpus.ieer.parsed_docs('NYT_19980315'):
    for rel in nltk.sem.extract_rels('PER', 'ORG', doc, corpus='ieer', pattern = IN):
        print(nltk.sem.rtuple(rel))

for doc in nltk.corpus.ieer.parsed_docs('NYT_19980315'):
    for rel in nltk.sem.extract_rels('PER', 'ORG', doc, corpus='ieer', pattern = AT):
        print(nltk.sem.rtuple(rel))

for doc in nltk.corpus.ieer.parsed_docs('NYT_19980315'):
    for rel in nltk.sem.extract_rels('PER', 'ORG', doc, corpus='ieer', pattern = WITH):
        print(nltk.sem.rtuple(rel))

for doc in nltk.corpus.ieer.parsed_docs('NYT_19980315'):
    for rel in nltk.sem.extract_rels('PER', 'ORG', doc, corpus='ieer', pattern = ON):
        print(nltk.sem.rtuple(rel))