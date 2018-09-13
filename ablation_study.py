#!/usr/bin/env python3

"""Performs an ablation study."""

import os, pickle
from conf import Vectors

## EDIT OUT DIMENSIONS ##
srcfiles = [Vectors('gen/'), Vectors('inf/')]
for obj in srcfiles:
	#load 50-dim pickles
	with open(obj.wordvec, 'rb') as w:
		wordvec = pickle.load(w)
	with open(obj.posvec, 'rb') as p:
		posvec = pickle.load(p)

	#remove dimensions
	for i in range(50):
		out = {}
		for vec in [wordvec, posvec]:
			for k, v in vec.items():
				out[k] = v[:i] + v[i+1:]

			#construct output filename
			outname = obj.wordvec if vec == wordvec \
				else obj.posvec
			outname = outname.split('.')
			outname = f'{outname[0]}_{i}.{outname[1]}'

			#dump 49-dim pickle
			with open(outname, 'wb') as outfile:
				pickle.dump(out, outfile)

	## RUN CLASSIFIER ##

#	for i in range(50):
#		os.system(f'python3 -u scripts/classify.py {i} >> ' \
#			f'{Vectors.vecdir}_ABLST_out.txt')
