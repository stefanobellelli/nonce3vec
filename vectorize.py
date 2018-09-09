#!/usr/bin/env python3

"""Takes formatted corpora and creates vector spaces (saved as pickles in a
subdir). Dumps a lot of logfiles (in a separate subdir) in the process.
"""

import sys, json, pickle, numpy as np
from conf import Corpora, Vectors
from lib import newdirs, postag, dictize, vecindex, vectorize, unifiedindex

## INITIAL SETTINGS ##
#c: access conf settings and populate with new attrs
class Topic:
	def __init__(self, fname, name):
		self.fname  = fname
		self.subdir = name + '/'
		self.vec    = Vectors(self.subdir)

gen = Topic(Corpora.gen.formatted, Corpora.gen.kind)
inf = Topic(Corpora.inf.formatted, Corpora.inf.kind)
corpora = [gen, inf]

#wcreate dirs for dumps (logs and bins)
for c in corpora:
	newdirs(c.vec.logs.dir, c.vec.dir)

## POS-TAG & COUNT N-GRAMS ##
for c in corpora:
	#pos-tag source file
	with open(c.fname, 'r') as src:
		tag_dict, log = postag(src)
	#dump log
	with open(c.vec.logs.postag, 'w') as lf:
		lf.write(log)

	#create dictionary of n-grams
	c.ngrdict, log = dictize(tag_dict, Vectors.ngrsize, Vectors.exclude)
	#dump log
	with open(c.vec.logs.dic, 'w') as lf:
		lf.write(log)

## CREATE UNIFIED INDEXES OF ALL WORD/POS N-GRAMS ##
wordindex, posindex, udict_log, uindex_log = \
	unifiedindex(Vectors.vecsize, gen.ngrdict, inf.ngrdict)
#dump logs (word & pos are in the same file)
with open(gen.vec.logs.udict, 'w') as dl, open(gen.vec.logs.uindex, 'w') as il:
	dl.write(udict_log)  #unified dict
	il.write(uindex_log) #unified index

## CREATE DICTS OF N-GRAM VECTORS ##
#(nonce:n-gram-vec), word and pos are separated
for c in corpora:
	#words
	c.wordvec, log = vectorize(c.ngrdict, wordindex, 'word')
	with open(c.vec.logs.wordvec, 'w') as l, open(c.vec.wordvec, 'wb') as b:
		l.write(log) #log
		pickle.dump(c.wordvec, b) #bin

	#pos
	c.posvec, log  = vectorize(c.ngrdict, posindex,  'pos')
	with open(c.vec.logs.posvec, 'w') as l, open(c.vec.posvec, 'wb') as b:
		l.write(log) #log
		pickle.dump(c.posvec, b) #bin
