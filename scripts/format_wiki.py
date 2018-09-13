#!/usr/bin/env python3

"""Takes a dump of the 1st sentences of Wikipedia pages; then random-picks a set
no. of nonce :: context pairs therefrom, purges invalid entries, and formats
them so that they can be parsed by vectorize.py.
"""

import random, spacy
from conf import Corpora
from lib import getline_inf, sanitize

## PREPARE SOURCE CORPUS ##

with open(Corpora.inf.srcdir + 'wiki_src.txt', 'r') as src:
	src = src.readlines() #store lines in list
	src = [sanitize(line.lower()) for line in src] #sanitize and lowercase

## FILTER OUT INVALID ENTRIES ##

#lambda: lines coming from disambiguation wiki pages
disamb = lambda x : 'may refer to'   in x or 'may stand for'   in x \
	         or 'can refer to'   in x or 'can stand for'   in x \
	         or 'might refer to' in x or 'might stand for' in x \
	         or 'also refer to'  in x or 'also stand for'  in x

#lambda: empty lines (nonce without definition)
empty = lambda x : len(x) <= 1 or '::' in x[-5:]

#filter out
src = [line for line in src if not (disamb(line) or empty(line))]

## RANDOM-PICK LINES THEN OUTPUT ##

#prepare vars
srcrange = range(len(src)) #no. of lines in Wiki
outrange = range(Corpora.size) #no. of desired lines in output
nums   = []
lines  = []

#parse src corpus, get already-paired lines and nonces
for i in outrange:
	n, line = getline_inf(srcrange, src, nums)
	nums.append(n)
	lines.append(line)

#output to file
with open(Corpora.inf.maxi, 'w') as f:
	for line in lines:
		f.write(line)
