import nltk
import codecs

files = ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt', '6.txt', '7.txt', '8.txt', '9.txt', '10.txt']
directory = 'articles'

def scan_tree(tree):
  for n in tree:
    if type(n) is nltk.Tree:
      entity = [t[0] for t in n]
      print ' '.join(entity) + ', ' + n._label

for filename in files:
  print 'File: ' + filename + ' ==============================================='
  with codecs.open(directory + '/' + filename, 'r', encoding='utf-8') as f:
    data = f.read()
  sentences = nltk.sent_tokenize(data)
  sentences = [nltk.word_tokenize(sent) for sent in sentences]
  sentences = [nltk.pos_tag(sent) for sent in sentences]
  for s in sentences:
    scan_tree(nltk.ne_chunk(s))
  print
