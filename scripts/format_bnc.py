#!/usr/bin/env python3

"""Takes sliced & tarballed BNC and merges it into one file; then random-picks
a set no. of lines therefrom, couples them with random-picked nonces, and format
them so that they can be parsed by vectorize.py.
"""

import os, random, re, tarfile, spacy
from shutil import rmtree
from conf import Corpora
from lib import getcontext_gen, sanitize

## UNPACK BNC & ASSEMBLE IT IN ONE TXT FILE ##

#directories
corpusdir = Corpora.gen.srcdir
tmp       = corpusdir + 'tmp/'

#unpack tarballs in temp subfolder
tarballs = [corpusdir + f for f in os.listdir(corpusdir) if f[-7:] == '.tar.gz']
for t in tarballs:
	with tarfile.open(t, 'r:gz') as t:
		t.extractall(path = tmp)

#list relevant txt files
reg = re.compile('^[A-Z]$')
corpusfiles = [tmp + f for f in os.listdir(tmp) if reg.match(f)]

#store all sentences in one list (already sanitized and lowercased)
corpus = []
for f in corpusfiles:
	with open(f, 'r') as f:
		for line in f.readlines():
			corpus.append(sanitize(line.lower()))

#delete temp subdir
rmtree(tmp)

## RANDOM-PICK LINES AND NONCES ##

#prepare vars
srcrange = range(len(corpus)) #no. of lines in BNC
outrange = range(Corpora.size) #no. of desired lines in output
nums   = []
nonces = []
out    = []

#load pos-tagger (to avoid selecting punctuation as nonces)
nlp = spacy.load('en')

#parse src corpus, get context and nonces
for i in outrange:
	n, context, nonce = getcontext_gen(srcrange, corpus, nums, nonces, nlp)
	nums.append(n)
	nonces.append(nonce)
	out.append(nonce + ' :: ' + context)

#output 'nonce :: sentence' to file
with open(Corpora.gen.maxi, 'w') as f:
	for line in out:
		f.write(line)
